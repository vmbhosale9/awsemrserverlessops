import boto3, botocore
import json
from AWSEMRServerlessOps import AWSEMRServerlessOperations

# CREATE EMR APPLICATION DEFAULTS
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

# JOB EXECUTION DEFAULTS
JOB_EXEC_TIMEOUT_IN_MINS = 15

def exception_handler(e):
    # exception to status code mapping goes here...
    status_code = 400
    return {
        'statusCode': status_code,
        'body': json.dumps(str(e))
    }

def env_details():
    print("Boto3 version being used is {}".format(boto3.__version__))
    print("BotoCore version being used is {}".format(botocore.__version__))
    print("Current AWS Region is {}".format(boto3.session.Session().region_name))

def delete_emr_serverless_app(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_delete_application(appId)

def start_emr_serverless_app(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_start_application(appId)

def stop_emr_serverless_app(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_stop_application(appId)

def get_emr_serverless_app_status(appId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_get_application_status(appId)

def emr_serverless_get_job_run(appId: str, jobrunId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_get_job_run(appId, jobrunId)

def emr_serverless_get_dashboard_for_job_run(appId: str, jobrunId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_get_dashboard_for_job_run(appId, jobrunId)

def emr_serverless_cancel_job_run(appId: str, jobrunId: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_cancel_job_run(appId, jobrunId)

def start_emr_serverless_job_run(jobrunname: str, appId: str, rolearn: str, entryPoint: str,entryPointArgs: str, sparkSubmitParameters: str,loguri: str, contact: str, environment: str, exectimeout: int):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_start_spark_job_run(jobrunname, appId, rolearn, entryPoint,entryPointArgs, sparkSubmitParameters,loguri, contact, environment, exectimeout)

def create_emr_serverless_app(appname: str, apptype: str, releaselabel: str, driver_init_worker_count: int, driver_init_vcpu: str, driver_init_memory: str, driver_init_disk: str, executor_init_worker_count: int, executor_init_vcpu: str, executor_init_memory:str, executor_init_disk:str, max_cpu:str, max_memory:str, autostart_enabled: bool, autostop_enabled: bool, autostop_idletimeout_in_mins: int, contact: str, environment: str):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_create_application(appname, apptype, releaselabel, driver_init_worker_count, driver_init_vcpu, driver_init_memory, driver_init_disk, executor_init_worker_count, executor_init_vcpu, executor_init_memory, executor_init_disk, max_cpu, max_memory, eval(autostart_enabled), eval(autostop_enabled), autostop_idletimeout_in_mins, contact, environment)

def update_emr_serverless_app(appid: str, driver_init_worker_count: int, driver_init_vcpu: str, driver_init_memory: str, driver_init_disk: str, executor_init_worker_count: int, executor_init_vcpu: str, executor_init_memory:str, executor_init_disk:str, max_cpu:str, max_memory:str, autostart_enabled: bool, autostop_enabled: bool, autostop_idletimeout_in_mins: int):
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_update_application(appid, driver_init_worker_count, driver_init_vcpu, driver_init_memory, driver_init_disk, executor_init_worker_count, executor_init_vcpu, executor_init_memory, executor_init_disk, max_cpu, max_memory, eval(autostart_enabled), eval(autostop_enabled), autostop_idletimeout_in_mins)


def list_emr_serverless_apps():
    AWSEMRSLOps = AWSEMRServerlessOperations()
    return AWSEMRSLOps.emr_serverless_list_applications()

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
                return exception_handler("contact needs to be defined else program will fail!")

            try:
                environment = requestparams['environment']
                print("I got environment")
            except:
                print("environment needs to be defined else program will fail!")
                return exception_handler("environment needs to be defined else program will fail!")

            try:
                responsedata = create_emr_serverless_app(appname, apptype, releaselabel,driver_init_worker_count,driver_init_vcpu,driver_init_memory,driver_init_disk,executor_init_worker_count,executor_init_vcpu,executor_init_memory,executor_init_disk, max_cpu, max_memory, autostart_enabled,autostop_enabled,autostop_idletimeout_in_mins,contact,environment)
                if not responsedata['applicationId']:
                    responsedata = "I am unable to create an EMR serverless application!"
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_update_app':
        print("Calling emr_serverless_update_app method!")
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']

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
                responsedata = update_emr_serverless_app(appid, driver_init_worker_count, driver_init_vcpu, driver_init_memory, driver_init_disk, executor_init_worker_count, executor_init_vcpu, executor_init_memory, executor_init_disk, max_cpu, max_memory, autostart_enabled,autostop_enabled,autostop_idletimeout_in_mins)
                if responsedata['ResponseMetadata']['HTTPStatusCode'] == 200:
                    responsedata = "EMR serverless application ID# {} has been successfully updated!".format(appid)
                else:
                    responsedata = "EMR serverless application ID# {} failed to update!".format(appid)
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_delete_app':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']
            print("Calling delete_emr_serverless_app method!")
            try:
                responsedata = delete_emr_serverless_app(appid)
                if not responsedata:
                    responsedata = "I failed to delete EMR serverless app with appid {}!".format(appid)
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_list_apps':
        print("Calling emr_serverless_list_apps method!")
        try:
            responsedata = list_emr_serverless_apps()
            applications = None
            if not responsedata['applications']:
                print("There are no EMR serverless applications!")
                applications = "There are no EMR serverless applications!"
                return exception_handler(applications)
            else:
                print("I do see EMR serverless applications!")
                print(responsedata['applications'])
                for app in responsedata['applications']:
                    print(app['name'])
                    if not applications:
                        applications = responsedata['applications'][0]['name']
                    else:
                        applications = applications + ", " + app['name']
                return {
                    'statusCode': 200,
                    'body': json.dumps(applications)
                }
        except Exception as e:
            return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_start_app':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            try:
                appid = requestparams['appid']
            except Exception as e:
                return exception_handler(e)

            print("Calling start_emr_serverless_apps method!")
            try:
                responsedata = start_emr_serverless_app(appid)
                if not responsedata:
                    responsedata = "I failed to start EMR serverless app with appid {}!".format(appid)
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_stop_app':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']
            print("Calling stop_emr_serverless_app method!")
            try:
                responsedata = stop_emr_serverless_app(appid)
                if not responsedata:
                    responsedata = "I failed to stop EMR serverless app with appid {}!".format(appid)
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_get_app_status':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            appid = requestparams['appid']
            print("Calling get_emr_serverless_app_status method!")
            try:
                responsedata = get_emr_serverless_app_status(appid)
                if not responsedata['application']['applicationId']:
                    responsedata = "I failed to get EMR serverless app status with appid {}!".format(appid)
                else:
                    responsedata = "EMR serverless app status with appid {} is {}".format(appid, responsedata['application']['state'])
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_start_job_run':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))

            try:
                jobtype = requestparams['jobtype']
            except Exception as e:
                return exception_handler("To start a job, I need jobtype, which is not passed, I can't proceed further!")

            if str(jobtype).casefold() == "spark":
                try:
                    jobrunname = requestparams['jobrunname']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need jobrunname, which is not passed, I can't proceed further!")

                try:
                    appid = requestparams['appid']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need appID, which is not passed, I can't proceed further!")

                try:
                    rolearn = requestparams['rolearn']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need rolearn, which is not passed, I can't proceed further!")

                try:
                    entryPoint = requestparams['entryPoint']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need job entryPoint, which is not passed, I can't proceed further!")

                try:
                    entryPointArguments = requestparams['entryPointArguments']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need job entryPointArguments, which is not passed, I can't proceed further!")

                try:
                    sparkSubmitParameters = requestparams['sparkSubmitParameters']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need job sparkSubmitParameters, which is not passed, I can't proceed further!")

                try:
                    loguri = requestparams['loguri']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need loguri to store logs, which is not passed, I can't proceed further!")

                try:
                    contact = requestparams['contact']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need job contact for accountability, which is not passed, I can't proceed further!")

                try:
                    environment = requestparams['environment']
                except Exception as e:
                    return exception_handler(
                        "To start a job, I need environment to run job, which is not passed, I can't proceed further!")

                try:
                    exectimeout = requestparams['exectimeout']
                    print("I got job execution timeout value of {}".format(exectimeout))
                except:
                    print("I cant see job execution timeout, setting the default value of {}!".format(
                        JOB_EXEC_TIMEOUT_IN_MINS))
                    exectimeout = JOB_EXEC_TIMEOUT_IN_MINS

                print("Calling start_emr_serverless_job_run method!")
                try:
                    responsedata = start_emr_serverless_job_run(jobrunname, appid, rolearn, entryPoint,
                                                                entryPointArguments, sparkSubmitParameters, loguri,
                                                                contact, environment, exectimeout)
                    if not responsedata['jobRunId']:
                        responsedata = "I failed to run EMR serverless app with appid {}!".format(appid)
                    return {
                        'statusCode': 200,
                        'body': json.dumps(responsedata)
                    }
                except Exception as e:
                    return exception_handler(e)
            elif str(jobtype).casefold() == "hive":
                print("MAJOR ERROR HIVE JOB NOT SUPPORTED YET - Human intervention is needed!")
                return exception_handler("MAJOR ERROR HIVE JOB NOT SUPPORTED YET - Human intervention is needed!")
            else:
                print("MAJOR ERROR Job Type not defined - Human intervention is needed!")
                return exception_handler("MAJOR ERROR Job Type not defined- Human intervention is needed!")
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_cancel_job_run':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            try:
                appid = requestparams['appid']
            except Exception as e:
                return exception_handler(e)

            try:
                jobrunid = requestparams['jobrunid']
            except Exception as e:
                return exception_handler(e)

            print("Calling emr_serverless_cancel_job_run method!")
            try:
                responsedata = emr_serverless_cancel_job_run(appid, jobrunid)
                if not responsedata:
                    responsedata = "I failed to cancel EMR serverless job run with appid {} & jobrunid {} !".format(appid, jobrunid)
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata, indent=4, sort_keys=True, default=str)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_get_dashboard_for_job_run':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            try:
                appid = requestparams['appid']
            except Exception as e:
                return exception_handler(e)

            try:
                jobrunid = requestparams['jobrunid']
            except Exception as e:
                return exception_handler(e)

            print("Calling emr_serverless_get_dashboard_for_job_run method!")
            try:
                responsedata = emr_serverless_get_dashboard_for_job_run(appid, jobrunid)
                if not responsedata:
                    responsedata = "I failed to get dashboard url for EMR serverless job with appid {} & jobrunid {} !".format(appid, jobrunid)
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata, indent=4, sort_keys=True, default=str)
                }
            except Exception as e:
                return exception_handler(e)
    elif event['httpMethod'] == 'POST' and event['path'] == '/emr_serverless_get_job_run':
        requestparams = json.loads(event['body'])
        if bool(requestparams):
            print("requestparams are: {}".format(requestparams))
            try:
                appid = requestparams['appid']
            except Exception as e:
                return exception_handler(e)

            try:
                jobrunid = requestparams['jobrunid']
            except Exception as e:
                return exception_handler(e)

            print("Calling emr_serverless_get_job_run method!")
            try:
                responsedata = emr_serverless_get_job_run(appid, jobrunid)
                if not responsedata:
                    responsedata = "I failed to get job run status for EMR serverless job with appid {} & jobrunid {} !".format(appid, jobrunid)
                return {
                    'statusCode': 200,
                    'body': json.dumps(responsedata, indent=4, sort_keys=True, default=str)
                }
            except Exception as e:
                return exception_handler(e)
    else:
        print("MAJOR ERROR - Human intervention is needed!")
        return exception_handler("MAJOR ERROR - Human intervention is needed!")