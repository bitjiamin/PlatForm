# -*- coding: UTF-8 -*-
"""
FileName: main.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 主程序
Update date：2017.7.20
version 1.0.0
"""
import compilepy
import sys
import systempath
import os
import platform
import multiprocessing
from PyQt5.QtGui import QPalette, QColor, QBrush
from PyQt5.QtCore import QCoreApplication
sys.path.append(systempath.bundle_dir + '\\Module')
sys.path.append(systempath.bundle_dir + '\\Scripts')
sys.path.append(systempath.bundle_dir + '\\Vision')
sys.path.append(systempath.bundle_dir + '\\UI')
sys.path.append(systempath.bundle_dir + '\\Refrence')
import log
from login import *
log.loginfo = log.Log()
from tcptool import *
import zmqtool
import serialtool
from usermanage import *
import zmqserver
from mainattach import *
from autoattach import *
import editslots
import autoslots
from scansnsetup import *
import mainsetup
import testthread
import load
import globaldata


class TestSeq(QMainWindow):
    def __init__(self, parent=None):
        super(TestSeq, self).__init__(parent)
        globaldata.GlobalSingnal()
        globaldata.init_singnal()
        # 实例化tcp，串口，zmq调试工具类
        self.mainui = mainsetup.MainUI()
        # 实例化log类
        log.loginfo.refreshlog.connect(self.refresh_log)
        # 初始化用户名
        self.mainui.lb_main_user.setText(UserManager.username)

        self.refresh_user([UserManager.username])
        log.loginfo.process_log(UserManager.username + ' login')
        testthread.init_thread()
        log.loginfo.process_log('Initialize test thread')
        self.mains = MainAttach()
        self.tcptool = TcpTool()
        self.serialtool = serialtool.SerialTool()
        self.zmqtool = zmqtool.ZmqTool()
        self.usertool = UserManage()
        # 获取屏幕分辨率
        self.screen = QDesktopWidget().screenGeometry()
        self.width = self.screen.width()
        self.height = self.screen.height()
        self.snwd = SNUI()
        # 菜单项槽函数连接
        self.mainui.actionReload_CSV.triggered.connect(self.load_sequence)
        self.mainui.nextAction.triggered.connect(self.next_step)
        self.mainui.actionReload_Scripts.triggered.connect(self.reload_scripts)
        self.mainui.actionLogin.triggered.connect(self.change_user)
        self.mainui.actionUser_Manage.triggered.connect(self.user_management)
        self.mainui.actionMain_Window.triggered.connect(self.switch_to_mainwindow)
        self.mainui.actionEdit_Window.triggered.connect(self.seq_debug_tool)
        self.mainui.actionMotion_Window.triggered.connect(self.motion_debug)
        self.mainui.actionZmq_Debug.triggered.connect(self.zmq_debug_tool)
        self.mainui.actionTcp_Debug.triggered.connect(self.tcp_debug_tool)
        self.mainui.actionSerial_Debug.triggered.connect(self.serial_debug_tool)
        self.mainui.actionToolBar.triggered.connect(self.view_toolbar)
        self.mainui.actionOpen_CSV.triggered.connect(self.open_sequence_thread)
        self.mainui.actionOpen_Result.triggered.connect(self.open_result_thread)
        self.mainui.actionOpen_Log.triggered.connect(self.open_log_thread)
        self.mainui.actionClose_System.triggered.connect(QCoreApplication.instance().quit)
        self.mainui.actionSN_Window.triggered.connect(self.sn_window)
        # 默认隐藏toolbar
        self.mainui.actionToolBar.setChecked(False)
        self.view_toolbar()
        # 工具栏信号连接
        self.mainui.actionStart.triggered.connect(self.test_start)
        self.mainui.actionStop.triggered.connect(self.test_break)
        self.mainui.actionPause.triggered.connect(self.test_pause)
        self.mainui.actionContinue.triggered.connect(self.continue_tool)
        self.mainui.actionLoginTool.triggered.connect(self.change_user)
        self.mainui.actionAutomation.triggered.connect(self.motion_debug)
        self.mainui.actionEdit.triggered.connect(self.seq_debug_tool)
        self.mainui.actionMainwindow.triggered.connect(self.switch_to_mainwindow)
        self.mainui.actionRefresh.triggered.connect(self.reload_scripts)
        self.mainui.myloopbar.clicked.connect(self.enable_loop)
        # self.myeditbar.textEdited.connect(self.edit_looptime)
        self.mainui.mystepbar.clicked.connect(self.step_test)
        self.mainui.actionLog.triggered.connect(self.test_log)
        self.switch_to_mainwindow()
        # 右键菜单信号连接
        self.mainui.actstarttest.triggered.connect(self.test_start)
        self.mainui.actstoptest.triggered.connect(self.test_break)
        # 两个树形控件的root items
        self.root = []
        self.mode = []
        for i in range(load.threadnum):
            self.root.append([])
        # 连接子进程的信号和槽函数
        for i in range(load.threadnum):
            globaldata.singnal.runsingnal[i].connect(testthread.t_thread[i].get_step)
            globaldata.singnal.runsingnal[i].connect(self.remote_test)
            testthread.t_thread[i].finishSignal.connect(self.test_end)
            testthread.t_thread[i].refresh.connect(self.refresh_ui)
            testthread.t_thread[i].refreshloop.connect(self.loop_refresh)
            self.mode.append(testthread.t_load[i].seq_col3)
        # 加载sequence
        # testthread.t_load[0].load_seq()
        # log.loginfo.process_log('Load sequence')
        self.initialize_sequence()
        # 开启zmq server
        self.zmq = zmqserver.ZmqComm()
        self.zmq.zmqrecvsingnal.connect(self.recv_server)
        self.zmq.start()
        # 实例化登陆类
        user.loginsignal.connect(self.refresh_user)
        # 连接zmq发送接收信号，显示信息到调试工具界面
        self.zmq.zmqrecvsingnal.connect(self.zmqtool.display_recv_msg)
        self.zmq.zmqsendsingnal.connect(self.zmqtool.display_send_msg)

    def sn_window(self):
        self.snwd.show()

        # 初始化测试序列
    def initialize_sequence(self):
        try:
            for i in range(load.threadnum):
                log.loginfo.process_log('ThreadID'+str(i+1)+':'+'Initialize sequence tree')
                self.root[i] = self.initialize_tree(self.mainui.testtree[i], testthread.t_load[i].seq_col1, testthread.t_load[i].seq_col7)
                self.mainui.bar[i].setRange(0, len(self.root[i]) - 1)
        except Exception as e:
            log.loginfo.process_log('main:initialize_sequence:' + str(e))

    # 初始化显示测试信息的树形结构
    def initialize_tree(self, tree, items, levels):
        try:
            tree.setColumnCount(5)
            # tree.setColumnWidth(0,int(tree.width()*0.4))
            # tree.setHeaderLabels(['TestItems', 'Test Time', 'TestData', 'TestResult', ' Details'])
            # 设置行高为25
            tree.setStyleSheet("QTreeWidget::item{height:%dpx}"%int(self.height*0.03))
            header = tree.header()
            header.setStretchLastSection(True)
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

            j = 0
            root = []
            for seq in items[1:len(items)]:
                if(levels[j+1] == 'root'):
                    root0 = QTreeWidgetItem(tree)
                    root0.setTextAlignment(1, Qt.AlignCenter)
                    root0.setTextAlignment(2, Qt.AlignCenter)
                    root0.setTextAlignment(3, Qt.AlignCenter)
                    root0.setTextAlignment(4, Qt.AlignCenter)
                    root.append(root0)
                # 设置根节点的名称
                    root0.setText(0, seq)
                else:
                    child = QTreeWidgetItem(root0)
                    child.setTextAlignment(1, Qt.AlignCenter)
                    child.setTextAlignment(2, Qt.AlignCenter)
                    child.setTextAlignment(3, Qt.AlignCenter)
                    child.setTextAlignment(4, Qt.AlignCenter)
                    child.setText(0, seq)
                j = j + 1
        except Exception as e:
            log.loginfo.process_log('main:initialize_tree:' + str(e))
        return root

    # 循环测试时刷新UI
    def loop_refresh(self, times):
        for i in range(load.threadnum):
            if (testthread.t_thread[i].seq_end):
                if(testthread.t_thread[i].loop == True):                     # 确保最后一次只更新循环次数
                    self.clear_seq(self.root[i], self.mainui.bar[i])
                    self.set_state('Testing',i)
                    self.mainui.pe.setColor(QPalette.Window, QColor(255, 255, 0))  # 设置背景颜色
                    #self.myeditbar.setText(str(testthread.t_thread[0].looptime))

    def thread_start(self, threadid):
        try:
            log.loginfo.process_log('Start test')
            testthread.t_load[threadid].seq_col3 = self.mode[threadid]
            testthread.t_thread[threadid].stop = False
            self.mainui.actionStart.setDisabled(True)
            # self.mainui.myloopbar.setDisabled(True)
            # self.mainui.myeditbar.setDisabled(True)
            # 开始执行 run() 函数里的内容,只有测试结束了的线程才能开始(改成单步运行后序列结束前可以重复start)
            if(testthread.t_thread[threadid].seq_end):
                self.clear_seq(self.root[threadid],self.mainui.bar[threadid])
            if(testthread.t_thread[threadid].step_end):
                testthread.t_thread[threadid].start()
                self.set_state('Testing', threadid)
                self.mainui.pe.setColor(QPalette.Window, QColor(255, 255, 0))  # 设置背景颜色
        except Exception as e:
            log.loginfo.process_log('main:test_start:' + str(e))

    # 开始测试
    def test_start(self):
        try:
            log.loginfo.process_log('Start test')
            for i in range(load.threadnum):
                self.thread_start(i)
        except Exception as e:
            log.loginfo.process_log('main:test_start:' + str(e))

    # 测试结束后刷新UI等
    def test_end(self, ls):
        # 使用传回的返回值
        #self.le_time.setText(str(round(ls[0], 2)) + 's')
        if(self.mainui.myloopbar.isChecked()==True):
            self.mainui.actionStart.setDisabled(True)
            # self.mainui.myloopbar.setDisabled(True)
            # self.mainui.myeditbar.setDisabled(True)
        else:
            self.mainui.actionStart.setDisabled(False)
            # self.mainui.myloopbar.setDisabled(False)
            # self.mainui.myeditbar.setDisabled(False)
        self.set_state(ls[1], ls[2])
        self.set_count(ls)
        if ls[1] == 'Pass':
            #self.le_pass.setText(str(int(self.le_pass.text()) + 1))
            self.mainui.pe.setColor(QPalette.Window, QColor(0, 255, 0))  # 设置背景颜色
        else:
            self.mainui.pe.setColor(QPalette.Window, QColor(255, 0, 0))  # 设置背景颜色

    # 中止测试
    def test_break(self):
        log.loginfo.process_log('Break test')
        for i in range(load.threadnum):
            testthread.t_thread[i].stop = True
            self.set_state('Break', i)

    # 暂停测试
    def test_pause(self):
        log.loginfo.process_log('Pause test')
        for i in range(load.threadnum):
            testthread.t_thread[i].pause = True
        self.mainui.actionPause.setDisabled(True)
        self.mainui.actionContinue.setDisabled(False)

    # 开启或关闭单步测试
    def step_test(self):
        if(self.mainui.mystepbar.isChecked()):
            for i in range(load.threadnum):
                testthread.t_thread[i].pause = True
            self.mainui.nextAction.setDisabled(False)
            log.loginfo.process_log('Enable step test')
        else:
            for i in range(load.threadnum):
                testthread.t_thread[i].pause = False
            self.mainui.nextAction.setDisabled(True)
            log.loginfo.process_log('Disable step test')

    # 暂停后继续测试
    def continue_tool(self):
        for i in range(load.threadnum):
            testthread.t_thread[i].pause = False
        self.mainui.actionPause.setDisabled(False)
        self.mainui.actionContinue.setDisabled(True)
        log.loginfo.process_log('continue test')

    # 开启或关闭循环测试
    def enable_loop(self):
        try:
            if(self.mainui.myloopbar.isChecked()):
                for i in range(load.threadnum):
                    testthread.t_thread[i].loop = True
                    # testthread.t_thread[i].looptime = int(self.myeditbar.text())
                log.loginfo.process_log('Enable loop test')
            else:
                for i in range(load.threadnum):
                    testthread.t_thread[i].loop = False
                log.loginfo.process_log('Disable loop test')
        except Exception as e:
            log.loginfo.process_log('main:enable_loop:' + str(e))

    # 修改循环测试次数
    def edit_looptime(self):
        try:
            for i in range(load.threadnum):
                testthread.t_thread[i].looptime = int(self.myeditbar.text())
        except Exception as e:
            log.loginfo.process_log(str(e))

    def refresh_log(self, msg):
        self.mainui.te_log.setStyleSheet("color:blue")
        self.mainui.te_log.append(msg)

    # 测试过程中刷新UI，线程1
    def refresh_ui(self,ls):
        try:
            thread_id = ls[5]
            # 每个测试项测试结果个数
            l_result = len(ls[2]) - 1
            # 有子项时显示子项
            if(l_result > 0):
                for i in range(l_result):
                    self.root[thread_id][ls[0]].child(i).setText(2, str(ls[2][i+1]))
                    self.root[thread_id][ls[0]].child(i).setText(3, ls[3][i+1])

            # 将结果列表的括号去掉后再显示
            ls[4] = str(ls[4])[1:len(str(ls[4])) - 1]
            # 显示其他信息
            for i in range(1, 5):
                if (i == 0 or i == 1 or i == 4 or i == 5):
                    # 将结果列表的括号去掉后再显示
                    self.root[thread_id][ls[0]].setText(i, str(ls[i]))
                if (i == 2):
                    if(l_result>1):
                        self.root[thread_id][ls[0]].setText(i, str(ls[i][0]))
                    else:
                        try:
                            self.root[thread_id][ls[0]].setText(i, str(ls[i][0]))
                        except Exception as e:
                            pass
                if(i == 3):
                    if('Fail' in ls[i]):
                        self.root[thread_id][ls[0]].setText(i, 'Fail')
                    elif(ls[i][0]== 'Skip'):
                        self.root[thread_id][ls[0]].setText(i, 'Skip')
                    elif('Testing' in ls[i]):
                        self.root[thread_id][ls[0]].setText(i, 'Testing')
                    else:
                        self.root[thread_id][ls[0]].setText(i, 'Pass')

            if ls[3] == "Testing":
                for i in range(0,5):
                    self.root[thread_id][ls[0]].setBackground(i, QBrush(QColor(0,255,100)))    # 设置树形控件的item为绿色
                    self.mainui.testtree[thread_id].scrollToItem(self.root[thread_id][ls[0]])  # 2018.5.5更新，树形控件自动滚动到当前测试的行
            elif "Fail" in ls[3]:
                self.mainui.bar[thread_id].setValue(ls[0])
                for i in range(0, 5):
                    self.root[thread_id][ls[0]].setBackground(i, QBrush(QColor(255, 0, 0)))

                if(len(ls[3]) > 1):      # 将fail的子项标红
                    for j in range(len(ls[3])-1):
                        if(ls[3][j+1] == 'Fail'):
                            for i in range(0, 5):
                                self.root[thread_id][ls[0]].child(j).setBackground(i, QBrush(QColor(255, 0, 0)))
                                pass

            elif ls[3] == 'Pause':
                self.mainui.bar[thread_id].setValue(ls[0])
                for i in range(0, 5):
                    self.root[thread_id][ls[0]].setBackground(i, QBrush(QColor(255, 255, 0)))
            else:
                self.mainui.bar[thread_id].setValue(ls[0])
                for i in range(0,5):
                    self.root[thread_id][ls[0]].setBackground(i, QBrush(QColor(255,255,255)))
        except Exception as e:
            print(e)


    def set_state(self, result, thread_id):
        # 设置系统测试状态
        newItem = QTableWidgetItem(result)
        self.mainui.info[thread_id].setItem(0, 1, newItem)
        if(result=='Testing'):
            newItem.setBackground(QColor(255,255,0))
        elif (result == 'Fail'):
            newItem.setBackground(QColor(255, 0, 0))
        elif (result == 'Pass'):
            newItem.setBackground(QColor(0, 255, 0))

    def set_count(self, ls):
        thread_id = ls[2]
        newItem = QTableWidgetItem(str(round(ls[0],2))+'s')
        self.mainui.info[thread_id].setItem(4, 1, newItem)
        # 统计测试个数及通过率
        self.mainui.total_cnt[thread_id] = int(self.mainui.info[thread_id].item(1, 1).text()) + 1
        newItem = QTableWidgetItem(str(self.mainui.total_cnt[thread_id]))
        self.mainui.info[thread_id].setItem(1, 1, newItem)
        if(ls[1]=='Pass'):
            self.mainui.pass_cnt[thread_id] = int(self.mainui.info[thread_id].item(2,1).text()) + 1
            newItem = QTableWidgetItem(str(self.mainui.pass_cnt[thread_id]))
            self.mainui.info[thread_id].setItem(2, 1, newItem)
        self.mainui.y_cnt[thread_id] = self.mainui.pass_cnt[thread_id] / self.mainui.total_cnt[thread_id]
        newItem = QTableWidgetItem(str("%.2f" % (self.mainui.y_cnt[thread_id] * 100)) + '%')
        self.mainui.info[thread_id].setItem(3, 1, newItem)

    # 清除除了测试名称外测试树形结构的其他内容以及进度条
    def clear_seq(self, tree, bar):
        try:
            bar.setValue(0)
            for root in tree:
                for i in range(0, 5):
                    if(i != 0):
                        root.setText(i, '')
                    root.setBackground(i, QBrush(QColor(255, 255, 255)))
                    for j in range(root.childCount()):
                        root.child(j).setText(2, '')
                        root.child(j).setText(3, '')
        except Exception as e:
            log.loginfo.process_log('main:clear_seq:' + str(e))

    # 切换到主界面
    def switch_to_mainwindow(self):
        self.mainui.tabWidget.setCurrentIndex(0)

    def test_log(self):
        self.mainui.tabWidget.setCurrentIndex(1)

    # 刷新用户
    def refresh_user(self, ls):
        self.mainui.lb_main_user.setText(ls[0])
        self.authority()
        # 切换权限会将所有控件显示出来，需要再根据配置文件屏蔽某些控件
        self.mainui.disable_window()

    # 打开zmq调试工具
    def zmq_debug_tool(self):
        self.zmqtool.resize(self.width*0.5, self.height*0.5)
        self.zmqtool.lb_zmqtitle.setMaximumHeight(self.height*0.05)
        self.zmqtool.show()

    # 重新加载Sequence
    def load_sequence(self):
        try:
            for i in range(load.threadnum):
                log.loginfo.process_log('Reload sequence')
                testthread.t_load[i].load_seq()
                self.mainui.testtree[i].clear()
                self.root[i] = self.initialize_tree(self.mainui.testtree[i], testthread.t_load[i].seq_col1, testthread.t_load[i].seq_col7)
        except Exception as e:
            log.loginfo.process_log('main:load_sequence:' + str(e))

    def reload_scripts(self):
        try:
            log.loginfo.process_log('Reload scripts')
            #testthread.reload_scripts()
            for i in range(load.threadnum):
                testthread.t_thread[i].reload_scripts()
            autoslots.reload_scripts()
        except Exception as e:
            log.loginfo.process_log('main:reload_scripts:' + str(e))

    # 切换用户
    def change_user(self):
        global user
        user.le_pwd.setText('')
        user.show()

    # 下一步测试
    def next_step(self):
        for i in range(load.threadnum):
            testthread.t_thread[i].pause = False
            time.sleep(0.1)
            testthread.t_thread[i].pause = True

    # 打开用户管理界面
    def user_management(self):
        self.usertool.resize(self.width * 0.5, self.height * 0.5)
        self.usertool.lb_usertitle.setMaximumHeight(self.height * 0.05)
        self.usertool.get_users()
        self.usertool.show()

    # 显示或隐藏toolbar
    def view_toolbar(self):
        if(self.mainui.actionToolBar.isChecked()):
            self.mainui.toolBar.setHidden(False)
        else:
            self.mainui.toolBar.setHidden(True)

    # 打开tcp调试工具
    def tcp_debug_tool(self):
        #self.tcptool.resize(self.width*0.5, self.height*0.5)
        self.tcptool.lb_tcptitle.setMaximumHeight(self.height * 0.05)
        self.tcptool.show()

        # 打开seq调试工具
    def seq_debug_tool(self):
        edit = editslots.EditSlots()
        edit.editui.resize(self.width * 0.8, self.height * 0.7)
        edit.editui.show()

    # 打开串口调试工具
    def serial_debug_tool(self):
        self.serialtool.list_serial_port()
        self.serialtool.show()

    # 切换到手动控制界面
    def motion_debug(self):
        try:
            self.autos = AutoAttach()
            auto = autoslots.AutoThread()
            auto.autoui.resize(self.width * 0.8, self.height * 0.7)
            auto.autoui.show()
        except Exception as e:
            log.loginfo.process_log('main:motion_debug:' + str(e))

    # 解析zmq server收到的内容
    def recv_server(self, ls):
        if(ls[0][0:5] == 'Start'):
            self.test_start()
        if (ls[0] == 'Stop'):
            self.test_break()
        if (ls[0] == 'Pause'):
            self.test_pause()
        if (ls[0] == 'Continue'):
            self.continue_tool()

    def remote_test(self, ls):
        try:
            if (ls[1][0:5] == 'Start'):
                self.thread_start(ls[0])
            if (ls[1] == 'Stop'):
                self.test_break()
            if (ls[1] == 'Pause'):
                self.test_pause()
            if (ls[1] == 'Continue'):
                self.continue_tool()
        except Exception as e:
            log.loginfo.process_log('main: remote_test:' +str(e))

    def open_sequence_thread(self):
        thread = threading.Thread(target=self.open_sequence)
        thread.setDaemon(True)
        thread.start()

    def open_sequence(self):
        try:
            filename = QFileDialog.getOpenFileName(self, "open", systempath.bundle_dir + '/CSV Files', "Csv files(*.csv)")
            if (platform.system() == "Windows"):
                os.startfile(filename[0])
            else:
                import subprocess
                subprocess.call(["open", filename[0]])
        except Exception as e:
            log.loginfo.process_log('main:open_sequence:' + str(e))

    def open_result_thread(self):
        thread = threading.Thread(target=self.open_result)
        thread.setDaemon(True)
        thread.start()

    def open_result(self):
        filename = QFileDialog.getOpenFileName(self, "open", systempath.bundle_dir + '/Result', "Csv files(*.csv)")
        if (platform.system() == "Windows"):
            os.startfile(filename[0])
        else:
            import subprocess
            subprocess.call(["open", filename[0]])

    def open_log_thread(self):
        thread = threading.Thread(target=self.open_log)
        thread.setDaemon(True)
        thread.start()

    def open_log(self):
        filename = QFileDialog.getOpenFileName(self, "open", systempath.bundle_dir + '/Log',"Log files(*.log)")
        if (platform.system() == "Windows"):
            os.startfile(filename[0])
        else:
            import subprocess
            subprocess.call(["open", filename[0]])

    def authority(self):
        if(self.mainui.lb_main_user.text() == 'Administrator'):
            self.mainui.toolBar.setVisible(True)
            self.mainui.menuTool.setVisible(True)
            self.mainui.actionAutomation.setVisible(True)
            self.mainui.actionOpen_CSV.setVisible(True)
            self.mainui.actionReload_CSV.setVisible(True)
            self.mainui.actionReload_Scripts.setVisible(True)
            self.mainui.actionUser_Manage.setVisible(True)
            self.mainui.actionEdit_Window.setVisible(True)
            self.mainui.actionMotion_Window.setVisible(True)
            self.mainui.actionVision_Window.setVisible(True)
            self.mainui.actionZmq_Debug.setVisible(True)
            self.mainui.actionTcp_Debug.setVisible(True)
            self.mainui.actionSerial_Debug.setVisible(True)
            self.mainui.actionToolBar.setVisible(True)
            self.mainui.actionVision_Window.setVisible(False)
        else:
            self.mainui.toolBar.setVisible(False)
            self.mainui.menuTool.setVisible(False)
            self.mainui.actionAutomation.setVisible(False)
            self.mainui.actionOpen_CSV.setVisible(False)
            self.mainui.actionReload_CSV.setVisible(False)
            self.mainui.actionReload_Scripts.setVisible(False)
            self.mainui.actionUser_Manage.setVisible(False)
            self.mainui.actionEdit_Window.setVisible(False)
            self.mainui.actionMotion_Window.setVisible(False)
            self.mainui.actionVision_Window.setVisible(False)
            self.mainui.actionZmq_Debug.setVisible(False)
            self.mainui.actionTcp_Debug.setVisible(False)
            self.mainui.actionSerial_Debug.setVisible(False)
            self.mainui.actionToolBar.setVisible(False)
            self.mainui.actionVision_Window.setVisible(False)


if __name__ == '__main__':
    '''
    主函数
    '''
    multiprocessing.freeze_support()
    if(platform.system() == "Windows"):
        QApplication.setStyle(QStyleFactory.create("Fusion"))   #Plastique
        font = QtGui.QFont()
        font.setPointSize(10);
        font.setFamily(("arial"))
        QApplication.setFont(font)

    app = QApplication(sys.argv)
    app.setStyleSheet("QTabWidget { background-color: rgb(207, 207, 207) }")
    if(False):
        QMessageBox.information(None, ("Warning!"), ("Script Load Error!"), QMessageBox.StandardButton(QMessageBox.Ok))
    else:
        global user
        user = UserManager()
        user.show()
        # 等待对话框结束
        app.exec_()
        if(user.loginok):
            seq = TestSeq()
            seq.mainui.showMaximized()
            # seq.snwd.show()
            sys.exit(app.exec_())