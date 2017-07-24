from socket import *
import time 
import json
from cStringIO import StringIO
import simplejson
import smtplib

s = socket(AF_INET, SOCK_STREAM)
s.connect(("api.vexdb.io", 80))
t = """GET http://api.vexdb.io/v1/get_events?region=California&season=In+The+Zone HTTP/1.1
Host: api.vexdb.io

"""
response = ""
stime=time.time()
s.setblocking(0)
s.send(t)
while(True):
	if(time.time()-stime >= 1.25):
        	break
	try:
		t=s.recv(1024)
		response+=t

	except:
		pass
nohead=response[response.find('{'):]
#print(nohead)
data = json.loads(nohead)
name=[]
date=[]
loc=[]
for i in range(0, len(data["result"])):	
	name.append(data["result"][i]["name"])
	date.append(data["result"][i]["start"]) 
	loc.append(data["result"][i]["loc_city"])

file = open("/var/u_out/prev_store", "a+")
prev = file.read().split("\r\n")
newtournaments = []
for n in range(0, len(name)):
	flag = False
	for line in prev:
		if(line == name[n]):
			 flag = True
	if(flag != True):
		newtournaments.append(n)
		file.write("\r\n"+name[n]);
file.close()

if(len(newtournaments)>0):
	readable = [
        	"From: postmaster.smash@gmail.com",
       		"To: ashwingupta2000@gmail.com",
        	"Subject: New Tourneys!",
        	"",
	]

	for i in newtournaments:
		readable.append(name[i] + " " + date[i] + " " + loc[i]);

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("postmaster.smash@gmail.com", "fakepassword") #fake password
	msg = "\r\n".join(readable)
	print(msg)

	server.sendmail("postmaster.smash@gmail.com", "ashwingupta2000@gmail.com", msg)

