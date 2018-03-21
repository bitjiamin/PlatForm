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

    def connect_camera(self):
        self.baumer = Class1()
        self.baumer.init_window(int(self.visionui.lb_image.winId()), 0, 0, self.visionui.lb_image.width(),
                                self.visionui.lb_image.height())
        ret = self.baumer.Initialize()
        if(ret==True):
            print('connect ok')
        return ret

    def get_extime(self):
        ret = self.baumer.get_extime()
        print(ret)

    def set_extime(self, extime):
        ret = self.baumer.set_extime(extime)
        print(ret)

    def toQImage(self, im, copy=False):
        gray_color_table = [qRgb(i, i, i) for i in range(256)]
        if im is None:
            return QImage()
        if len(im.shape) == 2:
            qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Grayscale8)
            qim.setColorTable(gray_color_table)
            return qim.copy() if copy else qim
        elif len(im.shape) == 3:
            if im.shape[2] == 3:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                return qim.copy() if copy else qim
            elif im.shape[2] == 4:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                return qim.copy() if copy else qim

    def disp_image(self, qImage):
        self.visionui.lb_image.setPixmap(qImage)

    def capture(self):
        #cv2.imwrite('1.png', grayImage)
        try:
            print(time.time())
            ret = self.baumer.snap(5000)
            print(time.time())
            #print(time.time())
            #data = list(self.baumer.databuffer)
            #grayImage = np.array(data, dtype=np.uint8).reshape(1944, 2592)
            #print(time.time())
            #self.img = cv2.imread('1.png', 0)
            #qimg = QPixmap(self.toQImage(grayImage))
            #qimg.scaled(self.visionui.lb_image.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.baumer.disp_image()
            print(time.time())
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
            ret = self.baumer.snap(5000)
            self.baumer.disp_image()
            if(self.stop):
                break