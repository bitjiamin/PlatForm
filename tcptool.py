# -*- coding: UTF-8 -*-
"""
FileName: tcptool.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: tcp调试工具
Update date：2017.7.20
version 1.0.0
"""

from PyQt5.QtWidgets import QDialog, QDesktopWidget
from PyQt5 import QtGui
import socket
import threading
import time
import log
import systempath
import inihelper
from PyQt5.uic import loadUi


socket.setdefaulttimeout(0.5)
class TcpTool(QDialog):
    def __init__(self, parent=None):
        super(TcpTool, self).__init__(parent)
        loadUi(systempath.bundle_dir + '/UI/tcptool.ui', self)  # 看到没，瞪大眼睛看

        # 设置窗口图标
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.setWindowIcon(QtGui.QIcon(systempath.bundle_dir + '/Resource/tcp.ico'))

        self.screen = QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        self.resize(self.width * 0.5, self.height * 0.5)
        self.lb_tcptitle.setMaximumHeight(self.height * 0.05)
        self.pb_tcpconnect.clicked.connect(self.tcp_connect)
        self.setWindowTitle('Tcp Debug')
        self.pb_send.clicked.connect(self.tcp_send)
        self.le_ip.setText('127.0.0.1:5000')
        self.ip = ''
        self.port = 0
        self.pb_send.setEnabled(False)
        self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
        self.change_language(self.lan)

    def tcp_connect(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(self.pb_tcpconnect.text() == 'Connect' or self.pb_tcpconnect.text() == '连接'):
            try:
                s_list = self.le_ip.text().split(':')
                self.ip = s_list[0]
                self.port = int(s_list[1])
                con_ok = self.skt.connect((self.ip, self.port))
                if(con_ok == None):
                    log.loginfo.process_log('tcp connect ok')
                    if(self.lan == 'EN'):
                        self.pb_tcpconnect.setText('Close')
                    else:
                        self.pb_tcpconnect.setText('关闭')
                    self.recving = True
                    self.recv_thread = threading.Thread(target=self.tcp_recv)
                    self.recv_thread.setDaemon(True)
                    self.recv_thread.start()
                    self.pb_send.setEnabled(True)
            except Exception as e:
                log.loginfo.process_log(str(e))
                self.pb_send.setEnabled(False)
        else:
            self.recving = False
            self.skt.close()
            if (self.lan == 'EN'):
                self.pb_tcpconnect.setText('Connect')
            else:
                self.pb_tcpconnect.setText('连接')
            self.pb_send.setEnabled(False)

    def tcp_send(self):
        try:
            sendmsg = self.te_sendmsg.toPlainText()
            self.skt.send(sendmsg.encode())
        except Exception as e:
            log.loginfo.process_log(str(e))

    def display_recv(self, msg):
        self.te_recvmsg.append(msg)

    def tcp_recv(self):
        while self.recving:
            try:
                recvmsg = self.skt.recv(1024)
                self.te_recvmsg.append(recvmsg.decode())
            except Exception as e:
                log.loginfo.process_log(str(e))
            time.sleep(0.01)

    # def closeEvent(self, event):
    #     try:
    #         self.recving = False
    #         self.pb_tcpconnect.setText('Connect')
    #         self.pb_send.setEnabled(False)
    #         self.skt.close()
    #         log.loginfo.process_log('tcp close ok')
    #     except Exception as e:
    #         log.loginfo.process_log(str(e))

    def English_ui(self):
        self.lb_tcptitle.setText('TCP Debug Tool')
        self.pb_tcpconnect.setText('Connect')
        self.pb_send.setText('Send')
        self.setWindowTitle('TCP Debug')

    def Chinese_ui(self):
        self.lb_tcptitle.setText('TCP调试工具')
        self.pb_tcpconnect.setText('连接')
        self.pb_send.setText('发送')
        self.setWindowTitle('TCP调试')

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()