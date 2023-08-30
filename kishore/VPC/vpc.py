import boto3

# Create a Boto3 client for EC2 (VPC)
ec2_client = boto3.client('ec2')

# Retrieve details about all VPCs
response = ec2_client.describe_vpcs()

# Extract and print VPC details
for vpc in response['Vpcs']:
    vpc_id = vpc['VpcId']
    cidr_block = vpc['CidrBlock']
    state = vpc['State']
    print(f"VPC ID: {vpc_id}, CIDR Block: {cidr_block}, State: {state}")
