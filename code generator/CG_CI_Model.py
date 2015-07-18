from Strings import *
from switch import *
from Config import * 

import MySQLdb


DB = 'empleos_test'
HOST = 'localhost'
USER = 'root'
PASS = ''

class CIModelGenerator:
	connection = None
	code = "";
	config = None

	def __init__(self):
		self.connection = MySQLdb.connect(
						host = HOST,
						user = USER,
						passwd = PASS)  # create the connection
		
	def Default(self):
		self.config = TableConfig("tbl_users")
		self.config.className = "Users"
		self.config.columns = self.QueryColumns(False)
		
	def renderMenu(self):
		print "1 = Print Tables"
		print "2 = Select Table"
		print "3 = Print Columns of Selected Table"
		print "4 = Set Class Name"
		print "5 = Set Special Functions"
		print "9 = Generate PHP file"
		print "0 = Exit"
		print ""
	
	def inputSelection(self):
		runing = True
		while runing:
			self.renderMenu()
			selection = input("Option: ") 

			while switch(selection):
				if case(1):
					self.QueryTables(True)
					break
				if case(2):
					self.SelectTable()
					break
				if case(3):
					self.QueryColumns(True)
					break	
				if case(4):
					self.SetClassName()
					break
					
				if case(5):
					self.PutFuntions()
					break

				
				if case(9):
					self.GenerateCode()
					self.PrintCode()
					self.WriteFile()
					break	
					
				if case(0):
					runing = False
					break
				
				#default
				break
			
	def QueryTables(self, printable):
		cursor = self.connection.cursor()     # get the cursor
		cursor.execute("USE " + DB) # select the database
		cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)
		tables = cursor.fetchall()       # return data from last query
		
		if printable:
			print "Tables Found:"
			for (table_name,) in cursor:
				print(table_name)
			print ""
		return tables
		
	def SelectTable(self):
		table = raw_input("Set Table Name: ")
		self.config = TableConfig(table)
		
	def QueryColumns(self,printable):
		cursor = self.connection.cursor()     # get the cursor
		cursor.execute("USE " + DB) # select the database
		cursor.execute("desc " + self.config.table )    # execute 'SHOW TABLES' (but data is not returned)
		columns = cursor.fetchall()
		cols = []
		for c in columns:
				cols.append(c[0])
		if printable:
			print cols
			print ""
		return cols
		
	def SetClassName(self):
		self.config.className = raw_input("Class Name: ")
	
	def PutFuntions(self):
		self.config.columns = self.QueryColumns(False)
		self.config.SetFunctions()
	
	def GenerateCode(self):
		self.config.WriteFile()
		
		s = StringBuilder()
		cols = self.QueryColumns(False)
		s.appendln("class " + self.config.className + " extends CI_Model {")
		
		s.appendln("")
		s.appendln("	public function __construct()")
		s.appendln("	{")
		s.appendln("		parent::__construct();")
		s.appendln("	}")
		s.appendln("	")
		
		#Append Insert Function
		s.append("	public function insertEntry(")
		
		for i in range(1,len(cols)-1): 
			s.append("$" + cols[i] + ", ")
		s.appendln("$" + cols[-1] + ")")
		s.appendln("	{")
		s.appendln("		$data = array(")
		
		for i in range(0,len(cols)-1): 
			s.appendln("			'" + cols[i] + "' => $" + cols[i] + ",")
		s.appendln("			'" + cols[-1] + "' => $" + cols[-1])
		
		s.appendln("		);")
		s.appendln("		$this->db->insert('" + self.config.table + "', $data);")
		s.appendln("		return $this->db->insert_id();")
		s.appendln("	}")
		s.appendln("	")
		
		#Append Delete Function
		s.append("	public function deleteEntry(")
		s.appendln("$" + cols[0] + ")")
		s.appendln("	{")
		s.appendln("		$this->db->where('" + cols[0] + "', $" +  cols[0] + " );")
		s.appendln("		$this->db->delete('" + self.config.table + "');")
		s.appendln("	}")
		s.appendln("	")
		
		#Append Update Function
		s.append("	public function updateEntry(")
		
		for i in range(0,len(cols)-1): 
			s.append("$" + cols[i] + ", ")
		s.appendln("$" + cols[-1] + ")")
		s.appendln("	{")
		s.appendln("		$data = array(")
		
		for i in range(0,len(cols)-1): 
			s.appendln("			'" + cols[i] + "' => $" + cols[i] + ",")
		s.appendln("			'" + cols[-1] + "' => $" + cols[-1])
		
		s.appendln("		);")
		s.appendln("		$this->db->insert('" + self.config.table + "', $data);")
		s.appendln("		return $this->db->insert_id();")
		s.appendln("	}")
		s.appendln("	")
		
		#Append Get Function
		s.append("	public function getEntryById(")
		s.appendln("$" + cols[0] + ")")
		s.appendln("	{")
		s.appendln("		$conditions = array('" + cols[0] + "' => $" + cols[0] + ");")
		s.appendln("		$this->db->get_where('" + self.config.table + "', $conditions);")
		s.appendln("		return $query->row();")
		s.appendln("	}")
		s.appendln("	")
		
		for function in self.config.specialFunctions:
			self.GenerateSpecial(s,function)
		
		s.appendln("}")
		s.appendln("")
		
		self.code = s
	
	def GenerateSpecial(self,s, function):
		funcs = function["params"]
		s.append("	public function " + function["name"] + "(")
		for i in range(0,len(funcs)-1): 
			s.append("$" + funcs[i] + ",")
		s.appendln("$" + funcs[-1] + ")")
		s.appendln("	{")
		s.appendln("		$conditions = array('");
		
		for i in range(0,len(funcs)-1): 
			s.appendln("			'" + funcs[i] + "' => $" + funcs[i] + ",")
		s.appendln("			'" + funcs[-1] + "' => $" + funcs[-1])
		s.appendln("		);");
		
		s.appendln("		$query = $this->db->get_where('" + self.config.table + "', $conditions);")
		if  function["onlyRow"] == "1":
			s.appendln("		return $query->row();")
		else:
			s.appendln("		return $query->result_array();")
		s.appendln("	}")
		s.appendln("	")

	
	def PrintCode(self):
		print self.code
		
	def WriteFile(self):
		with open("generated/" + self.config.className + ".php", "wb") as text_file:
			text_file.write(self.code.__str__())
	
gen = CIModelGenerator()
gen.Default()
gen.inputSelection()
	