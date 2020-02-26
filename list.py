import boto3
ec2 = boto3.resource('ec2')

def get_name(instance):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return "unknown"

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    print(get_name(instance).ljust(50), instance.private_ip_address.ljust(10))

