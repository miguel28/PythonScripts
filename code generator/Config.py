from switch import *
import json
import os.path

class TableConfig:
	className = ""
	table = ""
	fileName = ""
	columns = []
	specialFunctions = []
	
	def __init__(self, tableName):
		self.table = tableName
		self.fileName = "settings/" + self.table + ".json"
		self.ReadFile();
		
	def ReadFile(self):
		if os.path.isfile(self.fileName): 
			text = ""
			with open(self.fileName, "rb") as myfile:
				text = myfile.read()
			
			dicti = json.loads(text)
			self.className = dicti["class"]
			self.specialFunctions = dicti["special"]
		
	def WriteFile(self):
		toJson = { "class" : self.className, "special":  self.specialFunctions }
		js = json.dumps(toJson)
		with open(self.fileName, "wb") as text_file:
			text_file.write(js)
			
	def SetFunctions(self):
		self.MainSelection();

		
	def PrintUsage(self):
		print "Set Special for " + self.table
		print "a = Add function"
		print "l = list functions"
		print "d = delete function"
		print "e = edit function"
		print "q = exit"
	
	def MainSelection(self):
		running = True
		while running:
			self.PrintUsage()
			selection = raw_input("Option: ") 
			while switch(selection):
				if case("a"):
					self.AddFunction()
					break
				if case("l"):
					self.PrintFunctions()
					break
				if case("d"):
					self.DeleteFunction()
					break	
				if case("e"):
					
					break
					
				if case("q"):
					running = False
					break
				
				#default
				break
			
	def PrintFunctions(self):
		for i in range(0, len(self.specialFunctions)):
			print i,":", self.specialFunctions[i]
		print ""
		
	def AddFunction(self):
		params = []
		name = raw_input("Function name: ")
		prtRow = raw_input("Print one row [0 , 1]: ")
		
		print "Columns"
		for i in range(0,len(self.columns)) :
			print "Col",i,"info:",self.columns[i]
		
		if len(name) > 0:
			while True:
				col = raw_input("param: ")
				if len(col) == 0: break
				else: params.append(self.columns[int(col)])
			
			d = {"name": name, "onlyRow": prtRow, "params": params}
			self.specialFunctions.append(d)
	
	def DeleteFunction(self):
		index = input("Delete index [0 - " + str(len(self.specialFunctions)) + "]")
		if index < len(self.specialFunctions) and index >= 0:
			del self.specialFunctions[index]
		
	
	