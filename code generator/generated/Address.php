class Address extends CI_Model {

	public function __construct()
	{
		parent::__construct();
	}
	
	public function insertEntry($addr_direction, $addr_city, $addr_state, $addr_country, $addr_zipcode)
	{
		$data = array(
			'address_id' => $address_id,
			'addr_direction' => $addr_direction,
			'addr_city' => $addr_city,
			'addr_state' => $addr_state,
			'addr_country' => $addr_country,
			'addr_zipcode' => $addr_zipcode
		);
		$this->db->insert('tbl_address', $data);
		return $this->db->insert_id();
	}
	
	public function deleteEntry($address_id)
	{
		$this->db->where('address_id' $address_id );
		$this->db->delete('tbl_address');
	}
	
	public function updateEntry($address_id, $addr_direction, $addr_city, $addr_state, $addr_country, $addr_zipcode)
	{
		$data = array(
			'address_id' => $address_id,
			'addr_direction' => $addr_direction,
			'addr_city' => $addr_city,
			'addr_state' => $addr_state,
			'addr_country' => $addr_country,
			'addr_zipcode' => $addr_zipcode
		);
		$this->db->insert('tbl_address', $data);
		return $this->db->insert_id();
	}
	
	public function getEntryById($address_id)
	{
		$conditions = array('address_id' => $address_id);
		$this->db->get_where('tbl_address', $conditions);
		return $query->row();
	}
	
}

