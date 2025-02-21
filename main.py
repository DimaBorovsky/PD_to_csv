# import logging
import requests
import datetime
import csv
import os
from time import sleep
# import boto3
# from botocore.exceptions import ClientError
# import json


timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"pagerduty_incidents_{timestamp}.csv"
print(f"Saving data to: {csv_filename}")


url = "https://api.pagerduty.com/incidents"
auth = os.getenv("API_KEY")

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Token token={auth}"
}


now = datetime.datetime.utcnow()
since = (now - datetime.timedelta(hours=3)).isoformat() + "Z"
until = now.isoformat() + "Z"


params = {
    "statuses[]": ["acknowledged", "resolved", "triggered"],
    "since": since,
    "until": until,
    "sort_by": "created_at:desc",
    "include[]": ["assignees", "services", "teams"]

}


incident_data = []

while True:
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        incidents = response.json().get("incidents", [])
        print(f"Number of alerts: {len(incidents)}")

        for incident in incidents:
            incident_number = incident.get("number")
            incident_id = incident.get("id")
            status = incident.get("status")
            created_at = incident.get("created_at")
            title = incident.get("title", "N/A")
            assignees = incident.get("assignments", [])
            teams = incident.get("teams", [])
            updated_at = incident.get("updated_at")
            service_name = incident.get("service", {}).get("summary", "id")
            priority = incident.get("priority", [])

            priority_level = priority["id"]["summary"]
            for pl in priority:
                if "summary" and "id" in pl:
                    print("")

            assignee_names = [
                assignment["assignee"]["summary"]
                for assignment in assignees
                if "assignee" in assignment
            ]

            team_names = [
                team["summary"]
                for team in teams if team.get("summary") == "NOC Level 1"
            ]

            # Fetch incident notes
            fetch_notes_url = f"https://api.pagerduty.com/incidents/{incident_id}/notes"
            fetch_comment = requests.get(fetch_notes_url, headers=headers)

            notes_text = []
            if fetch_comment.status_code == 200:
                notes = fetch_comment.json().get("notes", [])
                notes_text = [note.get("content", "No content") for note in notes]

            fetch_log_url = f"https://api.pagerduty.com/incidents/{incident_id}/log_entries"
            fetch_log = requests.get(fetch_log_url, headers=headers)

            resolver = "Unknown"
            if fetch_log.status_code == 200:
                log_entries = fetch_log.json().get("log_entries", [])
                for log in log_entries:
                    if log.get("type") == "resolve":
                        resolver = log.get("agent", {}).get("summary", "Unknown")
                        break

            # Append data
            incident_data.append([
                incident_id, status, created_at, updated_at, title,
                ", ".join(assignee_names) if assignee_names else "No assignees",
                service_name,
                "; ".join(notes_text) if notes_text else "No notes",
                resolver, priority
            ])

        sleep(4)

        more_incidents = response.json().get("more", False)
        if not more_incidents:
            break
        params["offset"] = params.get("offset", 0) + 25

    else:
        print(f"Failed to fetch incidents. Status Code: {response.status_code}")
        print(f"Error: {response.text}")
        break


file_exists = os.path.exists(csv_filename)

with open(csv_filename, mode="w+" if file_exists else "w+", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header only if the file is new
    if not file_exists:
        csv_writer.writerow(["Incident ID", "Status", "Created At", "Updated At",
                             "Title", "Assignees", "Service", "Notes", "Priority"])

    csv_writer.writerows(incident_data)

# Verify file creation
file_path = os.path.abspath(csv_filename)
if os.path.exists(file_path):
    print(f"Data successfully saved in: {file_path}")
else:
    print(f"Error: File not found at {file_path}")


# AWS S3 Configuration
# S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
# S3_BUCKET_PATH = os.getenv('S3_BUCKET_PATH')
# S3_BUCKET_REGION = os.getenv('S3_BUCKET_REGION')


# def create_bucket(bucket_name, region=None):
#     s3 = boto3.client('s3')
#     existing_buckets = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]
#
#     if bucket_name in existing_buckets:
#         print("Bucket already exists. No need to create, just upload the file.")
#         return True
#
#     try:
#         if region is None:
#             s3.create_bucket(Bucket=bucket_name)
#         else:
#             location = {'LocationConstraint': region}
#             s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
#         print(f"Bucket '{bucket_name}' created successfully.")
#         bucket_policy = {
#             'Version': '2012-10-17',
#             'Statement': [{
#                 'Sid': 'AddPerm',
#                 'Effect': 'Allow',
#                 'Principal': '*',
#                 'Action': ['s3:GetObject'],
#                 'Resource': f'arn:aws:s3:::{bucket_name}/*'
#             }]
#         }
#         bucket_policy = json.dumps(bucket_policy)
#         s3 = boto3.client('s3')
#         s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
#     except ClientError as e:
#         logging.error(e)
#         return False
#
#     return True
#
#
# def upload_to_s3(file_name, bucket_name, object_name=None):
#     """Upload data to S3"""
#     if object_name is None:
#         object_name = os.path.basename(csv_filename)
#
#     s3_client = boto3.client('s3')
#     try:
#         s3_client.upload_file(file_name, bucket_name, object_name)
#     except ClientError as er:
#         logging.error(er)
#         return False
#     return True
#
#
# create_bucket(S3_BUCKET_NAME, S3_BUCKET_REGION)
# upload_to_s3(csv_filename, S3_BUCKET_NAME, S3_BUCKET_PATH)
