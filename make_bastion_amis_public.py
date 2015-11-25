import boto3
from botocore.exceptions import ClientError
from time import sleep

def lambda_handler(event, context):
  ec2 = boto3.client('ec2')
  regions = ec2.describe_regions()['Regions']
  for r in regions:
    print 'Publishing bastion AMIs %s' % (r['RegionName'])
    region_client = boto3.client('ec2', region_name=r['RegionName'])

    images = region_client.describe_images(
      Filters = [
        {
          'Name': 'owner-id',
          'Values': [ '933693344490' ],
        },
        {
          'Name': 'state',
          'Values': [ 'available' ],
        },
        {
          'Name': 'is-public',
          'Values': [ 'false' ],
        },
      ]
    )['Images']
    
    images = sorted(images, key=lambda k: k['CreationDate'], reverse=True)

    for d in images:
      image_id = d['ImageId']
      print 'Publishing image %s' % (image_id,)
      if d['State'] == 'available':
        try:
          region_client.modify_image_attribute(
            ImageId = image_id,
            Attribute = 'launchPermission',
            OperationType = 'add',
            LaunchPermission={
              'Add': [
                {
                  'Group': 'all',
                },
              ],
            }
          )
        except ClientError as e:
          print 'Exception when publishing image: %s' % (e,)

if __name__ == '__main__':
  lambda_handler({}, {})
