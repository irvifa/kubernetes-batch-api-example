import json, requests

class Slack:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, is_successful):

        status = "SUCCESSFUL" if is_successful else "FAILED"

        text = "Status : {status}".format(status=status)

        message = {'text': text, 'mrkdwn': True}
        response = requests.post(
            self.webhook_url, data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
