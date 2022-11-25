import time
import json

from locust import HttpUser, task, between
from locust.contrib.fasthttp import FastHttpUser

KEYWORD = "tmc"

class QuickstartUser(FastHttpUser):
    wait_time = between(0.1, 1.1)

    @task
    def on_start(self):
        payload = {"data":{"type":"apiSession","attributes":{"app_id":"wisembly_app","hash":"67608b0127f18b15cc8bee4c4f9caeb9cbde5b0c"},"relationships":{}}}
        headers = {'content-type': 'application/vnd.api+json'}
        self.client.post("/api/6/authentication", data=json.dumps(payload), headers=headers)

    @task
    def get_event(self):
        self.client.get("/api/6/event/%s" % KEYWORD)
        self.client.get("/api/6/event/%s/medias?limit=50&offset=0" % KEYWORD)
        self.client.get("/api/6/event/%s/surveys?limit=50&offset=0" % KEYWORD)

