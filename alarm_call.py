#!/usr/bin/python

import shutil
import time
import MySQLdb

db = MySQLdb.connect("localhost","teta","tetacam","tetacam")
sql = "select phone,userid from contacts where phoneactive=true"

cursor = db.cursor()

try:
	cursor.execute(sql)

	data = cursor.fetchall()

	for row in data:
#		print("%s" % row[0])
		phonenumber = "%s" % row[0]
		id = "%d" % row[1]
		t=str(time.time())
		f=open("/tmp/alarm-" + t + id, "w")
		f.write("Channel: Local/1" + phonenumber + "@outbound-allroutes\n")
		f.write("Callerid: tetacam\n")
		f.write("MaxRetries: 3\n")
		f.write("RetryTime: 10\n")
		f.write("WaitTime: 30\n")
		f.write("Context: motion-alarm\n")
		f.write("Extension: s\n")
		f.write("Priority: 1\n")
		f.close()
		shutil.move(f.name, '/var/spool/asterisk/outgoing/')
#		print("moving %s" % phonenumber)
except:
	print("Unable to fetch data")

db.close()



#import sys

#print "\n".join(sys.argv)
