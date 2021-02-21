# -*- coding: utf-8 -*-
# @Time     : 2021/2/6 9:53
# @Author   : qtf
# File      : test_invest.py
import pytest,requests,json
from jsonpath import jsonpath

from middleware.handler import Handler

data = Handler.excel.read('Invest')

@pytest.mark.parametrize('datas', data)
def test_audit(datas):
    # 要保证替换成功，excel当中的 #investor_phone# 必须和属性名保持一致。
    # datas转化成json字符串
    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    resp = requests.request(url=Handler.env_config["envurl"] + datas['path'],
                            method=datas['method'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['data']))
    assert resp.json()['code'] == datas['expected']

    # 设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            # value = 'token'
            value = jsonpath(resp.json(), jsonpath_exp)[0]
            # setastr(Handler, "loan_token", "yfowepfpwefwoefowf"
            setattr(Handler, prop, value)
