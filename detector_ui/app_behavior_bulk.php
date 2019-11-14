<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');

$t1 = microtime(true);

$data = $_REQUEST["data"];
putLog("data :".$data);
//echo $data."\n";
$item_arr = json_decode($data);


$_records = "";
foreach ($item_arr as $item){
//    echo json_encode($json)."\n";
    $_records = $_records."{\"create\":{}}\n".json_encode($item, JSON_UNESCAPED_SLASHES)."\n";
}
//echo $_records."\n";

$url = Config::$serverurl_es.'/app_behavior/log/_bulk?pretty';
putLog("url:".$url);
$resRaw = http_request($url, $_records);


putLog($resRaw);
//echo $resRaw."\n";
$res = json_decode($resRaw, true);
echo "{\"code\":0".",\"took\":".$res["took"].",\"total\":".count($res["items"]).",\"data\":\"批量导入成功\"}";
?>


