#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 09:39:58 2017

@author: tangzilu
"""

import tushare as ts
import pandas as pd
import time
from datetime import datetime
import numpy as np
import os
import sys
#exit()

print "hello"
allpd = pd.read_csv("./resources/daily/all.csv", index_col=0)

allpdTop10 = allpd[0:15]
allpdTop10Set = allpdTop10.values
codeSet = set()

for i, row in enumerate(allpdTop10.values):
    print i
    for code in row:
        codeSet.add(code)
        
codeList = list(codeSet)
columns = allpd.columns
newpd = pd.DataFrame(columns=columns)
newpd = newpd.join(pd.DataFrame(columns=["name", "scoreToday"]))
offset = 0
D1 = -1 - offset
D2 = -2 - offset
D3 = -3 - offset
D4 = -4 - offset
D5 = -5 - offset
for code in codeList:
    lineDict = dict()
    for column in columns:
        seriesInColumn = allpd[column]
        indexInColumn = seriesInColumn[seriesInColumn == code].index
        if not indexInColumn.empty:
            lineDict.update({column:indexInColumn.values[0] + 1})
    lineDict.update({"name":code})
    if lineDict.has_key(columns[D1]) and lineDict.has_key(columns[D2]) and lineDict.has_key(columns[D3]):
        d1 = lineDict.get(columns[D1])
        d2 = lineDict.get(columns[D2])
        d3 = lineDict.get(columns[D3])
        if d1 <= d2 and d2 <= d3:
            lineDict.update({"scoreToday":"3"})
        if lineDict.has_key("scoreToday") and lineDict.has_key(columns[D4]):
            d4 = lineDict.get(columns[D4])
            if d3 <= d4:
                lineDict.update({"scoreToday":"4"})
        if lineDict.has_key(columns[D5]) and lineDict.get("scoreToday") == 4:
            d5 = lineDict.get(columns[D5])
            if d4 <= d5:
                lineDict.update({"scoreToday":"5"})
        
    else:
        pass
        
        
    newpd = newpd.append(lineDict, ignore_index=True)
    print code
    
newpd.to_csv("./resources/daily/score.csv")
import commands
commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/score.csv > ./resources/daily/scoretoday-" + str(offset) + ".csv")
