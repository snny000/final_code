<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);

require_once(dirname(__FILE__).'/config.php');
require_once(dirname(__FILE__).'/../service/service.php');

function http_request($url, $data = null)
{
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, FALSE);
    //putLog("1111:");

    if (!empty($data)){

        //curl_setopt($curl, CURLOPT_SAFE_UPLOAD, false);
        //putLog("3333".json_encode($data));
        curl_setopt($curl, CURLOPT_POST, 1);


        //curl_setopt($curl, CURLOPT_UPLOAD, 1);//???????????
        curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
    }

    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    $output = curl_exec($curl);
    curl_close($curl);
    return $output;
}


?>