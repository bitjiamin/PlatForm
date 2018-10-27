# -*- coding: UTF-8 -*-
"""
FileName: automationscript.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 自动化脚本，将运动控制相关函数定义在改文件
Update date：2017.7.20
version 1.0.0
"""


import socket
import struct
import threading


l = threading.Lock()
class FX5U():
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_connect(self):
        try:
            con_ok = self.skt.connect(('192.168.250.20', 6000))
            if (con_ok == None):
                return True
        except Exception as e:
            return False

    def close_connect(self):
        self.skt.close()

    def send_and_recv(self, msg):
        l.acquire()
        try:
            self.skt.send(msg)
            ret = self.skt.recv(2048)
        except Exception as e:
            ret = b''
        l.release()  # 释放锁
        return ret

    def read_d(self, index, length):
        head = b'\x50\x00\x00\xFF\xFF\x03\x00\x0C\x00\x10\x00\x01\x04\x00\x00'
        # 起始位转6位字符串
        b_d0 = index.to_bytes(3, 'little')
        # 寄存器类型
        r_type = b'\xA8'
        # 寄存器长度
        b_cnt=length.to_bytes(2,'little')
        # 发送数据
        ret = self.send_and_recv(head + b_d0 + r_type + b_cnt)
        if(ret[9]!=0 or ret[10]!=0):
            return [-1]*length
        data = ret[11:]
        d_result = []
        for i in range(int(len(data) / 2)):
            result0 = struct.pack('>B',data[2 * i + 1]) + struct.pack('>B',data[2 * i])
            result = struct.unpack('>H',result0)[0]
            d_result.append(result)
        return d_result

    def write_d(self, index, value):
        head1 = b'\x50\x00\x00\xFF\xFF\x03\x00'
        d_len = 12 + 2*len(value)
        b_len = d_len.to_bytes(2, 'little')
        head2 = b'\x10\x00\x01\x14\x00\x00'
        b_index = index.to_bytes(3, 'little')
        r_len = len(value).to_bytes(2, 'little')
        # 寄存器类型
        r_type = b'\xA8'
        b_data = b''
        for data0 in value:
            data0 = int(data0)
            b_data0 = data0.to_bytes(2, 'little')
            b_data = b_data + b_data0
        ret = self.send_and_recv(head1 + b_len + head2 + b_index + r_type + r_len + b_data)
        if(ret[9]!=0 or ret[10]!=0):
            return True
        else:
            return False

    def write_m(self, index, value):    # value为整数型list
        head1 = b'\x50\x00\x00\xFF\xFF\x03\x00'
        # 数据长度
        if(len(value)%2==0):
            d_len = int(12 + len(value)/2)
        else:
            d_len = int(12 + len(value) / 2 + 1)
        b_len = d_len.to_bytes(2, 'little')
        head2 = b'\x10\x00\x01\x14\x01\x00'
        b_index = index.to_bytes(3, 'little')
        # 寄存器类型
        r_type = b'\x90'
        # 寄存器数
        r_len = len(value).to_bytes(2, 'little')
        if(len(value)%2!=0):
            value.append(0)
        b_data = b''
        for i in range(int(len(value)/2)):
            if(value[2 * i]==0 and value[2*i+1]==0):
                b_data0 = b'\x00'
            elif(value[2 * i]==1 and value[2*i+1]==0):
                b_data0 = b'\x10'
            elif (value[2 * i] == 0 and value[2 * i + 1] == 1):
                b_data0 = b'\x01'
            elif (value[2 * i] == 1 and value[2 * i + 1] == 1):
                b_data0 = b'\x11'
            b_data = b_data + b_data0
        ret = self.send_and_recv(head1 + b_len + head2 + b_index + r_type + r_len + b_data)
        if(ret[9]!=0 or ret[10]!=0):
            return False
        else:
            return True

    def read_m(self, index, length):
        # 根据需要读取的M寄存器的数量确定需要读取多少个字节
        index = int(index)
        m_cnt = int(length/16) + 1
        delta_m = index%16
        delta_cnt = length%16

        head = b'\x50\x00\x00\xFF\xFF\x03\x00\x0C\x00\x10\x00\x01\x04\x00\x00'
        # 起始位转6位字符串
        b_d0 = (int(index/16)*16).to_bytes(3, 'little')
        # 寄存器类型
        r_type = b'\x90'
        # 寄存器长度
        s_cnt = hex(m_cnt)[2:].zfill(4).upper()  # 转16进制字符串
        d_cnt = int(s_cnt)
        b_cnt = d_cnt.to_bytes(2, 'little')
        # 发送数据
        ret = self.send_and_recv(head + b_d0 + r_type + b_cnt)
        if (ret[9] != 0 or ret[10] != 0):
            return [-1] * length
        data = ret[11:]
        d_result = []
        s_result = ''
        for i in range(int(len(data) / 2)):
            result0 = struct.pack('>B', data[2 * i + 1]) + struct.pack('>B', data[2 * i])
            result = struct.unpack('>H', result0)[0]
            s_result = bin(result)[2:].zfill(16) + s_result
        s_result = s_result[::-1]
        s_ret = list(s_result[delta_m:delta_m+length])
        ret = [int(i) for i in s_ret]
        return ret