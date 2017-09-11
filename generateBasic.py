#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 09:38:01 2017

@author: tangzilu
"""

import tushare as ts
import pandas as pd
import time
import datetime
import numpy as np
import os
from tgrocery import Grocery


stocks = ts.get_stock_basics()


beginDate = str(datetime.date.today() - datetime.timedelta(days=200)).replace('-', '/')
endDate = str(datetime.date.today() - datetime.timedelta(days=2)).replace('-', '/')
print beginDate
print endDate


index = stocks.index.values

alreadyGetFiles = []

folder = "2014"

for file in os.listdir("./resources/data/export/"):
    alreadyGetFiles.append(str(file)[3:-4])

dates = pd.date_range(start="20140101", end="20141231")

allpd = pd.DataFrame(index=dates.sort_values(ascending=False))

i = 0
for code in alreadyGetFiles:
    i += 1
    if code[:1] == '6' :
        prefix = "SH"
    else:
        prefix = "SZ"
    
    #name=stocks.name[code]
    f1 = pd.read_csv("./resources/data/export/" + prefix + "#" + code + ".txt",usecols=[0,6], names=['a', code], index_col=0)

    f1[code] = f1[code]/100000000
    allpd=allpd.join(f1[code], how='left')
    print str(i) + ":" + code

allpd.to_csv("./resources/" + folder + "/allCodepd.csv")
allpd = allpd.sort_index()

allpdT= allpd.T

allpd.sort_index().to_csv("./resources/" + folder + "/allCodepd.csv")

allpdT.to_csv("./resources/" + folder + "/allCodepdT.csv")


allpdT1 = pd.read_csv("./resources/" + folder + "/allCodepdT.csv", index_col=0)
allpd1 = pd.read_csv("./resources/" + folder + "/allCodepd.csv", index_col=0)
columns = allpd1.index

sortpd = pd.DataFrame(index=range(150))
i = 0
for column in columns:
    i = i + 1
    print i
    col = (allpdT1[column]).sort_values(ascending=False).index
    if (str(col[0]) == "600000") : continue
    L1 = []
    for code in col:
        L1.append(stocks.at[str(code).zfill(6), "name"])
    sortpd = sortpd.join(pd.DataFrame(L1, columns=[column]))
    #if i == 20: break
sortpd.to_csv("./resources/" + folder + "/all.csv")

#iconv -f utf-8 -t GBK all.csv > allbb.csv 转换编码让Excel可读