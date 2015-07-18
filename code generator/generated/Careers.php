class Careers extends CI_Model {

	public function __construct()
	{
		parent::__construct();
	}
	
	public function insertEntry($career_name, $career_type, $university_id)
	{
		$data = array(
			'career_id' => $career_id,
			'career_name' => $career_name,
			'career_type' => $career_type,
			'university_id' => $university_id
		);
		$this->db->insert('tbl_careers', $data);
		return $this->db->insert_id();
	}
	
	public function deleteEntry($career_id)
	{
		$this->db->where('career_id' $career_id );
		$this->db->delete('tbl_careers');
	}
	
	public function updateEntry($career_id, $career_name, $career_type, $university_id)
	{
		$data = array(
			'career_id' => $career_id,
			'career_name' => $career_name,
			'career_type' => $career_type,
			'university_id' => $university_id
		);
		$this->db->insert('tbl_careers', $data);
		return $this->db->insert_id();
	}
	
	public function getEntryById($career_id)
	{
		$conditions = array('career_id' => $career_id);
		$this->db->get_where('tbl_careers', $conditions);
		return $query->row();
	}
	
}

