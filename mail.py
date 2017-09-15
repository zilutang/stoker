#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:40:13 2017

@author: tangzilu
"""

import commands
import pandas as pd
import os
import sys
import xlwt
import csv
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

reload(sys)
sys.setdefaultencoding('utf-8')
scorepd = pd.read_csv("/data/codes/stoker/resources/daily/score.csv")
scorepd = scorepd.sort_values(by=todayColumn, ascending=True).reset_index()
scorepd.to_csv("/data/codes/stoker/resources/daily/score1.csv")
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
    return excel_filename

csv_to_xls("/data/codes/stoker/resources/daily/all.csv")
csv_to_xls("/data/codes/stoker/resources/daily/score1.csv")
'''
all = pd.read_csv("/data/codes/stoker/resources/daily/all.csv")
all.to_excel("/data/codes/stoker/resources/daily/alltoday.xlsx", encoding='utf-8')

scorepd = pd.read_csv("/data/codes/stoker/resources/daily/score.csv")
scorepd = scorepd.sort_values(by=todayColumn, ascending=True).reset_index()
scorepd.to_excel("/data/codes/stoker/resources/daily/score.xlsx", encoding='utf-8')
'''
#todayScoreText = todayScoreText.
#commands.getstatusoutput('/data/codes/stoker/resources/daily/sending.sh')
#os.popen('echo "This is with attach" | mail -s "subject" 184083376@qq.com -A /data/codes/stoker/resources/daily/score.txt')