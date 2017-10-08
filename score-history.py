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
import xlwt
import csv
#score.csv-->allpdScoreHistory.csv
#allpdScoreHistory.csv-->filterpdSplitSortDate.csv(filterpdSplitSortDate-today.xls*),filterpdSplitSortName.csv(filterpdSplitSortName-today.xls*)
#fly, climb, rank; strong=climb/rank; rocket=strong/rank
#关注rocket排名靠前的个股，第二次rank再次靠前时，并且有MACD的机会，是绝佳进场机会
#rocket字段定义了rocket算法大于10的个股出现的日期和数值，拥有值的个股再次出现fly排行榜中，并且MACD金叉时，是绝佳买入机会
#exit()
def csv_to_xls(filename):
    myexcel = xlwt.Workbook(encoding = 'utf-8')
    mysheet = myexcel.add_sheet("sheet1")
    csvfile = open(filename,"rb")
    reader = csv.reader(csvfile)
    l = 0
    for line in reader:
        r = 0
        for i in line:
            mysheet.write(l,r,i)
            r=r+1
        l=l+1
    excel_filename = str(filename.split(".")[0]) + "-today.xls"
    myexcel.save(excel_filename)
    print excel_filename
    return excel_filename

os.chdir("/data/codes/stoker")
#todayAll = ts.get_today_all()
#allIndestory = ts.get_industry_classified()
print "hello"
allpd = pd.read_csv("./resources/daily/score.csv", index_col=0)
se1 = allpd.iloc[0]
allpdindex = allpd.index
#allpdScoreHistory = pd.DataFrame(columns=allpd.columns)
allpdScoreHistory = allpd.copy()
for i in allpdindex:
    #print i
    lineDict = dict()
    line = allpd.iloc[i].copy()
    lineIndex = line.index
    j = len(line) - 3
    while j -2 >= 0:
        if (line[j].astype(str) == 'nan' and line[j - 1].astype(str) == 'nan' and line[j - 2].astype(str) == 'nan'):
            line[j - 1] = np.nan
            line[j - 2] = np.nan
            line[j] = np.nan
            j = j - 3
            continue
        elif (line[j - 4] >= line[j - 3] >= line[j - 2] >= line[j - 1] >= line[j]):
            line[j] = "5/" + str(int(line[j - 4] - line[j])) + "/" + str(int(line[j]))
            line[j - 4] = np.nan
            line[j - 3] = np.nan
            line[j - 2] = np.nan
            line[j - 1] = np.nan
            j = j - 5
            continue
        elif (line[j - 3] >= line[j - 2] >= line[j - 1] >= line[j]):
            line[j] = "4/" + str(int(line[j - 3] - line[j])) + "/" + str(int(line[j]))
            line[j - 3] = np.nan
            line[j - 2] = np.nan
            line[j - 1] = np.nan
            j = j - 4
            continue
        elif (line[j - 2] >= line[j - 1] >= line[j]):
            line[j] = "3/" + str(int(line[j - 2] - line[j])) + "/" + str(int(line[j]))
            line[j - 2] = np.nan
            line[j - 1] = np.nan
            j = j - 3
            continue
        else:
            line[j] = np.nan
            j = j - 1
    allpdScoreHistory = allpdScoreHistory.append(line)
    #allpdScoreHistory[j] = line
        
allpdScoreHistory.to_csv("./resources/daily/allpdScoreHistory.csv")
commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/allpdScoreHistory.csv > ./resources/daily/allpdScoreHistoryGBK.csv")

nameWatching = []
allpdScoreHistory = pd.read_csv("./resources/daily/allpdScoreHistory.csv")
allpdScoreHistoryIndex = allpdScoreHistory.index
filterResult = []
for i in allpdScoreHistoryIndex:
    lineFilter = allpdScoreHistory.iloc[i][:-2].str.contains("/")
    countOfName = 0
    maxRocket = 10 
    hasLargeRocket = False
    name = allpdScoreHistory.iloc[i]["name"].replace(' ', '')
    if name in nameWatching:
        name = "* " + name
    for ii in lineFilter.index:
        if str(lineFilter[ii]) == "True":
            countOfName = countOfName + 1
            score = allpdScoreHistory.iloc[i][ii]
            scoreSplit = score.split("/")
            scoreRocket = round(float(scoreSplit[1])/(float(scoreSplit[2]) * float(scoreSplit[2])), 1)
            if (scoreRocket > maxRocket):
                maxRocket = scoreRocket
                hasLargeRocket = True
                rocketDate = ii
            #result = ii + " " + score + " " + str(countOfName) + " " + allpdScoreHistory.iloc[i]["name"]
            
            if (hasLargeRocket == False):
                resultAndRocket = ii + " " + score + " " + str(countOfName) + " " + "--" + " " + str(scoreRocket) + " " + name
            else:
                resultAndRocket = ii + " " + score + " " + str(countOfName) + " " + str(scoreRocket) + " " + str(maxRocket) + '-' + rocketDate[3:] + " " + name
            
            filterResult.append(resultAndRocket)
    
filterpd = pd.DataFrame(filterResult) 
columnList = ['date','score', 'count', 'rocket', 'rocketMax', 'name']
filterpdSplit = pd.DataFrame(filterpd[0].str.split(' ', len(columnList) - 1).tolist(),columns = columnList)
filterpdSplit["count"] = filterpdSplit["count"].astype(int)
filterpdSplit["date"] = pd.to_datetime(filterpdSplit['date'])

climbMean=pd.DataFrame(filterpdSplit['score'].str.split('/').tolist(), index=filterpdSplit.date)[1]
climbMeanpd=pd.DataFrame(climbMean)
climbMeanpd.columns=['climbMean']
climbMeanpd = climbMeanpd.astype(int)
climbMeanDict = dict()
climbMeanpdIndexList = list(set(climbMeanpd.index))
for index in climbMeanpdIndexList:
    climbMeanDict[index] = climbMeanpd[climbMeanpd.index==index].mean().round(2)

climbMeanNewpd = pd.DataFrame(climbMeanDict).T
newfilterpdSplit = filterpdSplit.join(climbMeanNewpd, how='left', on='date')

columnList.append('climbMean')
#columnList.append('gap')
filterpdSplit = newfilterpdSplit
filterpdSplit.sort_values(["date"], ascending=False).reset_index()[columnList].to_csv("./resources/daily/filterpdSplitSortDate.csv")
filterpdSplit.sort_values(["name", "count"]).reset_index()[columnList].to_csv("./resources/daily/filterpdSplitSortName.csv")

commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/filterpdSplitSortDate.csv > ./resources/daily/filterpdSplitSortDateGBK.txt")
commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/filterpdSplitSortName.csv > ./resources/daily/filterpdSplitSortNameGBK.txt")
csv_to_xls("/data/codes/stoker/resources/daily/filterpdSplitSortDate.csv")
csv_to_xls("/data/codes/stoker/resources/daily/filterpdSplitSortName.csv")