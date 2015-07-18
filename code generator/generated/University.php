class University extends CI_Model {

	public function __construct()
	{
		parent::__construct();
	}
	
	public function insertEntry($university_name, $university_description, $university_address, $university_webpage, $university_email)
	{
		$data = array(
			'university_id' => $university_id,
			'university_name' => $university_name,
			'university_description' => $university_description,
			'university_address' => $university_address,
			'university_webpage' => $university_webpage,
			'university_email' => $university_email
		);
		$this->db->insert('tbl_university', $data);
		return $this->db->insert_id();
	}
	
	public function deleteEntry($university_id)
	{
		$this->db->where('university_id' $university_id );
		$this->db->delete('tbl_university');
	}
	
	public function updateEntry($university_id, $university_name, $university_description, $university_address, $university_webpage, $university_email)
	{
		$data = array(
			'university_id' => $university_id,
			'university_name' => $university_name,
			'university_description' => $university_description,
			'university_address' => $university_address,
			'university_webpage' => $university_webpage,
			'university_email' => $university_email
		);
		$this->db->insert('tbl_university', $data);
		return $this->db->insert_id();
	}
	
	public function getEntryById($university_id)
	{
		$conditions = array('university_id' => $university_id);
		$this->db->get_where('tbl_university', $conditions);
		return $query->row();
	}
	
}

