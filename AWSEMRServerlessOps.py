import boto3
from botocore.exceptions import ClientError
import json
import pkg_resources

class AWSEMRServerlessOperations:
    def __init__(self) -> None:
        print("AWSEMRServerlessOperations constructor called...")
        self.client = boto3.client("emr-serverless", region_name=boto3.session.Session().region_name)

    def emr_serverless_list_applications(self):
        return self.client.list_applications(
            states=[
                'CREATING','CREATED','STARTING','STARTED','STOPPING','STOPPED','TERMINATED'
            ]
        )
    def emr_serverless_delete_application(self, appId: str):
        return self.client.delete_application(
            applicationId=appId
        )

    def emr_serverless_create_application(self, appname: str, apptype: str, releaselabel: str):
        print("Create application function called...")
        return self.client.create_application(
            name=appname,
            releaseLabel=releaselabel,
            type=apptype,
            initialCapacity={
                'DRIVER': {
                    'workerCount': 1,
                    'workerConfiguration': {
                        'cpu': '2vCPU',
                        'memory': '4GB'
                    }
                },
                'EXECUTOR': {
                    'workerCount': 2,
                    'workerConfiguration': {
                        'cpu': '4vCPU',
                        'memory': '8GB'
                    }
                }
            },
            maximumCapacity={
                'cpu': '400vCPU',
                'memory': '1024GB'
            },
            tags={
                'Contact': 'Vikram',
                'Environment': 'Testing'
            },
            autoStartConfiguration={
                'enabled': True
            },
            autoStopConfiguration={
                'enabled': True,
                'idleTimeoutMinutes': 10
            }
        )

