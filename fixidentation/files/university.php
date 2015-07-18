<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class University extends CI_Model {

    function __construct()
    {
        // Call the Model constructor
        parent::__construct();
    }
    
	function get_all_university()
	{
        $query = $this->db->get("tbl_university");
		return $query->result_array();
	}
	
	function get_careers_from_university($university_id)
	{
		$conditions = array('university_id' => $university_id);
		$query = $this->db->get_where('tbl_careers', $conditions);
		return $query->result_array();
	}
	
}