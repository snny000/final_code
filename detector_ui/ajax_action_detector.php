<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');

require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

putLog('');
putLog('');


//$data="loginid=".$uuid."&password=".$password."&key=".session_id()."&token=".$_SESSION['token'];

//$data = file_get_contents("php://input"); //接收POST数据
//$xml = simplexml_load_string($input); //提取POST数据为simplexml对象
$t1 = microtime(true);



//unset($_REQUEST["uu"]);



require_once(dirname(__FILE__).'/require_send_uuid_for_ajax.php');


unset($_REQUEST["uu"]);
unset($_REQUEST["random"]);
$data = http_build_query($_REQUEST);


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
//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];

putLog("url:".$url);

putLog("data:".$data);
//$t1 = microtime(true);
$resRaw = http_request($url, $data);
//putLog(url);
putLog($resRaw);
//$res = json_decode($resRaw, true);

//putLog($res);
echo $resRaw;
//$res = json_decode($resRaw, true);

//echo $resRaw;//json_encode($res);

$t2 = microtime(true);

putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');
putLog('');
putLog('');

?>