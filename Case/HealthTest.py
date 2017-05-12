import unittest
from Data.interface import *
import requests


class HealthTest(unittest.TestCase):
    def __init__(self, method_name=config['setting']['method_name'], env=config['setting']['environment'],
                 port=config['setting']['port']):
        super(HealthTest, self).__init__(method_name)
        self.env = env
        self.host = config[env]['base_url'] + ':' + str(port)
        self.url_health = self.host + config['api']['health']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # =========================================================================
    # Test Cases
    # =========================================================================
    def test_health_001(self):
        case = 'Check service health'
        print('Case ID: %s' % unittest.TestCase.id(self))
        print('Description: %s' % case)
        url = self.url_health
        print("url: %s" % url)
        response = requests.post(url)
        print("response: status_code is %s\n%s\n" % (response.status_code, response.text))
        self.assertEqual(200, response.status_code, 'Expected response code = 200. Actual = %s' % response.status_code)
