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
from PyQt5.QtGui import QColor, QBrush
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
class AutoThread(QDialog,QtCore.QThread):
    refreshpara = QtCore.pyqtSignal(list)
    refreshio = QtCore.pyqtSignal(list)
    refreshaxis = QtCore.pyqtSignal(list)
    # 实现一个单例类,只初始化一次
    _instance = None
    __first_init = True
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self, parent=None):
        if (self.__class__.__first_init):  # 只初始化一次
            self.__class__.__first_init = False  # 只初始化一次
            super(AutoThread, self).__init__(parent)
            self.stop_rt = False
            self.autoui = autosetup.AutoUI()
            self.autoui.showsingnal.connect(self.show_event)
            self.autoui.closesingnal.connect(self.close_event)
            self.auto = automationscript.AutoMation()
            self.io_name = []
            self.io_on = []
            self.io_off = []
            self.io_value = []
            self.io_index = []
            self.in_en = []
            self.io_value_en = []
            self.refreshpara.connect(self.refresh_para)
            self.refreshio.connect(self.refresh_io)
            self.refreshaxis.connect(self.refresh_axis_ui)
            init_iopath = systempath.bundle_dir + '/CSV Files/IO.csv'
            self.read_io_config(0, True)
            self.read_axis_config()
            self.read_para_config(0, True)
            self.initialize_motion_ui()
            self.initialize_motion_state()
            # 连接写参数信号与槽
            self.autoui.cb_axis.currentIndexChanged.connect(self.auto.choose_axis)
            self.autoui.tw_para.itemChanged.connect(self.set_para)
            self.autoui.pb_jog1.pressed.connect(self.auto.jog_forward)
            self.autoui.pb_jog1.released.connect(self.auto.jog_forward_stop)
            self.autoui.pb_jog2.pressed.connect(self.auto.jog_backward)
            self.autoui.pb_jog2.released.connect(self.auto.jog_backward_stop)
            self.autoui.pb_absolute.clicked.connect(self.auto.absolute_run)
            self.autoui.pb_relative.clicked.connect(self.auto.relative_run)
            self.autoui.pb_home.clicked.connect(self.auto.axis_home)
            self.autoui.pb_reset.clicked.connect(self.auto.axis_reset)
            self.autoui.pb_axis_stop.clicked.connect(self.auto.axis_stop)
            self.autoui.cb_io.currentIndexChanged.connect(self.choose_io_module)
            self.autoui.cb_para.currentIndexChanged.connect(self.choose_para_module)

    def show_event(self, show):
        self.stop_rt = False
        self.auto.mannual_mode(True)

    def close_event(self, close):
        self.stop_rt = True
        self.auto.mannual_mode(False)

    def choose_io_module(self, index):
        try:
            self.read_io_config(index, False)
            self.initialize_motion_ui()
        except Exception as e:
            log.loginfo.process_log('choose_io_module:' + str(e))

    def choose_para_module(self, index):
        try:
            self.read_para_config(index, False)
            self.initialize_motion_ui()
        except Exception as e:
            log.loginfo.process_log('choose_para_module:' + str(e))

    # 读取IO表
    def read_io_config(self, class_index, init):
        try:
            # 读取IO配置表
            self.path = systempath.bundle_dir + '/CSV Files/IO.csv'
            csvfile = open(self.path, 'r')
            reader = csv.reader(csvfile)
            self.io_en = []
            self.io_name = []   # IO名字
            self.io_name_en = []  # 需要显示的名字
            self.io_on = []     # IO打开时的描述
            self.io_on_en = []
            self.io_off = []    # IO关闭时的描述
            self.io_off_en = []
            self.io_index = []  # IO通道
            self.io_index_en = []
            self.hold = []     # 是否为保持型按钮
            self.hold_en = []
            self.io_class = []  # IO模块类型

            self.io_max = 0
            self.io_min = 0
            i = 0
            for seq in reader:
                if(i!=0):
                    self.io_class.append(seq[6])
                i = i + 1
            csvfile.close()      # 关闭后才能再次读取
            # 删除相同的类型，确认IO模块个数，并按原有顺序排序
            self.io_class_list = list(set(self.io_class))
            self.io_class_list.sort(key=self.io_class.index)

            # 将类型添加到Combo中,注意只有第一次加载时初始化，不然会造成坑爹的死循环
            if(init):
                self.autoui.cb_io.clear()
                for io_class0 in self.io_class_list:
                    self.autoui.cb_io.addItem(io_class0)

            csvfile = open(self.path, 'r')
            reader = csv.reader(csvfile)
            i = 0
            for seq in reader:
                if(i!=0):
                    if(self.io_class[i-1]==self.io_class_list[class_index]):   # io_class不包括csv中的标题行
                        self.io_name.append(seq[0])
                        self.io_on.append(seq[2])
                        self.io_off.append(seq[3])
                        self.io_index.append(seq[1])
                        self.io_en.append(seq[4])
                        self.hold.append(seq[5])
                        # 需要显示的io
                        if (seq[4] == 'Yes'):
                            self.io_name_en.append(seq[0])
                            self.io_index_en.append(seq[1])
                            self.io_on_en.append(seq[2])
                            self.io_off_en.append(seq[3])
                            self.hold_en.append(seq[5])
                i = i + 1
            self.io_max = max(self.io_index)   # 最大通道
            self.io_len = len(self.io_index)   # 通道长度
        except Exception as e:
            log.loginfo.process_log('read_io_config:' + str(e))

    # 读取参数表
    def read_para_config(self, class_index, init):
        try:
            self.path = systempath.bundle_dir + '/CSV Files/' + 'Parameters.csv'
            csvfile = open(self.path, 'r')
            reader = csv.reader(csvfile)
            self.para_name = []     # 参数名称
            self.para_name_en = []  # 使能的参数名称
            self.para_index = []    # 寄存器序号
            self.para_index_en = [] #使能的寄存器序号
            self.para_en = []       # 使能信号
            self.para_class = []    # Para模块类型
            i = 0
            for seq in reader:
                if (i != 0):
                    self.para_class.append(seq[3])
                i = i + 1

            csvfile.close()  # 关闭后才能再次读取
            # 删除相同的类型，确认IO模块个数，并按原有顺序排序
            self.para_class_list = list(set(self.para_class))
            self.para_class_list.sort(key=self.para_class.index)

            # 将类型添加到Combo中,注意只有第一次加载时初始化，不然会造成坑爹的死循环
            if (init):
                self.autoui.cb_para.clear()
                for para_class0 in self.para_class_list:
                    self.autoui.cb_para.addItem(para_class0)
            csvfile = open(self.path, 'r')
            reader = csv.reader(csvfile)
            i = 0
            for seq in reader:
                if (i != 0):
                    if (self.para_class[i - 1] == self.para_class_list[class_index]):  # io_class不包括csv中的标题行
                        self.para_name.append(seq[0])
                        self.para_index.append(seq[1])
                        self.para_en.append(seq[2])
                        if (seq[2] == 'Yes'):
                            self.para_name_en.append(seq[0])
                            self.para_index_en.append(seq[1])
                i = i + 1

            self.para_max = max(self.para_index)  # 最大通道
            self.para_len = len(self.para_index)  # 最小通道
        except Exception as e:
            log.loginfo.process_log('read_para_config:' + str(e))

    # 初始化IO表，从配置文件中读取信息
    def initialize_motion_ui(self):
        self.read_axis_config()
        # 初始化参数表格
        self.autoui.tw_para.setRowCount(len(self.para_name_en))

        i = 0
        for seq in self.para_name_en:
            newItem = QTableWidgetItem(seq)
            newItem.setForeground(QBrush(QColor(0, 85, 255)))
            self.autoui.tw_para.setItem(i, 0, newItem)
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
            i = i + 1

        # 初始化io表格
        self.autoui.tw_io.setRowCount(len(self.io_name_en))
        # 连接io表格信号与槽函数
        self.mapper = QtCore.QSignalMapper(self)
        i = 0
        for seq in self.io_name_en:
            #if(i != 0):
            self.MyCheck = QPushButton()
            self.MyCheck.setText(seq)
            self.autoui.tw_io.setCellWidget(i, 0, self.MyCheck)
            #self.MyCheck.setStyleSheet("QPushButton { background-color: rgb(85, 170, 255) }")
            self.MyCheck.setStyleSheet("QPushButton { color: rgb(0, 85, 255) }")

            # newItem = QTableWidgetItem(self.io_desc[i])
            # self.tw_io.setItem(i - 1, 1, newItem)
            # 原始信号（表格中checkbox的鼠标点击信号）传递给map
            self.autoui.tw_io.cellWidget(i, 0).clicked.connect(self.mapper.map)
            # 设置map信号的转发规则, 转发为参数为int类型的信号
            self.mapper.setMapping(self.autoui.tw_io.cellWidget(i, 0), i)
            i = i+1

        # map信号连接到自定义的槽函数，参数类型为int
        self.mapper.mapped[int].connect(self.set_io)
        # 初始化轴信息
        j = 0
        self.autoui.cb_axis.clear()
        for seq in self.axis_name:
            if(j != 0):
                self.autoui.cb_axis.addItem(seq)
            j = j+1

    def read_axis_config(self):
        try:
            self.path = systempath.bundle_dir + '/CSV Files/' + 'Axis.csv'
            csvfile = open(self.path, 'r')
            reader = csv.reader(csvfile)
            self.axis_name = []
            self.axis_desc = []
            for seq in reader:
                self.axis_name.append(seq[0])
                self.axis_desc.append(seq[1])
        except Exception as e:
            log.loginfo.process_log('read_axis_config:'+str(e))

    def refresh_para(self, data):
        try:
            newItem = QTableWidgetItem(str(data[0]))
            self.autoui.tw_para.setItem(data[1], 1, newItem)
            newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        except Exception as e:
            log.loginfo.process_log('refresh_para:' + str(e))

    def refresh_io(self, data):
        try:
            self.autoui.tw_io.setItem(data[0], 1, data[1])
        except Exception as e:
            log.loginfo.process_log('refresh_io:' + str(e))

    def refresh_axis_ui(self, data):
        self.autoui.dsb_real_pos.setValue(float(data[0]))
        self.autoui.dsb_real_speed.setValue(float(data[1]))

    def initialize_motion_state(self):
        self.recv_thread = threading.Thread(target=self.refresh_rt_info)
        self.recv_thread.setDaemon(True)
        self.recv_thread.start()

    def refresh_rt_info(self):
        while(True):
            try:
                if(self.stop_rt):
                    break
                axis_para = self.auto.get_rt_info()
                self.refreshaxis.emit(axis_para)
                self.io_value = self.auto.read_io(self.io_index[0], len(self.io_index))
                self.io_value_en = []
                # 挑出读取到的IO中使能的点，并赋值到io_value_en
                for i in range(len(self.io_value)):
                    if (self.io_en[i] == 'Yes'):
                        self.io_value_en.append(self.io_value[i])
                self.para_value = self.auto.read_para(self.para_index[0], len(self.para_index))
                # 挑出读取到的参数中使能的值，并赋值到para_value_en
                self.para_value_en = []
                for i in range(len(self.para_value)):
                    if (self.para_en[i] == 'Yes'):
                        self.para_value_en.append(self.para_value[i])
                self.refresh_motion_para(self.io_value_en, self.para_value_en)
            except Exception as e:
                log.loginfo.process_log('refresh_rt_info:' + str(e))

    def set_io(self, index):
        try:
            if(len(self.io_value)==self.io_len):    # 没读到当前IO状态则不能写入
                state = self.io_value_en[index]
                if(state==0):
                    if(self.hold_en[index]=='Yes'):   # 保持型，直接赋值
                        self.io_value_en[index] = 1
                        ret = self.auto.write_io(self.io_index_en[index], [1])
                    else:   # 触发型按钮
                        self.io_value_en[index] = 1
                        ret = self.auto.write_io(self.io_index_en[index], [1])
                        time.sleep(0.1)
                        self.io_value_en[index] = 0
                        ret = self.auto.write_io(self.io_index_en[index], [0])
                else:
                    if (self.hold_en[index] == 'Yes'):  # 保持型，直接赋值
                        self.io_value_en[index] = 0
                        ret = self.auto.write_io(self.io_index_en[index], [0])
                    else:       # 触发型按钮
                        self.io_value_en[index] = 0
                        ret = self.auto.write_io(self.io_index_en[index], [0])
                        time.sleep(0.1)
                        self.io_value_en[index] = 1
                        ret = self.auto.write_io(self.io_index_en[index], [1])
                #self.autoui.tw_io.setItem(index, 1, newItem)
                # 需添加自定义写IO代码
            else:
                print('Read IO state fail!')
        except Exception as e:
            log.loginfo.process_log('set_io:' + str(e))

    def set_para(self, item):
        try:
            if (item.column() == 2):
                newItem = QTableWidgetItem(item.text())
                #self.autoui.tw_para.setItem(item.row(), 1, newItem)
                ret = self.auto.write_para(self.para_index_en[item.row()], [float(item.text())])
                # 需添加自定义写参数代码
        except Exception as e:
            log.loginfo.process_log('set_para:' + str(e))

    def read_init_state(self):
        # 从最小的寄存器开始读取，中间无间断
        try:
            self.io_value = self.auto.read_io(self.io_index[0], len(self.io_index))
            self.para_value = self.auto.read_para(self.para_index[0], len(self.para_index))
            self.refresh_motion_para(self.io_value, self.para_value)
        except Exception as e:
            log.loginfo.process_log('read_init_state:' + str(e))

    # 刷新运动控制参数（IO,Para）
    def refresh_motion_para(self, ls_io, ls_para):
        try:
            i = 0
            for io in ls_io:
                if (io == 1):
                    #self.autoui.tw_io.cellWidget(i, 0).setChecked(True)
                    newItem = QTableWidgetItem(self.io_on_en[i])
                    newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    # self.autoui.tw_io.setItem(i, 1, newItem)
                    self.refreshio.emit([i, newItem])
                elif(io == 0):
                    #self.autoui.tw_io.cellWidget(i, 0).setChecked(False)
                    newItem = QTableWidgetItem(self.io_off_en[i])
                    newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    # self.autoui.tw_io.setItem(i, 1, newItem)
                    self.refreshio.emit([i, newItem])
                else:
                    newItem = QTableWidgetItem(str(io))
                    newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    # self.autoui.tw_io.setItem(i, 1, newItem)
                    self.refreshio.emit([i, newItem])
                i = i + 1
            i = 0
            for para in ls_para:
                self.refreshpara.emit([para,i])
                # newItem1 = QTableWidgetItem(str(para))
                # self.autoui.tw_para.setItem(i, 2, newItem1)
                i = i + 1
        except Exception as e:
            log.loginfo.process_log('refresh_motion_para:' + str(e))