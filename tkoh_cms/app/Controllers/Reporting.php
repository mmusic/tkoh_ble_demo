<?php namespace App\Controllers;

use App\Models\ReportingModel;
use App\Models\MonitorModel;
use CodeIgniter\Controller;

class Reporting extends Controller
{
	public function __construct()
    {
		// parent::__construct();
		$this->model = new ReportingModel();
		$this->model_monitor = new MonitorModel();
	}

	public function index()
	{
        // $site_info = $this->model_monitor->get_site_info_by_name($site_name);
		// $data = 
		// [
		// 	'icon' => 'fa-file-text',
		// 	'title' => 'Reporting',
		// 	'sub_title' => '',
		// 	'site_names' => $this->model_monitor->get_site_name_all(),
		// ];

		// echo view('head', $data);
		// echo view('js');
		// echo view('ajax/reporting', $data);
		// echo view('foot');
	}

	public function get_report($delivery_date)
	{
		$reports = $this->model->get_report($delivery_date);
		$file_name = 'Report_raw_'.$delivery_date.'.csv';

		header('Content-Type: application/csv');
		header('Content-Disposition: attachment; filename="'.$file_name.'";');

		$f = fopen('php://output', 'w');
		fprintf($f, chr(0xEF).chr(0xBB).chr(0xBF));
		foreach ($reports as $report) {
			$data = array(
				$report['sensor'],
				$report['shop_name'],
				$report['shop_id'],
				$report['delivery_date'],
				$report['alert'],
				$report['alert_time'],
				$report['warning'],
			);
			fputcsv($f, $data);
		}
	}

}
