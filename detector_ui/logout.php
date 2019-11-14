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
setcookie(session_name(), '', time()-42000, '/');
session_destroy();

putLog("logout!");
header('Location:/login.php');//相对调用该函数的路径
?>
