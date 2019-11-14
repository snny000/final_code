<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);


require_once(dirname(__FILE__).'/data/get.json.from.server.php');

function getParam($para){
    if(!isset($_REQUEST[$para])){
        return null;
    } else {
        return $_REQUEST[$para];
    }
}

function term(&$data,$key,$value){ //过滤语句
    if($value){
        $d = array("term"=>array($key=>$value));
        array_push($data["query"]["bool"]["must"],$d);
//        echo json_encode($d)."<br/>";
//        echo json_encode($data)."<br/>";
    }
}

function wildcard(&$data,$key,$value){ //通配符过滤语句
    if($value){
        $d = array("wildcard"=>array($key=>$value));
        array_push($data["query"]["bool"]["must"],$d);
//        echo json_encode($d)."<br/>";
//        echo json_encode($data)."<br/>";
    }
}

//echo "-------------".file_get_contents("php://input")."<br/>";

$t1 = microtime(true);

$sip = trim(getParam("sip"));
$sport =trim(getParam("sport"));
$smac = trim(getParam("smac"));
$dip = trim(getParam("dip"));
$dport = trim(getParam("dport"));
$dmac = trim(getParam("dmac"));
$protocol = trim(getParam("protocol"));
$app = trim(getParam("app"));
$start_time = trim(getParam("start_time"));
$end_time = trim(getParam("end_time"));
$size = trim(getParam("size"));
$pn=0;
if(isset($_REQUEST["pn"])){
    $pn = $_REQUEST["pn"]-1;
}

$url = Config::$serverurl_es.'/app_behavior/log/_search?pretty';
//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];

putLog("url:".$url);

if(!$size){
    $size = 10;
}
$data=array("query" => array("bool"=>array("must"=>array())),
    "from" => $pn*$size);
$data["sort"]=array("time" =>array("order"=>"desc"));
$data["size"]=$size; //每一页的数据量

if($start_time && $end_time) {
    //$s = array("range"=>array("test_date"=>array("gte"=>substr($start_time,1,strlen($start_time)-2),"lte"=>substr($end_time,1,strlen($end_time)-2))));
    $s = array("range"=>array("time"=>array("gte"=>$start_time,"lte"=>$end_time)));
    array_push($data["query"]["bool"]["must"],$s);
    //echo json_encode($s)."<br/>";
}

wildcard($data,"sip",$sip);
term($data,"sport",$sport);
term($data,"smac",$smac);
wildcard($data,"dip",$dip);
term($data,"dport",$dport);
term($data,"dmac",$dmac);
term($data,"protocol",$protocol);
term($data,"app",$app);

//echo json_encode($data)."<br/>";
putLog("---data:".json_encode($data));


$resRaw = http_request($url, json_encode($data));
//putLog($resRaw);
//$res = json_decode($resRaw, true);
//putLog($res);
$res = json_decode($resRaw, true);

//echo var_dump($res["hits"]["hits"][0]["_source"]);

$array = array();
$length = count($res["hits"]["hits"]);
for($x=0;$x<$length;$x++) {
    array_push($array,$res["hits"]["hits"][$x]["_source"]);
}

$result =array("code"=>0,"total"=>$res["hits"]["total"],"took"=>$res["took"],"data"=>$array);
echo json_encode($result,JSON_UNESCAPED_SLASHES);

$t2 = microtime(true);

putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');
?>