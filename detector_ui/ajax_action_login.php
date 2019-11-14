<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/data/get.json.from.server.php');



//$data="loginid=".$uuid."&password=".$password."&key=".session_id()."&token=".$_SESSION['token'];

//$data = file_get_contents("php://input"); //接收POST数据
//$xml = simplexml_load_string($input); //提取POST数据为simplexml对象
$t1 = microtime(true);


//unset($_REQUEST["uu"]);
//unset($_REQUEST["random"]);
$data = http_build_query($_REQUEST);

//putLog("getPost loginid:".getPost("loginid"));


//$uu = getGet("uu");

//$arr = explode(".",$uu);
//putLog("uu:".$uu);
//putLog("$_REQUEST:".$_REQUEST);




//$data = file_get_contents("php://input");
//putLog($data);

//$arr = str_replace(".","/",$uu,$i);
//putLog("替换数：".$i);

//foreach($arr as $u){

  //  echo $newstr."</br>";
//putLog($arr);

//putLog("arr:".$arr);
//}

//putLog($uu);
$url = Config::$serverurl_detector.'/'.'login/user_login';
//$url = Config::$serverurl_detector.'/'.$arr[0].'/'.$arr[1];
putLog("url:".$url);

putLog("data:".$data);

$resRaw = http_request($url, $data);
//putLog(url);
putLog($resRaw);
//$res = json_decode($resRaw, true);

//putLog($res);

$res = json_decode($resRaw, true);

if (isset($res["code"]) && $res["code"] ==200){
    putLog("code:".$res["code"]);

//session_start();
    if (!isset($_SESSION)) {
        session_start();
    }
    $_SESSION=array();

    $_SESSION['loginid']=getPost("username");
    // $_SESSION['level']=0;

    putLog("getPost[\"username\"]:".getPost("username"));

    putLog("loginid:".$_SESSION['loginid']);
    // putLog("level:".$_SESSION['level']);

    setcookie(session_name(), session_id(), time()+Config::$cookie_timeout, '/');

}


echo $resRaw;
//echo $resRaw;//json_encode($res);

$t2 = microtime(true);
putLog('IP地址是:'.@$_SERVER['REMOTE_ADDR']);
putLog('耗时'.round(($t2-$t1)*1000,1).'毫秒');


?>