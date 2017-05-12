import unittest
import json
import uuid
import requests
from Utils.DbHelper import *


class ShopTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(ShopTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.headers = {'content-type': "application/json"}
        self.url_register = self.host + config['api']['account']['register']
        self.url_login = self.host + config['api']['account']['login']
        self.url_refresh = self.host + config['api']['shop']['refresh']
        self.url_delete = self.host + config['api']['shop']['delete']
        self.url_query = self.host + config['api']['shop']['query']
        self.url_order = self.host + config['api']['shop']['order']
        self.url_update_order = self.host + config['api']['shop']['update_order']
        self.url_query_order = self.host + config['api']['shop']['query_order']
        self.url_query_order_detail = self.host + config['api']['shop']['query_order_detail']
        self.url_payment = self.host + config['api']['shop']['payment']
        self.url_query_payment = self.host + config['api']['shop']['query_payment']
        self.url_refunds = self.host + config['api']['shop']['refunds']
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
    def test_refresh_cart_item_001_one_item(self):
        case = 'refresh cart item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 1, "token": token}
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s\n" % response.status_code)
        data = response.json()
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual('update cart success', data['Msg'],
                         'Expected response: Msg = update cart success. Actual = %s.' % data['Msg'])

    def test_refresh_cart_item_002_two_item(self):
        case = 'refresh cart item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 2, "token": token}
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertEqual('update cart success', data['Msg'],
                         'Expected response: Msg = update cart success. Actual = %s.' % data['Msg'])

    def test_refresh_cart_item_003_item_not_exist(self):
        case = 'test refresh cart item, but the item does not exist'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_refresh
        payload = {"item_id": 9527, "amount": 2, "token": token}
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('60001', data['errorCode'], 'Expected response error code = 60001. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('no item', data['errorMsg'],
                         'Expected errorMsg is: no item. Actual = %s.' % data['errorMsg'])

    def test_refresh_cart_item_004_item_amount_float(self):
        case = 'test refresh cart item, but amount is float'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 0.3, "token": token}
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('10100', data['errorCode'], 'Expected response error code = 10100. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('amount error', data['errorMsg'],
                         'Expected errorMsg is: amount error. Actual = %s.' % data['errorMsg'])

    def test_refresh_cart_item_005_item_amount_negative_number(self):
        case = 'test refresh cart item, but the item does not exist'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_refresh
        payload = {"item_id": 2, "amount": -3, "token": token}
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('10100', data['errorCode'], 'Expected response error code = 10100. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('amount error', data['errorMsg'],
                         'Expected errorMsg is: amount error. Actual = %s.' % data['errorMsg'])

    def test_refresh_cart_item_006_wrong_token(self):
        case = 'test refresh cart item, but the item does not exist'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 3, "token": 9527}
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('30005', data['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('user token check failed', data['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data['errorMsg'])

    def test_refresh_cart_item_007_zero_item(self):
        case = 'refresh cart item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 0, "token": token}
        print("url: %s\npayload: %s" % (url, payload))
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        data = response.json()
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('10100', data['errorCode'], 'Expected response error code = 10100. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('amount error', data['errorMsg'],
                         'Expected errorMsg is: amount error. Actual = %s.' % data['errorMsg'])

    def test_delete_cart_item_001(self):
        case = 'test delete cart item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # refresh item
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 1, "token": token}
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        # delete item
        url_delete = self.url_delete + token + '&item_id=' + '2'
        rp2 = requests.delete(url_delete, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete: %s\n" % url_delete)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(200, rp2.status_code, 'Expected response code = 200. Actual = %s.' % rp2.status_code)
        self.assertEqual('delete ok', data_rp2['Msg'],
                         'Expected response: Msg = delete ok. Actual = %s.' % data_rp2['Msg'])

    def test_delete_cart_item_002_wrong_item(self):
        case = 'test delete cart item but the item does not exist'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # refresh item
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 1, "token": token}
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        # delete item
        url_delete = self.url_delete + token + '&item_id=' + '9527'
        rp2 = requests.delete(url_delete, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete: %s\n" % url_delete)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code, 'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10100', data_rp2['errorCode'], 'Expected response error code = 10100. Actual = %s.'
                         % data_rp2['errorCode'])
        self.assertEqual('no item', data_rp2['errorMsg'],
                         'Expected errorMsg is: no item. Actual = %s.' % data_rp2['errorMsg'])

    def test_delete_cart_item_003_wrong_token(self):
        case = 'test delete cart item with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # refresh item
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 1, "token": token}
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        # delete item
        url_delete = self.url_delete + token + '9527' + '&item_id=' + '2'
        rp2 = requests.delete(url_delete, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete: %s\n" % url_delete)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code, 'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('30005', data_rp2['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % data_rp2['errorCode'])
        self.assertEqual('user token check failed', data_rp2['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data_rp2['errorMsg'])

    def test_delete_cart_item_004_item_amount_is_zero(self):
        case = 'test delete cart item but the item amount is zero in cart'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[1], self.password[1])
        # delete item
        url_delete = self.url_delete + token + '&item_id=' + '2'
        rp2 = requests.delete(url_delete, headers=self.headers)
        data_rp2 = rp2.json()
        print("url_delete: %s\n" % url_delete)
        print("response: status_code is %s , %s\n" % (rp2.status_code, rp2.text))
        self.assertEqual(400, rp2.status_code, 'Expected response code = 400. Actual = %s.' % rp2.status_code)
        self.assertEqual('10100', data_rp2['errorCode'], 'Expected response error code = 10100. Actual = %s.'
                         % data_rp2['errorCode'])
        self.assertEqual('no item', data_rp2['errorMsg'],
                         'Expected errorMsg is: no item. Actual = %s.' % data_rp2['errorMsg'])

    def test_query_cart_item_001(self):
        case = 'test query cart item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # refresh cart item
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 1, "token": token}
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        # query cart info
        url_query = self.url_query + token
        query_rp = requests.get(url_query, headers=self.headers)
        print("url_query: %s\n" % url_query)
        print("response: status_code is %s\n" % query_rp.status_code)
        self.assertEqual(200, query_rp.status_code, 'Expected response code = 200. Actual = %s.' % query_rp.status_code)

    def test_query_cart_item_002_wrong_token(self):
        case = 'test query cart item with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # refresh cart item
        url = self.url_refresh
        payload = {"item_id": 2, "amount": 1, "token": token}
        response = requests.put(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (response.status_code, response.text))
        # query cart info
        url_query = self.url_query + token + '0'
        query_rp = requests.get(url_query, headers=self.headers)
        print("url_query: %s\n" % url_query)
        print("response: status_code is %s\n" % query_rp.status_code)
        self.assertEqual(400, query_rp.status_code, 'Expected response code = 400. Actual = %s.' % query_rp.status_code)

    def test_order_001(self):
        case = 'order 1 item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s.' % response.status_code)
        self.assertNotEqual('', data['order_no'],
                            'Expected response: order_no should != empty. Actual = %s' % data['order_no'])
        self.assertEqual(1, len(data['items']),
                         'Expected response: item count should = 1. Acutal = %s' % len(data['items']))
        self.assertEqual(amount, data['items'][0]['amount'],
                         'Expected response: item amount should = %s. Actual = %s.' % (
                             amount, data['items'][0]['amount']))
        self.assertEqual(item_id, data['items'][0]['item_id'],
                         'Expected response: item amount should = %s. Actual = %s.' % (
                             amount, data['items'][0]['item_id']))

    def test_order_001_wrong_item(self):
        case = 'order 1 item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        url_order = self.url_order
        payload = {'items': [{
            'amount': 1,
            'item_id': 99
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)

    def test_order_002_wrong_token(self):
        case = 'order 1 item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': 9527}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s, %s\n" % (response.status_code, response.text))
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('30005', data['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('user token check failed', data['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data['errorMsg'])

    def test_order_003_item_amount_float(self):
        case = 'order 1 item but the item number is float'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1.1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)
        self.assertEqual('60007', data['errorCode'], 'Expected response error code = 60007. Actual = %s.'
                         % data['errorCode'])
        self.assertEqual('id: 2 out of limit', data['errorMsg'],
                         'Expected errorMsg is: id: 2 out of limit. Actual = %s.' % data['errorMsg'])

    def test_order_004_item_amount_negative_number(self):
        case = 'order 1 item but the item number is negative number'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = -3
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        self.assertEqual(400, response.status_code, 'Expected response code = 400. Actual = %s.' % response.status_code)

    def test_update_order_001(self):
        case = 'test update an order'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print(data)
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        # update the order
        new_order_no = data['order_no']
        new_token = token
        new_address = "somewhere"
        new_city = 'sh'
        new_country = 'cn'
        new_province = 'sh'
        new_mobile = "18817712345"
        new_need_receipt = ''
        new_receipt = 'Tesla9527'
        url_update_order = self.url_update_order
        new_payload = {
            "order_no": new_order_no,
            "token": new_token,
            "address": new_address,
            "city": new_city,
            "country": new_country,
            "province": new_province,
            "mobile": new_mobile,
            "need_receipt": new_need_receipt,
            "receipt": new_receipt
        }
        rp_update = requests.put(url_update_order, data=json.dumps(new_payload), headers=self.headers)
        data_rp_update = rp_update.json()
        print("url_update_order: %s\n new_payload: %s" % (url_update_order, new_payload))
        print("response: status_code is %s\n" % rp_update.status_code)
        self.assertEqual(200, rp_update.status_code,
                         'Expected response code = 200. Actual = %s.' % rp_update.status_code)
        self.assertEqual(new_address, data_rp_update['address'],
                         'Expected response: new_address should = %s. Actual = %s' % (
                             new_address, data_rp_update['address']))
        self.assertEqual(new_city, data_rp_update['city'],
                         'Expected response: new_city should = %s. Actual = %s' % (
                             new_city, data_rp_update['city']))
        self.assertEqual(new_country, data_rp_update['country'],
                         'Expected response: new_country should = %s. Actual = %s' % (
                             new_country, data_rp_update['country']))
        self.assertEqual(new_province, data_rp_update['province'],
                         'Expected response: new_province should = %s. Actual = %s' % (
                             new_province, data_rp_update['province']))
        self.assertEqual(new_mobile, data_rp_update['mobile'],
                         'Expected response: new_mobile should = %s. Actual = %s' % (
                             new_mobile, data_rp_update['mobile']))
        self.assertEqual(new_need_receipt, data_rp_update['need_receipt'],
                         'Expected response: new_need_receipt should = %s. Actual = %s' % (
                             new_need_receipt, data_rp_update['need_receipt']))
        self.assertEqual(new_receipt, data_rp_update['receipt'],
                         'Expected response: new_receipt should = %s. Actual = %s' % (
                             new_receipt, data_rp_update['receipt']))

    def test_update_order_002_wrong_token(self):
        case = 'test update an order'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print(data)
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        # update the order
        new_order_no = data['order_no']
        new_token = token + '9527'
        new_address = "somewhere"
        new_city = 'sh'
        new_country = 'cn'
        new_province = 'sh'
        new_mobile = "18817712345"
        new_need_receipt = ''
        new_receipt = 'Tesla9527'
        url_update_order = self.url_update_order
        new_payload = {
            "order_no": new_order_no,
            "token": new_token,
            "address": new_address,
            "city": new_city,
            "country": new_country,
            "province": new_province,
            "mobile": new_mobile,
            "need_receipt": new_need_receipt,
            "receipt": new_receipt
        }
        rp_update = requests.put(url_update_order, data=json.dumps(new_payload), headers=self.headers)
        data_rp_update = rp_update.json()
        print("url_update_order: %s\n new_payload: %s" % (url_update_order, new_payload))
        print("response: status_code is %s\n" % rp_update.status_code)
        self.assertEqual(400, rp_update.status_code,
                         'Expected response code = 400. Actual = %s.' % rp_update.status_code)
        self.assertEqual('30005', data_rp_update['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % data_rp_update['errorCode'])
        self.assertEqual('user token check failed', data_rp_update['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data_rp_update['errorMsg'])

    def test_update_order_003_wrong_order_no(self):
        case = 'test update an order'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print(data)
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        # update the order
        new_order_no = data['order_no']
        new_token = token
        new_address = "somewhere"
        new_city = 'sh'
        new_country = 'cn'
        new_province = 'sh'
        new_mobile = "18817712345"
        new_need_receipt = ''
        new_receipt = 'Tesla9527'
        url_update_order = self.url_update_order
        new_payload = {
            "order_no": new_order_no + '9527',
            "token": new_token,
            "address": new_address,
            "city": new_city,
            "country": new_country,
            "province": new_province,
            "mobile": new_mobile,
            "need_receipt": new_need_receipt,
            "receipt": new_receipt
        }
        rp_update = requests.put(url_update_order, data=json.dumps(new_payload), headers=self.headers)
        data_rp_update = rp_update.json()
        print("url_update_order: %s\nnew_payload: %s" % (url_update_order, new_payload))
        print("response: status_code is %s\n" % rp_update.status_code)
        self.assertEqual(400, rp_update.status_code,
                         'Expected response code = 400. Actual = %s.' % rp_update.status_code)
        self.assertEqual('10000', data_rp_update['errorCode'], 'Expected response error code = 10000. Actual = %s.'
                         % data_rp_update['errorCode'])
        self.assertEqual('no order', data_rp_update['errorMsg'],
                         'Expected errorMsg is: no order. Actual = %s.' % data_rp_update['errorMsg'])

    def test_query_order_001(self):
        case = 'order 1 item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        # query the newly added order
        url_query_order = self.url_query_order + token
        rp_query_order = requests.get(url_query_order, headers=self.headers)
        data_rp_query_order = rp_query_order.json()
        print("url_query_order: %s\n" % url_query_order)
        print("response: status_code is %s\n" % rp_query_order.status_code)
        self.assertEqual(200, rp_query_order.status_code,
                         'Expected response code = 200. Actual = %s.' % rp_query_order.status_code)
        self.assertEqual(data['order_no'], data_rp_query_order['orders'][0]['order_no'],
                         'Expected response order no is %s. Actual = %s.' % (
                             data['order_no'], data_rp_query_order['orders'][0]['order_no']))

    def test_query_order_002_wrong_token(self):
        case = 'order 1 item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        # query the newly added order
        url_query_order = self.url_query_order + token + '9527'
        rp_query_order = requests.get(url_query_order, headers=self.headers)
        data_rp_query_order = rp_query_order.json()
        print("url_query_order: %s\n" % url_query_order)
        print("response: status_code is %s\n" % rp_query_order.status_code)
        self.assertEqual(400, rp_query_order.status_code,
                         'Expected response code = 400. Actual = %s.' % rp_query_order.status_code)
        self.assertEqual('30005', data_rp_query_order['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % data_rp_query_order['errorCode'])
        self.assertEqual('user token check failed', data_rp_query_order['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data_rp_query_order[
                             'errorMsg'])

    def test_query_order_003_no_order(self):
        case = 'order 1 item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[1], self.password[1])
        # query order
        url_query_order = self.url_query_order + token
        rp_query_order = requests.get(url_query_order, headers=self.headers)
        data_rp_query_order = rp_query_order.json()
        print("url_query_order: %s\n" % url_query_order)
        print("response: status_code is %s\n" % rp_query_order.status_code)
        print(data_rp_query_order)
        print(len(data_rp_query_order['orders']))
        self.assertEqual(200, rp_query_order.status_code,
                         'Expected response code = 200. Actual = %s.' % rp_query_order.status_code)
        self.assertEqual(0, len(data_rp_query_order['orders']),
                         'Expected response order length is 0. Actual = %s.' % len(data_rp_query_order['orders']))

    def test_query_order_detail_001(self):
        case = 'order 1 item'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        print("url: %s\npayload: %s" % (url_order, payload))
        print("response: status_code is %s\n" % response.status_code)
        # query the newly added order detail into
        url_query_order_detail = self.url_query_order_detail + data['order_no'] + '&token=' + token
        rp_query_order_detail = requests.get(url_query_order_detail, headers=self.headers)
        data_rp_query_order_detail = rp_query_order_detail.json()
        print("url_query_order_detail: %s\n" % url_query_order_detail)
        print("response: status_code is %s\n" % rp_query_order_detail.status_code)
        self.assertEqual(200, rp_query_order_detail.status_code,
                         'Expected response code = 200. Actual = %s.' % rp_query_order_detail.status_code)
        self.assertEqual(data['order_no'], data_rp_query_order_detail['order_no'],
                         'Expected response order no is %s. Actual = %s.' % (
                             data['order_no'], data_rp_query_order_detail['order_no']))

    def test_payment_001(self):
        case = 'test make a payment'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        self.assertEqual(200, payment_rp.status_code,
                         'Expected response code = 200. Actual = %s.' % payment_rp.status_code)
        self.assertNotEqual('', data_payment_rp['alipay_url'],
                            'Expected response: url should != empty. Actual = %s' % data_payment_rp['alipay_url'])

    def test_payment_002_wrong_token(self):
        case = 'test make a payment'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token + '9527',
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        self.assertEqual(400, payment_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % payment_rp.status_code)
        self.assertEqual('30005', data_payment_rp['errorCode'], 'Expected response error code = 30005. Actual = %s.'
                         % data_payment_rp['errorCode'])
        self.assertEqual('user token check failed', data_payment_rp['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data_payment_rp['errorMsg'])

    def test_payment_003_wrong_order_no(self):
        case = 'test make a payment'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'] + '9527',
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        self.assertEqual(400, payment_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % payment_rp.status_code)
        self.assertEqual('10000', data_payment_rp['errorCode'],
                         'Expected response: errorCode = 10000. Actual = %s' % data_payment_rp['errorCode'])
        self.assertEqual('no order', data_payment_rp['errorMsg'],
                         'Expected response: errorMsg = no order. Actual = %s' %
                         data_payment_rp['errorMsg'])

    def test_payment_004_two_requests(self):
        case = 'test make a payment'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment and request twice
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        self.assertEqual(200, payment_rp.status_code,
                         'Expected response code = 200. Actual = %s.' % payment_rp.status_code)
        self.assertNotEqual('', data_payment_rp['alipay_url'],
                            'Expected response: url should != empty. Actual = %s' % data_payment_rp['alipay_url'])

    def test_payment_005_fee_negative(self):
        case = 'test make a payment with negative fee'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": -1,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        self.assertEqual(400, payment_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % payment_rp.status_code)

    def test_query_payment_001(self):
        case = 'test query a payment'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        # query the newly created payment
        url_query_payment = self.url_query_payment + token + '&order_no=' + data['order_no']
        query_payment_rp = requests.get(url_query_payment, headers=self.headers)
        print("url_query_payment: %s\n" % url_query_payment)
        print("response: status_code is %s %s\n" % (query_payment_rp.status_code, query_payment_rp.text))
        data_query_payment_rp = query_payment_rp.json()
        self.assertEqual(200, query_payment_rp.status_code,
                         'Expected response code = 200. Actual = %s.' % query_payment_rp.status_code)

    def test_query_payment_002_no_payment(self):
        case = 'test query a payment but user has not make the payment yet'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # query the newly created payment
        url_query_payment = self.url_query_payment + token + '&order_no=' + data['order_no']
        query_payment_rp = requests.get(url_query_payment, headers=self.headers)
        print("url_query_payment: %s\n" % url_query_payment)
        print("response: status_code is %s %s\n" % (query_payment_rp.status_code, query_payment_rp.text))
        data_query_payment_rp = query_payment_rp.json()
        self.assertEqual(400, query_payment_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % query_payment_rp.status_code)
        self.assertEqual('10000', data_query_payment_rp['errorCode'],
                         'Expected response error code = 10000. Actual = %s.'
                         % data_query_payment_rp['errorCode'])
        self.assertEqual('no such order', data_query_payment_rp['errorMsg'],
                         'Expected errorMsg is: no such order. Actual = %s.' % data_query_payment_rp[
                             'errorMsg'])

    def test_query_payment_003_wrong_token(self):
        case = 'test query a payment with wrong token'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        # query the newly created payment
        url_query_payment = self.url_query_payment + token + '9527' + '&order_no=' + data['order_no']
        query_payment_rp = requests.get(url_query_payment, headers=self.headers)
        print("url_query_payment: %s\n" % url_query_payment)
        print("response: status_code is %s %s\n" % (query_payment_rp.status_code, query_payment_rp.text))
        data_query_payment_rp = query_payment_rp.json()
        self.assertEqual(400, query_payment_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % query_payment_rp.status_code)
        self.assertEqual('30005', data_query_payment_rp['errorCode'],
                         'Expected response error code = 30005. Actual = %s.'
                         % data_query_payment_rp['errorCode'])
        self.assertEqual('user token check failed', data_query_payment_rp['errorMsg'],
                         'Expected errorMsg is: user token check failed. Actual = %s.' % data_query_payment_rp[
                             'errorMsg'])

    def test_query_payment_004_wrong_order(self):
        case = 'test query a payment with wrong order no'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        # query the newly created payment
        url_query_payment = self.url_query_payment + token + '&order_no=' + data['order_no'] + '9527'
        query_payment_rp = requests.get(url_query_payment, headers=self.headers)
        print("url_query_payment: %s\n" % url_query_payment)
        print("response: status_code is %s %s\n" % (query_payment_rp.status_code, query_payment_rp.text))
        data_query_payment_rp = query_payment_rp.json()
        self.assertEqual(400, query_payment_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % query_payment_rp.status_code)
        self.assertEqual('10000', data_query_payment_rp['errorCode'],
                         'Expected response error code = 10000. Actual = %s.'
                         % data_query_payment_rp['errorCode'])
        self.assertEqual('no such order', data_query_payment_rp['errorMsg'],
                         'Expected errorMsg is: no such order. Actual = %s.' % data_query_payment_rp[
                             'errorMsg'])

    def test_refunds_payment_001_order_not_paid(self):
        case = 'test refunds payment but order not paid'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        token = self.get_login_token(self.email[0], self.password[0])
        # order 1 item
        amount = 1
        item_id = 2
        url_order = self.url_order
        payload = {'items': [{
            'amount': amount,
            'item_id': item_id
        }],
            'token': token}
        response = requests.post(url_order, data=json.dumps(payload), headers=self.headers)
        data = response.json()
        # make a payment
        url_payment = self.url_payment
        payment_payload = {
            "token": token,
            "order_no": data['order_no'],
            "subject": "description of the order",
            "total_fee": 22.00,
            "body": "description of the products,exp:2*HMD,2*Controller"
        }
        payment_rp = requests.post(url_payment, data=json.dumps(payment_payload), headers=self.headers)
        data_payment_rp = payment_rp.json()
        print("url_payment: %s %s\n" % (url_payment, payment_payload))
        print("response: status_code is %s %s\n" % (payment_rp.status_code, payment_rp.text))
        # refund the payment
        url_refunds = self.url_refunds
        refunds_payload = {
            "token": token,
            "order_no": data['order_no'],
            "total_fee": 0.01,
            "reason": "test"
        }
        refunds_rp = requests.post(url_refunds, data=json.dumps(refunds_payload), headers=self.headers)
        data_refunds_rp = refunds_rp.json()
        print("url_refunds: %s %s\n" % (url_refunds, refunds_payload))
        print("response: status_code is %s %s\n" % (refunds_rp.status_code, refunds_rp.text))
        self.assertEqual(400, refunds_rp.status_code,
                         'Expected response code = 400. Actual = %s.' % refunds_rp.status_code)
        self.assertEqual('60009', data_refunds_rp['errorCode'],
                         'Expected response error code = 60009. Actual = %s.'
                         % data_refunds_rp['errorCode'])
        self.assertEqual('order not paid', data_refunds_rp['errorMsg'],
                         'Expected errorMsg is: order not paid. Actual = %s.' % data_refunds_rp[
                             'errorMsg'])
