# -*- coding: utf-8 -*-
# @Time     : 2021/2/1 22:35
# @Author   : qtf
# File      : handler.py
import os,random,re
from pymysql.cursors import DictCursor

from common.yaml_handler import read_yaml
from common.excel_handler import ExcelHandler
from common.db_handler import DBHandler
from config import path


class MidDBHandler(DBHandler):
    def __init__(self):
        db_path = os.path.join(path.config_path, 'db_config.yaml')
        db_config = read_yaml(db_path)

        super().__init__(host=db_config['db']['host'],
                         port=db_config['db']['port'],
                         user=db_config['db']['user'],
                         password=db_config['db']['password'],
                         # 不要写成utf-8
                         charset=db_config['db']['charset'],
                         # 指定数据库
                         database=db_config['db']['database'],
                         cursorclass=DictCursor)

class Handler():
    """任务：中间层。 common 和 调用层。
    使用项目的配置数据，填充common模块
    """
    env_path = os.path.join(path.config_path, 'env_config.yaml')
    env_config = read_yaml(env_path)

    user_path = os.path.join(path.config_path, 'user_config.yaml')
    user_config = read_yaml(user_path)

    db_path = os.path.join(path.config_path, 'db_config.yaml')
    db_config = read_yaml(db_path)

    # excel对象
    excel_file = os.path.join(path.data_path, 'case_datas.xlsx')
    excel = ExcelHandler(excel_file)

    # 数据库
    db_class = MidDBHandler()

    # 需要动态替换#...# 的数据
    investor_phone = user_config['investor_user']['phone']
    investor_pwd = user_config['investor_user']['pwd']
    loan_phone = user_config['loan_user']['phone']
    loan_pwd = user_config['loan_user']['pwd']
    admin_phone = user_config['admin_user']['phone']
    admin_pwd = user_config['admin_user']['pwd']
    wrong_member_id = '888888'
    wrong_loan_id = '888888'

    @classmethod
    def replace_data(cls, string, pattern='#(.*?)#'):
        """数据动态替换"""
        # pattern = '#(.*?)#'
        results = re.finditer(pattern=pattern, string=string)
        for result in results:
            # old= '#investor_phone#'
            old = result.group()
            # key = 'investor_phone'
            key = result.group(1)
            new = str(getattr(cls, key, ''))
            string = string.replace(old, new)
        return string

    # 生成手机号
    @classmethod
    def generate_new_phone(cls):
        while True:
            phone = '1' + random.choice(['3', '5', '8'])
            for i in range(9):
                num = random.randint(0, 9)
                phone += str(num)
            db = MidDBHandler()
            phone_in_db = db.query('SELECT * FROM member WHERE mobile_phone = {}'.format(phone))
            db.close()
            if not phone_in_db:
                cls.new_phone = phone
                return phone

# if __name__ == '__main__':
#     MidDBHandler()
    # YZHandler.logger.warning("可以正常使用吗？？")
    # h = Handler()
    # h.logger.warning("还可以吗？？")
    # print(Handler.generate_new_phone())
    # print(h.db_class.query("select leave_amount from member where mobile_phone='15558191960'",one=True))

# if __name__ == '__main__':
#     string = '{"mobile_phone": "#investor_phone#", "pwd": "#investor_pwd#", "mobile_phone": "#loan_phone#", "pwd": "#loan_pwd#", "mobile_phone": "#admin_phone#", "pwd": "#admin_pwd#"}'
#     a = Handler.replace_data(string)
#     print(a)

