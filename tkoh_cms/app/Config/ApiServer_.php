<?php namespace Config;

use CodeIgniter\Config\BaseConfig;

class ApiServer_ extends BaseConfig
{
    #public $apiServerUrl = 'http://143.89.49.63:8080/';
    public $apiServerUrl = 'http://192.168.10.123:8080/';
    public $sensor = [
        'sensor_status'      => 'status',
        'sensor_status_dev'  => 'status2'
    ];
    public $beacon = [
        'beacon_list'      => 'beacon',
    ];
    public $station = [
        'KowloonBay'      => 'KOB',
        'Central'      => 'CEN',
        'YauMaTei'      => 'YMT',
    ];

    public $mapbox = [
        'key' => 'pk.eyJ1Ijoic3RhcnJ5ZmFuIiwiYSI6ImNrZDVrc3N1NDE4NmkyeG54Zzk0dTQ1MmkifQ.TgZ1kXuLRQpNoUy4nApcxg'
    ];
}