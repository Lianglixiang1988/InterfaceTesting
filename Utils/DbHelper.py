import MySQLdb
from Data.interface import *
from Data.accounts import *


class DbHelper(object):
    def __init__(self, env='dev'):
        self.host = config[env]['db_host']
        self.port = config[env]['db_port']
        self.schema = config[env]['db_schema']
        self.uid = accounts[env]['db'][0]['uid']
        self.pwd = accounts[env]['db'][0]['pwd']
        self.db = MySQLdb.connect(host=self.host, user=self.uid, passwd=self.pwd, db=self.schema, port=self.port)
        self.cursor = self.db.cursor()

    def query(self, sql='SELECT * FROM qa.web_sms'):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def update(self, sql=''):
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        self.cursor.close()
