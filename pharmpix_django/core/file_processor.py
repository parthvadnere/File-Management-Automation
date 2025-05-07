# core/file_processor.py
import logging
import time
from utils.helpers import extract_file_info
from datetime import datetime
import os

logger = logging.getLogger(__name__)

def process_client(client_name, client_config, client_obj, download_files=True, selected_date=None):
    """
    Process a specific client according to its configuration
    
    Args:
        client_name (str): Name of the client
        client_config (dict): Configuration for the client
        client_obj: Initialized API client object
        download_files (bool): Whether to download files or just list them
        selected_date (date, optional): Date to filter files (YYYY-MM-DD)
        
    Returns:
        dict: Results of processing, including downloaded files
    """
    results = {}
    
    for path_config in client_config["paths"]:
        path = path_config["path"]
        file_types = path_config["file_types"]
        max_files = path_config.get("max_files", 3)
        file_pattern = path_config.get("file_pattern", None)
        
        logger.info(f"\n=== PROCESSING {path} ===")
        
        for file_type in file_types:
            response = client_obj.get_files(path, file_type=file_type, file_pattern=file_pattern)
            
            if response and isinstance(response, dict) and 'rows' in response:
                files = extract_file_info(response)
                files = sorted(files, key=lambda x: x['Date'], reverse=True)
                
                if file_pattern:
                    logger.info(f"Found {len(files)} {file_type} files matching pattern '{file_pattern}' in {path}")
                else:
                    logger.info(f"Found {len(files)} {file_type} files in {path}")
                
                # Filter files by selected date
                if selected_date:
                    filtered_files = []
                    for file_info in files:
                        file_date_str = file_info['Date'].split()[0]  # e.g., "2025-04-29"
                        try:
                            file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()
                            if file_date == selected_date:
                                filtered_files.append(file_info)
                        except ValueError:
                            logger.warning(f"Invalid date format for file {file_info['Filename']}: {file_date_str}")
                            continue
                    files = filtered_files
                    logger.info(f"After date filter ({selected_date}), {len(files)} {file_type} files remain")
                
                if not files:
                    logger.info(f"No files match the selected date for {path} with file type {file_type}")
                    continue
                
                # Print the first few files
                for i, file_info in enumerate(files[:max_files], 1):
                    logger.info(f"{i}. {file_info['Filename']} - {file_info['Size (bytes)']} bytes - {file_info['Date']}")
                
                # Download files if requested
                if download_files and files:
                    downloaded = []
                    for i, file_info in enumerate(files[:max_files]):
                        logger.info(f"Downloading file {i+1}/{min(max_files, len(files))}: {file_info['Filename']}")
                        
                        if i > 0:
                            time.sleep(1)
                            
                        file_path = client_obj.download_file(path, file_info, file_type=file_type)
                        if file_path:
                            if isinstance(file_path, list):
                                # Ensure each item in the list is a string
                                for fp in file_path:
                                    if not isinstance(fp, str):
                                        logger.error(f"Expected file path to be a string, got {type(fp)}: {fp}")
                                        continue
                                    downloaded.append(fp)
                            else:
                                if not isinstance(file_path, str):
                                    logger.error(f"Expected file path to be a string, got {type(file_path)}: {file_path}")
                                    continue
                                downloaded.append(file_path)
                            logger.info(f"Downloaded file(s): {downloaded}")
                    
                    # Store results
                    path_key = path.replace('/', '_') + file_type
                    results[path_key] = downloaded
                    logger.info(f"Stored results for {path_key}: {downloaded}")
            else:
                if file_pattern:
                    logger.warning(f"No data returned for {path} with file type {file_type} and pattern '{file_pattern}'")
                else:
                    logger.warning(f"No data returned for {path} with file type {file_type}")
    
    return results

def process_all_clients(client_obj, username, password, client_configs, clients=None, download_files=True, selected_date=None):
    """
    Process all or selected clients
    
    Args:
        client_obj: Initialized API client object
        username (str): Username for authentication
        password (str): Password for authentication
        client_configs (dict): Client configurations
        clients (list, optional): List of client names to process. If None, process all.
        download_files (bool, optional): Whether to download files.
        selected_date (date, optional): Date to filter files
        
    Returns:
        dict: Results of processing
    """
    if not client_obj.login(username, password):
        logger.error("Login failed. Cannot continue.")
        return {}
    
    if clients:
        clients_to_process = {k: v for k, v in client_configs.items() if k in clients}
    else:
        clients_to_process = client_configs
    
    if not clients_to_process:
        logger.warning("No valid clients specified to process.")
        return {}
        
    all_results = {}
    
    for client_name, config in clients_to_process.items():
        logger.info(f"\n\n========== PROCESSING CLIENT: {client_name} ==========")
        results = process_client(client_name, config, client_obj, download_files, selected_date=selected_date)
        all_results[client_name] = results
    
    return all_results

def print_summary(results, list_only=False):
    """
    Print a summary of processing results
    
    Args:
        results (dict): Processing results
        list_only (bool): Whether only listing was done
    """
    if list_only:
        return
        
    logger.info("\n\n=== DOWNLOAD SUMMARY ===")
    for client, client_results in results.items():
        logger.info(f"\nClient: {client}")
        total_files = sum(len(files) for files in client_results.values())
        logger.info(f"Total files: {total_files}")
        
        for path_type, files in client_results.items():
            logger.info(f"  - {path_type}: {len(files)} files")
            for file_path in files:
                logger.info(f"    * {os.path.basename(file_path)}")