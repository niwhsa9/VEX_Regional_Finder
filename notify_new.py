from socket import *
import time 
import json
from cStringIO import StringIO
import simplejson
import smtplib
import sys
# ONLY MODIFY THESE ----------------------------
SEASON = "current"			#manualy generate mailing list from VexForum
REGION = sys.argv[1] 			#cron job w/ cmd line input
GMAIL = "postmaster.smash@gmail.com"
PASSWORD = "[redacted]"
RECIPIENT = "niwhsa9@gmail.com"
TOURNAMENT_FILE = "tournaments.log" 
RECIPIENT_FILE = "maillist.log"
COUNTRY = "United+States"
# DON'T MODIFY HERE DOWN- ----------------------
#print(REGION)
s = socket(AF_INET, SOCK_STREAM)
s.connect(("api.vexdb.io", 80))
t = """GET http://api.vexdb.io/v1/get_events?region={region}&season={season} HTTP/1.1\r\nHost: api.vexdb.io\r\n\r\n
""".format(region=REGION, season=SEASON)
if(REGION == "Puerto+Rico" or REGION == "United+Kingdom"):  #TEMPORARY, FIX ME
	t = '''GET http://api.vexdb.io/v1/get_events?country={region}&season={season} HTTP/1.1\r\nHost: api.vexdb.io\r\n\r\n
'''.format(region=REGION, season=SEASON)
#print(t)
#print(len(t))	
response = ""
stime=time.time()
s.setblocking(0)
s.send(t)
while(True):
	if(time.time()-stime >= 0.5):
        	break
	try:
		t=s.recv(1024)
		response+=t

	except:
		pass
nohead=response[response.find('{'):response.rfind('}')+1]
#print(response)
#if(REGION == "Puerto+Rico"):
	#print(nohead)
print(REGION)
data = json.loads(nohead)
name=[]
date=[]
loc=[]
sku=[]
for i in range(0, len(data["result"])):	
	name.append(data["result"][i]["name"])
	date.append(data["result"][i]["start"]) 
	loc.append(data["result"][i]["loc_city"])
	sku.append(data["result"][i]["sku"]) #latest

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
	print(list)
	#REGION.replace(' ', '_')
	for user in list:
		if(REGION not in user):
			#print(user)
			continue
		RECIPIENT = user.split(" ")[1]
		readable = [
        		"From: " + GMAIL,
       			"To: " + RECIPIENT,
        		"Subject: New Tournaments!",
        		"",
		] #optimize, don't generate a new msg every time

		for i in newtournaments:
			readable.append(name[i] + " " + date[i] + " " + loc[i] + "\nhttps://www.robotevents.com/robot-competitions/vex-robotics-competition/" + sku[i] + ".html\n");

		msg = "\r\n".join(readable) #"\r\n"
		#print(msg)
		server.sendmail(GMAIL, RECIPIENT, msg)
	
