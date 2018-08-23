# -*- coding: UTF-8 -*-
"""
FileName: visionscript.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 视觉脚本
Update date：2017.7.20
version 1.0.0
"""

import clr
import time
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import systempath
import visionsetup
import sys
import mainsetup
clr.FindAssembly('BaumerSDKV2.dll')  # 加载c#dll文件
from BaumerSDKV2 import *


class Vision():
    # 实现一个单例类
    _instance = None
    __first_init = True
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent=None):
        if (self.__class__.__first_init):  # 只初始化一次
            self.visionui = visionsetup.VisionUI()
            self.visionui.pb_live.setText('Live')
            self.baumer = BaumerSDKV2()
            self.mainui = mainsetup.MainUI()
            self.mainui.actsnap.triggered.connect(self.read_image)
            self.__class__.__first_init = False  # 只初始化一次

    def read_image(self):
        try:
            win = self.init_image_window(self.mainui.lb_image)
            self.baumer.read_image('C:\\Project\\Image\\123.bmp')
            self.baumer.disp_image(win)
        except Exception as e:
            print(e)

    def init_image_window(self, image_win):
        ret = self.baumer.init_window(int(image_win.winId()), 0, 0, image_win.width(),
                                 image_win.height())
        return ret

    def connect_camera(self):
        ret = self.baumer.Initialize()
        if(ret==True):
            print('connect ok')
        self.cam = list(self.baumer.init_camera())
        print(self.cam)
        return ret

    def get_extime(self):
        ret = self.baumer.get_extime()
        return ret

    def set_extime(self, extime):
        ret = self.baumer.set_extime(extime)
        return float(ret)

    def capture(self):
        try:
            self.baumer.set_camera('0680113115')
            ret = self.baumer.snap()
            self.baumer.disp_image()
        except Exception as e:
            print(e)

    def live(self):
        if(self.visionui.pb_live.text() == 'Live'):
            self.stop = False
            self.visionui.pb_live.setText('Stop')
            live = threading.Thread(target=self.live_image)
            live.setDaemon(True)
            live.start()
        else:
            self.visionui.pb_live.setText('Live')
            self.stop = True

    def live_image(self):
        while (True):
            ret = self.baumer.snap()
            self.baumer.disp_image()
            if(self.stop):
                break