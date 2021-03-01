import logging
from django.db import DatabaseError, OperationalError, Error

from .models import UploadManager
from .s3 import S3FileManager
from .file_operator import CSVFileWriter
from .utils import get_upload_id_s3_url

logger = logging.getLogger()


class AWSError(IOError):
    pass


class UploadManagerService:

    UPLOAD_PATH_PREFIX = 'uploadmanager'

    def __init__(self, upload_name, user, storage_path, files=None, file_content=None):
        self.upload_name = upload_name
        self.user = user
        self.s3_storage_path = storage_path
        self.files = files
        self.file_content = file_content
        self.s3_service = S3FileManager()

    def start_upload(self):
        """
        function starts upload process
        """
        logger.info("Starting upload event for %s", self.upload_name)
        self.upload_to_file_storage()
        upload = self.create_upload()
        return upload

    def update_response_for_upload(self, upload_id):
        """
        function uploads response file to s3 and
         updates download path in DB for given upload ID
        Note: This function will be soon deprecated. Recommended func is -> upload_response_to_s3
        """
        writer = self._get_response_writer(upload_id)
        writer.write_rows_to_file(self.file_content)
        file_obj = writer.get_file_object()
        try:
            s3_download_path = \
                self.s3_service.upload_file_content_to_s3(file_obj.getvalue(), file_obj.name)

            UploadManager.objects.filter(id=upload_id).update(s3_download_path=s3_download_path)
        except Exception as e:
            logger.exception("S3 Upload for %s failed with exception: %s", self.upload_name, e)
            raise AWSError
        finally:
            writer.close_writer()

    @classmethod
    def upload_response_to_s3(cls, upload_id, file_content):
        """
        function uploads response file to s3 and
        updates download path in DB for given upload ID
        """
        s3_service = S3FileManager()
        writer = cls._get_response_writer(upload_id)
        writer.write_rows_to_file(file_content)
        file_obj = writer.get_file_object()
        try:
            s3_download_path = \
                s3_service.upload_file_content_to_s3(file_obj.getvalue(), file_obj.name)
            UploadManager.objects.filter(id=upload_id).update(s3_download_path=s3_download_path)
        except Exception as e:
            logger.exception("S3 Upload for %s failed with exception: %s", upload_id, e)
            raise AWSError
        finally:
            writer.close_writer()

    @classmethod
    def _get_response_writer(cls, upload_id):
        """
        function creates response writer and returns it
        """
        s3_upload_path = UploadManager.objects.get(id=upload_id).s3_upload_path
        bucket_path = s3_upload_path.split(".com/")[-1]
        file_path, uploaded_file_name = bucket_path.rsplit("/", 1)
        response_file_name = "response_" + uploaded_file_name
        writer = CSVFileWriter("/".join([file_path, response_file_name]))
        return writer

    def upload_to_file_storage(self):
        """
        function uploads input file to S3
        """
        try:
            for file in self.files:
                # to remove slashes from start & end of path as we are adding it
                self.s3_storage_path = self.s3_storage_path.strip("/")

                self.s3_storage_path = \
                    self.s3_service.upload_file_to_s3(file, "/".join([self.UPLOAD_PATH_PREFIX,
                                                                      self.s3_storage_path,
                                                                      file.name.split("/")[-1]]))
        except Exception as e:
            logger.exception("S3 Upload for %s failed with exception: %s", self.upload_name, e)
            raise AWSError

    def create_upload(self):
        """
        function creates Upload manager DB entry
        """
        try:
            upload = UploadManager.objects.create(upload_name=self.upload_name, user=self.user,
                                                  s3_upload_path=self.s3_storage_path,
                                                  s3_download_path=None,
                                                  status=UploadManager.OPEN)
        except (DatabaseError, OperationalError, Error) as e:
            logger.error("Database population failed for %s with exception: %s",
                         self.upload_name, e)
            raise DatabaseError
        return upload

    @classmethod
    def get_upload_content_for_id(cls, upload_id):
        s3_url = get_upload_id_s3_url(upload_id)
        return S3FileManager().read_file_from_s3(s3_url)

    @classmethod
    def change_upload_status_to_inprocess(cls, upload_id):
        """
        function to changes upload status to in process
        """
        UploadManager.change_upload_status(upload_id, UploadManager.IN_PROCESS)
        logger.info(f"changed upload status for {upload_id} to 'IN Progress'")

    @classmethod
    def change_upload_status_to_complete(cls, upload_id):
        """
        function to changes upload status to complete
        """
        UploadManager.change_upload_status(upload_id, UploadManager.COMPLETED)
        logger.info(f"changed upload status for {upload_id} to 'Completed'")

    @classmethod
    def change_upload_status_to_failed(cls, upload_id):
        """
        function to changes upload status to failed
        """
        UploadManager.change_upload_status(upload_id, UploadManager.FAILED)
        logger.info(f"changed upload status for {upload_id} to 'Failed'")

    @classmethod
    def change_upload_status_to_validation_failed(cls, upload_id):
        """
        function to changes upload status to validation failed
        """
        UploadManager.change_upload_status(upload_id, UploadManager.VALIDATION_FAILED)
        logger.info(f"changed upload status for {upload_id} to 'Validation Failed'")
