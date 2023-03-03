import boto3
## https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html
## https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html

from pick import pick
import base64
import os
import hashlib

session = boto3.session.Session(profile_name='XXXprod')
## ec2 = session.resource('ec2', region_name='us-west-2')
k8s = session.client('eks', region_name='us-east-1')

def get_db_connection(instance):
    dbName = instance.get('DBName', 'XXX')
    if instance['Engine'] == 'postgres':
        connect_db = 'psql -h ' + instance['Endpoint']['Address'] + ' -p ' + str(instance['Endpoint']['Port']) + ' -d ' + dbName + ' -U ' + instance['MasterUsername'] + ' -W '
    elif instance['Engine'] == 'mysqldb':
        connect_db = 'mysql -h ' + instance['Endpoint']['Address'] + ' -P ' + str(instance['Endpoint']['Port']) + ' -d ' + dbName + ' -u ' + instance['MasterUsername'] + ' -W '
    else:
        connect_db = 'XXX'
    return connect_db

instances = k8s.list_clusters()

ssh_vms = []
vms = []

dbs = instances['clusters']

for instance in dbs:
    c = instance
    ## https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.describe_cluster
    cluster_desc = k8s.describe_cluster(name=c)
    cd = cluster_desc['cluster']
    cd_desc = cd['name'] + ' v' + cd['version'] + ' : ' + cd['endpoint']

    nodes = k8s.list_nodegroups(
        clusterName=c
    )['nodegroups']

    node_names = "".join(list(map(lambda x: x + '\n', nodes)))
    
    for n in nodes:
        node_names = node_names + '               ' + n + '\n'
        ng = k8s.describe_nodegroup(
            clusterName=c,
            nodegroupName=n)['nodegroup']
        print('Size: ' + str(ng['diskSize']) + ' Gb')

    cd_desc2 = cd_desc + ' \n ' + node_names

    print(cd_desc2)

# ssh_, index = pick(ssh_vms, "Select database you want to connect...")

#print(vms[index])
# os.system(vms[index])
