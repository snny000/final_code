<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');





//$data="loginid=".$uuid."&password=".$password."&key=".session_id()."&token=".$_SESSION['token'];

//$data = file_get_contents("php://input"); //接收POST数据
//$xml = simplexml_load_string($input); //提取POST数据为simplexml对象
putLog('');
putLog('');

$t1 = microtime(true);

require_once(dirname(__FILE__).'/require_send_uuid_for_ajax.php');

//unset($_REQUEST["uu"]);
//unset($_REQUEST["random"]);
//$data = http_build_query($_REQUEST);
//var_dump($_FILES);
putLog("start upload:");
//putLog("$_REQUEST:".$_REQUEST);



move_uploaded_file($_FILES['upfile']['tmp_name'], 'up_tmp/'.$_FILES['upfile']['name']);

//$fname='/alidata/www/default/up_tmp/'.$_FILES['upfile']['name'];
$fname='up_tmp/'.$_FILES['upfile']['name'];


//'name'=>'tanteng',
//$file = realpath('temp.jpg'); //要上传的文件

//$data = array('upfile'=>'@'.$fname); //这里是要上传的文件，key与后台处理文件对应

//$data = array('upfile'=>curl_file_create($fname)); //这里是要上传的文件，key与后台处理文件对应

putLog("realpath:".realpath($fname));
//$data['upfile'] = '@'.$fname;
//$data = array('upfile' => new CURLFile(realpath($fname)));


if (class_exists('CURLFile')) {
    $data['upfile'] = new CURLFile(realpath($fname));
} else {
    $data['upfile'] = '@'.realpath($fname);
}



putLog("upfile:".json_encode($data));
//$data = http_build_query($data);

$uu = getGet("uu");

//$arr = explode(".",$uu);
putLog("uu:".$uu);
//putLog("$_REQUEST:".$_REQUEST);




//$data = file_get_contents("php://input");
//putLog($data);

$arr = str_replace(".","/",$uu,$i);
putLog("替换数：".$i);

//foreach($arr as $u){

  //  echo $newstr."</br>";
//putLog($arr);

putLog("arr:".$arr);
//}

//putLog($uu);
$url = Config::$serverurl_detector.'/'.$arr;

//$url = "http://192.168.120.75/up.php";

//$url = "http://192.168.120.234/file/upload";


//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];

putLog("url:".$url);

//putLog("data:".$data);
putLog(json_encode($data));


$resRaw = http_request($url, $data);

putLog($resRaw);
//$res = json_decode($resRaw, true);

//putLog($res);
echo $resRaw;
//$res = json_decode($resRaw, true);

//echo $resRaw;//json_encode($res);
unlink($fname);  //$file是文件名


$t2 = microtime(true);
putLog('IP地址是:'.@$_SERVER['REMOTE_ADDR']);
putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');

putLog('');
putLog('');
?>