import boto3


def main():
    create_instance( 'ami-06116566' )
    running = get_running_instances()
    list_instances(running)
#    for instance in running:
#       describe_image(instance.image_id)

def get_running_instances():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    return instances

def create_instance( ami, i_type='m3.medium', count=1 ):
    ec2 = boto3.resource('ec2')
#    ec2.create_instances(ImageId=ami, InstanceType=i_type, MinCount=count, MaxCount=count)

def describe_images( amis ):
    for image in amis:
        describe_image(image)

def describe_image( ami ):
    ec2 = boto3.client('ec2')
    image_attr = ec2.describe_images(
        ImageIds=[ami]
    )
    print '{}, {}, {}, {}, {}, {}, root:{}({}), {}:'.format(ami,
        image_attr['Images'][0]['Name'],
        image_attr['Images'][0]['CreationDate'],
        image_attr['Images'][0]['Public'],
        image_attr['Images'][0]['Hypervisor'],
        image_attr['Images'][0]['Architecture'],
        image_attr['Images'][0]['RootDeviceType'],
        image_attr['Images'][0]['RootDeviceName'],
        )
    describe_volumes(image_attr['Images'][0]['BlockDeviceMappings'])

def describe_volumes( block_device_map ):
    for device_attrs in block_device_map:
        print "{}".format(device_attrs['DeviceName'])
        if 'Ebs' in device_attrs:
            ebs_attrs=device_attrs['Ebs']
            print "type:{}, {}, from:{}, encrypted:{} delete:{}".format(
                ebs_attrs['VolumeType'],
                ebs_attrs['VolumeSize'],
                ebs_attrs['SnapshotId'],
                ebs_attrs['Encrypted'],
                ebs_attrs['DeleteOnTermination']
                )

def list_instances( instances ):
    idx = 0
    for instance in instances:
        idx += 1
        print '{:4d}. {}, {}, {}, {}, st:\'{}\', sg:\'{}\', k:\'{}\', mon:{}, {} @ pub:(\'{}\', {}), priv:(\'{}\', {}) [{}]'.format(
            idx,
            instance.launch_time,
            instance.id,
            instance.image_id,
            instance.placement['AvailabilityZone'],
            instance.state['Name'],
            instance.security_groups[0]['GroupName'],
            instance.key_name,
            instance.monitoring['State'],
            instance.instance_type,
            instance.public_dns_name,
            instance.public_ip_address,
            instance.private_dns_name,
            instance.private_ip_address,
            instance.tags
            )

if __name__ == '__main__':
    main()
