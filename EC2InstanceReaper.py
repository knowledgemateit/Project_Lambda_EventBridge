import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # 1. Find all running instances
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    
    # Extract just the Instance IDs into a list
    instance_ids = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])

    # 2. Stop the instances if any are found
    if instance_ids:
        print(f"Stopping instances: {instance_ids}")
        ec2.stop_instances(InstanceIds=instance_ids)
    else:
        print("No running instances found.")

    return {
        "status": "Success",
        "stopped_count": len(instance_ids)
    }
