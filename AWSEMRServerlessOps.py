import boto3
from botocore.exceptions import ClientError
import json
import pkg_resources
# Testing

aws_region = boto3.session.Session().region_name


class AWSEMRServerlessOperations:
    def __init__(self) -> None:
        print("AWSEMRServerlessOperations constructor called...")
        self.client = boto3.client("emr-serverless", region_name=aws_region)

    def create_application(self, apptype, releaselabel):
        print("Create application function called...")
        return self.client.create_application(
            releaseLabel=releaselabel,
            type=apptype,
            # clientToken='string',
        )

