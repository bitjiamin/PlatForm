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
#import visionscript


class TestFunc():
    def __init__(self):
        try:
            self.zmq_open()
            #self.vision = visionscript.Vision()
        except Exception as e:
            log.loginfo.process_log('testscript1 init:' + str(e))

    def __del__(self):
        self.zmq_close()

    def zmq_open(self):
        self.con = zmq.Context()
        self.socket = self.con.socket(zmq.REQ)
        #接收超时2秒，发送超时1秒
        self.socket.RCVTIMEO = 2000
        self.socket.SNDTIMEO = 1000
        try:
            self.socket.connect('tcp://127.0.0.1:5555')
        except Exception as e:
            log.loginfo.process_log(str(e))

    def zmq_comm(self, msg):
        try:
            #发送数据
            snd = self.socket.send_string(msg)
            #接收数据
            ret = self.socket.recv_string()
            return ret
        except Exception as e:
            log.loginfo.process_log(str(e))
            return ''

    def zmq_close(self):
        self.socket.close()

    def pretest(self):
        time.sleep(0.2)
        ret = [0,  'pretest']
        return ret

    def function1(self):
        time.sleep(0.2)
        ret = [0,  'step1']
        return ret

    def function2(self):
        time.sleep(0.2)
        ret = [0, 'step2']
        return ret

    def function3(self):
        time.sleep(0.1)
        ret = [0, 'step3']
        return ret

    def function4(self):
        time.sleep(0.1)
        ret = [0, 'step4']
        return ret

    def function5(self):
        time.sleep(0.1)
        ret = [0, 'step5']
        return ret

    def function6(self):
        time.sleep(0.1)
        ret = [0, 'step6']
        return ret

    def function7(self):
        time.sleep(0.1)
        ret = [0, 'step7']
        return ret

    def function8(self):
        time.sleep(0.1)
        ret = [0, 'step8']
        return ret

    def function9(self):
        time.sleep(0.1)
        ret = [0, 'step9']
        return ret

    def function10(self):
        time.sleep(0.1)
        ret = [0, 'step10']
        return ret

    def posttest(self):
        time.sleep(0.1)
        ret = [0, 'posttest']
        return ret