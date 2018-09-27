# -*- coding: UTF-8 -*-
"""
FileName: tcptool.py
Author: jiaminbit@sina.com
Create date: 2018.9.26
description: tcp调试工具
Update date：2018.9.26
version 1.0.0
"""


import configparser
import csv


class IniHelper():
    def __init__(self):
        self.cf = configparser.ConfigParser()

    def read_ini(self, filename, section, key):

        self.cf.read(filename)
        value = self.cf.get(section, key)
        return value

    def write_ini(self, filename, section, key, value):
        self.cf.read(filename)
        self.cf.set(section, key, value)
        # write to file
        self.cf.write(open(filename, "w"))

class CsvHelper():
    def __init__(self):
        pass
    def write_csv(self, filename, value):
        # value为字符串list
        f = open(filename, 'w', encoding='utf8', newline='')
        writer = csv.writer(f)
        writer.writerows(value)

    def add_line(self, filename, value):
        # value为字符串list
        f = open(filename, 'a+', encoding='utf8', newline='')
        writer = csv.writer(f)
        writer.writerow(value)

    def read_csv(self, filename):
        data = []
        csvfile = open(filename, 'r')
        reader = csv.reader(csvfile)
        for seq in reader:
            data.append(seq)
        return data