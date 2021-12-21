import boto3
ec2 = boto3.resource('ec2')
rds = boto3.client('rds')

from pick import pick
import base64
import os
import hashlib

def get_db_connection(instance):
    dbName = instance.get('DBName', 'XXX')
    if instance['Engine'] == 'postgres':
        connect_db = 'psql -h ' + instance['Endpoint']['Address'] + ' -p ' + str(instance['Endpoint']['Port']) + ' -d ' + dbName + ' -U ' + instance['MasterUsername'] + ' -W '
    elif instance['Engine'] == 'mysqldb':
        connect_db = 'mysql -h ' + instance['Endpoint']['Address'] + ' -P ' + str(instance['Endpoint']['Port']) + ' -d ' + dbName + ' -u ' + instance['MasterUsername'] + ' -W '
    else:
        connect_db = 'XXX'
    return connect_db

instances = rds.describe_db_instances()

ssh_vms = []
vms = []

dbs = instances['DBInstances']

for instance in dbs:
    dbName = instance.get('DBName', 'XXX')
    connect_db = get_db_connection(instance)
    c = instance['DBInstanceIdentifier'] + ' > ' + connect_db
    if connect_db != 'XXX':
        ssh_vms.append(instance['DBInstanceIdentifier'] + ' > ' + connect_db)
        vms.append(connect_db)
        print(c)

# ssh_, index = pick(ssh_vms, "Select database you want to connect...")

#print(vms[index])
# os.system(vms[index])
