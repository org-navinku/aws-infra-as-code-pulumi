
import pulumi
from pulumi_aws import s3
import boto3

s3 = boto3.client('s3')

for bucket in s3.list_buckets()['Buckets']:
    print(f'Found bucket: {bucket["Name"]}')

# Create an AWS resource (S3 Bucket)
# bucket = s3.BucketV2('my-bucket')

# Export the name of the bucket
# pulumi.export('bucket_name', bucket.id)
