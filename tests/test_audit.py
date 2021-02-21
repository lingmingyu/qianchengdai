# -*- coding: utf-8 -*-
# @Time     : 2021/2/4 20:51
# @Author   : qtf
# File      : test_audit.py
import pytest,requests,json
from jsonpath import jsonpath
from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('Audit')

@pytest.mark.parametrize('datas', excel_datas)
def test_audit(datas, admin_login, add_loan):
    """审核接口"""
    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    resp = requests.request(method=datas['method'],
                            url=Handler.env_config["envurl"] + datas['path'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['data']))
    logger.info("resp:{}".format(resp.json()))
    expected = json.loads(datas['expected'])

    # 第一版多值断言
    # assert resp.json()['code'] == expected["code"]
    # assert resp.json()['msg'] == expected['msg']

    # 第二版多值断言
    # for key, value in expected.items():
    #     # ("code", 0)
    #     # ("msg", "OK")
    #     # try:
    #     assert resp.json()[key] == value

    # 第三版多值断言
    for key, value in expected.items():
        # 实际结果的value 怎么获取
        assert jsonpath(resp.json(), key)[0] == value

# 设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            value = jsonpath(resp.json(), jsonpath_exp)[0]
            setattr(Handler, prop, value)
