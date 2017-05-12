import unittest
import json
import requests
import uuid
from Utils.DbHelper import *


class P2PServerTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(P2PServerTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.url_login = self.host + config['api']['account']['login']
        self.url_logout = self.host + config['api']['account']['logout']
        self.url_oauth = self.host + config['api']['oauth']
        self.url_register = self.host + config['api']['account']['register']
        self.email = accounts[env]['customer'][2]['email']
        self.password = accounts[env]['customer'][2]['password']
        self.headers = {'content-type': "application/json"}
        self.url_create_163_account = self.host + config['api']['p2p']['create']
        self.url_refresh = self.host + config['api']['p2p']['refresh']
        self.url_query = self.host + config['api']['p2p']['query']
        self.url_send_msg = self.host + config['api']['p2p']['send_msg']
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
    def test_create_163_account_001_new_user(self):
        case = 'test create a 163 account'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a 163 account using the newly created account's token
        url_create_163_account = self.url_create_163_account
        create_163_account_payload = {
            "token": token
        }
        create_163_account_rp = requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                                              headers=self.headers)
        print("url_create_163_account: %s\n create_163_account_payload: %s" % (
            url_create_163_account, create_163_account_payload))
        print("response: status_code is %s %s\n" % (create_163_account_rp.status_code, create_163_account_rp.text))
        self.assertEqual(200, create_163_account_rp.status_code,
                         'Expected response code = 200. Actual = %s.' % create_163_account_rp.status_code)

    def test_create_163_account_002_user_existed(self):
        case = 'test create a 163 account but the user already existed'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a 163 account using the newly created account's token
        url_create_163_account = self.url_create_163_account
        create_163_account_payload = {
            "token": token
        }
        requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                      headers=self.headers)
        create_163_account_rp = requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                                              headers=self.headers)
        data_create_163_account_rp = create_163_account_rp.json()
        print("url_create_163_account: %s\ncreate_163_account_payload: %s" % (
            url_create_163_account, create_163_account_payload))
        print("response: status_code is %s %s\n" % (create_163_account_rp.status_code, create_163_account_rp.text))
        self.assertEqual(400, create_163_account_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % create_163_account_rp.status_code)
        self.assertEqual('10000', data_create_163_account_rp['errorCode'],
                         'Expected response error code = 10000. Actual = %s.'
                         % data_create_163_account_rp['errorCode'])
        self.assertEqual('already created', data_create_163_account_rp['errorMsg'],
                         'Expected errorMsg is: already created. Actual = %s.' % data_create_163_account_rp['errorMsg'])

    def test_create_163_account_003_wrong_token(self):
        case = 'test create a 163 account with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a 163 account using the newly created account's token
        url_create_163_account = self.url_create_163_account
        create_163_account_payload = {
            "token": token + '9527'
        }
        create_163_account_rp = requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                                              headers=self.headers)
        data_create_163_account_rp = create_163_account_rp.json()
        print("url_create_163_account: %s\ncreate_163_account_payload: %s" % (
            url_create_163_account, create_163_account_payload))
        print("response: status_code is %s %s\n" % (create_163_account_rp.status_code, create_163_account_rp.text))
        self.assertEqual(400, create_163_account_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % create_163_account_rp.status_code)
        self.assertEqual('30005', data_create_163_account_rp['errorCode'],
                         'Expected response error code = 30005. Actual = %s.'
                         % data_create_163_account_rp['errorCode'])
        self.assertEqual('user token check failed', data_create_163_account_rp['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data_create_163_account_rp[
                             'errorMsg'])

    def test_refresh_account_001(self):
        case = 'test create a 163 account'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a 163 account using the newly created account's token
        url_create_163_account = self.url_create_163_account
        create_163_account_payload = {
            "token": token
        }
        requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                      headers=self.headers)
        url_refresh = self.url_refresh
        refresh_163_account_payload = {
            "token": token
        }
        refresh_163_account_rp = requests.post(url_refresh, data=json.dumps(refresh_163_account_payload),
                                               headers=self.headers)
        print("url_refresh: %s\nrefresh_163_account_payload: %s" % (
            url_refresh, refresh_163_account_payload))
        print("response: status_code is %s %s\n" % (refresh_163_account_rp.status_code, refresh_163_account_rp.text))

    def test_query_163_account_001(self):
        case = 'test query a 163 account'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a 163 account using the newly created account's token
        url_create_163_account = self.url_create_163_account
        create_163_account_payload = {
            "token": token
        }
        create_163_account_rp = requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                                              headers=self.headers)
        print("url_create_163_account: %s\ncreate_163_account_payload: %s" % (
            url_create_163_account, create_163_account_payload))
        print("response: status_code is %s %s\n" % (create_163_account_rp.status_code, create_163_account_rp.text))
        # query 163 account
        url_query = self.url_query + token
        query_rp = requests.get(url_query, headers=self.headers)
        print("url_query: %s\n" % url_query)
        print("response: status_code is %s %s\n" % (query_rp.status_code, query_rp.text))
        self.assertEqual(200, create_163_account_rp.status_code,
                         'Expected response code = 200. Actual = %s.' % create_163_account_rp.status_code)

    def test_query_163_account_002_wrong_token(self):
        case = 'test query a 163 account with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # create a 163 account using the newly created account's token
        url_create_163_account = self.url_create_163_account
        create_163_account_payload = {
            "token": token
        }
        create_163_account_rp = requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                                              headers=self.headers)
        print("url_create_163_account: %s\ncreate_163_account_payload: %s" % (
            url_create_163_account, create_163_account_payload))
        print("response: status_code is %s %s\n" % (create_163_account_rp.status_code, create_163_account_rp.text))
        # query 163 account
        url_query = self.url_query + token + '9527'
        query_rp = requests.get(url_query, headers=self.headers)
        data_query_rp = query_rp.json()
        print("url_query: %s\n" % url_query)
        print("response: status_code is %s %s\n" % (query_rp.status_code, query_rp.text))
        self.assertEqual(400, query_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % query_rp.status_code)
        self.assertEqual('30005', data_query_rp['errorCode'],
                         'Expected response error code = 30005. Actual = %s.' % data_query_rp['errorCode'])
        self.assertEqual('user token check failed', data_query_rp['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data_query_rp['errorMsg'])

    def test_query_163_account_002_not_created(self):
        case = 'test query a 163 account but the account has not been created yet'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # query 163 account
        url_query = self.url_query + token
        query_rp = requests.get(url_query, headers=self.headers)
        data_query_rp = query_rp.json()
        print("url_query: %s\n" % url_query)
        print("response: status_code is %s %s\n" % (query_rp.status_code, query_rp.text))
        self.assertEqual(400, query_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % query_rp.status_code)
        self.assertEqual('10000', data_query_rp['errorCode'],
                         'Expected response error code = 10000. Actual = %s.' % data_query_rp['errorCode'])
        self.assertEqual('no account', data_query_rp['errorMsg'],
                         'Expected errorMsg is: no account. Actual = %s.' % data_query_rp['errorMsg'])

    def test_send_msg_001(self):
        case = 'test batch send msg'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        user_id = self.get_user_id_by_email(self.email[0])
        # create a 163 account using account's token
        url_create_163_account = self.url_create_163_account
        create_163_account_payload = {
            "token": token
        }
        create_163_account_rp = requests.post(url_create_163_account, data=json.dumps(create_163_account_payload),
                                              headers=self.headers)
        data_create_163_account_rp = create_163_account_rp.json()
        print(create_163_account_rp.text)
        # send msg
        msg = 'test batch send msg'
        acc_token = data_create_163_account_rp['im_token']
        users = [].append(user_id)
        url_send_msg = self.url_send_msg
        payload_send_msg = {
            "token": token,
            "msg": msg,
            "acc_token": acc_token,
            "users": users
        }
        rp_send_msg = requests.post(url_send_msg, data=json.dumps(payload_send_msg), headers=self.headers)
        data_rp_send_msg = rp_send_msg.json()
        print("url_send_msg: %s\n" % url_send_msg)
        print("response: status_code is %s %s\n" % (rp_send_msg.status_code, rp_send_msg.text))
        self.assertEqual(200, rp_send_msg.status_code,
                         'Expected response code = 200. Actual = %s.' % rp_send_msg.status_code)
        self.assertEqual('send ok', data_rp_send_msg['Msg'],
                         'Expected response msg is send ok. Actual = %s.' % data_rp_send_msg['Msg'])
