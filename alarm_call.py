#!/usr/bin/python

import shutil
import time
import MySQLdb

class AlarmCall:
	def __init__(self):
	    db = MySQLdb.connect("localhost","teta","tetacam","tetacam")
	    sql_phone = "select phone,userid from contacts where phoneactive=true"
            sql_acct = "select id,pw from accounts where active=true"
	    sql_email = "select email from contacts where emailactive=true"
	    cursor = db.cursor()
	    cursor.execute(sql_phone)
	    phone_data = cursor.fetchall()
	    cursor.execute(sql_acct)
            acct_data = cursor.fetchall()
            cursor.execute(sql_email)
            email_data = cursor.fetchall()
            db.close()

	    for row in phone_data:
#		print("%s" % row[0])
		phonenumber = "%s" % row[0]
		id = "%d" % row[1]
		t=str(time.time())
		self._write_call_file(phonenumber,id,t)
	   
	    for row in acct_data:
	        print("%s" % row[0])
		use_id = "%s" % row[0]
		passwd = "%s" % row[1]
		t=str(time.time())
		#self._write_call_file(phonenumber,id,t)

            for row in email_data:
	        print("%s" % row[0])
		use_id = "%s" % row[0]
		t=str(time.time())
		#self._write_call_file(phonenumber,id,t)


	
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

	def _send_email(self,msg,imgpath):
            senddate=datetime.strftime(datetime.now(), '%Y-%m-%d')
            # Read a file and encode it into base64 format
            fo = open(imgpath, "rb")
            filecontent = fo.read()
            encodedcontent = base64.b64encode(filecontent)  # base64
            imgfile=os.path.basename(imgpath)
            marker = "AUNIQUEMARKER"
            p1="Date: %s\r\nFrom: %s <%s>\r\nTo: %s\r\nSubject: %s\r\nContent-Type: multipart/mixed; boundary=%s\r\n--%s\r\n" % (senddate, self.from_name, self.sender, self.recipient, self.subject, marker, marker)
            p2="Content-Type: text/plain\r\nContent-Transfer-Encoding:8bit\r\n\r\n%s\r\n--%s\r\n" % (msg, marker)
            p3="Content-Type: multipart/mixed; name=""%s""\r\nContent-Transfer-Encoding:base64\r\nContent-Disposition: attachment; filename=%s\r\n\r\n%s\r\n--%s--\r\n" % (imgfile, imgfile, encodedcontent, marker)

            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(self.username, self.password)
            # server.sendmail(self.sender, self.recipient, p1+p2+p3)
	    # change made here to not attach file so this can be sent to sms
	    server.sendmail(self.sender, self.recipient, p1+p2)
            server.quit()


try:   
    AlarmCall()
except Exception as e:
        exit('Error: [%s]' % e)




#import sys

#print "\n".join(sys.argv)
