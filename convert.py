from PIL import Image
import glob, os
import md5

onlyfiles = [ f for f in os.listdir(".") if not ".py" in f ]
print onlyfiles

for file in onlyfiles:
	print "Converting...",file 
	m = md5.new()
	size = os.path.getsize(file)
	m.update(str(size))
	im = Image.open(file).convert("RGB")
	im.save(m.hexdigest() + ".jpg", "JPEG")
	print "saved as " +m.hexdigest() + ".jpg"
	os.remove(file)