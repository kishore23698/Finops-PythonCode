import boto3
import sys
from datetime import datetime, timedelta

# Check if the 'n' argument is provided
if len(sys.argv) != 2:
    print("Usage: python list_s3_bucket_info.py <n>")
    sys.exit(1)

try:
    # Get the value of 'n' from the command-line argument
    n = int(sys.argv[1])
except ValueError:
    print("Error: Invalid 'n' value")
    sys.exit(1)

# Initialize S3 client
s3_client = boto3.client('s3')

three_days_ago = datetime.now() - timedelta(days=n)
date = three_days_ago.strftime('%Y-%m-%d')

# Get list of all S3 buckets
response = s3_client.list_buckets()

for bucket in response['Buckets']:
    bucket_name = bucket['Name']

    try:
        # Get bucket size and last modified date
        bucket_objects = s3_client.list_objects_v2(Bucket=bucket_name)
        total_size_bytes = 0
        last_modified = None

        if 'Contents' in bucket_objects:
            for obj in bucket_objects['Contents']:
                total_size_bytes += obj['Size']
                if last_modified is None or obj['LastModified'] > last_modified:
                    last_modified = obj['LastModified']
        
        # Convert total size from bytes to megabytes
        total_size_mb = total_size_bytes / (1024 * 1024)

        # Convert last modified date to a readable format without time
        formatted_last_modified = last_modified.strftime(
            '%Y-%m-%d') if last_modified else 'N/A'

        if formatted_last_modified < date:
            print("Bucket:", bucket_name)
            print("Total Storage Size (MB):", total_size_mb)
            print("Last Modified Date:", formatted_last_modified)
            print()
    except Exception as e:
        print("Error:", e)
