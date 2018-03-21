# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scansn.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SN(object):
    def setupUi(self, SN):
        SN.setObjectName("SN")
        SN.resize(874, 228)
        self.gridLayout = QtWidgets.QGridLayout(SN)
        self.gridLayout.setObjectName("gridLayout")
        self.lb_sn = QtWidgets.QLabel(SN)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_sn.sizePolicy().hasHeightForWidth())
        self.lb_sn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lb_sn.setFont(font)
        self.lb_sn.setObjectName("lb_sn")
        self.gridLayout.addWidget(self.lb_sn, 0, 0, 1, 1)
        self.le_sn = QtWidgets.QLineEdit(SN)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.le_sn.setFont(font)
        self.le_sn.setObjectName("le_sn")
        self.gridLayout.addWidget(self.le_sn, 0, 1, 1, 1)

        self.retranslateUi(SN)
        QtCore.QMetaObject.connectSlotsByName(SN)

    def retranslateUi(self, SN):
        _translate = QtCore.QCoreApplication.translate
        SN.setWindowTitle(_translate("SN", "SN"))
        self.lb_sn.setText(_translate("SN", "SN："))

