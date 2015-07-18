<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Companies extends CI_Model {
	function company_login_info($email, $pass)
    {
        $conditions = array('company_email' => $email, 'company_password' => $pass);
		$query = $this->db->get_where('tbl_company', $conditions);
		return $query->row();
    }
}