import unittest
import json
import requests
from Data.accounts import *
from Data.interface import *

class MembershipTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(MembershipTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.url_login = self.host + config['api']['account']['login']
        self.email = accounts[env]['customer'][5]['email']
        self.password = accounts[env]['customer'][5]['password']
        self.url_create_Membership_order = self.host + config['api']['Membership']['create_Membership_order']
        self.url_check_user_info = self.host + config['api']['Membership']['check_user_info']
        self.url_check_Membership_list = self.host + config['api']['Membership']['check_Membership_list']
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
    def test_001_create_Membership_order(self):
        case = 'create Membership order'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url = self.url_create_Membership_order
        payload = {
            "returnUrl": "http://www.hypereal.com",
            "sellableItemId": 1
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_002_null_returnUrl(self):
        case = 'returnUrl = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        returnUrl = ''
        url = self.url_create_Membership_order
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
        url = self.url_create_Membership_order
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
        url = self.url_create_Membership_order
        payload = {
            "returnUrl": "http://www.hypereal.com",
            "sellableItemId": sellableItemId
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(500, rp.status_code, 'Expected response code = 500. Actual = %s.' % rp.status_code)

    def test_001_check_user_info(self):
        case = 'check user info'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url_check_user_info = self.url_check_user_info
        rp = requests.get(url_check_user_info, headers=self.headers)
        print("url_check_user_info: %s\n" % url_check_user_info)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_002_null_Authorization(self):
        case = 'sellableItemId = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        Authorization = ''
        headers = {
            'content-type': "application/json",
            'Authorization': Authorization
        }
        url_check_user_info = self.url_check_user_info
        rp = requests.get(url_check_user_info, headers=headers)
        print("url_check_user_info: %s\n" % url_check_user_info)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)

    def test_001_check_all_sellableItems(self):
        case = 'check all sellableItems'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        url_check_Membership_list = self.url_check_Membership_list
        rp = requests.get(url_check_Membership_list, headers=self.headers)
        print("url_check_Membership_list: %s\n" % url_check_Membership_list)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)






