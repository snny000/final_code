<?php
    Class Config{
        public static $serverurl = "http://192.168.120.175";

        public static $serverurl_document = "http://192.168.120.234:8086"; //外网


       public static $serverurl_detector = "http://127.0.0.1:8089"; //外网
        //public static $serverurl_detector = "http://10.10.6.11";//内网
        #public static $serverurl_detector = "http://127.0.0.1:8080";//虚拟机
        //  public static $serverurl_detector = "http://127.0.0.1:8080";//一部

        //public static $serverurl_spark = "http://192.168.120.112:8088";

        // public static $serverurl_es = "http://192.168.120.75:9200";

        public static $serverurl_director = "http://192.168.120.75:9001"; //外网


        public static $serverurl_es = "http://127.0.0.1:9200";//虚拟机
        //public static $token_timeout = 240;
        public static $cookie_timeout = 3600;
        public static $repost_times = 2;

        

    }
?>
