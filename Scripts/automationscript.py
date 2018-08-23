# -*- coding: UTF-8 -*-
"""
FileName: automationscript.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 自动化脚本，将运动控制相关函数定义在改文件
Update date：2017.7.20
version 1.0.0
"""

import random
import socket
import struct
import time
import systempath
import csv
import os
import threading
import autosetup
import log


l = threading.Lock()
socket.setdefaulttimeout(0.5)
class AutoMation():
    # 实现一个单例类
    _instance = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent=None):
        if (self.__class__.__first_init):  # 只初始化一次
            self.currentaxis = 0
            self.__class__.__first_init = False  # 只初始化一次

    def get_rt_info(self):    # 框架固有函数，可自定义，勿删除
        time.sleep(0.1)
        rt_info = [0,0]
        return rt_info

    def create_connect(self):     #输入参数为本机IP，字符串
        return True

    def close_connect(self):
        return True

    def choose_axis(self, axis_index):   # 框架固有函数，可自定义，勿删除
        self.currentaxis = axis_index

    def choose_io_table(self, axis_index):
        path = systempath.bundle_dir + '/CSV Files/' + 'IO' + str(axis_index+1) + '.csv'
        return path

    def mannual_mode(self, mode):       # 框架固有函数，可自定义，勿删除
        if(mode):
            log.loginfo.process_log('start mannual mode')
        else:
            log.loginfo.process_log('start auto mode')

    def jog_forward(self):     # 框架固有函数，可自定义，勿删除
        print('forward')
        return True

    def jog_forward_stop(self):    # 框架固有函数，可自定义，勿删除
        print('forward stop')
        return True

    def jog_backward(self):    # 框架固有函数，可自定义，勿删除
        print('backward')
        return True

    def jog_backward_stop(self):    # 框架固有函数，可自定义，勿删除
        print('backward stop')
        return True

    def absolute_run(self, value):    # 框架固有函数，可自定义，勿删除
        print('absolute')
        return True

    def relative_run(self, value):    # 框架固有函数，可自定义，勿删除
        print('relative')
        return True

    def axis_home(self):    # 框架固有函数，可自定义，勿删除
        print(self.axisindex[self.currentaxis][1])
        print('home')
        return True

    def axis_reset(self):     # 框架固有函数，可自定义，勿删除
        print('reset')
        return True

    def axis_stop(self):    # 框架固有函数，可自定义，勿删除
        print('stop')
        return True

    def read_io(self, index, length):  # index格式两位小数的字符串，length为整数   # 框架固有函数，可自定义，勿删除
        time.sleep(0.1)
        data = [-1]*length
        return data

    def write_io(self,index,value):    # index格式两位小数的浮点数，index为字符串，value为list    # 框架固有函数，可自定义，勿删除
        return True

    def read_para(self, index, length):  # index为D寄存器开始位置, length为数据个数    # 框架固有函数，可自定义，勿删除
        time.sleep(0.1)
        length = length*2   # 所有数据均为双子，所以长度乘以2
        data = [0] * int(length/2)
        return data

    def write_para(self, index, value):  # index为D寄存器开始位置, value为写入的数值，每个数值占用两个D寄存器，两位小数   # 框架固有函数，可自定义，勿删除
        return True