# client_manager/tasks.py
from celery import shared_task
from client_manager.models import Client, DownloadedFile, FileConfig, UploadConfig
from core.api_client import PharmpixApiClient
import logging
from config.client_config import get_client_config
from core.file_processor import process_client
import os
from django.core.files import File
import paramiko
from client_manager.utils import validate_txt_file, validate_file, validate_umr_accumulator_file, validate_PBLXV_file_with_auto_date, validate_and_correct_RxEOB_umr_accumulator_file, validate_eligibility_file, validate_txt_file_10PM_Accumlator
from datetime import datetime
from core.sftp_client import SFTPClient
import requests

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
def download_10pm_files_task(client_id, selected_date=None):
    """
    Task to download Accumulator and Eligibility files from SFTP server for a specific client.
    Args:
        client_id (int): ID of the client to process.
        selected_date (str): Date in YYYY-MM-DD format. Defaults to today if None.
    """
    logger.info(f"Starting 10PM file download task for client_id: {client_id}, selected_date: {selected_date}")
    
    try:
        if selected_date:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
        else:
            date_obj = datetime.now()
        # date_str = date_obj.strftime('%Y%m%d')

        # Get the specific client
        try:
            client = Client.objects.get(id=client_id, is_active=True)
        except Client.DoesNotExist:
            logger.error(f"Client with id {client_id} not found or not active")
            return {"status": "Failed", "message": f"Client with id {client_id} not found or not active"}

        logger.info(f"\n========== PROCESSING CLIENT: {client.name} ==========")
        # Check if the client has SFTP credentials
        if not (client.sftp_host and client.sftp_username and client.sftp_password):
            logger.warning(f"SFTP credentials missing for client {client.name}. Skipping.")
            return {"status": "Failed", "message": f"SFTP credentials missing for client {client.name}"}
        
        # Get the upload configuration for this client
        upload_config = UploadConfig.objects.filter(client=client, is_active=True).first()
        if not upload_config:
            logger.warning(f"No upload configuration found for client {client.name}. Skipping upload.")
            return {"status": "Failed", "message": f"No upload configuration for client {client.name}"}

        # Initialize SFTP client
        sftp_client = SFTPClient(
            host=client.sftp_host,
            username=client.sftp_username,
            password=client.sftp_password,
            port=client.sftp_port,
            local_base_dir=""
        )
        logger.info(f"Connecting to SFTP server for client {client.name} at {client.sftp_host}:{client.sftp_port}")
        if not sftp_client.connect():
            logger.error(f"Failed to connect to SFTP for client {client.name}")
            return {"status": "Failed", "message": f"Failed to connect to SFTP for client {client.name}"}

        try:
            # Get file configurations for this client
            file_configs = FileConfig.objects.filter(client=client, is_active=True)
            client_results = []
            logger.info("into try stmt::::: file_configs:::" + str(file_configs))
            for file_config in file_configs:
                logger.info(f"Processing {file_config.file_type} file for {client.name}")
            
                # Download the file
                local_file_path = sftp_client.download_file(
                    remote_path=file_config.remote_path,
                    file_pattern=file_config.file_pattern,
                    local_path=file_config.local_path,
                    renamed_pattern=file_config.renamed_pattern,
                    # date_str=date_str,
                    date_obj=date_obj
                )

                if not local_file_path:
                    logger.warning(f"No {file_config.file_type} file downloaded for {client.name}")
                    continue

                # Store the file details in the database
                logger.info(f"File downloaded successfully: {local_file_path}")
                with open(local_file_path, 'rb') as f:
                    file_content = f.read()
                logger.info(f"File content read successfully for {local_file_path}")
                logger.info(f"File content length: {len(file_content)} bytes :::: {file_content[:70]}...")
                file_name = os.path.basename(local_file_path)
                logger.info(f"File name extracted::::::::::::::: {file_name}")
                
                validation_result = validate_txt_file_10PM_Accumlator(
                    file_content,
                    client.name,
                    filename=file_name,
                    selected_date=date_obj.strftime('%Y%m%d') if selected_date else None
                )

                # Validate accumulator files
                # if "ACCUM" in file_config.file_type.upper() or "TRXALBION" in file_name or "ACCUM_UMR" in file_name:
                #     logger.info(f"Validating accumulator file: {file_name}")
                #     validation_result = validate_txt_file_10PM_Accumlator(file_content, client.name)
                # Add eligibility validation here later when sample is provided
                # elif "eligibility" in file_config.file_type.upper():
                #     logger.info(f"Validating eligibility file: {file_name}")
                #     validation_result = validate_eligibility_file(file_content, client.name)


                # logger.info(f"Validation result for {file_name}: {validation_result}")

                # Store the file details in the database
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

                if validation_result["is_valid"]:
                    client_results.append(local_file_path)
                    # Upload the file
                    upload_result = upload_file_to_pharmpix(
                        local_file_path,
                        upload_config.upload_endpoint,
                        upload_config.token,
                        client.name
                    )
                    if upload_result["success"]:
                        downloaded_file.is_uploaded = True
                        downloaded_file.save()
                        logger.info(f"File {file_name} uploaded successfully to {upload_config.upload_endpoint}")
                    else:
                        downloaded_file.upload_errors = "\n".join(upload_result["errors"])
                        downloaded_file.save()
                        logger.error(f"Upload failed for {file_name}: {upload_result['errors']}")
                else:
                    logger.warning(f"File {file_name} validation failed: {validation_result['errors']}")

            return {"status": "Completed", "message": f"10PM task completed for {client.name}: {client_results}"}
        finally:
            sftp_client.disconnect()
    except Exception as e:
        logger.error(f"Error in 10PM file download task: {str(e)}", exc_info=True)
        return {"status": "Failed", "message": f"Error: {str(e)}"}

def upload_file_to_pharmpix(file_path, upload_endpoint, token, client_name):
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "text/plain",
        "X-CSRF-TOKEN": token,
        "X-Jument-Version": "v1.2.0 build 1",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Cookie": f"token={token}; savedpath=/{upload_endpoint},https",
        "Referer": f"https://eft.pharmpix.com/?token={token}",
        "Origin": "https://eft.pharmpix.com"
    }
    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        files = {
            'file': (file_name, f, 'text/plain', {'Content-Disposition': f'attachment; filename="{file_name}"'})
        }
        try:
            response = requests.post(
                f"https://eft.pharmpix.com{upload_endpoint}",
                headers=headers,
                files=files,
                timeout=30
            )
            response.raise_for_status()
            logger.info(f"Upload response for {file_name}: {response.status_code} - {response.text}")
            return {"success": True, "errors": []}
        except requests.exceptions.RequestException as e:
            logger.error(f"Upload failed for {file_name}: {str(e)}")
            return {"success": False, "errors": [str(e)]}