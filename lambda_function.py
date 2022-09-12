import boto3, botocore
import json
from AWSEMRServerlessOps import AWSEMRServerlessOperations


def env_details():
    print("Boto3 version being used is {}".format(boto3.__version__))
    print("BotoCore version being used is {}".format(botocore.__version__))
    print("Current AWS Region is {}".format(boto3.session.Session().region_name))


def create_emr_serverless_app(apptype, releaselabel):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.create_application(apptype, releaselabel)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"


def lambda_handler(event, context):
    # TODO implement
    # create_emr_serverless_app("SPARK", "emr-6.7.0")
    env_details()
    create_emr_serverless_app("SPARK", "emr-6.7.0")