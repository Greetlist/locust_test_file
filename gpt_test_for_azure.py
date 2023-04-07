from locust import HttpUser, task, between
from hashlib import sha256
import random
from json import JSONDecodeError
import uuid

class GPTForAzureUser(HttpUser):
    wait_time = between(1, 3)

    phone_number_list = [
        '18474629910', '18374612203', '12388102341', '13622310021',
        '17583212233', '17355420912', '12033128764', '19233100012',
        '19873261091', '17220200123', '19120103346', '15612331923',
    ]

    # @task(2)
    # def test_get_answer(self):
       # for i in range(1, 40):
           # req_json = {'user_id': random.randint(1, 10), 'question': 'test_question'}
           # res = self.client.post('/get_answer', json=req_json):
           # try:
               # if res.json()["return_code"] != 0:
                   # res.failure("ReturnCode is not 0")
           # except JSONDecodeError as e:
               # print(e)

    #@task(4)
    #def test_get_topic_list(self):
    #    req_json = {'user_id': random.randint(1, 20)}
    #    res = self.client.post('/get_all_topic', json=req_json)
    #    try:
    #        if res.json()["return_code"] != 0:
    #            res.failure("ReturnCode is not 0")
    #    except JSONDecodeError as e:
    #        print(e)

    #@task(4)
    #def test_get_history(self):
    #    user_id = random.randint(1, 20)
    #    topic_list = self.get_user_topics(user_id)
    #    for topic_info in topic_list:
    #        req_json = {'user_id': user_id, 'topic_id': topic_info['topic_id']}
    #        res = self.client.post('/get_history', json=req_json)
    #        try:
    #            if res.json()["return_code"] != 0:
    #                res.failure("ReturnCode is not 0")
    #        except JSONDecodeError as e:
    #            print(e)

    # @task
    # def test_add_va_code(self):
        # va_code, level = self.gen_random_level_va_code()
        # req_json = {'va_code': va_code, 'level': level}
        # res = self.client.post('/add_va_code', json=req_json)
        # try:
            # if res.json()["return_code"] != 0:
                # res.failure("ReturnCode is not 0")
        # except JSONDecodeError as e:
            # print(e)

    def gen_random_level_va_code(self):
        return str(uuid.uuid4()), random.randint(1, 3)

    # @task(1)
    # def test_login(self):
       # user_index = random.randint(0, len(GPTForAzureUser.phone_number_list)-1)
       # req_json = {'user_id': GPTForAzureUser.phone_number_list[user_index], 'verification_code': '002345'}
       # res = self.client.post('/login', json=req_json)

    @task(1)
    def test_bind_va_code(self):
        va_code_list = self.get_inactive_va_code()
        user_index = random.randint(0, len(GPTForAzureUser.phone_number_list)-1)
        va_code_index = random.randint(0, len(va_code_list)-1)
        req_json = {'va_code': va_code_list[user_index], 'user_id': GPTForAzureUser.phone_number_list[user_index]}
        res = self.client.post('/login', json=req_json)

    def get_inactive_va_code(self):
        res = self.client.get('/get_all_va_code')
        if res.json()["return_code"] == 0:
            return res.json()['topic_list']
        return []

    def get_user_topics(self, user_id):
        res = self.client.post('/get_all_topic', json={'user_id': user_id})
        if res.json()["return_code"] == 0:
            return res.json()['topic_list']
        return []
