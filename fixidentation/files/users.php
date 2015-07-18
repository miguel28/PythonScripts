<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Users extends CI_Model {

    function __construct()
    {
        // Call the Model constructor
        parent::__construct();
    }
    
    function insert_new_user($email, $pass)
    {
        $data = array(
		   'user_email' => $email,
		   'user_password' => $pass,
		   'user_active' => '0',
       'user_confirmed' => '0',
		   'user_date_registration' => date('Y-m-d H:i:s', time())
		);

		$this->db->insert('tbl_users', $data);
			return $this->db->insert_id();
    }
    function get_user_from_email($email)
    {
       $conditions = array('user_email' => $email);
			$query = $this->db->get_where('tbl_users', $conditions);
			return $query->row();
    }
    function get_user_by_email_and_password($email, $pass)
    {
      $conditions = array('user_email' => $email, 'user_password' => $pass);
			$query = $this->db->get_where('tbl_users', $conditions);
			return $query->row();
    }
	 function get_user_by_email($email)
    {
      $conditions = array('user_email' => $email);
			$query = $this->db->get_where('tbl_users', $conditions);
			return $query->row();
    }
    
    function get_user_info($id)
    {
       $conditions = array('user_id' => $id);
			$query = $this->db->get_where('tbl_users', $conditions);
			return $query->row();
    }
    function set_ative_user($user_id)
    {
      $data = array(
        'user_active' => '1'
      );

      $this->db->where('user_id', $user_id)
               ->update('tbl_users',$data);
    }
    
    
    function confirm_user($user_id)
    {
      $data = array(
        'user_confirmed' => '1'
      );

     $this->db->where('user_id', $user_id)
              ->update('tbl_users',$data);
    }
    function insert_hash_confirmation($id, $hash)
    {
        $curent_date = new DateTime('NOW');
        $curent_date->modify('+ 1 day');
        $exp_date = $curent_date->format('Y-m-d H:i:s');
        
        $data = array(
		   'confirm_hash' => $hash,
		   'confirm_expiration' => $exp_date,
		   'confirm_user_id' => $id,
       'confirmed' => '0'
		);

		$this->db->insert('tbl_reg_confirm', $data);
			return $this->db->insert_id();
    }
    function get_last_hash_by_user_id($id)
    {
      $conditions = array('confirm_user_id' => $id, 'confirmed' => '0', 'confirm_expiration >=' => date('Y-m-d'));
			$query = $this->db->get_where('tbl_reg_confirm', $conditions);
			return $query->last_row();
    }
    function get_last_hash_expired($id)
    {
      $conditions = array('confirm_user_id' => $id, 'confirmed' => '0', 'confirm_expiration <' =>  date('Y-m-d'));
			$query = $this->db->get_where('tbl_reg_confirm', $conditions);
			return $query->last_row();
    }
    function confirm_hash_by_id($hash_id)
    {
      $data = array(
        'confirmed' => '1'
      );

      $this->db->where('confirm_id', $hash_id)
               ->update('tbl_reg_confirm',$data);
    }
    
    function complete_user_info($id,$fname,$lname,$phone,$celphone,$gender,$birth,$addr,$city,$state,$country,$zipcode,$university, $career, $career_status)
    {
      $data = array(
		   'addr_direction' => $addr,
		   'addr_city' => $city,
		   'addr_state' => $state,
       'addr_country' => $country,
		   'addr_zipcode' => $zipcode
			);

			$this->db->insert('tbl_address', $data);
			$address_id = $this->db->insert_id();
        
			$data2 = array(
		   'user_id' => $id,
		   'user_fname' => $fname,
		   'user_lname' => $lname,
       'user_birthdate' => $birth,
		   'user_address_id' => $address_id,
       'user_phone' => $phone,
       'user_celphone' => $celphone,
       'user_sex' => $gender,
		   'user_study' => $career_status,
		   'user_university' => $university,
		   'user_career' =>  $career
			);
      $this->db->insert('tbl_user_info', $data2);
      return $this->db->insert_id();
    }
}