# -*- coding: utf-8 -*-
# @Time     : 2021/1/18 21:37
# @Author   : qtf
# File      : request_handler.py
import requests
from common.logger_handler import logger
from middleware.handler import Handler

def send_requests(datas):
    method = datas["method"]
    url = Handler.env_config["envurl"] + datas["path"]
    headers = datas["headers"]     # 将字符串转换为字典
    data = datas["body"]
    if '#new_phone#' in data:
        phone = Handler.generate_new_phone()
        data = data.replace('#new_phone#',phone)

    logger.info(data)
    resp = {}     # 接收返回数据
    res = ""
    try:
        res = requests.request(method, url, headers=eval(headers), json=eval(data),verify=False)
        resp = res.json()
        resp["StatusCode"] = str(res.status_code)     # 状态码转成str
        resp["time"] = str(res.elapsed.total_seconds())     # 接口请求时间转str
        if resp["StatusCode"] != "200":
            resp["error"] = resp["text"]
            resp["return_code"] = str(res.status_code)
        else:
            resp["error"] = ""
    except Exception as msg:
        resp["msg"] = str(msg)
        resp["text"] = res.content.decode("utf-8")     # 打印错误返回信息以文本形式输出
        resp["return_code"] = "error"
    resp["rowNum"] = datas["rowNum"]
    logger.info("resp{}".format(resp))
    return resp
