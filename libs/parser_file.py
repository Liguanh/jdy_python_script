#!/usr/bin/env python3
#! -*- coding:utf-8 -*-
__author__ = 'Liguanh'

import os
import xlrd,xlwt

class ParserFile(object):

    def __init__(self, file_name = None):

        self.file = self.get_file(file_name)

    #获取要解析的文件的名称
    def get_file(self, file_name = None):

        if file_name is None:
            print("filename is empty, please input your import file")
            exit()

        self_name = os.path.abspath(__file__)
        self_dirname = os.path.dirname(self_name)

        return os.path.join(self_dirname,file_name)

    #解析execl文件
    def parser_execl(self):

        if not os.path.exists(self.file):
            print("%s is not exists"%self.file)
            exit()
        try:
            data =xlrd.open_workbook(self.file)
            return data.sheet_by_index(0)
        except Exception as e:
            print(str(e))

    #获取PHP的配置文件
    def get_php_config_file(self):

        with open(self.file, 'r') as f:
            file_content = f.read()

        return file_content

    #导出数据到execl文件中
    def export_data_to_execl(self, data):

        if data is  None:
            return False

        workbook = xlwt.Workbook(encoding='ascii')

        worksheet = workbook.add_sheet('Sheet1')

        for i in range(len(data)):
            for j in range(len(data[i])):
                worksheet.write(i,j, data[i][j])

        workbook.save(self.file)