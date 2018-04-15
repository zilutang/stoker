#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 23:48:08 2017

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
from libs import *

dfpe = ts.get_stock_basics()[['name', 'pe']]
pdraw = pd.read_csv('/data/codes/stoker/resources/daily/allraw.csv', sep='\t')
dfpe.to_csv('./resources/daily/dfpe.csv')
filterpdSplitSortNameLastYear = "/data/codes/stoker/resources/daily/2016/filterpdSplitSortName.csv"
pdLastYear = pd.read_csv(filterpdSplitSortNameLastYear)
namelistLastYear = list(set(pdLastYear.name))
dictLastYear = dict()
for name in namelistLastYear:
    date = pdLastYear[pdLastYear.name==name].tail(1).date
    dictLastYear[name] = date

filterpdSplitSortNameThisYear = "/data/codes/stoker/resources/daily/filterpdSplitSortName.csv"
filterpdSplitSortNameThisYearWithGap = "/data/codes/stoker/resources/daily/filterpdSplitSortNameWithGap.csv"
filterpdSplitSortDateThisYearWithGap = "/data/codes/stoker/resources/daily/filterpdSplitSortDateWithGap.csv"
filterpdSplitSortDateThisYearWithGapCount1 = "/data/codes/stoker/resources/daily/filterpdSplitSortDateWithGapCount1.csv"
pdThisYear = pd.read_csv(filterpdSplitSortNameThisYear)
listThisYear = list(set(pdThisYear['name']))
pdThisYear['gap'] = 'nan'
gaplist = list()
gaplist.append('nan')
indexThisYear = pdThisYear.index
for index in indexThisYear[1:]:
    key = pdThisYear.iloc[index]['name']
    if key == pdThisYear.iloc[index - 1]['name']:
        d1 = datetime.strptime(pdThisYear.iloc[index]['date'],'%Y-%m-%d')
        d0 = datetime.strptime(pdThisYear.iloc[index - 1]['date'],'%Y-%m-%d')
        gap = (d1 - d0).days     
        gaplist.append(gap)
    else:
        if dictLastYear.has_key(key):
            gap = (datetime.strptime(pdThisYear.iloc[index]['date'], '%Y-%m-%d')- datetime.strptime(dictLastYear[key].tolist()[0], '%Y-%m-%d')).days
            gaplist.append(gap)
        else:
            gaplist.append(0)
        
gappd = pd.DataFrame(gaplist)
pdThisYear.gap=gappd

pdThisYearWithIndustry = pdThisYear.join(pdraw.set_index('name'), how='left', on='name')
pdThisYearWithIndustry = pdThisYearWithIndustry.join(dfpe.set_index('name'), how='left', on='name')
pdThisYearWithIndustry.sort_values(["industry", "pe", "count"], ascending=True).reset_index().to_csv(filterpdSplitSortNameThisYearWithGap)
pdThisYearWithIndustry.sort_values(["date", "industry", "pe"], ascending=False).reset_index().to_csv(filterpdSplitSortDateThisYearWithGap)
commands.getstatusoutput("iconv -f utf-8 -t GBK ./resources/daily/filterpdSplitSortNameWithGap.csv > ./resources/daily/filterpdSplitSortNameWithGap.txt")
pdfilterpdSplitSortDateThisYearWithGapCount1 = pdThisYearWithIndustry[pdThisYearWithIndustry['count'] ==1]
pdfilterpdSplitSortDateThisYearWithGapCount1 = pdfilterpdSplitSortDateThisYearWithGapCount1[pdfilterpdSplitSortDateThisYearWithGapCount1['rocket'] != '--']
pdfilterpdSplitSortDateThisYearWithGapCount1.sort_values(["date"], ascending=True).reset_index().to_csv(filterpdSplitSortDateThisYearWithGapCount1)
csv_to_xls(filterpdSplitSortNameThisYearWithGap)
csv_to_xls(filterpdSplitSortDateThisYearWithGap)
csv_to_xls(filterpdSplitSortDateThisYearWithGapCount1)
