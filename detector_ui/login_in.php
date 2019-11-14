<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__).'/data/get.json.from.server.php');
require_once(dirname(__FILE__).'/service/service.php');

//$ref = getGet("ref");
//if(empty($ref)){
//    $ref = "summary.php";
//}checkLoginForLoginPage($ref);

//session_start();
if (!isset($_SESSION)) {
    session_start();
}
$_SESSION=array();

$_SESSION['loginid']=$_REQUEST["loginid"];
putLog("loginid:".$_SESSION['loginid']);

setcookie(session_name(), session_id(), time()+Config::$cookie_timeout, '/');



?>
