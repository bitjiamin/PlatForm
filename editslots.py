from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from editsetup import *
import load
import systempath
import csv
import log
import testthread

class EditSlots(EditUI):
    def __init__(self, parent=None):
        super(EditSlots, self).__init__(parent)
        self.connect_signal()

    def connect_signal(self):
        self.cb_seq.currentIndexChanged.connect(self.edit_sequence)
        self.pb_saveseq.clicked.connect(self.save_sequence)
        self.pb_delrow.clicked.connect(self.delete_row)
        self.pb_insertrow.clicked.connect(self.insert_row)

    # 切换到序列编辑页面，并且将Seq1的信息读取到表格
    def edit_sequence(self):
        #self.tableseq.clear()
        ld = testthread.t_load[self.cb_seq.currentIndex()]
        ld.load_seq()
        items = [ld.seq_col1, ld.seq_col2, ld.seq_col3, ld.seq_col4, ld.seq_col5, ld.seq_col6, ld.seq_col7]
        for j in range(7):
            i = 0
            for seq in items[j][1:len(items[j])]:
                if(j==10000):  #2
                    self.MyCombo = QComboBox()
                    self.MyCombo.addItem("test")
                    self.MyCombo.addItem("skip")
                    self.tableseq.setCellWidget(i, j, self.MyCombo)
                    if(seq == 'test'):
                        self.MyCombo.setCurrentIndex(0)
                    else:
                        self.MyCombo.setCurrentIndex(1)
                elif(j==10000):   #5
                    self.MyCombo1 = QComboBox()
                    self.MyCombo1.addItem("continue")
                    self.MyCombo1.addItem("finish")
                    self.tableseq.setCellWidget(i, j, self.MyCombo1)
                    if (seq == 'continue'):
                        self.MyCombo1.setCurrentIndex(0)
                    else:
                        self.MyCombo1.setCurrentIndex(1)
                elif (j == 10000):  #6
                    self.MyCombo2 = QComboBox()
                    self.MyCombo2.addItem("root")
                    self.MyCombo2.addItem("child")
                    self.tableseq.setCellWidget(i, j, self.MyCombo2)
                    if (seq == 'root'):
                        self.MyCombo2.setCurrentIndex(0)
                    else:
                        self.MyCombo2.setCurrentIndex(1)
                else:
                    newItem1 = QTableWidgetItem(seq)
                    self.tableseq.setItem(i, j, newItem1)
                i = i + 1

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
        filepath = systempath.bundle_dir + '/CSV Files/Seq' + str(self.cb_seq.currentIndex()+1) + '.csv'
        f = open(filepath, 'w',encoding='utf8',newline='')
        writer = csv.writer(f)
        writer.writerow(['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])
        try:
            for i in range(200):
                row = []
                if (self.tableseq.item(i, 0) != None):
                    for j in range(7):
                        if(j==100000):  #2
                            if(self.tableseq.cellWidget(i, j).currentIndex()==0):
                                row.append('test')
                            else:
                                row.append('skip')
                        elif(j==100000):  #5
                            if (self.tableseq.cellWidget(i, j).currentIndex() == 0):
                                row.append('continue')
                            else:
                                row.append('finish')
                        elif(j==100000):  #6
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

    # 删除当前行
    def delete_row(self):
        self.tableseq.removeRow(self.tableseq.currentRow())

    def insert_row(self):
        row_cnt = self.tableseq.currentRow()
        self.tableseq.insertRow(row_cnt)
        for j in range(7):
                if(j==2):
                    self.MyCombo = QComboBox()
                    self.MyCombo.addItem("test")
                    self.MyCombo.addItem("skip")
                    self.tableseq.setCellWidget(row_cnt, j, self.MyCombo)
                elif(j==5):
                    self.MyCombo1 = QComboBox()
                    self.MyCombo1.addItem("continue")
                    self.MyCombo1.addItem("finish")
                    self.tableseq.setCellWidget(row_cnt, j, self.MyCombo1)
                elif (j == 6):
                    self.MyCombo2 = QComboBox()
                    self.MyCombo2.addItem("root")
                    self.MyCombo2.addItem("child")
                    self.tableseq.setCellWidget(row_cnt, j, self.MyCombo2)
                else:
                    newItem1 = QTableWidgetItem('')
                    self.tableseq.setItem(row_cnt, j, newItem1)