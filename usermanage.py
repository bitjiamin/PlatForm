# -*- coding: UTF-8 -*-
"""
FileName: usermanage.py
Author: jiaminbit@sina.com
Create date: 2017.8.31
description: 用户管理
Update date：2017.8.31
version 1.0.0
"""

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import systempath
import base64
import log
import inihelper


class UserManage(QDialog):
    def __init__(self, parent=None):
        super(UserManage, self).__init__(parent)
        loadUi(systempath.bundle_dir + '/UI/usermanage.ui', self)  # 看到没，瞪大眼睛看


        # 设置窗口图标
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.setWindowIcon(QtGui.QIcon(systempath.bundle_dir + '/Resource/user.ico'))

        self.pb_savepw.clicked.connect(self.change_password)
        self.pb_deluser.clicked.connect(self.delete_user)
        self.init_ui()
        self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
        self.change_language(self.lan)

    def change_password(self):
        old_pw = self.get_password()
        if(self.le_old.text()!=old_pw):
            QMessageBox.information(self, ("Warning!"), ("Old Password Error!"), QMessageBox.StandardButton(QMessageBox.Ok))
        else:
            pw = self.le_new.text()
            if(pw==''):
                QMessageBox.information(self, ("Warning!"), ("Invalid New Password!"),
                                        QMessageBox.StandardButton(QMessageBox.Ok))

            else:
                # 加密密码
                pw_bin = base64.encodestring(pw.encode()).decode()
                # r+覆盖写
                f = open(systempath.bundle_dir + '/Config/User.dat', 'r+')
                # 覆盖第一行内容
                f.seek(0)
                f.write(pw_bin)
                f.close()
                log.loginfo.process_log('change password ok')
                QMessageBox.information(self, ("Warning!"), ("Change Password Success!"),
                                        QMessageBox.StandardButton(QMessageBox.Ok))

    def get_password(self):
        f = open(systempath.bundle_dir + '/Config/User.dat', 'r+')
        f.seek(0)
        pw = f.readline()
        # 解密
        pw = base64.decodestring(pw.encode()).decode()
        f.close()
        return pw

    def init_ui(self):
        self.le_old.setEchoMode(2)
        self.le_new.setEchoMode(2)
        self.le_old.setFocus()
        self.tw_user.horizontalHeader().setStretchLastSection(True)
        self.tw_user.setColumnCount(3)
        self.tw_user.setRowCount(50)

    def get_users(self):
        f = open(systempath.bundle_dir + '/Config/User.dat', 'r+')
        data = f.readlines()
        f.close()
        self.users = []
        i = 0
        for user in data:
            if(i!=0):
                newItem = QTableWidgetItem(user.split(',')[0])
                self.tw_user.setItem(i-1, 0, newItem)
                if(user.split(',')[0] == 'Administrator'):
                    newItem = QTableWidgetItem('Administrator')
                    self.tw_user.setItem(i-1, 1, newItem)
                else:
                    newItem = QTableWidgetItem('Operator')
                    self.tw_user.setItem(i-1, 1, newItem)
                newItem = QTableWidgetItem(user.split(',')[1])
                self.tw_user.setItem(i-1, 2, newItem)
            i=i+1

    def delete_user(self):
        f = open(systempath.bundle_dir + '/Config/User.dat', 'r')
        data = f.readlines()
        f.close()
        i = self.tw_user.currentRow()
        if(i==-1):
            QMessageBox.information(self, ("Warning!"), ("Choose a user!"), QMessageBox.StandardButton(QMessageBox.Ok))
        elif(i==0):
            QMessageBox.information(self, ("Warning!"), ("Can't remove Admin!"), QMessageBox.StandardButton(QMessageBox.Ok))
        else:
            self.tw_user.removeRow(i)
            del_user = data[i+1].split(',')[0]
            data = data[0:i+1] + data[i+2:]
            f = open(systempath.bundle_dir + '/Config/User.dat', 'w')
            f.writelines(data)
            f.close()
            log.loginfo.process_log('delete user: ' + del_user)

    def English_ui(self):
        self.lb_usertitle.setText('User Management')
        self.lb_old.setText('Old Password:')
        self.lb_new.setText('New Password:')
        self.pb_savepw.setText('Save Password')
        self.pb_deluser.setText('Delete')
        self.setWindowTitle('User Management')
        self.tw_user.setHorizontalHeaderLabels(['User', 'Authority', 'Latest login'])

    def Chinese_ui(self):
        self.lb_usertitle.setText('用户管理')
        self.lb_old.setText('旧密码:')
        self.lb_new.setText('新密码:')
        self.pb_savepw.setText('保存密码')
        self.pb_deluser.setText('删除')
        self.setWindowTitle('用户管理')
        self.tw_user.setHorizontalHeaderLabels(['用户', '权限', '最近登录时间'])

    def change_language(self, lan):
        if (lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()