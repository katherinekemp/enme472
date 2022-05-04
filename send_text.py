# fXdNurYPnPxY9XEe2llbFAgxG36D394uFYry31Ch

import os
from twilio.rest import Client

def send_text():
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    #account_sid = os.getenv('account_sid')
    #auth_token = os.environ.get('auth_token')
    account_sid = os.environ['ACa78f536eae6f850d9501e8fe2c22794b']
    auth_token = os.environ['86be2f06eb163703b04f7b7df83451b0']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='The water level is 0',
            from_='+12566951179',
            to='+12404380186'
        )

    print(message.sid)

if __name__ == "main":
    send_text()
