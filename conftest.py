# -*- coding: utf-8 -*-
# @Time     : 2021/1/30 20:41
# @Author   : qtf
# File      : conftest.py
import pytest
import requests
from middleware.handler import Handler,MidDBHandler
from jsonpath import jsonpath

def login(phone,pwd):
    """登录。 得到 ID, token, leave_amount
    """
    user = {
        "mobile_phone":phone,
        "pwd":pwd
    }
    resp = requests.request(method='POST',
                    url=Handler.env_config["envurl"] + '/member/login',
                    headers={"X-Lemonban-Media-Type": "lemonban.v2"},
                    json=user
                     )
    resp_json = resp.json()

    token = jsonpath(resp_json, '$..token')[0]
    token_type = jsonpath(resp_json, '$..token_type')[0]
    id = jsonpath(resp_json, '$..id')[0]
    leave_amount = jsonpath(resp_json, '$..leave_amount')[0]

    token = " ".join([token_type, token])
    return {"id": id,
            "token": token,
            "leave_amount": leave_amount}

@pytest.fixture()
def admin_login():
    """管理员登录"""
    user = {
        "mobile_phone":Handler.user_config['admin_user']['phone'],
        "pwd":Handler.user_config['admin_user']['pwd']
    }
    return login(user['mobile_phone'],user['pwd'])

@pytest.fixture()
def loan_login():
    """借款人登录"""
    user = {
        "mobile_phone": Handler.user_config['loan_user']['phone'],
        "pwd": Handler.user_config['loan_user']['pwd']
    }
    return login(user['mobile_phone'], user['pwd'])

@pytest.fixture()
def add_loan(loan_login):
    headers = {
        "X-Lemonban-Media-Type": "lemonban.v2",
        "Authorization": loan_login["token"]
    }
    data = {
        "member_id": loan_login['id'],
        "title": "报名 Python 全栈自动化课程",
        "amount": 6300.00,
        "loan_rate": 12.0,
        "loan_term": 12,
        "loan_date_type": 1,
        "bidding_days": 5
    }
    resp = requests.request(method='POST',
                            url=Handler.env_config['envurl'] + '/loan/add',
                            headers=headers,
                            json=data)
    resp_json = resp.json()
    loan_id = jsonpath(resp_json,'$..id')[0]
    return loan_id

@pytest.fixture()
def db():
    """管理数据库链接的夹具"""
    db_conn = MidDBHandler()
    # db_conn = Handler.db_class
    yield db_conn
    db_conn.close()

# if __name__ == '__main__':
#     print(login())
#     print(type(login()['leave_amount']))