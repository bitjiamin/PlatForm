# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from scansn import *
import dataexchange


class SNUI(Ui_SN, QDialog):
    def __init__(self, parent=None):
        super(SNUI, self).__init__(parent)
        self.setupUi(self)
        # 获取屏幕分辨率
        self.screen = QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        self.resize(self.width * 0.3, self.height * 0.1)
        self.le_sn.setMaximumHeight(self.height*0.03)
        self.lb_sn.setMaximumHeight(self.height * 0.03)
        self.le_sn.returnPressed.connect(self.input_sn)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.le_sn.setEnabled(True)
        self.le_sn.setText('')
        self.le_sn.setFocus()

    def input_sn(self):
        dataexchange.sn = self.le_sn.text()
        self.close()

