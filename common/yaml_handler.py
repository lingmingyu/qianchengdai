# -*- coding: utf-8 -*-
# @Time     : 2021/1/18 21:36
# @Author   : qtf
# File      : yaml_handler.py
import yaml

def read_yaml(fpath):
    with open(fpath, encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data
