import unittest
import json
import requests
import time
import uuid
from Utils.DbHelper import *


class SessionTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(SessionTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.headers = {'content-type': "application/json"}
        self.url_login = self.host + config['api']['account']['login']
        self.url_logout = self.host + config['api']['account']['logout']
        self.url_oauth = self.host + config['api']['oauth']
        self.url_register = self.host + config['api']['account']['register']
        self.email = accounts[env]['customer'][2]['email']
        self.password = accounts[env]['customer'][2]['password']
        self.url_create_session = self.host + config['api']['session']['create_session']
        self.url_delete_session = self.host + config['api']['session']['delete_session']
        self.url_update_session = self.host + config['api']['session']['update_session']
        self.url_query_session = self.host + config['api']['session']['query_session']
        self.url_add_session_user = self.host + config['api']['session']['add_session_user']
        self.url_query_session_user = self.host + config['api']['session']['query_session_user']
        self.url_delete_session_user = self.host + config['api']['session']['delete_session_user']
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
    def test_create_session_001_correct_token(self):
        case = 'create a new session with correct token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)
        self.assertEqual('123', data['appid'], 'Expected appid is 123. Actual = %s.' % data['appid'])
        self.assertEqual('session$123', data['name'], 'Expected name is session$123. Actual = %s.' % data['name'])
        self.assertEqual('up', data['state'], 'Expected state is up. Actual = %s.' % data['state'])
        self.assertEqual('test session', data['content'],
                         'Expected content is test session. Actual = %s.' % data['content'])
        self.assertNotEqual('', data['id'], 'Expected id is not null, Actual = %s.' % data['id'])

    def test_create_session_002_wrong_token(self):
        case = 'create a new session with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        url = self.url_create_session
        payload = {"token": '9527', "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('30005', data['errorCode'], 'Expected error code = 30005. Actual = %s.' % data['errorCode'])
        self.assertEqual('user token check failed', data['errorMsg'],
                         'Expected errorMsg is user token check failed. Actual = %s.' % data['errorMsg'])

    def test_create_session_003_empty_content(self):
        case = 'create a new session with correct token but empty content'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token and empty content
        url = self.url_create_session
        payload = {"token": token, "appid": "", "name": "", "content": "", "state": ""}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('10100', data['errorCode'], 'Expected error code = 10100. Actual = %s.' % data['errorCode'])
        self.assertEqual('invalid session name', data['errorMsg'],
                         'Expected errorMsg is invalid session name. Actual = %s.' % data['errorMsg'])

    def test_delete_session_001_correct_token(self):
        case = 'test delete session with correct token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        # delete the session with correct token
        data = rp.json()
        session_id = str(data['id'])
        url_delete_session = self.url_delete_session + token + '&id=' + session_id
        delete_rp = requests.delete(url_delete_session, headers=self.headers)
        print("url_delete_session: %s" % url_delete_session)
        print("response: status_code is %s , %s\n" % (delete_rp.status_code, delete_rp.text))
        self.assertEqual(200, delete_rp.status_code,
                         'Expected response code = 200. Actual = %s.' % delete_rp.status_code)

    def test_delete_session_002_wrong_token(self):
        case = 'test delete session with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        # delete the session with correct token
        data = rp.json()
        session_id = str(data['id'])
        url_delete_session = self.url_delete_session + '' + '&id=' + session_id
        delete_rp = requests.delete(url_delete_session, headers=self.headers)
        delete_data = delete_rp.json()
        print("url_delete_session: %s" % url_delete_session)
        print("response: status_code is %s , %s\n" % (delete_rp.status_code, delete_rp.text))
        self.assertEqual(400, delete_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % delete_rp.status_code)
        self.assertEqual('30005', delete_data['errorCode'],
                         'Expected error code = 30005. Actual = %s.' % delete_data['errorCode'])
        self.assertEqual('user token error', delete_data['errorMsg'],
                         'Expected errorMsg is user token error. Actual = %s.' % delete_data['errorMsg'])

    def test_delete_session_003_not_creator(self):
        case = 'test delete session with not creator'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        # register another user and get the new user's nickname
        token1 = self.get_login_token(self.email[1], self.password[1])
        # delete the session with not creator
        data = rp.json()
        session_id = str(data['id'])
        url_delete_session = self.url_delete_session + token1 + '&id=' + session_id
        delete_rp = requests.delete(url_delete_session, headers=self.headers)
        delete_data = delete_rp.json()
        print("url_delete_session: %s" % url_delete_session)
        print("response: status_code is %s , %s\n" % (delete_rp.status_code, delete_rp.text))
        self.assertEqual(400, delete_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % delete_rp.status_code)
        self.assertEqual('10000', delete_data['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % delete_data['errorCode'])
        self.assertEqual('No session for such user', delete_data['errorMsg'],
                         'Expected errorMsg is No session for such user. Actual = %s.' % delete_data['errorMsg'])

    def test_delete_session_004_wrong_session(self):
        case = 'test delete session with wrong session and correct token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        requests.post(url, data=json.dumps(payload), headers=self.headers)
        # delete the session with wrong session and correct token
        url_delete_session = self.url_delete_session + token + '&id=' + '000'
        delete_rp = requests.delete(url_delete_session, headers=self.headers)
        delete_data = delete_rp.json()
        print("url_delete_session: %s" % url_delete_session)
        print("response: status_code is %s , %s\n" % (delete_rp.status_code, delete_rp.text))
        self.assertEqual(400, delete_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % delete_rp.status_code)
        self.assertEqual('10100', delete_data['errorCode'],
                         'Expected error code = 10100. Actual = %s.' % delete_data['errorCode'])
        self.assertEqual('error session id', delete_data['errorMsg'],
                         'Expected errorMsg is error session id. Actual = %s.' % delete_data['errorMsg'])

    def test_update_session_001_correct_token(self):
        case = 'test update session with correct token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        url_update_session = self.url_update_session
        update_payload = {"token": token, "id": data['id'],
                          "name": "session$321", "content": "test update session", "state": "up"}
        update_rp = requests.put(url_update_session, data=json.dumps(update_payload), headers=self.headers)
        update_data = update_rp.json()
        print("url_update_session: %s\nupdate_payload: %s" % (url_update_session, update_payload))
        print("response: status_code is %s , %s\n" % (update_rp.status_code, update_rp.text))
        self.assertEqual(200, update_rp.status_code,
                         'Expected response code = 200. Actual = %s.' % update_rp.status_code)
        self.assertEqual('session$321', update_data['name'],
                         'Expected name is session$321. Actual = %s.' % update_data['name'])
        self.assertEqual('test update session', update_data['content'],
                         'Expected content is test update session. Actual = %s.' % update_data['content'])

    def test_update_session_002_wrong_token(self):
        case = 'test update session with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        url_update_session = self.url_update_session
        update_payload = {"token": '9527', "id": data['id'],
                          "name": "session$321", "content": "test update session", "state": "up"}
        update_rp = requests.put(url_update_session, data=json.dumps(update_payload), headers=self.headers)
        update_data = update_rp.json()
        print("url_update_session: %s\nupdate_payload: %s" % (url_update_session, update_payload))
        print("response: status_code is %s , %s\n" % (update_rp.status_code, update_rp.text))
        self.assertEqual(400, update_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % update_rp.status_code)
        self.assertEqual('30005', update_data['errorCode'],
                         'Expected error code = 30005. Actual = %s.' % update_data['errorCode'])
        self.assertEqual('user token check failed', update_data['errorMsg'],
                         'Expected errorMsg is user token check failed. Actual = %s.' % update_data['errorMsg'])

    def test_update_session_003_wrong_session(self):
        case = 'test update session with wrong session'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        requests.post(url, data=json.dumps(payload), headers=self.headers)
        url_update_session = self.url_update_session
        update_payload = {"token": token, "id": '',
                          "name": "session$321", "content": "test update session", "state": "up"}
        update_rp = requests.put(url_update_session, data=json.dumps(update_payload), headers=self.headers)
        update_data = update_rp.json()
        print("url_update_session: %s\n update_payload: %s" % (url_update_session, update_payload))
        print("response: status_code is %s , %s\n" % (update_rp.status_code, update_rp.text))
        self.assertEqual(400, update_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % update_rp.status_code)
        self.assertEqual('10000', update_data['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % update_data['errorCode'])
        self.assertEqual('No session for such user', update_data['errorMsg'],
                         'Expected errorMsg is No session for such user. Actual = %s.' % update_data['errorMsg'])

    def test_query_session_001_correct_token(self):
        case = 'test query session with correct token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        url_query_session = self.url_query_session + '?token=' + token + '&id=' + str(data['id'])
        query_rp = requests.get(url_query_session, headers=self.headers)
        query_data = query_rp.json()
        print("url_query_session: %s" % url_query_session)
        print("response: status_code is %s , %s\n" % (query_rp.status_code, query_rp.text))
        self.assertEqual(200, query_rp.status_code, 'Expected response code = 200. Actual = %s.' % query_rp.status_code)
        self.assertEqual('123', query_data['appid'], 'Expected appid is 123. Actual = %s.' % query_data['appid'])
        self.assertEqual('session$123', query_data['name'],
                         'Expected name is session$123. Actual = %s.' % query_data['name'])
        self.assertEqual('up', query_data['state'], 'Expected state is up. Actual = %s.' % query_data['state'])
        self.assertEqual('test session', query_data['content'],
                         'Expected content is test session. Actual = %s.' % query_data['content'])
        self.assertNotEqual('', query_data['id'], 'Expected id is not null, Actual = %s.' % query_data['id'])

    def test_query_session_002_wrong_token(self):
        case = 'test query session with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        url_query_session = self.url_query_session + '?token=' + '' + '&id=' + str(data['id'])
        query_rp = requests.get(url_query_session, headers=self.headers)
        query_data = query_rp.json()
        print("url_query_session: %s" % url_query_session)
        print("response: status_code is %s , %s\n" % (query_rp.status_code, query_rp.text))
        self.assertEqual(400, query_rp.status_code, 'Expected response code = 400. Actual = %s.' % query_rp.status_code)
        self.assertEqual('30005', query_data['errorCode'],
                         'Expected error code = 30005. Actual = %s.' % query_data['errorCode'])
        self.assertEqual('user token error', query_data['errorMsg'],
                         'Expected errorMsg is user token error. Actual = %s.' % query_data['errorMsg'])

    def test_query_session_003_wrong_session(self):
        case = 'test query session with wrong session'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        url_query_session = self.url_query_session + '?token=' + token + '&id=' + ''
        query_rp = requests.get(url_query_session, headers=self.headers)
        query_data = query_rp.json()
        print("url_query_session: %s" % url_query_session)
        print("response: status_code is %s , %s\n" % (query_rp.status_code, query_rp.text))
        self.assertEqual(400, query_rp.status_code, 'Expected response code = 400. Actual = %s.' % query_rp.status_code)
        self.assertEqual('10000', query_data['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % query_data['errorCode'])
        self.assertEqual('No session for such user', query_data['errorMsg'],
                         'Expected errorMsg is No session for such user. Actual = %s.' % query_data['errorMsg'])

    def test_add_session_user_001(self):
        case = 'test add a session user'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        data_rp1 = rp1.json()
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(200, rp1.status_code,
                         'Expected response code = 200. Actual = %s.' % rp1.status_code)
        self.assertEqual('add ok', data_rp1['Msg'],
                         'Expected errorMsg is add ok. Actual = %s.' % data_rp1['Msg'])

    def test_add_session_user_002_user_not_existed(self):
        case = 'test add a session user but the user does not existed'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": 000000}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        data_rp1 = rp1.json()
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('30009', data_rp1['errorCode'],
                         'Expected error code = 30009. Actual = %s.' % data_rp1['errorCode'])
        self.assertEqual('no such user', data_rp1['errorMsg'],
                         'Expected errorMsg is no such user. Actual = %s.' % data_rp1['errorMsg'])

    def test_add_session_user_003_wrong_session_id(self):
        case = 'test add a session user but with wrong session id'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": 000000, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        data_rp1 = rp1.json()
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('10000', data_rp1['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % data_rp1['errorCode'])
        self.assertEqual('No session for such user', data_rp1['errorMsg'],
                         'Expected errorMsg is No session for such user. Actual = %s.' % data_rp1['errorMsg'])

    def test_add_session_user_004_wrong_token(self):
        case = 'test add a session user but with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": 9527, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        data_rp1 = rp1.json()
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('30005', data_rp1['errorCode'],
                         'Expected error code = 30005. Actual = %s.' % data_rp1['errorCode'])
        self.assertEqual('user token check failed', data_rp1['errorMsg'],
                         'Expected errorMsg is user token check failed. Actual = %s.' % data_rp1['errorMsg'])

    def test_add_session_user_005_user_existed_in_the_session(self):
        case = 'test add a session user'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add session user
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        # add the user to session again
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        data_rp1 = rp1.json()
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code,
                         'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('10000', data_rp1['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % data_rp1['errorCode'])
        self.assertEqual('user exists in the session', data_rp1['errorMsg'],
                         'Expected errorMsg is user exists in the session. Actual = %s.' % data_rp1['errorMsg'])

    def test_query_session_user_001(self):
        case = 'test query session user info'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        url_query_session_user = self.url_query_session_user + token + '&session_id=' + session_id
        rp2 = requests.get(url_query_session_user, headers=self.headers)
        print("url_query_session_user: %s\n" % url_query_session_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(200, rp2.status_code,
                         'Expected response code = 200. Actual = %s.' % rp2.status_code)

    def test_query_session_user_002_wrong_session_id(self):
        case = 'test query session user info with wrong session id'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        url_query_session_user = self.url_query_session_user + token + '&session_id=' + '000000'
        rp2 = requests.get(url_query_session_user, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_query_session_user: %s\n" % url_query_session_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10000', data_rp2['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % data_rp2['errorCode'])
        self.assertEqual('No session for such user', data_rp2['errorMsg'],
                         'Expected errorMsg is No session for such user. Actual = %s.' % data_rp2['errorMsg'])

    def test_query_session_user_002_wrong_token(self):
        case = 'test query session user info with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        url_query_session_user = self.url_query_session_user + '9527' + '&session_id=' + session_id
        rp2 = requests.get(url_query_session_user, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_query_session_user: %s\n" % url_query_session_user)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('30005', data_rp2['errorCode'],
                         'Expected error code = 30005. Actual = %s.' % data_rp2['errorCode'])
        self.assertEqual('user token check failed', data_rp2['errorMsg'],
                         'Expected errorMsg is user token check failed. Actual = %s.' % data_rp2['errorMsg'])

    def test_delete_session_user_001(self):
        case = 'test delete a session user'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add session user
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        data_rp1 = rp1.json()
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete session user
        url_delete_session_user = self.url_delete_session_user + token + '&user_id=' + str(
            user_id) + '&session_id=' + session_id
        rp2 = requests.delete(url_delete_session_user, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete_session_user: %s\n" % url_delete_session_user,)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(200, rp2.status_code,
                         'Expected response code = 200. Actual = %s.' % rp2.status_code)
        self.assertEqual('delete ok', data_rp2['Msg'],
                         'Expected errorMsg is delete ok. Actual = %s.' % data_rp2['Msg'])

    def test_delete_session_user_002_user_not_existed(self):
        case = 'test delete a session user but the user does not exist in the session'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # delete session user
        url_delete_session_user = self.url_delete_session_user + token + '&user_id=' + str(
            user_id) + '&session_id=' + session_id
        rp2 = requests.delete(url_delete_session_user, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete_session_user: %s\n" % url_delete_session_user,)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10000', data_rp2['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % data_rp2['errorCode'])
        self.assertEqual('user does not exist in the session', data_rp2['errorMsg'],
                         'Expected errorMsg is user does not exist in the session. Actual = %s.' % data_rp2['errorMsg'])

    def test_delete_session_user_003_wrong_session(self):
        case = 'test delete a session user with wrong session'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add session user
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete session user
        url_delete_session_user = self.url_delete_session_user + token + '&user_id=' + str(
            user_id) + '&session_id=' + '000000'
        rp2 = requests.delete(url_delete_session_user, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete_session_user: %s\n" % url_delete_session_user,)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10000', data_rp2['errorCode'],
                         'Expected error code = 10000. Actual = %s.' % data_rp2['errorCode'])
        self.assertEqual('No session for such user', data_rp2['errorMsg'],
                         'Expected errorMsg is No session for such user. Actual = %s.' % data_rp2['errorMsg'])

    def test_delete_session_user_004_wrong_token(self):
        case = 'test delete a session user with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a new session with newly created user's token
        url = self.url_create_session
        payload = {"token": token, "appid": "123", "name": "session$123", "content": "test session", "state": "up"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        session_id = str(data['id'])
        print("url: %s\n payload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # another user
        user_id = int(self.get_user_id_by_email(self.email[1]))
        # add session user
        url_add_session_user = self.url_add_session_user
        payload1 = {"token": token, "session_id": session_id, "user_id": user_id}
        rp1 = requests.post(url_add_session_user, data=json.dumps(payload1), headers=self.headers)
        data_rp1 = rp1.json()
        print("url_add_session_user: %s\n payload1: %s" % (url_add_session_user, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        # delete session user
        url_delete_session_user = self.url_delete_session_user + '000000' + '&user_id=' + str(
            user_id) + '&session_id=' + session_id
        rp2 = requests.delete(url_delete_session_user, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete_session_user: %s\n" % url_delete_session_user,)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code,
                         'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('30005', data_rp2['errorCode'],
                         'Expected error code = 30005. Actual = %s.' % data_rp2['errorCode'])
        self.assertEqual('user token check failed', data_rp2['errorMsg'],
                         'Expected errorMsg is user token check failed. Actual = %s.' % data_rp2['errorMsg'])
