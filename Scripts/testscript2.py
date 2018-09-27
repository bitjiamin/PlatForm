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
import threading
import visionscript
import globaldata
from tcpclient import *


class TestFunc():
    def __init__(self):
        try:
            self.vision = visionscript.Vision()
            self.done = False
            self.tcp1 = TcpClient()
            self.tcp2 = TcpClient()
            self.tcp1.tcp_connect('172.11.0.55', 4000)
            self.tcp1.tcp_send('tcp1')
            self.main_thread()
        except Exception as e:
            log.loginfo.process_log('testscript1 init:' + str(e))

    def __del__(self):
        self.zmq_close()

    def run_step(self, step):
        self.done = False
        globaldata.singnal.runsingnal[1].emit([1, 'Start'+step])

    def main_thread(self):
        self.recv_thread = threading.Thread(target=self.tcp_recv)
        self.recv_thread.setDaemon(True)
        self.recv_thread.start()

    def tcp_recv(self):
        time.sleep(5)
        self.sequence()
        while(True):
            ret = self.tcp1.tcp_recv()
            if(ret!=''):
                self.run_step(ret)

    def sequence(self):
        self.run_step('prerun')
        while(self.done==False):
            time.sleep(0.1)
        self.run_step('function1')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function2')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function3')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function4')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function5')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function6')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function7')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function8')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('function9')
        while (self.done == False):
            time.sleep(0.1)
        self.run_step('postrun')
        while (self.done == False):
            time.sleep(0.1)

    def zmq_open(self):
        self.con = zmq.Context()
        self.socket = self.con.socket(zmq.REQ)
        # 接收超时2秒，发送超时1秒
        self.socket.RCVTIMEO = 2000
        self.socket.SNDTIMEO = 1000
        try:
            self.socket.connect('tcp://127.0.0.1:5555')
        except Exception as e:
            log.loginfo.process_log(str(e))

    def zmq_comm(self, msg):
        try:
            # 发送数据
            snd = self.socket.send_string('Start' + msg)
            # 接收数据
            ret = self.socket.recv_string()
            return ret
        except Exception as e:
            log.loginfo.process_log(str(e))
            return ''

    def zmq_close(self):
        self.socket.close()

    def prerun(self):
        time.sleep(1)
        ret = [0, 'pretest']
        self.done = True
        return ret

    def function1(self):
        self.vision.read_image()
        ret = [0, 0, 0, 'step1']
        self.done = True
        return ret

    def function2(self):
        time.sleep(1)
        ret = [0, 'step2']
        self.done = True
        return ret

    def function3(self):
        time.sleep(1)
        ret = [0, 'step3']
        self.done = True
        return ret

    def function4(self):
        time.sleep(0.1)
        ret = [0, 'step4']
        self.done = True
        return ret

    def function5(self):
        time.sleep(1)
        ret = [0, 'step5']
        self.done = True
        return ret

    def function6(self):
        time.sleep(0.1)
        ret = [0, 'step6']
        self.done = True
        return ret

    def function7(self):
        time.sleep(1)
        ret = [0, 'step7']
        self.done = True
        return ret

    def function8(self):
        time.sleep(0.1)
        ret = [0, 'step8']
        self.done = True
        return ret

    def function9(self):
        time.sleep(0.1)
        ret = [0, 'step9']
        self.done = True
        return ret

    def function10(self):
        time.sleep(0.1)
        ret = [0, 'step10']
        self.done = True
        return ret

    def postrun(self):
        time.sleep(0.1)
        ret = [0, 'posttest']
        self.done = True
        return ret