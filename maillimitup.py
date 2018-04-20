#!/usr/bin/env python2
# -*- coding: utf-8 -*-


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

# prepare basic info
import tushare as ts

baseinfoFileName='baseinfo20180415.csv'
lowerBoundNmc = 80
upperBoundNmc = 260

import tushare as ts

todayAll = ts.get_today_all()
todayAllLimitUp = todayAll[todayAll['changepercent'] > 9.6]
print "完成数据更新"
baseInfo = pd.read_csv(baseinfoFileName, encoding='gbk')
todayAllLimitUpWithBaseInfo = todayAllLimitUp.merge(baseInfo)
todayAllLimitUpWithBaseInfo.nmc = todayAllLimitUpWithBaseInfo.nmc.apply(lambda x: round(x/10000, 1))
todayAllLimitUpWithBaseInfoSimple = todayAllLimitUpWithBaseInfo[['code', 'name', 'nmc', 'industory', 'city']]
todayAllLimitUpWithBaseInfoSimpleSortIndustory = todayAllLimitUpWithBaseInfoSimple.sort_values('industory').reindex()
todayAllLimitUpWithBaseInfoSimpleSortCity = todayAllLimitUpWithBaseInfoSimple.sort_values('city').reindex()
todayAllLimitUpWithBaseInfoSimpleSlice = todayAllLimitUpWithBaseInfoSimple.query('nmc > %s' % (lowerBoundNmc))

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
    
def saveTraductionPic(code):
    if code[0] == '6':
        url = 'https://xueqiu.com/S/sh%s' % code
    else:
        url = 'https://xueqiu.com/S/sz%s' % code
        
    xPath1Day = '//*[@id="app"]/div[2]/div[2]/div[6]/div[1]/div[1]/ul[1]/li[1]'
    global brower
    brower.get(url)
    brower.maximize_window()
    time.sleep(3)
    brower.find_element_by_xpath(xPath1Day).click()
    time.sleep(3)
    brower.save_screenshot('./tpics/%s.jpg' % code)
    time.sleep(3)
    cutPic('./tpics/%s.jpg' % code)
    print "got Traduction line pic %s" % code
    
    
linkString=""
baseUrl = "https://xueqiu.com/S/"
baseGdrsUrl = "http://stock.jrj.com.cn/share,%s,gdhs.shtml"
zjBaseUrl = "http://vip.stock.finance.sina.com.cn/moneyflow/#!ssfx!"
zjbdUrl = "http://vip.stock.finance.sina.com.cn/moneyflow/#zljlrepm"
nameString = ""

todayStr = str(datetime.today())[:10]
savePic(zjbdUrl, 'zjbd-%s' % todayStr)
codeList = []

print todayAllLimitUpWithBaseInfoSimpleSortIndustory
print todayAllLimitUpWithBaseInfoSimpleSortCity
print todayAllLimitUpWithBaseInfoSimpleSlice

reload(sys)
sys.setdefaultencoding('utf-8')

for line in todayAllLimitUpWithBaseInfoSimpleSlice.name.tolist():
    try:
        nameString += line + ','
        code = str(todayAllLimitUpWithBaseInfoSimpleSlice[todayAllLimitUpWithBaseInfoSimpleSlice['name']==line]['code'].get_values()[0]).zfill(6)
        codeList.append(code)
        saveGdrsPic(code)
        saveKPic(code)
        saveTraductionPic(code)
        print 'code: ' + code
        print code[0]
        
        if code[0] == '6':
            print 'in if 6'
            linkString += line + ": " + '<a href=" '+ baseUrl + "sh" + code + '">' + 'K线</a>' + "&nbsp"  
            linkString += '<a href=" ' + zjBaseUrl + "sh" + code + '">' + '主力净流入</a>' + "&nbsp"
        else:
            linkString += line + ": " + '<a href=" '+ baseUrl + "sz" + code + '">' + 'K线</a>' + "&nbsp"  
            linkString += '<a href=" ' + zjBaseUrl + "sz" + code + '">' + '主力净流入</a>' + "&nbsp"
        linkString += '<a href=" ' + baseGdrsUrl % code + '">' + '股东人数</a>'+ "<br/>"
        linkString += '<br><img src="cid:image-%s"></br>' % code
        linkString += '<br><img src="cid:kline-%s"></br></br></br>' % code
        linkString += '<br><img src="cid:Tline-%s"></br></br></br>' % code
    except:
        print 'exception'
        pass

