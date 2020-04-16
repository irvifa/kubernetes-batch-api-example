from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from api.exceptions import BatchApiNamespaceNotExistedException

class Constants:
    BACKOFF_LIMIT = 1
    STATUS_RUNNING = "RUNNING"
    STATUS_SUCCEED = "SUCCEED"
    STATUS_FAILED = "FAILED"
    STATUS_NOT_FOUND = "NOT FOUND"

class KubernetesApi:
    def __init__(self):
        try:
            config.load_incluster_config()
        except:
            config.load_kube_config()
        self.configuration = client.Configuration()
        self.api_instance = client.BatchV1Api(client.ApiClient(self.configuration))
        self.api_instance_v1_beta = client.BatchV1beta1Api(client.ApiClient(self.configuration))

    def get_job_status(self, job):
        if job is not None:
            total_failed_pod = job.status.failed or 0
            total_succeeded_pod = job.status.succeeded or 0
            if total_failed_pod + total_succeeded_pod < Constants.BACKOFF_LIMIT:
                return Constants.STATUS_RUNNING
            elif total_succeeded_pod > 0:
                return Constants.STATUS_SUCCEED
            return Constants.STATUS_FAILED
        return Constants.STATUS_NOT_FOUND

    def get_cron_job_status(self, namespace):
        try:
            cron_job_list = self.api_instance_v1_beta.list_namespaced_cron_job(namespace=namespace,
                                                                          watch=False)
        except ApiException as e:
            raise BatchApiNamespaceNotExistedException("Exception when calling BatchV1Api->list_namespaced_cron_job: %s\n" % e)

        for cron_job in cron_job_list.items:
            if cron_job.status.active is not None:
                for active_cron_job in cron_job.status.active:
                    print(active_cron_job.name)
                    job = self.api_instance.read_namespaced_job(namespace=namespace,
                                                            name=active_cron_job.name)
                    job_status = self.get_job_status(job)
                    return job_status, job

        return None, None
