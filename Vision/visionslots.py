# -*- coding: utf-8 -*-
import visionsetup
import visionscript


class VisionSlots():
    def __init__(self):
        self.visionui = visionsetup.VisionUI()
        self.vision = visionscript.Vision()
        # self.vision.connect_camera()
        self.vision.init_image_window(self.visionui.lb_image)
        self.connect_singnals()
        model = self.vision.get_model()
        print(model)
        extime = self.vision.get_extime()
        self.vision.set_extime(50000.0)
        self.visionui.cb_camera.clear()
        self.visionui.cb_camera.addItem(str(model))
        self.visionui.dsb_extime.setValue(float(extime))

    def connect_singnals(self):
        self.visionui.pb_snap.clicked.connect(self.vision.capture)
        self.visionui.pb_live.clicked.connect(self.vision.live)