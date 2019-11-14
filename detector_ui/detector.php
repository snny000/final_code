<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');

require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');


//require_once( 'data/get.json.from.server.php');
//require_once( 'service/service.php');
//$user = new User();
//$user = checkLogin(1, 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>检测器状态管理</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="css/bootstrap-switch.css" rel="stylesheet">
    <link href="css/bootstrap-toggle.min.css" rel="stylesheet">


    <!-- Add custom CSS here -->
    <link href="css/frame.css" rel="stylesheet">
    <link href="css/product.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <link href="css/detector.css" rel="stylesheet">
    <link href="bootstrap-datetimepicker-master/css/bootstrap-datetimepicker.min.css" rel="stylesheet" media="screen">


    <style>
        body {
            background-color: white;
        }

        .widget {
            clear: both;
            margin-top: 0px;
            margin-bottom: 10px;
        }

        .widget .widget-header {
            border: 1px solid #e1e6eb;
            position: relative;
            background-color: #f5f6fa;
            height: 52px;
            padding: 0 15px;
            line-height: 52px;
        }

        .widget .widget-header .title {
            color: #3693cf;
            font-weight: bold;
        }

        /*监控详情页*/
        .widget-header-index {
            border-bottom: 0px solid #e1e6eb !important;
            border-left: 4px solid #328FCA !important;

        }
        .widget-header-index-title {

            text-align: left;
            font-size: 14px;
        }

        ul.dropdown-list-style > li:hover{
            cursor:pointer;
            background-color: #D9D9D9;
        }

        ul.dropdown-list-style> li{
            padding-left: 10px;
            border-bottom: solid 1px #D9D9D9;
            height: 34px;
            line-height: 34px;
        }

        .dropdown-list-style{
            padding: 0px
        }

        .td_8_percent {
            width: 8% !important;
        }

        .date_label{
            float: left;
            margin-top: 5px;
            margin-right: 4px;
        }
        .date_div{
            /*width: 400px;*/
            float: left;
        }





         body {
            background-color: white;
        }

        .widget {
            clear: both;
            margin-top: 0px;
            margin-bottom: 10px;
        }

        .widget .widget-header {
            border: 1px solid #e1e6eb;
            position: relative;
            background-color: #f5f6fa;
            height: 52px;
            padding: 0 15px;
            line-height: 52px;
        }

        .widget .widget-header .title {
            color: #3693cf;
            font-weight: bold;
        }

        /*监控详情页*/
        .widget-header-index {
            border-bottom: 0px solid #e1e6eb !important;
            border-left: 4px solid #328FCA !important;

        }
        .widget-header-index-title {

            text-align: left;
            font-size: 14px;
        }

        ul.dropdown-list-style > li:hover{
            cursor:pointer;
            background-color: #D9D9D9;
        }

        ul.dropdown-list-style> li{
            padding-left: 10px;
            border-bottom: solid 1px #D9D9D9;
            height: 34px;
            line-height: 34px;
        }

        .dropdown-list-style{
            padding: 0px
        }

        .upper-btn-group{
            position: relative;
            display: inline-block;
        }

        .upper-line{
            border-bottom: solid 1px #DDDDDD;
            margin-bottom: 20px;
        }
        .date_div{
            float: left;
        }
        .virtual_group_cls{
            height: 50px;
            width: 10%;
            display: inline-block;
            background: #43BFE3;
            color: white;
            margin-right: 20px;
            line-height: 50px;
            float: left;
            margin: 20px;
            cursor: pointer;
        }
        #topo_tooltip{
            border-radius: 5px;
            background: #43BFE3;
            color: white;
            padding:5px;
        }
        .device-detail {
            /*height: 70%;*/
            position: absolute;
            right: 15px;
            /*background: #428bca;*/
            overflow-y: auto;
            display: none;
            /*transition: 1s;*/
            z-index: 9999;
        }
        .device-detail .panel-primary,.device-detail .panel-heading{
            border-radius: 0;
            margin-bottom: 0;
        }

        .device-detail table{
            font-size: 14px;
        }

        .sub-title{
            background-color: #F5F6FA;
            font-weight: bold;
        }

        .highlightValue{
            color: orange;
            font-size: large;
            font-weight: bold;
        }
        #director-detail{
            width:227px;
        }
        #manage-detail{
            width: 290px;
        }
        #device-detail{
            width:299px;
        }
        #auditModal{
            z-index: 10000;
        }
        #auditModal .modal-dialog{
            width: 80%;
        }
        #auditModal .modal-body{
            text-align: center;
        }
        #auditModal .panel-primary, #auditModal .panel-heading {
            border-radius: 0;
            margin-bottom: 0;
        }
        .step{
            display: inline-block;
            min-width: 10px;
            padding: 5px;
            font-size: 12px;
            font-weight: bold;
            line-height: 1;
            color: #ffffff;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            background-color: orange;
            border-radius: 10px;
        }
        .step:hover{
            color:#000;
            text-decoration:none;
        }

        #auditModal .panel-body{
            display: flex;
            justify-content: space-around;
        }

        #auditModal .panel-body>div{
            width: 49%;
            border: 1px solid #dddddd;
            
        }

        #auditModal .panel-body>div>span{
            color: orange;
            font-weight: bold;
        }
        #cpuPanel table td, #diskPanel table td, #contactPanel table td,#interfacePanel table td{
            border-top: 1px solid #dddddd;
            border-bottom: 1px solid #dddddd;
        }


    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;检测器状态管理
