<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');

$t1 = microtime(true);
$start_time = null;
$end_time = null;
$id = null;
$pn=0;
if(isset($_REQUEST["id"])){
    $id =trim($_REQUEST["id"]);
}
if(isset($_REQUEST["start_time"])){
    $start_time =trim($_REQUEST["start_time"]);
}
if(isset($_REQUEST["end_time"])){
    $end_time =trim($_REQUEST["end_time"]);
}
if(isset($_REQUEST["pn"])){
    $pn = trim($_REQUEST["pn"])-1;
}

putLog("id:".$id);
putLog("start_time:".$start_time);
putLog("end_time:".$end_time);

$url = Config::$serverurl_es.'/project2/log/_search?pretty';
//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];

putLog("url:".$url);


$data=array("query" => array("bool"=>array("must"=>array())),
    "from" => $pn, "size"=>10,
    "sort"=>array("test_date" =>array("order"=>"desc")));
if($id){
    $d = array("term"=>array("id"=>$id));
    array_push($data["query"]["bool"]["must"],$d);
    //echo json_encode($d)."<br/>";
}
if($start_time && $end_time) {
    //$s = array("range"=>array("test_date"=>array("gte"=>substr($start_time,1,strlen($start_time)-2),"lte"=>substr($end_time,1,strlen($end_time)-2))));
    $s = array("range"=>array("test_date"=>array("gte"=>$start_time,"lte"=>$end_time)));
    array_push($data["query"]["bool"]["must"],$s);
    //echo json_encode($s)."<br/>";
}

//echo json_encode($data)."<br/>";
putLog("data:".json_encode($data));

$resRaw = http_request($url, json_encode($data));
//echo $resRaw."<br/>";

putLog($resRaw);
//$res = json_decode($resRaw, true);
//putLog($res);
$res = json_decode($resRaw, true);
//echo var_dump($res["hits"]["hits"][0]["_source"]);

$array = array();
$length = count($res["hits"]["hits"]);
for($x=0;$x<$length;$x++) {
    array_push($array,$res["hits"]["hits"][$x]["_source"]);
}

$result =array("took"=>$res["took"],"code"=>0,"total"=>$res["hits"]["total"],"data"=>$array);
echo json_encode($result);
//echo count($res["hits"]["hits"]);
//echo $resRaw;//json_encode($res);

$t2 = microtime(true);

putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');
?>