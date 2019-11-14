<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

$id = $_REQUEST["id"];

?>

<!DOCTYPE html>
<html>
<head>
    <title>告警详情</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

   <!-- <link href="default/css/new.css" rel="stylesheet">
         <link href="default/css/charts-graphs.css" rel="stylesheet">
   -->

     <!-- Datepicker CSS -->
    <!--
    <link rel="stylesheet" type="text/css" href="default/css/datepicker.css">
    <link href="default/fonts/font-awesome.min.css" rel="stylesheet">
    -->

    <!-- HTML5 shiv and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
    <script src="default/js/html5shiv.js"></script>
    <script src="default/js/respond.min.js"></script>
    <![endif]-->

    <link href="css/server.css" rel="stylesheet">
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="css/frame.css" rel="stylesheet">
    <link href="css/product.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">

    <style>
        body {
            background-color: white;
        }

        .chart-row{
            border:solid 1px #E1E6EB;
            margin-left: 15px;
            margin-right: 0px;
            margin-bottom: 15px;
        }

        .chart-size{
            width: auto;height: 270px; /* width: 1080px;height:270px; */
        }

        .sub-title{
            background-color: #F5F6FA;
            font-weight: bold;
        }
    </style>
</head>
<body>
<div id="whole-wrapper">
    <div class="container-whole">
        <div class="container-left">
            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                检测器基本信息
                            </div>
                        </div>
                        <div class="widget-body">
                            <table class="table no-margin">
                                <tbody id="base-form">
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                检测器运行状态
                            </div>
                        </div>
                        <div class="widget-body">
                            <table class="table no-margin">
                                <tbody id="running-form">

                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="container-right">

            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                检测器业务状态
                            </div>
                        </div>
                        <div class="widget-body">
                            <table class="table no-margin">
                                <tbody id="business-form">

                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>



            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                检测器概述
                            </div>
                        </div>
                        <div class="widget-body">
                            <table class="table no-margin">
                                <tbody id="summarize-form">

                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>

