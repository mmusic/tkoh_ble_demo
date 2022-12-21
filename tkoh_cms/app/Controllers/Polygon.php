<?php namespace App\Controllers;

use App\Models\PolygonModel;
use App\Models\MonitorModel;
use CodeIgniter\Controller;
use CodeIgniter\I18n\Time;

class Polygon extends Controller
{
	public function __construct(){
		$this->model = new PolygonModel();
		$this->model_monitor = new MonitorModel();
	}

	public function _remap($method, ...$params)
	{
		if ($method === 'save')
		{
			$site = $params[0];
			$floor = $params[1];
			$this->save_polygons($site, $floor);
		}
		// elseif($method === 'import')
		// {
		// 	$site = $params[0];
		// 	$floor = $params[1];
		// 	$this->import_polygons($site, $floor);
		// }
		elseif($method === 'export_geojson')
		{
			$site = $params[0];
			$ts_create = $params[1];
			$this->export_polygons_geojson($site, $ts_create);
		}
		elseif($method === 'export_meter')
		{
			$site = $params[0];
			$ts_create = $params[1];
			$this->export_polygons_meter($site, $ts_create);
		}
		elseif($method === 'del')
		{
			$site = $params[0];
			$ts_create = $params[1];
			$this->del_polygon($site, $ts_create);
		}
		elseif($method === 'update_source')
		{
			$ts_create = $params[0];
			$this->update_source($ts_create);
		}
		elseif ($method === 'index')
		{
			return $this->index();
		}
		else
		{
			$site_name = $method;
			$ts_create = $params[0];
			return $this->view_polygon($site_name, $ts_create);
		}
	}

	private function index()
	{	
		$site_info = 0;
		$data = 
		[
			'icon' => 'fa-gear',
			'title' => 'Polygon',
			'sub_title' => '',
			'site_names' => $this->model_monitor->get_site_name_all(),

			'site_info' => $site_info,
			'site_polygons' => $this->model->get_lastest_polygon(1001, 1),
			'site_ts_create' => $this->model->get_ts_create($site, $floor),
			'mapbox_key' => config('ApiServer_')->mapbox['key'],
		];

		echo view('head', $data);
		echo view('js');
		echo view('ajax/polygon', $data);
		echo view('foot');
	}

	private function view_polygon($site_name, $ts_create)
	{
		$site_info = $this->model_monitor->get_site_info_by_name($site_name);

		if($ts_create){
			$site_polygons = $this->model->get_polygon($site_info[0]['site'], $ts_create);
			$site_sources = $this->model->get_source($site_info[0]['site'], $ts_create);
		}else{
			$site_polygons = 0;
			$site_sources = 0;
		}
		$site_ts_create = $this->model->get_ts_create($site_info[0]['site']);

		$data = 
		[
			'icon' => 'fa-gear',
			'title' => 'Polygon',
			'sub_title' => ' > '. $site_info[0]['site_name'] . ' - ' . $ts_create,
			'site_names' => $this->model_monitor->get_site_name_all(),

			'site_info' => $site_info,
			'ts_create' => $ts_create,
			// 'site_beacons' => $this->model_monitor->get_site_beacons($site_info[0]['site']),
			'site_sources' => $site_sources,
			'site_polygons' => $site_polygons,
			'site_ts_create' => $site_ts_create,
			'mapbox_key' => config('ApiServer_')->mapbox['key'],
		];

		echo view('head', $data);
		echo view('js');
		echo view('ajax/polygon', $data);
		echo view('foot');
	}

	// private function import_polygons($site, $floor)
	// {
	// 	$import_polygons = $this->request->getPost(['import']);
	// 	$raw_polygons = json_decode($import_polygons['import']);
	// 	if($raw_polygons){
	// 		$poly = 1;
	// 		$ts_create = $this->get_timestamp();
	// 		foreach($raw_polygons as $raw_polygon_item){
	// 			if(count($raw_polygon_item) == 4){
	// 				foreach($raw_polygon_item as $raw_polygon_item_coor){
	// 					//conversion formula 
	// 					//$raw_polygon_item_coor[0] == longitude
	// 					//$raw_polygon_item_coor[1] == latitude
	// 				}
	// 				array_push($raw_polygon_item, $raw_polygon_item[0]);
	// 				$polygon_data = 
	// 				[
	// 					'site' => $site,
	// 					'floor' => $floor,
	// 					'poly' => $poly,
	// 					'geojson' => '['.json_encode($raw_polygon_item).']',
	// 					'ts_create' => $ts_create,
	// 					'flag' => 1
	// 				];
	// 				$this->model->set_polygons($polygon_data);
	// 	 			$poly += 1;
	// 				// print_r($polygon_data);				
	// 			}else{
	// 				echo 0;
	// 			}				
	// 		}
	// 		echo $ts_create;
	// 	}else{
	// 		echo 0;
	// 	}	
	// }

