import boto3

# Initialize S3 client
s3_client = boto3.client('s3')

# Get list of all S3 buckets
response = s3_client.list_buckets()

for bucket in response['Buckets']:
    bucket_name = bucket['Name']

    try:
        # Get bucket size and last modified date
        bucket_objects = s3_client.list_objects_v2(Bucket=bucket_name)
        total_size = 0
        last_modified_date = None

        if 'Contents' in bucket_objects:
            for obj in bucket_objects['Contents']:
                total_size += obj['Size']
                if last_modified_date is None or obj['LastModified'] > last_modified_date:
                    last_modified_date = obj['LastModified']

        print("Bucket:", bucket_name)
        print("Total Storage Size (Bytes):", total_size)
        print("Last Modified Date:", last_modified_date)
        print()
    except Exception as e:
        print("Error:", e)
