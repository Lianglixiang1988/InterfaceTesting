import unittest
import json
from Data.interface import *
import requests


class FirmwareTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(FirmwareTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.headers = {'content-type': "application/json"}
        self.url_get_firmware = self.host + config['api']['firmware']['get_firmware']
        self.url_create_firmware = self.host + config['api']['firmware']['create_firmware']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =========================================
    # Test Cases
    # =========================================
    def test_get_firmware_001_get_latestversion(self):
        case = 'get latest firmware version'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        url = self.url_get_firmware
        rp = requests.get(url, headers=self.headers)
        print("url: %s\n" % url)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)

    def test_create_firmware_001_correct_secret(self):
        case = 'test create the latest firmware file with correct secret'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        url = self.url_create_firmware
        payload = {"secret": "N3Ld6PpBKd0vwUtywQ63", "bucket": "hyperfw", "file_path": "v3.2/hmd-v3.2-s1292.dfu",
                   "endpoint": "oss-cn-shenzhen.aliyuncs.com", "type": "hmd", "device": "dfu",
                   "pid": "pid", "version": "V3.2", "md5": "82e4777533900867cecb33e4b0e605ba"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\n" % url)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(200, rp.status_code, 'Expected response code = 200. Actual = %s.' % rp.status_code)
        self.assertEqual('add version ok', data['Msg'],
                         'Expected response Msg is add version ok. Actual = %s.' % data['Msg'])

    def test_create_firmware_002_wrong_secret(self):
        case = 'test create the latest firmware file with wrong secret'
        print('Case ID: %s\nDescription: %s' % (unittest.TestCase.id(self), case))
        url = self.url_create_firmware
        payload = {"secret": "xxxxxxxxx", "bucket": "hyperfw", "file_path": "v3.2/hmd-v3.2-s1292.dfu",
                   "endpoint": "oss-cn-shenzhen.aliyuncs.com", "type": "hmd", "device": "dfu",
                   "pid": "pid", "version": "V3.2", "md5": "82e4777533900867cecb33e4b0e605ba"}
        rp = requests.post(url, data=json.dumps(payload), headers=self.headers)
        data = rp.json()
        print("url: %s\n" % url)
        print("response: status_code is %s , %s\n" % (rp.status_code, rp.text))
        self.assertEqual(400, rp.status_code, 'Expected response code = 400. Actual = %s.' % rp.status_code)
        self.assertEqual('10000', data['errorCode'],
                         'Expected response errorCode is 10000. Actual = %s.' % data['errorCode'])
        self.assertEqual('parameter check failed', data['errorMsg'],
                         'Expected response errorMsg is parameter check failed. Actual = %s.' % data['errorMsg'])
