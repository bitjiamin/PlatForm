# -*- coding: UTF-8 -*-
"""
FileName: visionscript.py
Author: jiaminbit@sina.com
Create date: 2017.6.20
description: 视觉脚本
Update date：2017.7.20
version 1.0.0
"""


import systempath
import time
import ctypes
from ctypes import *

# Create a black image
#baumer = ctypes.cdll.LoadLibrary(systempath.bundle_dir + '\Scripts\BaumerDll.dll')
#baumer.open_interface()
#a = baumer.get_device_cnt()
#baumer.open_device(0)
#baumer.open_buffer()
#baumer.set_exposuretime(160000)
#filename = c_char_p(b'C:\\Project\\Image\\a.tif')
# image_data为char*类型
#image_data = baumer.one_shot
#image_data.restype = c_char_p
#image_data=baumer.one_shot(5000)
#baumer.save_image(filename, image_data, 2592, 1944)


class Vision():
    def __init__(self):
        self.cap = None
        self.baumer = ctypes.cdll.LoadLibrary(systempath.bundle_dir + '\BaumerDll.dll')
        self.halcon = ctypes.cdll.LoadLibrary(systempath.bundle_dir + '\dlltest.dll')

    def init_window(self,id,row1,col1,row2,col2):
        self.halcon.initialize_window(c_int(id), row1, col1, row2, col2)

    def load_image(self):
        img = cv.imread('test.bmp', cv.IMREAD_GRAYSCALE)  # IMREAD_GRAYSCALE   IMREAD_COLOR
        qimg = self.convert_to_qimage(img)
        return qimg

    def convert_to_qimage(self, im, copy=False):
        gray_color_table = [qRgb(i, i, i) for i in range(256)]
        if im is None:
            return QImage()

        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(gray_color_table)
                return qim.copy() if copy else qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888);
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32);
                    return qim.copy() if copy else qim

    def find_cameras(self):
        cams = []
        try:
            self.baumer.open_interface()
            # type = c_char_p(dev)
            device = self.baumer.get_device_name
            device.restype = c_char_p
            device = self.baumer.get_device_name(0)
            cam = device.decode()
            if(cam!=''):
                cams.append(cam)
        except Exception as e:
            print(e)
        return cams

    def open_camera(self, num):
        try:
            self.baumer.open_device(num)
            self.baumer.open_buffer()
            extime = c_double(80000)
            self.baumer.set_exposuretime(extime)
            return True
        except Exception as e:
            print(e)
            return False

    def close_camera(self):
        try:
            self.baumer.close_system()
        except Exception as e:
            print(e)

    def snap(self):
        image_data = self.baumer.one_shot
        image_data.restype = c_char_p
        image_data = self.baumer.one_shot(5000)
        #print(image_data)
        self.halcon.array_to_image(image_data)
        self.halcon.display_image()
        # filename = c_char_p(b'C:\\Project\\Image\\b.tif')
        # self.baumer.save_image(filename, image_data, 2592, 1944)