<?php namespace App\Controllers;

use App\Models\DashboardModel;
use App\Models\MonitorModel;
use CodeIgniter\Controller;
use CodeIgniter\I18n\Time;

class Dashboard extends Controller
{
	public function __construct()
    {
		// parent::__construct();
		$this->valid_log_level = array('info', 'warning', 'error', 'debug');
		$this->log_level_mapping = array("info" => "default",
										 "debug" => "danger",
										 "warning" => "warning",
										 "error" => "danger");

        $this->loglevel2todo_mapping = array("info" => array("event", "bg-color-greenLight"),
										 "debug" => array("event", "bg-color-greenLight"),
										 "warning" => array("event", "bg-color-orange"),
										 "error" => array("event", "bg-color-red"));

		$this->model = new DashboardModel();
		$this->model_monitor = new MonitorModel();

		$this->valid_src_type = array('sensor', 'server', 'report');
		$this->request = \Config\Services::request();

		$this->sensor_info = $this->model->get_sensor_info()->getResult();
		
	}

	public function index()
	{
		$data = 
		[
			'icon' => 'fa-home',
			'title' => 'Dashboard',
			'sub_title' => '',
			'site_names' => $this->model_monitor->get_site_name_all(),

			'logs' => $this->model->get_logs(30),
			'log_level_mapping' => $this->log_level_mapping,
			'todos' => $this->todos(),
			'reports' => $this->reports(),
		];

		echo view('head', $data);
		echo view('js');
		echo view('ajax/dashboard', $data);
		echo view('foot');
		// echo '<br>';
		// print_r($this->model->get_reporing_all_date()[0]['delivery_date']);
		// echo '<br>';
		// echo substr($this->model->get_reporing_all_date()[0]['delivery_date'],4,2);
		// echo '<br>';
		// echo substr($this->model->get_reporing_all_date()[0]['delivery_date'],0,4);
	}

	public function reports()
	{
		$report_date = $this->model->get_reporing_all_date();
		$res = array();
		foreach($report_date as $date){
			$report_status['title'] = 'Rep. '.$date['delivery_date'];
			$report_status['allDay'] = true;
			$report_status['className'] = array("event", "bg-color-greenLight");
			$report_status['start'] = substr($date['delivery_date'], 0, 4).'-'.substr($date['delivery_date'], 4, 2).'-'.substr($date['delivery_date'], 6, 2);
			
			// link to todos page
			$report_status['url'] = "reporting/get_report/".$date['delivery_date'];
			array_push($res, $report_status);
		}
		return ($res);
	}

	public function todos($src_type='all', $log_level='all')
	{
		$res = array();
		$todos = $this->model->get_todos(30);

		foreach($todos as $todo){
			$todo_status['title'] = $todo->content;
			$todo_status['allDay'] = true;
			$time = Time::createFromTimestamp($todo->ts/1000, 'Asia/Hong_Kong', 'en_US');
			$todo_status['start'] = "{$time->getYear()}-{$time->getMonth()}-{$time->getDay()}";
			$todo_status['className'] = $this->loglevel2todo_mapping[$todo->level];

			$todo_status['id'] = "todos{$todo->id}"; //todo
			$todo_status['ts'] = $time;
			$todo_status['src_type'] = $todo->src_type;
			$todo_status['content'] = $todo->content;
			$todo_status['level'] = $todo->level;
			
			// link to todos page
			$todo_status['url'] = "maintenance/todos/".$todo_status['src_type']."/".$todo->id;
			array_push($res, $todo_status);
		}
		return ($res);
	}

	public function get_time()
	{
	    $time = Time::now('Asia/Hong_Kong', 'en_US');
	    echo $time;
	}
}
