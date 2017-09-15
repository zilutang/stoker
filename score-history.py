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
#exit()
os.chdir("/data/codes/stoker")
print "hello"
allpd = pd.read_csv("./resources/daily/score.csv", index_col=0)
se1 = allpd.iloc[0]
allpdindex = allpd.index
for i in allpdindex[4:5]:
    lineDict = dict()
    line = allpd.iloc[i]
    j = len(line) - 3
    while j >= 0:
        if (line[j].astype(str) == 'nan' and line[j-1].astype(str) == 'nan' and line[j-2].astype(str) == 'nan'): 
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
        
        
        

