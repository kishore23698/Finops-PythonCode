#!/bin/bash

# List all AWS regions
regions=$(aws ec2 describe-regions --query "Regions[].RegionName" --output text)

# Header for the CSV file
echo "Region,InstanceId,InstanceType,State,CPUUtilization" > instance_utilization.csv

# Loop through each region
for region in $regions; do
    echo "Fetching CPU utilization in $region"

    # Fetch instance IDs in the region
    instance_ids=$(aws ec2 describe-instances --region $region --query "Reservations[].Instances[?State.Name=='running'].InstanceId" --output text)


    # Loop through each instance and fetch CPU utilization (replace 'SampleCount' with your desired metric)
    for instance_id in $instance_ids; do
        cpu_utilization=$(aws cloudwatch get-metric-statistics --region $region --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=$instance_id --start-time $(date -d '6 hours ago' -u +"%Y-%m-%dT%H:%M:%S") --end-time $(date -u +"%Y-%m-%dT%H:%M:%S") --period 3600 --statistics Average --unit Percent --query "Datapoints[0].Average"  --output text)

        instance_type=$(aws ec2 describe-instances --region $region --instance-ids $instance_id --query "Reservations[].Instances[].InstanceType" --output text)

        #Fetch state of instances
        state=$(aws ec2 describe-instances --region $region --instance-ids $instance_id  --query "Reservations[].Instances[].[State.Name]" --output text)


        echo "$region,$instance_id,$instance_type,$state,$cpu_utilization " >> instance_utilization.csv
    done
done

echo "Instance utilization details collected and saved in instance_utilization.csv"
