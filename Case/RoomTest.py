import unittest
import json
import requests
import time
import uuid
from Utils.DbHelper import *


class RoomTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(RoomTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.headers = {'content-type': "application/json"}
        self.url_login = self.host + config['api']['account']['login']
        self.url_logout = self.host + config['api']['account']['logout']
        self.url_oauth = self.host + config['api']['oauth']
        self.url_register = self.host + config['api']['account']['register']
        self.email = accounts[env]['customer'][2]['email']
        self.password = accounts[env]['customer'][2]['password']
        self.url_create_room = self.host + config['api']['room']['create_room']
        self.url_update_room = self.host + config['api']['room']['update_room']
        self.url_query_room = self.host + config['api']['room']['query_room']
        self.url_delete_room = self.host + config['api']['room']['delete_room']
        self.url_add_room_user = self.host + config['api']['room']['add_room_user']
        self.url_delete_room_user = self.host + config['api']['room']['delete_room_user']
        # test data
        self.email = []
        self.password = []
        self.email.append(accounts[env]['customer'][0]['email'])
        self.password.append(accounts[env]['customer'][0]['password'])
        self.email.append(accounts[env]['customer'][1]['email'])
        self.password.append(accounts[env]['customer'][1]['password'])

    def setUp(self):
        self.create_user_if_not_exist(env=config['setting']['environment'])

    def tearDown(self):
        pass

    def get_login_token(self, email, password):
        url = self.url_login
        payload = {'email': email, 'passphrase': password}
        headers = {'content-type': "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        token = response.json()['token']
        return token

    def register_user(self):
        nickname = str(uuid.uuid4())[-10:]
        email = 'test.%s@hypereal.com' % str(uuid.uuid4())[-8:]
        password = 'Test1234'
        url = self.url_register
        payload = {"nickname": nickname, "email": email, "image_path": "1",
                   "birthday": "1980-01-02", "gender": "M", "passphrase": password}
        requests.post(url, data=json.dumps(payload), headers=self.headers)
        return {'email': email, 'password': password, 'nickname': nickname}

    def get_user_id_by_email(self, email):
        try:
            sql = "select id from web_user where web_user.email = '" + email + "'"
            db_helper = DbHelper(self.env)
            result = db_helper.query(sql)
            db_helper.close()
            return result[0][0]
        except:
            return False
            print("user does not exist!")

    def register_new_user(self, nickname, email, password):
        url = self.url_register
        payload = {"nickname": nickname, "email": email, "image_path": "1",
                   "birthday": "1980-01-02", "gender": "M", "passphrase": password}
        requests.post(url, data=json.dumps(payload), headers=self.headers)
        return {'email': email, 'password': password, 'nickname': nickname}

    def create_user_if_not_exist(self, env):
        i = 0
        while i < 5:
            nickname = accounts[env]['customer'][i]['nickname']
            email = accounts[env]['customer'][i]['email']
            password = accounts[env]['customer'][i]['password']
            user_id = self.get_user_id_by_email(email)
            if user_id:
                pass
            else:
                self.register_new_user(nickname, email, password)
            i += 1

    # =========================================
    # Test Cases
    # =========================================
    def test_create_room_001(self):
        case = 'create a new room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        url = self.url_create_room + self.get_login_token(self.email[0], self.password[0])
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual(name, data['room']['name'],
                         'Expected room name is %s. Actual = %s.' % (name, data['room']['name']))
        self.assertEqual(description, data['room']['description'],
                         'Expected room description is %s. Actual = %s.' % (description, data['room']['description']))
        self.assertNotEqual('', data['room']['id'], 'Expected room id is not null, actual is %s' % data['room']['id'])

    def test_create_room_002_empty_name(self):
        case = 'create a new room with empty name'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room with empty room name using the newly created user
        name = ''
        description = str(uuid.uuid4())[-10:]
        url = self.url_create_room + self.get_login_token(self.email[0], self.password[0])
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('10100', data['errorCode'], 'Expected response error code = 10100. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('invalid room name', data['errorMsg'],
                         'Expected errorMsg is: invalid room name. Actual = %s.' % data['errorMsg'])

    def test_create_room_003_empty_description(self):
        case = 'create a new room with empty name'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room with empty description using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = ''
        url = self.url_create_room + self.get_login_token(self.email[0], self.password[0])
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual(name, data['room']['name'],
                         'Expected room name is %s. Actual = %s.' % (name, data['room']['name']))
        self.assertEqual(description, data['room']['description'],
                         'Expected room description is %s. Actual = %s.' % (description, data['room']['description']))
        self.assertNotEqual('', data['room']['id'], 'Expected room id is not null, actual is %s' % data['room']['id'])

    def test_update_room_001(self):
        case = 'update room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        # update the newly created room
        room_id = str(data['room']['id'])
        update_name = str(uuid.uuid4())[-11:]
        update_description = str(uuid.uuid4())[-10:]
        update_payload = {"room": {"name": update_name, "description": update_description}}
        update_room_url = self.url_update_room + room_id + '?access_token=' + token
        print("update_room_url: %s\nupdate_payload: %s" % (update_room_url, update_payload))
        update_response = requests.put(update_room_url, data=json.dumps(update_payload), headers=self.headers)
        print("update_response: status_code is %s , %s\n" % (update_response.status_code, update_response.text))
        update_data = update_response.json()
        self.assertEqual(200, update_response.status_code,
                         'Expected response code = 200. Actual = %s.' % update_response.status_code)
        self.assertEqual(update_name, update_data['room']['name'],
                         'Expected room name is %s. Actual = %s.' % (name, update_data['room']['name']))
        self.assertEqual(update_description, update_data['room']['description'],
                         'Expected room description is %s. Actual = %s.' % (
                             description, update_data['room']['description']))
        self.assertNotEqual('', data['room']['id'], 'Expected room id is not null, actual is %s' % data['room']['id'])

    def test_update_room_002_empty_name(self):
        case = 'update room with empty room name'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        # update the newly created room with empty name
        room_id = str(data['room']['id'])
        update_name = ''
        update_description = str(uuid.uuid4())[-10:]
        update_payload = {"room": {"name": update_name, "description": update_description}}
        update_room_url = self.url_update_room + room_id + '?access_token=' + token
        print("update_room_url: %s\nupdate_payload: %s" % (update_room_url, update_payload))
        update_response = requests.put(update_room_url, data=json.dumps(update_payload), headers=self.headers)
        print("update_response: status_code is %s , %s\n" % (update_response.status_code, update_response.text))
        update_data = update_response.json()
        self.assertEqual(400, update_response.status_code,
                         'Expected response code = 400. Actual = %s.' % update_response.status_code)
        self.assertEqual('10100', update_data['errorCode'], 'Expected response error code = 10100. Actual = %s.'
                         % update_data['errorCode'])
        self.assertEqual('invalid room name', update_data['errorMsg'],
                         'Expected errorMsg is: invalid room name. Actual = %s.' % update_data['errorMsg'])

    def test_aquery_room_001(self):
        case = 'query room info'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # add a new room
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        # query the newly created room info
        room_id = str(data['room']['id'])
        query_room_url = self.url_query_room + room_id + '?access_token=' + token
        query_response = requests.get(query_room_url, headers=self.headers)
        print("query_room_url: %s" % query_room_url)
        print("query_response: status_code is %s , %s\n" % (query_response.status_code, query_response.text))
        query_data = query_response.json()
        self.assertEqual(200, query_response.status_code,
                         'Expected response code = 200. Actual = %s.' % query_response.status_code)
        self.assertEqual(data['room']['id'], query_data['room']['id'],
                         'Expected room name is %s. Actual = %s.' % (data['room']['id'], query_data['room']['id']))
        self.assertEqual(data['room']['name'], query_data['room']['name'],
                         'Expected room name is %s. Actual = %s.' % (data['room']['name'], query_data['room']['name']))
        self.assertEqual(data['room']['description'], query_data['room']['description'],
                         'Expected room description is %s. Actual = %s.' % (
                             data['room']['description'], query_data['room']['description']))

    def test_delete_room_001_correct_token(self):
        case = 'test delete room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # add a new room
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        # delete the newly created room
        room_id = str(data['room']['id'])
        delete_room_url = self.url_delete_room + room_id + '?access_token=' + token
        delete_response = requests.delete(delete_room_url, headers=self.headers)
        print("delete_room_url: %s" % delete_room_url)
        print("delete_response: status_code is %s , %s\n" % (delete_response.status_code, delete_response.text))
        self.assertEqual(200, delete_response.status_code,
                         'Expected response code = 200. Actual = %s.' % delete_response.status_code)

    def test_delete_room_002_not_existed_room(self):
        case = 'test delete a not existed room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # delete a not existed room
        token = self.get_login_token(self.email[0], self.password[0])
        delete_room_url = self.url_delete_room + '' + '?access_token=' + token
        delete_response = requests.delete(delete_room_url, headers=self.headers)
        print("delete_room_url: %s" % delete_room_url)
        print("delete_response: status_code is %s , %s\n" % (delete_response.status_code, delete_response.text))
        self.assertEqual(400, delete_response.status_code,
                         'Expected response code = 400. Actual = %s.' % delete_response.status_code)

    def test_delete_room_003_not_creator(self):
        case = 'test delete room with a user who is not the creator of the room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # add a new room
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # delete the newly created room with not creator
        room_id = str(data['room']['id'])
        token1 = self.get_login_token(self.email[1], self.password[1])
        delete_room_url = self.url_delete_room + room_id + '?access_token=' + token1
        delete_response = requests.delete(delete_room_url, headers=self.headers)
        data = delete_response.json()
        print("delete_room_url: %s" % delete_room_url)
        print("delete_response: status_code is %s , %s\n" % (delete_response.status_code, delete_response.text))
        self.assertEqual(400, delete_response.status_code,
                         'Expected response code = 400. Actual = %s.' % delete_response.status_code)
        self.assertEqual('10000', data['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % data['errorCode'])
        self.assertEqual('No room for such user', data['errorMsg'],
                         'Expected errorMsg is No room for such user. Actual = %s.' % data['errorMsg'])

    def test_add_room_user_001(self):
        case = 'test add a new room user'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(200, rp1.status_code,
                         'Expected response code = 200. Actual = %s.' % rp1.status_code)

    def test_add_new_room_user_002_wrong_room_id(self):
        case = 'test add a new room user with wrong room id'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": 000000, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        data1 = rp1.json()
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('10000', data1['errorCode'], 'Expected response error code = 10000. Actual = %s.'
                         % data1['errorCode'])
        self.assertEqual('No room for such user', data1['errorMsg'],
                         'Expected errorMsg is: No room for such user. Actual = %s.' % data1['errorMsg'])

    def test_add_new_room_user_003_wrong_token(self):
        case = 'test add a new room user with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room but wrong token
        url_add_room_user = self.url_add_room_user + '000000'
        payload1 = {"room_id": room_id, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        data1 = rp1.json()
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('30005', data1['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % data1['errorCode'])
        self.assertEqual('user token check failed', data1['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data1['errorMsg'])

    def test_add_new_room_user_004_wrong_user_id(self):
        case = 'test add a new room user with wrong user id'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        # add the new user to the newly created room but wrong token
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": -9527}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        data1 = rp1.json()
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('30009', data1['errorCode'], 'Expected response error code = 30009. Actual = %s.'
                         % data1['errorCode'])
        self.assertEqual('no such user', data1['errorMsg'],
                         'Expected errorMsg is: no such user. Actual = %s.' % data1['errorMsg'])

    def test_add_new_room_user_004_user_existed(self):
        case = 'test add a new room user with a user who is already in the room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room but wrong token
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": user_id}
        requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        # add again
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        data1 = rp1.json()
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('10000', data1['errorCode'], 'Expected response error code = 10000. Actual = %s.'
                         % data1['errorCode'])
        self.assertEqual('user exists in the room', data1['errorMsg'],
                         'Expected errorMsg is: user exists in the room. Actual = %s.' % data1['errorMsg'])

    def test_delete_room_user_001(self):
        case = 'test delete a room user'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete the newly added room user
        url_delete_room_user = self.url_delete_room_user + token + '&user_id=' + str(user_id) + '&room_id=' + str(
            room_id)
        rp2 = requests.delete(url_delete_room_user, headers=self.headers)
        print("url_delete_room_user: %s" % url_delete_room_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(200, rp2.status_code,
                         'Expected response code = 200. Actual = %s.' % rp2.status_code)

    def test_delete_room_user_002_user_not_existed(self):
        case = 'test delete a room user who is not in the room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete the newly added room user
        url_delete_room_user = self.url_delete_room_user + token + '&user_id=' + str(user_id) + '&room_id=' + str(
            room_id)
        requests.delete(url_delete_room_user, headers=self.headers)
        # delete again
        rp2 = requests.delete(url_delete_room_user, headers=self.headers)
        rp2_data = rp2.json()
        print("url_delete_room_user: %s" % url_delete_room_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10000', rp2_data['errorCode'], 'Expected response error code = 10000. Actual = %s.'
                         % rp2_data['errorCode'])
        self.assertEqual('user does not exist in the room', rp2_data['errorMsg'],
                         'Expected errorMsg is: user does not exist in the room. Actual = %s.' % rp2_data['errorMsg'])

    def test_delete_room_user_003_wrong_token(self):
        case = 'test delete a room user with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete the newly added room user
        url_delete_room_user = self.url_delete_room_user + token + '0' + '&user_id=' + str(user_id) + '&room_id=' + str(
            room_id)
        rp2 = requests.delete(url_delete_room_user, headers=self.headers)
        rp2_data = rp2.json()
        print("url_delete_room_user: %s" % url_delete_room_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('30005', rp2_data['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % rp2_data['errorCode'])
        self.assertEqual('user token check failed', rp2_data['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % rp2_data['errorMsg'])

    def test_delete_room_user_004_wrong_room(self):
        case = 'test delete a room user with wrong room'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete the newly added room user with wrong room id
        url_delete_room_user = self.url_delete_room_user + token + '&user_id=' + str(user_id) + '&room_id=' + str(
            room_id) + '9527'
        rp2 = requests.delete(url_delete_room_user, headers=self.headers)
        rp2_data = rp2.json()
        print("url_delete_room_user: %s" % url_delete_room_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10000', rp2_data['errorCode'], 'Expected response error code = 10000. Actual = %s.'
                         % rp2_data['errorCode'])
        self.assertEqual('No room for such user', rp2_data['errorMsg'],
                         'Expected errorMsg is: No room for such user. Actual = %s.' % rp2_data['errorMsg'])

    def test_delete_room_user_005_not_creator(self):
        case = 'test delete a room user with a user who is not the room creator'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # create a new room using the newly created user
        name = str(uuid.uuid4())[-11:]
        description = str(uuid.uuid4())[-10:]
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_create_room + token
        payload = {"room": {"name": name, "description": description}}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        room_id = data['room']['id']
        # register another new user
        token1 = self.get_login_token(self.email[1], self.password[1])
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add the new user to the newly created room
        url_add_room_user = self.url_add_room_user + token
        payload1 = {"room_id": room_id, "user_id": user_id}
        rp1 = requests.post(url_add_room_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_room_user: %s\n payload1: %s" % (url_add_room_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete the newly added room user with another user's token
        url_delete_room_user = self.url_delete_room_user + token1 + '&user_id=' + str(user_id) + '&room_id=' + str(
            room_id)
        rp2 = requests.delete(url_delete_room_user, headers=self.headers)
        rp2_data = rp2.json()
        print("url_delete_room_user: %s" % url_delete_room_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10000', rp2_data['errorCode'], 'Expected response error code = 10000. Actual = %s.'
                         % rp2_data['errorCode'])
        self.assertEqual('No room for such user', rp2_data['errorMsg'],
                         'Expected errorMsg is: No room for such user. Actual = %s.' % rp2_data['errorMsg'])


