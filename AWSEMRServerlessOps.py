import boto3
from botocore.exceptions import ClientError
import json
import pkg_resources

class AWSEMRServerlessOperations:
    def __init__(self) -> None:
        print("AWSEMRServerlessOperations constructor called...")
        self.client = boto3.client("emr-serverless", region_name=boto3.session.Session().region_name)

    def create_application(self, apptype, releaselabel):
        print("Create application function called...")
        return self.client.create_application(
            releaseLabel=releaselabel,
            type=apptype,
            # clientToken='string',
        )

