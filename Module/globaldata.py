# -*- coding: utf-8 -*-
from PyQt5 import QtCore


# 全局变量
sn = ''
username = ''


# 全局信号
class GlobalSingnal(QtCore.QThread):
    singnal1 = QtCore.pyqtSignal(list)
    singnal2 = QtCore.pyqtSignal(list)
    singnal3 = QtCore.pyqtSignal(list)
    singnal4 = QtCore.pyqtSignal(list)
    def __init__(self,parent=None):
        super(GlobalSingnal, self).__init__(parent)
        self.runsingnal = [self.singnal1, self.singnal2, self.singnal3, self.singnal4]

# 初始化全局信号
global singnal
def init_singnal():
    global singnal
    singnal = GlobalSingnal()