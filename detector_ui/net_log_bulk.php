<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');

$t1 = microtime(true);

$data = $_REQUEST["data"];
putLog("data :".$data);

$keys=array("sip","sport","smac","dip","dport","dmac",
    "protocol","app","tcp_flag","in_bytes","out_bytes","in_pkts",
    "out_pkts","start_time","end_time");


$records = explode("~=~", $data);
$_records = "";
foreach ($records as $record){
    $items = explode("#", $record);
//    echo "count(items):".count($items)."\n";
    $_items = array();
    for ($i= 0;$i< count($items); $i++){
        $_items[$keys[$i]]=$items[$i];
//        echo $keys[$i].":".$items[$i]."\n";
    }
    $_records = $_records."{\"create\":{}}\n".json_encode($_items)."\n";
}
//echo $_records."\n";

$url = Config::$serverurl_es.'/net_log/log/_bulk?pretty';
putLog("url:".$url);
$resRaw = http_request($url, $_records);

putLog($resRaw);
//echo $resRaw."\n";
$res = json_decode($resRaw, true);


if(isset($res["errors"])){
    if($res["errors"] == false){
        echo "{\"code\":0".",\"took\":".$res["took"].",\"total\":".count($res["items"]).",\"data\":\"批量导入成功\"}";
    }else{
        echo "{\"code\":1,\"data\":\"部分执行失败\"}";
    }
}else{
    echo "{\"code\":1,\"data\":\"执行失败\"}";
}


//echo "errors:".($res["errors"] == true);
//echo "errors:".var_dump($res["errors"]);


?>


