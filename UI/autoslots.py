# -*- coding: UTF-8 -*-
"""
FileName: motioncthread.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 运动控制相关操作
Update date：2017.7.20
version 1.0.0
"""

import csv
import time
import threading
from PyQt5.QtWidgets import *
import systempath
import log
from autosetup import *
from imp import reload

try:
    import automationscript
except Exception as e:
    log.loginfo.process_log(str(e))

def reload_scripts():
    try:
        reload(automationscript)
        log.loginfo.process_log('reload auto script ok')
    except Exception as e:
        log.loginfo.process_log(str(e))

auto = None
class AutoThread(AutoUI, QDialog):
    def __init__(self, parent=None):
        super(AutoThread, self).__init__(parent)
        self.io_name = []
        self.io_desc = []
        self.io_value = []
        self.io_index = []
        self.writing = False
        self.read_io_config()
        self.read_axis_config()
        self.initialize_motion_ui()
        self.initialize_motion()

    # 初始化IO表，从配置文件中读取信息
    def initialize_motion_ui(self):
        self.tw_io.setMaximumWidth(self.width * 0.4)
        self.read_io_config()
        self.read_axis_config()
        self.tw_io.setColumnCount(2)
        self.tw_io.setRowCount(len(self.io_name) + 10)
        self.tw_io.setHorizontalHeaderLabels(['IO', 'Description'])
        self.mapper = QtCore.QSignalMapper(self)
        i = 0
        for seq in self.io_name:
            if(i != 0):
                self.MyCheck = QCheckBox()
                self.MyCheck.setText('--- ' + seq)
                self.tw_io.setCellWidget(i-1, 0, self.MyCheck)
                newItem = QTableWidgetItem(self.io_desc[i])
                self.tw_io.setItem(i - 1, 1, newItem)
                # 原始信号（表格中checkbox的鼠标点击信号）传递给map
                self.tw_io.cellWidget(i - 1, 0).clicked.connect(self.mapper.map)
                # 设置map信号的转发规则, 转发为参数为int类型的信号
                self.mapper.setMapping(self.tw_io.cellWidget(i - 1, 0), i - 1)
            i = i+1

        # map信号连接到自定义的槽函数，参数类型为int
        self.mapper.mapped[int].connect(self.write_io)

        self.tw_io.horizontalHeader().setStretchLastSection(True)
        j = 0
        self.cb_axis.clear()
        for seq in self.axis_name:
            if(j != 0):
                self.cb_axis.addItem(seq)
            j = j+1

    def read_io_config(self):
        self.path = systempath.bundle_dir + '/CSV Files/' + 'IO Config.csv'
        csvfile = open(self.path, 'r')
        reader = csv.reader(csvfile)
        self.io_name = []
        self.io_desc = []
        self.io_index = []
        i = 0
        for seq in reader:
            self.io_name.append(seq[0])
            self.io_desc.append(seq[1])
            if(i!=0):
                self.io_index.append(int(seq[2]))
            i = i + 1

    def read_axis_config(self):
        self.path = systempath.bundle_dir + '/CSV Files/' + 'Axis Config.csv'
        csvfile = open(self.path, 'r')
        reader = csv.reader(csvfile)
        self.axis_name = []
        self.axis_desc = []
        for seq in reader:
            self.axis_name.append(seq[0])
            self.axis_desc.append(seq[1])

    def initialize_motion(self):
        # 创建连接
        #if(self.create_connect()):
            #log.loginfo.process_log('Connect PLC OK!')
        #else:
            #log.loginfo.process_log('Connect PLC Fail!')
        self.recv_thread = threading.Thread(target=self.refresh_rt_info)
        self.recv_thread.setDaemon(True)
        self.recv_thread.start()

    def write_io(self, index):
        self.writing = True
        m_index = self.io_index[index]
        self.writing = False

    def read_io_state(self):
        # 从最小的寄存器开始读取，中间无间断
        ret = [0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.io_value = []
        for index in self.io_index:
            self.io_value.append(ret[index-min(self.io_index)])
        return self.io_value

    def refresh_rt_info(self):
        while(True):
            if(self.writing == False):
                self.refresh_motion_para([1, self.read_io_state()])
                time.sleep(0.05)

    # 刷新运动控制参数（IO）
    def refresh_motion_para(self, ls):
        self.dsb_real_pos.setValue(ls[0])
        i = 0
        for io in ls[1]:
            if (io == 1):
                self.tw_io.cellWidget(i, 0).setChecked(True)
            else:
                self.tw_io.cellWidget(i, 0).setChecked(False)
            i = i + 1