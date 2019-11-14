<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');



$t1 = microtime(true);


unset($_REQUEST["uu"]);
unset($_REQUEST["random"]);
$data = http_build_query($_REQUEST);


$uu = getGet("uu");

//$arr = explode(".",$uu);
putLog("uu:".$uu);
//putLog("$_REQUEST:".$_REQUEST);



//  echo $newstr."</br>";
//putLog($arr);

//putLog("arr:".$arr);
//}

//putLog($uu);
$url = Config::$serverurl.'/'.$uu;
//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];

putLog("url:".$url);

putLog("data:".$data);

$resRaw = http_request($url, $data);

putLog($resRaw);
//$res = json_decode($resRaw, true);

//putLog($res);
echo $resRaw;
//$res = json_decode($resRaw, true);

//echo $resRaw;//json_encode($res);

$t2 = microtime(true);
putLog('IP地址是:'.@$_SERVER['REMOTE_ADDR']);
putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');











?>