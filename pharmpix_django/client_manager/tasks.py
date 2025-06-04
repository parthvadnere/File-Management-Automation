# client_manager/tasks.py
from celery import shared_task
from client_manager.models import Client, DownloadedFile, FileConfig
from core.api_client import PharmpixApiClient
import logging
from config.client_config import get_client_config
from core.file_processor import process_client
import os
from django.core.files import File
import paramiko
from client_manager.utils import validate_txt_file, validate_file, validate_umr_accumulator_file, validate_PBLXV_file_with_auto_date, validate_and_correct_RxEOB_umr_accumulator_file, validate_eligibility_file
from datetime import datetime
from core.sftp_client import SFTPClient

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
                logger.info(f"file_type.lower(): {file_type.lower()}")
                if file_type.lower() == 'txt':
                    if "RxEOB" in file_path and "Accum" in file_path or "ACCUM" in file_path:
                        # UMR Accumulator file validation
                        logger.info("Validating UMR Accumulator file")
                        validation_result = validate_and_correct_RxEOB_umr_accumulator_file(
                            file_content=file_content,
                            client_name=client_name,  # Replace with actual client name if known
                            output_file_path="corrected_EMP_Accum_20250529_001.txt"
                        )
                    elif "UMR-Accum-EFTP-to-SFTP" in file_path and "PBLXV426_P_" in file_path:
                        # PBLXV426_P_ claims files validation logic (using existing layout)
                        logger.info("Validating PBLXV426_P_ claims file")
                        validation_result = validate_umr_accumulator_file(file_content, client_name)
                        # validation_result = validate_PBLXV_file_with_auto_date(
                        #     file_content=file_content,
                        #     client_name=client_name,
                        #     filename=file_name,
                        #     selected_date=selected_date
                        # )
                    elif "Eligibility" in file_path:
                        # RxEOB claims files validation logic (using existing layout)
                        logger.info("Validating RxEOB Eligibility txt file")
                        validation_result = validate_eligibility_file(file_content, client_name)
                    else:
                        # Regular claims files validation logic
                        logger.info("Validating claims file")
                        validation_result = validate_txt_file(file_content, client_name)
                elif file_type.lower() == 'xlsx':
                    # Add xlsx file validation logic if needed
                    logger.info("XLSX file validation not implemented yet")
                    validation_result = {"is_valid": True, "errors": []}
                else:
                    validation_result = {"is_valid": False, "errors": [f"Unsupported file type: {file_type}"]}
                # if file_type.lower() == 'xlsx':
                #     # add xlsx file validation logic if needed
                #     pass
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


@shared_task
def download_10pm_files_task(selected_date=None):
    """
    Task to download Accumulator and Eligibility files from SFTP servers for all active clients.
    Args:
        selected_date (str): Date in YYYY-MM-DD format. Defaults to today if None.
    """
    logger.info(f"Starting 10PM file download task, selected_date: {selected_date}")
    
    try:
        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
        else:
            date_obj = datetime.now()
        date_str = date_obj.strftime('%Y%m%d')

        # Get all active clients
        clients = Client.objects.filter(is_active=True)
        if not clients:
            logger.warning("No active clients found for 10PM task")
            return {"status": "Completed", "message": "No active clients found"}

        all_results = {}

        for client in clients:
            logger.info(f"\n========== PROCESSING CLIENT: {client.name} ==========")
            if client.name == "Allied":
                date_str = date_obj.strftime('%m%d%Y')
            logger.info(f"date_str::{date_str}")
            # Check if the client has SFTP credentials
            if not (client.sftp_host and client.sftp_username and client.sftp_password):
                logger.warning(f"SFTP credentials missing for client {client.name}. Skipping.")
                continue

            # Initialize SFTP client
            sftp_client = SFTPClient(
                host=client.sftp_host,
                username=client.sftp_username,
                password=client.sftp_password,
                port=client.sftp_port,
                local_base_dir=""
            )

            if not sftp_client.connect():
                logger.error(f"Failed to connect to SFTP for client {client.name}")
                continue

            try:
                # Get file configurations for this client
                file_configs = FileConfig.objects.filter(client=client, is_active=True)
                client_results = []

                for file_config in file_configs:
                    logger.info(f"Processing {file_config.file_type} file for {client.name}")

                    # Download the file
                    local_file_path = sftp_client.download_file(
                        remote_path=file_config.remote_path,
                        file_pattern=file_config.file_pattern,
                        local_path=file_config.local_path,
                        renamed_pattern=file_config.renamed_pattern,
                        date_str=date_str
                    )

                    if not local_file_path:
                        logger.warning(f"No {file_config.file_type} file downloaded for {client.name}")
                        continue

                    # Validate the file
                    validation_result = validate_file(local_file_path)
                    logger.info(f"Validation result for {local_file_path}: {validation_result}")

                    # Store the file details in the database
                    with open(local_file_path, 'rb') as f:
                        file_content = f.read()

                    file_name = os.path.basename(local_file_path)
                    downloaded_file = DownloadedFile(
                        client=client,
                        file_content=file_content,
                        original_filename=file_name,
                        file_type=file_config.file_type,
                        path=file_config.local_path,
                        is_validated=validation_result["is_valid"],
                        validation_errors="\n".join(validation_result["errors"]) if validation_result["errors"] else None,
                        downloaded_at=datetime.now()
                    )
                    downloaded_file.save()
                    logger.info(f"Saved file to database: {file_name}")

                    client_results.append(local_file_path)

                all_results[client.name] = client_results
            finally:
                sftp_client.disconnect()

        return {"status": "Completed", "message": f"10PM task completed successfully: {all_results}"}
    except Exception as e:
        logger.error(f"Error in 10PM file download task: {str(e)}", exc_info=True)
        return {"status": "Failed", "message": f"Error: {str(e)}"}