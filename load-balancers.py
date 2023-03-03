import boto3
client = boto3.client('elb')

from pick import pick
import base64
import os
import hashlib

def get_name(instance):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return "unknown"

instances = client.describe_load_balancers()['LoadBalancerDescriptions']

ssh_vms = []
vms = []

for instance in instances:
    lb = instance['LoadBalancerName'] + " : " + instance['DNSName'] + ' : created on ' + str(instance['CreatedTime'])
    print(lb)
