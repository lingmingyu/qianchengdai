# -*- coding: utf-8 -*-
# @Time     : 2021/1/18 21:20
# @Author   : qtf
# File      : run.py
"""
项目入口，主程序
收集用例，运行用例，生成报告
"""
import os,pytest
from datetime import datetime
from config.path import reports_path

# pytest 收集用例
def run_case():
    timestamp = str(datetime.now().strftime("%Y-%m-%d %H_%M_%S"))
    reportfilename = 'report%s.html' % timestamp
    htmlreport = os.path.join(reports_path,reportfilename)
    pytest.main(['--html={}'.format(htmlreport)])

run_case()
