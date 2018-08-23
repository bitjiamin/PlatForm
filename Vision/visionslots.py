# -*- coding: utf-8 -*-
import visionsetup
import visionscript


class VisionSlots():
    def __init__(self):
        self.visionui = visionsetup.VisionUI()
        self.vision = visionscript.Vision()
        self.vision.connect_camera()
        self.vision.init_image_window(self.visionui.lb_image)
        self.connect_singnals()

        extime = self.vision.get_extime()

        print(extime)
        self.vision.set_extime(50000.0)
        self.visionui.cb_camera.clear()
        extime = self.vision.get_extime()
        self.visionui.dsb_extime.setValue(float(extime))
        self.visionui.cb_camera.clear()
        for c in self.vision.cam:
            self.visionui.cb_camera.addItem(str(c))

    def connect_singnals(self):
        self.visionui.pb_snap.clicked.connect(self.vision.capture)
        self.visionui.pb_live.clicked.connect(self.vision.live)
        self.visionui.dsb_extime.valueChanged.connect(self.vision.set_extime)