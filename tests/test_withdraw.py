# -*- coding: utf-8 -*-
# @Time     : 2021/1/31 11:32
# @Author   : qtf
# File      : test_withdraw.py
from decimal import Decimal
import requests,pytest,json
from jsonpath import jsonpath
from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('Withdraw')

@pytest.mark.parametrize('datas', excel_datas)
def test_withdraw(datas):

    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    if json.loads(datas['expected'])['code'] == 1002:
        datas['data'] = datas['data'].replace(str(json.loads(datas['data'])['amount']), str(json.loads(datas['data'])['amount'] + 1))

    money_before = Decimal(0)
    if json.loads(datas['expected'])['code'] in (0,1002) and 'member_id' in datas['data']:
        sql = 'select leave_amount from member where id={}'.format(json.loads(datas['data'])['member_id'])
        result = Handler.db_class.query(sql, one=True)
        money_before = Decimal(result['leave_amount'])
        logger.info("充值前账号金额:{}".format(money_before))

    resp = requests.request(method=datas['method'],
                            url=Handler.env_config["envurl"] + datas['path'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['data']))

    # 断言code是否正确
    try:
        assert resp.json()['code'] == json.loads(datas['expected'])['code']
    except AssertionError as e:
        logger.info("code不正确,{}测试失败{}".format(datas["title"],e))
        raise e

    # 接口返回值断言提现前后账户金额是否正确
    # try:
    #     if resp.json()['code'] == 0 and 'member_id' in datas['data']:
    #         assert json.loads(datas['data'])['amount'] - json.loads(datas['data'])['amount'] == resp.json()['data']['leave_amount']    # 账户提现前金额 - 提现金额= 账户提现后金额
    #         logger.info("提现前金额{} - 提现金额{} == 提现后金额{}".format(datas['extractor']['money'],datas['data']['amount'],resp.json()['data']['leave_amount']))
    # except AssertionError as err:
    #     logger.info("提现前后账户金额不正确,{}测试失败{}".format(datas["title"],err))
    #     raise err

    # 数据库查询断言提现前后账户金额是否正确
    if resp.json()['code'] == 0 and 'member_id' in datas['data']:
        sql = 'select leave_amount from member where id={}'.format(json.loads(datas['data'])['member_id'])
        result = Handler.db_class.query(sql, one=True)
        money_after = result['leave_amount']
        money = Decimal(json.loads(datas['data'])['amount'])
        assert money_before - money == money_after
        logger.info("提现前账号金额{},提现金额{},提现后账户总金额{}".format(money_before, money, money_after))

    # 设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            value = jsonpath(resp.json(), jsonpath_exp)[0]
            setattr(Handler, prop, value)

