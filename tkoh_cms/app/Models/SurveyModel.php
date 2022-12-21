<?php namespace App\Models;

use CodeIgniter\Model;

class SurveyModel extends Model
{	
	function __construct()
    {
        parent::__construct();
    }

    // EVENT START
    public function get_event_all()
    {
        // get all survey event
        $builder = $this->db->table('survey_event');
        $builder->orderBy('id', 'DESC');
        $query = $builder->get();
        return $query;
    }

    public function get_event_item($event)
    {
        // get survey event item
        $builder = $this->db->table('survey_event');
        $builder->where('event', $event);
        $query = $builder->get();
        return $query;
    }

    public function add_event($data)
    {
        // add new survey event
        $builder = $this->db->table('survey_event');
        $builder->insert($data);
        return 1;
    }

    public function update_event($event, $data)
    {
        // update survey event
        $builder = $this->db->table('survey_event');
        $builder->where('event', $event);
        $builder->update($data);
        return 1;
    }
    // EVENT END

    public function api_data($source, $event)
    {
        $builder = $this->db->table($source);
        $builder->where('event', $event);
        $query = $builder->get();
        return $query;
    }

    
    // SURVEY DATA START
    public function get_beacon($event)
    {
        // get survey event
        $builder = $this->db->table('survey_beacon');
        $builder->where('event', $event);
        $query = $builder->get();
        return $query;
    }

    public function get_wifi($event)
    {
        // get survey event
        $builder = $this->db->table('survey_wifi');
        $builder->where('event', $event);
        $query = $builder->get();
        return $query;
    }

    public function get_imu($event)
    {
        // get survey event
        $builder = $this->db->table('survey_imu');
        $builder->where('event', $event);
        $query = $builder->get();
        return $query;
    }

    public function get_uwb_loc($event)
    {
        // get survey event
        $builder = $this->db->table('survey_uwb_loc');
        $builder->where('event', $event);
        $query = $builder->get();
        return $query;
    }

    public function get_uwb_dist($event)
    {
        // get survey event
        $builder = $this->db->table('survey_uwb_dist');
        $builder->where('event', $event);
        $query = $builder->get();
        return $query;
    }
    // SURVEY DATA END
    
}