# -*- coding: utf-8 -*-
# @Time     : 2021/1/27 22:17
# @Author   : qtf
# File      : test_login.py
import requests,pytest,json
from jsonpath import jsonpath

from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('Login')

@pytest.mark.parametrize('datas', excel_datas)
def test_login(datas):

    if '#new_phone#' in datas["data"]:
        phone = Handler.generate_new_phone()
        datas["data"] = datas["data"].replace('#new_phone#',phone)

    if '*phone*' in datas['data']:
        new_phone = Handler.generate_new_phone()
        datas['data'] = datas['data'].replace('*phone*', new_phone)

    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    resp = requests.request(method=datas['method'],
                            url=Handler.env_config["envurl"] + datas['path'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['data']))
    try:
        assert resp.json()['msg'] == datas['expected']
    except AssertionError as e:
        logger.info("msg不正确,{}测试失败{}".format(datas["title"],e))
        raise e

# 设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            # value = 'token'
            value = jsonpath(resp.json(), jsonpath_exp)[0]
            # setastr(Handler, "loan_token", "yfowepfpwefwoefowf"
            setattr(Handler, prop, value)