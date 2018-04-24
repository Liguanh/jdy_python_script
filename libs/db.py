#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
__author__ = 'Liguanh'

import pymysql
from warnings import filterwarnings

class Db(object):

    def __init__(self, db_config):

        #过滤pymysql的warning信息
        filterwarnings('ignore', category=pymysql.Warning)

        #core
        self.core_conn(db_config)

        #module
        self.module_conn(db_config)

    #连接核心库
    def core_conn(self,db_config):
        self.db = pymysql.connect(host=db_config['hostname'],
                                  user=db_config['user'],
                                  password=db_config['password'],
                                  db=db_config['core_db_name'],
                                  cursorclass=pymysql.cursors.DictCursor,
                                  charset=db_config['charset'],
                                  port=db_config['port'])
        self.cursor = self.db.cursor()
        charset_sql = "set names utf8"
        self.cursor.execute(charset_sql)

    #连接module库
    def module_conn(self, db_config):
        self.module_db = pymysql.connect(host=db_config['hostname'],
                                  user=db_config['user'],
                                  password=db_config['password'],
                                  db=db_config['module_db_name'],
                                  cursorclass=pymysql.cursors.DictCursor,
                                  charset=db_config['charset'],
                                  port=db_config['port'])
        self.module_cursor = self.module_db.cursor()
        charset_sql = "set names utf8"
        self.module_cursor.execute(charset_sql)


    # def __del__(self):
    #     self.cursor.close()
    #     self.db.close()

