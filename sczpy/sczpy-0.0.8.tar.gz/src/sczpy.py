import os, random, struct, sys, socket
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256, SHA512
from Crypto.Protocol.KDF import PBKDF2
import requests, json, base64, jwt, datetime, hashlib
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_der_x509_certificate
from adal import AuthenticationContext
from typing import Sequence
from opentelemetry import metrics
from opentelemetry.sdk.metrics import Counter, Metric
from opentelemetry.sdk.metrics.export import (
    MetricRecord,
    MetricsExporter,
    MetricsExportResult,
)
from opentelemetry import trace
from opentelemetry.sdk.trace import Span, TracerProvider
from opentelemetry.sdk.trace.export import (
    SpanExporter, 
    SpanExportResult, 
    SimpleExportSpanProcessor,
)
import json

class SCZClient:
    def __init__(self, scz_url=None, attest_provider=None, attestation=False):
        self.__scz_url = scz_url
        self.__signature_size= hashlib.sha256().digest_size
        if self.__scz_url is None:
            self.__scz_url = os.environ['SANTA_CRUZ_URL']
        self.__attest_provider = attest_provider
        if self.__attest_provider is None and "ATTESTATION_PROVIDER" in os.environ:
            self.__attest_provider = os.environ['ATTESTATION_PROVIDER']
        if attestation:
            self.__attest()
        else: 
            self.__bootstrap()
    def __bootstrap(self):
        response = requests.get(self.__scz_url  + '/api/v1/bootstrap', verify=False)
        bootstrap = response.json()        
        kv_url = f"https://{bootstrap['kv']}.vault.azure.net"
        credential = DefaultAzureCredential()
        kvClient = SecretClient(kv_url, credential = credential)
        bootstrapKey = kvClient.get_secret(bootstrap['key']).value
        response = requests.post(self.__scz_url  + '/api/v1/login',
        json={
            "CLIENT_SECRET": bootstrapKey,
            "CLIENT_ID": "TBD"
        }, verify=False)
        self.__token = response.json()['access_token']
    def __encrypt(self, key, in_filename, out_filename=None, chunksize=64*1024):
        enc_key, mac_key = self.__create_enc_and_mac_keys(key)
        if not out_filename:
            out_filename = in_filename + '.enc'
        
        iv = os.urandom(16)
        encryptor = AES.new(enc_key, AES.MODE_CBC, iv)
        hmac = HMAC.new(mac_key, digestmod=SHA256)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.seek(self.__signature_size, 0)
                rawdata = struct.pack('<Q', filesize)
                outfile.write(rawdata)
                hmac.update(rawdata)
                outfile.write(iv)
                hmac.update(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        pad = 16 - len(chunk) % 16
                        chunk += (pad * chr(pad)).encode('ascii')
                    encdata = encryptor.encrypt(chunk)
                    outfile.write(encdata)
                    hmac.update(encdata)
                outfile.seek(0, 0)
                outfile.write(hmac.digest())

    def __decrypt(self, key, in_filename, out_filename=None, chunksize=24*1024):
        enc_key, mac_key = self.__create_enc_and_mac_keys(key)
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]
        
        with open(in_filename, 'rb') as infile:
            digest = infile.read(self.__signature_size)
            hmac = HMAC.new(mac_key, digestmod=SHA256)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                hmac.update(chunk)
            try:
                hmac.verify(digest)
            except ValueError:
                print("The encrypted data appears to be corrupt and cannot be verified.")  
                return

            infile.seek(self.__signature_size, 0)
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(enc_key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)
    def __acquirekey(self, model_id, model_version):
        headers = {"Authorization": f"Bearer {self.__token}"}
        response = requests.get(self.__scz_url + f'/api/v1/keys/{model_id}/{model_version}', headers=headers, verify=False)
        return response.text
    def __upload(self, model_id, model_version, in_file):
        headers = {"Authorization": f"Bearer {self.__token}"}
        files = {'file': open(in_file,'rb')}
        response = requests.post(self.__scz_url + f'/api/v1/models/{model_id}/{model_version}', files=files, headers=headers, verify=False) # TODO: Remove verify=False 
        return response.text   
    def __upload_data(self, model_id, model_version, in_file, attributes):
        headers = {"Authorization": f"Bearer {self.__token}"}
        files = {'file': open(in_file,'rb')}
        response = requests.post(self.__scz_url + f'/api/v1/data/{model_id}/{model_version}', files=files, headers=headers, data=attributes, verify=False) # TODO: Remove verify=False 
        return response.text   
        
    def __download(self, model_id, model_version, out_filename):
        headers = {"Authorization": f"Bearer {self.__token}"}
        response = requests.get(self.__scz_url + f'/api/v1/models/{model_id}/{model_version}', headers=headers, verify=False) # TODO: Remove verify=False 
        with open(out_filename, 'wb') as outfile:
            outfile.write(response.content)       
    def register_model(self, model_id, model_version):
        headers = {"Authorization": f"Bearer {self.__token}"}
        response = requests.post(self.__scz_url + f'/api/v1/registry/{model_id}/{model_version}', headers=headers, verify=False)
        return response.text
    def encrypt(self, model_id, model_version, in_filename, out_filename=None):
        key = self.__acquirekey(model_id, model_version)
        self.__encrypt(key, in_filename, out_filename, 64*1024)
    def decrypt(self, model_id, model_version, in_filename, out_filename=None):
        key = self.__acquirekey(model_id, model_version)
        self.__decrypt(key, in_filename, out_filename, 64*1024)
    def upload_model(self, model_id, model_version, in_filename):
        return self.__upload(model_id, model_version, in_filename)  
    def upload_data(self, model_id, model_version, in_filename, attributes):
        return self.__upload_data(model_id, model_version, in_filename, attributes)
    def download_model(self, model_id, model_version, out_filename):
        self.__download(model_id, model_version, out_filename)
    def __create_enc_and_mac_keys(self, master_key):
        keys = PBKDF2(master_key, 'Microsoft Santa Cruz Secure AI Lifecycle', 64, count=100000, hmac_hash_module=SHA512)
        return keys[:32], keys[32:]
    def __attest(self):
        token = self.__get_azure_token(os.environ["AZURE_TENANT_ID"],os.environ["AZURE_CLIENT_ID"],os.environ["AZURE_CLIENT_SECRET"])
        f = open(os.environ["SIMULATED_QUOTE"], 'rb') # TODO: This is temporary. Get actual TPM quote instead
        data = json.load(f)
        token = self.__attestation(token, os.environ["ATTESTATION_PROVIDER"], data)
        response = requests.post(self.__scz_url  + '/api/v1/login',
            json={
                "ATTESTATION_REPORT": token
            }, verify=False) # TODO: Remove verify=False before release
        self.__token = response.json()['access_token']
    def __attestation(self, token, provider, data):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            url = f"https://{provider}:443/attest/SgxEnclave?api-version=2018-09-01-preview"
            response = requests.post(url, headers=headers, json=data)
            jwt_text = response.text[1:-1]
            return jwt_text
        except:
            return None
    def __get_azure_token(self, tenant, client_id, client_secret):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "resource": "https://attest.azure.net"
        }
        response = requests.get(f"https://login.microsoftonline.com/{tenant}/oauth2/token", headers=headers, data = data)
        return response.json()['access_token']
        
