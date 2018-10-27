# -*- coding: UTF-8 -*-
"""
FileName: visionscript.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 视觉脚本
Update date：2017.7.20
version 1.0.0
"""


import time
import threading
import systempath
import sys
import mainsetup
import clr
clr.FindAssembly(systempath.bundle_dir +  '/Vision/BaumerSDKV2.dll')  # 加载c#dll文件
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
            self.baumer = BaumerSDKV2()
            # ret = self.baumer.init_system()
            # self.baumer.open_camera('0680113115')
            self.mainui = mainsetup.MainUI()
            # 初始化图像窗口，并在界面加载完成后调整halcon窗口为label大小
            self.win = self.init_image_window(self.mainui.lb_image1)
            self.win_thread = threading.Thread(target=self.resize_win)
            self.win_thread.setDaemon(True)
            self.win_thread.start()
            # 连接右键事件
            self.mainui.actsnap1.triggered.connect(self.read_image)
            self.__class__.__first_init = False  # 只初始化一次

    def resize_win(self):
        # 界面加载完成后重新调整halcon图像窗体大小
        time.sleep(2)
        self.baumer.set_winsize(self.win, self.mainui.lb_image1.width(), self.mainui.lb_image1.height())

    def read_image(self):
        try:
            self.baumer.read_image('C:\\Project\\Image\\3-1.jpg')
            self.baumer.disp_imageH(self.win)
            # self.baumer.get_roi(self.win)
        except Exception as e:
            print(e)

    def init_image_window(self, image_win):
        ret = self.baumer.init_window(int(image_win.winId()))
        return ret

    def connect_camera(self):
        ret = True
        return ret

    def get_extime(self):
        ret = self.baumer.get_extime()
        return ret

    def set_extime(self, extime):
        ret = self.baumer.set_extime(extime)
        return float(ret)

    def capture(self):
        try:
            print('capture1')
        except Exception as e:
            print(e)

    def live(self):
        print('live1')
        pass

    def live_image(self):
        while (True):
            ret = self.baumer.snap()
            self.baumer.disp_image()
            if(self.stop):
                break