# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from editsequence import *
import load
import systempath
import log
import inihelper

class EditUI(Ui_editsequence, QDialog):
    def __init__(self, parent=None):
        super(EditUI, self).__init__(parent)
        self.setupUi(self)
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
        self.tableseq.setRowCount(50)
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

    def English_ui(self):
        # 序列编辑
        self.lb_edit.setText('Edit Test Sequence')
        self.pb_insertrow.setText('Insert Row')
        self.pb_delrow.setText('Delete Row')
        self.pb_saveseq.setText('Save')
        self.tableseq.setHorizontalHeaderLabels(
            ['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])

    def Chinese_ui(self):
        # 序列编辑
        self.lb_edit.setText('序列编辑')
        self.pb_insertrow.setText('插入行')
        self.pb_delrow.setText('删除选定行')
        self.pb_saveseq.setText('保存序列')
        self.tableseq.setHorizontalHeaderLabels(['测试项', '函数', '模式', '下限', '上限', '失败后跳转', '等级'])

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()