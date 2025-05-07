# client_manager/tasks.py
from celery import shared_task
from client_manager.models import Client, DownloadedFile
from core.api_client import PharmpixApiClient
import logging
from config.client_config import get_client_config
from core.file_processor import process_client
import os
from django.core.files import File
import paramiko
from client_manager.utils import validate_txt_file
from datetime import datetime

logger = logging.getLogger(__name__)

@shared_task
def test_task():
    print("This is a test task")
    return "Test task completed"

@shared_task
def download_files_task(client_id, username="it@transparentrx.com", password="_4ajPc,Owjkc", download_dir="5PM-Work", selected_date=None):
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
        results = process_client(client_name, client_config, api_client, download_files=True, selected_date=selected_date)
        logger.info(f"Processing results for {client_name}: {results}")

        # Check if any files were downloaded
        if not results:
            logger.warning(f"No files downloaded for {client_name}")
            return {"status": "Completed", "message": f"No files found to download for {client_name}."}

        # Save downloaded files to the database
        saved_files = []
        for path_key, file_paths_list in results.items():
            # Ensure file_paths_list is a list
            if not isinstance(file_paths_list, list):
                logger.error(f"Expected file_paths_list to be a list, got {type(file_paths_list)}: {file_paths_list}")
                continue

            # Iterate over the list of file paths
            for file_path in file_paths_list:
                if not isinstance(file_path, str):
                    logger.error(f"Expected file_path to be a string, got {type(file_path)}: {file_path}")
                    continue

                logger.info(f"Processing file: {file_path}")
                # Normalize file path
                file_path = file_path.replace('\\', '/')
                logger.info(f"Normalized file path: {file_path}")

                # Validate file path
                if not file_path or file_path in ['/', '\\'] or not os.path.exists(file_path):
                    logger.warning(f"Invalid or non-existent file path: {file_path}")
                    continue

                file_name = os.path.basename(file_path)
                logger.info(f"File found: {file_name}")
                file_type = os.path.splitext(file_name)[1].lstrip('.')
                logger.info(f"File type: {file_type}")
                path = path_key.replace(file_type, '').replace('_', '/')

                with open(file_path, 'rb') as f:
                    file_content = f.read()
                logger.info(f"client: {client_name}, file_content: {file_content[:50]}..., original_filename: {file_name}, file_type: {file_type}, path: {path}")

                validation_result = {"is_valid": True, "errors": []}
                if file_type.lower() == 'txt':
                    validation_result = validate_txt_file(file_content, client_name)
                    logger.info(f"Validation result for {file_name}: {validation_result}")

                downloaded_file = DownloadedFile(
                    client=client,
                    file_content=file_content,
                    original_filename=file_name,
                    file_type=file_type,
                    path=path,
                    is_validated=validation_result["is_valid"],
                    validation_errors="\n".join(validation_result["errors"]) if validation_result["errors"] else None,
                    downloaded_at=datetime.now()
                )
                downloaded_file.save()
                saved_files.append(downloaded_file.original_filename)
                logger.info(f"Saved file to database: {file_name}")

                if validation_result["is_valid"]:
                    if client.sftp_host and client.sftp_username and client.sftp_password:
                        try:
                            transport = paramiko.Transport((client.sftp_host, client.sftp_port or 22))
                            transport.connect(username=client.sftp_username, password=client.sftp_password)
                            sftp = paramiko.SFTPClient.from_transport(transport)

                            remote_path = f"/{client_name}/{file_name}"
                            with open(file_path, 'rb') as local_file:
                                sftp.putfo(local_file, remote_path)
                            logger.info(f"File {file_name} sent to SFTP server at {remote_path}")

                            downloaded_file.sent_to_sftp = True
                            downloaded_file.save()

                            sftp.close()
                            transport.close()
                        except Exception as e:
                            logger.error(f"Failed to send {file_name} to SFTP for client {client_name}: {str(e)}")
                            downloaded_file.validation_errors = f"SFTP transfer failed: {str(e)}"
                            downloaded_file.save()
                    else:
                        logger.warning(f"No SFTP credentials for client {client_name}. File not sent.")

                os.remove(file_path)
                logger.info(f"Deleted local file: {file_path}")

        return {"status": "Completed", "message": f"Files for {client_name} downloaded successfully."}
    except Exception as e:
        logger.error(f"Error downloading files for client {client_id}: {str(e)}", exc_info=True)
        return {"status": "Failed", "message": f"Error: {str(e)}"}
