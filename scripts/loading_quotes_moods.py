import time
import json
import hashlib

from locust import HttpUser, task, between

# FastHttpUser is 5-6X faster than HttpUser but does not support headers persist in on_start
# https://github.com/locustio/locust/issues/2035
# from locust.contrib.fasthttp import FastHttpUser

KEYWORD = "tmc"

class QuickstartUser(HttpUser):
    wait_time = between(20, 45)

    def shaHash(self, string):
        m = hashlib.sha1()
        m.update(string.encode('utf-8'))
        return str(m.hexdigest())

    def on_start(self):
        token = ""
        payload = {"data":{"type":"apiSession","attributes":{"app_id":"wisembly_app","hash":"67608b0127f18b15cc8bee4c4f9caeb9cbde5b0c"},"relationships":{}}}
        headers = {'content-type': 'application/vnd.api+json'}

        clientParams = {
            "catch_response": True,
            "verify": False,
            "data": json.dumps(payload),
            "headers": headers
        }

        with self.client.post("/api/6/authentication", **clientParams) as response:
            if response.status_code == 200:
                json_response = json.loads(response.text)
                token = response.json()['data']['attributes']['token']

                self.client.headers = {
                    'content-type': 'application/vnd.api+json',
                    'Wisembly-Token': token
                }

                response.success()
            else:
                response.failure("Could not get credentials")

        self.client.get("/api/6/event/%s" % KEYWORD)
        self.client.post("/api/6/event/%s/watchers" % KEYWORD)

        clientParams = {
            "data": json.dumps({"event": {"keyword": KEYWORD}}),
            "headers": {'content-type': 'application/json'}
        }

        self.client.post("/api/4/users/node/credentials", **clientParams)

        self.client.get("/api/6/event/%s/medias?limit=25&offset=0&active=true" % KEYWORD)
        self.client.get("/api/6/event/%s/surveys?limit=50" % KEYWORD)
        self.client.get("/api/6/event/%s/quotes?sort=recent&limit=10&unmoderated=false" % KEYWORD)

    @task(10)
    def post_quote(self):
        hash = self.shaHash(str(time.time()))
        payload = {"data":{"id": hash,"type":"quote","attributes":{"quote":"Hello %s" % hash,"username":"Guillaume Potier","via":"tablet"},"relationships":{}}}
        clientParams = {
            "catch_response": True,
            "verify": False,
            "data": json.dumps(payload),
        }

        with self.client.post("/api/6/event/%s/quotes" % KEYWORD, **clientParams) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Could not post quote")

    @task(30)
    def post_mood(self):
        clientParams = {
            "catch_response": True,
            "verify": False,
        }

        with self.client.get("/api/4/event/%s/mood?mood=tada" % KEYWORD, **clientParams) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure("Could not post quote")

    @task(70)
    def do_nothing(self):
        pass

