#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
__author__ = 'Liguanh'

import argparse

from app.loanUserData import LoanUserData
from libs.parser_yaml import ParserYaml
from libs.common import Common
from app.recordUcfRecharge import RecordUcfRecharge

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="jiudouyu scripts")

    parser.add_argument('--user', metavar='import_loan_user', help="import user info from execl file", nargs=1, required=False)
    parser.add_argument('--file', metavar='filename', help="input the file you want parser", nargs=1, required=False)
    parser.add_argument('--order', metavar="record_ucf_recharge", help="find the new ucf recharge and sign it", nargs=1, required=False)

    args = parser.parse_args()

    #解析ymal配置文件
    parserYmal = ParserYaml()
    db_config = parserYmal.get_jdy_db_config()

    common = Common()
    #导入借款人信息
    if args.user and args.file:
        getattr(LoanUserData(db_config, args.file[0]), common.convert(args.user[0]))()


    #先锋充值订单处理
    if args.order:
        getattr(RecordUcfRecharge(db_config), common.convert(args.order[0]))()


