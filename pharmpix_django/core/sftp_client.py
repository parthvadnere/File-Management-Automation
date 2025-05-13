# core/sftp_client.py
import paramiko
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SFTPClient:
    def __init__(self, host, username, password, port=22, local_base_dir=""):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.local_base_dir = local_base_dir
        self.sftp = None
        self.transport = None

    def connect(self):
        logger.info(f"Connecting to SFTP server: {self.host}:{self.port}")
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            logger.info("SFTP connection successful")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SFTP server: {str(e)}")
            return False

    def disconnect(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        logger.info("SFTP connection closed")

    def download_file(self, remote_path, file_pattern, local_path, renamed_pattern, date_str):
        """
        Download a file from the remote path matching the file pattern,
        rename it, and store it in the local path.
        Returns the local file path if successful, None otherwise.
        """
        try:
            # Replace date placeholders in file pattern
            file_name = file_pattern.replace('YYYYMMDD', date_str)
            file_name = file_name.replace('HHMMSS', datetime.now().strftime('%H%M%S'))
            remote_file_path = f"{remote_path}/{file_name}"

            logger.info(f"Attempting to download file: {remote_file_path}")

            # Check if the file exists on the remote server
            try:
                self.sftp.stat(remote_file_path)
            except FileNotFoundError:
                logger.warning(f"File not found on remote server: {remote_file_path}")
                return None

            # Create local directory if it doesn't exist
            local_dir = os.path.join(self.local_base_dir, local_path)
            os.makedirs(local_dir, exist_ok=True)

            # Replace date placeholders in renamed pattern
            renamed_file_name = renamed_pattern.replace('YYYYMMDD', date_str)
            renamed_file_name = renamed_file_name.replace('HHMMSS', datetime.now().strftime('%H%M%S'))
            local_file_path = os.path.join(local_dir, renamed_file_name)

            # Download the file
            logger.info(f"Downloading to: {local_file_path}")
            self.sftp.get(remote_file_path, local_file_path)
            logger.info(f"File downloaded successfully to: {local_file_path}")

            return local_file_path
        except Exception as e:
            logger.error(f"Error downloading file {remote_file_path}: {str(e)}")
            return None