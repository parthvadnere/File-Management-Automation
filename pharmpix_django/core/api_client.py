# core/api_client.py
import os
import re
import time
import logging
import requests
import json
import ssl
import urllib3
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
from client_manager.models import OutputConfig

logger = logging.getLogger(__name__)

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
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=ctx
        )

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
        self.csrf_token = None
        self.websessionid = None
        self.ssl_adapter = None  # Store the working SSL adapter
        
        # Suppress InsecureRequestWarning globally
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Create the download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logger.info(f"Created download directory: {self.download_dir}")
        
    def _get_ssl_configurations(self):
        """
        Get different SSL configurations to try for compatibility
        
        Returns:
            list: List of SSL configuration dictionaries
        """
        return [
            {
                "check_hostname": False,
                "verify_mode": ssl.CERT_NONE
            },
            {
                "check_hostname": False,
                "verify_mode": ssl.CERT_NONE,
                "options": ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
            },
            {
                "check_hostname": False,
                "verify_mode": ssl.CERT_NONE,
                "options": ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
            },
            {
                "check_hostname": False,
                "verify_mode": ssl.CERT_NONE,
                "options": ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
            }
        ]
    
    def _setup_session_with_ssl(self, ssl_config):
        """
        Setup a session with specific SSL configuration
        
        Args:
            ssl_config (dict): SSL configuration dictionary
            
        Returns:
            requests.Session: Configured session
        """
        session = requests.Session()
        adapter = TLSAdapter(ssl_options=ssl_config)
        session.mount('https://', adapter)
        return session, adapter
    
    def login(self, username, password):
        """
        Authenticate with the PharmpPix EFT system and store session cookies and CSRF token
        
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
            # Try each SSL configuration until one works
            ssl_configurations = self._get_ssl_configurations()
            last_exception = None
            
            for config in ssl_configurations:
                try:
                    logger.info(f"Trying SSL configuration: {config}")
                    session, adapter = self._setup_session_with_ssl(config)
                    
                    response = session.post(login_url, data=payload, headers=headers)
                    
                    if response.status_code == 200:
                        logger.info("Login successful!")
                        # Store the working session and adapter
                        self.session = session
                        self.ssl_adapter = adapter
                        
                        logger.debug(f"Cookies received: {self.session.cookies.get_dict()}")
                        
                        # Extract websessionid from cookies
                        self.websessionid = self.session.cookies.get('websessionid')
                        logger.debug(f"Extracted websessionid: {self.websessionid}")
                        
                        # Extract X-CSRF-TOKEN from response headers
                        self.csrf_token = response.headers.get('X-CSRF-TOKEN')
                        if not self.csrf_token:
                            # If not in headers, try to extract from response body or subsequent request
                            try:
                                # Make a GET request to the main page to get the token
                                main_page_response = session.get(
                                    urljoin(self.base_url, "/?token="),
                                    headers={'Accept': 'text/html'}
                                )
                                if main_page_response.status_code == 200:
                                    # Search for token in response body (e.g., in JavaScript or meta tag)
                                    token_match = re.search(r'token=([A-F0-9\-]+)', main_page_response.text)
                                    if token_match:
                                        self.csrf_token = token_match.group(1)
                                        logger.debug(f"Extracted csrf_token from response body: {self.csrf_token}")
                            except Exception as e:
                                logger.warning(f"Failed to extract CSRF token from main page: {e}")
                        
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

    def upload_file(self, file_path, upload_endpoint, max_retries=3):
        """
        Upload a file to the specified endpoint on the Pharmpix server with retry logic.
        
        Args:
            file_path (str): Local path to the file to upload.
            upload_endpoint (str): API endpoint for upload (e.g., '/To_Pharmpix/AUTOMATION_TEST/').
            max_retries (int): Maximum number of retry attempts.
            
        Returns:
            dict: {'success': bool, 'errors': list} indicating upload status and any errors.
        """
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return {"success": False, "errors": [f"File not found: {file_path}"]}

        file_name = os.path.basename(file_path)
        upload_url = urljoin(self.base_url, upload_endpoint)
        
        headers = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-CSRF-TOKEN": self.csrf_token or "AF9AAE7F-6935-11f0-813E-005056BDF0C9",
            "X-Jument-Version": "v1.2.0 build 1",
            "X-Requested-With": "XMLHttpRequest",
            "X-DIRECTION": "UPLOAD",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Cookie": f"websessionid={self.websessionid or 'FF25A81A9F13950D9E3740B91E9B299650E3D5B50AA0C5F030FED0F5CE63CE43'}; savedpath={upload_endpoint},https; fileListSort=%7B%22property%22%3A%22date%22%2C%22sortAsc%22%3Afalse%7D; fileListThumbnail=false; i18next=en",
            "Referer": f"{self.base_url}/?token={self.csrf_token or 'AF9AAE7F-6935-11f0-813E-005056BDF0C9'}",
            "Origin": self.base_url
        }

        # Try with existing session first, then try different SSL configurations if needed
        sessions_to_try = [self.session]
        
        # If the main session fails, try creating new sessions with different SSL configs
        if self.ssl_adapter:
            ssl_configurations = self._get_ssl_configurations()
            for config in ssl_configurations:
                try:
                    session, adapter = self._setup_session_with_ssl(config)
                    # Copy cookies from the main session
                    session.cookies.update(self.session.cookies)
                    sessions_to_try.append(session)
                except Exception as e:
                    logger.warning(f"Failed to create session with SSL config {config}: {e}")

        last_error = None
        
        for attempt in range(max_retries):
            for session_idx, session in enumerate(sessions_to_try):
                try:
                    logger.info(f"Upload attempt {attempt + 1}/{max_retries} for {file_name} using session {session_idx}")
                    logger.debug(f"Upload URL: {upload_url}")
                    logger.debug(f"Session cookies: {session.cookies.get_dict()}")
                    
                    with open(file_path, 'rb') as f:
                        files = {
                            'file': (file_name, f, 'text/plain', {
                                'Content-Disposition': f'attachment; filename="{file_name}"'
                            })
                        }
                        
                        # Set longer timeouts for upload
                        response = session.post(
                            upload_url,
                            headers=headers,
                            files=files,
                            timeout=(30, 120),  # (connect_timeout, read_timeout)
                            verify=False  # Explicitly disable SSL verification
                        )
                        
                        response.raise_for_status()
                        logger.info(f"Upload successful for {file_name}: {response.status_code} - {response.text}")
                        
                        # Update main session if a different session was successful
                        if session_idx > 0:
                            self.session = session
                            logger.info(f"Updated main session to use successful SSL configuration")
                        
                        return {"success": True, "errors": []}
                        
                except (requests.exceptions.SSLError, 
                        requests.exceptions.ConnectionError,
                        ssl.SSLEOFError) as e:
                    logger.warning(f"SSL/Connection error on attempt {attempt + 1} with session {session_idx}: {str(e)}")
                    last_error = str(e)
                    # Continue to next session configuration
                    continue
                    
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Request error on attempt {attempt + 1} with session {session_idx}: {str(e)}")
                    last_error = str(e)
                    if 'response' in locals():
                        logger.debug(f"Response status: {response.status_code}")
                        logger.debug(f"Response headers: {response.headers}")
                        logger.debug(f"Response text: {response.text[:1000]}...")
                    # Continue to next session configuration
                    continue
                    
                except Exception as e:
                    logger.error(f"Unexpected error on attempt {attempt + 1} with session {session_idx}: {str(e)}")
                    last_error = str(e)
                    # Continue to next session configuration
                    continue
            
            # If we've tried all sessions and still failed, wait before next attempt
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff: 2, 4, 6 seconds
                logger.info(f"All sessions failed for attempt {attempt + 1}. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

        # All attempts failed
        logger.error(f"Upload failed for {file_name} after {max_retries} attempts. Last error: {last_error}")
        return {"success": False, "errors": [last_error or "Upload failed after all retry attempts"]}

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
            'Accept': 'application/json, text/html',
            'X-CSRF-TOKEN': self.csrf_token or '',
            'Cookie': f'websessionid={self.websessionid or ""}; savedpath=/{formatted_path},https'
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
        logger.info(f"path: {path}, file_type: {file_type}, file_date: {file_date}")
        try:
            if "Eligibility" not in path and "UMR_ACCUM" not in filename and "trx_UMR_RxEOB" not in filename: 
                file_date_obj = datetime.strptime(file_date, '%Y-%m-%d')
                file_date_obj -= timedelta(days=1)
                file_date = file_date_obj.strftime('%Y-%m-%d')
            else:
                logger.info("Eligibility path detected, skipping date adjustment")
        except ValueError:
            pass
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
        logger.info("**********************")
        logger.info(f"file_date: {file_date}, file_type: {file_type}")
        logger.info("**********************")
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
            headers = {
                'X-CSRF-TOKEN': self.csrf_token or '',
                'Cookie': f'websessionid={self.websessionid or ""}; savedpath=/{url_formatted_path},https'
            }
            response = self.session.get(full_url, headers=headers, timeout=60)
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