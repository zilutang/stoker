#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:40:13 2017

@author: tangzilu
"""

import commands
import pandas as pd
import os
#exit()
#发送文本信息
#commands.getstatusoutput('mail -s "testing message" 184083376@qq.com <<< "body from python"')
#添加附件发送/
alltodaypd = pd.read_csv("/data/codes/stoker/resources/daily/score.csv")
todayScorepd = alltodaypd[alltodaypd.columns[-3:]]
todayColumn = todayScorepd.columns[0]
todayScorepd = todayScorepd.sort_values(by=todayColumn, ascending=True).reset_index()
todayScoreNewpd = todayScorepd[[todayColumn, "name", "scoreToday"]]
todayScoreNewpd.to_csv("/data/codes/stoker/resources/daily/score.txt")
all = pd.read_csv("/data/codes/stoker/resources/daily/all.csv")
all.to_excel("/data/codes/stoker/resources/daily/alltoday.xlsx")
#todayScoreText = todayScoreText.
#commands.getstatusoutput('/data/codes/stoker/resources/daily/sending.sh')
#os.popen('echo "This is with attach" | mail -s "subject" 184083376@qq.com -A /data/codes/stoker/resources/daily/score.txt')