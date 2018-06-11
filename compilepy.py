# -*- coding: utf-8 -*-

import py_compile
import os
import systempath

rootDir = systempath.bundle_dir
f_list = os.listdir(rootDir)
py_list = []
if('main.pyc' not in f_list):
    for f in f_list:
        if('.py' in f):
            py_list.append(f)
            py_compile.compile(rootDir + '\\' + f, rootDir + '\\' + f + 'c')