<!--                    <span>&nbsp;&nbsp;检测器审核模式：</span>-->
<!--                    <div class='btn-interval audit_mode' style='display: inline'>-->
<!--                        <input name='audit-checkbox' type='checkbox' id='auditMode' checked/>-->
<!--                    </div>-->
                </h4>

            </div>

        </div>

        <div class="row btn-banner">
                <div class="dropdown dropdown-inline">
                    <button type="button" data-toggle="dropdown"
                            class="btn dropdown-btn dropdown-menu-width"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <span id="contractor" class="pull-left" value="00">所有厂商</span>
                        <i class="fa fa-sort-down pull-right"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                        <?php
                        require_once(dirname(__FILE__) . '/require_contractor_list_for_all_page.php');
                        ?>
                    </ul>
                </div>

                <div class="dropdown btn-interval dropdown-inline">
                    <button type="button" data-toggle="dropdown"
                            class="btn dropdown-btn dropdown-menu-width"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <span id="address_code" class="pull-left" value="0">所有位置</span>
                        <i class="fa fa-sort-down pull-right"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                        <li onclick="selectProtoFwd(this);" value="0">所有位置</li>
                        <li onclick="selectProtoFwd(this);" value="100000">北京</li>
                        <li onclick="selectProtoFwd(this);" value="200000">上海</li>
                        <li onclick="selectProtoFwd(this);" value="510000">广州</li>
                    </ul>
                </div>

                <div class="dropdown btn-interval dropdown-inline">
                    <button type="button" data-toggle="dropdown"
                            class="btn dropdown-btn dropdown-menu-width"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <span id="device_status" class="pull-left" value="0">所有接入状态</span>
                        <i class="fa fa-sort-down pull-right"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                        <li onclick="selectProtoFwd(this);" value="0">所有接入状态</li>
                        <li onclick="selectProtoFwd(this);" value="1">认证成功</li>
                        <li onclick="selectProtoFwd(this);" value="2">暂未审核</li>
                        <li onclick="selectProtoFwd(this);" value="3">审核失败</li>
                        <li onclick="selectProtoFwd(this);" value="4">审核成功</li>
                        <li onclick="selectProtoFwd(this);" value="5">认证失败</li>
                        <li onclick="selectProtoFwd(this);" value="6">禁用</li>
                    </ul>
                </div>

            <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="device_is_effective" class="pull-left" value="-1">是否禁用</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="-1">是否禁用</li>
                    <li onclick="selectProtoFwd(this);" value="1">开启</li>
                    <li onclick="selectProtoFwd(this);" value="0">禁用</li>
                </ul>
            </div>

            <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="is_online" class="pull-left" value="-1">是否在线</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="-1">是否在线</li>
                    <li onclick="selectProtoFwd(this);" value="1">在线</li>
                    <li onclick="selectProtoFwd(this);" value="0">离线</li>
                </ul>
            </div>


        </div>

        <div class="row btn-banner">
            <div class="input-group date form_datetime date_div" style="width: 160px">
                <input id="time" class="form-control" size="16" type="text" value="" readonly placeholder="注册时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>
            <input id="device_id" type="text" class="form-control search-input  btn-interval" placeholder="检测器ID(模糊搜索)">
            <input id="organs" type="text" class="form-control search-input btn-interval" placeholder="部署单位(模糊搜索)">
            <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>

        </div>


        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <!-- <th width="2%">ID</th> -->
                    <th width="8%">检测器编号</th>
                    <th width="8%">版本号</th>
                    <th width="8%">生产厂商</th>
                    <th width="8%">部署位置</th>
                    <th width="8%">部署单位</th>
                    <th width="5%">接入状态</th>
                    <th width="8%">最后告警时间</th>
                    <th width="8%">注册时间时间</th>
                    <th width="6%">在线状态</th>
                    <th width="6%">禁用操作</th>
                    <th width="4%">操作</th>


                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
                    <td>
                        <div class="pull-left">

                            <button class="btn btn-default btn-sm" id="refresh">刷新</button>
                            <button class="btn btn-default btn-sm" id="export" onclick="export_file()">导出报表</button>
                            <button resourceid="412" class="btn btn-default btn-sm" id="delete">删除</button>
                            <div class='btn-interval audit_mode' style='height: 30px; display: inline'>
                                <div style='height: 30px; display: inline'>
                                    <input name='audit-checkbox' type='checkbox' id='auditMode'/>
                                    <span style="font-size: 18px"></span>
                                </div>
                            </div>

                        </div>
                            <div class="pull-right">

                            <?php
                            require_once(dirname(__FILE__) . '/require_page_bar_for_all_page.php');
                            ?>

<!--                            <nav id="paginationbox">
                                <span style="vertical-align:10px;">共有<strong id="totalcount"></strong>条，每页显示：<strong>10</strong>条</span>
                                <ul id="pagination" class="pagination pagination-sm" style="margin: 0%;"> </ul>
                            </nav>-->
                        </div>
                    </td>
                </tr>

                </tfoot>
            </table>

        </div>

    </div>
</div>
<!-- /#page-wrapper -->



