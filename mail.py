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
from selenium import webdriver
import time
from datetime import datetime
#exit()
#score.csv-->score.txt(today-sort.txt),score1.csv,(score.txt*)
#score1.csv-->score1-today.xls*
#all.csv-->all-today.xls*

#添加附件发送/
alltodaypd = pd.read_csv("/data/codes/stoker/resources/daily/score.csv")
dfpe = pd.read_csv('/data/codes/stoker/resources/daily/dfpe.csv')
todayScorepd = alltodaypd[alltodaypd.columns[-3:]]
todayColumn = todayScorepd.columns[0]
todayScorepd = todayScorepd.sort_values(by=todayColumn, ascending=True).reset_index()
todayScoreNewpd = todayScorepd[[todayColumn, "name", "scoreToday"]]
todayScoreNewpd.index.name = todayColumn;
todayScoreNewpd.index= range(1,len(todayScoreNewpd.index) + 1)
del todayScoreNewpd[todayColumn]
todayScoreNewpd.to_csv("/data/codes/stoker/resources/daily/score.txt")
filterpdSplitSortDateWithGap = pd.read_csv("/data/codes/stoker/resources/daily/filterpdSplitSortDateWithGap.csv")
lines=filterpdSplitSortDateWithGap[filterpdSplitSortDateWithGap['date']==filterpdSplitSortDateWithGap['date'][0]]
linkString=""
#baseUrl = "http://finance.china.com.cn/stock/quote/"
baseUrl = "https://xueqiu.com/S/"
baseGdrsUrl = "http://stock.jrj.com.cn/share,%s,gdhs.shtml"
zjBaseUrl = "http://vip.stock.finance.sina.com.cn/moneyflow/#!ssfx!"
zjbdUrl = "http://vip.stock.finance.sina.com.cn/moneyflow/#zljlrepm"

nameString = ""
brower = webdriver.PhantomJS()

from PIL import Image
def cutPic(filename):
    im = Image.open(filename)
    # 图片的宽度和高度
    img_size = im.size
    print("图片宽度和高度分别是{}".format(img_size))
    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
    '''
    # 截取图片中一块宽和高都是250的
    x = 280
    y = 80
    w = 680
    h = 700
    region = im.crop((x, y, x+w, y+h))
    region.save(filename)


def saveGdrsPic(code):
    url = 'http://stock.jrj.com.cn/share,%s,gdhs.shtml' % code
    global brower
    brower.get(url)
    brower.maximize_window()
    time.sleep(3)
    brower.save_screenshot('./pics/%s.jpg' % code)
    print "got pic code %s" % code
    
def savePic(url, filename):
    global brower
    brower.get(url)
    brower.maximize_window()
    time.sleep(3)
    brower.save_screenshot('./pics/%s.png' % filename)
    print "got pic filename %s" % filename
    
    
def saveKPic(code):
    if code[0] == '6':
        url = 'https://xueqiu.com/S/sh%s' % code
    else:
        url = 'https://xueqiu.com/S/sz%s' % code
        
    xPath1Day = '//*[@id="app"]/div[2]/div[2]/div[6]/div[1]/div[1]/ul[1]/li[2]'
    global brower
    brower.get(url)
    brower.maximize_window()
    time.sleep(3)
    brower.find_element_by_xpath(xPath1Day).click()
    time.sleep(3)
    brower.save_screenshot('./kpics/%s.jpg' % code)
    time.sleep(3)
    cutPic('./kpics/%s.jpg' % code)
    print "got k line pic %s" % code
todayStr = str(datetime.today())[:10]
savePic(zjbdUrl, 'zjbd-%s' % todayStr)
codeList = []
for line in lines['name']:
    print line
    
for line in lines['name']:
    try:
        nameString += line + ','
        code = str(dfpe[dfpe['name']==line]['code'].get_values()[0]).zfill(6)
        codeList.append(code)
        saveGdrsPic(code)
        saveKPic(code)
        
        if code[0] == '6':
            linkString += line + ": " + '<a href=" '+ baseUrl + "sh" + code + '">' + 'K线</a>' + "&nbsp"  
            #linkString += zjBaseUrl + "sh" + code + "\r\n" 
            linkString += '<a href=" ' + zjBaseUrl + "sh" + code + '">' + '主力净流入</a>' + "&nbsp"
        else:
            #linkString += line + ": " + baseUrl + "sz" + code + "\r\n"
            linkString += line + ": " + '<a href=" '+ baseUrl + "sz" + code + '">' + 'K线</a>' + "&nbsp"  
            #linkString += zjBaseUrl + "sz" + code + "\r\n"
            linkString += '<a href=" ' + zjBaseUrl + "sz" + code + '">' + '主力净流入</a>' + "&nbsp"
        linkString += '<a href=" ' + baseGdrsUrl % code + '">' + '股东人数</a>'+ "<br/>"
        linkString += '<br><img src="cid:image-%s"></br>' % code
        linkString += '<br><img src="cid:kline-%s"></br></br></br>' % code
    except:
        pass


#print linkString

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
    print filename
    #excel_filename = str(filename.split(".")[0]) + "-today.xls"
    excel_filename = filename.split(".")[0] + "-today.xls"
    myexcel.save(excel_filename)
    return excel_filename

#csv_to_xls("/data/codes/stoker/resources/daily/all.csv")
#csv_to_xls("/data/codes/stoker/resources/daily/score1.csv")
csv_to_xls("/data/codes/stoker/resources/daily/score.txt")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
mailto_list=['184083376@qq.com', '379055439@qq.com', '270424167@qq.com']           #收件人(列表)
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址

with open('mailuser.txt', 'r') as file_to_read:
                while True:
                    line = file_to_read.readline()
                    if not line:
                        break
                        pass
                    (mail_user, mail_pass) = line.split(',')
                    
mail_postfix="postfix"
def send_mail(to_list,sub):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    message = MIMEMultipart()
    message['From'] = me
    message['To'] =  ";".join(to_list)
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = sub

    #邮件正文内容
    #1.http://finance.china.com.cn/stock/quote/sh600499
    #2.http://stock.jrj.com.cn/share,002247,gdhs.shtml
    #3.http://vip.stock.finance.sina.com.cn/moneyflow/#!ssfx!sz000725
    messageContent = '''
