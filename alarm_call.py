#!/usr/bin/python

import shutil
import time
import MySQLdb
import base64
import os.path
import sys
import smtplib
from datetime import datetime
import gdata.data
import gdata.docs.data
import gdata.docs.client
import ConfigParser

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
	    self.send_email = 0
	    self.delete_after_upload = 1
	    self.message = ""
	    

	    
	    for row in phone_data:
#		print("%s" % row[0])
		phonenumber = "%s" % row[0]
		id = "%d" % row[1]
		t=str(time.time())
		if len(sys.argv) < 2:
		    self._write_call_file(phonenumber,id,t)

	    #this is wacked, I need to only grab one row here. fixit 
	    for row in acct_data:
	        #print("%s" % row[0])
		self.usrname = "%s" % row[0]
		self.password = "%s" % row[1]
                

            for row in email_data:
	        #print("%s" % row[0])
		self.recipient = "%s" % row[0]
		self.sender = "%s" % row[0]
		self.subject = "Teta's on the move"
		self.from_name = "Teta"
		image_path = ""
		msg = "You better check on her"
		#print("self.recipient is %s" % self.recipient)
		if len(sys.argv) < 2:
		    self._send_email(msg,image_path)
	    
	    if len(sys.argv) == 2:
		self._create_gdata_client()

	def _create_gdata_client(self):
            """Create a Documents List Client."""
            self.client = gdata.docs.client.DocsClient(source='motion_uploader')
            self.client.http_client.debug = False
            self.client.client_login(self.usrname, self.password, service=self.client.auth_service, source=self.client.source)

	def _get_folder_resource(self):
            """Find and return the resource whose title matches the given folder."""
	    self.folder = 'motion'
            col = None
            for resource in self.client.GetAllResources(uri='/feeds/default/private/full/-/folder'):
                if resource.title.text == self.folder:
                    col = resource
                    break    
            return col
	
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
	    imgfile = ""
	    encodedcontent = ""
            # Read a file and encode it into base64 format
	    if imgpath != "":
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
            server.login(self.usrname, self.password)
            # server.sendmail(self.sender, self.recipient, p1+p2+p3)
	    # change made here to not attach file so this can be sent to sms
	    if imgfile == "":
	    	server.sendmail(self.sender, self.recipient, p1+p2)
	    else:
		server.sendmail(self.sender, self.recipient, p1+p2+p3)
            server.quit()

	def _upload(self, video_file_path, folder_resource):
		'''Upload the video and return the doc'''
		doc = gdata.docs.data.Resource(type='video', title=os.path.basename(video_file_path))
		media = gdata.data.MediaSource()
		media.SetFileHandle(video_file_path, 'video/avi')
		doc = self.client.CreateResource(doc, media=media, collection=folder_resource)
		return doc
    
	def upload_video(self, video_file_path):
		"""Upload a video to the specified folder. Then optionally send an email and optionally delete the local file."""
		folder_resource = self._get_folder_resource()
		if not folder_resource:
		    raise Exception('Could not find the %s folder' % self.folder)

		doc = self._upload(video_file_path, folder_resource)
		
		              
		if self.send_email:
		    #print("sending email from upload_video: self.send_email is %s" % self.send_email)
		    video_link = None
		    for link in doc.link:
		        if 'video.google.com' in link.href:
		            video_link = link.href
		            break
		    # Send an email with the link if found
		    msg = self.message
		    if video_link:
		        msg += '\n\n' + video_link
		    imgfile = os.path.splitext(video_file_path)[0] + ".jpg"
		    self._send_email(msg,imgfile)
		    if self.delete_after_upload:
		        os.remove(imgfile)

		if self.delete_after_upload:
		    os.remove(video_file_path)
		    #print("in delete after upload block")


if __name__ == '__main__':         
    try:
	if len(sys.argv) == 2:
	    cfg_path = sys.argv[0]
	    vid_path = sys.argv[1]    
	    AlarmCall().upload_video(vid_path)
	else:
	    AlarmCall()      
    except gdata.client.BadAuthentication:
	exit('Invalid user credentials given.')
    except gdata.client.Error:
	exit('Login Error')
    except Exception as e:
	exit('Error: [%s]' % e)

