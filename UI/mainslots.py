from serialwindow import *
import log
import dataexchange
import load
from mainsetup import *
from scansnsetup import *


class MainSlots(MainUI):
    def __init__(self, parent=None):
        super(MainSlots, self).__init__(parent)
        self.connect_singnals()
        self.snwd = SNUI()

    def connect_singnals(self):
        for j in range(load.threadnum):
            self.info[j].itemChanged.connect(self.info_changed)

    def info_changed(self, item):
        if(item.row()==5 and item.column()==1):
            dataexchange.sn = item.text()
            print(dataexchange.sn)

    def set_state(self, result, thread_id):
        # 设置系统测试状态
        newItem = QTableWidgetItem(result)
        self.info[thread_id].setItem(0, 1, newItem)
        if(result=='Testing'):
            newItem.setBackground(QColor(255,255,0))
        elif (result == 'Fail'):
            newItem.setBackground(QColor(255, 0, 0))
        elif (result == 'Pass'):
            newItem.setBackground(QColor(0, 255, 0))

    def set_count(self, ls):
        thread_id = ls[2]
        newItem = QTableWidgetItem(str(round(ls[0],2)))
        self.info[thread_id].setItem(4, 1, newItem)
        # 统计测试个数及通过率
        self.total_cnt[thread_id] = int(self.info[thread_id].item(1, 1).text()) + 1
        newItem = QTableWidgetItem(str(self.total_cnt[thread_id]))
        self.info[thread_id].setItem(1, 1, newItem)
        if(ls[1]=='Pass'):
            self.pass_cnt[thread_id] = int(self.info[thread_id].item(2,1).text()) + 1
            newItem = QTableWidgetItem(str(self.pass_cnt[thread_id]))
            self.info[thread_id].setItem(2, 1, newItem)
        self.y_cnt[thread_id] = self.pass_cnt[thread_id] / self.total_cnt[thread_id]
        newItem = QTableWidgetItem(str("%.2f" % (self.y_cnt[thread_id] * 100)) + '%')
        self.info[thread_id].setItem(3, 1, newItem)
