# fXdNurYPnPxY9XEe2llbFAgxG36D394uFYry31Ch

import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['ACa78f536eae6f850d9501e8fe2c22794b']
auth_token = os.environ['9cbd5432f7cd350c8068e5be6397e093']
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='The water level is 0',
         from_='+12566951179',
         to='+12404380186'
     )

print(message.sid)