import boto3, botocore
import json
from AWSEMRServerlessOps import AWSEMRServerlessOperations

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def env_details():
    print("Boto3 version being used is {}".format(boto3.__version__))
    print("BotoCore version being used is {}".format(botocore.__version__))
    print("Current AWS Region is {}".format(boto3.session.Session().region_name))

def delete_emr_serverless_app(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_delete_application(appId)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"
def create_emr_serverless_app(appname: str, apptype: str, releaselabel: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_create_application(appname, apptype, releaselabel)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"

def list_emr_serverless_apps():
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_list_applications()
    return response

def lambda_handler(event, context):
    # TODO implement
    # create_emr_serverless_app("SPARK", "emr-6.7.0")
    print("1")
    print(event)
    env_details()
    print("2")
    responsedata = None
    if event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_create_app':
        print("Calling create_emr_serverless_app method!")
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appname = requestparams['appname']
            apptype = requestparams['apptype']
            releaselabel = requestparams['releaselabel']
            responsedata = create_emr_serverless_app(appname, apptype, releaselabel)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_delete_app':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appname = requestparams['appname']
            print("Calling delete_emr_serverless_app method!")
            responsedata = delete_emr_serverless_app(appname)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_list_apps':
        print("Calling emr_serverless_list_apps method!")
        responsedata = list_emr_serverless_apps()
    else:
        print("Something is not right!")
        responsedata = "Something is not right!"

    print(responsedata)
    if validateJSON(responsedata) == True:
        print("responsedata is a valid json")
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": responsedata
        }
    else:
        print("responsedata is not a valid json")
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "Response ": responsedata
            })
        }
