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
from PyQt5 import QtCore
import systempath
import log
import autosetup
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
class AutoThread(QDialog):
    # 实现一个单例类
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self, parent=None):
        super(AutoThread, self).__init__(parent)
        self.autoui = autosetup.AutoUI()
        self.io_name = []
        self.io_on = []
        self.io_off = []
        self.io_value = []
        self.io_index = []
        self.read_io_config()
        self.read_axis_config()
        self.read_para_config()
        self.initialize_motion_ui()
        self.initialize_motion_state()
        # 连接写参数信号与槽
        self.autoui.tw_para.itemChanged.connect(self.write_para)


    # 初始化IO表，从配置文件中读取信息
    def initialize_motion_ui(self):
        self.autoui.tw_io.setMaximumWidth(self.autoui.width * 0.4)
        self.read_io_config()
        self.read_axis_config()
        # 初始化参数表格
        self.autoui.tw_para.setColumnCount(3)
        self.autoui.tw_para.setRowCount(len(self.para_name)-1)
        self.autoui.tw_para.setHorizontalHeaderLabels(['Parameters', 'Read', 'Write'])
        self.autoui.tw_para.horizontalHeader().setStretchLastSection(True)
        i = 0
        for seq in self.para_name:
            if(i>0):
                newItem = QTableWidgetItem(seq)
                self.autoui.tw_para.setItem(i-1, 0, newItem)
            i = i + 1

        # 初始化io表格
        self.autoui.tw_io.setColumnCount(2)
        self.autoui.tw_io.setRowCount(len(self.io_name)-1)
        self.autoui.tw_io.setHorizontalHeaderLabels(['IO', 'State'])
        self.autoui.tw_io.horizontalHeader().setStretchLastSection(True)
        # 连接io表格信号与槽函数
        self.mapper = QtCore.QSignalMapper(self)
        i = 0
        for seq in self.io_name:
            if(i != 0):
                self.MyCheck = QCheckBox()
                self.MyCheck.setText('--- ' + seq)
                self.autoui.tw_io.setCellWidget(i-1, 0, self.MyCheck)
                # newItem = QTableWidgetItem(self.io_desc[i])
                # self.tw_io.setItem(i - 1, 1, newItem)
                # 原始信号（表格中checkbox的鼠标点击信号）传递给map
                self.autoui.tw_io.cellWidget(i - 1, 0).clicked.connect(self.mapper.map)
                # 设置map信号的转发规则, 转发为参数为int类型的信号
                self.mapper.setMapping(self.autoui.tw_io.cellWidget(i - 1, 0), i - 1)
            i = i+1
        # map信号连接到自定义的槽函数，参数类型为int
        self.mapper.mapped[int].connect(self.write_io)
        # 初始化轴信息
        j = 0
        self.autoui.cb_axis.clear()
        for seq in self.axis_name:
            if(j != 0):
                self.autoui.cb_axis.addItem(seq)
            j = j+1


    def read_io_config(self):
        self.path = systempath.bundle_dir + '/CSV Files/' + 'IO.csv'
        csvfile = open(self.path, 'r')
        reader = csv.reader(csvfile)
        self.io_name = []
        self.io_on = []
        self.io_off = []
        self.io_index = []
        i = 0
        for seq in reader:
            self.io_name.append(seq[0])
            self.io_on.append(seq[2])
            self.io_off.append(seq[3])
            if(i!=0):
                self.io_index.append(int(seq[1]))
            i = i + 1

    def read_para_config(self):
        self.path = systempath.bundle_dir + '/CSV Files/' + 'Parameters.csv'
        csvfile = open(self.path, 'r')
        reader = csv.reader(csvfile)
        self.para_name = []
        self.para_index = []
        i = 0
        for seq in reader:
            self.para_name.append(seq[0])
            self.para_index.append(seq[1])
            i = i + 1

    def read_axis_config(self):
        self.path = systempath.bundle_dir + '/CSV Files/' + 'Axis.csv'
        csvfile = open(self.path, 'r')
        reader = csv.reader(csvfile)
        self.axis_name = []
        self.axis_desc = []
        for seq in reader:
            self.axis_name.append(seq[0])
            self.axis_desc.append(seq[1])

    def initialize_motion_state(self):
        # self.recv_thread = threading.Thread(target=self.refresh_rt_info)
        # self.recv_thread.setDaemon(True)
        # self.recv_thread.start()
        self.read_init_state()

    def write_io(self, index):
        state = self.autoui.tw_io.cellWidget(index, 0).isChecked()
        if(state):
            newItem = QTableWidgetItem(self.io_on[index+1])
        else:
            newItem = QTableWidgetItem(self.io_off[index+1])
        self.autoui.tw_io.setItem(index, 1, newItem)
        print('write io ok')
        # 需添加自定义写IO代码

    def write_para(self, item):
        if (item.column() == 2):
            newItem = QTableWidgetItem(item.text())
            self.autoui.tw_para.setItem(item.row(), 1, newItem)
            # 需添加自定义写参数代码
            print('write para ok')

    def read_init_state(self):
        # 从最小的寄存器开始读取，中间无间断
        try:
            ret = [0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            para = [0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            self.io_value = []
            self.para_value = []
            for index in self.io_index:
                self.io_value.append(ret[index-min(self.io_index)])

            for i in range(len(self.para_name)-1):
                self.para_value.append(para[i])
            self.refresh_motion_para(self.io_value, self.para_value)
        except Exception as e:
            print(e)

    # 刷新运动控制参数（IO,Para）
    def refresh_motion_para(self, ls_io, ls_para):
        # self.dsb_real_pos.setValue(ls_io[0])
        i = 0
        for io in ls_io:
            if (io == 1):
                self.autoui.tw_io.cellWidget(i, 0).setChecked(True)
                newItem = QTableWidgetItem(self.io_on[i + 1])
                self.autoui.tw_io.setItem(i, 1, newItem)
            else:
                self.autoui.tw_io.cellWidget(i, 0).setChecked(False)
                newItem = QTableWidgetItem(self.io_off[i + 1])
                self.autoui.tw_io.setItem(i, 1, newItem)
            i = i + 1
        i = 0
        for para in ls_para:
            newItem = QTableWidgetItem(str(para))
            self.autoui.tw_para.setItem(i, 1, newItem)
            newItem1 = QTableWidgetItem(str(para))
            self.autoui.tw_para.setItem(i, 2, newItem1)
            i = i + 1