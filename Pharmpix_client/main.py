# main.py
import os
import argparse
from core.api_client import PharmpixApiClient
from core.file_processor import process_all_clients, print_summary
from config.client_config import get_client_config
from utils.helpers import setup_logging

def main():
    """Main function to run the script with command line arguments"""
    # Set up logging
    logger = setup_logging()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download files from PharmpPix EFT system')
    parser.add_argument('--username', type=str, default="it@transparentrx.com", help='Username for authentication')
    parser.add_argument('--password', type=str, default="_4ajPc,Owjkc", help='Password for authentication')
    parser.add_argument('--clients', type=str, nargs='+', help='Clients to process (e.g., ALLIED ASR)')
    parser.add_argument('--list-only', action='store_true', help='Only list files, do not download')
    parser.add_argument('--download-dir', type=str, default="5PM-Work", help='Directory to store downloaded files')
    
    args = parser.parse_args()
    
    # Initialize API client
    client = PharmpixApiClient(download_dir=args.download_dir)
    
    # Get client configuration
    client_configs = get_client_config()
    
    # Process clients
    results = process_all_clients(
        client,
        args.username, 
        args.password,
        client_configs, 
        clients=args.clients, 
        download_files=not args.list_only
    )
    
    # Print summary
    print_summary(results, list_only=args.list_only)


if __name__ == "__main__":
    main()