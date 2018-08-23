# -*- coding: utf-8 -*-

import py_compile
import os
import systempath


try:
    # 根目录文件
    rootDir = systempath.bundle_dir
    rootlist = os.listdir(rootDir)
    for f in rootlist:
        childDir = os.path.join(rootDir, f)
        # 获取子文件夹中文件列表
        if(os.path.isdir(childDir)):
            childlist = os.listdir(childDir)
            # 编译子文件夹中的py文件
            for f1 in childlist:
                if ('.py' in f1 and '.pyc' not in f1):
                    py_compile.compile(childDir + '\\' + f1, childDir + '\\' + f1 + 'c')
        # 编译根目录下的py文件
        elif('.py' in f and '.pyc' not in f):
            py_compile.compile(rootDir + '\\' + f, rootDir + '\\' + f + 'c')
except Exception as e:
    print(e)
