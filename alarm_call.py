#!/usr/bin/python

import shutil
import time
import MySQLdb

class AlarmCall:
	def __init__(self):
	    db = MySQLdb.connect("localhost","teta","tetacam","tetacam")
	    sql = "select phone,userid from contacts where phoneactive=true"
	    cursor = db.cursor()
	    cursor.execute(sql)
	    data = cursor.fetchall()
	    db.close()

	    for row in data:
#		print("%s" % row[0])
		phonenumber = "%s" % row[0]
		id = "%d" % row[1]
		t=str(time.time())
		self._write_call_file(phonenumber,id,t)

	def _write_call_file(self,phonenumber,id,t):
	#write and move a file for asterisk to pick up to call out with
		f=open("/tmp/alarm-" + t + id, "w")
		f.write("Channel: Local/1" + phonenumber + "@outbound-allroutes\n")
		f.write("Callerid: tetacam\n")
		f.write("MaxRetries: 3\n")
		f.write("RetryTime: 30\n")
		f.write("WaitTime: 20\n")
		f.write("Context: motion-alarm\n")
		f.write("Extension: s\n")
		f.write("Priority: 1\n")
		f.close()
		shutil.move(f.name, '/var/spool/asterisk/outgoing/')
#		print("moving %s" % phonenumber)


try:   
    AlarmCall()
except Exception as e:
        exit('Error: [%s]' % e)




#import sys

#print "\n".join(sys.argv)
