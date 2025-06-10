# core/sftp_client.py
import paramiko
import os
import logging
from datetime import datetime
import re

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

    def download_file(self, remote_path, file_pattern, local_path, renamed_pattern, date_obj):
        """
        Download a file from the remote path matching the file pattern,
        rename it, and store it in the local path.
        Returns the local file path if successful, None otherwise.
        """
        try:
            # Create regex pattern for file matching
            date_str = date_obj.strftime('%Y%m%d')
            
            # Build regex pattern based on the file_pattern
            if "YYYYMMDD" in file_pattern:
                # Replace YYYYMMDD with actual date
                regex_pattern = file_pattern.replace("YYYYMMDD", date_str)
            elif "MMDDYYYY" in file_pattern:
                # Handle MMDDYYYY format
                date_str_mmddyyyy = date_obj.strftime('%m%d%Y')
                regex_pattern = file_pattern.replace("MMDDYYYY", date_str_mmddyyyy)
            else:
                regex_pattern = file_pattern

            # Replace HHMMSS with regex pattern to match any 6 digits
            if "HHMMSS" in regex_pattern:
                regex_pattern = regex_pattern.replace("HHMMSS", r"\d{6}")
                
            logger.info(f"Looking for files matching pattern: {regex_pattern}")
            
            # Compile the regex pattern
            compiled_pattern = re.compile(regex_pattern)
            
            # List files in the remote directory
            try:
                remote_files = self.sftp.listdir(remote_path)
                logger.info(f"Files in remote directory {remote_path}: {remote_files}")
            except Exception as e:
                logger.error(f"Error listing remote directory {remote_path}: {str(e)}")
                return None
            
            # Find matching files
            matching_files = []
            for remote_file in remote_files:
                if compiled_pattern.match(remote_file):
                    matching_files.append(remote_file)
                    logger.info(f"Found matching file: {remote_file}")
            
            if not matching_files:
                logger.warning(f"No files found matching pattern: {regex_pattern}")
                return None
            
            # Sort files by name (newest first if timestamp is in filename)
            matching_files.sort(reverse=True)
            selected_file = matching_files[0]
            logger.info(f"Selected file for download: {selected_file}")
            
            # Construct remote file path
            remote_file_path = f"{remote_path}/{selected_file}"
            
            # Create local directory if it doesn't exist
            local_dir = os.path.join(self.local_base_dir, local_path)
            os.makedirs(local_dir, exist_ok=True)
            
            # Generate renamed filename
            renamed_file_name = renamed_pattern
            if "YYYYMMDD" in renamed_file_name:
                renamed_file_name = renamed_file_name.replace('YYYYMMDD', date_str)
            if "HHMMSS" in renamed_file_name:
                # Extract timestamp from the original filename if needed
                # or use current time
                current_time = datetime.now().strftime('%H%M%S')
                renamed_file_name = renamed_file_name.replace('HHMMSS', current_time)
            
            local_file_path = os.path.join(local_dir, renamed_file_name)
            
            # Download the file
            logger.info(f"Downloading from: {remote_file_path}")
            logger.info(f"Downloading to: {local_file_path}")
            
            self.sftp.get(remote_file_path, local_file_path)
            logger.info(f"File downloaded successfully to: {local_file_path}")
            
            return local_file_path
            
        except Exception as e:
            logger.error(f"Error downloading file with pattern {file_pattern}: {str(e)}")
            return None