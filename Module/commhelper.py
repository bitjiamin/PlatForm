# -*- coding: UTF-8 -*-
"""
FileName: tcptool.py
Author: jiaminbit@sina.com
Create date: 2018.9.26
description: tcp调试工具
Update date：2018.9.26
version 1.0.0
"""

import socket
import time
import threading
import log


socket.setdefaulttimeout(0.5)
class TcpClient():
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tcp_connect(self, ip, port):
        try:
            ret = self.skt.connect((ip, port))
            if(ret == None):
                return True
            else:
                return False
        except Exception as e:
            log.loginfo.process_log('tcp_connect '+str(e))
            return False

    def tcp_send(self, sendmsg):
        try:
            self.skt.send(sendmsg.encode())
            return True
        except Exception as e:
            log.loginfo.process_log('tcp_send'+str(e))
            return False

    def tcp_recv(self):
        try:
            recvbytes = self.skt.recv(1024)
            recvmsg = recvbytes.decode()
            return recvmsg
        except Exception as e:
            if(str(e)!='timed out'):
                log.loginfo.process_log('tcp_recv'+str(e))
            return ''

    def tcp_close(self):
        try:
            self.skt.close()
        except Exception as e:
            log.loginfo.process_log('tcp_close'+str(e))
            return False

class TcpServer():
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socks = []
        self.clientname = []
        self.recv_data = []

    def start_server(self, port):
        server_address = ('127.0.0.1', port)
        # bind port
        print('starting listen on ip %s, port %s' % server_address)
        self.skt.bind(server_address)
        # starting listening, allow only one connection
        try:
            self.skt.listen(1)
            self.listen_thread = threading.Thread(target=self.listening)
            self.listen_thread.setDaemon(True)
            self.listen_thread.start()

            self.recv_thread = threading.Thread(target=self.server_recv)
            self.recv_thread.setDaemon(True)
            self.recv_thread.start()

        except Exception as e:
            print("fail to listen on port %s" % e)
            sys.exit(1)

    def listening(self):
        while(True):
            try:
                self.client, addr = self.skt.accept()
                print(addr)
                self.socks.append(self.client)
                self.recv_data.append('')
            except Exception as e:
                pass

    def server_recv(self):
        while(True):
            for index, s in enumerate(self.socks):
                try:
                    data = s.recv(1024)  # 到这里程序继续向下执行
                    s_data = data.decode()
                    if(s_data.split(',')[1]=='SYN'):
                        self.clientname.append(s_data.split(',')[0])
                    if(s_data!=''):
                        self.recv_data[index] = data.decode()
                except Exception as e:
                    pass

    def server_send(self, clientid, sendmsg):
        # clientid指定朝哪个客户端发送
        for addr in self.addrs:
            print(addr)
        self.socks[clientid].send(sendmsg.encode())