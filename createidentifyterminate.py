import boto3


def create_instance():
    ec2_resource = boto3.resource('ec2')
    instances = ec2_resource.create_instances(ImageId='ami-6871a115',
                MinCount=1, MaxCount=3,InstanceType='t2.micro',
                SecurityGroupIds=['sep06'],KeyName='fullstack')
    instance_ids = []
    for instance in instances:
        instance_ids.append(instance.id)
    ec2_client = boto3.client('ec2')
    waiter=ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=instance_ids)
    print ( "Created Instances", instance_ids)

create_instance()




import boto3
from botocore.exceptions import ClientError


def prepare_instance_list():
    mylist = []
    ec2_resource = boto3.resource('ec2')
    instances = ec2_resource.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.id, instance.instance_type)
        mylist.append(instance.id)
    return mylist

def delete_instances(instance_list):
    ec2_client = boto3.client('ec2')
    try:
        ec2_client.terminate_instances(InstanceIds=instance_list,DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    ec2_client.terminate_instances(InstanceIds=instance_list,DryRun=False)

instance_list = prepare_instance_list()
if len(instance_list) !=0:
    print ( "Deleting Instances", instance_list)
    delete_instances(instance_list)
else:
    print ("No Instances to delete ")
