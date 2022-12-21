<?php namespace App\Controllers;

use App\Models\RegisterModel;
use App\Models\MonitorModel;
use CodeIgniter\Controller;

class Register extends Controller
{
	public function __construct()
    {
		// parent::__construct();
		$this->model = new RegisterModel();
		$this->model_monitor = new MonitorModel();
    }
    
    public function _remap($method, ...$params)
	{
		if ($method == 'index')
		{
			return $this->index();
		}elseif ($method == 'update_sensor')
		{
			return $this->update_sensor();
		}elseif ($method == 'add_sensor')
		{
			$this->add_sensor();
		}elseif ($method == 'update')
		{
			$this->update();
		}else
		{
			$sensor = $method;
			return $this->register($sensor);
		}
    }

	public function index()
	{
        $site_info = $this->model_monitor->get_site_info_by_name($site_name);
		$data = 
		[
			'icon' => 'fa-gear',
			'title' => 'Register',
			'sub_title' => ' > Full Record',
            'site_names' => $this->model_monitor->get_site_name_all(),
            
            'sensors' => $this->model->get_sensor_all(),
		];

		echo view('head', $data);
		echo view('js');
		echo view('ajax/register', $data);
		echo view('foot');
    }
    
    public function register($sensor)
	{
        $sensor_info = $this->model->get_sensor($sensor);
        $data = 
		[
			'icon' => 'fa-gear',
			'title' => 'Register',
			
            'site_names' => $this->model_monitor->get_site_name_all(),
        ];
        
        // find sensor in sensor table
        if ($sensor_info) {
            // revise
            $data['sub_title'] = ' >  Update ['.$sensor_info[0]['sensor'].']';
            $data['sensor_info'] = $sensor_info[0];
            echo view('head', $data);
            echo view('js');
            echo view('ajax/register_data', $data);
        }else{
            // register
            $data['sub_title'] = ' >  New ['.$sensor.']';
            $data['sensor_ble_mac'] = $sensor;
            echo view('head', $data);
            echo view('js');
            echo view('ajax/register_new', $data);
        }

		echo view('foot');
    }
    
    private function add_sensor()
    {
        if($this->request->getPost()['sensor'])
        {
            $data = array(
                'sensor' => $this->request->getPost()['sensor'],
                'site' => intval($this->request->getPost()['site']),
                'label' => intval($this->request->getPost()['label']),
            );
            $this->model->add_sensor($data);
            echo $data['sensor'];
        } else{
            echo '0';
        }
    }

    private function update_sensor()
    {
        $sensor = $this->request->getPost()['sensor'];
        if($this->request->getPost()['sensor'])
        {
            $data = array(
                'site' => intval($this->request->getPost()['site']),
                'label' => intval($this->request->getPost()['label']),
            );
            $this->model->update_sensor($sensor, $data);
            echo $sensor;
        } else{
            echo '0';
        }
    }
}
