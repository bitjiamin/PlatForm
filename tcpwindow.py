# -*- coding: UTF-8 -*-
"""
FileName: tcpwindow.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: tcp调试工具UI
Update date：2017.7.20
version 1.0.0
"""

# Form implementation generated from reading ui file '/Users/jiamin/Desktop/Develop/Python/Program/TestUI/tcptool.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tcptool(object):
    def setupUi(self, tcptool):
        tcptool.setObjectName("tcptool")
        tcptool.resize(564, 377)
        self.gridLayout = QtWidgets.QGridLayout(tcptool)
        self.gridLayout.setObjectName("gridLayout")
        self.le_ip = QtWidgets.QLineEdit(tcptool)
        self.le_ip.setObjectName("le_ip")
        self.gridLayout.addWidget(self.le_ip, 1, 0, 1, 1)
        self.pb_tcpconnect = QtWidgets.QPushButton(tcptool)
        self.pb_tcpconnect.setObjectName("pb_tcpconnect")
        self.gridLayout.addWidget(self.pb_tcpconnect, 1, 1, 1, 1)
        self.te_sendmsg = QtWidgets.QTextEdit(tcptool)
        self.te_sendmsg.setObjectName("te_sendmsg")
        self.gridLayout.addWidget(self.te_sendmsg, 2, 0, 1, 1)
        self.pb_send = QtWidgets.QPushButton(tcptool)
        self.pb_send.setObjectName("pb_send")
        self.gridLayout.addWidget(self.pb_send, 2, 1, 1, 1)
        self.te_recvmsg = QtWidgets.QTextEdit(tcptool)
        self.te_recvmsg.setObjectName("te_recvmsg")
        self.gridLayout.addWidget(self.te_recvmsg, 3, 0, 1, 1)
        self.lb_tcptitle = QtWidgets.QLabel(tcptool)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lb_tcptitle.setFont(font)
        self.lb_tcptitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_tcptitle.setObjectName("lb_tcptitle")
        self.gridLayout.addWidget(self.lb_tcptitle, 0, 0, 1, 2)

        self.retranslateUi(tcptool)
        QtCore.QMetaObject.connectSlotsByName(tcptool)

    def retranslateUi(self, tcptool):
        _translate = QtCore.QCoreApplication.translate
        tcptool.setWindowTitle(_translate("tcptool", "Dialog"))
        self.pb_tcpconnect.setText(_translate("tcptool", "Connect"))
        self.pb_send.setText(_translate("tcptool", "Send"))
        self.lb_tcptitle.setText(_translate("tcptool", "TCP Debug Tool"))

