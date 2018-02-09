# -*- coding: UTF-8 -*-
"""
FileName: load.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 加载CSV，初始化logger，写log
Update date：2017.7.20
version 1.0.0
"""

import time
import csv
import os
import inihelper
import systempath

threadnum = int(inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Thread'))
class Load():
    def __init__(self, path, parent=None):
        global loginfo
        self.path = systempath.bundle_dir + '/CSV Files/' + path
        self.seq_col1 = []
        self.seq_col2 = []
        self.seq_col3 = []
        self.seq_col4 = []
        self.seq_col5 = []
        self.seq_col6 = []
        self.seq_col7 = []
        self.testitems = []
    def load_seq(self):
        self.seq_col1 = []
        self.seq_col2 = []
        self.seq_col3 = []
        self.seq_col4 = []
        self.seq_col5 = []
        self.seq_col6 = []
        self.seq_col7 = []
        self.testitems = []
        # 除第一次加载外，其他时候的加载都会弹出文件选择对话框
        global stationnum
        Load.firstload = False
        csvfile = open(self.path, 'r')
        reader = csv.reader(csvfile)
        for seq in reader:
            self.seq_col1.append(seq[0])
            self.seq_col2.append(seq[1])
            self.seq_col3.append(seq[2])
            self.seq_col4.append(seq[3])
            self.seq_col5.append(seq[4])
            self.seq_col6.append(seq[5])
            self.seq_col7.append(seq[6])

    def load_seq_from_file(self):
        # 除第一次加载外，其他时候的加载都会弹出文件选择对话框
        dir_path = QFileDialog.getOpenFileName(None, "choose directory", "", "Csv files(*.csv)")
        if(dir_path[0] != ''):
            csvfile = open(dir_path[0], 'r')
            reader = csv.reader(csvfile)
            self.seq_col1 = []
            self.seq_col2 = []
            self.seq_col3 = []
            self.seq_col4 = []
            self.seq_col5 = []
            self.seq_col6 = []
            self.seq_col7 = []
        for seq in reader:
            self.seq_col1.append(seq[0])
            self.seq_col2.append(seq[1])
            self.seq_col3.append(seq[2])
            self.seq_col4.append(seq[3])
            self.seq_col5.append(seq[4])
            self.seq_col6.append(seq[5])
            self.seq_col7.append(seq[6])

    def write_csv(self, data, seqnum):
        st = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        filepath = systempath.bundle_dir + '/Result/' + st + '_sequence' + str(seqnum+1) + '.csv'
        if (not os.path.exists(filepath)):
            f = open(filepath, 'a+', newline='')
            writer = csv.writer(f)
            datalog1 = ['SN', 'Pass/Fail', 'errStr', 'StartTime', 'EndTime', 'TestTime']
            datalog1.extend(self.seq_col1[1:len(self.seq_col1)])
            datalog2 = ['Function', '', '', '', '', '']
            datalog2.extend(self.seq_col2[1:len(self.seq_col2)])
            datalog3 = ['Mode', '', '', '', '', '']
            datalog3.extend(self.seq_col3[1:len(self.seq_col3)])
            datalog4 = ['Lower Limit', '', '', '', '', '']
            datalog4.extend(self.seq_col4[1:len(self.seq_col4)])
            datalog5 = ['Upper Limit', '', '', '', '', '']
            datalog5.extend(self.seq_col5[1:len(self.seq_col5)])
            writer.writerow(datalog1)
            writer.writerow(datalog2)
            writer.writerow(datalog3)
            writer.writerow(datalog4)
            writer.writerow(datalog5)
            f.close()
        f = open(filepath, 'a+',newline='')
        writer = csv.writer(f)
        writer.writerow(data)