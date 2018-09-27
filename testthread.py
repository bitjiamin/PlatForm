# -*- coding: UTF-8 -*-
"""
FileName: testthread.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 测试线程
Update date：2018.9.6
version 1.0.0
"""

import sys
import systempath
import inihelper
import log
import time
import load
from imp import reload
sys.path.append(systempath.bundle_dir + '/Scripts')
sys.path.append(systempath.bundle_dir + '/UI')
sys.path.append(systempath.bundle_dir + '/Module')
from PyQt5 import QtCore, QtGui, QtWidgets
import imp
import globaldata
import os


global testscript
testscript = []
try:
    for i in range(load.threadnum):
        f = systempath.bundle_dir + '/Scripts/testscript' + str(i+1) + '.py'
        mod = imp.load_compiled('testscript' + str(i+1), systempath.bundle_dir + '/Scripts/testscript'+ str(i+1)+'.pyc')
        if(os.path.isfile(f)):
            mod = imp.load_source('testscript' + str(i+1), f)
        testscript.append(mod)
except Exception as e:
    log.loginfo.process_log(str(e))

# 测试线程类
class TestThread(QtCore.QThread):
    # 声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(list)
    refresh = QtCore.pyqtSignal(list)
    refreshloop = QtCore.pyqtSignal(int)
    # 构造函数里增加形参
    def __init__(self, load,  threadid, parent=None):
        super(TestThread, self).__init__(parent)
        # 储存参数
        self.load = load
        self.seq_end = True
        self.step_end = True
        self.threadid = threadid
        self.ret = []
        self.result = []
        self.pause = False
        self.stop = False
        self.loop = False
        self.mode = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Mode')
        self.ts = testscript[self.threadid].TestFunc()

    def get_step(self, ls):
        print(ls)
        ret = ''
        if (ls[1][0:5] == 'Start'):
            ret = ls[1][5:]
        self.func = ret

    def reload_scripts(self):
        try:
            reload(testscript[self.threadid])
            self.ts = testscript[self.threadid].TestFunc()
            log.loginfo.process_log('reload testscript' + str(self.threadid + 1) + ' ok')
        except Exception as e:
            log.loginfo.process_log(str(e))

    def test_func(self):
        self.step_end = False
        # 获取需要开始的step函数名
        funcs = sorted(set(self.load.seq_col2), key=self.load.seq_col2.index)
        if(self.mode == 'Seq'):
            self.func = 'prerun'
            self.seq_len = len(self.load.seq_col1)-1
        else:
            self.seq_len = 1

        if(self.func == 'prerun'):
            self.seq_end = False
            self.total_time = 0
            self.total_result = 'Pass'
            self.total_data = []
            self.time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.time1_int = time.time()

        # 所有行的序号
        i = self.load.seq_col2.index(self.func)
        root_i = funcs.index(self.func)
        # 主测试项的序号
        j = root_i-1
        try:
            for seq in range(self.seq_len):
                self.result = []
                if(self.load.seq_col7[i] == 'root'):
                    self.refresh.emit([j, '', '', "Testing", 1, self.threadid])
                    st_int = time.time()
                    st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st_int))
                    if self.load.seq_col3[i]!='skip':
                        k = getattr(self.ts, self.load.seq_col2[i])
                        self.ret = k()
                        log.loginfo.process_log('Thread' + str(self.threadid+1) + ':'+'Test item: ' + self.load.seq_col2[i])
                        # 每个测试项测试结果个数
                        l_result = int(len(self.ret))-1
                        # 如果有子项，则需判断子项pass或fail
                        for m in range(l_result):
                            # 有子项时需索引子项的limit
                            if(l_result > 1):
                                index = i+m
                            # 无子项时直接索引当前行的limit
                            else:
                                index = i+m
                            # limit为nan时，表示无穷大
                            if(self.load.seq_col5[index] == 'nan'):
                                uplimit = float('Inf')
                            else:
                                uplimit = float(self.load.seq_col5[index])
                            if (self.load.seq_col4[index] == 'nan'):
                                lowlimit = float('-Inf')
                            else:
                                lowlimit = float(self.load.seq_col4[index])
                            if (self.ret[m] <= uplimit)&(self.ret[m] >= lowlimit):
                                self.result.append('Pass')   # 所有结果的列表
                                single_result = 'Pass'       # 单个测试项的结果
                            else:
                                self.result.append('Fail')
                                single_result = 'Fail'
                                self.total_result = 'Fail'        # 总的测试结果，有任何一项失败都会Fail
                    else:
                        log.loginfo.process_log('Thread' + str(self.threadid+1) + ':'+'Skip item: ' + self.load.seq_col2[i])
                        # skip时测试结果与结果详细描述都是None
                        self.ret = ['Skip','Skip']
                        l_result = 1
                        single_result = 'skip'
                        self.result = ['Skip']
                    # 有子项时，将子项测试数据添加到写入csv的data中
                    if(l_result > 1):
                        #total_data.append('0')
                        pass
                    for n in range (l_result):
                        self.total_data.append(str(self.ret[n]))
                    # 统计测试时间
                    et_int = time.time()
                    et = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(et_int))
                    tt = round(et_int - st_int, 2)
                    self.total_time = self.total_time + tt
                    # 暂停测试
                    while (self.pause):
                        time.sleep(0.02)
                        self.refresh.emit([j, tt, self.ret[0:len(self.ret)-1], 'Pause', self.ret[len(self.ret)-1:], self.threadid])  #发送暂停测试信号，更新界面
                    # 发送测试结果并更新界面,测试脚本返回的结果中前半部分为结果，后半部分为详细描述
                    self.refresh.emit([j, tt, self.ret[0:len(self.ret)-1], self.result,  self.ret[len(self.ret)-1:], self.threadid])
                    log.loginfo.process_log('Thread' + str(self.threadid+1) + ':'+self.load.seq_col2[i] + ' result:' + str(self.ret))
                    # 按了停止后结束测试
                    if(self.stop):
                        self.total_result = 'Break'
                        break
                    # 判断失败后是否跳出测试
                    if (self.load.seq_col6[i] == 'finish' and single_result == 'Fail'):
                        break
                    j = j + 1
                i = i + 1
        except Exception as e:
            print(e)
        if(self.mode == 'Seq'):
            self.func = 'postrun'
        # 更新测试时间和测试结果，保存测试结果
        if(self.func == 'postrun'):
            time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.time2_int = time.time()
            self.total_time = round(self.time2_int - self.time1_int, 2)
            data_head = [globaldata.sn, self.total_result, 'no error', self.time1, time2, str(self.total_time)]
            data_head.extend(self.total_data)
            self.load.write_csv(data_head, self.threadid)
            log.loginfo.process_log('Thread' + str(self.threadid+1) + ':'+'total time： ' + str("%.2f" %self.total_time))
            self.seq_end = True
            self.finishSignal.emit([self.total_time, self.total_result, self.threadid])

        self.step_end = True

    # 重写 run() 函数，在该线程中执行测试函数
    def run(self):
        if(self.loop):
            while(True):
                self.test_func()
                # self.looptime = self.looptime - 1
                self.refreshloop.emit(0)
                if((self.loop == False) or self.stop):
                    break
                time.sleep(0.5)
        else:
            self.test_func()

global t_thread, t_load, sload
t_thread = []
t_load = []
for i in range(load.threadnum):
    s_load = load.Load('Sequence'+str(i+1)+'.csv')
    s_load.load_seq()
    t_load.append(s_load)
    # log.loginfo.process_log('Load sequence')

def init_thread():
    for i in range(load.threadnum):
        global sload, t_thread
        s_thread = TestThread(s_load, i)
        t_thread.append(s_thread)