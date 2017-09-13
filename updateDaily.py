#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:17:37 2017

@author: tangzilu
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 09:38:01 2017

@author: tangzilu
"""

import tushare as ts
import pandas as pd
import time
from datetime import datetime
import numpy as np
import os
from tgrocery import Grocery
import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
os.chdir("/data/codes/stoker")

todayDate = datetime.today()
todayDateFormat0 = "{0}-{1}-{2}".format(todayDate.year, todayDate.month, todayDate.day)
todayDateFormat = "{0}/{1}/{2}".format(todayDate.year, todayDate.month, todayDate.day)
allpd = pd.read_csv("./resources/daily/all.csv", index_col=0)
if todayDateFormat in allpd.columns.tolist():
    exit()
    
stocks = ts.get_today_all()
stocks.to_csv("./resources/daily/everyday/" + todayDateFormat0 + ".csv")
    
todaySortedPd = stocks[["name", "amount"]].sort_values(by="amount", ascending=False).reset_index()[["name"]]

allpdToday = allpd.join(todaySortedPd.rename_axis({"name": todayDateFormat},axis=1))

allpdToday.to_csv("./resources/daily/all.csv")

import commands
commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/all.csv > ./resources/daily/alltoday.csv")
commands.getstatusoutput("cp ./resources/daily/alltoday.csv ./resources/daily/alltoday.txt")
#iconv -f utf-8 -t GBK all.csv > allbb.csv 转换编码让Excel可读
