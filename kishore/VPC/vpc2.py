import boto3


def get_vpc_details():
    # Create a Boto3 client for the Amazon EC2 service
    ec2_client = boto3.client('ec2')

    # Retrieve information about all VPCs
    response = ec2_client.describe_vpcs()

    vpcs = response['Vpcs']

    for vpc in vpcs:
        vpc_id = vpc['VpcId']
        cidr_block = vpc['CidrBlock']
        state = vpc['State']
        print(f"VPC ID: {vpc_id}, CIDR Block: {cidr_block}, State: {state}")

    

        # Check if the VPC has associated resources
        associated_resources = check_associated_resources(ec2_client, vpc_id)

        if associated_resources:
            print("Associated resources:")
            for resource_type, resource_data in associated_resources.items():
                print(f"  {resource_type}: {resource_data['count']}")

                if 'subnets' in resource_data:
                    print("    Subnet IDs:")
                    for subnet_id in resource_data['subnets']:
                        print(f"      {subnet_id}")

                if 'instances' in resource_data:
                    print("    Instance IDs:")
                    for instance_id in resource_data['instances']:
                        print(f"      {instance_id}")
        else:
            print("No associated resources found.")

        print("-" * 40)


def check_associated_resources(ec2_client, vpc_id):
    associated_resources = {}

    # Check for associated subnets
    response = ec2_client.describe_subnets(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    subnet_count = len(response['Subnets'])
    if subnet_count > 0:
        associated_resources['Subnets'] = {'count': subnet_count, 'subnets': [
            subnet['SubnetId'] for subnet in response['Subnets']]}

    # Check for associated instances
    response = ec2_client.describe_instances(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    instance_count = sum(len(reservations['Instances'])
                         for reservations in response['Reservations'])
    if instance_count > 0:
        associated_resources['Instances'] = {'count': instance_count, 'instances': [
            instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]}

    # Add checks for other resource types as needed (e.g., security groups, route tables, etc.)

    return associated_resources


if __name__ == "__main__":
    get_vpc_details()
