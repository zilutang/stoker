#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 09:40:13 2017

@author: tangzilu
1.generateBasic.py 生成基本数据文件
2.updateDaily.py 基于基本数据文件每天更新当天数据
3.scoring.py 对当天及前5天内更新过数据的个股进行打分
4.score-history.py 对个股历史数据进行打分
5.mail.py 将数据处理结果发邮件，并附带处理结果附件
"""

import commands
import pandas as pd
import os
import sys
import xlwt
import csv
import uuid
#exit()
#score.csv-->score.txt(today-sort.txt),score1.csv,(score.txt*)
#score1.csv-->score1-today.xls*
#all.csv-->all-today.xls*

#添加附件发送/
alltodaypd = pd.read_csv("/data/codes/stoker/resources/daily/score.csv")
todayScorepd = alltodaypd[alltodaypd.columns[-3:]]
todayColumn = todayScorepd.columns[0]
todayScorepd = todayScorepd.sort_values(by=todayColumn, ascending=True).reset_index()
todayScoreNewpd = todayScorepd[[todayColumn, "name", "scoreToday"]]
todayScoreNewpd.index.name = todayColumn;
todayScoreNewpd.index= range(1,len(todayScoreNewpd.index) + 1)
del todayScoreNewpd[todayColumn]
todayScoreNewpd.to_csv("/data/codes/stoker/resources/daily/score.txt")

reload(sys)
sys.setdefaultencoding('utf-8')
scorepd = pd.read_csv("/data/codes/stoker/resources/daily/score.csv")
scorepd = scorepd.sort_values(by=todayColumn, ascending=True).reset_index()
scorepd[scorepd.columns[2:]].to_csv("/data/codes/stoker/resources/daily/score1.csv")
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
csv_to_xls("/data/codes/stoker/resources/daily/score.txt")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
mailto_list=['184083376@qq.com']           #收件人(列表)
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址
mail_user="weiminghu1984@163.com"                           #用户名
mail_pass="uuru1gexnmima"                             #密码
mail_postfix="postfix"                     #邮箱的后缀
def send_mail(to_list,sub):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    message = MIMEMultipart()
    message['From'] = me
    message['To'] =  ";".join(to_list)
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = sub

    #邮件正文内容
    messageContent = '''
    雪球趋势-今日榜单
    说明：
        score-today-by-date.xls 包括所有拥有评分资格的个股的历史评分-按日期排名
        score-today-by-name.xls 包括所有拥有评分资格的个股的历史评分-按名称排名    
        all-history-score.xls 包括所有个股的历史评分
        score-today.xls 包括按成交额排名的今日个股评分
        all-history-sort.xls 包括所有个股的历史成交额排名
    '''
    message.attach(MIMEText(messageContent, 'plain', 'utf-8'))
    
    # 构造附件4，传送当前目录下的 test.txt 文件
    att4 = MIMEText(open("/data/codes/stoker/resources/daily/filterpdSplitSortDateWithGap-today.xls", 'rb').read(), 'base64', 'utf-8')
    att4["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att4["Content-Disposition"] = 'attachment; filename="score-today-by-date.xls"'
    message.attach(att4)
    
    # 构造附件5，传送当前目录下的 test.txt 文件
    att5 = MIMEText(open("/data/codes/stoker/resources/daily/filterpdSplitSortNameWithGap-today.xls", 'rb').read(), 'base64', 'utf-8')
    att5["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att5["Content-Disposition"] = 'attachment; filename="score-today-by-name.xls"'
    message.attach(att5)
    
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open("/data/codes/stoker/resources/daily/score1-today.xls", 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="all-history-score.xls"'
    message.attach(att1)
    
    # 构造附件2，传送当前目录下的 test.txt 文件
    att2 = MIMEText(open("/data/codes/stoker/resources/daily/score-today.xls", 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att2["Content-Disposition"] = 'attachment; filename="score-today.xls"'
    message.attach(att2)
    
    # 构造附件3，传送当前目录下的 test.txt 文件
    att3 = MIMEText(open("/data/codes/stoker/resources/daily/all-today.xls", 'rb').read(), 'base64', 'utf-8')
    att3["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att3["Content-Disposition"] = 'attachment; filename="all-history-sort.xls"'
    message.attach(att3)

    

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me, to_list, message.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False
for i in range(1):                             #发送五封，不过会被拦截的。。。
    if send_mail(mailto_list,todayColumn + "-score-" + str(uuid.uuid4())):  #邮件主题和邮件内容
        print "done!"
    else:
        print "failed!"
#todayScoreText = todayScoreText.
#commands.getstatusoutput('/data/codes/stoker/resources/daily/sending.sh')
#os.popen('echo "This is with attach" | mail -s "subject" 184083376@qq.com -A /data/codes/stoker/resources/daily/score.txt')