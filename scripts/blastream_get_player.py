import time
import json
import uuid
import hashlib

import random
import string

from locust import HttpUser, task, constant
from locust.contrib.fasthttp import FastHttpUser

CHANNEL_ID = "3439-93605"

class QuickstartUser(FastHttpUser):
    wait_time = constant(10000)

    def on_start(self):

        message = ''.join(random.choices(string.ascii_lowercase, k=10))
        payload = {"nickname":"test","id":"test"}
        headers = {
            "content-type": "application/json",
            "X-Api-Public": "1650371027699-nReuxg6MCJ5LEodAIIFcnt9I3CqkcKqb",
            "X-Api-Private": "1650371027699-YOfVdxTrDudeLHTtNYb3gMI1g1UuLip4"
        }

        self.client.post(f'/space/channel/{CHANNEL_ID}/participant', data=json.dumps(payload), headers=headers)

    @task
    def do_nothing(self):
        pass