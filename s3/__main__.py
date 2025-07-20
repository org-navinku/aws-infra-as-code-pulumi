import boto3
import pulumi
from pulumi_aws import s3
from pulumi import Config

config = Config()
bucket_name = config.require("bucket-name")
region = config.get("region") or "us-east-2"

bucket = s3.Bucket("ai-data-bucket",
    bucket=bucket_name,
    acl="private",
    tags={
        "ManagedBy": "Pulumi",
        "CostCenter": "ai-research"
    }
)

def configure_bucket_lifecycle(bucket_name_value):
    s3_client = boto3.client('s3', region_name=region)
    
    lifecycle_config = {
        'Rules': [
            {
                'ID': 'transition-to-ia-boto3',
                'Status': 'Enabled',
                'Filter': {
                    'Prefix': ''  # Apply to all objects
                },
                'Transitions': [
                    {
                        'Days': 1,  # Transition objects to Infrequent Access after 1 day
                        'StorageClass': 'GLACIER_IR'
                    }
                ]
            }
        ]
    }
    
    try:
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name_value,
            LifecycleConfiguration=lifecycle_config
        )
        print(f"Lifecycle policy applied to bucket: {bucket_name_value}")
    except Exception as e:
        print(f"Error applying lifecycle policy: {e}")

bucket.id.apply(configure_bucket_lifecycle)

pulumi.export("bucket_arn", bucket.arn)
pulumi.export("bucket_name", bucket.id)