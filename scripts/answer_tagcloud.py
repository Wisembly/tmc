import time
import json
import uuid
import hashlib

import random
import string

from locust import HttpUser, task, constant
from locust.contrib.fasthttp import FastHttpUser

KEYWORD = "tmc"
SURVEY_HASH = "2d2e36786c5f1dee206620413313dd8031d0ef8f"
SURVEY_ITEM_HASH = "5f3e2a52627e5902ed5987177ff546d47e645066"

class QuickstartUser(FastHttpUser):
    wait_time = constant(10000)

    def shaHash(self, string):
        m = hashlib.sha1()
        m.update(string.encode('utf-8'))
        return str(m.hexdigest())

    def on_start(self):

        token = ''
        payload = {"data":{"type": "apiSession", "attributes": {"app_id":"wisembly_app","hash":"67608b0127f18b15cc8bee4c4f9caeb9cbde5b0c"}, "relationships":{}}}
        headers = {'content-type': 'application/vnd.api+json'}

        clientParams = {
            "catch_response": True,
            "verify": False,
            "data": json.dumps(payload),
            "headers": headers
        }

        with self.client.post("/api/6/authentication", **clientParams) as response:
            if response.status_code == 200:
                token = response.json()['data']['attributes']['token'];
                response.success()
            else:
                response.failure("Could not get credentials")

        message = ''.join(random.choices(string.ascii_lowercase, k=10))
        payload = {"data":{"type":"surveyAnswer","attributes":{"username":"foo","via":"web","items":[{"hash":SURVEY_ITEM_HASH,"value":message}]},"relationships":{"survey":{"data":{"id":SURVEY_HASH,"type":"survey"}}}}}
        headers = {'content-type': 'application/vnd.api+json'}

        newHeaders = {
            'content-type': 'application/vnd.api+json',
            'Wisembly-Token': token
        }

        self.client.post(f'/api/6/event/{KEYWORD}/surveys/{SURVEY_HASH}/answers', data=json.dumps(payload), headers=newHeaders)

    @task
    def do_nothing(self):
        pass