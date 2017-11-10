# -*- coding: UTF-8 -*-
"""
FileName: automationscript.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 自动化脚本，将运动控制相关函数定义在改文件
Update date：2017.7.20
version 1.0.0
"""

import random
import socket
import struct
import time
import systempath
import csv

class AutoMation():
    def __init__(self):
        self.running = False
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dev_id = 0

    def create_connect(self):
        try:
            con_ok = self.skt.connect(('169.254.11.146', 5000))
            # con_ok = self.skt.connect(('192.168.52.74', 5000))
            if (con_ok != None):
                return True
        except Exception as e:
            print(e)
            return False
        return True

    def close_connect(self):
        self.skt.close()

    def choose_axis(self, axis_name):
        if(axis_name == 'AXIS1'):
            self.dev_id = 0
        if (axis_name == 'AXIS2'):
            self.dev_id = 1
        if (axis_name == 'AXIS3'):
            self.dev_id = 6

    def send_and_recv(self, msg):
        while(self.running):
            time.sleep(0.02)
        self.running = True
        try:
            self.skt.send(msg)
            recvmsg = (self.skt.recv(1024)).decode()
        except Exception as e:
            print(e)
        self.running = False

    def convert_data(self, func_id, value):
        func_id = struct.pack('<H', func_id)
        dev_id = struct.pack('<H', self.dev_id)
        value = struct.pack('<I', value)
        return func_id + dev_id + value

    def read_rt_pos(self):
        return random.random()

    def jog_forward(self):
        data = self.convert_data(5, 0)
        self.send_and_recv(data)
        return True

    def jog_backward(self):
        data = self.convert_data(5, 0)
        self.send_and_recv(data)
        return True

    def absolute_run(self, value):
        data = self.convert_data(2, value)
        self.send_and_recv(data)
        return True

    def relative_run(self, value):
        data = self.convert_data(2, value)
        self.send_and_recv(data)
        return True

    def go_home(self):
        data = self.convert_data(6, 0)
        self.send_and_recv(data)

    def reset(self):
        data = self.convert_data(7, 0)
        self.send_and_recv(data)
        return True

    def stop(self):
        data = self.convert_data(8, 0)
        self.send_and_recv(data)
        return True

    def read_io_state(self):
        self.path = systempath.bundle_dir + '/CSV Files/' + 'IO State.csv'
        csvfile = open(self.path, 'r')
        reader = csv.reader(csvfile)
        io_value = []
        for seq in reader:
            io_value.append(seq[0])
        return io_value

    def write_io_state(self, data):
        print(data)
        self.path = systempath.bundle_dir + '/CSV Files/' + 'IO State.csv'
        csvfile = open(self.path, 'w')
        writer = csv.writer(csvfile)
        writer.writerows(data)