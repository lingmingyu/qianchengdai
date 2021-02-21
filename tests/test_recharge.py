# -*- coding: utf-8 -*-
# @Time     : 2021/1/28 22:01
# @Author   : qtf
# File      : test_recharge.py
import requests,pytest,json
from decimal import Decimal
from jsonpath import jsonpath
from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('Recharge')

@pytest.mark.parametrize('datas', excel_datas)
def test_recharge(datas):

    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    money_before = Decimal(0)
    if datas['expected'] == 0 and 'member_id' in datas['data']:
        sql = 'select leave_amount from member where id={}'.format(json.loads(datas['data'])['member_id'])
        result = Handler.db_class.query(sql,one=True)
        money_before = Decimal(result['leave_amount'])
        logger.info("充值前账号金额:{}".format(money_before))

    resp = requests.request(method=datas['method'],
                            url=Handler.env_config["envurl"] + datas['path'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['data']))
    try:
        assert resp.json()['code'] == datas['expected']
    except AssertionError as e:
        logger.info("code不正确,{}测试失败{}".format(datas["title"],e))
        raise e

    if resp.json()['code'] == 0 and 'member_id' in datas['data']:
        sql = 'select leave_amount from member where id={}'.format(json.loads(datas['data'])['member_id'])
        result = Handler.db_class.query(sql,one=True)
        money_after = result['leave_amount']
        money = Decimal(json.loads(datas['data'])['amount'])
        assert money_before + money == money_after
        logger.info("充值前账号金额{},充值金额{},充值后账户总金额{}".format(money_before,money,money_after))

    # 设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            # value = 'token'
            value = jsonpath(resp.json(), jsonpath_exp)[0]
            # setastr(Handler, "loan_token", "yfowepfpwefwoefowf"
            setattr(Handler, prop, value)
