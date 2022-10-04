import boto3

Available_emr_application_stats = ['CREATING','CREATED', 'STARTING', 'STARTED', 'STOPPING', 'STOPPED', 'TERMINATED']
Valid_emr_application_stats = ['CREATING','CREATED', 'STARTING', 'STARTED', 'STOPPING', 'STOPPED']

class AWSEMRServerlessOperations:
    def __init__(self) -> None:
        print("AWSEMRServerlessOperations constructor called...")
        self.client = boto3.client("emr-serverless", region_name=boto3.session.Session().region_name)

    def emr_serverless_list_applications(self):
        return self.client.list_applications(
            states=Valid_emr_application_stats
        )
    def emr_serverless_delete_application(self, appId: str):
        return self.client.delete_application(
            applicationId=appId
        )

    def emr_serverless_start_application(self, appId: str):
        return self.client.start_application(
            applicationId=appId
        )

    def emr_serverless_cancel_job_run(self, appId: str, jobId: str):
        return self.client.cancel_job_run(
            applicationId=appId,
            jobRunId=jobId
        )

    def emr_serverless_get_job_run(self, appId: str, jobId: str):
        return self.client.get_job_run(
            applicationId=appId,
            jobRunId=jobId
        )
    def emr_serverless_get_dashboard_for_job_run(self, appId: str, jobId: str):
        return self.client.get_dashboard_for_job_run(
            applicationId=appId,
            jobRunId=jobId
        )
    def emr_serverless_stop_application(self, appId: str):
        return self.client.stop_application(
            applicationId=appId
        )
    def emr_serverless_start_spark_job_run(self, jobrunname: str, appId: str, rolearn: str, entryPoint: str,entryPointArgs: str, sparkSubmitParameters: str,loguri: str, contact: str, environment: str, exectimeout: int):
        sparkSubmitconf = {
        'entryPoint': entryPoint,
        'entryPointArguments': [entryPointArgs],
        'sparkSubmitParameters': sparkSubmitParameters
        }
        return self.client.start_job_run(
            applicationId=appId,
            executionRoleArn=rolearn,
            jobDriver={
                'sparkSubmit': sparkSubmitconf
            },
            configurationOverrides={
                'monitoringConfiguration': {
                    "s3MonitoringConfiguration": {
                        "logUri": loguri
                    }
                }
            },
            tags={
                'Contact': contact,
                'Environment': environment
            },
            executionTimeoutMinutes=exectimeout,
            name=jobrunname
        )

    def emr_serverless_get_application_status(self, appId: str):
        return self.client.get_application(
            applicationId=appId
        )

    def emr_serverless_start_hive_job_run(self, appId: str):
        return self.client.start_job_run(
            applicationId=appId
        )


    # update_application does not care about networkConfiguration in this version
    def emr_serverless_update_application(self, appid: str, driver_init_worker_count: int, driver_init_vcpu: str, driver_init_memory: str, driver_init_disk: str, executor_init_worker_count: int, executor_init_vcpu: str, executor_init_memory:str, executor_init_disk: str, max_cpu: str, max_memory: str, autostart_enabled: bool, autostop_enabled: bool, autostop_idletimeout_in_mins:int):
        print("Update application function called...")
        return self.client.update_application(
            applicationId=appid,
            initialCapacity={
                'DRIVER': {
                    'workerCount': driver_init_worker_count,
                    'workerConfiguration': {
                        'cpu': driver_init_vcpu,
                        'memory': driver_init_memory,
                        'disk': driver_init_disk
                    }
                },
                'EXECUTOR': {
                    'workerCount': executor_init_worker_count,
                    'workerConfiguration': {
                        'cpu': executor_init_vcpu,
                        'memory': executor_init_memory,
                        'disk': executor_init_disk
                    }
                }
            },
            maximumCapacity={
                'cpu': max_cpu,
                'memory': max_memory
            },
            autoStartConfiguration={
                'enabled': autostart_enabled
            },
            autoStopConfiguration={
                'enabled': autostop_enabled,
                'idleTimeoutMinutes': autostop_idletimeout_in_mins
            }
        )

    def emr_serverless_create_application(self, appname: str, apptype: str, releaselabel: str, driver_init_worker_count: int, driver_init_vcpu: str, driver_init_memory: str, driver_init_disk: str, executor_init_worker_count: int, executor_init_vcpu: str, executor_init_memory:str, executor_init_disk: str, max_cpu: str, max_memory: str, autostart_enabled: bool, autostop_enabled: bool, autostop_idletimeout_in_mins:int, contact: str, environment: str):
        print("Create application function called...")
        return self.client.create_application(
            name=appname,
            type=apptype,
            releaseLabel=releaselabel,
            initialCapacity={
                'DRIVER': {
                    'workerCount': driver_init_worker_count,
                    'workerConfiguration': {
                        'cpu': driver_init_vcpu,
                        'memory': driver_init_memory,
                        'disk': driver_init_disk
                    }
                },
                'EXECUTOR': {
                    'workerCount': executor_init_worker_count,
                    'workerConfiguration': {
                        'cpu': executor_init_vcpu,
                        'memory': executor_init_memory,
                        'disk': executor_init_disk
                    }
                }
            },
            maximumCapacity={
                'cpu': max_cpu,
                'memory': max_memory
            },
            tags={
                'Contact': contact,
                'Environment': environment
            },
            autoStartConfiguration={
                'enabled': autostart_enabled
            },
            autoStopConfiguration={
                'enabled': autostop_enabled,
                'idleTimeoutMinutes': autostop_idletimeout_in_mins
            }
        )

