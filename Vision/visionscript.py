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
sys.path.append(systempath.bundle_dir + '/Vision')
clr.FindAssembly(systempath.bundle_dir + '/Vision/BaumerDll.dll')  # 加载c#dll文件
from BaumerDll import *


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
            self.__class__.__first_init = False  # 只初始化一次

    def init_image_window(self, image_win):
        self.baumer.init_windowH(int(image_win.winId()), 0, 0, image_win.width(),
                                 image_win.height())

    def connect_camera(self):
        self.baumer = BaumerH()
        ret = self.baumer.open_cameraH()
        if(ret==True):
            print('connect ok')
        return ret

    def get_extime(self):
        ret = self.baumer.get_extimeH()
        return ret

    def set_extime(self, extime):
        ret = self.baumer.set_extimeH(extime)
        return float(ret)

    def get_model(self):
        ret = self.baumer.get_device_modelH()
        return str(ret)

    def capture(self):
        try:
            ret = self.baumer.snapH()
            self.baumer.disp_imageH()
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
            ret = self.baumer.snapH()
            self.baumer.disp_imageH()
            if(self.stop):
                break