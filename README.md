# S3 Client File Management Tool

## Overview

This is a Python-based command-line application for interacting with Amazon S3 buckets. The application provides a simple, menu-driven interface to perform common S3 operations such as:

- Creating S3 buckets
- Uploading single or multiple files to buckets
- Downloading files from buckets
- Listing bucket contents
- Deleting buckets

## Prerequisites

- Python 3.x
- Boto3 library
- AWS Account
- AWS Credentials

## Setup

1. Clone the repository:
```bash
git clone https://github.com/AmirKatorza/AWS_Boto3_S3_Automation.git
cd AWS_Boto3_S3_Automation
```

2. Install required dependencies:
```bash
pip install boto3
```

3. Create Credentials
Create a `credentials.py` file in the project root with the following structure:
```python
AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"
AWS_SESSION_TOKEN = "your_session_token"  # Optional, depends on your AWS setup
```

**Note:** Never commit your actual credentials to version control. Use environment variables or AWS CLI configuration for production use.

## How to Use

Run the application:
```bash
python app.py
```

### Menu Options

1. **Create S3 bucket**: Create a new S3 bucket by providing a unique bucket name.
2. **Upload a single file**: Choose a file from your local system to upload to a selected S3 bucket.
3. **Upload multiple files**: Select a directory to upload all files from that directory to a chosen S3 bucket.
4. **Download File**: Select a file from a bucket to download to a local directory.
5. **List files**: View all files in a selected S3 bucket.
6. **Delete a bucket**: Remove an existing S3 bucket (with option to delete non-empty buckets).
7. **Quit**: Exit the application.

## Important Security Notes

- Always protect your AWS credentials
- Use IAM roles and principles of least privilege
- Consider using AWS IAM users with restricted permissions for this tool

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## License

This project is licensed under the MIT License.
