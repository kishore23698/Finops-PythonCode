import boto3

# Initialize ECS client
ecs_client = boto3.client('ecs')

# List all ECS clusters
response = ecs_client.list_clusters()

for cluster_arn in response['clusterArns']:
    cluster_name = cluster_arn.split('/')[-1]
    print("Cluster:", cluster_name)

    # List all services in the cluster
    services_response = ecs_client.list_services(cluster=cluster_name)

    for service_arn in services_response['serviceArns']:
        service_name = service_arn.split('/')[-1]
        print("Service:", service_name)

        # Describe the service to get detailed information
        service_details = ecs_client.describe_services(cluster=cluster_name, services=[service_name])

        if 'services' in service_details and len(service_details['services']) > 0:
            service = service_details['services'][0]
            print("Status:", service['status'])
            print("Desired Count:", service['desiredCount'])
            print("Running Count:", service['runningCount'])
            print("Pending Count:", service['pendingCount'])
            print("Task Definition:", service['taskDefinition'])
            print("Created At:", service['createdAt'])
            print("Last Updated At:", service['updatedAt'])

        print()
