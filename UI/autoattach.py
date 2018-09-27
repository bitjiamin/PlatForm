# -*- coding: UTF-8 -*-
"""
FileName: mainslots.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 主UI自定义脚本，用于添加主UI主需要自定义的部分
Update date：2017.7.20
version 1.0.0
"""

import autosetup

"""
自带auto ui中主要控件：
dsb_real_pos: 轴实时位置（DoubleSpinBox）
dsb_real_speed：轴实时速度（DoubleSpinBox）
dsb_auto_speed：轴自动速度（DoubleSpinBox）
dsb_man_speed：轴手动速度（DoubleSpinBox）
dsb_step：轴相对运动距离（绝对运动位置）（DoubleSpinBox）
pb_jog1：轴正向jog（PushButton）
pb_jog2：轴反方向jog（PushButton）
pb_absolute：轴绝对运动（PushButton）
pb_relative：轴相对运动（PushButton）
pb_home：轴回原点（PushButton）
pb_reset：轴复位（PushButton）
pb_axis_stop：轴停止（PushButton）
cb_io：IO模块选择（ComboBox）
tw_io：IO读取与写入（TableWidget）
cb_para：参数模块选择（ComboBox）
tw_para：参数读取与写入（TableWidget）
"""


class AutoAttach():
    def __init__(self, parent=None):
        self.autoui = autosetup.AutoUI()