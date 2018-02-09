# -*- coding: utf-8 -*-

import py_compile
import os
import sys

rootDir = 'C:\\Project\\TestSeq'
f_list = os.listdir(rootDir)
py_list = []
for f in f_list:
    if('.py' in f):
        py_list.append(f)
        py_compile.compile(rootDir + '\\' + f, rootDir + '\\' + f + 'c')
print(py_list)