import boto3

def get_rds_details():
    # Create a Boto3 client for the Amazon RDS service
    rds_client = boto3.client('rds')

    # Get a list of all available AWS regions
    regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    for region in regions:
        print(f"Region: {region}")

        # Create a Boto3 client for the Amazon RDS service in the current region
        rds_client_region = boto3.client('rds', region_name=region)

        # Retrieve information about all RDS instances in the current region
        response = rds_client_region.describe_db_instances()

        db_instances = response['DBInstances']

        for instance in db_instances:
            instance_identifier = instance['DBInstanceIdentifier']
            instance_type = instance['DBInstanceClass']

            print(f"  Instance ID: {instance_identifier}")
            print(f"    Instance Type: {instance_type}")

            # Retrieve CPU utilization metric from CloudWatch
            cpu_utilization = get_cpu_utilization(instance_identifier, region)
            if cpu_utilization is not None:
                print(f"    CPU Utilization: {cpu_utilization}%")
            else:
                print("    CPU Utilization data not available")

            # Retrieve and print database connection details
            endpoint = instance.get('Endpoint')
            if endpoint:
                print(f"    Endpoint: {endpoint['Address']}:{endpoint['Port']}")
                print(f"    Username: {instance['MasterUsername']}")
                print(f"    Database Engine: {instance['Engine']}")
                print(f"    Engine Version: {instance['EngineVersion']}")
            else:
                print("    Database connection details not available")

            print("-" * 40)

def get_cpu_utilization(instance_identifier, region):
    # Create a Boto3 client for the Amazon CloudWatch service
    cloudwatch_client = boto3.client('cloudwatch', region_name=region)

    # Retrieve CPU utilization metric from CloudWatch
    response = cloudwatch_client.get_metric_statistics(
        MetricName='CPUUtilization',
        Namespace='AWS/RDS',
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_identifier}],
        StartTime='2023-01-01T00:00:00Z',  # Specify an appropriate start time
        EndTime='2023-08-21T00:00:00Z',    # Specify an appropriate end time
        Period=86400,  # Change the period to 24 hours (86400 seconds)
        Statistics=['Average']
    )

    if 'Datapoints' in response:
        datapoint = response['Datapoints'][0]
        return datapoint['Average']
    else:
        return None

if __name__ == "__main__":
    get_rds_details()
