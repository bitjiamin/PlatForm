# -*- coding: UTF-8 -*-
"""
FileName: main.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 主程序
Update date：2017.7.20
version 1.0.0
"""

from login import *
import systempath
import sys
import csv
import load
import log
import os
import platform
from mainwindow import *
from tcptool import *
from zmqtool import *
from serialtool import *
from usermanage import *
import motionthread
import testthread
import zmqserver
import visionthread
from uiprocess import *
import ctypes
sys.path.append(systempath.bundle_dir + '/UI')

class TestSeq(UIProcess, QMainWindow):
    def __init__(self, parent=None):
        super(TestSeq, self).__init__(parent)
        # 按钮槽函数连接
        self.pb_saveseq.clicked.connect(self.save_sequence)
        self.pb_delrow.clicked.connect(self.delete_row)
        self.pb_insertrow.clicked.connect(self.insert_row)
        self.actionReload_CSV.triggered.connect(self.load_sequence)
        self.cb_seq.currentIndexChanged.connect(self.edit_sequence)
        self.tabWidget.currentChanged.connect(self.change_tab_view)
        # 菜单项槽函数连接
        self.actionReload_Scripts.triggered.connect(self.reload_scripts)
        self.actionLogin.triggered.connect(self.change_user)
        self.actionUser_Manage.triggered.connect(self.user_management)
        self.actionMain_Window.triggered.connect(self.switch_to_mainwindow)
        self.actionEdit_Window.triggered.connect(self.edit_sequence)
        self.actionMotion_Window.triggered.connect(self.motion_debug)
        self.actionZmq_Debug.triggered.connect(self.zmq_debug_tool)
        self.actionTcp_Debug.triggered.connect(self.tcp_debug_tool)
        self.actionSerial_Debug.triggered.connect(self.serial_debug_tool)
        self.actionToolBar.triggered.connect(self.view_toolbar)
        self.actionVision_Window.triggered.connect(self.switch_to_visionwindow)
        self.actionOpen_CSV.triggered.connect(self.open_sequence)
        self.actionOpen_Result.triggered.connect(self.open_result)
        self.actionOpen_Log.triggered.connect(self.open_log)
        self.actionClose_System.triggered.connect(self.close)
        # 工具栏信号连接
        self.actionStart.triggered.connect(self.test_start)
        self.actionStop.triggered.connect(self.test_break)
        self.actionPause.triggered.connect(self.test_pause)
        self.actionContinue.triggered.connect(self.continue_tool)
        self.actionLoginTool.triggered.connect(self.change_user)
        self.actionEdit.triggered.connect(self.edit_sequence)
        self.actionAutomation.triggered.connect(self.motion_debug)
        self.actionMainwindow.triggered.connect(self.switch_to_mainwindow)
        self.actionRefresh.triggered.connect(self.reload_scripts)
        self.actionClear.triggered.connect(self.te_log.clear)
        self.myloopbar.clicked.connect(self.enable_loop)
        self.myeditbar.textEdited.connect(self.edit_looptime)
        self.mystepbar.clicked.connect(self.step_test)
        # 两个树形控件的root items
        self.root1 = []
        self.load1 = load.Load('Seq.csv')
        self.bwThread1 = testthread.TestThread(self.load1, 1)
        # 连接子进程的信号和槽函数
        self.bwThread1.finishSignal.connect(self.test_end)
        self.bwThread1.refresh.connect(self.refresh_ui)
        self.bwThread1.refreshloop.connect(self.loop_refresh)
        # 实例化log类
        log.loginfo = log.Log()
        log.loginfo.refreshlog.connect(self.refresh_log)
        # 加载sequence
        self.load1.load_seq()
        log.loginfo.process_log('Load sequence')
        self.initialize_sequence()
        # 初始化用户名
        self.lb_main_user.setText(UserManager.username)
        # 开启zmq server
        self.zmq = zmqserver.ZmqComm()
        self.zmq.zmqrecvsingnal.connect(self.recv_server)
        self.zmq.start()
        # 实例化登陆类
        global user
        user.loginsignal.connect(self.refresh_user)
        # 实例化tcp，串口，zmq调试工具类
        self.tcptool = TcpTool()
        self.serialtool = SerialTool()
        self.zmqtool = ZmqTool()
        self.usertool = UserManage()
        # 连接zmq发送接收信号，显示信息到调试工具界面
        self.zmq.zmqrecvsingnal.connect(self.zmqtool.display_recv_msg)
        self.zmq.zmqsendsingnal.connect(self.zmqtool.display_send_msg)
        # 实例化手动控制类
        self.motion = motionthread.Motion()
        self.motion.iosingnal.connect(self.refresh_motion_para)
        # 连接运动控制相关函数
        self.pb_jog1.pressed.connect(self.jog_forward)
        self.pb_jog1.released.connect(self.axis_stop)
        self.pb_jog2.pressed.connect(self.jog_backward)
        self.pb_jog2.released.connect(self.axis_stop)
        self.pb_absolute.clicked.connect(self.absolute_run)
        self.pb_relative.clicked.connect(self.relative_run)
        self.cb_axis.currentIndexChanged.connect(self.change_axis)
        self.pb_reset.clicked.connect(self.axis_reset)
        # 初始化运动控制界面
        self.motion.initialize_motion()
        self.initialize_motion_ui()
        # 视觉界面槽函数连接
        self.vision = visionthread.VisionThread()
        self.pb_loadimg.clicked.connect(self.load_image)
        self.pb_opencamera.clicked.connect(self.open_camera)
        self.pb_snap.clicked.connect(self.snap)
        self.pb_live.clicked.connect(self.live)
        self.vision.imgsignal.connect(self.refresh_image)

    # 初始化测试序列
    def initialize_sequence(self):
        # self.testlist.setColumnWidth(0, self.width * 0.4)
        self.root1 = self.initialize_tree(self.testlist, self.load1.seq_col1, self.load1.seq_col7)
        self.pbar.setRange(0, len(self.root1) - 1)

    # 初始化显示测试信息的树形结构
    def initialize_tree(self, tree, items, levels):
        log.loginfo.process_log('Initialize sequence tree')
        tree.setColumnCount(5)
        tree.setHeaderLabels(['TestItems', 'Test Time', 'TestData', 'TestResult', 'TestDetails'])
        # 设置行高为25
        tree.setStyleSheet("QTreeWidget::item{height:%dpx}"%int(self.height*0.03))
        header = tree.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        j = 0
        root = []
        for seq in items[1:len(items)]:
            if(levels[j+1] == 'root'):
                root0 = QTreeWidgetItem(tree)
                root.append(root0)
            # 设置根节点的名称
                root0.setText(0, seq)
            else:
                child = QTreeWidgetItem(root0)
                child.setText(0, seq)
            j = j + 1
        return root

    # 重新加载Sequence
    def load_sequence(self):
        log.loginfo.process_log('Reload sequence')
        self.load1.load_seq()
        self.testlist.clear()
        self.root1 = self.initialize_tree(self.testlist, self.load1.seq_col1, self.load1.seq_col7)

    def reload_scripts(self):
        log.loginfo.process_log('Reload scripts')
        testthread.reload_scripts()
        motionthread.reload_scripts()

    # 循环测试时刷新UI
    def loop_refresh(self, times):
        if (self.bwThread1.seq_end):
            if(self.bwThread1.looptime != 0):                     # 确保最后一次只更新循环次数
                self.clear_seq(self.root1, self.pbar)
                self.set_state('Testing')
                self.pe.setColor(QPalette.Window, QColor(255, 255, 0))  # 设置背景颜色
                self.myeditbar.setText(str(self.bwThread1.looptime))

    # 开始测试
    def test_start(self):
        log.loginfo.process_log('Start test')
        self.bwThread1.stop = False
        self.actionStart.setDisabled(True)
        self.myloopbar.setDisabled(True)
        self.myeditbar.setDisabled(True)
        # 开始执行 run() 函数里的内容,只有测试结束了的线程才能开始
        if(self.bwThread1.seq_end):
            self.clear_seq(self.root1,self.pbar)
            self.bwThread1.start()
            self.set_state('Testing')
            self.pe.setColor(QPalette.Window, QColor(255, 255, 0))  # 设置背景颜色

    # 测试结束后刷新UI等
    def test_end(self, ls):
        # 使用传回的返回值
        #self.le_time.setText(str(round(ls[0], 2)) + 's')
        if(self.myloopbar.isChecked()==True and self.myeditbar.text()!='1'):
            self.actionStart.setDisabled(True)
            self.myloopbar.setDisabled(True)
            self.myeditbar.setDisabled(True)
        else:
            self.actionStart.setDisabled(False)
            self.myloopbar.setDisabled(False)
            self.myeditbar.setDisabled(False)

        #self.le_total.setText(str(int(self.le_total.text()) + 1))
        self.set_state(ls[1])
        self.set_count(ls[1])
        if ls[1] == 'Pass':
            #self.le_pass.setText(str(int(self.le_pass.text()) + 1))
            self.pe.setColor(QPalette.Window, QColor(0, 255, 0))  # 设置背景颜色
        else:
            self.pe.setColor(QPalette.Window, QColor(255, 0, 0))  # 设置背景颜色
        #y = int(self.le_pass.text()) / int(self.le_total.text())
        #self.le_yield.setText(str("%.2f" % (y * 100)) + '%')

    # 中止测试
    def test_break(self):
        log.loginfo.process_log('Break test')
        self.bwThread1.stop = True
        self.set_state('Break')

    # 暂停测试
    def test_pause(self):
        log.loginfo.process_log('Pause test')
        self.bwThread1.pause = True
        self.actionPause.setDisabled(True)
        self.actionContinue.setDisabled(False)

    # 开启或关闭单步测试
    def step_test(self):
        if(self.mystepbar.isChecked()):
            self.bwThread1.pause = True
            self.nextAction.setDisabled(False)
            log.loginfo.process_log('Enable step test')
        else:
            self.bwThread1.pause = False
            self.nextAction.setDisabled(True)
            log.loginfo.process_log('Disable step test')

    # 下一步测试
    def next_step(self):
        self.bwThread1.pause = False
        time.sleep(0.1)
        self.bwThread1.pause = True

    # 暂停后继续测试
    def continue_tool(self):
        self.bwThread1.pause = False
        self.actionPause.setDisabled(False)
        self.actionContinue.setDisabled(True)
        log.loginfo.process_log('continue test')

    # 开启或关闭循环测试
    def enable_loop(self):
        if(self.myloopbar.isChecked()):
            self.bwThread1.loop = True
            self.bwThread1.looptime = int(self.myeditbar.text())
            log.loginfo.process_log('Enable loop test')
        else:
            self.bwThread1.loop = False
            log.loginfo.process_log('Disable loop test')

    # 修改循环测试次数
    def edit_looptime(self):
        try:
            self.bwThread1.looptime = int(self.myeditbar.text())
        except Exception as e:
            log.loginfo.process_log(str(e))

    # 测试过程中刷新UI，线程1
    def refresh_ui(self,ls):
        print(ls)
        # 每个测试项测试结果个数
        l_result = int(len(ls[2]) / 2)
        print(l_result)
        # 有子项时显示子项
        if(l_result > 1):
            for i in range(l_result):
                self.root1[ls[0]].child(i).setText(2, str(ls[2][i]))
                self.root1[ls[0]].child(i).setText(3, ls[3][i])
        # 将结果列表的括号去掉后再显示
        ls[2] = str(ls[2])[1:len(str(ls[2])) - 1]
        ls[4] = str(ls[4])[1:len(str(ls[4])) - 1]

        # 显示其他信息
        for i in range(1, 5):
            if (i != 3):
                self.root1[ls[0]].setText(i, str(ls[i]))
            else:
                if('Fail' in ls[i]):
                    self.root1[ls[0]].setText(i, 'Fail')
                elif(ls[i][0]== 'Skip'):
                    self.root1[ls[0]].setText(i, 'Skip')
                else:
                    self.root1[ls[0]].setText(i, 'Pass')

        if ls[3] == "Testing":
            for i in range(0,5):
                self.root1[ls[0]].setBackground(i, QBrush(QColor(0,255,100)))
        elif "Fail" in ls[3]:
            self.pbar.setValue(ls[0])
            for i in range(0,5):
                self.root1[ls[0]].setBackground(i, QBrush(QColor(255,0,0)))
        elif ls[3] == 'Pause':
            self.pbar.setValue(ls[0])
            for i in range(0, 5):
                self.root1[ls[0]].setBackground(i, QBrush(QColor(255, 255, 0)))
        else:
            self.pbar.setValue(ls[0])
            for i in range(0,5):
                self.root1[ls[0]].setBackground(i, QBrush(QColor(255,255,255)))

    # 清除除了测试名称外测试树形结构的其他内容以及进度条
    def clear_seq(self, tree, bar):
        bar.setValue(0)
        for root in tree:
            for i in range(0, 5):
                if(i != 0):
                    root.setText(i, '')
                root.setBackground(i, QBrush(QColor(255, 255, 255)))
                for j in range(root.childCount()):
                    root.child(j).setText(2, '')
                    root.child(j).setText(3, '')

    # 切换到序列编辑页面，并且将Seq1的信息读取到表格
    def edit_sequence(self):
        self.tabWidget.setCurrentIndex(1)
        #self.tableseq.clear()

        if(self.cb_seq.currentIndex() == 0):
            items = [self.load1.seq_col1, self.load1.seq_col2, self.load1.seq_col3, self.load1.seq_col4,
                     self.load1.seq_col5, self.load1.seq_col6, self.load1.seq_col7]
        else:
            items = [self.load2.seq_col1, self.load2.seq_col2, self.load2.seq_col3, self.load2.seq_col4,
                     self.load2.seq_col5, self.load2.seq_col6, self.load2.seq_col7]
        for j in range(7):
            i = 0
            for seq in items[j][1:len(items[j])]:
                if(j==2):
                    self.MyCombo = QComboBox()
                    self.MyCombo.addItem("test")
                    self.MyCombo.addItem("skip")
                    self.tableseq.setCellWidget(i, j, self.MyCombo)
                    if(seq == 'test'):
                        self.MyCombo.setCurrentIndex(0)
                    else:
                        self.MyCombo.setCurrentIndex(1)
                elif(j==5):
                    self.MyCombo1 = QComboBox()
                    self.MyCombo1.addItem("continue")
                    self.MyCombo1.addItem("finish")
                    self.tableseq.setCellWidget(i, j, self.MyCombo1)
                    if (seq == 'continue'):
                        self.MyCombo1.setCurrentIndex(0)
                    else:
                        self.MyCombo1.setCurrentIndex(1)
                elif (j == 6):
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
    def save_sequence(self):
        if (self.cb_seq.currentIndex() == 0):
            filepath = systempath.bundle_dir + '/CSV Files/Seq.csv'
        else:
            filepath = systempath.bundle_dir + '/CSV Files/Seq2.csv'
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
        self.load_sequence()

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

    def change_tab_view(self):
        index=self.tabWidget.currentIndex()
        if(index==1):
            self.edit_sequence()
        elif (index == 2):
            self.motion_debug()
        elif (index == 3):
            self.switch_to_visionwindow()

    # 切换到主界面
    def switch_to_mainwindow(self):
        self.tabWidget.setCurrentIndex(0)

    # 切换用户
    def change_user(self):
        global user
        user.le_pwd.setText('')
        user.show()

    # 刷新用户
    def refresh_user(self, ls):
        self.lb_main_user.setText(ls[0])
        self.authority()


    # 打开zmq调试工具
    def zmq_debug_tool(self):
        self.zmqtool.resize(self.width*0.5, self.height*0.5)
        self.zmqtool.lb_zmqtitle.setMaximumHeight(self.height*0.05)
        self.zmqtool.show()

    # 打开用户管理界面
    def user_management(self):
        self.usertool.resize(self.width * 0.5, self.height * 0.5)
        self.usertool.lb_usertitle.setMaximumHeight(self.height * 0.05)
        self.usertool.get_users()
        self.usertool.show()

    # 显示或隐藏toolbar
    def view_toolbar(self):
        if(self.actionToolBar.isChecked()):
            self.toolBar.setHidden(False)
        else:
            self.toolBar.setHidden(True)

    # 打开tcp调试工具
    def tcp_debug_tool(self):
        self.tcptool.resize(self.width*0.5, self.height*0.5)
        self.tcptool.lb_tcptitle.setMaximumHeight(self.height * 0.05)
        self.tcptool.show()

    # 打开串口调试工具
    def serial_debug_tool(self):
        self.serialtool.resize(self.width * 0.5, self.height * 0.5)
        self.serialtool.lb_serialtitle.setMaximumHeight(self.height * 0.05)
        self.serialtool.pb_serialsend.setMaximumWidth(self.width * 0.1)
        self.serialtool.pb_serialcon.setMaximumWidth(self.width * 0.1)
        self.serialtool.cb_serialname.setMaximumWidth(self.width * 0.1)
        self.serialtool.cb_baund.setMaximumWidth(self.width * 0.1)
        self.serialtool.cb_fluid.setMaximumWidth(self.width * 0.1)
        self.serialtool.cb_stopbit.setMaximumWidth(self.width * 0.1)
        self.serialtool.cb_checkbit.setMaximumWidth(self.width * 0.1)
        self.serialtool.cb_databit.setMaximumWidth(self.width * 0.1)
        self.serialtool.list_serial_port()
        self.serialtool.show()

    # 切换到手动控制界面
    def motion_debug(self):
        motionthread.auto.choose_axis(self.cb_axis.currentText())
        self.tabWidget.setCurrentIndex(2)

    # 初始化IO表，从配置文件中读取信息
    def initialize_motion_ui(self):
        self.motion.read_io_config()
        self.motion.read_axis_config()
        self.tw_io.setColumnCount(2)
        self.tw_io.setRowCount(len(self.motion.io_name) + 10)
        self.tw_io.setHorizontalHeaderLabels(['IO', 'Description'])
        self.mapper = QtCore.QSignalMapper(self)
        i = 0
        for seq in self.motion.io_name:
            if(i != 0):
                self.MyCheck = QCheckBox()
                self.MyCheck.setText('--- ' + seq)
                self.tw_io.setCellWidget(i-1, 0, self.MyCheck)
                newItem = QTableWidgetItem(self.motion.io_desc[i])
                self.tw_io.setItem(i - 1, 1, newItem)

                # 原始信号（表格中checkbox的鼠标点击信号）传递给map
                self.tw_io.cellWidget(i - 1, 0).clicked.connect(self.mapper.map)
                # 设置map信号的转发规则, 转发为参数为int类型的信号
                self.mapper.setMapping(self.tw_io.cellWidget(i - 1, 0), i - 1)
            i = i+1

        # map信号连接到自定义的槽函数，参数类型为int
        self.mapper.mapped[int].connect(self.write_io)

        self.tw_io.horizontalHeader().setStretchLastSection(True)
        j = 0
        self.cb_axis.clear()
        for seq in self.motion.axis_name:
            if(j != 0):
                self.cb_axis.addItem(seq)
            j = j+1

    # 刷新运动控制参数（IO）
    def refresh_motion_para(self,ls):
        self.dsb_real_pos.setValue(ls[0])
        i = 0
        for io in ls[1]:
            if(io == '1'):
                self.tw_io.cellWidget(i, 0).setChecked(True)
            else:
                self.tw_io.cellWidget(i, 0).setChecked(False)
            i = i + 1

    # 写IO信号
    def write_io(self, index):
        if(self.tw_io.cellWidget(index,0).isChecked()==True):
            value = 1
        else:
            value = 0
        self.motion.write_io(index, value)

    # 解析zmq server收到的内容
    def recv_server(self, ls):
        if(ls[0] == 'Start'):
            self.test_start()

    def refresh_log(self, msg):
        self.te_log.setStyleSheet("color:blue")
        self.te_log.append(msg)

    # 运动相关函数
    def change_axis(self):
        motionthread.auto.choose_axis(self.cb_axis.currentText())

    def absolute_run(self, value):
        value = int(self.dsb_step.value()*1000)
        motionthread.auto.absolute_run(value)

    def relative_run(self):
        value = int(self.dsb_step.value() * 1000)
        motionthread.auto.relative_run(value)
        return True

    def jog_backward(self):
        motionthread.auto.jog_backward()

    def jog_forward(self):
        motionthread.auto.jog_forward()

    def axis_reset(self):
        motionthread.auto.go_home()

    def axis_stop(self):
        motionthread.auto.stop()

    def switch_to_visionwindow(self):
        self.tabWidget.setCurrentIndex(3)
        winxy = self.mapToGlobal(QPoint(0, 0))
        # 图像显示窗口坐标减去主窗口坐标
        imagexy = self.lb_image.mapToGlobal(-winxy)
        self.vision.init_win(int(self.lb_image.winId()),imagexy.y(),imagexy.x(),self.lb_image.width(),self.lb_image.height())
        #self.vision.init_win(0,imagexy.y(),imagexy.x(),self.lb_image.width(),self.lb_image.height())
        cams = self.vision.find_cameras()
        for cam in cams:
            self.cb_camera.addItem(cam)

    def load_image(self):
        qimg = self.vision.load_image()
        # 根据控件大小调整图片大小
        qimg = qimg.scaled(self.lb_image.height(), self.lb_image.width())
        self.lb_image.setPixmap(QPixmap(qimg))

    def open_camera(self):
        if(self.pb_opencamera.text() == 'Open'):
            if(self.vision.open_camera(self.cb_camera.currentIndex())):
                self.pb_opencamera.setText('Close')
                self.pb_live.setDisabled(False)
                self.pb_snap.setDisabled(False)
        else:
            self.vision.close_camera()
            self.pb_opencamera.setText('Open')
            self.pb_live.setDisabled(True)
            self.pb_snap.setDisabled(True)

    def snap(self):
        self.vision.snap()

    def live(self):
        self.vision.stoplive = False
        if(self.pb_live.text() == 'Live'):
            self.vision.start_live()
            self.pb_live.setText('Stop')
        else:
            self.vision.stoplive = True
            self.pb_live.setText('Live')

    def refresh_image(self, img):
        qimg = img.scaled(self.lb_image.width(), self.lb_image.height())
        self.lb_image.setPixmap(QPixmap(qimg))

    def open_sequence(self):
        filename = QFileDialog.getOpenFileName(self, "open", systempath.bundle_dir + '/CSV Files', "Csv files(*.csv)")
        if (platform.system() == "Windows"):
            os.startfile(filename[0])
        else:
            import subprocess
            subprocess.call(["open", filename[0]])

    def open_result(self):
        filename = QFileDialog.getOpenFileName(self, "open", systempath.bundle_dir + '/Result', "Csv files(*.csv)")
        if (platform.system() == "Windows"):
            os.startfile(filename[0])
        else:
            import subprocess
            subprocess.call(["open", filename[0]])

    def open_log(self):
        filename = QFileDialog.getOpenFileName(self, "open", systempath.bundle_dir + '/Log',"Log files(*.log)")
        if (platform.system() == "Windows"):
            os.startfile(filename[0])
        else:
            import subprocess
            subprocess.call(["open", filename[0]])

    def authority(self):
        if(self.lb_main_user.text() == 'Administrator'):
            self.actionPause.setVisible(True)
            self.actionContinue.setVisible(True)
            self.actionEdit.setVisible(True)
            self.actionAutomation.setVisible(True)
            self.actionOpen_CSV.setVisible(True)
            self.actionReload_CSV.setVisible(True)
            self.actionUser_Manage.setVisible(True)
            self.actionEdit_Window.setVisible(True)
            self.actionMotion_Window.setVisible(True)
            self.actionVision_Window.setVisible(True)
            self.mystepbar.setDisabled(False)
            self.nextAction.setDisabled(False)
            self.myloopbar.setDisabled(False)
            self.myeditbar.setDisabled(False)

        else:
            self.actionPause.setVisible(False)
            self.actionContinue.setVisible(False)
            self.actionEdit.setVisible(False)
            self.actionAutomation.setVisible(False)
            self.actionOpen_CSV.setVisible(False)
            self.actionReload_CSV.setVisible(False)
            self.actionUser_Manage.setVisible(False)
            self.actionEdit_Window.setVisible(False)
            self.actionMotion_Window.setVisible(False)
            self.actionVision_Window.setVisible(False)
            self.mystepbar.setDisabled(True)
            self.nextAction.setDisabled(True)
            self.myloopbar.setDisabled(True)
            self.myeditbar.setDisabled(True)


if __name__ == '__main__':
    '''
    主函数
    '''
    #print(QStyleFactory.keys())
    if(platform.system() == "Windows"):
        QApplication.setStyle(QStyleFactory.create("Fusion"))   #Plastique
        font = QtGui.QFont()
        font.setPointSize(10);
        font.setFamily(("arial"))
        QApplication.setFont(font)

    scriptpath = systempath.bundle_dir+'/Scripts/testscript.py'
    app = QApplication(sys.argv)
    app.setStyleSheet("QTabWidget { background-color: rgb(207, 207, 207) }")
    if(not os.path.exists(scriptpath)):
        QMessageBox.information(None, ("Warning!"), ("Script Error!"), QMessageBox.StandardButton(QMessageBox.Ok))
    else:
        global user
        user = UserManager()
        user.show()
        # 等待对话框结束
        app.exec_()
        if(user.loginok):
            seq = TestSeq()
            seq.showMaximized()
            sys.exit(app.exec_())