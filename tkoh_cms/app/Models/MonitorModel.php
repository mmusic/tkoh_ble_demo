<?php namespace App\Models;

use CodeIgniter\Model;

class MonitorModel extends Model
{	
    function __construct()
    {
        parent::__construct();
    }

    public function get_site_sources($site)
    {
        $builder = $this->db->table('source_release');
        $builder->where('site', $site);
        $query = $builder->get();
        return $query->getResult('array');
    }

    public function get_site_info_by_name($site_name)
    {
        // get all sensor
        $builder = $this->db->table('site');
        $builder->where('site_name', $site_name);
        $builder->orderBy('floor, site', 'ASC');
        $query = $builder->get();
        return $query->getResult('array');
    }

    public function get_site_name_all()
    {
        // get all sensor
        $query = $this->db->query("SELECT max(id), site, site_name FROM site GROUP BY site, site_name ORDER BY max(id) ASC");
        return $query->getResult('array');
    }

    public function get_sensor_info_all()
    {
        // get all sensor
        $builder = $this->db->table('sensor');
        $query = $builder->get();
        return $query->getResult();
    }

    public function get_site_sensors($site)
    {
        $builder = $this->db->table('source_release');
        $builder->where('site', $site);
        // $builder->orderBy('label', 'ASC');
        $query = $builder->get();
        return $query->getResult();
    }

    public function get_site_beacons($site)
    {
        $builder = $this->db->table('site');
        $builder->select('floor');
        $builder->where('site', $site);
        $floors = $builder->get()->getResult();

        $builder = $this->db->table('beacon');
        foreach ($floors as $floor) {
            $builder->orWhere('major', $site.$floor->floor);
        }
        $query = $builder->get();
        return $query->getResult();
    }

    public function get_site_geojson($site)
    {
        // get site geojson data
        $builder = $this->db->table('site');
        $builder->where('site', $site);
        $query = $builder->get();
        $builder->orderBy('floor', 'ASC');
        return $query->getResult();
    }

}