	// backup
	// private function save_polygons($site, $floor)
	// {
	// 	$raw_polygons = $this->request->getPost(['raw_polygons']);
	// 	if ($raw_polygons['raw_polygons']['features']) {
	// 		// get raw ploygons
	// 		// geometry coordinates
	// 		$poly = 1;
	// 		$ts_create = $this->get_timestamp();
	// 		foreach ($raw_polygons['raw_polygons']['features'] as $polygon_item) {
	// 			if (count($polygon_item['geometry']['coordinates'][0]) == (4 + 1)) {
	// 				//todo vertex
	// 				$polygon_data = 
	// 				[
	// 					'site' => $site,
	// 					'floor' => $floor,
	// 					'poly' => $poly,
	// 					'geojson' => str_replace('"', '', json_encode($polygon_item['geometry']['coordinates'])),
	// 					'vertex' => $this->xy2vertex(($polygon_item['geometry']['xy'][0]), $poly, $floor),
	// 					'ts_create' => $ts_create,
	// 					'flag' => 1
	// 				];
	// 				$this->model->set_polygons($polygon_data);
	// 				$poly += 1;
	// 			}
	// 		}
	// 		echo $ts_create;
	// 	}else {
	// 		echo 0;
	// 	}	
	// }
	
	// new function to combine polygon in geojson coordinate & source points
	private function save_polygons($site, $floor)
	{
		$raw_polygons = $this->request->getPost(['raw_polygons']);
		if ($raw_polygons['raw_polygons']['features']) {
			// get raw ploygons
			// geometry coordinates
			$idx_poly = 1;
			$idx_source = 1;
			$ts_create = $this->get_timestamp();
			// find idx source
			foreach ($raw_polygons['raw_polygons']['features'] as $polygon_item) {
				if ($polygon_item['geometry']['type'] == 'Point') {
					if ($polygon_item['properties']['source_idx']) {
						if ($idx_source <= $polygon_item['properties']['source_idx']) {
							$idx_source = $polygon_item['properties']['source_idx'] + 1;
						}
					}
				}
			}

			foreach ($raw_polygons['raw_polygons']['features'] as $polygon_item) {
				if ($polygon_item['geometry']['type'] == 'Polygon') {
					if (count($polygon_item['geometry']['coordinates'][0]) == (4 + 1)) {
						//todo vertex
						$polygon_data = 
						[
							'site' => $site,
							'floor' => $floor,
							'poly' => $idx_poly,
							'geojson' => str_replace('"', '', json_encode($polygon_item['geometry']['coordinates'])),
							// 'vertex' => $this->xy2vertex(($polygon_item['geometry']['xy'][0]), $poly, $floor),
							'ts_create' => $ts_create,
							'flag' => 1
						];
						$this->model->set_polygons($polygon_data);
						$idx_poly += 1;
					}
				}elseif ($polygon_item['geometry']['type'] == 'Point') {
					$source_data = 
					[
						'site' => $site,
						'lng' => floatval($polygon_item['geometry']['coordinates'][0]),
						'lat' => floatval($polygon_item['geometry']['coordinates'][1]),
						'floor' => $floor,
						'ts_create' => $ts_create,
						'flag' => 1,
					];
					if ($polygon_item['properties']['source_idx']) {
						$source_data['idx'] = $polygon_item['properties']['source_idx'];
					}else {
						$source_data['idx'] = $idx_source;
						$idx_source += 1;
					};
					if ($polygon_item['properties']['source_name']) {
						$source_data['name'] = $polygon_item['properties']['source_name'];
					}
					$this->model->set_sources($source_data);
					
				}
			}
			echo $ts_create;
		}else {
			echo 0;
		}	
	}

	private function xy2vertex($xy, $poly, $floor)
	{
		$vertex = [];
		foreach ($xy as $idx => $xy_item) {
			if ($idx < 4) {
				$vertex_item = [floatval(sprintf("%.1f", $xy_item[0])), floatval(sprintf("%.1f", $xy_item[1])), intval($floor)];
				array_push($vertex, $vertex_item);
			}
		}
		return $poly.': '.json_encode($vertex);
	}

	private function del_polygon($site, $ts_create)
	{
		$result = $this->model->del_polygon($site, $ts_create);
		echo '<Strong style="color:red">Delete polygon:'.$site.' '.$ts_create.' SUCCESS!</Strong>';
	}

	// backup
	// private function export_polygons($site, $ts_create)
	// {
	// 	// get floor
	// 	$polygons = $this->model->get_polygon($site, $ts_create);
	// 	$vertex = '{';
	// 	foreach ($polygons as $polygon_item) {
	// 		$vertex = $vertex.$polygon_item->vertex.',';
	// 	}
	// 	$vertex = $vertex.'}';
		
