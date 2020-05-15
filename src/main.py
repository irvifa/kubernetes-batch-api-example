import os
from api.kubernetes import KubernetesApi
from tools.slack import Slack

webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
namespace = os.environ.get('CLUSTER_NAMESPACE')
slack_api_token=os.environ.get('SLACK_API_TOKEN')
api = KubernetesApi()
slack_client = Slack(webhook_url, slack_api_token)

if __name__ == '__main__':
    while True:
        status, job = api.get_all_cron_job_status(namespace)
        if status is not None:
            slack_client.send_message(job)