<div class="modal fade" id="auditModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    审核检测器信息
                </h4>
            </div>
            <div class="modal-body">
                <!--基本信息-->
                <div class="panel panel-primary">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <a data-toggle="collapse" data-parent="#accordion" class="" style="margin-left:60px">①基本信息</a>
                            <a class="step pull-right" onclick="showStep(1)">
                                下一项&nbsp;&nbsp;<i class="fa fa-arrow-circle-right"></i></a>
                        </h3>
                    </div>
                    <div id="basePanel" class="panel-collapse in" style="height: auto;">
                        <div class="panel-body">
                            <div>
                                <span>备案信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <tbody style="display: table-row-group;">
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">设备编号:</span><span key="device_id"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">设备厂商:</span><span key="contractor"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">CA证书号:</span><span key="device_ca"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">产品软件版本号:</span><span key="soft_version"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">检测器部署的客户单位名:</span><span key="organs"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">检测器部署的地理位置:</span><span key="address"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">行政区域编码:</span><span key="address_code"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">内存:</span><span key="mem_total"></span><span>&nbsp;MB</span></td>
                                        </tr>
                                        <!-- <tr style="display: table-row;">
                                            <td><span class="text-muted">所在机房位置:</span><span key="computer_position"></span></td>
                                        </tr> -->
                                    </tbody>
                                </table>
                            </div>
                            <div>
                                <span>上传信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <tbody style="display: table-row-group;">
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">设备编号:</span><span key="device_id"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">设备厂商:</span><span key="contractor"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">CA证书号:</span><span key="device_ca"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">产品软件版本号:</span><span key="soft_version"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">检测器部署的客户单位名:</span><span key="organs"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">检测器部署的地理位置:</span><span key="address"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">行政区域编码:</span><span key="address_code"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">内存:</span><span key="mem_total"></span><span>&nbsp;MB</span></td>
                                        </tr>
                                        <!-- <tr style="display: table-row;">
                                            <td><span class="text-muted">所在机房位置:</span><span key="computer_position"></span></td>
                                        </tr> -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <!--接口-->
                <div class="panel panel-primary" style="display:none">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <a class="step pull-left" style="background-color:orange;" onclick="showStep(0)">
                                <i class="fa fa-arrow-circle-left">&nbsp;&nbsp;</i>上一项</a>
                            <a data-toggle="collapse" data-parent="#accordion" class="">②接口信息</a>
                            <a class="step pull-right" style="background-color:orange;" onclick="showStep(2)">
                                下一项&nbsp;&nbsp;<i class="fa fa-arrow-circle-right"></i></a>
                        </h3>
                    </div>
                    <div id="interfacePanel" class="panel-collapse in" style="height: auto;">
                        <div class="panel-body">
                            <div>
                                <span>备案信息:</span>
                                <!--<table class="table" style="margin-bottom:0px">
                                    <tbody style="display: table-row-group;">
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">IP地址:</span><span key="ip"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">MAC地址:</span><span key="mac"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">子网掩码:</span><span key="netmask"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">网关地址:</span><span key="gateway"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">是否为管理端口:</span><span key="manage"></span></td>
                                        </tr>
                                    </tbody>
                                </table>-->
                                <table class="table" style="margin-bottom:0px;word-wrap:break-word;word-break:break-all;">
                                    <thead>
                                        <tr>
                                            <td width="20%">IP地址</td>
                                            <td width="20%">MAC地址</td>
                                            <td width="20%">子网掩码</td>
                                            <td width="20%">网关地址</td>
                                            <td width="20%">管理端口</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                    </tbody>
                                </table>
                            </div>
                            <div>
                                <span>上传信息:</span>
                                <!--<table class="table" style="margin-bottom:0px">
                                    <tbody style="display: table-row-group;">
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">IP地址:</span><span key="ip"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">MAC地址:</span><span key="mac"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">子网掩码:</span><span key="netmask"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">网关地址:</span><span key="gateway"></span></td>
                                        </tr>
                                        <tr style="display: table-row;">
                                            <td><span class="text-muted">是否为管理端口:</span><span key="manage"></span></td>
                                        </tr>
                                    </tbody>
                                </table>-->
                                <table class="table" style="margin-bottom:0px;word-wrap:break-word;word-break:break-all;">
                                    <thead>
                                        <tr>
                                            <td width="20%">IP地址</td>
                                            <td width="20%">MAC地址</td>
                                            <td width="20%">子网掩码</td>
                                            <td width="20%">网关地址</td>
                                            <td width="20%">管理端口</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!--CPU信息-->
                <div class="panel panel-primary" style="display:none">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <a class="step pull-left" style="background-color:orange;" onclick="showStep(1)">
                                <i class="fa fa-arrow-circle-left">&nbsp;&nbsp;</i>上一项</a>
                            <a data-toggle="collapse" data-parent="#accordion" class="">③CPU信息</a>
                            <a class="step pull-right" style="background-color:orange;" onclick="showStep(3)">
                                下一项&nbsp;&nbsp;<i class="fa fa-arrow-circle-right"></i></a>
                        </h3>
                    </div>
                    <div id="cpuPanel" class="panel-collapse in" style="height: auto;">
                        <div class="panel-body">
                            <div>
                                <span>备案信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <thead>
                                        <tr>
                                            <td>CPU编号</td>
                                            <td>CPU核心数</td>
                                            <td>CPU主频</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                    </tbody>
                                </table>
                            </div>
                            <div>
                                <span>上传信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <thead>
                                        <tr>
                                            <td>CPU编号</td>
                                            <td>CPU核心数</td>
                                            <td>CPU主频</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                        
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!--磁盘信息-->
                <div class="panel panel-primary" style="display:none">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <a class="step pull-left" style="background-color:orange;" onclick="showStep(2)">
                                <i class="fa fa-arrow-circle-left">&nbsp;&nbsp;</i>上一项</a>
                            <a data-toggle="collapse" data-parent="#accordion" class="">④磁盘信息</a>
                            <a class="step pull-right" style="background-color:orange;" onclick="showStep(4)">
                                下一项&nbsp;&nbsp;<i class="fa fa-arrow-circle-right"></i></a>
                        </h3>
                    </div>
                    <div id="diskPanel" class="panel-collapse in" style="height: auto;">
                        <div class="panel-body">
                            <div>
                                <span>备案信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <thead>
                                        <tr>
                                            <td>磁盘序列号</td>
                                            <td>磁盘大小</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                    </tbody>
                                </table>
                            </div>
                            <div>
                                <span>上传信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <thead>
                                        <tr>
                                            <td>磁盘序列号</td>
                                            <td>磁盘大小</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                        
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!--联系人信息-->
                <div class="panel panel-primary" style="display:none">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <a class="step pull-left" style="background-color:orange;" onclick="showStep(3)">
                                <i class="fa fa-arrow-circle-left">&nbsp;&nbsp;</i>上一项</a>
                            <a data-toggle="collapse" data-parent="#accordion" class="">⑤联系人信息</a>
                            <a class="step pull-right" style="background-color:orange;" onclick="showStep(5)">
                                下一项&nbsp;&nbsp;<i class="fa fa-arrow-circle-right"></i></a>
                        </h3>
                    </div>
                    <div id="contactPanel" class="panel-collapse in" style="height: auto;">
                        <div class="panel-body">
                            <div>
                                <span>备案信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <thead>
                                        <tr>
                                            <td>姓名</td>
                                            <td>工作</td>
                                            <td>电话</td>
                                            <td>邮箱</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                    </tbody>
                                </table>
                            </div>
                            <div>
                                <span>上传信息:</span>
                                <table class="table" style="margin-bottom:0px">
                                    <thead>
                                        <tr>
                                            <td>姓名</td>
                                            <td>工作</td>
                                            <td>电话</td>
                                            <td>邮箱</td>
                                        </tr>
                                    </thead>
                                    <tbody style="display: table-row-group;">
                                        
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!--填写审核信息-->
                <div class="panel panel-primary" style="display:none">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <a class="step pull-left" style="background-color:orange;" onclick="showStep(4)">
                                <i class="fa fa-arrow-circle-left">&nbsp;&nbsp;</i>上一项</a>
                            <a data-toggle="collapse" data-parent="#accordion" class="">确认审核信息</a>
                        </h3>
                    </div>
                    <div id="contactPanel" class="panel-collapse in" style="height: auto;">
                        <div class="panel-body">
                                    <input id="auditDeviceId" style="display:none"/>
                                    <p>
                                    <span>审核状态:</span>
                                    <select id="is_audit" class="form-control search-input">
                                        <option value="0">审核通过</option>
                                        <option value="1">审核不通过</option>
                                    </select>
                                    </p>
                                    <p>
                                        <span>审核备注:</span>
                                        <input id="audit_detail" type="text" class="form-control search-input" placeholder="审核备注">
                                    </p>
                                    <p>
                                        <button resourceid='352' type="button" class="btn btn-primary" onclick="submitAuditCenter()"><i class="fa fa-check-square-o">&nbsp;&nbsp;</i>提交</button>
                                    </p>
                        </div>
                    </div>
                </div>
                
            </div>

            <!--       class="modal-footer"-->

            <div class="modal-footer">
                <!--<button id="resourceSubmit" type="button" class="btn btn-primary">确定</button>-->
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->











