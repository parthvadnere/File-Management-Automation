# core/api_client.py
import os
import re
import time
import logging
import requests
import json
from datetime import datetime
from urllib.parse import urljoin, quote
from client_manager.models import OutputConfig

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
        
    # def login(self, username, password):
    #     """
    #     Authenticate with the PharmpPix EFT system and store session cookies
        
    #     Args:
    #         username (str): Username for authentication
    #         password (str): Password for authentication
            
    #     Returns:
    #         bool: True if login successful, False otherwise
    #     """
    #     login_url = urljoin(self.base_url, "/EFTClient/Account/Login.htm")
    #     logger.info(f"Login URL: {login_url}")
    #     payload = {
    #         'username': username,
    #         'password': password
    #     }
        
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded',
    #         'Accept': 'application/json, text/html'
    #     }
    #     logger.info(f"login_url: {login_url}")
    #     logger.info(f"Payload: {payload}")
    #     logger.info(f"Logging in as {username}...")
    #     try:
    #         response = self.session.post(login_url, data=payload, headers=headers, verify=False)
            
    #         if response.status_code == 200:
    #             logger.info("Login successful!")
    #             logger.debug(f"Cookies received: {self.session.cookies.get_dict()}")
    #             return True
    #         else:
    #             logger.error(f"Login failed with status code: {response.status_code}")
    #             return False
    #     except requests.exceptions.RequestException as e:
    #         logger.error(f"Login request failed: {e}")
    #         return False
    
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
            # Create multiple adapters with different SSL configurations to try
            import ssl
            import urllib3
            from urllib3.poolmanager import PoolManager
            from requests.adapters import HTTPAdapter
            
            # Suppress InsecureRequestWarning
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            class TLSAdapter(HTTPAdapter):
                def __init__(self, ssl_options=None):
                    self.ssl_options = ssl_options
                    super(TLSAdapter, self).__init__()
                    
                def init_poolmanager(self, connections, maxsize, block=False):
                    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                    
                    # Apply custom SSL options if provided
                    if self.ssl_options:
                        for opt, value in self.ssl_options.items():
                            setattr(ctx, opt, value)
                    
                    # Set cipher configurations to be more compatible with older servers
                    # Use a more permissive cipher list
                    ctx.set_ciphers('DEFAULT@SECLEVEL=1')
                    
                    self.poolmanager = PoolManager(
                        num_pools=connections,
                        maxsize=maxsize,
                        block=block,
                        ssl_context=ctx
                    )
            
            # Try different SSL configurations
            ssl_configurations = [
                # Configuration 1: Default with relaxed security
                {
                    "check_hostname": False,
                    "verify_mode": ssl.CERT_NONE
                },
                # Configuration 2: TLS v1 only
                {
                    "check_hostname": False,
                    "verify_mode": ssl.CERT_NONE,
                    "options": ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
                },
                # Configuration 3: TLS v1.1 only
                {
                    "check_hostname": False,
                    "verify_mode": ssl.CERT_NONE,
                    "options": ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
                },
                # Configuration 4: TLS v1.2 only
                {
                    "check_hostname": False,
                    "verify_mode": ssl.CERT_NONE,
                    "options": ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
                }
            ]
            
            # Try each configuration until one works
            last_exception = None
            for config in ssl_configurations:
                try:
                    logger.info(f"Trying SSL configuration: {config}")
                    session = requests.Session()
                    adapter = TLSAdapter(ssl_options=config)
                    session.mount('https://', adapter)
                    
                    response = session.post(login_url, data=payload, headers=headers)
                    
                    if response.status_code == 200:
                        logger.info("Login successful!")
                        # Copy cookies to the original session
                        self.session.cookies.update(session.cookies)
                        logger.debug(f"Cookies received: {self.session.cookies.get_dict()}")
                        
                        # Update our session with the working adapter
                        self.session = session
                        return True
                    else:
                        logger.warning(f"Login attempt failed with status code: {response.status_code}")
                except Exception as e:
                    logger.warning(f"Login attempt failed with error: {str(e)}")
                    last_exception = e
            
            # If we get here, all configurations failed
            if last_exception:
                logger.error(f"All SSL configurations failed. Last error: {str(last_exception)}")
            else:
                logger.error("All SSL configurations failed with non-200 status codes.")
            return False
            
        except Exception as e:
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
        Fetch output configurations from the database.
        """
        # Normalize file_type
        file_type = file_type.lower().strip('.')

        # Format date for naming conventions
        yyyymmdd = file_date.replace('-', '')
        try:
            mmddyyyy = datetime.strptime(file_date, '%Y-%m-%d').strftime('%m%d%Y')
        except ValueError:
            mmddyyyy = yyyymmdd  # Fallback if date format is unexpected

        output_configs = []

        # Fetch configurations from the database
        configs = OutputConfig.objects.filter(
            client__name=client_name,
            path__path=path,
            file_type=file_type
        )
        for config in configs:
            # Replace date placeholders in the filename template
            output_filename = config.filename_template.replace('{yyyymmdd}', yyyymmdd).replace('{mmddyyyy}', mmddyyyy)
            # Handle special case for Lucent Health
            if 'OriginalFilename' in config.filename_template:
                output_filename = output_filename.replace('OriginalFilename', filename)
            output_configs.append({
                'output_dir': config.output_dir,
                'filename': output_filename
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
        
        if not file_type:
            _, ext = os.path.splitext(filename)
            file_type = ext if ext else '.unknown'
            
        file_date = file_info['Date'].split()[0]
        output_configs = self._get_output_configs(client_name, path, filename, file_type, file_date)

        if not output_configs:
            logger.warning(f"No output configuration defined for client: {client_name}, path: {path}, file_type: {file_type}")
            return None

        url_path_components = [quote(p) for p in path.split('/')]
        url_formatted_path = '/'.join(url_path_components)
        
        if file_type.lower() == ".xlsx":
            full_url = urljoin(self.base_url, f"/To_TransparentRX/{url_formatted_path}/{filename}")
        else:
            full_url = urljoin(self.base_url, file_info['Path'])
        
        if "&#37;20" in full_url:
            full_url = full_url.replace("&#37;20", "%20")
        full_url = full_url.split('&')[0]
        logger.info(f"Downloading file from: {full_url}")
        
        try:
            response = self.session.get(full_url, timeout=60)
            if response.status_code == 200:
                output_paths = []
                for config in output_configs:
                    output_dir = config['output_dir']
                    output_filename = config['filename']
                    output_path = os.path.join(output_dir, output_filename)

                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                        logger.debug(f"Created directory: {output_dir}")

                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"File downloaded successfully to: {output_path}")
                    output_paths.append(output_path)

                return output_paths
            else:
                logger.error(f"Failed to download file. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Download request failed: {e}")
            return None