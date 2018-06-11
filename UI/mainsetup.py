# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import QSize
from PyQt5 import QtGui
from PyQt5.uic import loadUi
import systempath
import log
import inihelper
import load


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
            log.loginfo.process_log('Initialize UI')
            # 获取屏幕分辨率
            self.screen = QDesktopWidget().screenGeometry()
            self.width = self.screen.width()
            self.height = self.screen.height()
            # 添加IA Logo
            pixMap = QPixmap(systempath.bundle_dir + '/Resource/IA.png')
            self.lb_ia.setMaximumWidth(self.width * 0.12)
            self.lb_ia.setFixedHeight(self.height * 0.11)
            self.lb_ia.setScaledContents(True)
            self.lb_ia.setPixmap(pixMap)

            # 读取标题与版本号
            self.lb_title.setText(inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Title'))
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
            self.init_main_ui()
            self.init_toolbar_ui()
            self.init_systeminfo()
            self.disable_window()
            # 实例化信号槽需要用到的类

    def init_main_ui(self):
        # 初始化主界面各控件大小
        self.lb_title.setFixedHeight(self.height * 0.11)
        self.pe2.setColor(QPalette.WindowText, QColor(8, 80, 208))  # 设置字体颜色
        self.lb_main_user.setPalette(self.pe2)
        self.lb_user_title.setPalette(self.pe2)
        for i in range(load.threadnum):
            #self.testtree[i].setStyleSheet('background-color: rgb(255, 255, 255);')
            pass
        self.tabWidget.tabBar().hide()

    def init_systeminfo(self):
        # 初始化系统信息栏，第一行为测试状态，2-4行为测试信息统计
        for j in range(load.threadnum):
            self.info[j].setRowCount(50)
            self.info[j].setColumnCount(2)
            self.info[j].setHorizontalHeaderLabels(['Item', 'Value'])
            self.info[j].horizontalHeader().setStretchLastSection(True)
            self.info[j].verticalHeader().hide()
            data1 = ['State:', 'Total:', 'Pass:', 'Yield:','Test Time:', 'SN:']
            data2 = ['Idle', '0', '0', '0', '0','']
            for i in range(6):
                newItem1 = QTableWidgetItem(data1[i])
                self.info[j].setItem(i, 0, newItem1)
                newItem2 = QTableWidgetItem(data2[i])
                self.info[j].setItem(i, 1, newItem2)
                if(i==5):
                    newItem1.setBackground(QColor(255, 255, 0))
                    newItem2.setBackground(QColor(255, 255, 0))
                    #self.info[j].editItem(newItem2)

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
        self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
        self.change_language(self.lan)

    def disable_window(self):
        self.actionSN_Window.setVisible(False)
        self.visionui = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Vision')
        self.autoui = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Automation')
        self.sequi = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Sequence')
        if (self.visionui != 'enable'):
            self.actionVision_Window.setVisible(False)
            self.tabWidget.removeTab(3)
        if (self.autoui != 'enable'):
            self.actionMotion_Window.setVisible(False)
            self.actionAutomation.setVisible(False)
            self.tabWidget.removeTab(2)
        if (self.sequi != 'enable'):
            self.actionEdit.setVisible(False)
            self.actionEdit_Window.setVisible(False)
            self.tabWidget.removeTab(1)

    def Chinese_ui(self):
        # 工具栏
        self.actionPause.setText('暂停')
        self.actionContinue.setText('继续')
        self.actionLoginTool.setText('登陆')
        self.actionEdit.setText('编辑')
        self.actionAutomation.setText('运动控制')
        self.actionLog.setText('日志')
        self.mystepbar.setText('单步测试')
        self.nextAction.setText('下一步')
        self.myloopbar.setText('循环测试:')
        # 菜单栏
        self.menuFile.setTitle('文件')
        self.actionOpen_CSV.setText('打开测试序列CSV')
        self.actionOpen_Result.setText('打开结果CSV')
        self.actionOpen_Log.setText('打开日志文件')
        self.actionReload_Scripts.setText('重新加载脚本')
        self.actionReload_CSV.setText('重新加载序列')
        self.actionClose_System.setText('退出系统')
        self.menuUser.setTitle('用户')
        self.actionLogin.setText('登陆系统')
        self.actionUser_Manage.setText('用户管理')
        self.menuTool.setTitle('工具')
        self.actionZmq_Debug.setText('Zmq调试工具')
        self.actionTcp_Debug.setText('Tcp调试工具')
        self.actionSerial_Debug.setText('串口调试工具')
        self.menuWindow.setTitle('窗口')
        self.actionMain_Window.setText('主窗口')
        self.actionEdit_Window.setText('序列编辑窗口')
        self.actionMotion_Window.setText('运动控制窗口')
        self.actionVision_Window.setText('视觉窗口')
        self.actionToolBar.setText('工具栏')
        # 测试序列
        for i in range(load.threadnum):
            self.testtree[i].setHeaderLabels(['测试项', '测试时间', '测试数据', '测试结果', '详细结果'])

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
        self.actionZmq_Debug.setText('Zmq Debug')
        self.actionTcp_Debug.setText('Tcp Debug')
        self.actionSerial_Debug.setText('Serial Debug')
        self.menuWindow.setTitle('Window')
        self.actionMain_Window.setText('Main Window')
        self.actionEdit_Window.setText('Sequence Window')
        self.actionMotion_Window.setText('Motion Window')
        self.actionVision_Window.setText('Vision Window')
        self.actionToolBar.setText('ToolBar')
        # 测试序列
        for i in range(load.threadnum):
            self.testtree[i].setHeaderLabels(['TestItems', 'TestTime', 'TestData', 'TestResult', 'TestDetails'])

    def change_language(self, lan):
        if(lan == 'EN'):
            self.English_ui()
        else:
            self.Chinese_ui()