from api.kubernetes import KubernetesApi

namespace = "default"
api = KubernetesApi()
if __name__ == '__main__':
    while True:
        api.get_cron_job_status(namespace)
