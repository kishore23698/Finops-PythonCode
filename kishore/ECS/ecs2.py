import boto3

# Initialize ECS and CloudWatch clients
ecs_client = boto3.client('ecs')
cloudwatch_client = boto3.client('cloudwatch')

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

            # Get Network Transmit (tx) and Receive (rx) Metrics from Container Insights
            network_metric_names = ["NetworkRxBytes", "NetworkTxBytes"]
            namespace = "ECS/ContainerInsights"
            dimensions = [
                {
                    "Name": "ClusterName",
                    "Value": cluster_name
                },
                {
                    "Name": "ServiceName",
                    "Value": service_name
                }
            ]

            for metric_name in network_metric_names:
                response = cloudwatch_client.get_metric_data(
                    MetricDataQueries=[
                        {
                            "Id": "network_metrics",
                            "MetricStat": {
                                "Metric": {
                                    "Namespace": namespace,
                                    "MetricName": metric_name,
                                    "Dimensions": dimensions
                                },
                                "Period": 3600,
                                "Stat": "Average"
                            },
                        }
                    ],
                    StartTime="2023-08-28T00:00:00Z",
                    EndTime="2023-08-29T00:00:00Z",
                )

                if 'MetricDataResults' in response:
                    for metric_data in response['MetricDataResults']:
                        values = metric_data.get('Values', [])
                        if values:
                            print(f"{metric_name} - Average:", values[0])
                        else:
                            print(f"{metric_name} - No data available")

            # Get CPU and Memory Utilization Metrics from Container Insights
            utilization_metric_names = ["CpuUtilized", "MemoryUtilized"]

            for metric_name in utilization_metric_names:
                response = cloudwatch_client.get_metric_data(
                    MetricDataQueries=[
                        {
                            "Id": "utilization_metrics",
                            "MetricStat": {
                                "Metric": {
                                    "Namespace": namespace,
                                    "MetricName": metric_name,
                                    "Dimensions": dimensions
                                },
                                "Period": 3600,
                                "Stat": "Average"
                            },
                        }
                    ],
                    StartTime="2023-08-28T00:00:00Z",
                    EndTime="2023-08-29T00:00:00Z",
                )

                if 'MetricDataResults' in response:
                    for metric_data in response['MetricDataResults']:
                        values = metric_data.get('Values', [])
                        if values:
                            print(f"{metric_name} - Average:", values[0])
                        else:
                            print(f"{metric_name} - No data available")

        print()
