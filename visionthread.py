# -*- coding: UTF-8 -*-
"""
FileName: visionthread.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 视觉脚本
Update date：2017.7.20
version 1.0.0
"""

from PyQt5.QtGui import QImage
import threading
from PyQt5 import QtCore
import visionscript


visions = None
class VisionThread(QtCore.QThread):
    imgsignal = QtCore.pyqtSignal(QImage)
    def __init__(self, parent=None):
        super(VisionThread, self).__init__(parent)
        self.stoplive = False
        global visions
        visions = visionscript.Vision()

    def init_win(self,id,row1, col1, row2, col2):
        visions.init_window(id,row1, col1, row2, col2)

    def load_image(self):
        qimg = visions.load_image()
        return qimg

    def find_cameras(self):
        return visions.find_cameras()

    def open_camera(self, num):
        return visions.open_camera(num)

    def close_camera(self):
        visions.close_camera()

    def snap(self):
        visions.snap()

    def start_live(self):
        self.live_thread = threading.Thread(target=self.live)
        self.live_thread.setDaemon(True)
        self.live_thread.start()

    def live(self):
        while(True):
            visions.snap()
            if(self.stoplive):
                break