<!-- 模态框（Modal） -->
<!-- <div class="modal fade" id="checkModal" tabindex="-1" role="dialog" aria-labelledby="checkLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    审核
                </h4>
            </div>
            <div class="modal-body" id="check-form">

                <div class="widget no-margin">
                    <div class="widget-header widget-header-index">
                        <div class="title widget-header-index-title">
                            基本信息
                        </div>
                    </div>
                    <div>
                        <table class="table no-margin modal-form">
                            <tbody id="base-form">

                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="btn-group" role="group" id="ischeck" style="margin-top: 10px;width: 100%">
                    <button type="button" class="btn btn-default condition-btn singlechoose active" value="0" style="width: 50%">审核通过</button>
                    <button type="button" class="btn btn-default condition-btn singlechoose" value="1" style="width: 50%">审核不通过</button>
                </div>
                <div style="margin-top: 10px">
                   <span> 审核人:</span> <input id="op_person" type="text" class="search-input form-control" style="width:100%!important;";>
                    <div style="color:red"></div>
                </div>
                <div style="margin-top: 10px">
                     <span>未通过原因:</span>
                     <textarea id="register_message" style="width:100%;height:80px;resize: vertical;" class="form-control"></textarea>
                    <div style="color:red"></div>
                </div>

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭
                </button>
                <button id="check-submit" type="button" class="btn btn-primary">
                    提交
                </button>
            </div>
        </div>
    </div>
</div> -->

</div>
<div class="modal fade" id="failModal" tabindex="-1" role="dialog" aria-labelledby="failLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    未通过原因
                </h4>
            </div>
            <div class="modal-body">
                <div  id="fail-reason"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div>
    </div>
</div>
<div class="modal fade" id="hintModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    提示框
                </h4>
            </div>
            <div class="modal-body" style="text-align: center">
                <p style="color: red"></p>
                <p></p>
                <p></p>
                <p></p>
            </div>
            <div id="new_label_div" style="display: none;text-align: center;">
                <span>新备注标签1：</span> <input id="new_label" type="text" class="form-control" style="width: 250px !important;display: inline-block !important;">
                <div style="color:red"></div>
            </div>


            <!--       class="modal-footer"-->

            <div class="modal-footer">
                <button id="delSubmit" type="button" class="btn btn-primary">确定</button>

                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>

            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>
<!-- /#wrapper -->

<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/bootstrap-switch.js"></script>

<script src="js/bootstrap-toggle.min.js"></script>


<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>
<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script>
    buildFrame("menu-detector");
    $('.form_datetime').datetimepicker({
        language:  'zh-CN',
        minView: "month",
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayBtn: true,
    });

    $('.audit_mode span').html(helper_ele);
    $('.audit_mode span i.hint-helper').attr("value", detector_audit_mode);

    function export_file() {
        //  window.location.href = "detector_detail.php?id=" + id;

        var file_path = "/detector/export";
        var file_name = "检测器统计报表.xlsx";

        window.location.href ="/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+"";


        //post('detector_detail.php',{id:id});
    }


    function selectProtoFwd(obj) {
        $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
        $(obj).parent().parent().find("span:first").text($(obj).text());
        //$("#"+id).attr("value",$(obj).attr("value"));
       // $("#"+id).text($(obj).text());
    }

    $('button.condition-btn.singlechoose').click(function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
    })

    var option = {
      //  totalPages: totalPages,
        visiblePages: 3,
        first: "<<",
        prev: "<",
        next: ">",
        last: ">>",
        onPageClick: function (event, page){
            $.ajax({
                url: option.myurl+"&pn="+page,
                type: "post",
                data: option.searchParam,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200) {

                        List(ret["msg"]);
                    } else if (ret["code"] == 20000) {
                        $("#maintable tbody tr").remove();
                        $("<tr><td colspan='8' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
                    }else if (ret["code"] == 9001){
                        window.location.href = "login.php?ref="+window.location.href;
                    }else{
                        alert(ret["msg"]);
                    }
                },
                beforeSend: function () {
                    $("#maintable tbody tr").remove();
                    $("#maintable tbody").append("<tr><td colspan=" + col_size + "  style='text-align: center'><img src='images/loading.gif'></td></tr>")
                },
                error: function () {
                    alert("无法连接服务器");
                }
            });

        }
    }

    function pagination(totalcount,url,startPage,searchParam){
        var totalPages = 0;
        if(totalcount == 0){
            totalPages = 1; //0条数据会报错
        }else{
            totalPages = Math.ceil(totalcount/p_size);
        }
        option["totalPages"] = totalPages
        option["myurl"] = url
        option["startPage"] = startPage
        option["searchParam"] = searchParam
        //console.log(option)
        $('#pagination').twbsPagination(option);
    }

