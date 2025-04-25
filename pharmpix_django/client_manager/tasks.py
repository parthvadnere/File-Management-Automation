# client_manager/tasks.py
from celery import shared_task
from client_manager.models import Client, DownloadedFile
from core.api_client import PharmpixApiClient
import logging
from config.client_config import get_client_config
from core.file_processor import process_client
import os
from django.core.files import File

logger = logging.getLogger(__name__)

@shared_task
def test_task():
    print("This is a test task")
    return "Test task completed"

@shared_task
def download_files_task(client_id, username="it@transparentrx.com", password="_4ajPc,Owjkc", download_dir="5PM-Work"):
    logger.info(f"Starting download_files_task for client_id: {client_id}")
    
    try:
        logger.info("Fetching client from database")
        client = Client.objects.get(id=client_id)
        client_name = client.name
        logger.info(f"Client found: {client_name}")

        logger.info("Initializing PharmpixApiClient")
        api_client = PharmpixApiClient(download_dir=download_dir)
        
        # Log in to the API
        if not api_client.login(username, password):
            logger.error("Login failed. Cannot continue.")
            return {"status": "Failed", "message": "Failed to log in to Pharmpix API."}

        logger.info("Fetching client configurations from database")
        configs = get_client_config()
        logger.info(f"Configs: {configs}")

        if client_name not in configs:
            logger.error(f"Client {client_name} not found in configurations")
            return {"status": "Failed", "message": f"Client {client_name} not found in configurations."}

        logger.info(f"Downloading files for client: {client_name}")
        client_config = configs[client_name]
        logger.info(f"Processing client: {client_name} with configuration: {client_config}")
        
        # Process the client using the API client (pass api_client, not file_info)
        results = process_client(client_name, client_config, api_client, download_files=True)
        logger.info(f"Processing results for {client_name}: {results}")

        # Check if any files were downloaded
        if not results:
            logger.warning(f"No files downloaded for {client_name}")
            return {"status": "Completed", "message": f"No files found to download for {client_name}."}

        # Save downloaded files to the database
        saved_files = []
        for path_key, file_paths in results.items():
            for file_path in file_paths:  # Iterate over the list of file paths
                logger.info(f"Processing file: {file_path}")
                if os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    file_type = os.path.splitext(file_name)[1].lstrip('.')
                    path = path_key.replace(file_type, '').replace('_', '/')

                    with open(file_path, 'rb') as f:
                        downloaded_file = DownloadedFile(
                            client=client,
                            original_filename=file_name,
                            file_type=file_type,
                            path=path
                        )
                        downloaded_file.file.save(file_name, File(f), save=True)
                        downloaded_file.save()
                        saved_files.append(downloaded_file.original_filename)
                        logger.info(f"Saved file to database: {file_name}")
                else:
                    logger.warning(f"File not found: {file_path}")

        return {"status": "Completed", "message": f"Files for {client_name} downloaded successfully."}
    except Exception as e:
        logger.error(f"Error downloading files for client {client_id}: {str(e)}", exc_info=True)
        return {"status": "Failed", "message": f"Error: {str(e)}"}
