# fXdNurYPnPxY9XEe2llbFAgxG36D394uFYry31Ch

import os
from twilio.rest import Client

def send_text(message):
    print(message)
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    #print(account_sid)
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    #print(auth_token)
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=message,
            from_='+12566951179',
            to='+12404380186'
        )

    print(message.sid)

#send_text('The water level is 0')
