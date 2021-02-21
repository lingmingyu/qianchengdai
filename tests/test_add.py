# -*- coding: utf-8 -*-
# @Time     : 2021/2/3 22:10
# @Author   : qtf
# File      : test_add.py
import requests,pytest,json
from jsonpath import jsonpath
from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('Add')

@pytest.mark.parametrize('datas', excel_datas)
def test_withdraw(datas):
    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    resp = requests.request(method=datas['method'],
                            url=Handler.env_config["envurl"] + datas['path'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['data']))

    # 断言code是否正确
    try:
        assert resp.json()['code'] == datas['expected']
    except AssertionError as e:
        logger.info("code不正确,{}测试失败{}".format(datas["title"],e))
        raise e

    # 设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            value = jsonpath(resp.json(), jsonpath_exp)[0]
            setattr(Handler, prop, value)

