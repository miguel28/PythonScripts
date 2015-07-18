from FixLines import *
import sys
import os.path

def FixFolder(folder,filetype,recursive):
	files = os.listdir(folder)
	for file in files:
		if os.path.isfile(file):
			extension = os.path.splitext(file)[1][1:]
			if extension == filetype:
				print "Processing File", file
				FixIndentation(file,True,4,True)
				
		elif os.path.isdir(file):
			print "Opening Sub Folder", file
			FixFolder(file,filetype,recursive)
				
if __name__ == "__main__":
	print "Runing Fix Identation Script"
	folder = sys.argv[1]
	filetype = sys.argv[2]
	recursive = len(sys.argv) == 3
	
	if len(sys.argv) < 3:
		print "Error too few arguments"
		exit()
	
	if os.path.isdir(folder):
		print "Opening Folder", folder
		FixFolder(folder,filetype,recursive)
	else:
		print "folder does not exist"