# -*- coding: utf-8 -*-
# @Time     : 2021/1/18 21:38
# @Author   : qtf
# File      : db_handler.py
import pymysql
from pymysql.cursors import DictCursor

class DBHandler:
    def __init__(self,
                 host='',
                 port=3306,
                 user='',
                 password='',
                 # 不要写成utf-8
                 charset='utf8',
                 # 指定数据库
                 database='',
                 cursorclass=DictCursor
                 ):
        self.conn = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               password=password,
                               # 不要写成utf-8
                               charset=charset,
                               # 指定数据库
                               database=database,
                               cursorclass=cursorclass)


    def query_one(self,sql):
        self.cursor = self.conn.cursor()
        # 事务提交
        self.conn.commit()
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        self.cursor.close()
        return data

    def query_all(self,sql):
        self.cursor = self.conn.cursor()
        # 事务提交
        self.conn.commit()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.cursor.close()
        return data

    def query(self,sql,one=False):
        # 结果是个list
        if one:
            return self.query_one(sql)
        return self.query_all(sql)

    def close(self):
        # self.cursor.close()
        self.conn.close()

# db_sql = DBHandle().query("select leave_amount from member where mobile_phone='15558191960'",one=True)
# print(db_sql)

