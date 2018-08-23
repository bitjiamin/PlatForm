# -*- coding: UTF-8 -*-
"""
FileName: zmqtool.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: zmq调试工具
Update date：2017.7.20
version 1.0.0
"""

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import systempath
import inihelper
import time


class ZmqTool(QDialog):
    def __init__(self, parent=None):
        super(ZmqTool, self).__init__(parent)
        loadUi(systempath.bundle_dir + '/UI/zmqtool.ui', self)  # 看到没，瞪大眼睛看
        self.setWindowTitle('Zmq Debug')
        self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
        self.change_language(self.lan)

    def display_recv_msg(self, msg):
        st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.te_zmqmsg.append(st + ': Server Recv -- ' + msg[0])

    def display_send_msg(self, msg):
        st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.te_zmqmsg.append(st + ': Server Send -- ' + msg[0])

    def English_ui(self):
        self.lb_zmqtitle.setText('ZMQ Debug Info')

    def Chinese_ui(self):
        self.lb_zmqtitle.setText('ZMQ调试信息')

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()