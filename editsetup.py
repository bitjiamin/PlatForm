# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import load
import systempath
import log
import inihelper
import testthread
from PyQt5 import QtGui


global editui
class EditUI(QDialog):
    # 实现一个单例类
    _instance = None
    __first_init = True
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent=None):
        if (self.__class__.__first_init):  # 只初始化一次
            self.__class__.__first_init = False  # 只初始化一次
            super(EditUI, self).__init__(parent)
            # self.setupUi(self)
            loadUi(systempath.bundle_dir + '/UI/editsequence.ui', self)  # 看到没，瞪大眼睛看

            # 设置窗口图标
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
            self.setWindowIcon(QtGui.QIcon(systempath.bundle_dir + '/Resource/edit.ico'))

            # 获取屏幕分辨率
            self.screen = QDesktopWidget().screenGeometry()
            self.width = self.screen.width()
            self.height = self.screen.height()
            self.init_seq()
            # 加载sequence
            self.edit_sequence()

            self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
            self.change_language(self.lan)

    def init_seq(self):
        self.cb_seq.clear()
        for i in range(load.threadnum):
            self.cb_seq.addItem('Sequence' + str(i+1))
        log.loginfo.process_log('Initialize sequence table')
        self.tableseq.setRowCount(200)
        self.tableseq.setColumnCount(7)
        self.tableseq.setHorizontalHeaderLabels(
            ['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])
        self.tableseq.setColumnWidth(0, self.width * 0.3)
        self.tableseq.setColumnWidth(1, self.width * 0.1)
        self.tableseq.horizontalHeader().setStretchLastSection(True)
        self.pb_saveseq.setMaximumWidth(self.width * 0.08)
        self.cb_seq.setMaximumWidth(self.width * 0.08)
        self.pb_delrow.setMaximumWidth(self.width * 0.08)
        self.pb_insertrow.setMaximumWidth(self.width * 0.08)

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

    def English_ui(self):
        # 序列编辑
        self.lb_edit.setText('Edit Test Sequence')
        self.pb_insertrow.setText('Insert Row')
        self.pb_delrow.setText('Delete Row')
        self.pb_saveseq.setText('Save')
        self.setWindowTitle('Sequence')
        self.tableseq.setHorizontalHeaderLabels(
            ['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])

    def Chinese_ui(self):
        # 序列编辑
        self.lb_edit.setText('序列编辑')
        self.pb_insertrow.setText('插入行')
        self.pb_delrow.setText('删除选定行')
        self.pb_saveseq.setText('保存序列')
        self.setWindowTitle('序列编辑')
        self.tableseq.setHorizontalHeaderLabels(['测试项', '函数', '模式', '下限', '上限', '失败后跳转', '等级'])

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()