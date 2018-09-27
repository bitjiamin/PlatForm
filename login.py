# -*- coding: UTF-8 -*-
"""
FileName: login.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 用户登陆
Update date：2017.7.20
version 1.0.0
"""
from PyQt5.QtWidgets import QDialog, QMessageBox, QDesktopWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import time
import base64
import log
import systempath
import inihelper
from PyQt5.uic import loadUi

class UserManager(QDialog):
    loginsignal = QtCore.pyqtSignal(list)
    loginok = False
    username = ''
    def __init__(self, parent=None):
        super(UserManager, self).__init__(parent)
        loadUi(systempath.bundle_dir + '/UI/login.ui', self)  # 看到没，瞪大眼睛看

        # 设置窗口图标
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.setWindowIcon(QtGui.QIcon(systempath.bundle_dir + '/Resource/user.ico'))

        self.cb_user.currentIndexChanged.connect(self.userchange)
        self.pb_login.clicked.connect(self.userlogin)
        self.pb_exit.clicked.connect(self.exit)
        self.screen = QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        #self.setFixedSize(self.width*0.6,self.height * 0.56)
        self.resize(self.width*0.3, self.height*0.28)
        self.le_pwd.setFocus()
        pixMap = QPixmap(systempath.bundle_dir + '/Resource/user.png')
        pixMap = pixMap.scaled(int(self.width*0.3*0.3), int(self.height*0.28*0.5), aspectRatioMode=Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        self.lb_image.setPixmap(pixMap)
        log.loginfo.init_log()
        self.le_pwd.setText('')
        self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
        self.change_language(self.lan)

    def exit(self):
        self.accept()

    def get_password(self):
        f = open(systempath.bundle_dir + '/Config/User.dat', 'r+')
        f.seek(0)
        pw = f.readline()
        # 解密
        pw = base64.decodestring(pw.encode()).decode()
        f.close()
        return pw

    def save_user(self, name, time):
        f = open(systempath.bundle_dir + '/Config/User.dat', 'r+')
        users = f.readlines()
        exist = False
        i = 0
        for user in users:
            if(user.split(',')[0] == name):
                users[i] = name+','+time + '\n'
                exist = True
            i = i + 1
        if(exist==False):
            users.append(name+','+time + '\n')
        f = open(systempath.bundle_dir + '/Config/User.dat', 'r+')
        f.writelines(users)
        f.close()

    def closeEvent(self, event):
        UserManager.loginok = False
        self.accept()

    def userchange(self):
        self.le_pwd.setText('')
        if(self.cb_user.currentIndex()==0):
            if(self.lan=='EN'):
                self.lb_pwd.setText('Password:')
            else:
                self.lb_pwd.setText('密码:')
            self.le_pwd.setEchoMode(2)
        else:
            if (self.lan == 'EN'):
                self.lb_pwd.setText('OperatorID:')
            else:
                self.lb_pwd.setText('操作员ID:')
            self.le_pwd.setEchoMode(0)

    def userlogin(self):
        try:
            login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            pwd = self.get_password()
            if((self.cb_user.currentIndex()==0) and (self.le_pwd.text() == pwd)):
                #log.loginfo.process_log('Administrator login')
                UserManager.username = 'Administrator'
                self.loginsignal.emit(['Administrator'])
                self.save_user('Administrator', login_time)
                UserManager.loginok = True
                self.accept()
            elif(self.cb_user.currentIndex() == 1):
                if(self.le_pwd.text() == ''):
                    QMessageBox.information(self, ("Warning!"), ("Invalid operator!"),
                                            QMessageBox.StandardButton(QMessageBox.Ok))
                else:
                    #log.loginfo.process_log('Operator ' + self.le_pwd.text() + ' login')
                    UserManager.username = self.le_pwd.text()
                    self.loginsignal.emit([self.le_pwd.text()])
                    self.save_user(UserManager.username, login_time)
                    UserManager.loginok = True
                    self.accept()
            else:
                # 除了information还有warning、about等
                QMessageBox.information(self, ("Warning!"), ("Password Error!"), QMessageBox.StandardButton(QMessageBox.Ok))
                #log.loginfo.process_log('wrong password')
        except Exception as e:
            log.loginfo.process_log('userlogin' + str(e))

    def English_ui(self):
        self.lb_login.setText('Login System')
        self.lb_user.setText('Username:')
        self.lb_pwd.setText('Password:')
        self.pb_login.setText('Login')
        self.pb_exit.setText('Exit')
        self.setWindowTitle('Login')

    def Chinese_ui(self):
        self.lb_login.setText('登录系统')
        self.lb_user.setText('用户名:')
        self.lb_pwd.setText('密码:')
        self.pb_login.setText('登录')
        self.pb_exit.setText('退出')
        self.setWindowTitle('登录')

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()