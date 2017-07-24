import os 
FILE = "maillist.log"
file = open(FILE, 'r')
list = file.read().split('\n')
region = []
for e in list:
	if(e == '' or  e == ' '):
		continue 
	region.append(e.split(' ')[0])
print(region)	
for r in region:
	cmd  = "python notify.py " + r 
	#print(cmd)
	os.system(cmd)
