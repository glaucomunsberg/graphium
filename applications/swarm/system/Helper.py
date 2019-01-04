#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

class Helper:
    _instance   = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Helper, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        None
    
    def getSerialNow(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    def getTimeNow(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_time_elapsed(self, start_string, end_string):
        start_date = datetime.datetime.strptime(start_string, '%Y%m%d%H%M%S')
        end_date = datetime.datetime.strptime(end_string, '%Y%m%d%H%M%S')
        time_delta = end_date - start_date
        return time_delta.seconds + (time_delta.days*60*60*24)

    def filePathToList(self,path_file):
        lines = []
        file = open(path_file,'r')
        for line in file:
            lines.append(line.replace('\n', '').replace('\r', ''))
        return lines