import unittest
import json
import requests
import time
import uuid
from Utils.DbHelper import *


class AccountTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(AccountTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.url_login = self.host + config['api']['account']['login']
        self.url_logout = self.host + config['api']['account']['logout']
        self.url_query_user_role = self.host + config['api']['account']['query_user_role']
        self.url_oauth = self.host + config['api']['oauth']
        self.url_register = self.host + config['api']['account']['register']
        self.email = accounts[env]['customer'][2]['email']
        self.password = accounts[env]['customer'][2]['password']
        self.headers = {'content-type': "application/json"}
        # test data
        self.email = []
        self.password = []
        self.nickname = []
        self.email.append(accounts[env]['customer'][0]['email'])
        self.password.append(accounts[env]['customer'][0]['password'])
        self.nickname.append(accounts[env]['customer'][0]['nickname'])
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
        while i < 7:
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
    def test_register_001_new_user(self):
        case = 'register a new user'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        nickname = str(uuid.uuid4())[-10:]
        email = 'test+%s@hypereal.com' % str(uuid.uuid4())[-8:]
        url = self.url_register
        payload = {
            "nickname": nickname,
            "email": email,
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": "Test1234"
        }
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual('register ok', data['Msg'],'Expected response: Msg = register ok. Actual = %s.' % data['Msg'])

    def test_register_002_existed_name(self):
        case = 'register a new user using a existed nickname'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # register a new user with the existed user's nickname
        email = 'test.%s@hypereal.com' % str(uuid.uuid4())[-8:]
        url = self.url_register
        payload = {
            "nickname": self.nickname[0],
            "email": email,
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": "Test1234"
        }
        print("url: %s\npayload: %s" % (url, payload))
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        data = rp.json()
        self.assertEqual(400, rp.status_code,'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('30004', data['errorCode'],
                         'Expected response: errorCode = 30004. Actual = %s.' % data['errorCode'])
        self.assertEqual('User nickname already exist', data['errorMsg'],
                         'Expected response: errorMsg = User nickname already exist. Actual = %s.' % data['errorMsg'])

    def test_register_003_existed_email(self):
        case = 'register a new user using a existed email'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # register a new user with the existed user's email and password
        nickname = str(uuid.uuid4())[-10:]
        url = self.url_register
        payload = {
            "nickname": nickname,
            "email": self.email[0],
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": self.password[0]
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        data = rp.json()
        self.assertEqual(400, rp.status_code,'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('30004', data['errorCode'],
                         'Expected response: errorCode = 30004. Actual = %s.' % data['errorCode'])
        self.assertEqual('User email already exist', data['errorMsg'],
                         'Expected response: errorMsg = User email already exist. Actual = %s.' % data['errorMsg'])

    def test_register_004_empty_name(self):
        case = 'register a new user using a empty nick name'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        nickname = ''
        email = 'test.%s@hypereal.com' % str(uuid.uuid4())[-8:]
        url = self.url_register
        payload = {
            "nickname": nickname,
            "email": email,
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": "Test1234"
        }
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code,'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('30008', data['errorCode'],
                         'Expected response: errorCode = 30008. Actual = %s.' % data['errorCode'])
        self.assertEqual('User name size should between 4 to 16 characters\n', data['errorMsg'],
                         'Expected response: errorMsg = User name size should between 4 to 16 characters = %s.' % data['errorMsg'])

    def test_register_005_empty_email(self):
        case = 'register a new user using a empty email'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        nickname = str(uuid.uuid4())[-10:]
        email = ''
        url = self.url_register
        payload = {
            "nickname": nickname,
            "email": email,
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": "Test1234"
        }
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code,'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('30008', data['errorCode'],
                         'Expected response: errorCode = 30008. Actual = %s.' % data['errorCode'])
        self.assertEqual('Invalid Email Address Format\n', data['errorMsg'],
                         'Expected response: errorMsg = Invalid Email Address Format. Actual = %s.' % data['errorMsg'])

    def test_register_006_illegal_email(self):
        case = 'register a new user using a illegal email address'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        nickname = str(uuid.uuid4())[-10:]
        email = 'test.hypreal.com'
        url = self.url_register
        payload = {
            "nickname": nickname,
            "email": email,
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": "Test1234"
        }
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code,
                         'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('30008', data['errorCode'],
                         'Expected response: errorCode = 30008. Actual = %s.' % data['errorCode'])
        self.assertEqual('Invalid Email Address Format\n', data['errorMsg'],
                         'Expected response: errorMsg = email parameter error. Actual = %s.' % data['errorMsg'])

    def test_register_007_too_long_name(self):
        case = 'register a new user using a very long nick name'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        nickname = str(uuid.uuid4()) + str(uuid.uuid4())
        email = 'test.%s@hypereal.com' % str(uuid.uuid4())[-8:]
        url = self.url_register
        payload = {
            "nickname": nickname,
            "email": email,
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": "Test1234"
        }
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code,
                         'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('30008', data['errorCode'],
                         'Expected response: errorCode = 30008. Actual = %s.' % data['errorCode'])
        self.assertEqual('User name size should between 4 to 16 characters\n', data['errorMsg'],
                         'Expected response: errorMsg = User name size should between 4 to 16 characters = %s.'
                         % data['errorMsg'])

    def test_register_008_too_short_name(self):
        case = 'register a new user using a very short nick name'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        nickname = str(uuid.uuid4())[-2:]
        email = 'test.%s@hypereal.com' % str(uuid.uuid4())[-8:]
        url = self.url_register
        payload = {
            "nickname": nickname,
            "email": email,
            "image_path": "1",
            "birthday": "1980-01-02",
            "gender": "M",
            "passphrase": "Test1234"
        }
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code,'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('30008', data['errorCode'],
                         'Expected response: errorCode = 30008. Actual = %s.' % data['errorCode'])
        self.assertEqual('User name size should between 4 to 16 characters', data['errorMsg'],
                         'Expected response: errorMsg = User name size should between 4 to 16 characters. Actual = %s.'
                         %data['errorMsg'])

    def test_login_001_correct_credential(self):
        case = 'Check user can login with correct email and password'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # login
        url = self.url_login
        payload = {
            "email": self.email[0],
            "passphrase": self.password[0]
        }
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual('login success', data['Msg'],
                         "Expected response: Msg = login success. Actual = %s." % data['Msg'])
        self.assertNotEqual('', data['token'],'Expected response: token != ''. Actual = %s.' % data['token'])

    def test_login_002_wrong_password(self):
        case = 'Check user can not login with correct email and wrong password'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # login with user's mobile but wrong password
        url = self.url_login
        payload = {
            "email": self.email[0],
            "passphrase": "pwd"
        }
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: %s \n" % response.text)
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual('30002', data['errorCode'],
                         'Expected response: errorCode = login success. Actual = %s.' % data['errorCode'])
        self.assertNotEquals(5, data['leftTimes'],
                             'Expected response: leftTimes != 5. Actual = %s.' % data['leftTimes'])
        self.assertEqual('login failed', data['errorMsg'],'Expected response: errorMsg = login success. Actual = %s.'
                         % data['errorMsg'])

    def test_login_003_wrong_email(self):
        case = 'Check user can not login with wrong email and correct password'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        url = self.url_login
        payload = {'email': 'email', 'passphrase': self.password[0]}
        response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: %s \n" % response.text)
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual('30001', data['errorCode'],
                         'Expected response: errorCode = login success. Actual = %s.' % data['errorCode'])
        self.assertEqual('no user', data['errorMsg'],
                         'Expected response: errorMsg = no user. Actual = %s.' % data['errorMsg'])

    def test_logout_001_correct_token(self):
        case = 'Logout with correct token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # logout
        url = self.url_oauth + self.get_login_token(self.email[0], self.password[0])
        response = requests.delete(url, headers=self.headers)
        time.sleep(1)
        print("url: %s" % url)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.'
                         % response.status_code)

    def test_logout_002_wrong_token(self):
        case = 'Logout with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        url = self.url_oauth + '123'
        response = requests.delete(url, headers=self.headers)
        data = response.json()
        time.sleep(1)
        print("url: %s" % url)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('10000', data['errorCode'],
                         'Expected response: errorCode = 10000. Actual = %s.' % data['errorCode'])
        self.assertEqual('token not found', data['errorMsg'],
                         'Expected response: errorMsg = token not found. Actual = %s.' % data['errorMsg'])

    def test_logout_003_empty_token(self):
        case = 'user logout with empty token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # logout with empty token
        url = self.url_oauth
        response = requests.delete(url, headers=self.headers)
        data = response.json()
        print("url: %s" % url)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('10000', data['errorCode'],
                         'Expected response: errorCode = 10000. Actual = %s.' % data['errorCode'])
        self.assertEqual('token not found', data['errorMsg'],
                         'Expected response: errorMsg = token not found. Actual = %s.' % data['errorMsg'])

    def test_query_user_role_001_general_user(self):
        case = 'test query role of general user'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # register a new user
        return_data = self.register_user()
        email = return_data['email']
        password = return_data['password']
        token = self.get_login_token(email, password)
        # query user role
        url_query_user_role = self.url_query_user_role + token
        rp = requests.get(url_query_user_role, headers=self.headers)
        rp_data = rp.json()
        print("url_query_user_role: %s\n" % url_query_user_role)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)
        self.assertEqual(0, len(rp_data['roles']),
                         "Expected roles length is 0. Actual = %s." % len(rp_data['roles']))

    def test_query_user_role_002_wrong_token(self):
        case = 'test query role of general user with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # get token
        token = self.get_login_token(self.email[0], self.password[0])
        # query user role
        url_query_user_role = self.url_query_user_role + token + '9527'
        rp = requests.get(url_query_user_role, headers=self.headers)
        rp_data = rp.json()
        print("url_query_user_role: %s\n" % url_query_user_role)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('30005', rp_data['errorCode'],
                         'Expected response: errorCode = 30005. Actual = %s.' % rp_data['errorCode'])
        self.assertEqual('user token check failed', rp_data['errorMsg'],
                         'Expected response: errorMsg = user token check failed. Actual = %s.' % rp_data['errorMsg'])


