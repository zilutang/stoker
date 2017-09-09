#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 09:40:18 2017

@author: tangzilu
"""

import tushare as ts
import pandas as pd
import time
import datetime
#record = ts.get_h_data('002337', start='2015-01-01', end='2015-03-16') 
#print record

'''----------date tool
beginDate = datetime.date.today() - datetime.timedelta(days=200)
endDate = datetime.date.today() - datetime.timedelta(days=2)
print beginDate, endDate
'''

'''---------stock List tool
stocks = ts.get_stock_basics()
print stocks['name']
print stocks.index
index = stocks.index.values
print index
'''
import os
for i in os.listdir("./resources/data/stocksHis/"):
    print str(i)[:-4]
    time.sleep(3)