import os
import requests 
import struct

class AzureMSIAuth(object):
    """
    Defines the Azure Active Directory authentication class.
    """

    @classmethod
    def get_msi_token(cls):

      #get access token
      identity_endpoint = os.environ["IDENTITY_ENDPOINT"]
      identity_header = os.environ["IDENTITY_HEADER"]
      resource_uri="https://database.windows.net/"
      token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01"
      head_msi = {'X-IDENTITY-HEADER':identity_header}
      resp = requests.get(token_auth_uri, headers=head_msi)
      access_token = resp.json()['access_token']

      access_token = bytes(access_token, 'utf-8')
      exptoken = b""
      for i in access_token:
              exptoken += bytes({i})
              exptoken += bytes(1)
      return struct.pack("=i", len(exptoken)) + exptoken
