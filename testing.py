#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 09:40:18 2017

@author: tangzilu
"""

import tushare as ts
import pandas as pd
import time
import datetime
#record = ts.get_h_data('002337', start='2015-01-01', end='2015-03-16') 
#print record
exit()

'''----------date tool
beginDate = datetime.date.today() - datetime.timedelta(days=200)
endDate = datetime.date.today() - datetime.timedelta(days=2)
print beginDate, endDate
'''

'''---------stock List tool
stocks = ts.get_stock_basics()
print stocks['name']
print stocks.index
index = stocks.index.values
print index
'''
'''
import os
for i in os.listdir("./resources/data/stocksHis/"):
    print str(i)[:-4]
    time.sleep(3)
    '''
'''
    
#exit()
import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
sender = '184083376@qq.com'
receivers = ['184083376@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
 
try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "邮件发送成功"
except smtplib.SMTPException:
    print "Error: 无法发送邮件"
'''
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
mailto_list=['184083376@qq.com']           #收件人(列表)
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址
mail_user="weiminghu1984@163.com"                           #用户名
mail_pass="uuru1gexnmima"                             #密码
mail_postfix="postfix"                     #邮箱的后缀
def send_mail(to_list,sub,content):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    message = MIMEMultipart()
    message['From'] = me
    message['To'] =  ";".join(to_list)
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = sub

    #邮件正文内容
    #message.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', subtype='plain'))
    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open("/data/codes/stoker/resources/daily/score1-today.xls", 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="score1-today.xls"'
    message.attach(att1)

    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)                #将收件人列表以‘；’分隔
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
    if send_mail(mailto_list,"hello","haha!"):  #邮件主题和邮件内容
        print "done!"
    else:
        print "failed!"
'''