import boto3

## https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#volume

from pick import pick
import base64
import os
import hashlib
import sys

PROFILE_NAME=''
for line in sys.stdin:
    if 'Exit' == line.rstrip():
        break
    PROFILE_NAME=line.rstrip()

session = boto3.session.Session(profile_name=PROFILE_NAME)
ec2 = session.resource('ec2', region_name='us-east-1')

volumes = ec2.volumes.all()
inuse_volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['in-use']}])

def get_name(instance):
    if(instance.tags):
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                return tag['Value']
            return "unknown 1"
    else:
        return "unknown 2"

ssh_vms = []
vms = []

for instance in inuse_volumes:
    print(get_name(instance))
    ssh_vm = instance.volume_id + ' | ' + str(instance.size) + ' | ' + instance.volume_type
    ssh_vms.append(ssh_vm)
    vms.append(ssh_vm)

for i in ssh_vms:
    print(i)
