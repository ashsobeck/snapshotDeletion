#!/usr/bin/python3

import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

regions = ['us-east-1']


def main():
    logger.info('event: ' + str())
    ec2 = None
    cfn = None
    inUseAmis = []
    toDeleteAmis = []
    toDeleteSnapshots = []
    toDeleteVolumes = []
    print('here')
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        cfn = boto3.client('cloudformation', region_name=region)
        for stack in cfn.describe_stacks()['Stacks']:
            for output in stack['Parameters']:
                if ('ImageId' in output['ParameterKey']):
                    inUseAmis.append(output['ParameterValue'])
        for image in ec2.describe_images(Owners=['self'])['Images']:
            if (image['ImageId'] not in inUseAmis):
                toDeleteAmis.append(image['ImageId'])

        for snapshot in ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']:
            for ami in toDeleteAmis:
                if ami in snapshot['Description']:
                    toDeleteSnapshots.append(
                        snapshot['SnapshotId'])

        for volume in ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']:
            for snapshot in toDeleteSnapshots:
                if snapshot in volume['SnapshotId']:
                    toDeleteVolumes.append(volume['VolumeId'])
    print(inUseAmis)
    print(toDeleteAmis)
    print(toDeleteSnapshots)
    print(toDeleteVolumes)

    print(len(toDeleteAmis))
    print(len(toDeleteSnapshots))
    print(len(toDeleteVolumes))


if __name__ == "__main__":
    main()
