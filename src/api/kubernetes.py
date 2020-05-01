from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from api.exceptions import BatchApiNamespaceDoesNotExistException


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
        self.api_instance = client.BatchV1Api(
            client.ApiClient(self.configuration))
        self.api_instance_v1_beta = client.BatchV1beta1Api(
            client.ApiClient(self.configuration))

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

    def create_pod_template_spec(self, job_name, container_image, args, envs,
        resources=None):
        # Configure a Pod template container
        try:
            container = client.V1Container(
                name=job_name,
                image=container_image,
                args=args,
                resources=resources,
                env=envs,
                image_pull_policy="Always")

            pod_template_spec = client.V1PodSpec(restart_policy="Never",
                                                 containers=[container])
            return pod_template_spec
        except:
            print('error create_pod_template_spec')

    def create_job_object(self,
        job_name,
        container_image,
        args,
        envs,
        resources,
        label_key,
        label_value,
        backoff_limit=Constants.BACKOFF_LIMIT, ):
        try:
            pod_template_spec = self.create_pod_template_spec(
                job_name,
                container_image,
                args, envs,
                resources)
            # Create and configure a spec section
            template = client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={label_key: label_value}),
                spec=pod_template_spec)
            # Create the specification of deployment
            spec = client.V1JobSpec(
                template=template,
                backoff_limit=backoff_limit,
                ttl_seconds_after_finished=3 * 24 * 60 * 60)
            # Instantiate the job object
            job = client.V1Job(
                api_version="batch/v1",
                kind="Job",
                metadata=client.V1ObjectMeta(name=job_name),
                spec=spec)

            return job
        except:
            print('error create_job_object')

    def create_cron_job_object(self,
        cron_job_name, schedule,
        container_image, args, envs, resources,
        label_key,
        label_value,
        backoff_limit=Constants.BACKOFF_LIMIT):
        try:
            pod_template_spec = self.create_pod_template_spec(
                cron_job_name,
                container_image,
                args, envs,
                resources)
            # Create and configurate a spec section
            template = client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={label_key: label_value}),
                spec=pod_template_spec)

            job_spec = client.V1JobSpec(
                template=template,
                backoff_limit=backoff_limit,
                ttl_seconds_after_finished=3 * 24 * 60 * 60)
            # Create the specification of deployment
            spec = client.V1beta1JobTemplateSpec(
                metadata=client.V1ObjectMeta(labels={label_key: label_value}),
                spec=job_spec)
            # Create the specification of cron job with schedule
            cron_job_spec = client.V1beta1CronJobSpec(
                job_template=spec,
                schedule=schedule
            )
            # Instantiate the cron job object
            cron_job = client.V1beta1CronJob(
                api_version="batch/v1beta1",
                kind="CronJob",
                metadata=client.V1ObjectMeta(name=cron_job_name),
                spec=cron_job_spec)

            return cron_job
        except:
            print('error create_cron_job_object')

    def delete_all_expired_jobs(self, namespace, label_selector):
        try:
            job_list = self.api_instance.list_namespaced_job(
                namespace=namespace,
                label_selector=label_selector,
                watch=False)
            for job in job_list.items:
                if self.get_job_status(job) in [Constants.STATUS_SUCCEED,
                                                Constants.STATUS_FAILED]:
                    try:
                        body = client.V1DeleteOptions(
                            propagation_policy='Background')
                        self.api_instance.delete_namespaced_job(
                            namespace=namespace,
                            body=body,
                            name=job.metadata.name)
                    except ApiException as e:
                        raise BatchApiNamespaceDoesNotExistException(
                            "Exception when calling BatchV1Api->delete_namespaced_job: %s\n" % e)
        except ApiException as e:
            raise BatchApiNamespaceDoesNotExistException(
                "Exception when calling BatchV1Api->list_namespaced_job: %s\n" % e)

    def get_all_cron_job_status(self, namespace):
        try:
            cron_job_list = self.api_instance_v1_beta.list_namespaced_cron_job(
                namespace=namespace,
                watch=False)
        except ApiException as e:
            raise BatchApiNamespaceDoesNotExistException(
                "Exception when calling BatchV1Api->list_namespaced_cron_job: %s\n" % e)

        for cron_job in cron_job_list.items:
            if cron_job.status.active is not None:
                for active_cron_job in cron_job.status.active:
                    print(active_cron_job.name)
                    job = self.api_instance.read_namespaced_job(
                        namespace=namespace,
                        name=active_cron_job.name)
                    job_status = self.get_job_status(job)
                    return job_status, job

        return None, None
