import boto3

# Initialize the Boto3 client for EC2
ec2_client = boto3.client('ec2')

def get_all_ebs_volumes():
    response = ec2_client.describe_volumes()
    return response['Volumes']

def get_ebs_volume_utilization(volume_id):
    cloudwatch_client = boto3.client('cloudwatch')
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/EBS',
        MetricName='VolumeReadBytes',
        Dimensions=[
            {
                'Name': 'VolumeId',
                'Value': volume_id
            },
        ],
        StartTime='2023-08-01T00:00:00Z',  # Adjust as needed
        EndTime='2023-08-18T00:00:00Z',    # Adjust as needed
        Period=86400,  # 1 day in seconds
        Statistics=['Average'],
        Unit='Bytes'
    )
    datapoints = response['Datapoints']
    if datapoints:
        return datapoints[0]['Average']
    return None

# Get all EBS volumes
ebs_volumes = get_all_ebs_volumes()

# Print volume details and utilization
for volume in ebs_volumes:
    volume_id = volume['VolumeId']
    utilization = get_ebs_volume_utilization(volume_id)
    print(f"Volume ID: {volume_id}")
    print(f"Size: {volume['Size']} GB")
    print(f"Utilization: {utilization} Bytes/day")  # Adjust units as needed
    print("-----")
