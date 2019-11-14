<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);



require_once(dirname(__FILE__).'/data/get.json.from.server.php');

function downfile($fileurl,$rename)
{
    //ob_start();
    ob_end_clean();
    $filename = substr($fileurl,strrpos($fileurl,'/')+1);
    //header("Content-type:application/octet-stream");
    //header("Accept-Ranges:bytes");
    header("Content-Disposition:attachment;filename={$rename}");
    //header("Content-Disposition:attachment;filename='预算表.pdf'");
    //ob_clean();
    header('Content-Type: application/force-download');
    //$size = readfile($fileurl);
    echo file_get_contents($fileurl);
    //header('Content-Length:'.$size);
    //header("Accept-Length:".$size);
    //putLog("size:".$size);
}

//$data="loginid=".$uuid."&password=".$password."&key=".session_id()."&token=".$_SESSION['token'];

//$data = file_get_contents("php://input"); //接收POST数据
//$xml = simplexml_load_string($input); //提取POST数据为simplexml对象
putLog('');
putLog('');

$t1 = microtime(true);


require_once(dirname(__FILE__).'/require_send_uuid_for_ajax.php');

//unset($_REQUEST["uu"]);
//unset($_REQUEST["random"]);
$data = null;


$uu = $_SERVER["REQUEST_URI"];

$uu = substr($uu,41);

//$arr = explode(".",$uu);
//$arr = explode(".",$uu);
putLog("uu:".$uu);
//putLog("$_REQUEST:".$_REQUEST);


$rename = getGet("rename");

//$arr = explode(".",$uu);
//$arr = explode(".",$uu);
putLog("rename:".$rename);

//$data = file_get_contents("php://input");
//putLog($data);


//foreach($arr as $u){

//  echo $newstr."</br>";
//putLog($arr);


//}

//putLog($uu);
$url = Config::$serverurl_detector.$uu;
//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];

putLog("url:".$url);

//putLog("data:".$data);

//$resRaw = http_request($url, $data);
//putLog(url);
//putLog($resRaw);

//$res = json_decode($resRaw, true);
//header('Content-type:application/octet-stream');

downfile($url,$rename);

//putLog($res);
//echo $resRaw;
//$res = json_decode($resRaw, true);

//echo $resRaw;//json_encode($res);

$t2 = microtime(true);

putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');

putLog('');
putLog('');

?>