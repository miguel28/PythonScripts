import os, time, datetime
files = os.listdir(".")
print files

if not os.path.exists("old"):
	os.mkdir("old")

for file in files:
	t = os.path.getctime(file)
	modified_date = datetime.datetime.fromtimestamp(t)
	if modified_date.month < 6 :
		print "moved: %s" % time.ctime(t) + " File name " + file
		os.rename(file,"old/"+file)
	else:
		print "not moved: %s" % time.ctime(t) + " File name " + file