# -*- coding: UTF-8 -*-
"""
FileName: inihelper.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 读写ini文件
Update date：2017.7.20
version 1.0.0
"""

import configparser


def read_ini(filename, section, key):
    cf = configparser.ConfigParser()
    cf.read(filename)
    value = cf.get(section, key)
    return value

def write_ini(filename, section, key, value):
    cf = configparser.ConfigParser()
    cf.read(filename)
    cf.set(section, key, value)
    # write to file
    cf.write(open(filename, "w"))
