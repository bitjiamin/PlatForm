from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import systempath
import csv
import log
import editsetup


class EditSlots():
    # 实现一个单例类
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self):
        editsetup.editui = editsetup.EditUI()
        self.editui = editsetup.editui
        self.connect_signal()

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
        self.editui.tableseq.removeRow(self.tableseq.currentRow())

    def insert_row(self):
        row_cnt = self.tableseq.currentRow()
        self.editui.tableseq.insertRow(row_cnt)
        for j in range(7):
                if(j==2):
                    self.MyCombo = QComboBox()
                    self.MyCombo.addItem("test")
                    self.MyCombo.addItem("skip")
                    self.editui.tableseq.setCellWidget(row_cnt, j, self.MyCombo)
                elif(j==5):
                    self.MyCombo1 = QComboBox()
                    self.MyCombo1.addItem("continue")
                    self.MyCombo1.addItem("finish")
                    self.editui.tableseq.setCellWidget(row_cnt, j, self.MyCombo1)
                elif (j == 6):
                    self.MyCombo2 = QComboBox()
                    self.MyCombo2.addItem("root")
                    self.MyCombo2.addItem("child")
                    self.editui.tableseq.setCellWidget(row_cnt, j, self.MyCombo2)
                else:
                    newItem1 = QTableWidgetItem('')
                    self.editui.tableseq.setItem(row_cnt, j, newItem1)