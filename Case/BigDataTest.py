import unittest
import json
import requests
import time
import uuid
from Data.interface import *


class BigDataTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(BigDataTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.headers = {'content-type': "application/json"}
        self.url_register = self.host + config['api']['big_data']['register']
        self.url_upload = self.host + config['api']['big_data']['upload']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =========================================
    # Test Cases
    # =========================================
    def test_register_001_FirstRegister(self):
        case = 'register a new user with FirstRegister'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        url = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": "name",
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_register_002_RegisterAgain(self):
        case = 'register a new user with RegisterAgain'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        url = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": "name",
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        requests.post(url, data=json.dumps(payload), headers=self.headers)
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('70001', data['errorCode'], 'Expected state is up. Actual = %s.' % data['errorCode'])

    def test_register_003_Error_version(self):
        case = 'version = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        version = ""
        url = self.url_register
        payload = {
            "name": name,
            "version": version,
            "columns":
                [
                    {
                        "name": "name",
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('70004', data['errorCode'], 'Expected state is up. Actual = %s.' % data['errorCode'])

    def test_register_004_Error_ColumnsName(self):
        case = 'ColumnsName > 50 character'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        columns_name = "123456789012345678901234567890123456789012345678901"
        url = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": columns_name,
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(500, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('10000', data['errorCode'], 'Expected state is up. Actual = %s.' % data['errorCode'])

    def test_register_005_Error_ColumnsName(self):
        case = 'ColumnsName = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        columns_name = ""
        url = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": columns_name,
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('70004', data['errorCode'], 'Expected state is up. Actual = %s.' % data['errorCode'])

    def test_register_006_Error_ColumnsName2(self):
        case = 'ColumnsName2 > 50 character'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        columns_name2 = "123456789012345678901234567890123456789012345678901"
        url = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": "name",
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": columns_name2,
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(500, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('10000', data['errorCode'], 'Expected state is up. Actual = %s.' % data['errorCode'])

    def test_register_007_Error_ColumnsName2(self):
        case = 'ColumnsName = null'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        columns_name2 = ""
        url = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": "name",
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": columns_name2,
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\npayload: %s" % (url, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('70004', data['errorCode'], 'Expected state is up. Actual = %s.' % data['errorCode'])

    def test_data_UpLoad_001(self):
        case = 'UpLoad ok'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        url_register = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": "name",
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": ""
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url_register, data=json.dumps(payload), headers=self.headers)
        print("url_register: %s\npayload: %s" % (url_register, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # get user name
        url_upload = self.url_upload
        payload1 = {
            "table_name": name,
            "table_version": "1.0",
            "data":
                [
                    "JackMa,40",
                    "JeffBezos,33"
                ]
        }
        rp1 = requests.post(url_upload, data=json.dumps(payload1), headers=self.headers)
        print("url: %s\npayload1: %s" % (url_upload, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(200, rp1.status_code, 'Expected response code = 200. Actual = %s.' % rp1.status_code)

    def test_data_UpLoad_002_error_validator(self):
        case = 'error validator'
        print('Case ID: %s\n Description: %s' % (unittest.TestCase.id(self), case))
        name = str(uuid.uuid4())[-10:]
        validator = "123"
        url_register = self.url_register
        payload = {
            "name": name,
            "version": "1.0",
            "columns":
                [
                    {
                        "name": "name",
                        "type": "string",
                        "length": 100,
                        "column_sort": 1,
                        "validator": validator
                    },
                    {
                        "name": "age",
                        "type": "number",
                        "length": 3,
                        "column_sort": 2
                    }
                ]
        }
        rp = requests.post(url_register, data=json.dumps(payload), headers=self.headers)
        print("url: %s\n payload: %s" % (url_register, payload))
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        # get user name
        url_upload = self.url_upload
        payload1 = {
            "table_name": name,
            "table_version": "1.0",
            "data":
                [
                    "JackMa,40",
                    "JeffBezos,33"
                ]
        }
        rp1 = requests.post(url_upload, data=json.dumps(payload1), headers=self.headers)
        data = rp1.json()
        print("url: %s\npayload1: %s" % (url_upload, payload1))
        print("response: status_code is %s , %s\n" % (rp1.status_code, rp1.text))
        self.assertEqual(400, rp1.status_code, 'Expected response code = 400. Actual = %s.' % rp1.status_code)
        self.assertEqual('70004', data['errorCode'], 'Expected state is up. Actual = %s.' % data['errorCode'])
