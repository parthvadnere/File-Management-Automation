# core/api_client.py
import os
import re
import time
import logging
import requests
import json
from datetime import datetime
from urllib.parse import urljoin, quote

logger = logging.getLogger(__name__)

class PharmpixApiClient:
    def __init__(self, base_url="https://eft.pharmpix.com", download_dir="pharmpix_downloads"):
        """
        Initialize the PharmpixApiClient with base URL and download directory
        
        Args:
            base_url (str): Base URL of the PharmpPix EFT system
            download_dir (str): Directory to store downloaded files
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.allow_redirects = True
        self.download_dir = download_dir
        
        # Create the download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"Created download directory: {self.download_dir}")
        
    def login(self, username, password):
        """
        Authenticate with the PharmpPix EFT system and store session cookies
        
        Args:
            username (str): Username for authentication
            password (str): Password for authentication
            
        Returns:
            bool: True if login successful, False otherwise
        """
        login_url = urljoin(self.base_url, "/EFTClient/Account/Login.htm")
        payload = {
            'username': username,
            'password': password
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/html'
        }
        
        logger.info(f"Logging in as {username}...")
        try:
            response = self.session.post(login_url, data=payload, headers=headers)
            
            if response.status_code == 200:
                logger.info("Login successful!")
                logger.debug(f"Cookies received: {self.session.cookies.get_dict()}")
                return True
            else:
                logger.error(f"Login failed with status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Login request failed: {e}")
            return False
    
    def get_path_components(self, path):
        """
        Parse a path into its components for more flexible file retrieval
        
        Args:
            path (str): Path string like 'UMR/Empire' or 'ALLIED/Claims'
            
        Returns:
            tuple: (client, category, subcategory) where some values may be None
        """
        components = path.strip('/').split('/')
        
        client = components[0] if len(components) > 0 else None
        category = components[1] if len(components) > 1 else None
        subcategory = components[2] if len(components) > 2 else None
        
        return client, category, subcategory
        
    def get_files(self, path, file_type=None, file_pattern=None, params=None):
        """
        Get files for a specific path with optional file type filtering and pattern matching
        
        Args:
            path (str): Path like 'ALLIED/Claims' or 'UMR/Empire'
            file_type (str, optional): File extension to filter by (e.g., ".txt", ".results", ".xlsx"). 
                                      If None, returns all files. Defaults to None.
            file_pattern (str, optional): Regex pattern to match file names. Defaults to None.
            params (dict, optional): Additional query parameters. Defaults to None.
        
        Returns:
            dict: JSON-formatted response with file information
        """
        # Handle spaces in path components (e.g., "Lucent Health")
        path_components = [quote(p) for p in path.split('/')]
        formatted_path = '/'.join(path_components)
        
        url = f"/To_TransparentRX/{formatted_path}/"
        print(f"URL: {url}")
        # Default parameters for sorting and pagination
        default_params = {
            'json': None,
            'rows': 0,
            'page': 0,
            'sidx': 'filename',
            'sord': 'desc'
        }
        
        # Update with custom parameters if provided
        if params:
            default_params.update(params)
            
        full_url = urljoin(self.base_url, url)
        print("Full URL:", full_url)
        headers = {
            'Accept': 'application/json, text/html'
        }

        logger.info(f"Fetching data from: {full_url}")
        try:
            response = self.session.get(full_url, params=default_params, headers=headers)
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                
                # Check if we got JSON
                if 'application/json' in content_type:
                    try:
                        json_response = response.json()
                        # Apply file pattern filter if provided
                        if file_pattern:
                            json_response = self._filter_by_pattern(json_response, file_pattern)
                        return json_response
                    except json.JSONDecodeError:
                        logger.error("Failed to parse JSON response")
                
                # If we got HTML, parse it
                if 'text/html' in content_type:
                    html_response = self._parse_html_directory_listing(response.text, file_type=file_type)
                    # Apply file pattern filter if provided
                    if file_pattern:
                        html_response = self._filter_by_pattern(html_response, file_pattern)
                    return html_response
                    
                # If we can't determine the type, return the raw text
                return response.text
            else:
                logger.error(f"Request failed with status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def _filter_by_pattern(self, response_data, pattern):
        """
        Filter files in the response by a regex pattern
        
        Args:
            response_data (dict): API response data
            pattern (str): Regex pattern to match filenames
            
        Returns:
            dict: Filtered response data
        """
        if not response_data or 'rows' not in response_data:
            return response_data
            
        regex = re.compile(pattern)
        filtered_rows = []
        
        for row in response_data['rows']:
            if 'cell' in row and len(row['cell']) >= 1:
                filename = row['cell'][0]
                if regex.match(filename):
                    filtered_rows.append(row)
        
        # Update response with filtered rows
        filtered_response = response_data.copy()
        filtered_response['rows'] = filtered_rows
        filtered_response['records'] = str(len(filtered_rows))
        
        logger.info(f"Filtered files by pattern '{pattern}': found {len(filtered_rows)} matches")
        return filtered_response
    
    def _parse_html_directory_listing(self, html_content, file_type=None):
        """
        Parse HTML directory listing and convert to JSON format
        Filter by file_type if specified (e.g., '.txt', '.results', '.xlsx')
        
        Args:
            html_content (str): HTML content to parse
            file_type (str, optional): File type to filter by. Defaults to None.
            
        Returns:
            dict: Structured data of files
        """
        logger.debug("Parsing HTML directory listing")
        # Define regex pattern for file links with date and size
        pattern = r'(\d+ \w+ \d+\s+\d+:\d+)\s+(\d+) <a href="([^"]+)">([^<]+)</a>'
        
        # Find all matches in the HTML content
        matches = re.findall(pattern, html_content)
        
        rows = []
        for idx, match in enumerate(matches, 1):
            date_str, size, href, filename = match
            
            # Filter by file type if specified
            if file_type and not filename.lower().endswith(file_type.lower()):
                continue
                
            path = href.split('?')[0]  # Remove token from path
            
            # Convert date string to a consistent format
            try:
                date_obj = datetime.strptime(date_str, "%d %b %Y %H:%M")
                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = date_str
            
            # Create a row in the format similar to Postman JSON response
            row = {
                "id": str(idx),
                "cell": [
                    filename,
                    size,
                    formatted_date,
                    path,
                    {}
                ]
            }
            rows.append(row)
        
        # Reindex rows after filtering
        for i, row in enumerate(rows, 1):
            row["id"] = str(i)
        
        # Construct the full JSON response
        result = {
            "total": "1",
            "page": "1",
            "records": str(len(rows)),
            "rows": rows
        }
        
        logger.info(f"Found {len(rows)} files matching criteria")
        return result

    def _get_output_configs(self, client_name, path, filename, file_type, file_date):
        """
        Define output folder paths and naming conventions based on client, path, and file type
        """
        # Normalize file_type
        file_type = file_type.lower().strip('.')

        # Format date for naming conventions
        yyyymmdd = file_date.replace('-', '')
        mmddyyyy = datetime.strptime(file_date, '%Y-%m-%d').strftime('%m%d%Y')

        output_configs = []

        if client_name == "ALLIED":
            if path == "ALLIED/Claims" and file_type == "txt":
                # Store in 5PM-Work/Allied/Claims
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'Allied', 'Claims'),
                    'filename': f'Trans_RxClaims_{mmddyyyy}.txt'
                })
                # Also store in 5PM-Work/RxEOB/Claims/Sapp
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Claims', 'Sapp'),
                    'filename': f'Sapp_Claims_{yyyymmdd}_0004.txt'
                })
            elif path == "ALLIED/Eligibility" and file_type == "results":
                # Store in 5PM-Work/RxEOB/Eligibility
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Eligibility'),
                    'filename': f'Sapp_MEM_TRX_{yyyymmdd}_0001.txt'
                })
            elif path == "ALLIED/Eligibility" and file_type == "xlsx":
                # Store in 5PM-Work/Allied/Eligibility
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'Allied', 'Eligibility'),
                    'filename': f'Trans_Elig_{mmddyyyy}.xlsx'
                })

        elif client_name == "ASR":
            if path == "ASR/Claims" and file_type == "txt":
                # Store in 5PM-Work/ASR
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'ASR'),
                    'filename': f'TRX_CLAIMS_{yyyymmdd}.txt'
                })
                # Also store in 5PM-Work/RxEOB/Claims/ASR
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Claims', 'ASR'),
                    'filename': f'ASR_Claims_{yyyymmdd}_0001.txt'
                })
            elif path == "ASR/Eligibility" and file_type == "xlsx":
                # Store in 5PM-Work/ASR
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'ASR'),
                    'filename': f'TRXALBION_PPX_ELIG_{yyyymmdd}_001.xlsx'
                })
            elif path == "ASR/Eligibility" and file_type == "results":
                # Store in 5PM-Work/RxEOB/Eligibility
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Eligibility'),
                    'filename': f'TRXALBION_PPX_ELIG_{yyyymmdd}_001.txt'
                })

        elif client_name == "BML":
            if path == "BML/Claims" and file_type == "txt":
                # Store in 5PM-Work/RxEOB/Claims/BML
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Claims', 'BML'),
                    'filename': f'BML_Claims_{yyyymmdd}_0002.txt'
                })

        elif client_name == "Lucent Health":
            if path == "Lucent Health/Claims" and file_type == "txt":
                # Store in 5PM-Work/Lucent_health with original filename
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'Lucent_health'),
                    'filename': f'{filename}.txt'  # Assuming filename is available in scope
                })

        elif client_name == "UMR":
            if path == "UMR" and file_type == "txt":
                # Store in 5PM-Work/UMR-Accum-EFTP-to-SFTP
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'UMR-Accum-EFTP-to-SFTP'),
                    'filename': f'PBLXV426_P_TransparentRx_{yyyymmdd}.txt'
                })
            elif path == "UMR/Empire" and file_type == "txt":
                # Store in 5PM-Work/RxEOB/Claims/EMP
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Claims', 'EMP'),
                    'filename': f'EMP_Claims_{yyyymmdd}_0003.txt'
                })
            elif path == "UMR/IOA/Eligibility" and file_type == "results":
                # Store in 5PM-Work/RxEOB/Eligibility
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Eligibility'),
                    'filename': f'EMP_MEM_TRX_UMR_{yyyymmdd}_0001.txt'
                })
            elif path == "UMR/IOA/Eligibility" and file_type == "xlsx":
                # Store in 5PM-Work/UMR/Eligibility
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'UMR', 'Eligibility'),
                    'filename': f'ErrRpt_P_TransparentRx_IOA_{yyyymmdd}.xlsx'
                })
            elif path == "UMR/UMR_Exc_OOP" and file_type == "txt":
                # Store in 5PM-Work/RxEOB/Accum
                output_configs.append({
                    'output_dir': os.path.join(self.download_dir, 'RxEOB', 'Accum'),
                    'filename': f'EMP_Accum_{yyyymmdd}_0001.txt'
                })

        return output_configs

    def download_file(self, path, file_info, file_type=None):
        """
        Download a file from the server and save to the organized directory structure
        
        Args:
            path (str): Path like 'ALLIED/Claims' or 'UMR/Empire'
            file_info (dict): File information dictionary
            file_type (str, optional): File extension. Defaults to None.
            
        Returns:
            str: Path to the downloaded file, or None if download failed
        """
        filename = file_info['Filename']
        client_name, _, _ = self.get_path_components(path)
        
        # Get file type from filename if not provided
        if not file_type:
            _, ext = os.path.splitext(filename)
            file_type = ext if ext else '.unknown'
            
        file_date = file_info['Date'].split()[0]
        output_configs = self._get_output_configs(client_name, path, filename, file_type, file_date)

        if not output_configs:
            logger.warning(f"No output configuration defined for client: {client_name}, path: {path}, file_type: {file_type}")
            return None

        # Create directory structure for organized storage
        # Format: pharmpix_downloads/[PATH]/[FILETYPE]/
        # path_components = path.split('/')
        # path_dirs = os.path.join(self.download_dir, *path_components)
        # file_type_dir = os.path.join(path_dirs, file_type.strip('.').upper())
        
        # Create directories if they don't exist
        # if not os.path.exists(file_type_dir):
        #     os.makedirs(file_type_dir)
        #     logger.debug(f"Created directory: {file_type_dir}")
        
        # Handle spaces in path components for URL construction
        url_path_components = [quote(p) for p in path.split('/')]
        url_formatted_path = '/'.join(url_path_components)
        
        # Construct the URL for download
        if file_type.lower() == ".xlsx":
            # Fix for Excel files
            full_url = urljoin(self.base_url, f"/To_TransparentRX/{url_formatted_path}/{filename}")
        else:
            full_url = urljoin(self.base_url, file_info['Path'])
        print("Full URL in download_file function : ", full_url)
        print("filename in download_file function : ", filename)
        # Strip query parameters from the URL if present
        if "&#37;20" in full_url:
            full_url = full_url.replace("&#37;20", "%20")
        full_url = full_url.split('&')[0]
        print("full_url after stripping query parameters : ", full_url)
        logger.info(f"Downloading file from: {full_url}")
        
        try:
            response = self.session.get(full_url, timeout=60)
            if response.status_code == 200:
                output_paths = []
                for config in output_configs:
                    output_dir = config['output_dir']
                    output_filename = config['filename']
                    output_path = os.path.join(output_dir, output_filename)

                    # Create directory if it doesn't exist
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                        logger.debug(f"Created directory: {output_dir}")

                    # Save the file
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"File downloaded successfully to: {output_path}")
                    output_paths.append(output_path)

                # Return the first output path for compatibility with existing code
                return output_paths[0] if output_paths else None
            else:
                logger.error(f"Failed to download file. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Download request failed: {e}")
            return None