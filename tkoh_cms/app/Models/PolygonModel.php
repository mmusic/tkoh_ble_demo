<?php namespace App\Models;

use CodeIgniter\Model;

class PolygonModel extends Model
{	
    function __construct()
    {
        parent::__construct();
    }

    public function set_polygons($data)
    {
        $builder = $this->db->table('polygon');
        $builder->insert($data);
    }

    public function set_sources($data)
    {
        $builder = $this->db->table('source');
        $builder->insert($data);
    }

    public function get_ts_create($site)
    {
        // get site ts_create  
        $builder = $this->db->table('polygon');
        $builder->select('floor, ts_create');
        $builder->where('site', $site);
        $builder->where('flag', 1);
        $builder->groupBy('floor, ts_create');
        $builder->orderBy('ts_create', 'DESC');
        $query = $builder->get()->getResult();
        return $query;
    }

    public function get_polygon($site, $ts_create)
    {
        // get selected ts_create polygons
        $builder = $this->db->table('polygon');
        $builder->where('site', $site);
        $builder->where('ts_create', $ts_create);
        $query = $builder->get()->getResult();
        return $query;
    }

    public function get_source($site, $ts_create)
    {
        // get selected ts_create polygons
        $builder = $this->db->table('source');
        $builder->where('site', $site);
        $builder->where('ts_create', $ts_create);
        $query = $builder->get()->getResult();
        return $query;
    }

    public function get_lastest_polygon($site, $floor)
    {
        // get site polygon
        $builder = $this->db->table('polygon');
        $builder->selectMax('ts_create');
        $builder->where('flag', 1);
        $max_ts_create = $builder->get()->getResult()[0]->ts_create;

        $builder->where('site', $site);
        $builder->where('floor', $floor);
        $builder->where('ts_create', $max_ts_create);
        $query = $builder->get()->getResult();
        return $query;
    }

    public function del_polygon($site, $ts_create)
    {
        // delete selected ts_create polygons
        try {
            $builder = $this->db->table('polygon');
            $builder->set('flag', 0);
            $builder->where('site', $site);
            $builder->where('ts_create', $ts_create);
            $builder->update();
            return 1;
        }
        catch (\Exception $e)
        {
            die($e->getMessage());
        }
    }

    public function update_source($ts_create, $idx, $data)
    {
        // update source
        $builder = $this->db->table('source');
        $builder->where('ts_create', $ts_create);
        $builder->where('idx', $idx);
        $builder->update($data);
        return 1;
    }

}