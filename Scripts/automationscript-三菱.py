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
import serial

class AutoMation():
    def __init__(self):
        self.running = False
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dev_id = 0
        self.com = serial.Serial()
        self.com.timeout = 0.5

    def create_connect(self):
        try:
            #con_ok = self.skt.connect(('169.254.11.146', 5000))
            self.com.port = '/dev/cu.usbserial-FT9HNV6L'
            #self.com.port = 'com6'
            self.com.baudrate = 9600
            self.com.parity = serial.PARITY_EVEN
            self.com.bytesize = serial.SEVENBITS
            con_ok = self.com.open()
            if (con_ok == None):
                return True
        except Exception as e:
            return False

    def close_connect(self):
        self.com.close()

    def send_and_recv(self, msg):
        while(self.running):
            time.sleep(0.02)
        self.running = True
        try:
            self.com.flush()
            self.com.write_timeout = 0.5
            self.com.write(msg)
            ret = self.com.read(1024)
        except Exception as e:
            ret = b''
            print(e)
        self.running = False
        return ret

    def read_d(self, d0, cnt):
        stx = b'\x02'
        cmd = b'\x30'
        # 计算D寄存器地址
        d = d0*2 + 0x1000
        # 转换成4位16进制字符串, 注意PLC协议中需要大写
        h_d = hex(d)[2:].zfill(4).upper()
        # 将字符串转字节数组
        b_d = bytes(h_d.encode())
        h_cnt = hex(cnt*2)[2:].zfill(2).upper()
        b_cnt = bytes(h_cnt.encode())
        end = b'\x03'
        data = cmd+b_d+b_cnt+end
        # 计算校验和
        checksum=sum(data)
        # 取校验和的后两位
        h_sum = hex(checksum)[len(hex(checksum))-2:].zfill(2).upper()
        b_sum = bytes(h_sum.encode())
        # data = b'\x02\x31\x31\x30\x46\x36\x30\x34\x33\x34\x31\x32\x43\x44\x41\x42\x03\x34\x39'
        ret = self.send_and_recv(stx + cmd + b_d + b_cnt + end + b_sum)
        ret = ret[1:cnt*4+1]
        ret = ret.decode()
        result = []
        for i in range(int(len(ret)/4)):
            result.append(ret[4*i+2]+ret[4*i+3]+ret[4*i]+ret[4*i+1])
        d_result = []
        for r in result:
            d_result.append(int(r, 16))
        # 返回列表，内容为D寄存器数值（十进制形式）
        return d_result

    def write_d(self, d0, cnt, data):
        b_data = b''
        for data0 in data:
            data0 = hex(data0)[2:]     # 去除0x
            data0 = data0.zfill(4)     # 不满4位的添加到4位
            b_data = b_data + (data0.encode()[2:4] + data0.encode()[0:2]).upper()   # 调转高低位
        stx = b'\x02'
        cmd = b'\x31'
        end = b'\x03'
        # 计算D寄存器地址
        d = d0 * 2 + 0x1000
        # 转换成4位16进制字符串, 注意PLC协议中需要大写
        h_d = hex(d)[2:].zfill(4).upper()
        # 将字符串转字节数组
        b_d = bytes(h_d.encode())
        h_cnt = hex(cnt * 2)[2:].zfill(2).upper()
        b_cnt = bytes(h_cnt.encode())
        dataall = cmd+b_d+b_cnt+b_data+end
        # 计算校验和
        checksum = sum(dataall)
        # 取校验和的后两位
        h_sum = hex(checksum)[len(hex(checksum)) - 2:].zfill(2).upper()
        b_sum = bytes(h_sum.encode())
        ret = self.send_and_recv(stx + cmd + b_d + b_cnt + b_data + end + b_sum)
        if(ret==b'\x06'):
            return True
        else:
            return False

    def force_on_m(self, m0):
        stx = b'\x02'
        cmd = b'\x37'
        # 计算D寄存器地址
        m = m0 + 2048
        # 转换成4位16进制字符串, 注意PLC协议中需要大写
        h_m = hex(m)[2:].zfill(4).upper()
        h_m = h_m[2:4] + h_m[0:2]       # 高低位调转
        # 将字符串转字节数组
        b_m = bytes(h_m.encode())
        etx = b'\x03'
        data = cmd + b_m + etx
        # 计算校验和
        checksum = sum(data)
        # 取校验和的后两位
        h_sum = hex(checksum)[len(hex(checksum)) - 2:].zfill(2).upper()
        b_sum = bytes(h_sum.encode())
        ret = self.send_and_recv(stx + data + b_sum)
        if (ret == b'\x06'):
            return True
        else:
            return False

    def force_off_m(self, m0):
        stx = b'\x02'
        cmd = b'\x38'
        # 计算D寄存器地址
        m = m0 + 2048
        # 转换成4位16进制字符串, 注意PLC协议中需要大写
        h_m = hex(m)[2:].zfill(4).upper()
        h_m = h_m[2:4] + h_m[0:2]  # 高低位调转
        # 将字符串转字节数组
        b_m = bytes(h_m.encode())
        etx = b'\x03'
        data = cmd + b_m + etx
        # 计算校验和
        checksum = sum(data)
        # 取校验和的后两位
        h_sum = hex(checksum)[len(hex(checksum)) - 2:].zfill(2).upper()
        b_sum = bytes(h_sum.encode())
        ret = self.send_and_recv(stx + data + b_sum)
        if (ret == b'\x06'):
            return True
        else:
            return False

    def read_m(self, m0, cnt):
        # 根据需要读取的M寄存器的数量确定需要读取多少个字节
        if(cnt%8 != 0):      # 通过读取数量和读取位置判断实际从哪个地址开始读，读取几个字节（因为只能按字节读取，且开始位置必须是8位的整数倍）
            if(m0%8==0):
                cnt_byte = int(cnt/8 + 1)    # 开始位置为8的整数倍时实际需要读取的字节数
            else:
                cnt_byte = int(cnt / 8 + 2)  # 开始位置不是8的整数倍时需要多读一个字节
        else:
            if (m0 % 8 == 0):
                cnt_byte = int(cnt/8)
            else:
                cnt_byte = int(cnt / 8 + 1)
        stx = b'\x02'
        cmd = b'\x30'
        # 计算D寄存器地址
        m = int(m0/8 + 256)
        # 转换成4位16进制字符串, 注意PLC协议中需要大写
        h_m = hex(m)[2:].zfill(4).upper()
        # 将字符串转字节数组
        b_m = bytes(h_m.encode())
        h_cnt = hex(cnt_byte)[2:].zfill(2).upper()
        b_cnt = bytes(h_cnt.encode())
        end = b'\x03'
        data = cmd+b_m+b_cnt+end
        # 计算校验和
        checksum=sum(data)
        # 取校验和的后两位
        h_sum = hex(checksum)[len(hex(checksum))-2:].zfill(2).upper()
        b_sum = bytes(h_sum.encode())
        ret = self.send_and_recv(stx + cmd + b_m + b_cnt + end + b_sum)
        ret = ret[1:cnt_byte*2+1]
        ret = ret.decode()
        result = []
        # 高低位转换
        r_ret = ''
        for i in range(int(len(ret)/2)):
            r_ret = ret[2*i:2*i+2] + r_ret
        # 转换成二进制并合并
        b_ret = ''
        for r_ret0 in r_ret:
            b_ret0 = bin(int(r_ret0, 16))[2:].zfill(4)
            b_ret= b_ret + b_ret0
        # 反转字符串后索引出需要的位，靠前的字符对应较小的M寄存器
        return b_ret[::-1][m0%8:cnt+m0%8]

    def choose_axis(self, axis_name):
        if(axis_name == 'AXIS1'):
            self.dev_id = 0
        if (axis_name == 'AXIS2'):
            self.dev_id = 1
        if (axis_name == 'AXIS3'):
            self.dev_id = 6

    def read_rt_pos(self):
        return random.random()

    def jog_forward(self):
        ret = self.force_on_m(100)
        return ret

    def jog_backward(self):
        ret = self.force_on_m(100)
        return ret

    def absolute_run(self, value):
        ret = self.force_on_m(100)
        return ret

    def relative_run(self, value):
        ret = self.force_on_m(100)
        return ret

    def go_home(self):
        ret = self.force_on_m(100)
        return ret

    def reset(self):
        ret = self.force_on_m(100)
        return ret

    def stop(self):
        ret = self.force_on_m(100)
        return ret

    def read_io_state(self):
        # 需要读取的最小寄存器与最大寄存器之间的个数
        ret = self.read_m(100, 20)
        return ret

    def write_io_state(self, index, value):
        if(value == 0):
            self.force_off_m(index)
        else:
            self.force_on_m(index)