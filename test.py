# -*- coding: UTF-8 -*-
"""
FileName: tcpserver.py
Author: jiaminbit@sina.com
Create date: 2018.5.6
description: 测试脚本，将各测试项的函数定义在该文件中
Update date：2018.5.6
version 1.0.0
"""

import clr
import sys
import System
import os
import time
import threading


def live_image():
    while(True):
        time.sleep(1)
        print('run')


live = threading.Thread(target=live_image)
live.setDaemon(True)
live.start()

time.sleep(5)
os.system('pause')