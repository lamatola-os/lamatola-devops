import boto3
ec2 = boto3.resource('ec2')

from pick import pick
import base64
import os
import hashlib

def get_name(instance):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return "unknown"

instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

ssh_vms = []
vms = []

for instance in instances:
    # print(get_name(instance).ljust(50), instance.private_ip_address.ljust(10))
    ssh_vm = 'ssh ' + instance.private_ip_address
    ssh_vms.append(get_name(instance) + ' > ' + ssh_vm)
    vms.append(ssh_vm)

ssh_, index = pick(ssh_vms, "Select VM you want to ssh")

print(vms[index])
os.system(vms[index])
