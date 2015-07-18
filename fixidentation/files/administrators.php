<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Administrators extends CI_Model {
	function admin_login_info($username, $pass)
    {
        $conditions = array('admin_username' => $username, 'admin_password' => $pass);
		$query = $this->db->get_where('tbl_administrators', $conditions);
		return $query->row();
    }
}