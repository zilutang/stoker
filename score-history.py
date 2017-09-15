#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:18:29 2017

@author: tangzilu
"""

import tushare as ts
import pandas as pd
import time
from datetime import datetime
import numpy as np
import os
import sys
import commands
#exit()

os.chdir("/data/codes/stoker")
'''
print "hello"
allpd = pd.read_csv("./resources/daily/score.csv", index_col=0)
se1 = allpd.iloc[0]
allpdindex = allpd.index
allpdScoreHistory = pd.DataFrame(columns=allpd.columns)
for i in allpdindex:
    print i
    lineDict = dict()
    line = allpd.iloc[i]
    j = len(line) - 3
    while j -2 >= 0:
        if (line[j].astype(str) == 'nan' and line[j-1].astype(str) == 'nan' and line[j-2].astype(str) == 'nan'):
            line[j - 1] = np.nan
            line[j - 2] = np.nan
            line[j] = np.nan
            j = j - 3
            continue
        elif (line[j - 4] >= line[j - 3] >= line[j - 2] >= line[j - 1] >= line[j]):
            line[j] = "5/" + str(line[j - 4] - line[j])
            line[j - 4] = np.nan
            line[j - 3] = np.nan
            line[j - 2] = np.nan
            line[j - 1] = np.nan
            j = j - 5
            continue
        elif (line[j - 3] >= line[j - 2] >= line[j - 1] >= line[j]):
            line[j] = "4/" + str(line[j - 3] - line[j])
            line[j - 3] = np.nan
            line[j - 2] = np.nan
            line[j - 1] = np.nan
            j = j - 4
            continue
        elif (line[j - 2] >= line[j - 1] >= line[j]):
            line[j] = "3/" + str(line[j - 2] - line[j])
            line[j - 2] = np.nan
            line[j - 1] = np.nan
            j = j - 3
            continue
        else:
            line[j] = np.nan
            j = j - 1
    allpdScoreHistory = allpdScoreHistory.append(line)
        
allpdScoreHistory.to_csv("./resources/daily/allpdScoreHistory.csv")
commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/allpdScoreHistory.csv > ./resources/daily/allpdScoreHistoryGBK.csv")

'''
allpdScoreHistory = pd.read_csv("./resources/daily/allpdScoreHistory.csv")
allpdScoreHistoryIndex = allpdScoreHistory.index
filterResult = []
for i in allpdScoreHistoryIndex:
    lineFilter = allpdScoreHistory.iloc[i][:-2].str.contains("4/")
    countOfName = 0
    for ii in lineFilter.index:
        if str(lineFilter[ii]) == "True":
            countOfName = countOfName + 1
            result = ii + " " + allpdScoreHistory.iloc[i][ii] + " " + str(countOfName) + " " + allpdScoreHistory.iloc[i]["name"]
            print result
            filterResult.append(result)
    
filterpd = pd.DataFrame(filterResult) 
filterpdSplit = pd.DataFrame(filterpd[0].str.split(' ', 3).tolist(),columns = ['date','score', 'count', 'name'])
filterpdSplit.sort_values(["date"], ascending=False).to_csv("./resources/daily/filterpdSplitSortDate.csv")
filterpdSplit.sort_values(["name"]).to_csv("./resources/daily/filterpdSplitSortName.csv")

commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/filterpdSplitSortDate.csv > ./resources/daily/filterpdSplitSortDateGBK.txt")
commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/filterpdSplitSortName.csv > ./resources/daily/filterpdSplitSortNameGBK.txt")
