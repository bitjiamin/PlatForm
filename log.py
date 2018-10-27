# -*- coding: UTF-8 -*-
"""
FileName: log.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 加载CSV，初始化logger，写log
Update date：2017.7.20
version 1.0.0
"""

import logging
import time
from PyQt5 import QtCore
import systempath


global loginfo
class Log(QtCore.QObject):
    refreshlog = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self)
        global curpath, logger
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.LOG_FILE = systempath.bundle_dir + '/Log/' + date+'.log'
        # 创建一个handler，用于写入日志文件
        self.logger = logging.getLogger('mylogger')

    def init_log(self):
        # 创建一个handler，用于写入日志文件
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(self.LOG_FILE)
        self.fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        self.fh.setFormatter(formatter)
        self.ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    def process_log(self, msg):
        self.logger.debug(msg)
        st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.refreshlog.emit(st + ' - ' + msg)

    def process_err(self, msg):
        self.logger.debug(msg)
        st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.refreshlog.emit(st + ' - ' + msg)