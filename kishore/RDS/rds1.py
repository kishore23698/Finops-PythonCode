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

        instances = response['DBInstances']

        for instance in instances:
            instance_identifier = instance['DBInstanceIdentifier']
            instance_class = instance['DBInstanceClass']
            
            # Retrieve CPU utilization for the instance
            cpu_utilization = get_cpu_utilization(rds_client_region, instance_identifier)
            
            print(f"  Instance ID: {instance_identifier}")
            print(f"    Instance Type: {instance_class}")
            print(f"    CPU Utilization: {cpu_utilization}%")
            print("-" * 40)

def get_cpu_utilization(rds_client, instance_identifier):
    # Get CPU utilization metrics from Amazon CloudWatch
    response = rds_client.get_metric_statistics(
        MetricName='CPUUtilization',
        Namespace='AWS/RDS',
        Period=300,  # 5-minute intervals
        StartTime='2023-08-01T00:00:00Z',  # Adjust the start time as needed
        EndTime='2023-08-15T00:00:00Z',    # Adjust the end time as needed
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance_identifier}],
        Statistics=['Average']
    )
    
    if 'Datapoints' in response:
        datapoints = response['Datapoints']
        if datapoints:
            # CPU utilization values are returned in percentages
            avg_cpu_utilization = datapoints[-1]['Average']
            return avg_cpu_utilization
    return "N/A"

if __name__ == "__main__":
    get_rds_details()
