# -*- coding: utf-8 -*-
"""
FileName: motioncthread.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 运动控制相关操作
Update date：2017.7.20
version 1.0.0
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import log
import inihelper
import systempath


class AutoUI(QDialog, QtCore.QThread):
    showsingnal = QtCore.pyqtSignal(bool)
    closesingnal = QtCore.pyqtSignal(bool)
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
            super(AutoUI, self).__init__(parent)
            loadUi(systempath.bundle_dir + '/UI/automation.ui', self)  # 看到没，瞪大眼睛看
            # 获取屏幕分辨率
            self.screen = QDesktopWidget().screenGeometry()
            self.width = self.screen.width()
            self.height = self.screen.height()
            self.lb_axis.setMaximumHeight(self.height*0.1)
            self.lb_title.setMaximumHeight(self.height*0.1)
            self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
            self.change_language(self.lan)

    def showEvent(self, QShowEvent):
        self.showsingnal.emit(True)

    def closeEvent(self, QCloseEvent):
        self.closesingnal.emit(True)

    def English_ui(self):
        # 序列编辑
        self.tw_io.setHorizontalHeaderLabels(['IO', 'Description'])
        self.lb_title.setText('Automation')
        self.lb_axis.setText('Axis Name')
        self.lb_real_pos.setText('Current Position')
        self.lb_man_speed.setText('Manual Speed')
        self.lb_step.setText('Distance')
        self.pb_jog1.setText('Jog+')
        self.pb_jog2.setText('Jog-')
        self.pb_absolute.setText('Absolute')
        self.pb_relative.setText('Relative')
        self.pb_reset.setText('Reset')
        self.pb_axis_stop.setText('Stop')
        self.cb_zero.setText('Zero')
        self.cb_limitm.setText('Limit-')
        self.cb_limitp.setText('Limit+')

    def Chinese_ui(self):
        # 序列编辑
        self.tw_io.setHorizontalHeaderLabels(['IO', '描述'])
        self.lb_title.setText('运动控制')
        self.lb_axis.setText('轴名字')
        self.lb_real_pos.setText('当前位置')
        self.lb_man_speed.setText('手动速度')
        self.lb_step.setText('步长')
        self.pb_jog1.setText('Jog+')
        self.pb_jog2.setText('Jog-')
        self.pb_absolute.setText('绝对')
        self.pb_relative.setText('相对')
        self.pb_reset.setText('复位')
        self.pb_axis_stop.setText('停止')
        self.cb_zero.setText('原点')
        self.cb_limitm.setText('负极限')
        self.cb_limitp.setText('正极限')

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()