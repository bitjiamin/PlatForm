from mainwindow import *
from PyQt5.QtGui import QPixmap, QPalette, QColor, QBrush
from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtWidgets import *

import  systempath
import log
import inihelper

class UIProcess(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(UIProcess, self).__init__(parent)
        self.setupUi(self)
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
        # 切换到主界面
        #self.tabWidget.tabBar().hide()
        self.tabWidget.setCurrentIndex(0)

        self.pe = QPalette()
        self.pe2 = QPalette()

        self.pe.setColor(QPalette.Window, QColor(0, 255, 0))  # 设置背景颜色
        # 初始化各界面
        self.init_main_ui()
        self.init_toolbar_ui()
        self.init_vision_ui()
        self.init_seq()
        self.init_systeminfo()
        self.disable_window()

    def init_main_ui(self):
        # 初始化主界面各控件大小
        self.systeminfo.setMaximumWidth(self.width * 0.2)
        self.setMinimumHeight(self.height * 0.5)
        self.setMinimumWidth(self.width * 0.5)
        self.lb_title.setFixedHeight(self.height * 0.11)
        self.lb_main_user.setMaximumWidth(self.width * 0.1)

        self.pe2.setColor(QPalette.WindowText, QColor(8, 80, 208))  # 设置字体颜色
        self.lb_main_user.setPalette(self.pe2)
        self.lb_user_title.setPalette(self.pe2)
        self.testlist.setStyleSheet('background-color: rgb(255, 255, 255);')

    def init_systeminfo(self):
        # 初始化系统信息栏，第一行为测试状态，2-4行为测试信息统计
        self.systeminfo.setRowCount(50)
        self.systeminfo.setColumnCount(2)
        self.systeminfo.setHorizontalHeaderLabels(['Item', 'Value'])
        self.systeminfo.setColumnWidth(0, self.width * 0.06)
        self.systeminfo.horizontalHeader().setStretchLastSection(True)
        self.systeminfo.verticalHeader().hide()
        data1 = ['State:', 'Total:', 'Pass:', 'Yield:']
        data2 = ['Idle', '0', '0', '0']

        for i in range(4):
            newItem1 = QTableWidgetItem(data1[i])
            self.systeminfo.setItem(i, 0, newItem1)
            newItem2 = QTableWidgetItem(data2[i])
            self.systeminfo.setItem(i, 1, newItem2)

    def set_state(self, result):
        # 设置系统测试状态
        newItem = QTableWidgetItem(result)
        self.systeminfo.setItem(0, 1, newItem)
        if(result=='Testing'):
            newItem.setBackground(QColor(255,255,0))
        elif (result == 'Fail'):
            newItem.setBackground(QColor(255, 0, 0))
        elif (result == 'Pass'):
            newItem.setBackground(QColor(0, 255, 0))

    def set_count(self, result):
        # 统计测试个数及通过率
        total_cnt = int(self.systeminfo.item(1, 1).text()) + 1
        newItem = QTableWidgetItem(str(total_cnt))
        self.systeminfo.setItem(1, 1, newItem)
        if(result=='Pass'):
            pass_cnt = int(self.systeminfo.item(2,1).text()) + 1
            newItem = QTableWidgetItem(str(pass_cnt))
            self.systeminfo.setItem(2, 1, newItem)
        y_cnt = pass_cnt / total_cnt
        newItem = QTableWidgetItem(str("%.2f" % (y_cnt * 100)) + '%')
        self.systeminfo.setItem(3, 1, newItem)

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
        self.nextAction.triggered.connect(self.next_step)
        self.nextAction.setToolTip('Next step')
        self.nextAction.setDisabled(True)
        self.toolBar.addSeparator()
        self.myloopbar = QCheckBox()
        self.myloopbar.setText('LoopTest:')
        self.myloopbar.setToolTip('Enable loop test')
        self.toolBar.addWidget(self.myloopbar)
        self.myeditbar = QLineEdit()
        self.myeditbar.setText('0')
        self.myeditbar.setToolTip('Loop test times')
        self.myloopbar.setFont(font)
        self.myeditbar.setMaximumWidth(self.width * 0.03)
        self.myeditbar.setStyleSheet('background-color: rgb(237, 237, 237);')
        self.myeditbar.setFont(font)
        self.toolBar.addWidget(self.myeditbar)
        self.toolBar.addSeparator()
        self.actionContinue.setDisabled(True)

        self.language = QComboBox()
        #self.language.setText('LoopTest')
        self.language.setToolTip('Change language')
        self.language.addItem('English')
        self.language.addItem('中文')
        self.language.setFixedWidth(self.width * 0.05)
        # self.toolBar.addWidget(self.language)
        self.language.currentIndexChanged.connect(self.change_language)
        self.toolBar.setFixedHeight(self.height*0.03)
        self.toolBar.setIconSize(QSize(int(self.height*0.02),int(self.height*0.03)))
        self.language.setStyle(QStyleFactory.create("Fusion"))  # Plastique

        self.lan = inihelper.read_ini(systempath.bundle_dir + '/Config/Config.ini', 'Config', 'Language')
        if(self.lan=='EN'):
            self.English_ui()
        else:
            self.Chinese_ui()

    def disable_window(self):
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

    def init_vision_ui(self):
        # 初始化视觉界面

        self.pb_loadimg.setMaximumWidth(self.width * 0.1)
        self.pb_snap.setMaximumWidth(self.width * 0.1)
        self.pb_live.setMaximumWidth(self.width * 0.1)
        self.pb_opencamera.setMaximumWidth(self.width * 0.1)
        self.cb_camera.setMaximumWidth(self.width * 0.1)
        self.sb_extime.setMaximumWidth(self.width * 0.1)
        self.pb_snap.setDisabled(True)
        self.pb_live.setDisabled(True)

    # 初始化编辑测试序列的表格
    def init_seq(self):
        log.loginfo.process_log('Initialize sequence table')
        self.tableseq.setRowCount(50)
        self.tableseq.setColumnCount(7)
        self.tableseq.setHorizontalHeaderLabels(['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])
        self.tableseq.setColumnWidth(0, self.width * 0.4)
        self.tableseq.setColumnWidth(1, self.width * 0.2)
        self.tableseq.horizontalHeader().setStretchLastSection(True)
        self.pb_saveseq.setMaximumWidth(self.width * 0.08)
        self.cb_seq.setMaximumWidth(self.width * 0.08)
        self.pb_delrow.setMaximumWidth(self.width * 0.08)
        self.pb_insertrow.setMaximumWidth(self.width * 0.08)

    def Chinese_ui(self):
        # 工具栏
        self.actionPause.setText('暂停')
        self.actionContinue.setText('继续')
        self.actionLoginTool.setText('登陆')
        self.actionEdit.setText('编辑')
        self.actionAutomation.setText('运动控制')
        self.actionClear.setText('清除日志')
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
        self.testlist.setHeaderLabels(['测试项', '测试时间', '测试数据', '测试结果', '详细结果'])
        # 序列编辑
        self.lb_edit.setText('序列编辑')
        self.pb_insertrow.setText('插入行')
        self.pb_delrow.setText('删除选定行')
        self.pb_saveseq.setText('保存序列')
        self.tableseq.setHorizontalHeaderLabels(['测试项', '函数', '模式', '下限', '上限', '失败后跳转', '等级'])

    def English_ui(self):
        # 工具栏
        self.actionPause.setText('Pause')
        self.actionContinue.setText('Continue')
        self.actionLoginTool.setText('Login')
        self.actionEdit.setText('Edit')
        self.actionAutomation.setText('Automation')
        self.actionClear.setText('Clear')
        self.mystepbar.setText('StepTest')
        self.nextAction.setText('Next')
        self.myloopbar.setText('LoopTest:')
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
        self.testlist.setHeaderLabels(['TestItems', 'TestTime', 'TestData', 'TestResult', 'TestDetails'])
        # 序列编辑
        self.lb_edit.setText('Edit Test Sequence')
        self.pb_insertrow.setText('Insert Row')
        self.pb_delrow.setText('Delete Row')
        self.pb_saveseq.setText('Save')
        self.tableseq.setHorizontalHeaderLabels(['TestItem', 'Function', 'Mode', 'Low Limit', 'Up Limit', 'Next Step', 'Level'])

    def change_language(self):
        if(self.language.currentIndex() == 0):
            self.English_ui()
        else:
            self.Chinese_ui()