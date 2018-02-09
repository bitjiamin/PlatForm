# -*- coding: UTF-8 -*-
"""
FileName: zmqtool.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: zmq调试工具
Update date：2017.7.20
version 1.0.0
"""

from PyQt5.QtWidgets import QDialog, QMessageBox
from zmqwindow import *
import time

class ZmqTool(Ui_zmqtool, QDialog):
    def __init__(self, parent=None):
        super(ZmqTool, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Zmq Debug')

    def display_recv_msg(self, msg):
        st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.te_zmqmsg.append(st + ': Server Recv -- ' + msg[0])

    def display_send_msg(self, msg):
        st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.te_zmqmsg.append(st + ': Server Send -- ' + msg[0])