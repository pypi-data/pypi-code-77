import datetime

from django.db import models


class BaseModel(models.Model):
    created_on = models.DateTimeField(editable=False, default=datetime.datetime.now)
    updated_on = models.DateTimeField(editable=False, auto_now=True)
    created_by_id = models.IntegerField(null=False, default=1)
    updated_by_id = models.IntegerField(null=False, default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class UploadManager(BaseModel):
    OPEN = 'open'
    IN_PROCESS = 'in_process'
    VALIDATION_FAILED = 'validation_failed'
    COMPLETED = 'completed'
    FAILED = 'failed'
    STATUS_CHOICES = (
        (OPEN, 'Pushed to Queue'),
        (IN_PROCESS, 'In Process'),
        (COMPLETED, 'Completed'),
        (VALIDATION_FAILED, 'Validation Failed'),
        (FAILED, 'Failed'),
    )
    upload_name = models.CharField(max_length=255, db_index=True)
    user = models.CharField(max_length=50, db_index=True)
    s3_upload_path = models.CharField(max_length=255, blank=True, null=True)
    s3_download_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=OPEN, db_index=True)
    meta_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.id, self.upload_name)

    @classmethod
    def change_upload_status(cls, upload_id, status):
        upload = cls.objects.get(id=upload_id)
        upload.status = status
        upload.save()
