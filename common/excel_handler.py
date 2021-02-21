# -*- coding: utf-8 -*-
# @Time     : 2021/1/17 12:35
# @Author   : qtf
# File      : excel_handler.py
import openpyxl

class ExcelHandler:
    def __init__(self, fpath):
        self.fpath = fpath

    def read(self, sheet_name):
        """读取数据"""
        # 打开文件
        wb = openpyxl.open(self.fpath)
        # 获取表格
        ws = wb[sheet_name]
        data = list(ws.values)
        # 关闭文件
        wb.close()
        header = data[0]
        all_data = []
        for row in data[1:]:
            row_dict = dict(zip(header, row))
            all_data.append(row_dict)
        return all_data

    def write(self, sheet_name, data, row, column):
        """写入excel数据"""
        wb = openpyxl.load_workbook(self.fpath)
        # 获取表格
        ws = wb[sheet_name]
        ws.cell(row=row, column=column).value = data
        # 通过workbook 保存和关闭
        wb.save(self.fpath)
        wb.close()

# if __name__ == '__main__':
#     xls = ExcelHandler('cases.xlsx')
#     excel_data = xls.read('register')
#     # excel_data
#     print(excel_data)