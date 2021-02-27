class Storage(object):
    def init(self, batch):
        self.cache_bucket_name = batch.cache_bucket_name
        self.output_bucket_name = batch.output_bucket_name
        self.logger = batch.logger

    def __repr__(self):
        return "<Storage %s cache:%s output:%s>" % (
                self.__class__.__name__,
                getattr(self, 'cache_bucket_name', ''),
                getattr(self, 'output_bucket_name', ''),
                )

    def connect(self):
        pass

    def upload_cache(self, cache_filepath):
        """
        Uploads the file cached at cache_filepath to storage.

        Should raise an exception if the file at cache_filepath does not exist.

        Should return public_url to the file in storage if successful.
        """
        cache_filename = cache_filepath.name
        return self._upload_cache(cache_filename, cache_filepath)

    def _upload_cache(self, cache_filename, cache_filepath):
        """
        Implement this method in subclass
        """
        pass

    def download_cache(self, cache_filepath):
        """
        Download the file from storage to local file system at cache_filepath 

        Should return true if sucessful, false if file does not exist remotely
        """
        cache_filename = cache_filepath.name
        return self._download_cache(cache_filename, cache_filepath)

    def _download_cache(self, cache_filename, cache_filepath):
        """
        Implement this method in subclass
        """
        pass

    def reset_cache(self):
        """
        Deletes and re-creates the cache directory.
        """
        pass

    def reset_output(self):
        """
        Deletes and re-creates the output directory.
        """
        pass

    def upload_output(self, canonical_filename, cache_filepath):
        """
        Uploads the file cached at cache_filepath to storage.

        Should raise an exception if the file at cache_filepath does not exist.

        Should return public_url to the file in storage if successful.
        """
        return self._upload_output(canonical_filename, cache_filepath)

    def _upload_output(self, canonical_filename, cache_filepath):
        """
        Implement this method in subclass
        """
        pass


class GoogleCloudStorage(Storage):
    def find_or_create_bucket(self, bucket_name):
        import google.api_core.exceptions
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
        except google.api_core.exceptions.NotFound:
            self.logger.debug("creating bucket %s" % bucket_name)
            bucket = self.storage_client.create_bucket(bucket_name)

        #bucket.make_public(recursive=True, future=True)
        return bucket

    def delete_cache_bucket(self):
        try:
            self.cache_storage_bucket.delete(force=True)
        except ValueError:
            blobs = self.cache_storage_bucket.list_blobs()
            for blob in blobs:
                blob.delete()
            self.cache_storage_bucket.delete(force=True)

    def delete_output_bucket(self):
        try:
            self.output_storage_bucket.delete(force=True)
        except ValueError:
            blobs = self.output_storage_bucket.list_blobs()
            for blob in blobs:
                blob.delete()
            self.output_storage_bucket.delete(force=True)

    def create_public_bucket(self, name):
        bucket = self.storage_client.create_bucket(name)
        bucket.make_public(recursive=True, future=True)
        return bucket

    def connect(self):
        from google.cloud import storage
        self.storage_client = storage.Client()
        self.cache_storage_bucket = self.find_or_create_bucket(self.cache_bucket_name)
        self.output_storage_bucket = self.find_or_create_bucket(self.output_bucket_name)

    def _upload_cache(self, cache_filename, cache_filepath):
        blob = self.cache_storage_bucket.blob(cache_filename)
        self.logger.debug("  uploading blob to cache for %s" % cache_filename)
        blob.upload_from_filename(str(cache_filepath))
        return blob.public_url

    def _download_cache(self, cache_filename, cache_filepath):
        blob = self.cache_storage_bucket.blob(cache_filename)
        if blob.exists():
            self.logger.debug("  blob exists, downloading from %s to %s" % (self.cache_bucket_name, cache_filepath))
            blob.download_to_filename(cache_filepath)
            return True
        else:
            return False

    def reset_cache(self):
        self.delete_cache_bucket()
        self.cache_storage_bucket = self.create_public_bucket(self.cache_bucket_name)

    def _upload_output(self, canonical_filename, cache_filepath):
        blob = self.output_storage_bucket.blob(canonical_filename)
        self.logger.debug("  uploading blob to output for %s" % canonical_filename)
        blob.upload_from_filename(str(cache_filepath))
        return blob.public_url

    def reset_output(self):
        self.delete_output_bucket()
        self.output_storage_bucket = self.create_public_bucket(self.output_bucket_name)

AVAILABLE_STORAGES = {
        'google' : GoogleCloudStorage
        }
