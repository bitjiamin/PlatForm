# -*- coding: UTF-8 -*-
"""
FileName: testscript.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 测试脚本，将各测试项的函数定义在该文件中
Update date：2017.7.20
version 1.0.0
"""

import time
import log
import zmq
import os
import subprocess

#subprocess.Popen('C:\Project\Pnco.exe')
class TestFunc():
    def __init__(self):
        self.zmq_open()

    def zmq_open(self):
        self.con = zmq.Context()
        self.socket = self.con.socket(zmq.REQ)
        #接收超时2秒，发送超时1秒
        self.socket.RCVTIMEO = 2000
        self.socket.SNDTIMEO = 1000
        try:
            self.socket.connect('tcp://127.0.0.1:5000')
        except Exception as e:
            log.process_log(str(e))

    def zmq_comm(self):
        try:
            time.sleep(0.5)
            #发送数据
            #snd = self.socket.send_string('12345')
            #接收数据
            #ret = self.socket.recv_string()
            return ''
        except Exception as e:
            #log.loginfo.process_log(str(e))
            return ''

    def zeq_close(self):
        self.socket.close()

    def function1(self):
        self.zmq_comm()
        return[0.5, 0.1]

    def function2(self):
        self.zmq_comm()
        return [10]

    def function3(self):
        self.zmq_comm()
        return [3.0]

    def function4(self):
        self.zmq_comm()
        return [0.5]

    def function5(self):
        self.zmq_comm()
        return [0.5]

    def function6(self):
        self.zmq_comm()
        return [0.5]

    def function7(self):
        self.zmq_comm()
        return [0.5]

    def function8(self):
        self.zmq_comm()
        return [0.9]

    def function9(self):
        self.zmq_comm()
        return [0.9]

    def function10(self):
        self.zmq_comm()
        return [0.5]

    def function11(self):
        self.zmq_comm()
        return [0.9]

    def function12(self):
        self.zmq_comm()
        return [0.9]

class TestFunc2():

    def function1(self):
        time.sleep(0.2)
        return[0.5, 0.6]

    def function2(self):
        time.sleep(0.5)
        return [0.1]

    def function3(self):
        time.sleep(0.3)
        return [0.5]

    def function4(self):
        time.sleep(0.5)
        return [0.5]

    def function5(self):
        time.sleep(0.4)
        return [0.5]

    def function6(self):
        time.sleep(0.2)
        return [0.5]

    def function7(self):
        time.sleep(0.3)
        return [0.5]

    def function8(self):
        time.sleep(0.4)
        return [0.9]

    def function9(self):
        time.sleep(0.5)
        return [0.9]

    def function10(self):
        time.sleep(0.2)
        return [0.5]

    def function11(self):
        time.sleep(0.4)
        return [0.9]

    def function12(self):
        time.sleep(0.5)
        return [0.9]
