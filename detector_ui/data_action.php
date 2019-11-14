<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');



$t1 = microtime(true);




$id = $_REQUEST["id"];
putLog("id:".$id);

$url = Config::$serverurl_es.'/project/log/_search?pretty';
//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];

putLog("url:".$url);

$data="{\"query\":{\"match\":{\"test_date\" : \"2013-10-10 23:43:02\"}}}";

putLog("data:".$data);

$resRaw = http_request($url, $data);

putLog($resRaw);
//$res = json_decode($resRaw, true);

//putLog($res);
echo $resRaw;
//$res = json_decode($resRaw, true);

//echo $resRaw;//json_encode($res);

$t2 = microtime(true);

putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');











?>