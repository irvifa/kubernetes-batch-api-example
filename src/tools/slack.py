import json, requests
import slack

class Slack:
    def __init__(self, webhook_url, slack_api_token):
        self.webhook_url = webhook_url
        self.client = slack.WebClient(
            token=slack_api_token
        )

    def get_slack_handle(self, email):
        """
        In this function we can get the user email based on the email they are using
        for the slack.
        :param email:
        :return:
        """
        try:
            result = self.client.users_lookupByEmail(email=email)
            if result["ok"]:
                return result["user"]["id"]
        except:
            print(f'''[WARNING] Can't get the slack handle for email: {email}''')

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
