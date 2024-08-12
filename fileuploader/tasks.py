import logging
from celery import shared_task
from azure.storage.blob import BlobServiceClient
import os
import logging
   

logger = logging.getLogger(__name__)

# Initialize Azure Blob Storage client
AZURE_CONNECTION_STRING =  os.environ.get('AZURE_CONNECTION_STRING')  # Replace with your actual connection string
BLOB_SERVICE_CLIENT = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
CONTAINER_NAME = os.environ.get('AZURE_CONTAINER_NAME')  # Replace with your actual container name

@shared_task
def process_small_file(file_path, file_name):
    try:
        # Read the file from disk and upload to Azure Blob Storage
        with open(file_path, 'rb') as f:
            file_data = f.read()
        blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container=CONTAINER_NAME, blob=file_name)
        blob_client.upload_blob(file_data)
    finally:
        # Ensure the temp file is removed after processing
        if os.path.exists(file_path):
            os.remove(file_path)

@shared_task(bind=True)
def process_large_file(self, file_path, file_name, total_size):
    try:
        logger.info(f"Starting chunked file upload for {file_name}")
        chunk_size = 1024 * 1024  # 1 MB per chunk
        blob_client = BLOB_SERVICE_CLIENT.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        # Initialize the append blob if it's the first chunk
        if not blob_client.exists():
            blob_client.create_append_blob()

        with open(file_path, 'rb') as f:
            for chunk in range(0, total_size, chunk_size):
                chunk_data = f.read(chunk_size)
                blob_client.append_block(chunk_data)
        logger.info(f"Completed chunked file upload for {file_name}")
    except Exception as exc:
        logger.error(f"Error processing file {file_name}: {exc}")
        raise self.retry(exc=exc)
    finally:
        if os.path.exists(file_path):
            logger.info(f"Deleting temporary file {file_path}")
            os.remove(file_path)
        else:
            logger.warning(f"File {file_path} not found during cleanup.")