#! /usr/bin/env python3
#! -*- coding:utf-8 -*-
__author__='Liguanh'

from libs.db import Db
from libs.common import Common
import datetime
import math

class RecordUcfRecharge(Db):

    def __init__(self, db_config):

        Db.__init__(self, db_config)

        common = Common()
        self.common = common

    #标示用户用先锋支付充值的银行卡信息
    def recordUcfRecharge(self):
        order='core_order'
        order_extend='core_order_extend'
        auth='core_auth_card'
        start_time=datetime.datetime.now()
        RECHARGE_UCFPAY_AUTH_TYPE=1104
        SUCCESS_STATUS = 200
        size = 500

        #获取每个用户最近用先锋支付渠道最新充值成功一笔记录id
        sql = '''select substring_index(group_concat(o.id order by success_time desc),',',1) as last_id from `%s` as o join `%s`  as e on o.order_id = e.order_id where e.type=%s and status=%s group by user_id''' % (order, order_extend, RECHARGE_UCFPAY_AUTH_TYPE, SUCCESS_STATUS)
        print(self.common.log_template%('SQL', sql))
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        #总条数
        total = len(result)

        print("about %s lines id data"%total)
        print("\n")

        #分页处理数据
        s_num = f_num = 0
        pages = math.ceil(total / size)
        for page in range(1, int(pages) +1):
            start = (page - 1) * size

            # 组装id字符串
            id_str = ','.join([str(item['last_id']) for item in result[start:start+size]])

            try:
                start = (page - 1) * size

                # 获取相应的每个用户最新的订单记录
                sql = '''select user_id, bank_id,card_number from `%s` as o join `%s`  as e on o.order_id = e.order_id where o.id in (%s)''' % (
                order, order_extend, id_str)

                print(self.common.log_template % ('SQL', sql))
                self.cursor.execute(sql)
                bank_info_list = self.cursor.fetchall()

                #循环更新ucf的标示
                if len(bank_info_list) > 0:
                    for bank_info in bank_info_list:
                        sql = '''update `%s` set if_ucf = 1 where user_id= %d and card_number = '%s' and bank_id =%d '''%(auth, bank_info['user_id'], bank_info['card_number'], bank_info['bank_id'])
                        print(self.common.log_template % ('SQL', sql))
                        self.cursor.execute(sql)
                        s_num = s_num + 1

                print('\n')
                self.db.commit()
            except Exception as e:
                f_num = f_num + 1
                print(self.common.log_template % ('Exception', str(e)))
                self.db.rollback()

        end_time = datetime.datetime.now()

        print("record ucf recharge data compelte! success %s lines , failed %s lines, spent about %s seconds"%(s_num, f_num, (end_time-start_time).seconds))







