import unittest
import json
import requests
import time
import uuid
from Utils.DbHelper import *


class DeveloperTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(DeveloperTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.url_login = self.host + config['api']['account']['login']
        self.url_logout = self.host + config['api']['account']['logout']
        self.url_oauth = self.host + config['api']['oauth']
        self.url_register = self.host + config['api']['account']['register']
        self.email = accounts[env]['customer'][2]['email']
        self.password = accounts[env]['customer'][2]['password']
        self.headers = {'content-type': "application/json"}
        self.url_developer_dev = self.host + config['api']['developer_dev']['developer_dev']
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
    def test_developer_to_dev_001(self):
        case = 'test change developer to dev'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # register new user
        return_data = self.register_user()
        email = return_data['email']
        password = return_data['password']
        token = self.get_login_token(email, password)
        # change the user to dev
        url_developer_dev = self.url_developer_dev
        payload = {
            "token": token,
            "name": "1234567890151561",
            "cooperation": "capcom",
            "country": "JP",
            "state": "TKY",
            "city": "Tokyo",
            "address": "Coke",
            "zipcode": "123123123",
            "company_email": "123123",
            "website": "123123",
            "staff": "13123",
            "logo_url": "123123",
            "project_url": "123123",
            "project_year": "123123",
            "project_quarter": "123123",
            "project_type": "132123",
            "project_member": "123123",
            "has_pc": "12313",
            "project_brief": "123123",
            "real_name": "123123",
            "project_snapshots": ['http://www.capcom.com/mh2/snapshot1.png']
        }
        rp = requests.post(url_developer_dev, data=json.dumps(payload), headers=self.headers)
        data_rp = rp.json()
        print("url: %s\npayload: %s" % (url_developer_dev, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)
        self.assertEqual('apply ok', data_rp['Msg'],
                         'Expected response: Msg = apply ok. Actual = %s.' % data_rp['Msg'])

    def test_developer_to_dev_002_wrong_token(self):
        case = 'test change developer to dev with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # change the user to dev
        url_developer_dev = self.url_developer_dev
        payload = {
            "token": token + '9527',
            "name": "1234567890151561",
            "cooperation": "capcom",
            "country": "JP",
            "state": "TKY",
            "city": "Tokyo",
            "address": "Coke",
            "zipcode": "123123123",
            "company_email": "123123",
            "website": "123123",
            "staff": "13123",
            "logo_url": "123123",
            "project_url": "123123",
            "project_year": "123123",
            "project_quarter": "123123",
            "project_type": "132123",
            "project_member": "123123",
            "has_pc": "12313",
            "project_brief": "123123",
            "real_name": "123123",
            "project_snapshots": ['http://www.capcom.com/mh2/snapshot1.png']
        }
        rp = requests.post(url_developer_dev, data=json.dumps(payload), headers=self.headers)
        data_rp = rp.json()
        print("url: %s\npayload: %s" % (url_developer_dev, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('30005', data_rp['errorCode'],
                         'Expected response: errorCode = 30005. Actual = %s.' % data_rp['errorCode'])
        self.assertEqual('user token check failed', data_rp['errorMsg'],
                         'Expected response: errorMsg = user token check failed. Actual = %s.' % data_rp['errorMsg'])

    def test_developer_to_dev_003_already_applied(self):
        case = 'test change developer to dev'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # change the user to dev
        url_developer_dev = self.url_developer_dev
        payload = {
            "token": token,
            "name": "1234567890151561",
            "cooperation": "capcom",
            "country": "JP",
            "state": "TKY",
            "city": "Tokyo",
            "address": "Coke",
            "zipcode": "123123123",
            "company_email": "123123",
            "website": "123123",
            "staff": "13123",
            "logo_url": "123123",
            "project_url": "123123",
            "project_year": "123123",
            "project_quarter": "123123",
            "project_type": "132123",
            "project_member": "123123",
            "has_pc": "12313",
            "project_brief": "123123",
            "real_name": "123123",
            "project_snapshots": ['http://www.capcom.com/mh2/snapshot1.png']
        }
        requests.post(url_developer_dev, data=json.dumps(payload), headers=self.headers)
        rp = requests.post(url_developer_dev, data=json.dumps(payload), headers=self.headers)
        data_rp = rp.json()
        print("url: %s\npayload: %s" % (url_developer_dev, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('30102', data_rp['errorCode'],
                         'Expected response: errorCode = 30102. Actual = %s.' % data_rp['errorCode'])
        self.assertEqual('already applied', data_rp['errorMsg'],
                         'Expected response: errorMsg = already applied. Actual = %s.' % data_rp['errorMsg'])
