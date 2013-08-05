import csv
import sys
import requests
from time import sleep

def urlcreate(id):
	url = "http://biz.yahoo.com/p/csv/"
	url += str(id)
	url += "conameu.csv"
	r = requests.get(url)
	if r.status_code == 404:
		print str(id)," doesn't work"
		return None
	print str(id)," works---------------------------------"
	idlist = open("/Volumes/Macintosh HD/Users/Cookie/Programming/DataGrab/IndustryID.csv","a+")
	table = open("/Volumes/Macintosh HD/Users/Cookie/Programming/DataGrab/test.csv","wb")
	table.write(r.content)
	table.close()
	tables = open("/Volumes/Macintosh HD/Users/Cookie/Programming/DataGrab/test.csv","rb")
	for c in tables:
		a = c.replace('\x00', '').split(";")
		print a
		idlist.write(a)
		idlist.write("\n")
	table.close()
	idlist.close()
	return
		
def idrange():
	start = int(raw_input("Start number? "))
	end = int(raw_input("End number? "))
	idlist = open("/Volumes/Macintosh HD/Users/Cookie/Programming/DataGrab/IndustryID.csv","w")
	idlist.close()
	for i in range(start,end):
		print i 
		urlcreate(i)
			
idrange()