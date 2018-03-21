# -*- coding: UTF-8 -*-
"""
FileName: login.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 用户登陆
Update date：2017.7.20
version 1.0.0
"""
import systempath
from PyQt5.QtWidgets import QDialog, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QPixmap
from loginwindow import *
import time
import base64
import log

class UserManager(Ui_login,QDialog):
    loginsignal = QtCore.pyqtSignal(list)
    loginok = False
    username = ''
    def __init__(self, parent=None):
        super(UserManager, self).__init__(parent)
        self.setupUi(self)
        self.cb_user.currentIndexChanged.connect(self.userchange)
        self.pb_login.clicked.connect(self.userlogin)
        self.pb_exit.clicked.connect(self.exit)
        self.screen = QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        self.setFixedSize(self.width*0.3,self.height * 0.28)
        self.lb_login.setMaximumHeight(self.height * 0.16)
        self.lb_login.setMaximumWidth(self.width * 0.3)
        self.lb_image.setMaximumHeight(self.height * 0.08)
        self.lb_layout.setMaximumHeight(self.height * 0.03)
        self.lb_image.setMaximumWidth(self.width * 0.06)
        self.pb_login.setMaximumWidth(self.width * 0.1)
        self.pb_exit.setMaximumWidth(self.width * 0.1)
        self.le_pwd.setFocus()
        pixMap = QPixmap(systempath.bundle_dir + '/Resource/user.png')
        self.lb_image.setPixmap(pixMap)
        log.loginfo.init_log()
        self.le_pwd.setText('')

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
            self.lb_pwd.setText('PassWord:')
            self.le_pwd.setEchoMode(2)
        else:
            self.lb_pwd.setText('OperatorID:')
            self.le_pwd.setEchoMode(0)

    def userlogin(self):
        login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        pwd = self.get_password()
        if((self.cb_user.currentIndex()==0) and (self.le_pwd.text() == pwd)):
            log.loginfo.process_log('Administrator login')
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
                log.loginfo.process_log('Operator ' + self.le_pwd.text() + ' login')
                UserManager.username = self.le_pwd.text()
                self.loginsignal.emit([self.le_pwd.text()])
                self.save_user(UserManager.username, login_time)
                UserManager.loginok = True
                self.accept()
        else:
            # 除了information还有warning、about等
            QMessageBox.information(self, ("Warning!"), ("Password Error!"), QMessageBox.StandardButton(QMessageBox.Ok))
            log.loginfo.process_log('error password')