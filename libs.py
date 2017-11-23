#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 14:39:59 2017

@author: tangzilu
"""
import xlwt
import csv
import urllib2
import json
import pandas as pd

def csv_to_xls(filename):
    print "in libs"
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
    print filename
    myexcel.save(excel_filename)
    print excel_filename
    return excel_filename

#def getNetInputString(code='sh600123'):
'''    
def changeratio(x):
    #changeratio1 = repr(x['changeratio'])
    changeratio1 = x['changeratio'].encode('utf-8')
    return changeratio1
code='sh600123'
urlBase = r'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_qsfx_lscjfb?page=1&num=20&sort=opendate&asc=0&daima='
replacestr = lambda strbad: strbad.replace('{', '{\"').replace(':\"', '\":\"').replace(',', ',\"').replace('\"{', '{')
getdata = lambda stockid: urllib2.urlopen(urllib2.Request(urlBase+str(code))).read()
tmpresult = map(getdata, code)
mapedresult = map(replacestr,tmpresult)
jsonloadfun = lambda x: json.loads(x)
opendate=lambda x: x['opendate']
trade=lambda x: x['trade']
turnover=lambda x: x['turnover']
netamount=lambda x: x['netamount']
ratioamount=lambda x: x['ratioamount']
r0=lambda x: x['r0']
r1=lambda x: x['r1']
r2=lambda x: x['r2']
r3=lambda x: x['r3']
r0_net=lambda x: x['r0_net']
r1_net=lambda x: x['r1_net']
r2_net=lambda x: x['r2_net']
r3_net=lambda x: x['r3_net']
jsonloadfun = lambda x: json.loads(x)
print mapedresult
jsonresult = map(jsonloadfun, mapedresult)
frame = pd.DataFrame(jsonresult)
import string
s1 = frame.ix[0]
s1opendate = s1.apply(opendate)
s1trade = s1.apply(trade)
s1.apply(netamount)
frame.applymap(opendate)
frame.applymap(netamount)
frame.index=[code]
frame.columns=[s1opendate]
#frame.index.names = ['stockid', 'trade']
frame.columns.names = ['opendate']
frame1 = frame.applymap(netamount).applymap(string.atof).applymap(lambda x: x / 10 ** 4)

frametrade = frame.applymap(trade).applymap(string.atof)
frametrade.index=['trade']

frame_changeratio = frame.applymap(changeratio).applymap(string.atof).applymap(lambda x: x * 100)
frame_changeratio.index=['changeratio']

framer0_net = frame.applymap(r0_net).applymap(string.atof).applymap(lambda x: x / 10 ** 4)
framer0_net.index=['r0_net']

framer1_net = frame.applymap(r1_net).applymap(string.atof).applymap(lambda x: x / 10 ** 4)
framer1_net.index=['r1_net']

framer2_net = frame.applymap(r2_net).applymap(string.atof).applymap(lambda x: x / 10 ** 4)
framer2_net.index=['r2_net']

framer3_net = frame.applymap(r3_net).applymap(string.atof).applymap(lambda x: x / 10 ** 4)
framer3_net.index=['r3_net']

frame1 = frame1.append(frametrade).append(frame_changeratio).append(framer0_net).append(framer1_net).append(framer2_net).append(framer3_net)
frame1.head()
frame2 = frame1.T
frame2.head()
'''
    
#getNetInputString()