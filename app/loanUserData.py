#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
__author__ = 'Liguanh'

from libs.db import Db
from libs.parser_file import ParserFile
from libs.common import Common
from libs.parser_yaml import ParserYaml
import datetime
import socket

class LoanUserData(Db):

    def __init__(self, db_config, file = None):

        Db.__init__(self, db_config)

        self.file = file

        common = Common()
        self.common = common

    #导入借款人用户的相关操作
    def importLoanUser(self):

        core_user='core_user'
        core_auth_card='core_auth_card'
        core_bank_card='core_bank_card'
        module_user = 'module_user_info'
        module_identy = 'module_identity_card'

        parserFile = ParserFile('../storages/files/'+self.file)
        start_time = datetime.datetime.now()
        #获取解析的execl文件的内容
        execl_data = parserFile.parser_execl()

        if execl_data is None:
            print(self.common.log_template%('Error', 'execl is empty！'))

        j = m =  0
        faild_loan_user = []

        # 获取银行卡ID方法
        parser_yaml = ParserYaml()
        methods = parser_yaml.get_bank_id_method()

        for i in range(1, execl_data.nrows):
            try:
                # 获取每一行的数据
                line = execl_data.row_values(i)

                if line is None:
                    continue

                #检测手机号
                self.common.checkPhone(int(line[2]))

                # 插入用户表借款人信息
                sql = '''insert into `%s` (phone, real_name, identity_card,password_hash,trading_password, note) VALUES ('%s', '%s', '%s','','','jx_loan_user')''' % (core_user,
                int(line[2]), line[0], line[1])
                print(self.common.log_template % ('SQL', sql))
                self.cursor.execute(sql)

                # 获取最新的ID信息
                sql = '''select last_insert_id() as id'''
                print(self.common.log_template % ('SQL', sql))
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                print(self.common.log_template % ('Get the auto_increment user_id', result['id']))

                # 获取银行卡ID
                func = 'getBankIdBy'+methods
                bank_id = getattr(self, func)(line[3])
                # 插入到充值银行卡表中
                sql = '''insert into `%s` (user_id, bank_id, card_number, created_at, updated_at) VALUES (%d,%d,'%s','%s', '%s')''' % (core_auth_card,
                result['id'], bank_id, line[3], self.common.timestamp, self.common.timestamp)
                print(self.common.log_template % ('SQL', sql))
                self.cursor.execute(sql)

                # 插入到提现银行卡表中
                sql = '''insert into `%s` (user_id, bank_id, card_number, created_at, updated_at) VALUES (%d,%d, '%s','%s', '%s')''' % (core_bank_card,
                result['id'], bank_id, line[3],self.common.timestamp,self.common.timestamp)
                print(self.common.log_template % ('SQL', sql))
                self.cursor.execute(sql)

                self.db.commit()

                # 插入到user_info
                sql = ''' insert into `%s` (username, user_id, ip, source_code) VALUES ('%s', %d, '%s',1)''' % (
                    module_user, int(line[2]), result['id'], socket.gethostbyname(socket.gethostname()))
                print(self.common.log_template % ('SQL', sql))
                self.module_cursor.execute(sql)

                # 插入到identity_card表中
                sql = '''insert into `%s` (name, identity_card) VALUES ('%s', '%s')''' % (
                    module_identy, line[0], line[1])
                print(self.common.log_template % ('SQL', sql))
                self.module_cursor.execute(sql)

                self.module_db.commit()
                j = j + 1
                print("\n")
            except Exception as e:
                print(self.common.log_template % ('Exception', str(e)))
                m = m + 1
                line.append(str(e))
                faild_loan_user.append(line)
                self.db.rollback()
                self.module_db.rollback()

        #失败的信息导出
        if len(faild_loan_user) > 0:

            faild_loan_user.insert(0,['姓名','身份证号','手机','银行卡号','失败原因'])

            parserFile = ParserFile('../storages/files/failed_loan_user_%s.xls'%self.common.file_extends_time)
            parserFile.export_data_to_execl(faild_loan_user)

            print(self.common.log_template%('msg', 'failed data export compelete!'))

        end_time = datetime.datetime.now()

        print("insert loan user data compelete, successly %s lines, faild %s lines, total %s lines, spent about %s seconds"%(j,m,execl_data.nrows-1, (end_time-start_time).seconds))

    #通过Url获取银行id信息
    def getBankIdByUrl(self, card_no = None):

        if card_no is None:
            return

        #获取接口请求签名
        params = {'card_no': card_no}
        sign = self.common.getSign(params)
        params['sign'] = sign

        #请求接口
        common = Common(params)
        reponse = common.post_request()
        print(self.common.log_template%('jdy_url:'+common.url+'reponse data', reponse))

        #获取cardbin的配置
        parser_yaml = ParserYaml()
        cardbin_config = parser_yaml.get_cardbin_config()

        bank_id = 0

        if reponse['code'] == 200:
            bank_id = cardbin_config[reponse['data']['bank_code']]

        return bank_id

    #通过本地的数据库获取银行卡id信息
    def getBankIdByDb(self, card_no = None):

        if len(card_no) <=0:
            return

        try:
            card_no = card_no.replace(' ', '')

            self.common.checkBankCard(card_no)

            verify_code = card_no[0:6]

            sql = '''select verify_code, bin from module_bank_cardbin where verify_code = '%s' '''%verify_code
            print(self.common.log_template%('SQL', sql))
            self.module_cursor.execute(sql)

            result = self.module_cursor.fetchone()
        except Exception as e:
            print(self.common.log_template%('error_msg', str(e)))


        # 获取cardbin的配置
        parser_yaml = ParserYaml()
        cardbin_config = parser_yaml.get_cardbin_config()

        bank_id = cardbin_config[result['bin']]

        return bank_id