	// 	$file_name = 'Polygon_'.$site.'_'.$ts_create.'.txt';
	// 	// echo $vertex;

	// 	header('Content-Type: application/vnd.ms-excel;charset=UTF-8');
	// 	header('Content-Type: application/force-download');
	// 	header('Content-Disposition: attachment;filename='.$file_name);
	// 	$fp = fopen('php://output', 'w');
	// 	fwrite($fp, json_encode($vertex));
	// 	fclose($fp);
	// }

	// new function to combine polygon in geojson coordinate
	private function export_polygons_geojson($site, $ts_create)
	{
		// get floor
		$polygons = $this->model->get_polygon($site, $ts_create);
		$geojson_coor = 'MAPS = {'."\n";
		foreach ($polygons as $polygon_item) {
			$coor = json_decode($polygon_item->geojson);
			unset($coor[0][4]);
			for ($i=0; $i < 4; $i++) { 
				array_push($coor[0][$i], intval($polygon_item->floor));
			}
			$geojson_coor = $geojson_coor . $polygon_item->floor. $polygon_item->poly . ':' . json_encode($coor[0]) . ','."\n";
		}
		$geojson_coor = $geojson_coor.'}'."\n\n";

		$source_coor = 'SOURCE_INFO_DICT = {'."\n";
		$sources = $this->model->get_source($site, $ts_create);
		
		foreach ($sources as $source_item) {
			$coor = "'".$source_item->name."': SOURCE_INFO(source_identifier='".$source_item->name."', x=".$source_item->lng.", y=".$source_item->lat.", z=".$source_item->floor.", type='non-lon-lat', activated=True, addition_info={}), ,"."\n";
			$source_coor = $source_coor.$coor;
		}
		$source_coor = $source_coor."}";
		// print_r($geojson_coor);
		// print_r(($source_coor));
		$file_name = 'PolygonAndSource_GEO_'.$site.'_'.$ts_create.'.txt';
		header('Content-Type: application/vnd.ms-excel;charset=UTF-8');
		header('Content-Type: application/force-download');
		header('Content-Disposition: attachment;filename='.$file_name);
		$fp = fopen('php://output', 'w');
		fwrite($fp, $geojson_coor);
		fwrite($fp, $source_coor);
		fclose($fp);
	}

	private function export_polygons_meter($site, $ts_create)
	{
		$geo2meter = 111194.926644;
		// get floor
		$polygons = $this->model->get_polygon($site, $ts_create);
		$geojson_coor = 'MAPS = {'."\n";
		foreach ($polygons as $polygon_item) {
			$coor = json_decode($polygon_item->geojson);
			unset($coor[0][4]);
			for ($i=0; $i < 4; $i++) { 
				$coor[0][$i][0] = $coor[0][$i][0] * $geo2meter;
				$coor[0][$i][1] = $coor[0][$i][1] * $geo2meter;
				array_push($coor[0][$i], intval($polygon_item->floor));
			}
			$geojson_coor = $geojson_coor . $polygon_item->floor. $polygon_item->poly . ':' . json_encode($coor[0]) . ','."\n";
		}
		$geojson_coor = $geojson_coor.'}'."\n\n";

		$source_coor = 'SOURCE_INFO_DICT = {'."\n";
		$sources = $this->model->get_source($site, $ts_create);
		// 111194.926644
		foreach ($sources as $source_item) {
			$coor = "'".$source_item->name."': SOURCE_INFO(source_identifier='".$source_item->name."', x=".$source_item->lng * $geo2meter.", y=".$source_item->lat * $geo2meter.", z=".$source_item->floor.", type='non-lon-lat', activated=True, addition_info={}), "."\n";
			$source_coor = $source_coor.$coor;
		}
		$source_coor = $source_coor."}";
		// print_r($geojson_coor);
		// print_r(($source_coor));
		$file_name = 'PolygonAndSource_METER_'.$site.'_'.$ts_create.'.txt';
		header('Content-Type: application/vnd.ms-excel;charset=UTF-8');
		header('Content-Type: application/force-download');
		header('Content-Disposition: attachment;filename='.$file_name);
		$fp = fopen('php://output', 'w');
		fwrite($fp, $geojson_coor);
		fwrite($fp, $source_coor);
		fclose($fp);
	}

	private function update_source($ts_create)
	{
		$source_idx = $this->request->getPost(['idx']);
		$source_name = $this->request->getPost(['name']);
		$data = 
		[
			'name' => $source_name
		];
		$result = $this->model->update_source($ts_create, $source_idx, $data);
		echo $ts_create;
	}

	private function get_timestamp()
	{
	    $time = Time::now('Asia/Hong_Kong', 'en_US');
	    return $time->getTimestamp();
	}
}