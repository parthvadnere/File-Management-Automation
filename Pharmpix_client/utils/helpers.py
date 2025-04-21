# utils/helpers.py
import logging
import os

logger = logging.getLogger(__name__)

def setup_logging(log_file="pharmpix_api.log"):
    """
    Set up logging configuration
    
    Args:
        log_file (str): Path to log file
        
    Returns:
        logging.Logger: Configured logger
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def extract_file_info(response_data):
    """
    Extract and format file information from the API response
    
    Args:
        response_data (dict): API response data
        
    Returns:
        list: List of file information dictionaries
    """
    if not response_data or 'rows' not in response_data:
        logger.warning("No file data found in the response")
        return []
        
    files = []
    for row in response_data['rows']:
        if 'cell' in row and len(row['cell']) >= 4:
            file_info = {
                'Filename': row['cell'][0],
                'Size (bytes)': row['cell'][1],
                'Date': row['cell'][2],
                'Path': row['cell'][3]
            }
            files.append(file_info)
    
    return files