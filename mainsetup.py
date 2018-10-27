# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtGui
from PyQt5.uic import loadUi
import systempath
import log
import inihelper
import load
import globaldata


class MainUI(QMainWindow):
    # 实现一个单例类
    _instance = None
    __first_init = True
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self, parent = None):
        if (self.__class__.__first_init):  # 只初始化一次
            self.__class__.__first_init = False  # 只初始化一次
            super(MainUI, self).__init__(parent)
            loadUi(systempath.bundle_dir + '/UI/mainwindow.ui', self)  # 看到没，瞪大眼睛看

            self.setDockNestingEnabled(True)
            log.loginfo.process_log('Initialize main ui')
            # 获取屏幕分辨率
            self.screen = QDesktopWidget().screenGeometry()
            self.width = self.screen.width()
            self.height = self.screen.height()

            # 设置窗口图标
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
            self.setWindowIcon(QtGui.QIcon(systempath.bundle_dir + '/Resource/cyg.ico'))

            # 添加IA Logo
            pixMap = QPixmap(systempath.bundle_dir + '/Resource/IA.png')
            self.lb_ia.setMaximumWidth(self.width * 0.12)
            self.lb_ia.setFixedHeight(self.height * 0.11)
            self.lb_ia.setScaledContents(True)
            self.lb_ia.setPixmap(pixMap)

            # 读取标题与版本号
            self.lb_title.setText(inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Title'))
            self.setWindowTitle(inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Title'))
            self.lb_ver.setText(inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Version'))
            self.pe = QPalette()
            self.pe2 = QPalette()
            self.pe.setColor(QPalette.Window, QColor(0, 255, 0))  # 设置背景颜色
            self.testtree = []
            self.info = []
            self.bar = []

            for i in range(load.threadnum):
                listname = getattr(self, 'testlist' + str(i+1))
                infoname = getattr(self, 'systeminfo' + str(i + 1))
                barname = getattr(self, 'pbar' + str(i + 1))
                self.testtree.append(listname)
                self.info.append(infoname)
                self.bar.append(barname)

            self.total_cnt = []
            self.pass_cnt = []
            self.y_cnt = []
            for i in range(load.threadnum):
                self.total_cnt.append(0)
                self.pass_cnt.append(0)
                self.y_cnt.append(0)

            # 初始化各界面
            self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
            self.init_main_ui()
            self.init_systeminfo()
            self.init_toolbar_ui()

            #添加右键菜单image1
            self.lb_image1.setContextMenuPolicy(3)
            self.lb_image1.customContextMenuRequested.connect(self.showContextMenu1)
            self.cmenu1 = QMenu(self)
            if(self.lan=='EN'):
                self.actsnap1 = self.cmenu1.addAction('Shot')
                self.actstart1 = self.cmenu1.addAction('Live')
                self.actstop1 = self.cmenu1.addAction('Stop')
                self.actsave1 = self.cmenu1.addAction('Save')
            else:
                self.actsnap1 = self.cmenu1.addAction('抓拍')
                self.actstart1 = self.cmenu1.addAction('实时拍照')
                self.actstop1 = self.cmenu1.addAction('停止')
                self.actsave1 = self.cmenu1.addAction('保存图片')

            # 添加右键菜单image2
            self.lb_image2.setContextMenuPolicy(3)
            self.lb_image2.customContextMenuRequested.connect(self.showContextMenu2)
            self.cmenu2 = QMenu(self)
            if (self.lan == 'EN'):
                self.actsnap2 = self.cmenu2.addAction('Shot')
                self.actstart2 = self.cmenu2.addAction('Live')
                self.actstop2 = self.cmenu2.addAction('Stop')
                self.actsave2 = self.cmenu2.addAction('Save')
            else:
                self.actsnap2 = self.cmenu2.addAction('抓拍')
                self.actstart2 = self.cmenu2.addAction('实时拍照')
                self.actstop2 = self.cmenu2.addAction('停止')
                self.actsave2 = self.cmenu2.addAction('保存图片')

            # 添加右键菜单image3
            self.lb_image3.setContextMenuPolicy(3)
            self.lb_image3.customContextMenuRequested.connect(self.showContextMenu3)
            self.cmenu3 = QMenu(self)
            if (self.lan == 'EN'):
                self.actsnap3 = self.cmenu3.addAction('Shot')
                self.actstart3 = self.cmenu3.addAction('Live')
                self.actstop3 = self.cmenu3.addAction('Stop')
                self.actsave3 = self.cmenu3.addAction('Save')
            else:
                self.actsnap3 = self.cmenu3.addAction('抓拍')
                self.actstart3 = self.cmenu3.addAction('实时拍照')
                self.actstop3 = self.cmenu3.addAction('停止')
                self.actsave3 = self.cmenu3.addAction('保存图片')

            # 添加右键菜单image4
            self.lb_image4.setContextMenuPolicy(3)
            self.lb_image4.customContextMenuRequested.connect(self.showContextMenu4)
            self.cmenu4 = QMenu(self)
            if (self.lan == 'EN'):
                self.actsnap4 = self.cmenu4.addAction('Shot')
                self.actstart4 = self.cmenu4.addAction('Live')
                self.actstop4 = self.cmenu4.addAction('Stop')
                self.actsave4 = self.cmenu4.addAction('Save')
            else:
                self.actsnap4 = self.cmenu4.addAction('抓拍')
                self.actstart4 = self.cmenu4.addAction('实时拍照')
                self.actstop4 = self.cmenu4.addAction('停止')
                self.actsave4 = self.cmenu4.addAction('保存图片')
            # 连接信号
            self.connect_singnals()

    def showContextMenu1(self, pos):
        self.cmenu1.move(QtGui.QCursor.pos())
        self.cmenu1.show()

    def showContextMenu2(self, pos):
        self.cmenu2.move(QtGui.QCursor.pos())
        self.cmenu2.show()

    def showContextMenu3(self, pos):
        self.cmenu3.move(QtGui.QCursor.pos())
        self.cmenu3.show()

    def showContextMenu4(self, pos):
        self.cmenu4.move(QtGui.QCursor.pos())
        self.cmenu4.show()

    def showContextMenuTest(self, pos):
        self.cmenutest.move(QtGui.QCursor.pos())
        self.cmenutest.show()

    def connect_singnals(self):
        for j in range(load.threadnum):
            self.info[j].itemChanged.connect(self.info_changed)

    def info_changed(self, item):
        if(item.row()==5 and item.column()==1):
            globaldata.sn = item.text()

    def init_main_ui(self):
        # 初始化主界面各控件大小
        self.lb_title.setFixedHeight(self.height * 0.11)
        self.pe2.setColor(QPalette.WindowText, QColor(8, 80, 208))  # 设置字体颜色
        self.lb_main_user.setPalette(self.pe2)
        self.lb_user_title.setPalette(self.pe2)
        for i in range(load.threadnum):
            #self.testtree[i].setStyleSheet('background-color: rgb(255, 255, 255);')
            self.testtree[i].header().setDefaultAlignment(Qt.AlignCenter)
            self.testtree[i].setContextMenuPolicy(3)
            self.testtree[i].customContextMenuRequested.connect(self.showContextMenuTest)
            self.cmenutest = QMenu(self)
            if (self.lan == 'EN'):
                self.actstarttest = self.cmenutest.addAction('Start')
                self.actstoptest = self.cmenutest.addAction('Stop')
            else:
                self.actstarttest = self.cmenutest.addAction('开始测试')
                self.actstoptest = self.cmenutest.addAction('停止测试')

        self.tabWidget:QTabWidget
        self.tabWidget.tabBar().hide()
        for i in range(10):
            if(self.tabWidget.tabText(i)=='control_bak'):
                self.tabWidget.removeTab(i)

    def init_systeminfo(self):
        # 初始化系统信息栏，第一行为测试状态，2-4行为测试信息统计
        for j in range(load.threadnum):
            self.info[j].setRowCount(50)
            self.info[j].setColumnCount(2)
            # self.info[j].setHorizontalHeaderLabels(['Item', 'Value'])
            self.info[j].horizontalHeader().setStretchLastSection(True)
            self.info[j].verticalHeader().hide()
            if(self.lan=='EN'):
                data1 = ['State:', 'Total:', 'Pass:', 'Yield:','Test Time:', 'Serial Number:']
                data2 = ['Idle', '0', '0', '0', '0','']
            else:
                data1 = ['状态:', '总数:', '通过:', '通过率:', '测试时间:', '序列号:']
                data2 = ['空闲', '0', '0', '0', '0', '']
            for i in range(6):
                newItem1 = QTableWidgetItem(data1[i])
                self.info[j].setItem(i, 0, newItem1)
                newItem2 = QTableWidgetItem(data2[i])
                self.info[j].setItem(i, 1, newItem2)
                if(i==5):
                    #newItem1.setBackground(QColor(255, 255, 0))
                    #newItem2.setBackground(QColor(255, 255, 0))
                    #self.info[j].editItem(newItem2)
                    pass

    def init_toolbar_ui(self):
        # 初始化工具栏
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(systempath.bundle_dir + "/Resource/start.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(systempath.bundle_dir + "/Resource/stop.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(systempath.bundle_dir + "/Resource/home.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(systempath.bundle_dir + "/Resource/refresh.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.actionStart.setIcon(icon1)
        self.actionStop.setIcon(icon2)
        self.actionMainwindow.setIcon(icon3)
        self.actionRefresh.setIcon(icon4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mystepbar = QCheckBox()
        self.mystepbar.setText('StepTest')
        self.mystepbar.setToolTip('Enable step test')
        self.mystepbar.setFont(font)
        self.toolBar.addWidget(self.mystepbar)
        self.nextAction = QAction('Next', self)
        self.toolBar.addAction(self.nextAction)
        self.nextAction.setToolTip('Next step')
        self.nextAction.setDisabled(True)
        self.toolBar.addSeparator()
        self.myloopbar = QCheckBox()
        self.myloopbar.setText('LoopTest')
        self.myloopbar.setToolTip('Enable loop test')
        self.toolBar.addWidget(self.myloopbar)
        self.myloopbar.setFont(font)
        self.toolBar.addSeparator()
        self.actionContinue.setDisabled(True)
        self.language = QComboBox()
        self.language.setToolTip('Change language')
        self.language.addItem('English')
        self.language.addItem('中文')
        self.language.setFixedWidth(self.width * 0.05)
        self.toolBar.setFixedHeight(self.height*0.03)
        self.toolBar.setIconSize(QSize(int(self.height*0.02),int(self.height*0.03)))

        self.language.setStyle(QStyleFactory.create("Fusion"))  # Plastique
        self.change_language(self.lan)

    def disable_window(self):
        self.actionSN_Window.setVisible(False)
        self.autoui = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Automation')
        self.sequi = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Sequence')
        if (self.autoui != 'enable'):
            self.actionMotion_Window.setVisible(False)
            self.actionAutomation.setVisible(False)
        if (self.sequi != 'enable'):
            self.actionEdit.setVisible(False)
            self.actionEdit_Window.setVisible(False)

    def Chinese_ui(self):
        # 工具栏
        self.actionPause.setText('暂停')
        self.actionContinue.setText('继续')
        self.actionLoginTool.setText('登陆')
        self.actionEdit.setText('编辑序列')
        self.actionAutomation.setText('运动控制')
        self.actionLog.setText('日志')
        self.mystepbar.setText('单步测试')
        self.nextAction.setText('下一步')
        self.myloopbar.setText('循环测试')
        # 菜单栏
        self.menuFile.setTitle('文件')
        self.actionOpen_CSV.setText('打开测试序列CSV')
        self.actionOpen_Result.setText('打开结果CSV')
        self.actionOpen_Log.setText('打开日志文件')
        self.actionReload_Scripts.setText('重载脚本')
        self.actionReload_CSV.setText('重载序列')
        self.actionClose_System.setText('退出系统')
        self.menuUser.setTitle('用户')
        self.actionLogin.setText('登陆系统')
        self.actionUser_Manage.setText('用户管理')
        self.menuTool.setTitle('工具')
        self.actionZmq_Debug.setText('ZMQ调试工具')
        self.actionTcp_Debug.setText('TCP调试工具')
        self.actionSerial_Debug.setText('串口调试工具')
        self.menuWindow.setTitle('窗口')
        self.actionMain_Window.setText('主窗口')
        self.actionEdit_Window.setText('序列编辑窗口')
        self.actionMotion_Window.setText('运动控制窗口')
        self.actionVision_Window.setText('视觉窗口')
        self.actionToolBar.setText('工具栏')
        self.lb_user_title.setText('用户:')
        # 测试序列
        for i in range(load.threadnum):
            self.testtree[i].setHeaderLabels(['测试项', '测试时间', '测试数据', '测试结果', '详细结果'])
            self.info[i].setHorizontalHeaderLabels(['标签', '值'])

    def English_ui(self):
        # 工具栏
        self.actionPause.setText('Pause')
        self.actionContinue.setText('Continue')
        self.actionLoginTool.setText('Login')
        self.actionEdit.setText('Edit')
        self.actionAutomation.setText('Automation')
        self.actionLog.setText('Log')
        self.mystepbar.setText('StepTest')
        self.nextAction.setText('Next')
        self.myloopbar.setText('LoopTest')
        # 菜单栏
        self.menuFile.setTitle('File')
        self.actionOpen_CSV.setText('Open Sequence')
        self.actionOpen_Result.setText('Open Result')
        self.actionOpen_Log.setText('Open Log')
        self.actionReload_Scripts.setText('Reload Scripts')
        self.actionReload_CSV.setText('Reload Sequence')
        self.actionClose_System.setText('Close System')
        self.menuUser.setTitle('User')
        self.actionLogin.setText('Login System')
        self.actionUser_Manage.setText('User Manage')
        self.menuTool.setTitle('Tool')
        self.actionZmq_Debug.setText('ZMQ Debug')
        self.actionTcp_Debug.setText('TCP Debug')
        self.actionSerial_Debug.setText('Serial Debug')
        self.menuWindow.setTitle('Window')
        self.actionMain_Window.setText('Main Window')
        self.actionEdit_Window.setText('Sequence Window')
        self.actionMotion_Window.setText('Motion Window')
        self.actionVision_Window.setText('Vision Window')
        self.actionToolBar.setText('ToolBar')
        self.lb_user_title.setText('User:')
        # 测试序列
        for i in range(load.threadnum):
            self.testtree[i].setHeaderLabels(['TestItems', 'TestTime', 'TestData', 'TestResult', 'TestDetails'])
            self.info[i].setHorizontalHeaderLabels(['Item', 'Value'])

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()