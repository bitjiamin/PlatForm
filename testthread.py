# -*- coding: UTF-8 -*-
"""
FileName: testthread.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 测试线程
Update date：2017.7.20
version 1.0.0
"""

import sys
import log
import time
from imp import reload
sys.path.append(log.curpath + '/Scripts')
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
try:
    import testscript
except Exception as e:
    print(e)
import copy


def reload_scripts():
    reload(testscript)

# 测试线程类
class TestThread(QtCore.QThread):
    # 声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(list)
    refresh = QtCore.pyqtSignal(list)
    refreshloop = QtCore.pyqtSignal(int)
    # 构造函数里增加形参
    def __init__(self, load,  threadnum, parent=None):
        super(TestThread, self).__init__(parent)
        # 储存参数
        self.load = load
        self.seq_end = True
        self.threadnum = threadnum
        self.ret = []
        self.result = []
        self.pause = False
        self.stop = False
        self.loop = False
        self.looptime = 0
        # self.loginfo = log.Log()
    def test_func(self):
        if(self.threadnum == 1):
            self.ts = testscript.TestFunc()
        else:
            self.ts = testscript.TestFunc2()
        self.seq_end = False
        total_time = 0
        total_result = 'Pass'
        total_data = []
        time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 所有行的序号
        i = 1
        # 主测试项的序号
        j = 0
        for seq in range(len(self.load.seq_col1)-1):
            self.result = []
            if(self.load.seq_col7[i] == 'root'):
                self.refresh.emit([j, '', '', "Testing", 1])
                st_int = time.time()
                st = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st_int))
                if self.load.seq_col3[i]!='skip':

                    k = getattr(self.ts, self.load.seq_col2[i])
                    self.ret = k()
                    log.loginfo.process_log('Test item: ' + self.load.seq_col2[i])
                    # 如果有子项，则需判断子项pass或fail
                    for m in range(len(self.ret)):
                        # 有子项时需索引子项的limit
                        if(len(self.ret) > 1):
                            index = i+m+1
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
                        if (self.ret[m] < uplimit)&(self.ret[m] > lowlimit):
                            self.result.append('Pass')   # 所有结果的列表
                            single_result = 'Pass'       #单个测试项的结果
                        else:
                            self.result.append('Fail')
                            single_result = 'Fail'
                            total_result = 'Fail'        #总的测试结果，有任何一项失败都会Fail
                else:
                    log.loginfo.process_log('Skip item: ' + self.load.seq_col2[i])
                    self.ret = [None]
                    single_result = 'skip'
                    self.result = ['Skip']
                # 有子项时，将子项测试数据添加到写入csv的data中
                if(len(self.ret) > 1):
                    total_data.append('nan')
                for n in range (len(self.ret)):
                    total_data.append(str(self.ret[n]))

                # 统计测试时间
                et_int = time.time()
                et = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(et_int))
                tt = round(et_int - st_int, 2)
                total_time = total_time + tt
                # 暂停测试
                while (self.pause):
                    time.sleep(0.02)
                    self.refresh.emit([j, tt, self.ret, 'Pause', self.threadnum])  #发送暂停测试信号，更新界面
                # 发送测试结果并更新界面
                self.refresh.emit([j, tt, self.ret, self.result, self.threadnum])
                # 按了停止后结束测试
                if(self.stop):
                    total_result = 'Break'
                    break
                # 判断失败后是否跳出测试
                if (self.load.seq_col6[i] == 'finish' and single_result == 'Fail'):
                    break

                j = j + 1
            i = i + 1
        # 更新测试时间和测试结果
        # 保存测试结果
        time2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        data_head = ['12345678', total_result, 'no error', time1, time2, str(total_time)]
        data_head.extend(total_data)
        self.load.write_csv(data_head, self.threadnum)
        log.loginfo.process_log('total time： ' + str("%.2f" %total_time))
        self.seq_end = True
        self.finishSignal.emit([total_time, total_result, self.threadnum])

    # 重写 run() 函数，在该线程中执行测试函数
    def run(self):
        if(self.loop and (self.looptime>0)):
            while(True):
                self.test_func()
                self.looptime = self.looptime - 1
                self.refreshloop.emit(self.looptime)
                if((self.loop == False) or (self.looptime <= 0) or self.stop):
                    break
                time.sleep(0.2)
        else:
            self.test_func()

