#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 22:58:38 2017

@author: tangzilu
"""
import commands
import pandas as pd
import os
import sys
import xlwt
import csv
import uuid
import time
from selenium import webdriver

brower = webdriver.PhantomJS()

def saveGdrsPic(code):
    url = 'http://stock.jrj.com.cn/share,%s,gdhs.shtml' % code
    global brower
    brower.get(url)
    brower.maximize_window()
    time.sleep(3)
    brower.save_screenshot('./pics/%s.jpg' % code)
    print "got pic code %s" % code
    
    
alltodaypd = pd.read_csv("/data/codes/stoker/resources/daily/score.csv")
dfpe = pd.read_csv('/data/codes/stoker/resources/daily/dfpe.csv')
filterpdSplitSortDateWithGap = pd.read_csv("/data/codes/stoker/resources/daily/filterpdSplitSortDateWithGap.csv")

codeList = []
i = 0
for line in filterpdSplitSortDateWithGap['name']:
    i = i + 1
    if i > 200:
        break
    try:
        code = str(dfpe[dfpe['name']==line]['code'].get_values()[0]).zfill(6)
        codeList.append(code)
        saveGdrsPic(code)
    except:
        pass
    
brower.close()