from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.credentials import AzureNamedKeyCredential
import uuid
from app.config.env.data import (
    AZ_BLOB_ACCOUNT_KEY,
    AZ_BLOB_ACCOUNT_NAME,
    AZ_BLOB_CONTAINER_NAME,
)


class AzureBlobService:
    def __init__(self, account_name: str, account_key: str, container_name: str):
        credential = AzureNamedKeyCredential(account_name, account_key)

        self.blob_service_client = BlobServiceClient(
            f"https://{account_name}.blob.core.windows.net", credential=credential
        )

        self.container_name = container_name
        self.container_client = self.blob_service_client.get_container_client(
            container_name
        )

    def upload_image(self, file, folder=""):
        if isinstance(file, str):
            ext = file.split(".")[-1]
            file_name = f"{uuid.uuid4()}-{uuid.uuid4()}.{ext}"

            blob_path = f"{folder}/{file_name}" if folder else file_name

            blob_client = self.container_client.get_blob_client(blob_path)

            with open(file, "rb") as f:
                blob_client.upload_blob(
                    f,
                    overwrite=True,
                    content_settings=ContentSettings(content_type=f"image/{ext}"),
                )

            return blob_client.url

        ext = file.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}-{uuid.uuid4()}.{ext}"

        blob_path = f"{folder}/{file_name}" if folder else file_name

        blob_client = self.container_client.get_blob_client(blob_path)
        blob_client.upload_blob(
            file.file,
            overwrite=True,
            content_settings=ContentSettings(content_type=f"image/{ext}"),
        )

        return blob_client.url


blob_service = AzureBlobService(
    account_name=AZ_BLOB_ACCOUNT_NAME,
    account_key=AZ_BLOB_ACCOUNT_KEY,
    container_name=AZ_BLOB_CONTAINER_NAME,
)
