<?php namespace App\Models;

use CodeIgniter\Model;

class DashboardModel extends Model
{	
    function __construct()
    {
        parent::__construct();
    }

    public function get_reporing_all_date()
    {
        // get all delivery_date
        $builder = $this->db->table('reporting');
        $builder->select('delivery_date');
        $builder->groupBy('delivery_date');
        $query = $builder->get()->getResult('array');
        return $query;
    }

    public function get_sensor_info()
    {
        // get all sensor
        $builder = $this->db->table('sensor');
        $query = $builder->get();
        return $query;
    }

    public function get_site_info()
    {
        // get all sensor
        $builder = $this->db->table('site');
        $builder->select('site, site_name');
        $query = $builder->get();
        return $query;
    }

    public function get_raw_loc_data($minutes)
    {
        if($minutes <= 100)
        {
            // get lastest $minutes data
            $builder = $this->db->table('raw_loc_data');
            $builder->orderBy('id', 'DESC');
            $query = $builder->get($minutes);
            return $query;
        }
    }

    public function get_raw_beacon_data($minutes)
    {
        if($minutes <= 100)
        {
            // get lastest $minutes data
            $builder = $this->db->table('raw_beacon_data');
            $builder->orderBy('id', 'DESC');
            $query = $builder->get($minutes);
            return $query;
        }
    }

    public function get_logs($minutes)
    {
        if($minutes <= 100)
        {
            // get lastest $minutes data
            $builder = $this->db->table('daily_log');
            $builder->orderBy('ts', 'DESC');
            $query = $builder->get($minutes)->getResult('array');
            return $query;
        }
    }

    public function get_todos($minutes)
    {
        if($minutes <= 100)
        {
            // get lastest $minutes data
            $query   = $this->db->query('SELECT id, ts, src_type, content, level FROM daily_log WHERE todo=0');
            $results = $query->getResult();
            return $results;
        }
    }

}