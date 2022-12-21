<?php namespace App\Models;

use CodeIgniter\Model;

class MaintenanceModel extends Model
{
    function __construct()
    {
        parent::__construct();
    }

    public function get_related_offline_reporting_logs($id, $recent=20)
    {
        # todo
        # same level, same type, recently solved
        $row = $this->get_log($id);
        $related_level = $row->level;
        $related_src_type = $row->src_type;

        $query   = $this->db->query("SELECT id, ts, src_type, content, level, todo FROM daily_log WHERE src_type = '{$related_src_type}' and level = '{$related_level}' ORDER BY id DESC LIMIT {$recent}");
        $results = $query->getResult();
//         print_r($results);
        return $results;
    }

    public function get_related_sensor_logs($id, $recent=20)
    {
        # todo
        # same level, same type, recently solved
        $row = $this->get_log($id);
        $related_level = $row->level;
        $related_src_type = $row->src_type;

        $query   = $this->db->query("SELECT id, ts, src_type, content, level, todo FROM daily_log WHERE src_type = '{$related_src_type}' and level = '{$related_level}' ORDER BY id DESC LIMIT {$recent}");
        $results = $query->getResult();
//         print_r($results);
        return $results;
    }

    public function get_related_api_server_logs($id, $recent=20)
    {
        # todo
        # same level, same type, recently solved
        $row = $this->get_log($id);
        $related_level = $row->level;
        $related_src_type = $row->src_type;

        $query   = $this->db->query("SELECT id, ts, src_type, content, level, todo FROM daily_log WHERE src_type = '{$related_src_type}' and level = '{$related_level}' ORDER BY id DESC LIMIT {$recent}");
        $results = $query->getResult();
//         print_r($results);
        return $results;
    }

    public function get_related_reporting_server_logs($id, $recent=20)
    {
        # todo
        # same level, same type, recently solved
        $row = $this->get_log($id);
        $related_level = $row->level;
        $related_src_type = $row->src_type;

        $query   = $this->db->query("SELECT id, ts, src_type, content, level, todo FROM daily_log WHERE src_type = '{$related_src_type}' and level = '{$related_level}' ORDER BY id DESC LIMIT {$recent}");
        $results = $query->getResult();
//         print_r($results);
        return $results;
    }

    public function get_log($id)
    {
        $builder = $this->db->table('daily_log');
        $builder->where('id', $id);
        $query = $builder->get();
        return $query->getResult('array')[0];
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

    public function update_todos($id, $solve_msg)
    {
        $data = 
        [
            'solve_msg' => $solve_msg, 
            'todo' => 1
        ];
        $builder = $this->db->table('daily_log');
        $builder->where('id', $id);
        $builder->update($data);
        return 1;
    }

}