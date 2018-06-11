from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import systempath
import csv
import log
import editsetup


class EditSlots():
    # 实现一个单例类
    _instance = None
    __first_init = True
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self):
        if (self.__class__.__first_init):  # 只初始化一次
            editsetup.editui = editsetup.EditUI()
            self.editui = editsetup.editui
            self.connect_signal()
            self.__class__.__first_init = False  # 只初始化一次

    def connect_signal(self):
        self.editui.cb_seq.currentIndexChanged.connect(self.editui.edit_sequence)
        self.editui.pb_saveseq.clicked.connect(self.save_sequence)
        self.editui.pb_delrow.clicked.connect(self.delete_row)
        self.editui.pb_insertrow.clicked.connect(self.insert_row)

    # 保存测试序列信息
    def save_sequence_1(self):
        filepath = systempath.bundle_dir + '/CSV Files/Seq' + str(self.cb_seq.currentIndex()+1) + '.csv'
        f = open(filepath, 'w',encoding='utf8',newline='')
        writer = csv.writer(f)
        writer.writerow(['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])
        try:
            for i in range(50):
                row = []
                if (self.tableseq.item(i, 0) != None):
                    for j in range(7):
                        if(j==2):
                            if(self.tableseq.cellWidget(i, j).currentIndex()==0):
                                row.append('test')
                            else:
                                row.append('skip')
                        elif(j==5):
                            if (self.tableseq.cellWidget(i, j).currentIndex() == 0):
                                row.append('continue')
                            else:
                                row.append('finish')
                        elif(j==6):
                            if (self.tableseq.cellWidget(i, j).currentIndex() == 0):
                                row.append('root')
                            else:
                                row.append('child')
                        else:
                            row.append(self.tableseq.item(i,j).text())
                    writer.writerow(row)
        except Exception as e:
            log.loginfo.process_log(str(e))
        f.close()
        #self.load_sequence()

    def save_sequence(self):
        filepath = systempath.bundle_dir + '/CSV Files/Seq' + str(self.editui.cb_seq.currentIndex()+1) + '.csv'
        f = open(filepath, 'w',encoding='utf8',newline='')
        writer = csv.writer(f)
        writer.writerow(['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])
        try:
            for i in range(200):
                row = []
                if (self.editui.tableseq.item(i, 0) != None):
                    for j in range(7):
                        if(j==100000):  #2
                            if(self.editui.tableseq.cellWidget(i, j).currentIndex()==0):
                                row.append('test')
                            else:
                                row.append('skip')
                        elif(j==100000):  #5
                            if (self.editui.tableseq.cellWidget(i, j).currentIndex() == 0):
                                row.append('continue')
                            else:
                                row.append('finish')
                        elif(j==100000):  #6
                            if (self.editui.tableseq.cellWidget(i, j).currentIndex() == 0):
                                row.append('root')
                            else:
                                row.append('child')
                        else:
                            row.append(self.editui.tableseq.item(i,j).text())
                    writer.writerow(row)
        except Exception as e:
            log.loginfo.process_log(str(e))
        f.close()
        #self.load_sequence()

    # 删除当前行
    def delete_row(self):
        self.editui.tableseq.removeRow(self.editui.tableseq.currentRow())

    def insert_row(self):
        try:
            row_cnt = self.editui.tableseq.currentRow()
            self.editui.tableseq.insertRow(row_cnt)
            for j in range(7):
                    if(j==2):
                        newItem1 = QTableWidgetItem('test')
                        self.editui.tableseq.setItem(row_cnt, j, newItem1)
                    elif(j==3 or j==4):
                        newItem1 = QTableWidgetItem('nan')
                        self.editui.tableseq.setItem(row_cnt, j, newItem1)
                    elif (j == 5):
                        newItem1 = QTableWidgetItem('continue')
                        self.editui.tableseq.setItem(row_cnt, j, newItem1)
                    elif (j == 6):
                        newItem1 = QTableWidgetItem('root')
                        self.editui.tableseq.setItem(row_cnt, j, newItem1)
                    else:
                        newItem1 = QTableWidgetItem('')
                        self.editui.tableseq.setItem(row_cnt, j, newItem1)
        except Exception as e:
            print(e)