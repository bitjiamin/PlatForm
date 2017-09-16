# -*- coding: UTF-8 -*-
"""
FileName: serialtool.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 串口调试工具
Update date：2017.7.20
version 1.0.0
"""

from PyQt5.QtWidgets import QDialog
import serial
import serial.tools.list_ports
from serialwindow import *
import threading
import time
import log

class SerialTool(Ui_serialtool, QDialog):
    def __init__(self, parent = None):
        super(SerialTool, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Serial Debug')
        self.pb_serialcon.clicked.connect(self.serial_connect)
        self.pb_serialsend.clicked.connect(self.serial_send)
        self.com = serial.Serial()

    def list_serial_port(self):
        self.cb_serialname.clear()
        self.pb_serialsend.setEnabled(False)
        self.port_list = list(serial.tools.list_ports.comports())
        for port in self.port_list:
            self.serial_port = list(port)[0]
            self.cb_serialname.addItem(self.serial_port)


    def serial_connect(self):
        if (self.pb_serialcon.text() == 'Connect'):
            try:
                self.com.port = self.cb_serialname.currentText()
                self.com.baudrate = int(self.cb_baund.currentText())
                self.bytesize = [serial.EIGHTBITS, serial.SEVENBITS, serial.SIXBITS, serial.FIVEBITS]
                self.parity = [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK, serial.PARITY_SPACE]
                self.stopbit = [serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO]
                self.com.bytesize = self.bytesize[self.cb_databit.currentIndex()]
                self.com.parity = self.parity[self.cb_checkbit.currentIndex()]
                self.com.stopbits = self.stopbit[self.cb_stopbit.currentIndex()]
                if(self.cb_fluid.currentIndex()==0):
                    self.com.xonxoff = False
                    self.com.rtscts = False
                elif(self.cb_fluid.currentIndex()==1):
                    self.com.xonxoff = True
                    self.com.rtscts = False
                elif (self.cb_fluid.currentIndex() == 2):
                    self.com.xonxoff = False
                    self.com.rtscts = True
                self.com.open()
                if(self.com.is_open):
                    self.pb_serialsend.setEnabled(True)
                    self.pb_serialcon.setText('Close')
            except Exception as e:
                log.loginfo.process_log(e)
                self.pb_serialsend.setEnabled(False)
        else:
            self.recving = False
            self.com.close()
            self.pb_serialcon.setText('Connect')
        self.recving = True
        self.recv_thread = threading.Thread(target=self.serial_recv)
        self.recv_thread.setDaemon(True)
        self.recv_thread.start()
        return self.com.is_open

    def serial_send(self):
        try:
            self.com.write_timeout = 0.5
            self.com.write(self.te_serialsendmsg.toPlainText().encode())
        except Exception as e:
            log.loginfo.process_log(str(e))

    def serial_recv(self):
        while self.recving:
            try:
                self.com.timeout = 0.5
                ret = self.com.read(1024)
                if(len(ret)!=0):
                    self.te_serialrecvmsg.append(ret.decode())
            except Exception as e:
                log.loginfo.process_log(str(e))

    def closeEvent(self, event):
        try:
            self.recving = False
            self.pb_serialcon.setText('Connect')
            self.pb_serialsend.setEnabled(False)
            self.com.close()
        except Exception as e:
            log.loginfo.process_log(str(e))

