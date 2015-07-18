<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class News_mdl extends CI_Model {

	function getNewsRange($from, $to)
	{
		/*$conditions = array('user_email' => $email);
		$query = $this->db->get_where('tbl_users', $conditions);
		return $query->result_array();*/
	}
	function getTotalNews()
	{
		/*$conditions = array('user_email' => $email);
		$query = $this->db->get_where('tbl_users', $conditions);
		return $query->result_array();*/
		return 200;
	}
}
