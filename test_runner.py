import os
import argparse
from xmlrunner import XMLTestRunner

from Case.AccountTest import *
from Case.HealthTest import *
from Case.RoomTest import *
from Case.SessionTest import *
from Case.FirmwareTest import *
from Case.ShopTest import *
from Case.P2PServerTest import *
from Case.BigDataTest import *
from Case.DeveloperTest import *
from Case.GamgOrderTest import *
from Case.MembershipTest import *


def run_full_suite(env='dev', port=8080):
    # run full test cases under the specified env and port
    print('run full suite')
    account_test_cases = unittest.TestLoader().getTestCaseNames(AccountTest)
    health_test_case = unittest.TestLoader().getTestCaseNames(HealthTest)
    room_test_case = unittest.TestLoader().getTestCaseNames(RoomTest)
    session_test_case = unittest.TestLoader().getTestCaseNames(SessionTest)
    firmware_test_case = unittest.TestLoader().getTestCaseNames(FirmwareTest)
    shop_test_case = unittest.TestLoader().getTestCaseNames(ShopTest)
    p2p_test_case = unittest.TestLoader().getTestCaseNames(P2PServerTest)
    big_data_test_case = unittest.TestLoader().getTestCaseNames(BigDataTest)
    developer_test_case = unittest.TestLoader().getTestCaseNames(DeveloperTest)
    MembershipTest_test_case = unittest.TestLoader().getTestCaseNames(MembershipTest)
    GameOrderTest_test_case = unittest.TestLoader().getTestCaseNames(GameOrderTest)

    account_test_suite = unittest.TestSuite(AccountTest(case, env, port) for case in account_test_cases)
    health_test_suite = unittest.TestSuite(HealthTest(case, env, port) for case in health_test_case)
    room_test_suite = unittest.TestSuite(RoomTest(case, env, port) for case in room_test_case)
    session_test_suite = unittest.TestSuite(SessionTest(case, env, port) for case in session_test_case)
    firmware_test_suite = unittest.TestSuite(FirmwareTest(case, env, port) for case in firmware_test_case)
    shop_test_suite = unittest.TestSuite(ShopTest(case, env, port) for case in shop_test_case)
    p2p_test_suite = unittest.TestSuite(P2PServerTest(case, env, port) for case in p2p_test_case)
    big_data_test_suite = unittest.TestSuite(BigDataTest(case, env, port) for case in big_data_test_case)
    developer_test_suite = unittest.TestSuite(DeveloperTest(case, env, port) for case in developer_test_case)
    MembershipTest_test_suite = unittest.TestSuite(MembershipTest(case, env, port) for case in MembershipTest_test_case)
    GameOrderTest_test_suite = unittest.TestSuite(GameOrderTest(case, env, port) for case in GameOrderTest_test_case)

    suites = [account_test_suite, health_test_suite, room_test_suite, session_test_suite, firmware_test_suite,
              shop_test_suite, p2p_test_suite, big_data_test_suite, developer_test_suite, MembershipTest_test_suite,
              GameOrderTest_test_suite]

    for i in range(len(suites)):
        runner = XMLTestRunner(output=file('reports/report_' + str(i) + '.xml', 'w'))
        runner.run(suites[i])


def run_smoke_suite(env='dev', port=8080):
    # run smoke test cases under the specified env and port
    print('run smoke suite')
    account_test_cases = ['test_register_001_new_user']
    account_test_suite = unittest.TestSuite(AccountTest(case, env, port) for case in account_test_cases)
    suites = [account_test_suite]

    for i in range(len(suites)):
        runner = XMLTestRunner(output=file('reports/report_' + str(i) + '.xml', 'w'))
        runner.run(suites[i])


def run_suite(env, suite, port=8080):
    # run test cases under the specified test class and env and port
    print 'run suite'
    test_cases = unittest.TestLoader().getTestCaseNames(suite)
    suite = unittest.TestSuite(suite(case, env, port) for case in test_cases)
    runner = XMLTestRunner(output=file('reports/report.xml', 'w'))
    runner.run(suite)


def clean_reports():
    folder = 'reports'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print e


def main():
    parser = argparse.ArgumentParser(usage='Hypereal interface automation test')
    parser.add_argument('-e', '--env',
                        default='dev',
                        dest='env',
                        action='store',
                        type=str,
                        help='specify a server, dev or production. Default = dev')

    parser.add_argument('-p', '--port',
                        default='8080',
                        dest='port',
                        action='store',
                        type=str,
                        help='specify a port number. Default = 8080')

    parser.add_argument('-s', '--suite',
                        default='full',
                        dest='suite',
                        action='store',
                        type=str,
                        help='specify test type, smoke or full or specific test class. Default = full')

    args = parser.parse_args()

    env = args.env
    port = args.port
    suite = args.suite
    clean_reports()

    if suite == 'smoke':
        run_smoke_suite(env=env, port=port)
    elif suite == 'full':
        run_full_suite(env=env, port=port)
    else:
        s = globals()[suite]
        run_suite(env=env, port=port, suite=s)


if __name__ == '__main__':
    main()