class SCZMetricsExporter(MetricsExporter):
    def __init__(self, sczclient):
        self.__sczclient = sczclient
        self.__threshold = int(os.environ.get('CONFIDENCE_THRESHOLD', "90"))
        pass
    def export(self, metric_records: Sequence[MetricRecord]) -> MetricsExportResult:
        for metric_record in metric_records:
            if metric_record.instrument.name == "confidence":
                if metric_record.aggregator.checkpoint <= self.__threshold:
                    json = {}
                    json['name'] = metric_record.instrument.name
                    json['value'] = metric_record.aggregator.checkpoint
                    for label_tuple in metric_record.labels:
                        json[label_tuple[0]] = label_tuple[1]
                    print(json)
        return MetricsExportResult.SUCCESS
    def shutdown(self) -> None:
        pass

class SCZSpanExporter(SpanExporter):
    def __init__(self, sczclient):
        self.__sczclient = sczclient
        self.__threshold = int(os.environ.get('CONFIDENCE_THRESHOLD', "90"))
        pass
    def export(self, spans: Sequence[Span]) -> SpanExportResult:
        for span in spans:
            if span.events:
                for event in span.events:
                    if event.name == "inference" and event.attributes['confidence']:
                        if event.attributes['confidence'] < self.__threshold:
                            out_filename = event.attributes['file_ref'] + '.dec'
                            self.__sczclient.encrypt(event.attributes['model_name'], event.attributes['model_version'], event.attributes['file_ref'], out_filename)
                            self.__sczclient.upload_data(event.attributes['model_name'], event.attributes['model_version'], out_filename, event.attributes)
                            os.remove(out_filename)
                            print(event.attributes)

        return SpanExportResult.SUCCESS
    def shutdown(self):
        pass

if __name__ == "__main__":
    if len(sys.argv) == 7:
        server_url = sys.argv[1]
        command = sys.argv[2]
        model_name = sys.argv[3]
        model_version = sys.argv[4]
        in_file = sys.argv[5]
        out_file = sys.argv[6]
        client = SCZClient(server_url)
        device_name = socket.gethostname()

        trace.set_tracer_provider(TracerProvider())
        trace.get_tracer_provider().add_span_processor(
            SimpleExportSpanProcessor(SCZSpanExporter(client))
        )
        tracer = trace.get_tracer(__name__)

        if command == "decrypt":
            client.decrypt(model_name, model_version, in_file, out_file)
        elif command == "encrypt":
            client.encrypt(model_name, model_version, in_file, out_file)
        elif command == "upload":
            client.encrypt(model_name, model_version, in_file, out_file)
            client.upload_data(model_name, model_version, out_file, {})
        elif command == "download":
            client.download_model(model_name, model_version, in_file)
            client.decrypt(model_name, model_version, in_file, out_file)
        elif command == "export":
            confidence = int(sys.argv[5])
            data_file = sys.argv[6]
            with tracer.start_as_current_span("inference") as inference:
                inference.set_attribute('device', device_name)
                inference.add_event('inference', {
                    "confidence": confidence,
                    "model_name": model_name,
                    "model_version": model_version,
                    "file_ref": data_file
                })