import codecs
import csv
import chardet

import boto3
import botocore
import environ
import logging

env = environ.Env()
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
S3_OBJECT_LIFECYCLE_DAYS = env.str('S3_OBJECT_LIFECYCLE_DAYS', '')

logger = logging.getLogger()


class S3FileManager(object):
    """
    class to upload and read file in s3

    """
    LIFECYCLE_DAYS = S3_OBJECT_LIFECYCLE_DAYS or 30
    OBJECT_PREFIX = 'uploadmanager/'
    LIFE_CYCLE_RULE_NAME = 'UploadManagerBucketLCRule'

    def upload_file_content_to_s3(self, file_content, s3_storage_path):
        """
        core method to get the s3 connection and
        upload file in the given storage path
        :return:
        """
        s3 = boto3.client('s3')
        s3.put_object(Bucket=AWS_STORAGE_BUCKET_NAME,
                      Key=s3_storage_path,
                      Body=file_content)

        # commenting below lines to avoid functionality of setting life cycle
        # # setting bucket life cycle rule if not exists for upload manager
        # upload_manager_rule, other_rules = self.get_upload_manager_objects_lifecycle_rule(s3)
        # if upload_manager_rule is None:
        #     self.add_upload_manager_objects_lifecycle_rule(s3, other_rules)

        s3_url = "https://" + AWS_STORAGE_BUCKET_NAME + ".s3.amazonaws.com" + "/" + s3_storage_path
        logger.info("File successfully uploaded to s3 path: %s", s3_url)
        return s3_url

    def upload_file_to_s3(self, local_file_path, s3_storage_path):
        """
        core method to get the s3 connection and
        upload file in the given storage path
        :return:
        """
        s3 = boto3.client('s3')

        s3.upload_fileobj(local_file_path, AWS_STORAGE_BUCKET_NAME, s3_storage_path)

        s3_url = "https://" + AWS_STORAGE_BUCKET_NAME + ".s3.amazonaws.com" + "/" + s3_storage_path
        logger.info("File successfully uploaded to s3 path: %s", s3_url)
        return s3_url

    def read_file_from_s3(self, s3_url):
        if not s3_url:
            return None

        file_path = s3_url.split('com/')[1]
        s3 = boto3.client('s3')
        s3_response_object = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME,
                                           Key=file_path)

        # getting second stream to read about file formating
        # it is a temporary solution
        s3_response_object1 = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME,
                                            Key=file_path)
        content, content_copy = s3_response_object['Body'], s3_response_object1['Body']
        file_data = []

        # fetching encoding format
        encoding_format = chardet.detect(content_copy.read(1000))['encoding']
        try:
            for row in csv.DictReader(codecs.getreader(encoding_format.lower())(content)):
                file_data.append(row)
        except UnicodeDecodeError as e:
            logger.exception("Upload Manager: file decoding error %s" % e)
        return file_data

    def get_upload_manager_objects_lifecycle_rule(self, client):
        """
        function gets bucket life cycle rules for upload manager if present
        """
        rules = []
        try:
            config = client.get_bucket_lifecycle_configuration(Bucket=AWS_STORAGE_BUCKET_NAME)
            for rule in config['Rules']:
                if rule.get('ID') == self.LIFE_CYCLE_RULE_NAME:
                    return rule, rules
            rules = config['Rules']
        except botocore.exceptions.ClientError:
            logger.info("No life cycle rule found for bucket:%s" % AWS_STORAGE_BUCKET_NAME)
        return None, rules

    def add_upload_manager_objects_lifecycle_rule(self, client, existing_rules):
        """
        function adds upload manager life cycle rule
        """
        existing_rules.append({
            'ID': self.LIFE_CYCLE_RULE_NAME,
            'Status': 'Enabled',
            'Expiration': {
                'Days': self.LIFECYCLE_DAYS,
                },
            'Filter': {
                'Prefix': self.OBJECT_PREFIX,
                },
           })
        try:
            client.put_bucket_lifecycle_configuration(
                Bucket=AWS_STORAGE_BUCKET_NAME,
                LifecycleConfiguration={
                    'Rules': existing_rules,
                },
            )
        except botocore.exceptions.ClientError:
            logger.exception("Couldn't set life cycle rule for bucket:%s" % AWS_STORAGE_BUCKET_NAME)