linesOftodayAllLimitUpWithBaseInfoSimpleSortIndustory = ''
for i in range(len(todayAllLimitUpWithBaseInfoSimpleSortIndustory)):
    linesOftodayAllLimitUpWithBaseInfoSimpleSortIndustory += todayAllLimitUpWithBaseInfoSimpleSortIndustory.iloc[i].to_string() + '<br/>'
linesOftodayAllLimitUpWithBaseInfoSimpleSortIndustory = \
    linesOftodayAllLimitUpWithBaseInfoSimpleSortIndustory.replace('code', '').replace('name', '').replace('nmc', '').replace('industory', '').replace('city', '').replace(' ', '\t\t\t')
    
linesOftodayAllLimitUpWithBaseInfoSimpleSortCity = ''
for i in range(len(todayAllLimitUpWithBaseInfoSimpleSortCity)):
    linesOftodayAllLimitUpWithBaseInfoSimpleSortCity += todayAllLimitUpWithBaseInfoSimpleSortCity.iloc[i].to_string() + '<br/>'
linesOftodayAllLimitUpWithBaseInfoSimpleSortCity = \
    linesOftodayAllLimitUpWithBaseInfoSimpleSortCity.replace('code', '').replace('name', '').replace('nmc', '').replace('industory', '').replace('city', '').replace(' ', '\t\t\t')

#添加附件发送/
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
    me="stocks go"+"<"+mail_user+"@"+mail_postfix+">"
    message = MIMEMultipart()
    message['From'] = me
    message['To'] =  ";".join(to_list)
    subject = '短线选股'
    message['Subject'] = sub

    #邮件正文内容
    #1.http://finance.china.com.cn/stock/quote/sh600499
    #2.http://stock.jrj.com.cn/share,002247,gdhs.shtml
    #3.http://vip.stock.finance.sina.com.cn/moneyflow/#!ssfx!sz000725
    messageContent = '''
行业板块效应整理榜单<br/>
股票代码 股票名称 流通市值 所属行业 地区<br/>
%s<br/>
<br/>
地区板块效应整理榜单<br/>
股票代码 股票名称 流通市值 所属行业 地区<br/>
%s<br/>
说明：
此为短线选股名单，在股市下跌后的反弹中或企稳趋势中，及时判断跟进拉升牛股在短期内获利。
同时也能够发现有中线潜力的牛股<br/>
<br/>

<a href="http://finance.china.com.cn/stock/quote/sh000001/">上证指数</a><br/>
<a href="http://finance.china.com.cn/stock/quote/sh000001/">行业研究:</a>
<a href="http://app.finance.china.com.cn/report/list.php?type=1003">中国财经网</a>
<a href="http://data.eastmoney.com/report/hyyb.html">东方财富网</a>
<a href="http://stock.jrj.com.cn/yanbao/yanbaolist_hangye.shtml?dateInterval=30&orgCode=-1&xcfCode=-1">金融界</a>
<br/>
<a href="http://vip.stock.finance.sina.com.cn/moneyflow/#zljlrepm">资金榜单</a>
<br><img src="cid:image-zjbd"></br>'
<br/>''' % (linesOftodayAllLimitUpWithBaseInfoSimpleSortIndustory, linesOftodayAllLimitUpWithBaseInfoSimpleSortCity)

    #message.attach(MIMEText(messageContent, 'plain', 'utf-8'))
    
    html =  """
    <html> 
      <head>今日异动个股：</head> 
      <body> 
        <p>
           %s
        </p>
        <p>
        以下个股为精选牛股，需要结合技术面自行判断买入时机
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
        
    attzjbd = buildImageAtt("/data/codes/stoker/pics/zjbd-%s.png" % todayStr, "image-zjbd")
    message.attach(attzjbd)
    
    for codeitem in codeList:
        try:
            #att = buildAtt("/data/codes/stoker/pics/%s.jpg" % codeitem, "%s.jpg" % codeitem)
            att = buildImageAtt("/data/codes/stoker/pics/%s.jpg" % codeitem, "image-%s" % codeitem)
            attkline = buildImageAtt("/data/codes/stoker/kpics/%s.jpg" % codeitem, "kline-%s" % codeitem)
            attTline = buildImageAtt("/data/codes/stoker/tpics/%s.jpg" % codeitem, "Tline-%s" % codeitem)
            message.attach(att)
            message.attach(attkline)
            message.attach(attTline)
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
    if send_mail(mailto_list,todayStr + nameString):  #邮件主题和邮件内容
        print "done!"
    else:
        print "failed!"
        
brower.close()