/*

    $("#chk_all1,#chk_all2").click(function(){
        if(this.checked){
            $("table :checkbox").prop("checked", true);
        }else{
            $("table :checkbox").prop("checked", false);
        }
    });
*/


    function detail(id) {//查看详情
      //  window.location.href = "detector_detail.php?id=" + id;


        //window.open("detector_detail.php?id=" + id);


        post_blank('detector_detail.php',{id:id});
    }

    function check(id){
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.detail&id="+id, //ajax请求
            type: "post",
            success: function(data){
                console.log(data)
                var server = JSON.parse(data);



                var msg = server.msg;
                var base_form = "<tr style='display: none'><td><span class='text-muted'> ID：</span><span id='check_id'>"+msg.id+"</span></td></tr>" +
                    "<tr><td><span class='text-muted'> 设备编号:</span>"+msg.device_id+"</td></tr>" +
                    "<tr><td><span class='text-muted'> 设备厂商:</span>"+contractorMap[msg.contractor]+"</td></tr>" +
                    "<tr><td><span class='text-muted'> 产品软件版本号:</span>"+msg.soft_version+"</td></tr>" +
                    "<tr><td><span class='text-muted'> 检测器部署的客户单位名:</span>"+msg.organs+"</td></tr>" +
                    "<tr><td><span class='text-muted'> 检测器部署的地理位置:</span>"+msg.address+"</td></tr>" +
                    "<tr><td><span class='text-muted'> 行政区域:</span>"+msg.address_code+"</td></tr>" +
                    "<tr><td><span class='text-muted'> 客户单位联系人:</span>"+(msg.contact.length==0?" 无":list_name(msg.contact))+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 设备配置信息:</span>"+(msg.interface.length==0?" 无":list_interface(msg.interface))+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 内存总数:</span>"+msg.mem_total+"</td></tr>"+
                    "<tr><td><span class='text-muted'> CPU信息:</span>"+(msg.cpu_info.length==0?" 无":list_cpu(msg.cpu_info))+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 磁盘信息:</span>"+(msg.disk_info.length==0?" 无":list_disk(msg.disk_info))+"</td></tr>"
                // $("tbody#base-form").html(base_form);
                $("tbody#base-form").html(base_form);
            }
        });
    }

    function list_name(contact){
        var str = "<table class='table table-condensed modal-form'><tr><td>姓名</td><td>工作</td><td>电话</td><td>邮箱</td></tr>"
        for(var i=0;i<contact.length;i++){
            str  = str  + "<tr><td>"+ contact[i].name + "</td><td>"+
                contact[i].position + "</td><td>"+
                contact[i].phone + "</td><td>"+
                contact[i].email + "</td></tr>"
        }
        str += "</table>";
        return str;
    }

    function list_disk(disk_info){
        var str = "<table class='table table-condensed modal-form'><tr><td>磁盘序列号</td><td>磁盘大小</td></tr>"
        for(var i=0;i<disk_info.length;i++){
            str  = str  + "<tr><td>"+ disk_info[i].serial + "</td><td>"+disk_info[i].size + "</td></tr>"
        }
        str += "</table>";
        return str;
    }

    function list_interface(info){
        var str = "<table class='table table-condensed modal-form'><tr><td>IP地址</td><td>网关地址</td></tr>"  ///<td>网卡名</td>
        for(var i=0;i<info.length;i++){
            str  = str  + "<tr><td>"+    /*<td>"+ info[i].name + "</td>*/
                info[i].ip + "</td><td>"+
                info[i].mac + "</td></tr>"
        }
        str += "</table>";
        return str;
    }

    function list_cpu(info){
        var str = "<table class='table table-condensed modal-form'><tr><td>核心数</td><td>主频</td></tr>"
        for(var i=0;i<info.length;i++){
            str  = str  + "<tr><td>"+ info[i].core + "</td><td>"+
                info[i].clock + "</td></tr>"
        }
        str += "</table>";
        return str;
    }

    $("#check-submit").click(function(){

            var ischeck = true

            var op_person = $("#op_person").val()

            var register_message = $("#register_message").val()

            if(op_person == ""){
                $("#op_person").next("div").html("审核人不能为空")
                ischeck = false
            }else{
                $("#op_person").next("div").html("")
            }




            if($("#ischeck .active").prop("value")=='1' && register_message == ""){
                $("#register_message").next("div").html("未通过原因不能为空")
                ischeck = false
            }else{
                $("#register_message").next("div").html("")
            }

            if(!ischeck){
                return;
            }






        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.permit",
            type: "post",
            data: {id:$("#check_id").text(),type:$("#ischeck .active").prop("value"),op_person:$("#op_person").val(),register_message:$("#register_message").val()},
            success:function(data) {
                var ret = JSON.parse(data);
                console.log(ret)
                refresh()  //审核完刷新

            }
        })
        $("#checkModal").modal('hide');
    }
    )

    function fail(status,id){
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.detail&id="+id, //ajax请求
            type: "post",
            data:null,
            cache: false,
            success: function(data){
                var server = JSON.parse(data);
                var msg = server.msg;
                console.log(status)
                if (status == 3){
                    $("#fail-reason").html("审核未通过:"+msg.register_message)
                } else {
                    $("#fail-reason").html("认证未通过:"+msg.message)
                }
            }
        });
    }

    /**
     *
     * @param status 设备接入状态  {1:'认证成功',2:'暂未审核',3:'审核失败',4:'审核成功',5:'认证失败',6:'禁用'};
     * @param id
     * @returns {*}
     */
    function getStrManipulation(status, id,device_id) {
        switch (status) {
            case 1:
                return "<a href=\"javascript:void(0);\" class=\"fa fa-bars\" onclick=\"detail(" + id + ")\">详情</a>";
            case 2:
                return "<a href=\"javascript:void(0);\" data-toggle=\"modal\" data-target=\"#checkModal\" onclick=\"auditDetector("+ id +"," + device_id + ")\">审核</a>";
            case 3:
                return "<a href=\"javascript:void(0);\" data-toggle=\"modal\" data-target=\"#checkModal\" onclick=\"auditDetector("+ id +"," + device_id + ")\">审核</a> &nbsp; <a href=\"#;\" data-toggle=\"modal\" data-target=\"#failModal\" onclick=\"fail("+ status +"," + id + ")\">查看</a>";
            case 4:
                return "<a href=\"#;\" data-toggle=\"modal\" data-target=\"#failModal\" onclick=\"fail("+ status +"," + id + ")\">查看</a>";
//                if(auth_frequency == 0){
//                    return "<a href=\"#;\" data-toggle=\"modal\" data-target=\"#failModal\" onclick=\"fail("+ status +"," + id + ")\">暂未认证</a>";
//                }else{
//                    return "<a href=\"#;\" data-toggle=\"modal\" data-target=\"#failModal\" onclick=\"fail("+ status +"," + id + ")\">认证失败</a>";
//                }
            case 5:
                return "<a href=\"#;\" data-toggle=\"modal\" data-target=\"#failModal\" onclick=\"fail("+ status +"," + id + ")\">查看</a>";
            case 6:
                return "<span disabled='true' style='color: #F00;'>已禁用</span>";
            default:
                return "<a href=\"javascript:void(0);\"  class=\"fa fa-bars\" onclick=\"detail(" + id + ")\">详情</a>";
        }
    }


    // 审核检测器
    function auditDetector(id,device_id){
        console.log(id,device_id)
        $('#auditDeviceId').val(id); //赋值到隐藏的检测器框里
        $('#is_audit').val('0');
        $('#audit_detail').val('');
        showStep(0);
        // $('#auditCenterId').val(center_id);
        // $('#auditNodeId').val(node_id);
        // 上传的检测器的信息
        $.ajax({
                url:'/ajax_action_detector.php?uu=detector.detail&id='+id,
                success:function(data){
                    var msg = JSON.parse(data)['msg'];
                    initAuditPart(msg,1);
                }
        })
        // 备案检测器信息
        $.ajax({
                url:'/ajax_action_detector.php?uu=detector_info.detail&detector_id='+device_id,
                success:function(data){
                    var ret = JSON.parse(data);
                    if(ret.code!=200){
                        alert('检测器备案信息不存在，不能审核！');
                        $('#auditModal').modal('hide');
                    }
                    var msg = JSON.parse(data)['msg'];
                    initAuditPart(msg,0,id);
                    compareCenter();
                }
        })

        $('#auditModal').modal('show');
    }

    function compareCenter() {
        // 比对信息标红
        $('#auditModal table tbody td span[key]').css('color','');
        $('#auditModal table tbody td').css('color','');

        var base = $('#basePanel table:eq(1) span[key]');
        $.each(base, function (i) {
            if ($('#basePanel table:eq(1) span[key]:eq(' + i + ')').html() != $('#basePanel table:eq(0) span[key]:eq(' + i + ')').html()) {
                $('#basePanel table:eq(1) span[key]:eq(' + i + ')').css('color', 'red');
            }
        });

        var interface = $('#interfacePanel table:eq(1) tbody td');
        $.each(interface, function (i) {
            if ($('#interfacePanel table:eq(1) tbody td:eq(' + i + ')').html() != $('#interfacePanel table:eq(0) tbody td:eq(' + i + ')').html()) {
                $('#interfacePanel table:eq(1) tbody td:eq(' + i + ')').css('color', 'red');
            }
        });

        var cpu = $('#cpuPanel table:eq(1) tbody td');
        $.each(cpu, function (i) {
            if ($('#cpuPanel table:eq(1) tbody td:eq(' + i + ')').html() != $('#cpuPanel table:eq(0) tbody td:eq(' + i + ')').html()) {
                $('#cpuPanel table:eq(1) tbody td:eq(' + i + ')').css('color', 'red');
            }
        });

        var disk = $('#diskPanel table:eq(1) tbody td');
        $.each(disk, function (i) {
            if ($('#diskPanel table:eq(1) tbody td:eq(' + i + ')').html() != $('#diskPanel table:eq(0) tbody td:eq(' + i + ')').html()) {
                $('#diskPanel table:eq(1) tbody td:eq(' + i + ')').css('color', 'red');
            }
        });

        var contact = $('#contactPanel table:eq(1) tbody td');
        $.each(contact, function (i) {
            if ($('#contactPanel table:eq(1) tbody td:eq(' + i + ')').html() != $('#contactPanel table:eq(0) tbody td:eq(' + i + ')').html()) {
                $('#contactPanel table:eq(1) tbody td:eq(' + i + ')').css('color', 'red');
            }
        });
    }
    function showStep(step){
        $('#auditModal .panel').hide();
        $('#auditModal .panel').eq(step).show();
    }

    function getcontractor(contractor){
        contractor_name = ""
        contractor_dict = {
            '01': '中孚',
            '02': '蓝盾',
            '03': '天融信',
            '04': '鼎普',
            '05': '网安',
            '06': '信工所',
            '07': '网神360',
            '08': '金城'
        }
        contractor_name = contractor_dict[contractor]
        return contractor_name

    }
    function initAuditPart(msg,type,id){

        $('#basePanel table:eq('+type+') span[key=device_id]').html($('#director_node option[value='+msg['device_id']+']').text());
        for(var key in msg){
            if(key == "contractor"){
                contractor_name = getcontractor(msg['contractor'])
                $('#basePanel table:eq('+type+') span[key='+key+']').html(contractor_name)
            }else{
                $('#basePanel table:eq('+type+') span[key='+key+']').html(msg[key])
            }
        }

        /*var interface = msg['interface'][0];
        for(var key in interface){
            if(interface['manage'] == true){
                $('#interfacePanel table:eq('+type+') span[key=manage]').html('是');
            }
            if(interface['manage'] == false){
                $('#interfacePanel table:eq('+type+') span[key=manage]').html('否');
            }
            $('#interfacePanel table:eq('+type+') span[key='+key+']').html(interface[key])
        }*/

        var interface = msg['interface'];
        var interfacetr = "";
        for(var i=0;i<interface.length;i++){
            interfacetr += "<tr>"+
                "<td>"+ interface[i]['ip']+ "</td>"+
                "<td>"+ interface[i]['mac']+ "</td>"+
                "<td>"+ interface[i]['netmask']+ "</td>"+
                "<td>"+ interface[i]['gateway']+ "</td>"+
                "<td>"+ (interface[i]['manage'] == true ? "是": "否") + "</td>"+
                "</tr>"
        }
        $('#interfacePanel table:eq('+type+') tbody').html(interfacetr);

        var cpu = msg['cpu_info'];
        var tr = "";
        for(var i=0;i<cpu.length;i++){
            tr += "<tr>"+
                "<td>"+ cpu[i]['physical_id']+ "</td>"+
                "<td>"+ cpu[i]['core']+ "</td>"+
                "<td>"+ cpu[i]['clock']+ "</td>"+
                "</tr>"
        }
        $('#cpuPanel table:eq('+type+') tbody').html(tr);

        var disk = msg['disk_info'];
        var tr = "";
        for(var i=0;i<disk.length;i++){
            tr += "<tr>"+
                "<td>"+ disk[i]['serial']+ "</td>"+
                "<td>"+ disk[i]['size']+ "</td>"+
                "</tr>"
        }
        $('#diskPanel table:eq('+type+') tbody').html(tr);

        var contact = msg['contact'];
        var tr = "";
        for(var i=0;i<contact.length;i++){
            tr += "<tr>"+
                "<td>"+ contact[i]['name']+ "</td>"+
                "<td>"+ contact[i]['position']+ "</td>"+
                "<td>"+ contact[i]['phone']+ "</td>"+
                "<td>"+ contact[i]['email']+ "</td>"+
                "</tr>"
        }
        $('#contactPanel table:eq('+type+') tbody').html(tr);
    }


    function submitAuditCenter(){
        var isAudit = $('#is_audit').val();
        var auditDetail = $('#audit_detail').val();
        var auditDeviceId = $('#auditDeviceId').val();
        $.ajax({
            url:'/ajax_action_detector.php?uu=detector.permit',
            data:{
                id: auditDeviceId,
                op_person: "admin",
                type: isAudit,
                register_message: auditDetail
            },
            success:function(data){
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert('审核完成!');
                    $('#auditModal').modal('hide');
                }else{
                    alert("审核失败:"+ret.msg);
                }
                $('#manage-detail').hide();
                $('#searchButton').click();
            },
            error:function(){
                alert('审核失败')
            }
        })
    }





    function isSuccessFormat_new(status){
        var device_statusMap={1:'认证成功',2:'暂未审核',3:'审核失败',4:'审核成功',5:'认证失败',6:'禁用'};
        var status_html = $('<span>'+device_statusMap[status]+'</span>')
        switch(status){
            case 1:
                $(status_html).css('color','green');
                break;
            case 2:
                $(status_html).css('color','orange');
                break;
            case 3:
                $(status_html).css('color', 'red');
                break;
            case 4:
                $(status_html).css('color', 'blue');
                break;
            case 5:
                $(status_html).css({'color':'red','font-weight':'300'});
                break;
            case 6:
                $(status_html).css({'color':'red','font-weight':'bold'});
                break;
            default:
                $(status_html).css('color', 'red');
                break;
        }
        return status_html;
    }


    function isonlineFormat_new(status){
        var is_onlineMap={1:'在线',0:'离线'};
        var status_html = $('<span>'+is_onlineMap[status]+'</span>')
        switch(status){
            case 0:
                $(status_html).css('color','red');
                break;
            case 1:
                $(status_html).css('color','green');
                break;
        }
        return status_html;
    }


    $("#maintable tfoot").on('click', '#delete', function(){
        $('#hintModal').find(".modal-title").html("删除提示框");

        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");

        if(checkboxs.size() == 0){
            alert("请选择删除数据");
            return;
        }

        var content = "<p >将删除<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，请确认</p>"
        $('#hintModal').find(".modal-body").html(content)

        var footer = "<button id='delSubmit' type='button' class='btn btn-primary'>确定</button>"+
            "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
        $('#hintModal').find(".modal-footer").html(footer)

        $("#delSubmit").click(function(){
            var carray =new Array()
            var lines = $("#maintable tbody tr");
            var checkboxs = lines.find("input:eq(0):checkbox:checked");
            checkboxs.each(function(){
                carray.push(parseInt($(this).attr("id")))
            })
            console.log("carray:"+carray);
            $.ajax({
                url: "/ajax_action_detector.php?uu=detector.delete",
                type: "post",
                data: {id:JSON.stringify(carray)},
                success:function(data) {
                    var ret = JSON.parse(data);
                    alert(ret['msg']);
                    refresh()
                },
                error: function () {
                    alert("无法连接服务器");
                }
            })

            $('#hintModal').modal('hide')
        })

        $('#hintModal').modal('show')
    })


    /*
    var msgListObj = eval(msgList);
    List(msgListObj); //默认列表
    */

    function List(msgListObj){

        loadAuditMode();

        var address_codeMap={'100000':'北京','200000':'上海','510000':'广州'};
        // var device_statusMap={1:'认证成功',2:'暂未审核',3:'审核失败',4:'审核成功',5:'认证失败',6:'禁用'};

        var imgMap = {
            1: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
            2: "<i class='fa fa-circle' style='color:#5BC0DE; font-size:xx-small ' />",
            3: "&nbsp;&nbsp;<span style='background: #FF9900;padding: 3px;border-radius: 5px; color: white'>置顶</span>"
        }

        var device_status_imgMap = {
            1: "<i class='fa fa-circle' style='color:#5BC0DE; font-size:xx-small ' />",
            2: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
            3: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
            4: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
            5: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
            6: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
            7: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
            8: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>"

        }



        //var _row = $("#content").clone();
        //$("#content").remove();
        $("#maintable tbody tr").remove();

        var _row = $("<tr>" +
            "<td><input type='checkbox' class='checkbox'></td>"+
            "<td ></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();
            var imghtml = '';
            var titlehtml = "<a href = 'detector_detail.php?id="+msgListObj[i].id+"' style='color:#000000'>"+msgListObj[i].device_id+"</a>";


            $.fn.bootstrapSwitch.defaults.size = 'mini';
            $.fn.bootstrapSwitch.defaults.onText = '开启';
            $.fn.bootstrapSwitch.defaults.offText = '禁用';

            if(msgListObj[i].device_is_effective) {
                var operatehtml = getStrManipulation(msgListObj[i].device_status, msgListObj[i].id, msgListObj[i].device_id);
            } else {
                var operatehtml = getStrManipulation(6, msgListObj[i].id, msgListObj[i].device_id);
            }

           // var operatehtml = getStrManipulation(msgListObj[i].device_status, msgListObj[i].id)+"<div><input name='my-checkbox' type='checkbox' data-toggle='toggle' data-size='mini' id="+msgListObj[i].id+" checked /></div>";

            if(msgListObj[i].device_is_effective==1){

                var is_checked="checked"
            }else{

                var is_checked=""
            }
            var switchhtml = "<div><input name='my-checkbox' type='checkbox' id="+msgListObj[i].id+"  "+is_checked+" /></div>";

            var status = isSuccessFormat_new(msgListObj[i].device_status)
            var onlines = isonlineFormat_new(msgListObj[i].is_online)

            row.attr("id",msgListObj[i].id)
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+ ">")
          //  row.find("td:eq(1)").text(msgListObj[i].id);
//            row.find("td:eq(1)").html(device_status_imgMap[msgListObj[i].device_status]+titlehtml);
            row.find("td:eq(1)").html(msgListObj[i].device_id);
            row.find("td:eq(2)").html(msgListObj[i].soft_version);
            row.find("td:eq(3)").text(contractorMap[msgListObj[i].contractor]);
            row.find("td:eq(4)").html(address_codeMap[msgListObj[i].address_code]?address_codeMap[msgListObj[i].address_code]:"未知地区");
            row.find("td:eq(5)").html(msgListObj[i].organs);
            row.find("td:eq(6)").html(status);
            row.find("td:eq(7)").text(msgListObj[i].last_warning_time);
            row.find("td:eq(8)").html(msgListObj[i].register_time);
            row.find("td:eq(9)").html(onlines);
            row.find("td:eq(10)").html(switchhtml);
            row.find("td:eq(11)").html(operatehtml);

            row.show();
            row.appendTo("#maintable tbody");
        }

       // $("[name='my-checkbox']").bootstrapSwitch()

        $("[name='my-checkbox']").bootstrapSwitch({
            onText:"开启",
            offText:"禁用",
            onColor:"success",
            offColor:"warning",
            size:"mini",
            onSwitchChange:function(event,state){
                var type=0
                var module = $(this).parent();
                var select_obj = module.find("[name='my-checkbox']");

                var id = select_obj.attr("id")

                if(state==true){
                    //$(this).val("1");
                    alert('检查器将开启')
                    var comment=prompt("请输入备注","");
                    if(comment==null)
                    {
                        type=0
                        refresh()
                    }
                    else {
                        type=1
                        $.ajax({
                            url: "/ajax_action_detector.php?uu=detector.alert",
                            type: "post",
                            data: {id:id,type:type,comment:comment},
                            success:function(data) {
                                var ret = JSON.parse(data);
                                if(ret.code == 200){
                                    alert("状态切换成功");

                                }else{
                                    alert("状态切换失败");
                                }
                            }
                        })
                    }
                    //$("[name='my-checkbox']").bootstrapSwitch('setState', false);
                }else{
                    //$(this).val("2");
                    alert('检查器将禁用')
                    //$("[name='my-checkbox']").bootstrapSwitch('setState', true);
                    var comment=prompt("请输入备注","");
                    if(comment==null)
                    {
                        type=1
                        refresh()
                    }
                    else {
                        type=0
                        $.ajax({
                            url: "/ajax_action_detector.php?uu=detector.alert",
                            type: "post",
                            data: {id:id,type:type,comment:comment},
                            success:function(data) {
                                var ret = JSON.parse(data);
                                if(ret.code == 200){
                                    alert("状态切换成功");

                                }else{
                                    alert("状态切换失败");
                                }
                            }
                        })
                    }
                }
            }
        })

        rebindChkAll();
    }


    function loadAuditMode() {
        var is_checked = true;
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.audit_mode_show",
            type: "post",
            success: function (data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 200) {
                    $.fn.bootstrapSwitch.defaults.size = 'small';
                    $.fn.bootstrapSwitch.defaults.onText = '人工审核';
                    $.fn.bootstrapSwitch.defaults.offText = '自动审核';
                    is_checked = ret['msg'] == 1 ? true : false;
//                    is_checked = ret['msg'] == 1 ? "checked" : "";
                    console.log(is_checked);

                    $('#auditMode').attr('checked', is_checked);
                }
                else {
                    console.log(ret['msg']);
                }

                $("#auditMode").bootstrapSwitch({
                    onText:"人工审核",
                    offText:"自动审核",
                    onColor:"success",
                    offColor:"info",
                    size:"small",
                    onSwitchChange:function(event,state){
                        var mode = 1;

                        if(state==true){
                            var msg = "检查器审核将切换为人工模式，是否确定？";
                            if (confirm(msg)==true){
                                mode = 1;
                                $.ajax({
                                    url: "/ajax_action_detector.php?uu=detector.audit_mode_alert",
                                    type: "post",
                                    data: {'mode': mode},
                                    success:function(data) {
                                        var ret = JSON.parse(data);
                                        if(ret.code == 200){
                                            alert("模式切换成功");

                                        }else{
                                            alert(ret['msg']);
                                        }
                                    }
                                })
                            } else {
                                mode = 0;
                                refresh();
                            }
                        } else {
                            var msg = "检查器审核将切换为自动模式，是否确定？";
                            if (confirm(msg)==true){
                                mode = 0;
                                $.ajax({
                                    url: "/ajax_action_detector.php?uu=detector.audit_mode_alert",
                                    type: "post",
                                    data: {'mode': mode},
                                    success:function(data) {
                                        var ret = JSON.parse(data);
                                        if(ret.code == 200){
                                            alert("模式切换成功");

                                        }else{
                                            alert(ret['msg']);
                                        }
                                    }
                                })
                            } else{
                                mode = 1;
                                refresh();
                            }
                        }

                    }

                })
            }
        });

    }

    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.count",
            type: "post",
            data: searchParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 200)
                    ret = ret["msg"]["count"]
                else {
                    ret = 0;
                }
                $("#totalcount").text(ret);
                $('#pagination').empty();
                $('#pagination').removeData("twbs-pagination");
                $('#pagination').unbind("page");
                pagination(ret,"/ajax_action_detector.php?uu=detector.show&p_size="+p_size,parseInt(currentPage),searchParam)

                $("#isRead").removeClass("active");
                $("#allMessage").addClass("active");
                $("#unRead").removeClass("active");
            },
            beforeSend: function () {
                $(".loading-pic").removeClass("hidden");
            },
            error: function () {
                alert("无法连接服务器");
            }
        })
    }

    //var globalSearchParam = {random:1,register_ce_type:1,is_online:1}

    var globalSearchParam = {random:1}
    //第一次加载分页
    LoadPage(1,globalSearchParam)





    $("#searchButton").click(function(){
        var device_id =  $("#device_id").val();
        var organs =  $("#organs").val();
       // var rct = $("#select_verify").attr("value")
       // var ison = $("#select_isonline").attr("value")
        var contractor = $("#contractor").attr("value").toString()
        var address_code = $("#address_code").attr("value").toString()
        var device_status = $("#device_status").attr("value").toString()
        var device_is_effective = $("#device_is_effective").attr("value").toString()
        var is_online = $("#is_online").attr("value").toString()
        var time =$("#time").val()

       // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        globalSearchParam = {random:1}
        if(contractor!="00"){
            globalSearchParam["contractor"] = contractor
        }
        if(address_code!="0"){
            globalSearchParam["address_code"] = address_code
        }
        if(device_status!="0"){
            globalSearchParam["device_status"] = device_status
        }
        if(device_is_effective!="-1"){
            globalSearchParam["device_is_effective"] = device_is_effective
        }
        if(is_online!="-1"){
            globalSearchParam["is_online"] = is_online
        }
        if(time!=""){
            globalSearchParam["time"] = time
        }
        
        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
        }
        if(organs!=""){
            globalSearchParam["organs"] = organs
        }
        LoadPage(1,globalSearchParam)

    })

    $("#clearButton").click(function(){
        firstSelect("contractor");
        firstSelect("address_code");
        firstSelect("device_status");
        firstSelect("device_is_effective");
        firstSelect("is_online");
        $("#time").val("");
        $("#device_id").val("");
        $("#organs").val("");
    })


    function alterSwitch(obj){
        var id= $(obj).attr("id")

        alert(id)
    }

</script>

</body>
</html>