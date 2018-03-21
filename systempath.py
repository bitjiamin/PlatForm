# -*- coding: UTF-8 -*-
"""
FileName: systempath.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 获取脚本运行时的路径以及打包成应用程序后的运行路径
Update date：2017.7.20
version 1.0.0
"""

import sys
import os

frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = os.path.dirname(sys.executable)

else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))


