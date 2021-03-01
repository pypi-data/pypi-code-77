from .models import UploadManager


def get_upload_id_s3_url(upload_id):
    """
    function helps in fetching uploaded files s3 url
     for given upload id
    """
    try:
        upload_obj = UploadManager.objects.get(id=upload_id)
    except UploadManager.DoesNotExist:
        assert "Trying to fetch `s3_upload_path` of a id " \
               "which is not present in upload manager"
        return
    return upload_obj.s3_upload_path
