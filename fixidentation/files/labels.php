<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Labels extends CI_Model {

    function __construct()
    {
        // Call the Model constructor
        parent::__construct();
    }
    
	function get_all_labels($lang)
	{
		$this->db->select('label_name,label_'.$lang);
        $query = $this->db->get("tbl_labels");
		return $query->result_array();
	}
}