雪球趋势-今日榜单
说明：
当日下跌的个股须忽略<br/>
score-today-by-date.xls 包括所有拥有评分资格的个股的历史评分-按日期排名<br/>
score-today-by-name.xls 包括所有拥有评分资格的个股的历史评分-按名称排名 <br/>   
all-history-score.xls 包括所有个股的历史评分<br/>
score-today.xls 包括按成交额排名的今日个股评分
all-history-sort.xls 包括所有个股的历史成交额排名<br/><br/>
<a href="http://finance.china.com.cn/stock/quote/sh000001/">上证指数</a><br/>
<a href="http://finance.china.com.cn/stock/quote/sh000001/">行业研究:</a>
<a href="http://app.finance.china.com.cn/report/list.php?type=1003">中国财经网</a>
<a href="http://data.eastmoney.com/report/hyyb.html">东方财富网</a>
<a href="http://stock.jrj.com.cn/yanbao/yanbaolist_hangye.shtml?dateInterval=30&orgCode=-1&xcfCode=-1">金融界</a>
<br/>
<a href="http://vip.stock.finance.sina.com.cn/moneyflow/#zljlrepm">资金榜单</a>
<br><img src="cid:image-zjbd"></br>'
<br/>'''

    #message.attach(MIMEText(messageContent, 'plain', 'utf-8'))
    
    html =  """
    <html> 
      <head>今日异动个股：</head> 
      <body> 
        <p>
           %s
        </p>
        <p>
           %s 
        </p> 
      </body> 
    </html> 
    """ % (messageContent, linkString)
    
    htm = MIMEText(html,'html','utf-8') 
    message.attach(htm)
    
    def buildAtt(filename, showfilename):
        att = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att["Content-Disposition"] = 'attachment; filename=' + showfilename
        return att
    
    def buildImageAtt(filename, showfilename):
        print showfilename
        att = MIMEImage(open(filename, 'rb').read())
        att.add_header('Content-ID','<' + showfilename + '>')
        return att
    
    
    att1 = buildAtt("/data/codes/stoker/resources/daily/filterpdSplitSortDateWithGapCount1-today.xls", "Count1-till-today.xls")
    att2 = buildAtt("/data/codes/stoker/resources/daily/filterpdSplitSortDateWithGap-today.xls", "score-today-by-date.xls")
    att3 = buildAtt("/data/codes/stoker/resources/daily/filterpdSplitSortNameWithGap-today.xls", "score-today-by-name.xls")
    att4 = buildAtt("/data/codes/stoker/resources/daily/score1-today.xls", "all-history-score.xls")
    att5 = buildAtt("/data/codes/stoker/resources/daily/all-today.xls", "all-history-sort.xls")
    
    
    message.attach(att1)
    message.attach(att2)
    message.attach(att3)
    message.attach(att4)
    message.attach(att5)
    
    attzjbd = buildImageAtt("/data/codes/stoker/pics/zjbd-%s.png" % todayStr, "image-zjbd")
    message.attach(attzjbd)
    
    for codeitem in codeList:
        try:
            #att = buildAtt("/data/codes/stoker/pics/%s.jpg" % codeitem, "%s.jpg" % codeitem)
            att = buildImageAtt("/data/codes/stoker/pics/%s.jpg" % codeitem, "image-%s" % codeitem)
            attkline = buildImageAtt("/data/codes/stoker/kpics/%s.jpg" % codeitem, "kline-%s" % codeitem)
            message.attach(att)
            message.attach(attkline)
        except Exception:
            pass
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
    if send_mail(mailto_list,todayColumn[4:] + nameString):  #邮件主题和邮件内容
        print "done!"
    else:
        print "failed!"
        
brower.close()
#todayScoreText = todayScoreText.
#commands.getstatusoutput('/data/codes/stoker/resources/daily/sending.sh')
#os.popen('echo "This is with attach" | mail -s "subject" 184083376@qq.com -A /data/codes/stoker/resources/daily/score.txt')
