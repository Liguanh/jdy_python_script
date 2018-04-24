#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
__author__ = 'Liguanh'

import urllib.request
import urllib.parse
import datetime
import json
import hashlib
import re

from .parser_yaml import ParserYaml

class Common(object):

    # 加密sign所用的key
    SECRET_KEY = 'xuN1mFEI3viLXMg7'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_extends_time= datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    log_template = timestamp + '  %s[%s]'

    def __init__(self, params = None):

        self.params = params

        parser_yaml = ParserYaml()
        self.url = parser_yaml.get_jdy_url_config()

    #post请求api
    def post_request(self):

        data = urllib.parse.urlencode(self.params)
        data = data.encode('utf8')

        request = urllib.request.Request(self.url)

        reponse = urllib.request.urlopen(request, data)

        reponse = reponse.read().decode('utf8')

        parsed_json = json.loads(reponse)

        return parsed_json


    # 获取请求url验证sign值,
    def getSign(self, params):
        str = ''

        for (key, val) in params.items():
            str += key + '=' + val + '&'

        str = str[0:-1] + self.SECRET_KEY

        gen_str = hashlib.md5(str.encode('utf8'))

        return gen_str.hexdigest()

    #检测手机号
    def checkPhone(self, phone):

        if not re.match(r'^(13\d|14[57]|15[012356789]|18\d|17[0135678]|19[89]|166)\d{8}$', str(phone)):
            raise ValueError('%s invalid phone number'%phone)

    #检测银行卡号
    def checkBankCard(self, card_no):
        length = len(card_no)

        if length <= 0:
            raise ValueError('card_no is empty')

        if not (length == 16 or length==17 or length==19 or re.match(r'^\d{18}$',card_no)) or not re.match(r'^\d*$', card_no):
            raise ValueError('%s invalid bank card no'%card_no)

    # 字符串转为驼峰格式
    def convert(self,string=None, flag='_'):
        convert_string = None

        if string is None:
            return convert_string

        string_list = string.split(flag)

        first = string_list[0].lower()
        others = string_list[1:]

        other_capital = [word.capitalize() for word in others]

        other_capital[0:0] = [first]

        convert_string = ''.join(other_capital)

        return convert_string