import pulumi
from pulumi_aws import s3
import boto3
from pulumi import Config

# Configuration
config = Config()
bucket_name = config.require("bucket-name")
region = config.get("region") or "us-east-2"

# 1. Pulumi-managed bucket (primary infrastructure)
bucket = s3.Bucket("ai-data-bucket",
    bucket=bucket_name,
    acl="private",
    tags={
        "ManagedBy": "Pulumi",
        "CostCenter": "ai-research"
    }
)

# 2. Boto3 for operations handle
def configure_bucket(bucket_name):
    s3_client = boto3.client('s3', region_name=region)
    
    try:
        # Example: Enable intelligent tiering
        s3_client.put_bucket_intelligent_tiering_configuration(
            Bucket=bucket_name,
            Id="ai-data-tiering",
            IntelligentTieringConfiguration={
                'Status': 'Enabled',
                'Tierings': [
                    {
                        'Days': 1,
                        'AccessTier': 'ARCHIVE_ACCESS'
                    }
                ]
            }
        )
        print(f"Configured tiering for {bucket_name}")
    except Exception as e:
        print(f"Boto3 operation failed: {str(e)}")

# 3. Register post-creation callback
bucket.id.apply(configure_bucket)

# Export
pulumi.export("bucket_arn", bucket.arn)