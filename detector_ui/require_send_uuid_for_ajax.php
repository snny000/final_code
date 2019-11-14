<?php
//session_start();
if (!isset($_SESSION)) {
    session_start();
}

if (isset($_SESSION['loginid'])){
putLog("SESSION_loginid action:".$_REQUEST["uu"].'===='.$_SESSION['loginid']);

$_REQUEST["uuid"]=$_SESSION['loginid'];
}else{
putLog("no SESSION_loginid action:".$_REQUEST["uu"]);

}

?>