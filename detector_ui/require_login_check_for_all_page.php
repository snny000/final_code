<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__).'/data/get.json.from.server.php');
require_once(dirname(__FILE__).'/service/service.php');
//php验证登录
//session_start();
if (!isset($_SESSION)) {
    session_start();
}
putLog("SESSION_loginid:".$_SESSION['loginid']);
if (!isset($_SESSION['loginid'])){
    putLog("not SESSION_loginid goto:Location:/login.php");
    header('Location:/login.php');
    exit();
}else{

    setcookie(session_name(), session_id(), time()+Config::$cookie_timeout, '/');

}
?>
