import os 
FILE = "maillist.log"
file = open(FILE, 'r')
lst = file.read().split('\n')
#lst = list(set(lst))
region = []
for e in lst:
	if(e == '' or  e == ' '):
		continue 
	region.append(e.split(' ')[0])
region = list(set(region))
print(region)	
for r in region:
	cmd  = "python notify.py " + r 
	#print(cmd)
	os.system(cmd)
