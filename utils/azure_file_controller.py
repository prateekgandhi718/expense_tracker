from io import BytesIO
import uuid
from pathlib import Path
from azure.storage.blob import BlobClient
from django.conf import settings 


ALLOWED_EXTENTIONS = ['.jpg', '.jpeg', '.jpg', '.png']


def create_blob_client(file_name):

    return BlobClient(
        account_url=settings.AZURE_STORAGE_ACCOUNT,
        container_name=settings.AZURE_APP_BLOB_NAME,
        blob_name=file_name,
        credential=None,
    )



def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENTIONS


def download_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content


def upload_file_to_blob(file):
    if not check_file_ext(file.name):
        return

    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    file_name = f"{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    blob_client = create_blob_client(file_name=file_name)
    blob_client.upload_blob(data=file_io)
    print("file's new name that is uploaded to the storage account", file_name)
    return file_name


def delete_blob_client(file_name):
    blob_client = create_blob_client(file_name)
    print(settings.AZURE_BLOB_PATH+file_name)
    blob_client.delete_blob()
    return True