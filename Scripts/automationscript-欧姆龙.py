import os
import csv
import socket
import time
import struct
import sys
import random

socket.setdefaulttimeout(0.5)
class AutoMation():
    def __init__(self, parent=None):
        self.io = self.read_config()

    def choose_axis(self, axis_name):
        if(axis_name == 'AXIS1'):
            self.dev_id = 0
        if (axis_name == 'AXIS2'):
            self.dev_id = 1
        if (axis_name == 'AXIS3'):
            self.dev_id = 6

    def read_rt_pos(self):
        return random.random()

    #读取IO配置列表
    def read_config(self):
        self.path = os.getcwd()
        self.cvspath = str(self.path)+ '/CSV Files/' + 'IO Config.csv'
        csvfile = open(self.cvspath, 'r')
        reader = csv.reader(csvfile)
        self.io_channel=[]
        self.io_channel2=[]
        for seg in reader:
            self.io_channel.append(seg[2])
        for seg2 in self.io_channel[1:]:    #从csv表第2行开始读int数据
            self.io_channel2.append(int(seg2))
        self.io_channel2 = sorted(self.io_channel2)
        self.start_index = self.io_channel2[0]      #io开始位索引
        self.io_length = self.io_channel2[-1]-self.io_channel2[0]+1     #读取长度
        return [self.start_index, self.io_length]

    def create_connect(self):     #输入参数为本机IP，字符串
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            PC_ip = '192.168.250.2'
            self.ip = '192.168.250.1'   #PLC IP Adress, Port
            self.port = 9600
            pc_ip_list = PC_ip.split('.')   #本机ip 字符串分割
            self.pc_ip_last = int(pc_ip_list[3]).to_bytes(1,'big')  #提取本机ip末段
            con_ok = self.skt.connect((self.ip, self.port))
            if (con_ok == None):
                self.recving = True
                msg = b'\x46\x49\x4E\x53\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'+self.pc_ip_last
                ret = self.send_and_recv(msg)
                if ret == b'FINS\x00\x00\x00\x10\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'+self.pc_ip_last+b'\x00\x00\x00\x01':
                    return True
                else:
                    self.skt.close()
                    self.recving = False
                    return False
        except Exception as e:
            print(e)

    def close_connect(self):
        self.recving = False
        self.skt.close()
        return True

    def read_io_state(self):
        index = self.io[0]
        length = self.io[1]
        io_state = ''
        rs = index.to_bytes(1, 'big')    #io开始位索引转byte
        rl = length.to_bytes(1, 'big')      #长度转byte
        msg = b'\x46\x49\x4E\x53\x00\x00\x00\x1A\x00\x00\x00\x02\x00\x00\x00\x00\x80\x00\x02\x00\x01\x00\x00'\
              +self.pc_ip_last+b'\x00\xFF\x01\x01\xb1\x00' + rs + b'\x00\x00' + rl
        try:
            ret = self.send_and_recv(msg)
            values = ret[-length * 2:]         #返回数据进行切片
            d_ret = struct.unpack('>' + 'H' * length, bytes(values))       #解析成ushort
            for d_ret0 in d_ret:                                           #String
                io_state = io_state + str(d_ret0)
        except Exception as e:
            io_state = '0'
            io_state = io_state.zfill(length)
        return io_state

    def write_io_state(self,index,value):
        data = b''
        ws = index.to_bytes(1, 'big')               #io开始位索引转byte
        data = struct.pack('>H', value)             #写入值转byte
        msg = b'\x46\x49\x4E\x53\x00\x00\x00\x1c\x00\x00\x00\x02\x00\x00\x00\x00\x80\x00\x02\x00\x01\x00\x00'\
              +self.pc_ip_last+b'\x00\xFF\x01\x02\xb1\x00' + ws + b'\x00\x00\x01' + data
        ret = self.send_and_recv(msg)
        if ret == b'FINS\x00\x00\x00\x16\x00\x00\x00\x02\x00\x00\x00\x00\xc0\x00\x02\x00'\
                  +self.pc_ip_last+b'\x00\x00\x01\x00\xff\x01\x02\x00\x00':
            return True
        else:
            return False

    def send_and_recv(self, msg):
        try:
            self.skt.send(msg)
            ret = self.skt.recv(1024)
        except Exception as e:
            ret = b''
            print(e)
        return ret