<script type="text/javascript">
    buildFrame("");
    var php_id = <?php echo $id;?>;
    $(function () {
        console.log("执行js");
        get();
        //setInterval("get()",100000);
    });

    function get() {
        $.ajax({
            url: "/ajax_action_detector.php?uu=detail&id="+php_id, //ajax请求
            cache: false,
            success: function(data){
                console.log(data);
                buildTbody(data);
            }
        });

        function buildTbody(data){
            var server = JSON.parse(data);
            var msg = server.msg;

            var base_form =
                "<tr class='sub-title'><td><span class='text-muted'>注册信息</td></tr>" +
                "<tr><td><span class='text-muted'> ID：</span>"+msg.id+"</td></tr>" +
                "<tr><td><span class='text-muted'> 设备编号:</span>"+msg.device_id+"</td></tr>" +
                "<tr><td><span class='text-muted'> 磁盘序列号:</span>"+msg.disk_id+"</td></tr>" +
                "<tr><td><span class='text-muted'> 检测器部署的客户单位名:</span>"+msg.organs+"</td></tr>" +
                "<tr><td><span class='text-muted'> 检测器部署的地理位置:</span>"+msg.address+"</td></tr>" +
                "<tr><td><span class='text-muted'> 行政区域:</span>"+msg.address_code+"</td></tr>" +
                "<tr><td><span class='text-muted'> 客户单位联系人:</span>"+list_name(msg.contact)+"</td></tr>"+
                "<tr><td><span class='text-muted'> 审核人:</span>"+msg.op_person+"</td></tr>"+
                "<tr><td><span class='text-muted'> 审核时间:</span>"+msg.op_time+"</td></tr>"+
                "<tr><td><span class='text-muted'> 未通过原因:</span>"+msg.register_message+"</td></tr>"+
                "<tr><td><span class='text-muted'> 磁盘信息:</span>"+list_diskid(msg.disk_info)+"</td></tr>"+
                "<tr class='sub-title'><td><span class='text-muted'>认证信息</td></tr>" +
                "<tr><td><span class='text-muted'> 最后认证时间:</span>"+msg.auth_time+"</td></tr>"+
                "<tr><td><span class='text-muted'> 认证失败原因:</span>"+msg.message+"</td></tr>"
           // $("tbody#base-form").html(base_form);
            $("tbody#base-form").html(base_form);

            var business_form =
                "<tr class='sub-title'><td><span class='text-muted'>网卡连通性信息</td></tr>" +
                "<tr><td><span class='text-muted'> 设备编号:</span>"+msg.device_id+"</td></tr>" +
                "<tr><td>"+list_networkcard(msg.networkcard)+"</td></tr>"+
                "<tr class='sub-title'><td><span class='text-muted'>模块信息</td></tr>"+
                "<tr><td>"+list_module(msg)+"</td></tr>"+
                "<tr class='sub-title'><td><span class='text-muted'>异常状态信息</td></tr>"+
                "<tr><td>"+list_suspected(msg.suspected_status)+"</td></tr>"

            // $("tbody#base-form").html(base_form);
            $("tbody#business-form").html(business_form);

            var running_form =
                "<tr><td><span class='text-muted'> 设备编号:</span>"+msg.device_id+"</td></tr>" +
                "<tr><td>"+list_cpu(msg.run_resource.cpu)+"</td></tr>"+
                "<tr><td><span class='text-muted'> 磁盘整体可用空间:</span>"+msg.run_resource.disk+"</td></tr>" +
                "<tr><td><span class='text-muted'> 内存利用率:</span>"+msg.run_resource.mem+"</td></tr>"
            $("tbody#running-form").html(running_form);
           // run_resource
        }

        function list_name(contact){
            var str = "<table class='table table-condensed'><tr><td>姓名</td><td>工作</td><td>电话</td><td>邮箱</td></tr>"
            for(var i=0;i<contact.length;i++){
                str  = str  + "<tr><td>"+ contact[i].name + "</td><td>"+
                    contact[i].job + "</td><td>"+
                    contact[i].phone + "</td><td>"+
                    contact[i].email + "</td></tr>"
            }
            str += "</table>";
            return str;
        }

        function list_diskid(disk_info){
            var str = "<table class='table table-condensed'><tr><td>磁盘序列号</td><td>磁盘大小</td></tr>"
            for(var i=0;i<disk_info.length;i++){
                str  = str  + "<tr><td>"+ disk_info[i].disk_id + "</td><td>"+disk_info[i].size + "</td></tr>"
            }
            str += "</table>";
            return str;
        }

        function list_networkcard(networkcard){
            var str = ""
            for(var i=0;i<networkcard.length;i++) {
                str = str +
                "<span class='text-muted'> 网卡序列号:</span>" + networkcard[i].networkcard_seq +
                "<table class='table table-condensed'>"+
                "<tr><td><span class='text-muted'> 网卡状态:</span>" + networkcard[i].networkcard_stat + "</td></tr>" +
                "<tr><td><span class='text-muted'> 数据流量:</span>" + networkcard[i].networkcard_flow + "</td></tr>" +
                "<tr><td><span class='text-muted'> 无法处理的报文数:</span>" + networkcard[i].networkcard_error + "</td></tr>" +
                "<tr><td><span class='text-muted'> 丢包个数:</span>" + networkcard[i].networkcard_drop + "</td></tr>" +
                "<tr><td><span class='text-muted'> 采集时长:</span>" + networkcard[i].cap_time + "</td></tr>" +
                 "</table>";
            }
            return str;
        }

        function list_module(msg){
            var str = "<table class='table table-condensed'>" +
                "<tr><td>功能模块</td><td>状态</td><td>策略模块</td><td>版本信息</td></tr>"+
                "<tr><td rowspan ='3'>攻击窃密检测</td><td rowspan ='3'>"+msg.alarm_status+"</td><td>木马攻击监测策略</td><td>"+msg.trojan_version+"</td></tr>"+
                "<tr><td>漏洞利用监测策略</td><td>"+msg.attack_version+"</td></tr>"+
                "<tr><td>恶意程序监测策略</td><td>"+msg.pefile_version+"</td></tr>"+
                "<tr><td>未知攻击检测</td><td>"+msg.abnormal_status+"</td><td>未知攻击上报策略</td><td>"+msg.abnormal_version+"</td></tr>"+
                "<tr><td rowspan ='2'>违规泄密检测</td><td rowspan ='2'>"+msg.sensitive_status+"</td><td>内容监测策略</td><td>"+msg.sensitive_file_version+"</td></tr>"+
                "<tr><td>压缩文件监测策略</td><td>"+msg.compress_file_version+"</td></tr>"+
                "<tr><td rowspan ='4'>目标侦听</td><td rowspan ='4'>"+msg.object_listen_status+"</td><td>IP侦听监测策略</td><td>"+msg.ip_listen_version+"</td></tr>"+
                "<tr><td>域名侦听监测策略</td><td>"+msg.domain_listen_version+"</td></tr>"+
                "<tr><td>URL侦听监测策略</td><td>"+msg.url_listen_version+"</td></tr>"+
                "<tr><td>帐号侦听监测策略</td><td>"+msg.account_listen_version+"</td></tr>"+
                "<tr><td rowspan ='6'>网络行为审计</td><td rowspan ='6'>"+msg.net_audit_status+"</td><td>通联关系监测策略</td><td>"+msg.net_log_version+"</td></tr>"+
                "<tr><td>活跃IP监测策略</td><td>"+msg.active_ip_version+"</td></tr>"+
                "<tr><td>协议流量监测策略</td><td>"+msg.flow_stats_version+"</td></tr>"+
                "<tr><td>应用行为监测策略</td><td>"+msg.app_behavior_version+"</td></tr>"+
                "<tr><td>应用行为web过滤策略</td><td>"+msg.app_behavior_web_version+"</td></tr>"+
                "<tr><td>应用行为DNS过滤策略</td><td>"+msg.app_behavior_dns_version+"</td></tr>"
            str += "</table>";
            return str;
        }

        function list_suspected(info){
            var str = "<table class='table table-condensed'><tr><td>异常类型</td><td>异常产生时间</td><td>告警级别</td><td>事件描述</td></tr>"
            for(var i=0;i<info.length;i++){
                str  = str  + "<tr><td>"+ info[i].event_type + "</td><td>"+
                    info[i].time + "</td><td>"+
                    info[i].risk + "</td><td>"+
                    info[i].msg + "</td></tr>"
            }
            str += "</table>";
            return str;
        }

        function list_cpu(info){
            var str = "<table class='table table-condensed'><tr><td>CPU_id</td><td>cpu使用率</td></tr>"
            for(var i=0;i<info.length;i++){
                str  = str  + "<tr><td>"+ info[i].name + "</td><td>"+
                    info[i].cpu_usage + "</td></tr>"
            }
            str += "</table>";
            return str;
        }
    }
</script>
</body>
</html>

