<?php namespace App\Models;

use CodeIgniter\Model;

class ReportingModel extends Model
{	
	function __construct()
    {
        parent::__construct();
    }

    public function get_report($delivery_date)
    {
        // get all delivery_date
        $builder = $this->db->table('reporting');
        $builder->where('delivery_date', $delivery_date);
        $query = $builder->get()->getResult('array');
        return $query;
    }
}