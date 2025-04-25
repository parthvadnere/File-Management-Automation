# config/client_config.py
from client_manager.models import Client, Path

def get_client_config():
    """
    Fetch client configurations from the database.

    Returns:
        dict: Configuration for each client including paths and file types
    """
    client_configs = {}
    clients = Client.objects.all()
    print("into get_client_config")
    for client in clients:
        paths = Path.objects.filter(client=client)
        client_configs[client.name] = {
            "paths": [
                {
                    "path": path.path,
                    "file_types": path.file_types,
                    "max_files": path.max_files,
                    "file_pattern": path.file_pattern,
                }
                for path in paths
            ]
        }

    return client_configs