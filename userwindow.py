# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/jiamin/Desktop/Develop/Python/Program/TestUI/usermanage.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_usermanage(object):
    def setupUi(self, usermanage):
        usermanage.setObjectName("usermanage")
        usermanage.resize(446, 397)
        self.gridLayout = QtWidgets.QGridLayout(usermanage)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_deluser = QtWidgets.QPushButton(usermanage)
        self.pb_deluser.setObjectName("pb_deluser")
        self.gridLayout.addWidget(self.pb_deluser, 3, 2, 1, 1)
        self.le_new = QtWidgets.QLineEdit(usermanage)
        self.le_new.setObjectName("le_new")
        self.gridLayout.addWidget(self.le_new, 2, 1, 1, 1)
        self.lb_new = QtWidgets.QLabel(usermanage)
        self.lb_new.setObjectName("lb_new")
        self.gridLayout.addWidget(self.lb_new, 2, 0, 1, 1)
        self.tw_user = QtWidgets.QTableWidget(usermanage)
        self.tw_user.setObjectName("tw_user")
        self.tw_user.setColumnCount(0)
        self.tw_user.setRowCount(0)
        self.gridLayout.addWidget(self.tw_user, 3, 0, 1, 2)
        self.pb_savepw = QtWidgets.QPushButton(usermanage)
        self.pb_savepw.setObjectName("pb_savepw")
        self.gridLayout.addWidget(self.pb_savepw, 2, 2, 1, 1)
        self.lb_old = QtWidgets.QLabel(usermanage)
        self.lb_old.setObjectName("lb_old")
        self.gridLayout.addWidget(self.lb_old, 1, 0, 1, 1)
        self.le_old = QtWidgets.QLineEdit(usermanage)
        self.le_old.setObjectName("le_old")
        self.gridLayout.addWidget(self.le_old, 1, 1, 1, 1)
        self.lb_usertitle = QtWidgets.QLabel(usermanage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_usertitle.sizePolicy().hasHeightForWidth())
        self.lb_usertitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lb_usertitle.setFont(font)
        self.lb_usertitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_usertitle.setObjectName("lb_usertitle")
        self.gridLayout.addWidget(self.lb_usertitle, 0, 0, 1, 3)

        self.retranslateUi(usermanage)
        QtCore.QMetaObject.connectSlotsByName(usermanage)

    def retranslateUi(self, usermanage):
        _translate = QtCore.QCoreApplication.translate
        usermanage.setWindowTitle(_translate("usermanage", "Dialog"))
        self.pb_deluser.setText(_translate("usermanage", "Delete"))
        self.lb_new.setText(_translate("usermanage", "New Password:"))
        self.pb_savepw.setText(_translate("usermanage", "Save Password"))
        self.lb_old.setText(_translate("usermanage", "Old Password:"))
        self.lb_usertitle.setText(_translate("usermanage", "User Management"))

