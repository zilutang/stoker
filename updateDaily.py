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

#stocks = ts.get_today_all()
reload(sys) 
sys.setdefaultencoding( "utf-8" )
todayDate = datetime.today()
todayDateFormat = "{0}-{1}-{2}".format(todayDate.year, todayDate.month, todayDate.day)

allpd = pd.read_csv("./resources/daily/all.csv", index_col=0)
todaySortedPd = stocks[["name", "amount"]].sort_values(by="amount", ascending=False).reset_index()[["name"]]

allpdToday = allpd.join(todaySortedPd.rename_axis({"name": todayDateFormat},axis=1))


#iconv -f utf-8 -t GBK all.csv > allbb.csv 转换编码让Excel可读