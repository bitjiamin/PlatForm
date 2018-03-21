# -*- coding: utf-8 -*-
import visionsetup
import visionscript


class VisionSlots():
    def __init__(self):
        self.visionui = visionsetup.VisionUI()
        self.vision = visionscript.Vision()
        self.vision.connect_camera()
        self.connect_singnals()
        #self.vision.set_extime(100000.0)

    def connect_singnals(self):
        self.visionui.pb_snap.clicked.connect(self.vision.capture)
        self.visionui.pb_live.clicked.connect(self.vision.live)