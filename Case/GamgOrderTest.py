import unittest
import json
import requests
from Data.accounts import *
from Data.interface import *

class GameOrderTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(GameOrderTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.url_login = self.host + config['api']['account']['login']
        self.email = accounts[env]['customer'][5]['email']
        self.password = accounts[env]['customer'][5]['password']
        self.url_create_game_order = self.host + config['api']['GameOrder']['create_game_order']
        self.url_check_user_all_game = self.host + config['api']['GameOrder']['check_user_all_game']
        self.url_check_game_status = self.host + config['api']['GameOrder']['check_game_status']
        def get_login_token(self, email, password):
            url = self.url_login
            payload = {'email': email, 'passphrase': password}
            headers = {'content-type': "application/json"}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            token = response.json()['token']
            return token
        self.token = get_login_token(self, self.email, self.password)
        self.headers = {
            'content-type': "application/json",
            'Authorization': self.token
        }

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =========================================
    # Test Cases
    # =========================================
    def test_001_create_Game_order(self):
        case = 'create game order'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url = self.url_create_game_order
        payload = {
            "returnUrl": "http://www.hypereal.com",
            "sellableItemId": 2
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_002_null_returnUrl(self):
        case = 'returnUrl = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        returnUrl = ''
        url = self.url_create_game_order
        payload = {
            "returnUrl": returnUrl,
            "sellableItemId": 2
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_003_null_sellableItemId(self):
        case = 'sellableItemId = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        sellableItemId = ''
        url = self.url_create_game_order
        payload = {
            "returnUrl": "http://www.hypereal.com",
            "sellableItemId": sellableItemId
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(500, rp.status_code, 'Expected response code = 500. Actual = %s.' % rp.status_code)

    def test_004_error_sellableItemId(self):
        case = 'error sellableItemId'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        sellableItemId = '100'
        url = self.url_create_game_order
        payload = {
            "returnUrl": "http://www.hypereal.com",
            "sellableItemId": sellableItemId
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(500, rp.status_code, 'Expected response code = 500. Actual = %s.' % rp.status_code)

    def test_001_check_user_all_game(self):
        case = 'check List all ordered games by specific user'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url_check_user_all_game = self.url_check_user_all_game
        rp = requests.get(url_check_user_all_game, headers=self.headers)
        print("url_check_user_info: %s\n" % url_check_user_all_game)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_002_error_null_Authorization(self):
        case = 'Authorization = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        Authorization = ''
        headers = {
            'content-type': "application/json",
            'Authorization': Authorization
        }
        url_check_user_all_game = self.url_check_user_all_game
        rp = requests.get(url_check_user_all_game, headers=headers)
        print("url_check_user_info: %s\n" % url_check_user_all_game)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)

    def test_001_check_order_status(self):
        case = 'check game order status'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url_check_game_status = self.url_check_game_status + '2'
        rp = requests.get(url_check_game_status, headers=self.headers)
        print("url_check_user_info: %s\n" % url_check_game_status)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_002_error_null_orderid(self):
        case = 'orderid = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url_check_game_status = self.url_check_game_status
        rp = requests.get(url_check_game_status, headers=self.headers)
        print("url_check_user_info: %s\n" % url_check_game_status)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)

    def test_003_error_orderid(self):
        case = 'check game order status'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url_check_game_status = self.url_check_game_status + '100'
        rp = requests.get(url_check_game_status, headers=self.headers)
        print("url_check_user_info: %s\n" % url_check_game_status)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(500, rp.status_code, 'Expected response code = 500. Actual = %s.' % rp.status_code)



