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

Jenkins Pipeline for PD Incident Report

Overview
This Jenkins pipeline automates the process of fetching incident reports, generating a CSV file, and notifying relevant teams via Slack and email.

Stages:
Pull Repository: Cleans the workspace and checks out the latest code from SCM.
Prepare Environment: Sets up necessary environment variables and installs dependencies.
Run Script: Executes the Python script to generate the incident report.
Handle CSV File: Moves the generated CSV file to a predefined location.
Verify CSV File: Ensures the CSV file exists before proceeding.
Send Email: Sends an email with the report attached.
Slack Notification & Upload: Sends a Slack message and uploads the CSV file.

Configuration:
Jenkins Node: Update node('your-node-label') with the appropriate Jenkins agent label.
Paths: Replace path/to/requirements.txt and path/to/main.py with actual paths.
Slack Channel: Set the correct Slack channel in def channel = '#your-slack-channel'.
Email Recipient: Update TO=receiver@example.com with the desired recipient.

Dependencies:
Python 3
Required Python packages (defined in requirements.txt)
Jenkins plugins: Slack Notification, Email Extension

Notes:
Ensure that the workspace has the correct permissions to execute scripts and move files.
Modify environment variables as needed to match your setup.
