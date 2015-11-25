import boto3
from botocore.exceptions import ClientError
from time import sleep

def lambda_handler(event, context):
  ec2 = boto3.client('ec2')
  regions = ec2.describe_regions()['Regions']
  for r in regions:
    print 'Cleaning region %s' % (r['RegionName'])
    region_client = boto3.client('ec2', region_name=r['RegionName'])

    release_images = region_client.describe_images(
      Filters = [
        {
          'Name': 'owner-id',
          'Values': [ '933693344490' ],
        },
        {
          'Name': 'state',
          'Values': [ 'available', 'deregistered' ],
        }
      ]
    )['Images']
    
    build_images = region_client.describe_images(
      Filters = [
        {
          'Name': 'owner-id',
          'Values': [ '933693344490' ],
        },
        {
          'Name': 'state',
          'Values': [ 'available', 'deregistered' ],
        }
      ]
    )['Images']

    delete_images = []
    delete_images += sorted(release_images, key=lambda k: k['CreationDate'], reverse=True)[10:]
    delete_images += sorted(build_images, key=lambda k: k['CreationDate'], reverse=True)[10:]

    for d in delete_images:
      image_id = d['ImageId']
      print 'Deleteing image %s' % (image_id,)
      # TODO(greg): Only try to deregister if image is currently available
      if d['State'] == 'available':
        try:
          region_client.deregister_image(ImageId=image_id)
        except ClientError as e:
          print 'Exception when deregistering image: %s' % (e,)

      
      for bd in d['BlockDeviceMappings']:
        if 'Ebs' in bd:
          snap_id = bd['Ebs']['SnapshotId']
          if snap_id:
            try:
              print 'deleting snapshot %s' % (snap_id,)
              region_client.delete_snapshot(SnapshotId=snap_id)
            except ClientError as e:
              print 'Exception when deleting snapshot: %s' % (e,)

if __name__ == '__main__':
  lambda_handler({}, {})
