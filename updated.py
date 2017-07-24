from socket import *
import time 
import json
from cStringIO import StringIO
import simplejson
import smtplib

# ONLY MODIFY THESE ----------------------------
SEASON = "In+The+Zone"			#manualy generate mailing list from VexForum
REGION = "California" 			#cron job w/ cmd line input
GMAIL = "postmaster.smash@gmail.com"
PASSWORD = "[redacted]"
RECIPIENT = "niwhsa9@gmail.com"
TOURNAMENT_FILE = "tournaments.log" 
RECIPIENT_FILE = "maillist.log"
# DON'T MODIFY HERE DOWN- ----------------------

s = socket(AF_INET, SOCK_STREAM)
s.connect(("api.vexdb.io", 80))
t = """GET http://api.vexdb.io/v1/get_events?region={region}&season={season} HTTP/1.1
Host: api.vexdb.io

""".format(region=REGION, season=SEASON)
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


file = open(TOURNAMENT_FILE, "a+")
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
	server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(GMAIL, PASSWORD)
	
	file = open(RECIPIENT_FILE, "r")
	list = file.read().split("\n")
	#print(list)
	#REGION.replace(' ', '_')
	for user in list:
		if(REGION not in user):
			print(user)
			continue
		RECIPIENT = user.split(" ")[1]
		readable = [
        		"From: " + GMAIL,
       			"To: " + RECIPIENT,
        		"Subject: New Tournaments!",
        		"",
		] #optimize, don't generate a new msg every time

		for i in newtournaments:
			readable.append(name[i] + " " + date[i] + " " + loc[i]);

		msg = "\r\n".join(readable)
		#print(msg)
		#server.sendmail(GMAIL, RECIPIENT, msg)
	
