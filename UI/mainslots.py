from serialwindow import *
import log
import globaldata
import load
import mainsetup


class MainSlots():
    def __init__(self, parent=None):
        #super(MainSlots, self).__init__(parent)
        self.mainui = mainsetup.MainUI()
        self.connect_singnals()

    def connect_singnals(self):
        for j in range(load.threadnum):
            self.mainui.info[j].itemChanged.connect(self.info_changed)

    def info_changed(self, item):
        if(item.row()==5 and item.column()==1):
            globaldata.sn = item.text()
            print(globaldata.sn)