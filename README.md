# TransparentRx File Management Automation

This project automates the download and processing of files from the PharmpPix EFT system for various clients such as ALLIED, ASR, BML, UMR, and Lucent Health.

## Features

- Download client-specific files using PharmpPix API
- Configuration-driven file processing
- Logging and summary of operations
- Designed for extensibility

## Prerequisites

- Python 3.8 or above
- Redis (for Celery task queue)
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Dev-Devanggiri/TransparentRx-File-Management-Automation.git
cd TransparentRx-File-Management-Automation
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

> Note: If a `requirements.txt` is present, use it. Otherwise, install needed packages manually.

```bash
pip install -r requirements.txt
```
or (if requirements.txt is not present, typical dependencies might be)
```bash
pip install requests celery redis
```

### 4. Start Redis Server

Make sure Redis is running on your machine:
```bash
redis-server
```

### 5. Configure Environment Variables (Optional)

If your project requires environment variables, create a `.env` file in the root.

### 6. Start Celery Worker

Assuming you have a Celery app (e.g., in Pharmpix_client/celery_app.py):

```bash
celery -A Pharmpix_client.celery_app worker --loglevel=info
 or 
celery -A Pharmpix_client worker --loglevel=info -E --pool=solo
```

### 7. Run the Main Script

Navigate to the Pharmpix_client directory and run the main script:

```bash
cd Pharmpix_client
python main.py --username <your-username> --password <your-password> --clients ALLIED ASR --download-dir <directory>
```
- Replace `<your-username>` and `<your-password>` with your PharmpPix credentials.
- Specify clients as needed, or omit `--clients` to process all.
- Use the `--list-only` flag to only list files without downloading.

## Example Usage

```bash
python main.py --username user@example.com --password secret --clients ALLIED --download-dir ./downloads
```

## Project Structure

```
Pharmpix_client/
│
├── main.py                # Entry point for file processing
├── core/
│   ├── api_client.py      # PharmpPix API client
│   └── file_processor.py  # Client file processing logic
├── config/
│   └── client_config.py   # Configuration for clients
└── utils/
    └── helpers.py         # Logging and helpers
```

## Logging

Logs are written to `pharmpix_api.log` by default.

## Extending

- Add new clients in `config/client_config.py`
- Modify processing logic in `core/file_processor.py`

## License

MIT

---

**For issues or contributions, please open a GitHub issue or pull request.**
