# -*- coding: UTF-8 -*-
"""
FileName: mainslots.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 主UI自定义脚本，用于添加主UI主需要自定义的部分
Update date：2017.7.20
version 1.0.0
"""

import mainsetup

"""
自带main ui中主要控件：
lb_title: 软件标题显示（Label）
tabWidget：table页,用来切换主界面显示内容（TabWidget）
testlist1：主序列显示控件（TreeWidget）
systeminfo1：主界面信息显示控件（TableWidget）
lb_image：图像显示控件（Label）
pbar1：进度条（ProcessBar）
lb_ver：版本显示（Label）
lb_main_user：用户名显示（Label）
te_log：Log显示（TextEdit）

图像（最多支持4幅图像）右键菜单事件：
actsnap1,2,3,4——抓拍事件
actstart1,2,3,4——开始实时拍照事件
actstop1,2,3,4——停止实时拍照事件
actsave1,2,3,4——保存图片事件
"""

class MainAttach():
    def __init__(self, parent=None):
        self.mainui = mainsetup.MainUI()