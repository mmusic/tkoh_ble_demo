<?php namespace App\Models;

use CodeIgniter\Model;

class RegisterModel extends Model
{	
	function __construct()
    {
        parent::__construct();
    }

    // get sensor register
    public function get_sensor_all()
    {
        // get all survey event
        $builder = $this->db->table('sensor');
        // $builder->orderBy('id', 'DESC');
        $query = $builder->get()->getResult('array');
        return $query;
    }

    public function get_sensor($sensor)
    {
        $builder = $this->db->table('sensor');
        $builder->where('sensor', $sensor);
        $query = $builder->get()->getResult('array');
        return $query;
    }
    
    public function add_sensor($data)
    {
        // add new sensor
        $builder = $this->db->table('sensor');
        $builder->insert($data);
        return 1;
    }

    public function update_sensor($sensor, $data)
    {
        // update sensor
        $builder = $this->db->table('sensor');
        $builder->where('sensor', $sensor);
        $builder->update($data);
        return 1;
    }

}