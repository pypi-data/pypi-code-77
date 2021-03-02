from ..upload_manager.s3 import S3FileManager
from ..upload_manager.file_operator import CSVFileWriter

s3_object = S3FileManager()


def test_upload_file_to_s3():
    writer = CSVFileWriter("/".join(["mocks", "mock_upload.csv"]))
    writer.write_rows_to_file([("Client ID", "Client Name"), ("1", "abcd")])
    file_obj = writer.get_file_object()
    s3_url = s3_object.upload_file_content_to_s3(file_obj.getvalue(), file_obj.name)
    assert s3_url != ""


def test_read_from_s3():
    file_data = s3_object.read_file_from_s3("https://dharm-test.s3.amazonaws.com/" + "mocks/mock_upload.csv")
    assert file_data != []
