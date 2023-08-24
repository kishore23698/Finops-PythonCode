import boto3
import sys
from datetime import datetime, timedelta

# Check if the 'n' argument is provided
if len(sys.argv) != 2:
    print("Usage: python list_s3_bucket_info.py <n>")
    sys.exit(1)

try:
    # Get the value of 'n' from command-line argument
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
        total_size = 0
        last_modified = None

        if 'Contents' in bucket_objects:
            for obj in bucket_objects['Contents']:
                storage_class = obj['StorageClass']
                total_size += obj['Size']
                if last_modified is None or obj['LastModified'] > last_modified:
                    last_modified = obj['LastModified']
                # Get object storage class
                # object_info = s3_client.head_object(Bucket=bucket_name, Key=obj['Key'])
                #storage_class = bucket_details.get('Contents', [{}])[0].get('StorageClass', 'N/A')
                # storage_class = object_info['StorageClass']

        # Convert last modified date to a readable format without time
        formatted_last_modified = last_modified.strftime(
            '%Y-%m-%d') if last_modified else 'N/A'
        if formatted_last_modified < date:

            print("Bucket:", bucket_name)
            print("Total Storage Size (Bytes):", total_size)
            print("Last Modified Date:", formatted_last_modified)
            print("Storage Class:", storage_class)
            print()
    except Exception as e:
        print("Error:", e)
