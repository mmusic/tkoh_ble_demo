<?php namespace App\Controllers;

class Api extends BaseController
{
    public function __construct()
	{
		// parent::__construct();
    }

	public function index()
	{
        echo config('ApiServer_')->apiServerUrl;
    }

    public function get_sensor_status()
    {
        # code...
        $sensor_status = file_get_contents(config('ApiServer_')->apiServerUrl.config('ApiServer_')->sensor['sensor_status']);
        // $b = json_encode($a);
        return ($sensor_status);
    }

	//--------------------------------------------------------------------

}
