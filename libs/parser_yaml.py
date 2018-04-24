#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
__author__ = 'Liguanh'

import os
import yaml

class ParserYaml(object):

    def __init__(self, config_file='jdy_config.yml'):

        file_name = os.path.abspath(__file__)

        src_dirname = os.path.dirname(file_name)

        src_config_file = os.path.join(src_dirname, '../config', config_file)

        self.jdy_config = self.__loan_yaml_file(src_config_file)
        self.env = self.jdy_config['APP_ENV'].upper()

    # 解析yml配置文件
    def __loan_yaml_file(self, yaml_file):

        jdy_config = None

        if not os.path.exists(yaml_file):
            return jdy_config

        with open(yaml_file, 'r') as f:
            jdy_config = yaml.load(f)

        return jdy_config

    #获取九斗鱼的数据库配置
    def get_jdy_db_config(self):

        db_config = self.jdy_config['DB_' + self.env]

        return db_config

    #获取九斗鱼的借口请求域名
    def get_jdy_url_config(self):

        url = self.jdy_config['URL_'+self.env]

        return url

    #获取cardbin的配置信息
    def get_cardbin_config(self):

        cardbin_config = self.jdy_config['CARDBIN']

        return cardbin_config

    #获取得到bankid的方式
    def get_bank_id_method(self):

        methods = self.jdy_config['GET_BANKID_METHOD']

        return methods

