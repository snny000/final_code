


<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
//require_once(dirname(__FILE__).'/../model/User.class.php');
require_once(dirname(__FILE__).'/../model/Code.class.php');
require_once(dirname(__FILE__).'/../data/get.json.from.server.php');

//type = 0 : ajax
//type = 1 : php







function getGet($para){
    if(!isset($_GET[$para])){
        return "";
    } else {
        return $_GET[$para];
    }
}



function getPost($para){
    if(!isset($_POST[$para])){
        return "";
    } else {
        return $_POST[$para];
    }
}

function getRequest($para){
    if(!isset($_REQUEST[$para])){
        return "";
    } else {
        return $_REQUEST[$para];
    }
}


function getCommon($methodName){
    $check = checkAndUpdateToken();
    if($check->getCode()!=0){
        return $check;
    }
    $url = Config::$serverurl.'/'.$methodName.'.json';
    for ($i = 0; $i<Config::$repost_times; $i++){
        $data = "key=" . session_id() . "&token=" . $_SESSION['token'];
        $resRaw = http_request($url, $data);
        $res = json_decode($resRaw, true);
        $cr = checkRes($res);
        if($cr){
            return $cr;
        }
    }
    return $res;
}


function getCommonPlus($methodName,$data)
{
    //$check = checkAndUpdateToken();
    //if($check->getCode()!=0){
    //    return $check;
    //}
    $url = Config::$serverurl . '/' . $methodName;
    putLog($data);
    putLog($url);
    //for ($i = 0; $i<Config::$repost_times; $i++){
    //$data = "key=111";
    $resRaw = http_request($url, $data);
    putLog($resRaw);

    $res = json_decode($resRaw, true);

    //putLog($res);
    //$cr = checkRes($res);
    //if($cr){
    return $res;
    //}
    //}
    //return $res;
}




function checkRes($res){
    if (empty($res) || $res == null || $res == false) {
        $json = new Code();
        $json->setCode(9002);
        $json->setMsg("无法连接服务器");
        return $json;
        //return '{"code":9002,"msg":"无法连接服务器"}';
    } else if (isset($res["code"]) && ($res["code"] == 90001 || $res["code"] == 90006)) {
        $gt = getToken();
        if($gt->getCode()!=0){
            return $gt;
        } else {
            return null;
        }
    } else {
        return $res;
    }
}




/********************
1、写入内容到文件,追加内容到文件
2、打开并读取文件内容
 ********************/
function putLog($content){
    $file  = dirname(__FILE__).'/../log.txt';//要写入文件的文件名（可以是任意文件名），如果文件不存在，将会创建一个
    if($f  = file_put_contents($file, $content.PHP_EOL,FILE_APPEND)){// 这个函数支持版本(PHP 5)
        return true;
    } else {
        return false;
    }
}
?>