# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import systempath


global visionui
class VisionUI(QDialog):
    # 实现一个单例类
    _instance = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent=None):
        if (self.__class__.__first_init):  # 只初始化一次
            self.__class__.__first_init = False  # 只初始化一次
            super(VisionUI, self).__init__(parent)
            loadUi(systempath.bundle_dir + '/Vision/vision.ui', self)  # 看到没, 瞪大眼睛看
            self.lb_image.setScaledContents(True)
            self.lb_image.setMaximumWidth(self.width() * 0.75)
            self.lb_image.setMaximumHeight(self.height() * 0.75)