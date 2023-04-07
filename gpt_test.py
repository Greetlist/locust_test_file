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

    @task(4)
    def get_topic_list(self):
        req_json = {'user_id': random.randint(1, 20)}
        res = self.client.post('/get_all_topic', json=req_json, catch_response=True)
        try:
            if res.json()["return_code"] != 0:
                res.failure("ReturnCode is not 0")
        except JSONDecodeError as e:
            print(e)

    @task(4)
    def get_history(self):
        user_id = random.randint(1, 20)
        topic_list = self.get_user_topics(user_id)
        for topic_info in topic_list:
            req_json = {'user_id': user_id, 'topic_id': topic_info['topic_id']}
            res = self.client.post('/get_history', json=req_json, catch_response=True)
            try:
                if res.json()["return_code"] != 0:
                    res.failure("ReturnCode is not 0")
            except JSONDecodeError as e:
                print(e)

    def get_user_topics(self, user_id):
        res = self.client.post('/get_all_topic', json={'user_id': user_id}, catch_response=True)
        if res.json()["return_code"] == 0:
            return res.json()['topic_list']
        return []
