# config/client_config.py

def get_client_config():
    """
    Define configuration for different clients based on Postman collection
    
    Returns:
        dict: Configuration for each client including paths and file types
    """
    return {
        "ALLIED": {
            "paths": [
                {"path": "ALLIED/Claims", "file_types": [".txt"], "max_files": 1},
                {"path": "ALLIED/Eligibility", "file_types": [".results", ".xlsx"], "max_files": 1}
            ]
        },
        "ASR": {
            "paths": [
                {"path": "ASR/Claims", "file_types": [".txt"], "max_files": 1},
                {"path": "ASR/Eligibility", "file_types": [".results", ".xlsx"], "max_files": 1}
            ]
        },
        "BML": {
            "paths": [
                {"path": "BML/Claims", "file_types": [".txt"], "max_files": 1}
            ]
        },
        "UMR": {
            "paths": [
                {"path": "UMR", "file_types": [".txt"], "max_files": 1},
                {"path": "UMR/Empire", "file_types": [".txt", ".xls"], "max_files": 1},
                {"path": "UMR/IOA/Eligibility", "file_types": [".results", ".xlsx"], "max_files": 1},
                {"path": "UMR/UMR_Exc_OOP", "file_types": [".txt"], "max_files": 1, 
                 "file_pattern": r"trx_UMR_RxEOB__\d{8}\.txt"}
            ]
        },
        "Lucent Health": {
            "paths": [
                {"path": "Lucent Health/Claims", "file_types": [".txt"], "max_files": 1}
            ]
        }
    }