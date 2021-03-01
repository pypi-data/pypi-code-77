############################################################################
# Copyright 2020, Anteris Technologies LLC d/b/a Insipher.
# All rights reserved.
# info@insipher.com
# 
# NOTICE:  All information contained herein is, and remains
# the property of Anteris Technologies LLC d/b/a Insipher (“Insipher”).
# The intellectual and technical concepts contained herein are proprietary
# to Insipher and may be covered by U.S. and foreign patents or
# patent applications, trade secret, or copyright. Dissemination of
# this information or reproduction of this material is strictly
# forbidden unless prior written permission is obtained from Insipher.
#

import mlflow
import os
import random
import string
import shutil
from minio import Minio
from minio.error import S3Error
import yaml
import time
from abc import abstractmethod

class InsipherAlgorithm(object):
    __artifacts = []
    __algorithm_id = ''
    __minio_config = ''
    __mlflow_config = ''
    __minio_config_file = '/etc/config/minio-external-configmap.yaml'
    __minio_secret_file = '/vault/secrets/minio.txt'
    __mlflow_config_file = '/etc/config/mlflow-external-configmap.yaml'
    model = ''
    __tmpdir = ''

    def __init__(self):
        self.__algorithm_id = os.environ.get('ALGORITHM_ID')
        # wait for configmap to exist
        while not os.path.exists(self.__minio_config_file):
            time.sleep(1)
        with open(self.__minio_config_file, 'r') as f:
            self.__minio_config = yaml.load(f, Loader=yaml.FullLoader)

        # wait for configmap to exist
        while not os.path.exists(self.__mlflow_config_file):
            time.sleep(1)
        with open(self.__mlflow_config_file, 'r') as f:
            self.__mlflow_config = yaml.load(f, Loader=yaml.FullLoader)

        # set temp workspace for this process to prevent overwrites
        self.__tmpdir = "/tmp/" + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
        os.mkdir(self.__tmpdir)
        os.chdir(self.__tmpdir)

    #def set_model(self, model):
    #    self.__model = model

    def run_handler(self, data, query_params):
        response = self.run(data, query_params)
        self.__cleanup()
        return response

    def train_handler(self, data, query_params):
        mlflow.set_tracking_uri(self.__mlflow_config['endpoint'])
        mlflow.set_experiment(self.__algorithm_id)
        #experiment_id = mlflow.get_experiment_by_name(self.__algorithm_id).experiment_id
        #with mlflow.start_run(run_name='testrun', experiment_id=experiment_id):
        with mlflow.start_run():
            self.__run_id = mlflow.active_run().info.run_id
            mlflow.log_param("model", self.model)
            for param in query_params:
                mlflow.log_param(param, query_params[param])
            response = self.train(data, query_params)
        #mlflow.end_run()
        self.__cleanup()
        return response
    
    # abstract function to be implemented by algorithm developer
    @abstractmethod
    def run(self, data, query_params):
        pass

    # abstract function to be implemented by algorithm developer
    @abstractmethod
    def train(self, data, query_params):
        pass

    def log_metric(self, key, value):
        print("logging metric " + key + " with value " + value)

    def log_param(self, key, value):
        print("logging param " + key + " with value " + value)

    def persist_artifact(self, name):
        self.__artifacts.append(name)
        minioClient = self.__get_minio_client()
        metadata = {"X-Amz-Meta-Insipher-Mlflow-Run-Id": self.__run_id}
        try:
            with open(name, 'rb') as file_data:
                file_stat = os.stat(name)
                minioClient.put_object(self.__minio_config['algorithmBucket'], self.__algorithm_id+'/models/'+self.model+'/'+name,
                               file_data, file_stat.st_size, metadata=metadata)
        except S3Error as err:
            print(err)
        return name

    def get_artifact(self, name):
        minioClient = self.__get_minio_client()
        try:
            data = minioClient.get_object(self.__minio_config['algorithmBucket'], self.__algorithm_id+'/models/'+self.model+'/'+name)
            with open(name, 'wb') as file_data:
                for d in data.stream(32*1024):
                    file_data.write(d)
        except S3Error as err:
            print(err)
        return name

    def __get_minio_client(self):
        # get secret
        with open(self.__minio_secret_file, 'r') as f:
            secret = f.read()

        minio_access_key, minio_secret_key = secret.split(':')
        endpointSplit = self.__minio_config['endpoint'].split("//")
        return Minio(endpointSplit[1],
                  access_key=minio_access_key,
                  secret_key=minio_secret_key,
                  secure=self.__minio_config['useSSL'])

    def __cleanup(self):
        shutil.rmtree(self.__tmpdir)
        #for artifact in self.__artifacts:
        #    if os.path.exists(artifact):
        #        os.remove(artifact)