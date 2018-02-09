# -*- coding: UTF-8 -*-
"""
FileName: zmqwindow.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: zmq调试UI
Update date：2017.7.20
version 1.0.0
"""

# Form implementation generated from reading ui file '/Users/jiamin/Desktop/Develop/Python/Program/TestUI/zmqtool.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_zmqtool(object):
    def setupUi(self, zmqtool):
        zmqtool.setObjectName("zmqtool")
        zmqtool.setWindowModality(QtCore.Qt.WindowModal)
        zmqtool.resize(491, 357)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(zmqtool.sizePolicy().hasHeightForWidth())
        zmqtool.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(zmqtool)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lb_zmqtitle = QtWidgets.QLabel(zmqtool)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_zmqtitle.sizePolicy().hasHeightForWidth())
        self.lb_zmqtitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lb_zmqtitle.setFont(font)
        self.lb_zmqtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_zmqtitle.setObjectName("lb_zmqtitle")
        self.gridLayout.addWidget(self.lb_zmqtitle, 0, 0, 1, 1)
        self.te_zmqmsg = QtWidgets.QTextEdit(zmqtool)
        self.te_zmqmsg.setObjectName("te_zmqmsg")
        self.gridLayout.addWidget(self.te_zmqmsg, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(zmqtool)
        QtCore.QMetaObject.connectSlotsByName(zmqtool)

    def retranslateUi(self, zmqtool):
        _translate = QtCore.QCoreApplication.translate
        zmqtool.setWindowTitle(_translate("zmqtool", "ZMQ DEBUG"))
        self.lb_zmqtitle.setText(_translate("zmqtool", "<html><head/><body><p>ZMQ Debug Info</p></body></html>"))

