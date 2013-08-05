import csv
import requests
import os
import MySQLdb as mdb
import datetime as dat
import time as time
date = dat.date
timep = dat.timedelta

#SQL connections stuff
db = mdb.connect(host='localhost',user = 'root',passwd='nomnomnom',db="Stocks")
cur = db.cursor()

def urldata(ticker):
    url = 'http://ichart.yahoo.com/table.csv?s='
    enddateyear = str(date.today().year)
    enddateday = str(date.today().day)
    enddatemonth = str((date.today().month)-1)
    s5year = timep(weeks=520)
    startdateyear = str((date.today()-s5year).year)
    startdatemonth = str(((date.today()-s5year).month)-1)
    startdateday = str((date.today()-s5year).day)
    url += "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%sg=%s&ignore=.csv" % (ticker,startdatemonth,startdateday,startdateyear,enddatemonth,enddateday,enddateyear,'d')
    try:
        r = requests.get(url)
        c = open('table.csv','wb')
        c.write(r.content)
        c.close
    except:
        print "download went wrong"
    sizeinfo = os.stat('table.csv')
    if sizeinfo.st_size == 0:
        print ticker," something went wrong check your parameters and i'll try again"
        return
    else:
        try:
            create = "Create Table " + ticker + " (Date DATE,Open DECIMAL(10,2),High DECIMAL(10,2),Low DECIMAL(10,2),Close DECIMAL(10,2),Volume BIGINT,Adj DECIMAL(10,2));"
            cur.execute(create)
        except:
            drop = "Drop table " + ticker + ";"
            cur.execute(drop)
            create = "Create Table " + ticker + " (Date DATE,Open DECIMAL(10,2),High DECIMAL(10,2),Low DECIMAL(10,2),Close DECIMAL(10,2),Volume BIGINT,Adj DECIMAL(10,2));"
            cur.execute(create)
        csv = "LOAD DATA LOCAL INFILE 'table.csv'\n"
        csv += "INTO TABLE " + ticker + "\n"
        csv += "FIELDS TERMINATED BY ','\n"
        csv += "lines terminated by '\n'\n"
        csv += "IGNORE 1 LINES\n"
        csv += "(Date,Open,High,Low,Close,Volume,Adj);"
#csv += "SET Date = STR_TO_DATE(Date,'%Y-%m-%d');"
        cur.execute(csv)
        csv = "Update " + ticker + " set Close = Adj where Adj <> Close;"
        cur.execute(csv)
        csv = "Alter table " + ticker + " drop column Adj;"
        cur.execute(csv)
        print ticker," is in table"
    	db.commit()
    	return "committed"
    	
def startmain():
    pathck = os.getcwd()
    print pathck
    stock = open('/Users/Cookie/Programming/DataGrab/StockSymbolsandNames.csv','rU')
    stocks = csv.reader(stock)
    data = []
    for a in stocks:
        data.append(a[0])
    count = len(data)
    print data
    for a in data:
        check = urldata(a)
        if check == "committed":
            continue
        else:
            print "------------------------------"
            continue

startmain()
		