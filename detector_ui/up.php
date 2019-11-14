<?php

require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');

//putLog('1111111');
//if (isset($_POST['upfile'])) {

/*    putLog($_FILES['upfile']['tmp_name']);
    var_dump($_FILES);
    move_uploaded_file($_FILES['upfile']['tmp_name'], 'up_tmp/'.time().'.dat');
    //header('location: test.php');
    exit;*/
//}

var_dump($_FILES);

//putLog("55".json_encode($_REQUEST));
//putLog("545".$_REQUEST['upfile']);


putLog("44".json_encode($_FILES));


move_uploaded_file($_FILES['upfile']['tmp_name'], 'up_tmp/'.time().'.dat');

?>