from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    __version__,
)
from azure.core.exceptions import ResourceExistsError
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import io
import inspect
import os
import _pickle as cPickle
import joblib 
import json


def upload_function(f, module_name="postprocessor", serialization_type="plain/text", standarization="ml-flow", input_type="function"):
    source_code = b""
    container_name = "modules"
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    cloud_file_name = f"{module_name}"
    if serialization_type == "plain/text":
        if input_type=="function":
            source_code = inspect.getsource(f)
            cloud_file_name = cloud_file_name + ".py"
        elif input_type=="plain/yaml":
            source_code = f
            cloud_file_name = cloud_file_name + ".yaml"
        elif input_type=="dict":
            source_code = json.dumps(f)
            cloud_file_name = cloud_file_name + ".yaml"
    elif serialization_type == "bytes/cPickle":
        source_code = cPickle.dumps(f, 1)
        cloud_file_name = cloud_file_name + ".cpickle"
    elif serialization_type == "bytes/joblib":
        temp = io.BytesIO()
        joblib.dump(f, temp)
        temp.seek(0)
        source_code = temp.read()
    else:
        print(f"{serialization_type} is not an option")
        return
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # Create a blob client using the cloud_file_name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=cloud_file_name
    )
    # Upload the created file
    try:
        blob_client.upload_blob(source_code)
    except ResourceExistsError:
        print(
            "The specified blob already exists. Select a different name with module_name='new_name'."
        )


def register_flow(id, name, type="prediction"):
    table = "flows"
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    table_service = TableService(connection_string=connect_str)
    flow = {
        "PartitionKey": "tasksSeattle",
        "RowKey": "001",
        "description": "Take out the trash",
        "priority": 200,
    }
    table_service.insert_entity(table, flow)


def register_processor(
    id,
    name,
    type="preprocessor",
    company="None",
    flow_id="1",
    data_model=None,
    standarization="ml-flow",
):
    table = "processors"
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    table_service = TableService(connection_string=connect_str)
    processor = {
        "PartitionKey": type,
        "RowKey": id,
        "description": "",
        "company": company,
        "flow_id": flow_id,
        "data_model": data_model,
        "standarization": standarization,
    }
    table_service.insert_entity(table, processor)


def register_schema(
    id,
    name,
    type="preprocessor",
    company="None",
    flow_id="1",
    data_model=None,
    standarization="ml-flow",
):
    table = "schema"
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    table_service = TableService(connection_string=connect_str)
    processor = {
        "PartitionKey": type,
        "RowKey": id,
        "description": "",
        "company": company,
        "flow_id": flow_id,
        "data_model": data_model,
        "standarization": standarization,
    }
    table_service.insert_entity(table, processor)


def register_model(
    id, type="prediction", flow_id=None, processor_id=None, data_model=None
):
    table = "models"
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    table_service = TableService(connection_string=connect_str)
    model = {
        "PartitionKey": "tasksSeattle",
        "RowKey": "001",
        "description": "Take out the trash",
        "priority": 200,
    }
    table_service.insert_entity(table, model)
