# PD_to_csv
PagerDuty Incident Fetcher

Overview:
This script fetches incidents from PagerDuty within the last three hours and saves the data in a CSV file. It includes details such as:
status, timestamps, title, assignees, services, notes, and priority levels.
The script can optionally upload the CSV file to an AWS S3 bucket.

Disclaimer

I acknowledge that using Terraform for infrastructure management is the best practice. 
However, this script is intended as a quick solution for fetching and storing PagerDuty incidents and should not be considered a replacement for proper infrastructure-as-code management.

Features

Retrieves PagerDuty incidents based on status and timeframe.
Fetches additional incident details, including notes and resolution logs.
Saves incident data in a CSV file with a timestamped filename.
(Optional) Uploads the CSV file to an AWS S3 bucket (commented-out code).

Prerequisites:
Python 3.x
requests library (install with pip install requests)
(Optional) boto3 for AWS S3 uploads (install with pip install boto3)

Environment Variables:
The script requires the following environment variables:
API_KEY - Your PagerDuty API key.
(Optional) S3_BUCKET_NAME - The name of the AWS S3 bucket.
(Optional) S3_BUCKET_PATH - The path in the S3 bucket.
(Optional) S3_BUCKET_REGION - The AWS region for the S3 bucket.

Usage:
Set up the required environment variables.
Run the script:
python script.py
The script will output the CSV file location after execution.

CSV Output Format
The generated CSV file contains the following columns:
Incident ID
Status
Created At
Updated At
Title
Assignees
Service
Notes
Resolver
Priority

AWS S3 Integration (Optional)

The script includes commented-out code for uploading the CSV file to an AWS S3 bucket. To enable this feature:
Install boto3 using pip install boto3.
Uncomment the relevant sections in the script.
Ensure AWS credentials are configured properly using aws configure or environment variables.

Notes:
The script makes multiple API calls to fetch incident data, handling pagination automatically.
It respects API rate limits by adding a delay between requests.
Only incidents from the last three hours are retrieved.
The AWS S3 upload feature is currently disabled by default.

Disclaimer 
