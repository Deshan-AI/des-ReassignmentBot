# ReassignmentBot

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

4. Create a config.yaml file in the project root with your credentials:
```yaml
ERP:
  url: "your_erp_url"
  username: "your_username"
  password: "your_password"
ICP:
  url: "your_icp_url"
  username: "your_username"
  password: "your_password"
ZOHO:
  url: "your_zoho_url"
  username: "your_username"
  password: "your_password"
download_paths:
  Base: "path/to/downloads"
  Generated_Document: "path/to/generated"
  Icp: "path/to/icp"
data_path:
  Base: "path/to/data"
  Database: "path/to/database"
  Auth: "path/to/auth"
retry:
  max_attempts: 3
captcha:
  api_key: "your_2captcha_api_key"
sleep:
  max: 5
  min: 1
google_cloud:
  credentials: "path/to/credentials.json"
```

## Running the Application

To run the application:

```bash
python main.py
```

This will launch a browser window and perform the login operation.
