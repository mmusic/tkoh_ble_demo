<?php namespace App\Controllers;

class SysInfo extends BaseController
{
    public function __construct()
	{
        // parent::__construct();
        $this->OS = array("Windows" => "Windows",
                        "Linux" => "Linux");
    }

	public function index()
	{
    }

    public function get_os_status()
    {
        $os_name = php_uname();
        if (strpos($os_name, $this->OS["Windows"]) !== false){
            $status = $this->windows_status();
        }elseif (strpos($os_name, $this->OS["Linux"]) !== false){
            $status = $this->linux_status();
        }
        print_r(json_encode($status));
        return $status;
    }
    // -------------------------windows-------------------------------------
    private function get_windows_file_path($fileName, $content)
    {
        $path = dirname(__FILE__) . "\\$fileName";
        if (!file_exists($path)) {
            file_put_contents($path, $content);
        }
        return $path;
    }

    private function get_windows_cpu_usage()
    {
        $path = $this->get_windows_file_path(
            'cpu_usage.vbs',
            "On Error Resume Next
            Set objProc = GetObject(\"winmgmts:\\\\.\\root\cimv2:win32_processor='cpu0'\")
            WScript.Echo(objProc.LoadPercentage)");
        exec("cscript -nologo $path", $usage);
        unlink($path);
        return $usage[0];
    }

    private function get_windows_memory_usage()
    {
        $path = $this->get_windows_file_path(
            'memory_usage.vbs',
            "On Error Resume Next
            Set objWMI = GetObject(\"winmgmts:\\\\.\\root\cimv2\")
            Set colOS = objWMI.InstancesOf(\"Win32_OperatingSystem\")
            For Each objOS in colOS
            Wscript.Echo(\"{\"\"TotalVisibleMemorySize\"\":\" & objOS.TotalVisibleMemorySize & \",\"\"FreePhysicalMemory\"\":\" & objOS.FreePhysicalMemory & \"}\")
            Next");
        exec("cscript -nologo $path", $usage);
        $memory = json_decode($usage[0], true);
        $memory['usage'] = Round((($memory['TotalVisibleMemorySize'] - $memory['FreePhysicalMemory']) / $memory['TotalVisibleMemorySize']) * 100);
        unlink($path);
        return $memory;
    }
    
    private function windows_status(Type $var = null)
    {
        $status = array("cpu" => $this->get_windows_cpu_usage(),
                        "memory" => $this->get_windows_memory_usage(), 
                        "storage" => 0);
        return $status;
    }

    
    private function linux_status(Type $var = null)
    {
        $status = array("cpu" => 0,
                        "memory" => 0, 
                        "storage" => 0);
        return $status;
    }

    // -------------------------linux-------------------------------------
    public function test()
    {
        # code...
        $fp = popen('top -b -n 2 | grep -E "(Cpu|Mem)"',"r");//获取某一时刻系统cpu和内存使用情况
        $rs = "";
        while(!feof($fp)){
        $rs .= fread($fp,1024);
        }
        pclose($fp);
        echo $rs.'<br>';
        preg_match_all("/Cpu.*us\,/", $rs,$cpus);
        var_dump($cpus[1]);
        echo '<br>';
        preg_match('/(\d|\.)+/', $cpus[1], $cpu); //cpu使用百分比
        var_dump($cpu);
        echo '<br>';
        preg_match_all('/ \d+ used/', $rs,$cmems);
        var_dump($cmems[3]);
        echo '<br>';
        preg_match('/\d+/', $cmems[3],$cmem); //内存使用量 k
        var_dump($cmem);
        $log = "$cpu[0]--$cmem[0],\r\n";
        echo $log;
        $logres = file_put_contents('./yali.log',$log,FILE_APPEND);
    }
}
