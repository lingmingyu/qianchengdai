# -*- coding: utf-8 -*-
# @Time     : 2021/1/18 19:58
# @Author   : qtf
# File      : test_registers.py
import os,pytest,json
from common.logger_handler import logger
from common.request_handler import send_requests
from middleware.handler import Handler

excel_datas = Handler.excel.read("Register")

@pytest.mark.parametrize('datas',excel_datas)
def test_registers(datas):
    resp = send_requests(datas)
    exp = json.loads(datas["expected"])["msg"]
    try:
        assert exp == resp["msg"]
    except Exception as err:
        logger.error("{}测试失败{}".format(datas["case_name"],err))
        # 一定要记得抛出
        raise err

