from locust import HttpUser, task, between
from hashlib import sha256
import random
from json import JSONDecodeError

class GPTUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_save_question(self):
        for i in range(1, 40):
            req_json = {'user_id': random.randint(1, 10), 'question': 'test_question'}
            with self.client.post('/test_save_question', json=req_json, catch_response=True) as res:
                try:
                    if res.json()["return_code"] != 0:
                        res.failure("ReturnCode is not 0")
                except JSONDecodeError as e:
                    print(e)

    #@task
    #def get_topic(self):
    #    req_json = {'user_id': random.randint(1, 20)}
    #    res = self.client.post('/get_all_topic', json=req_json, catch_response=True)
    #    try:
    #        if res.json()["return_code"] != 0:
    #            res.failure("ReturnCode is not 0")
    #    except JSONDecodeError as e:
    #        print(e)

    #@task
    #def get_history(self):
    #    req_json = {'user_id': random.randint(1, 20)}
    #    res = self.client.post('/get_history', json=req_json, catch_response=True)
    #    try:
    #        if res.json()["return_code"] != 0:
    #            res.failure("ReturnCode is not 0")
    #    except JSONDecodeError as e:
    #        print(e)
