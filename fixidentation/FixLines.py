from Strings import *

def FixIndentation(filePath,tab,width,clean):
	# Walk through all input lines
	text = []
	s = StringBuilder()
	with open(filePath, "rb") as myfile:
		text = myfile.read().splt("\n")
		
	for l in text:
	
		if tab:		
			i = 0
			while l[:width] == " " * width:		
				l = l[width:]
				i += 1
			l = "\t" * i + l
		else:
			i = 0
			while l[0] == "\t":
				l = l[1:]
				i += 1
			l = " " * i * width + l				
			
		if clean:
			l = l.rstrip(" \t\n") + "\n"

		s.append(l)
	
	with open(filePath, "wb") as text_file:
		text_file.write(s.__str__())




