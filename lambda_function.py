import boto3, botocore
import json
from AWSEMRServerlessOps import AWSEMRServerlessOperations

RELEASELABEL = "emr-6.7.0"
APPTYPES = ['Spark', 'Hive']
DEFAULT_APPTYPE = "Spark"
DRIVER_INIT_WORKER_COUNT = 1
DRIVER_INIT_VCPU= "2vCPU"
DRIVER_INIT_MEMORY = "4GB"
DRIVER_INIT_DISK = "20GB"
EXECUTOR_INIT_WORKER_COUNT = 2
EXECUTOR_INIT_VCPU = "4vCPU"
EXECUTOR_INIT_MEMORY = "8GB"
EXECUTOR_INIT_DISK = "40GB"
MAX_CPU = "400vCPU"
MAX_MEMORY = "1024GB"
AUTOSTART_ENABLED = True
AUTOSTOP_ENABLED = True
AUTOSTOP_IDLETIMEOUT_IN_MINS = 10

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

def start_emr_serverless_app(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_start_application(appId)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"

def stop_emr_serverless_app(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_stop_application(appId)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"

def get_emr_serverless_app_status(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_get_application_status(appId)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"

def start_emr_serverless_job_run(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_start_spark_job_run(appId)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"

def create_emr_serverless_app(appname: str, apptype: str, releaselabel: str, driver_init_worker_count: int, driver_init_vcpu: str, driver_init_memory: str, driver_init_disk: str, executor_init_worker_count: int, executor_init_vcpu: str, executor_init_memory:str, executor_init_disk:str, max_cpu:str, max_memory:str, autostart_enabled: bool, autostop_enabled: bool, autostop_idletimeout_in_mins: int, contact: str, environment: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_create_application(appname, apptype, releaselabel, driver_init_worker_count, driver_init_vcpu, driver_init_memory, driver_init_disk, executor_init_worker_count, executor_init_vcpu, executor_init_memory, executor_init_disk, max_cpu, max_memory, eval(autostart_enabled), eval(autostop_enabled), autostop_idletimeout_in_mins, contact, environment)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return json.dumps(response)
    else:
        return "you are in trouble!"

def list_emr_serverless_apps():
    AWSEMRSLOps = AWSEMRServerlessOperations()
    response = AWSEMRSLOps.emr_serverless_list_applications()
    return response

def lambda_handler(event, context):
    env_details()
    responsedata = None
    if event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_create_app':
        print("Calling create_emr_serverless_app method!")
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appname = requestparams['appname']

            try:
                apptype = requestparams['apptype']
                if apptype not in APPTYPES:
                    print("Apptype has to be either Spark or Hive")
            except:
                print("I cant see Apptype, setting the default value of {}!".format(DEFAULT_APPTYPE))
                apptype = DEFAULT_APPTYPE

            try:
                releaselabel = requestparams['releaselabel']
                print("I got releaselabel")
            except:
                print("I cant see releaselabel, setting the default value of {}!".format(RELEASELABEL))
                releaselabel = RELEASELABEL

            try:
                driver_init_worker_count = requestparams['driver_init_worker_count']
                print("I got driver_init_worker_count")
            except:
                print("I cant see driver_init_worker_count, setting the default value of {}!".format(DRIVER_INIT_WORKER_COUNT))
                driver_init_worker_count = DRIVER_INIT_WORKER_COUNT

            try:
                driver_init_vcpu = requestparams['driver_init_vcpu']
                print("I got driver_init_vcpu")
            except:
                print("I cant see driver_init_vcpu, setting the default value of {}!".format(DRIVER_INIT_VCPU))
                driver_init_vcpu = DRIVER_INIT_VCPU

            try:
                driver_init_memory = requestparams['driver_init_memory']
                print("I got driver_init_memory")
            except:
                print("I cant see driver_init_memory, setting the default value of {}!".format(DRIVER_INIT_MEMORY))
                driver_init_memory = DRIVER_INIT_MEMORY

            try:
                driver_init_disk = requestparams['driver_init_disk']
                print("I got driver_init_disk")
            except:
                print("I cant see driver_init_disk, setting the default value of {}!".format(DRIVER_INIT_DISK))
                driver_init_disk = DRIVER_INIT_DISK

            try:
                executor_init_worker_count = requestparams['executor_init_worker_count']
                print("I got executor_init_worker_count")
            except:
                print("I cant see executor_init_worker_count, setting the default value of {}!".format(EXECUTOR_INIT_WORKER_COUNT))
                executor_init_worker_count = EXECUTOR_INIT_WORKER_COUNT

            try:
                executor_init_vcpu = requestparams['executor_init_vcpu']
                print("I got executor_init_vcpu")
            except:
                print("I cant see executor_init_vcpu, setting the default value of {}!".format(EXECUTOR_INIT_VCPU))
                executor_init_vcpu = EXECUTOR_INIT_VCPU

            try:
                executor_init_memory = requestparams['executor_init_memory']
                print("I got executor_init_memory")
            except:
                print("I cant see executor_init_memory, setting the default value of {}!".format(EXECUTOR_INIT_MEMORY))
                executor_init_memory = EXECUTOR_INIT_MEMORY

            try:
                executor_init_disk = requestparams['executor_init_disk']
                print("I got executor_init_disk")
            except:
                print("I cant see executor_init_disk, setting the default value of {}!".format(EXECUTOR_INIT_DISK))
                executor_init_disk = EXECUTOR_INIT_DISK

            try:
                max_cpu = requestparams['max_cpu']
                print("I got max_cpu")
            except:
                print("I cant see max_cpu, setting the default value of {}!".format(MAX_CPU))
                max_cpu = MAX_CPU

            try:
                max_memory = requestparams['max_memory']
                print("I got max_memory")
            except:
                print("I cant see max_memory, setting the default value of {}!".format(MAX_MEMORY))
                max_memory = MAX_MEMORY

            try:
                autostart_enabled = requestparams['autostart_enabled']
                print("I got autostart_enabled with value of {}".format(autostart_enabled))
            except:
                print("I cant see autostart_enabled, setting the default value of {}!".format(AUTOSTART_ENABLED))
                autostart_enabled = AUTOSTART_ENABLED

            try:
                autostop_enabled = requestparams['autostop_enabled']
                print("I got autostop_enabled with value of {}".format(autostop_enabled))
                try:
                    autostop_idletimeout_in_mins = requestparams['autostop_idletimeout_in_mins']
                except:
                    print("I cant see autostop_idletimeout_in_mins, setting the default value of {}!".format(AUTOSTOP_IDLETIMEOUT_IN_MINS))
                    autostop_idletimeout_in_mins = AUTOSTOP_IDLETIMEOUT_IN_MINS
            except:
                print("I cant see autostop_enabled, setting the default value of {}!".format(AUTOSTOP_ENABLED))
                autostop_enabled = AUTOSTOP_ENABLED
                autostop_idletimeout_in_mins = AUTOSTOP_IDLETIMEOUT_IN_MINS

            try:
                contact = requestparams['contact']
                print("I got contact")
            except:
                print("I cant see contact")
                responsedata = "contact needs to be defined else program will fail!"

            try:
                environment = requestparams['environment']
                print("I got environment")
            except:
                print("I cant see environment")
                responsedata = "environment needs to be defined else program will fail!"

            # responsedata = create_emr_serverless_app(appname, apptype, releaselabel,drive_init_worker_count,drive_init_vcpu,drive_init_memory,drive_init_disk)
            responsedata = create_emr_serverless_app(appname, apptype, releaselabel,driver_init_worker_count,driver_init_vcpu,driver_init_memory,driver_init_disk,executor_init_worker_count,executor_init_vcpu,executor_init_memory,executor_init_disk, max_cpu, max_memory, autostart_enabled,autostop_enabled,autostop_idletimeout_in_mins,contact,environment)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_delete_app':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            # appname = requestparams['appname']
            appid = requestparams['appid']
            print("Calling delete_emr_serverless_app method!")
            responsedata = delete_emr_serverless_app(appid)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_list_apps':
        print("Calling emr_serverless_list_apps method!")
        responsedata = list_emr_serverless_apps()
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_start_app':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']
            print("Calling start_emr_serverless_apps method!")
            responsedata = start_emr_serverless_app(appid)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_stop_app':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']
            print("Calling stop_emr_serverless_app method!")
            responsedata = stop_emr_serverless_app(appid)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_get_app_status':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']
            print("Calling get_emr_serverless_app_status method!")
            responsedata = get_emr_serverless_app_status(appid)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_start_job_run':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']
            print("Calling start_emr_serverless_job_run method!")
            responsedata = start_emr_serverless_job_run(appid)
    else:
        print("Something is not right!")
        responsedata = "Something is not right!"

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
