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
TOKEN="d416ef2d47c98b6804b5637ce3f386837196f3e5"

class QuickstartUser(FastHttpUser):
    wait_time = constant(10000)

    def shaHash(self, string):
        m = hashlib.sha1()
        m.update(string.encode('utf-8'))
        return str(m.hexdigest())

    def on_start(self):

        message = ''.join(random.choices(string.ascii_lowercase, k=10))
        payload = {"data":{"type":"surveyAnswer","attributes":{"username":"foo","via":"web","items":[{"hash":SURVEY_ITEM_HASH,"value":message}]},"relationships":{"survey":{"data":{"id":SURVEY_HASH,"type":"survey"}}}}}
        headers = {'content-type': 'application/vnd.api+json'}

        newHeaders = {
            'content-type': 'application/vnd.api+json',
            'Wisembly-Token': TOKEN
        }

        self.client.post(f'/api/6/event/{KEYWORD}/surveys/{SURVEY_HASH}/answers', data=json.dumps(payload), headers=newHeaders)

    @task
    def do_nothing(self):
        pass