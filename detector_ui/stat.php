<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');

require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');
require_once(dirname(__FILE__) . '/require_get_parameter_for_post.php');
?>

<!DOCTYPE html>
<html>
<head>
    <title>告警统计</title>
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
    <link href="css/detector.css" rel="stylesheet">
    <link href="bootstrap-datetimepicker-master/css/bootstrap-datetimepicker.min.css" rel="stylesheet" media="screen">

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
        .mainCountPanel{
            height: 768px;
            overflow: auto;
            text-align: left;
            display: flex;
            justify-content: space-around;
        }
        .mainCountPanel>div{
            border: 1px solid gray;
        }
        .mainCountPanel>div:nth-child(1){
            width:40%;
            height:100%;

        }
        .mainCountPanel>div:nth-child(2){
            width:55%;
            height:100%;
            
        }
        .countPanelTitle{
            font-size: 16px;
            font-weight: bold;
            color: #428bca;
            text-align: center;
            padding: 5px;
        }
        #riskCount,#trendAlarm,#deviceNum{
            width:100%;
            height: 30%;
            
        }
        .highlightValue{
            font-size: 24px;
            font-weight: bold;
            color: orange;
        }
        .countLabel{
            text-align: center;
        }
        .countLabel>span{
            margin-right: 10px;
        }
        #typeCount,#ruleTask{
            width:100%;
            height: 48%;
            
        }

        .devicePanel{
            height:300px;
            display: flex;
            justify-content: space-around;
            margin-left: 15px;
            margin-right: 15px;
            margin-top: 15px;
            border: 1px solid gray;
        }
        #nodeNum, #centerNum{
            width: 30%;
            height: 100%;   
        }
        

    </style>
</head>
<body>
<div id="whole-wrapper">
    <div class="row">
        <div class="pull-left margin_ddos1" style="margin-bottom:0px">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;告警统计
                    <a class="badge" id="showMore" style="
                        background: orange;
                        color: white;
                        font-size: 18px;
                        padding: 2px 10px;
                        font-weight: normal;
                    "><i class="fa fa-angle-double-right"></i>高级</a>
                </h4>
        </div>
    </div>
    <!--<div class="panel-heading">
            <h3 class="panel-title" style="color:#428bca">
                <a id="showMore"><i class="fa fa-angle-double-right"></i>高级</a>
            </h3>
    </div>-->
    <div id="collapseSearch" style="display:none">
            <div class="row btn-banner">
                    <div class="btn-group">
                            <button class="btn btn-default btn-sm"  onclick="switchTime('week')">近一周</button>
                            <button class="btn btn-default btn-sm"  onclick="switchTime('30days')">近30天</button>
                            <button class="btn btn-default btn-sm"  onclick="otherTime()">自定义 <i class="time_switch fa fa-chevron-down fa-chevron-up"></i></button>
                    </div>

                    <div class="btn-group">
                            <button class="btn btn-default btn-sm"  onclick="switchDevice()">按设备 <i class="device_switch fa fa-chevron-down fa-chevron-up"></i></button>
                    </div>

                    <button class="btn btn-default btn-sm"  onclick="switchRuleTask()">按策略ID/任务组ID <i class="rule_switch fa fa-chevron-down fa-chevron-up"></i></button>
                                
                    <button class="btn btn-default btn-sm"  onclick="switchAlarmType()">按告警类型 <i class="type_switch fa fa-chevron-down fa-chevron-up"></i></button>

                    <button type="button" class="btn btn-primary btn-sm btn-interval" onclick="searchData()"><i class="fa fa-search">&nbsp;&nbsp;</i>查询</button>        
                    <button class="btn btn-default btn-sm" onclick="clearAll()"><i class="fa fa-eraser">&nbsp;&nbsp;</i>重置</button>
                                
                                
                    <div class="pull-right">
                            <!--<button class="btn btn-primary" id="exportSearch" onclick="export_search()"><i class="fa fa-download">&nbsp;&nbsp;</i>导出(当前查询)</button>-->
                            <div class="btn-group btn-interval">
                                <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown"><i class="fa fa-download">&nbsp;&nbsp;</i>导出(按条件)
                                    <span class="caret"></span>
                                </button>
                                <ul class="dropdown-menu" role="menu">
                                            <li><a onclick="export_search('risk')">按告警级别</a></li>
                                            <li><a onclick="export_search('device_id')">按检测器</a></li>
                                            <li><a onclick="export_search('warning_module')">按告警大类</a></li>
                                            <li><a onclick="export_search('warning_type')">按告警小类</a></li>
                                            <li><a onclick="export_search('group_id')">按任务组</a></li>
                                            <!--<li><a onclick="export_search('rule_id')">按策略ID</a></li>-->
                                </ul>
                            </div>
                            <button class="btn btn-primary" id="exportSearch" onclick="export_search('time')"><i class="fa fa-download">&nbsp;&nbsp;</i>导出(按时间)</button>
                                <!--<button class="btn btn-primary" id="export1" onclick="export_file1()"><i class="fa fa-download">&nbsp;&nbsp;</i>导出(按类型)</button>
                                    <button class="btn btn-primary" id="export2" onclick="export_file2()"><i class="fa fa-download">&nbsp;&nbsp;</i>导出(按来源)</button>-->
                        </div>
                        <div id="searchCondition" style="color:orange"></div>
                    </div>

                    <div class="row btn-banner otherTime" style="display:none">
                        <div class="input-group date form_datetime date_div">
                            <input id="time_min" class="form-control" size="16" type="text" value="" readonly placeholder="开始时间">
                            <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                        </div>
                        <div class="input-group date form_datetime date_div btn-interval2">
                                <input id="time_max" class="form-control" size="16" type="text" value="" readonly placeholder="截止时间">
                                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                        </div>
                        <!--<button type="button" class="btn btn-primary btn-interval2" onclick="searchData()"><i class="fa fa-search">&nbsp;&nbsp;</i>查询</button>-->
                    </div>

                    <div class="row btn-banner device" style="display:none">
                        <div class="dropdown-inline btn-interval">
                                <select id="device_id" class="selectpicker form-control search-input" data-live-search="true" title="检测器">
                                    <option value="">全部检测器</option>
                                </select>
                        </div>
                        <!--<input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器ID">-->
                        <!--<button type="button" class="btn btn-primary btn-interval" onclick="searchData()"><i class="fa fa-search">&nbsp;&nbsp;</i>查询</button>-->
                    </div>

                    <div class="row btn-banner ruleTask" style="display:none">
                        <input id="rule_id" type="text" class="form-control search-input" placeholder="策略ID">
                        <div class="dropdown-inline btn-interval">
                        <select id="task_group_id" class="selectpicker form-control search-input task_group_select" data-live-search="true" title="任务组">
                                <option value="">全部任务组</option>
                        </select>
                        </div>
                        <!--<button type="button" class="btn btn-primary btn-interval" onclick="searchData()"><i class="fa fa-search">&nbsp;&nbsp;</i>查询</button>-->
                    </div>

                    <div class="row btn-banner alarmType" style="display:none">
                                <!--<div class="dropdown btn-interval dropdown-inline">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="risk" class="pull-left" value="-1">所有警报风险级别</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                        <li onclick="selectProtoFwd(this);" value="-1">所有警报风险级别</li>
                                        <li onclick="selectProtoFwd(this);" value="0">无风险</li>
                                        <li onclick="selectProtoFwd(this);" value="1">一般级</li>
                                        <li onclick="selectProtoFwd(this);" value="2">关注级</li>
                                        <li onclick="selectProtoFwd(this);" value="3">严重级</li>
                                        <li onclick="selectProtoFwd(this);" value="4">紧急级</li>
                                    </ul>
                                </div>-->

                                <div class="dropdown dropdown-inline">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="warning_module" class="pull-left" value="0">所有检测功能</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="warning_module_list">
                                        <li onclick="selectProtoFwd(this); syncWarningModuleAndType(this);" value="0">所有检测功能</li>
                                        <li onclick="selectProtoFwd(this); syncWarningModuleAndType(this);" value="1">攻击窃密</li>
                                        <li onclick="selectProtoFwd(this); syncWarningModuleAndType(this);" value="2">未知攻击</li>
                                        <li onclick="selectProtoFwd(this); syncWarningModuleAndType(this);" value="3">传输涉密</li>
                                        <li onclick="selectProtoFwd(this); syncWarningModuleAndType(this);" value="4">目标审计</li>
                                        <li onclick="selectProtoFwd(this); syncWarningModuleAndType(this);" value="5">通信阻断</li>
                                    </ul>
                                </div>

                                <div class="dropdown btn-interval dropdown-inline">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="warning_type" class="pull-left" value="0">所有告警类型</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="warning_type_list">
                                        <li onclick="selectProtoFwd(this);" value="0">所有告警类型</li>
                                        <li onclick="selectProtoFwd(this);" value="1">木马攻击窃密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="2">漏洞攻击窃密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="3">恶意程序窃密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="4">其他攻击窃密告警</li>

                                        <li onclick="selectProtoFwd(this);" value="5">未知攻击窃密告警</li>

                                        <li onclick="selectProtoFwd(this);" value="6">邮件涉密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="7">即时通信涉密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="8">文件传输涉密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="9">HTTP涉密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="10">网盘涉密告警</li>
                                        <li onclick="selectProtoFwd(this);" value="11">其他协议涉密告警</li>

                                        <li onclick="selectProtoFwd(this);" value="12">IP审计告警</li>
                                        <li onclick="selectProtoFwd(this);" value="13">域名审计告警</li>
                                        <li onclick="selectProtoFwd(this);" value="14">URL审计告警</li>
                                        <li onclick="selectProtoFwd(this);" value="15">账号审计告警</li>

                                        <li onclick="selectProtoFwd(this);" value="16">通信阻断告警</li>
                                    </ul>
                                </div>
                                <!--<button type="button" class="btn btn-primary btn-interval" onclick="searchData()"><i class="fa fa-search">&nbsp;&nbsp;</i>查询</button>-->
                    </div>

                    <div class="mainCountPanel">
                        <div>
                            <div class="countPanelTitle">
                                告警概览
                            </div>
                            <div class="countLabel">
                                <span>告警数：<span id="alarmCount" class="highlightValue">0</span></span>
                                <!-- <span>告警中心数：<span id="centerCount" class="highlightValue">0</span></span> -->
                                <span>告警设备数：<span id="deviceCount" class="highlightValue"></span></span>
                            </div>
                            
                            <!--告警级别统计-->
                            <div id="riskCount"></div>
                            <!--告警态势-->
                            <div id="trendAlarm" ></div>
                            <div id="deviceNum"></div>
                        </div>

                        <div>
                            <div class="countPanelTitle">
                                明细统计
                            </div>
                            <!--大类小类统计-->
                            <div id="typeCount"></div>
                            <!--产生告警的rule_id、group_id数-->
                            <div id="ruleTask"></div>
                        </div>
                    </div>

                   <!--  <div class="devicePanel">
                            <div id="nodeNum"></div>
                            <div id="centerNum"></div>
                            <div id="deviceNum"></div>
                    </div> -->

            </div>
    <div class="container-whole">
            

        <div class="container-left">
            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                态势统计（最近一个月告警数量二维图）
                            </div>
                        </div>
                        <div class="widget-body">
                            <div style=" border: 1px solid #e1e6eb;">
                                <div id = "newly-trend-div" class="chart-size"></div>
                                <div align="center">
                                    <p class="img-text">态势统计图</p>
                                    <p class="img-text2" id="newly-trend-per">(ammout/date)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                告警类型柱状统计图(大类)
                            </div>
                        </div>
                        <div class="widget-body">
                            <div style=" border: 1px solid #e1e6eb;">
                                <div id = "business-type-div" class="chart-size"></div>
                                <div align="center">
                                    <p class="img-text">告警类型统计图</p>
                                    <p class="img-text2" id="business-type-per">(amount/warning_module)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                告警任务统计(TOP10)
                            </div>
                        </div>
                        <div class="widget-body">
                            <div style=" border: 1px solid #e1e6eb;">
                                <div id = "alarm-task-div" class="chart-size"></div>
                                <div align="center">
                                    <p class="img-text">告警任务统计图</p>
                                    <p class="img-text2">(amount/task)</p>
                                </div>
                            </div>
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
                                检测器告警数量统计(TOP10)
                            </div>
                        </div>
                        <div class="widget-body">
                            <div style=" border: 1px solid #e1e6eb;">
                                <div id = "attacked-top-div" class="chart-size"></div>
                                <div align="center">
                                    <p class="img-text">告警检测器统计图</p>
                                    <p class="img-text2" id="attacked-top-per">(amount/device_id)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                告警类型柱状统计(小类)
                            </div>
                        </div>
                        <div class="widget-body">
                            <div style=" border: 1px solid #e1e6eb;">
                                <div id = "warning-div" class="chart-size"></div>
                                <div align="center">
                                    <p class="img-text">告警类型统计图</p>
                                    <p class="img-text2" id="warning-per">(amount/warning_type)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>



            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                告警级别统计
                            </div>
                        </div>
                        <div class="widget-body">
                            <div style=" border: 1px solid #e1e6eb;">
                                <div id = "attacked-risk-div" class="chart-size"></div>
                                <div align="center">
                                    <p class="img-text">告警级别统计图</p>
                                    <p class="img-text2">(amount/risk)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        
    </div>
</div>

<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/libs/echarts.min.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<link href="css/bootstrap-select.css" rel="stylesheet">
<script type="text/javascript" src="js/bootstrap-select.js"></script>


<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script type="text/javascript">
    buildFrame("menu-alert2");

    $('.form_datetime').datetimepicker({
        language:  'zh-CN',
        minView: "month",
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayBtn: true,
    });

    function selectProtoFwd(obj) {
        $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
        $(obj).parent().parent().find("span:first").text($(obj).text());
    }

    function export_file1() {
        //  window.location.href = "detector_detail.php?id=" + id;
        var file_path = "/alarm/export_by_type";
        var file_name = "告警统计报表（按类型）.xlsx";

        //window.location.href ="/ajax_action_download_rename.php?uu=/alarm/export_by_type&rename=bb123.xlsx";

        window.location.href ="/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name;
        //post('detector_detail.php',{id:id});
    }

    function export_file2() {
        //  window.location.href = "detector_detail.php?id=" + id;
        var file_path = "/alarm/export_by_source";
        var file_name = "告警统计报表（按来源）.xlsx";

        window.location.href ="/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+"";


        //post('detector_detail.php',{id:id});
    }

    var warning_module_type_map = {
        0: [0, 17], //所有类型
        1: [1, 4], //攻击窃密
        2: [5, 1], //未知攻击
        3: [6, 6], //传输涉密
        4: [12, 4], //目标审计
        5: [16, 1]  //通信阻断
    };

    function syncWarningModuleAndType(obj) {
        $("#warning_type_list>li").addClass("hidden");
        var list = warning_module_type_map[$(obj).attr("value")];
        var first_li = $("#warning_type_list>li:eq(" + list[0] + ")");
        first_li.removeClass("hidden");
        var lis = first_li.nextAll();
        console.log("size:" + lis.size() + " " + list[1]);
        for(var i = 0; i < list[1]-1; i++) {
            $(lis[i]).removeClass("hidden");
        }
    }

    var newly_trend_option = {
        title: {
           // text: '态势统计图',
            /*textStyle:{
                color:"#3693CF",
                fontSize:18,
            },
            left:'47%'*/
        },
        tooltip: {
            trigger: 'axis'
        },
        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        color:[ '#328FCA'],
        xAxis: [
            {
                type: 'category',
                axisLabel:{
                  //interval:0,
                  rotate:15,
                  margin:8,
                  textStyle: {
                       fontSize:12
                  }
                },
//                boundaryGap: true,
                nameLocation: 'middle',
//                nameTextStyle: {
//                    color: "#3693CF",
//                    fontSize: 10,
//                },
                splitLine : {
                    show:true,
                    lineStyle : {
                        type : 'solid',
                        color: '#F3F3F3'
                    }
                },
                data: (function (){
                    var now = new Date();
                    var res = [];
                    var len = 10;
                    while (len--) {
                        res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
                        now = new Date(now - 2000);
                    }
                    return res;
                })()
            },
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                // name: '流量',
                //max: 10,
                min: 0,
                boundaryGap: [0.2, 0.2],
                splitLine : {
                    show:true,
                    lineStyle : {
                        type : 'solid',
                        color: '#F3F3F3'
                    }
                }
            }
        ],
        series: [
            {
                name:'amount',
                type:'line',
                smooth: true,
                symbolSize: 12,
                lineStyle: {
                    normal: {
                        width: 5,
                    },
                },
                data:(function (){
                    var res = [];
                    var len = 0;
                    while (len < 10) {
                        res.push(0);
                        len ++;
                    }
                    return res;
                })()
            },
        ]
    };

    var warning_module_option = {
        title: {
            // text: '告警统计图',
            textStyle:{
                color:"#3693CF",
                fontSize:18,
            },
            left:'47%'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        color:[ '#328FCA'],
        xAxis : [
            {
                type : 'category',
                data : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    interval:0
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                min: 0,
                boundaryGap: [0.2, 0.2],
                splitLine : {
                    show:true,
                    lineStyle : {
                        type : 'solid',
                        color: '#F3F3F3'
                    }
                }
            }
        ],
        series: [
            {
                name:'amount',
                type:'bar',
                barWidth: '60%',
                data:[10, 52, 200, 334, 390, 330, 220]
            },
        ]
    }


    var warning_option = {
        title: {
            // text: '告警统计图',
            textStyle:{
                color:"#3693CF",
                fontSize:18,
            },
            left:'47%'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        color:[ '#328FCA'],
        xAxis : [
            {
                type : 'category',
                data : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    interval:0,
                    rotate: 15
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                min: 0,
                boundaryGap: [0.2, 0.2],
                splitLine : {
                    show:true,
                    lineStyle : {
                        type : 'solid',
                        color: '#F3F3F3'
                    }
                }
            }
        ],
        series: [
            {
                name:'amount',
                type:'bar',
                barWidth: '60%',
                data:[10, 52, 200, 334, 390, 330, 220]
            },
        ]
    };

    var attacked_top_option = {
        title: {
            // text: '告警统计图',
            textStyle:{
                color:"#3693CF",
                fontSize:18,
            },
            left:'47%'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        color:[ '#328FCA'],
        xAxis : [
            {
                type : 'category',
                data : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                min: 0,
                boundaryGap: [0.2, 0.2],
                splitLine : {
                    show:true,
                    lineStyle : {
                        type : 'solid',
                        color: '#F3F3F3'
                    }
                }
            }
        ],
        series: [
            {
                name:'amount',
                type:'bar',
                barWidth: '60%',
                data:[10, 52, 200, 334, 390, 330, 220]
            },
        ]
    };

    var task_option = {
        title: {
            // text: '任务组',
            textStyle:{
                color:"#3693CF",
                fontSize:18,
            },
            left:'47%'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        color:[ '#328FCA'],
        xAxis : [
            {
                type : 'category',
                data : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    interval:0
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                min: 0,
                boundaryGap: [0.2, 0.2],
                splitLine : {
                    show:true,
                    lineStyle : {
                        type : 'solid',
                        color: '#F3F3F3'
                    }
                }
            }
        ],
        series: [
            {
                name:'amount',
                type:'bar',
                barWidth: '60%',
                data:[10, 52, 200, 334, 390, 330, 220]
            },
        ]
    }

    /*var risk_option = {
        title: {
            // text: '告警统计图',
            textStyle:{
                color:"#3693CF",
                fontSize:18,
            },
            left:'47%'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer : {
                type : 'shadow'
            }
        },
        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        color:[ '#328FCA'],
        xAxis : [
            {
                type : 'category',
                data : ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    interval:0
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                scale: true,
                min: 0,
                boundaryGap: [0.2, 0.2],
                splitLine : {
                    show:true,
                    lineStyle : {
                        type : 'solid',
                        color: '#F3F3F3'
                    }
                }
            }
        ],
        series: [
            {
                name:'amount',
                type:'bar',
                barWidth: '60%',
                data:[10, 52, 200, 334, 390, 330, 220]
            },
        ]
    };*/

    var risk_option = {
        title: {
            // text: '告警统计图',
            textStyle:{
                color:"#3693CF",
                fontSize:18,
            },
            left:'47%'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        color:[ '#328FCA'],
        
        series : [
            {
                name: '告警级别',
                type: 'pie',
                radius : '80%',
                center: ['50%', '50%'],
                data:[
                    
                ],
                itemStyle: {
                    normal:{
                        borderWidth: 3,
                        borderColor: '#235894'
                    }
                }
            }
        ]
    };


    var newly_trend_chart = echarts.init(document.getElementById('newly-trend-div'));
    var trendAlarm = echarts.init(document.getElementById('trendAlarm'));
    var warning_chart =  echarts.init(document.getElementById('warning-div'));
    var warning_module_chart = echarts.init(document.getElementById('business-type-div'));
    var attacked_top_chart =  echarts.init(document.getElementById('attacked-top-div'));
    var task_chart = echarts.init(document.getElementById('alarm-task-div'));
    var risk_chart = echarts.init(document.getElementById('attacked-risk-div'));

    $(function () {
        console.log("执行js");
        get();
        //setInterval("get()",100000);

        //所有echart图标自适应改变大小
        window.onresize = function(){
            newly_trend_chart.resize();
            trendAlarm.resize();
            warning_chart.resize();
            warning_module_chart.resize();
            attacked_top_chart.resize();
            risk_chart.resize();
            task_chart.resize();
        }

    });

    function consturct_newly_trend(data){
        var arr1 = new Array();
        var arr2 = new Array();

        for(var i=0;i<data.length;i++){
            arr1[i] = data[i].amount
            arr2[i] = data[i].date
        }

        newly_trend_option.series[0].data = arr1
        newly_trend_option.xAxis[0].data = arr2

        newly_trend_chart.setOption(newly_trend_option);
        trendAlarm.setOption(newly_trend_option);
        var trendAlarmOption = trendAlarm.getOption();
        trendAlarmOption.title[0].text = "告警态势";
        trendAlarmOption.series[0].markLine = {
                            silent: true,
                            data: [
                                {type: 'average', name: '平均值'}
                            ]
                        }
        trendAlarm.setOption(trendAlarmOption);
    }

    function construct_warning_module(data){
        var warning_moduleMap=
        {   1:'攻击窃密',
            2:'异常行为',
            3:'违规泄密',
            4:'目标帧听',
            5:'通信阻断',
            // 5:'通信阻断',
            //6:'插件告警'
        }
        var arr1 = new Array();
        var arr2 = new Array();

        for(var i=0;i<data.length;i++){
            arr1[i] = data[i].amount
            arr2[i] = warning_moduleMap[data[i].warning_module]
        }

        warning_module_option.series[0].data = arr1
        warning_module_option.xAxis[0].data = arr2

        warning_module_chart.setOption(warning_module_option);
    }

    function consturct_warning(data){
        /*var warning_typeMap={1:'木马攻击',2:'漏洞攻击',3:'恶意程序',4:'未知攻击',5:'邮件泄密',6:'通讯泄密',7:'文件泄密',
            8:'HTTP泄密',9:'网盘泄密',10:'IP侦听',11:'域名侦听',12:'URL侦听',13:'账号侦听'}*/
        var warning_typeMap=
        {
        // 0:'未知告警',
        1:'木马攻击',
        2:'漏洞利用',
        3:'恶意程序',
        4:'其他攻击',
        5:'未知攻击',
        6:'Email涉密',
        7:'Im涉密',
        8:'FTP涉密',
        9:'HTTP涉密',
        10:'Netdisk涉密',
        11:'其他涉密',
        12:'IP审计',
        13:'域名审计',
        14:'URL审计',
        15:'账号审计',
        16:'通信阻断',
        // 17:'通信阻断'
    }

        var arr1 = new Array();
        var arr2 = new Array();

        for(var i=0;i<data.length;i++){
            arr1[i] = data[i].amount
            arr2[i] = warning_typeMap[data[i].warning_type]
        }

        warning_option.series[0].data = arr1
        warning_option.xAxis[0].data = arr2

        warning_chart.setOption(warning_option);
    }

    function consturct_attacked_top(data){
        var arr1 = new Array();
        var arr2 = new Array();

        for(var i=0;i<data.length;i++){
            arr1[i] = data[i].amount
            arr2[i] = data[i].device_id
        }

        attacked_top_option.series[0].data = arr1
        attacked_top_option.xAxis[0].data = arr2

        attacked_top_chart.setOption(attacked_top_option);
    }
    function construct_task(data){
        var arr1 = new Array();
        var arr2 = new Array();

        for(var i=0;i<data.length;i++){
            arr1[i] = data[i].amount
            arr2[i] = data[i].name
        }

        task_option.series[0].data = arr1
        task_option.xAxis[0].data = arr2

        task_chart.setOption(task_option);
    }
    function construct_risk(data){
        var riskMap = {
            '-1':'未知',
            0:'无风险',
            1:'一般级',
            2:'关注级',
            3:'严重级',
            4:'紧急级'
        }
        var arr1 = new Array();
        var arr2 = new Array();

        for(var i=0;i<data.length;i++){
            //arr1[i] = data[i].amount
            //arr2[i] = riskMap[data[i].risk]
            if(data[i].risk!=-1){
                var obj = {'name':riskMap[data[i].risk],'value':data[i].amount};
                risk_option.series[0].data.push(obj);
            }
        }

        //risk_option.series[0].data = arr1
        //risk_option.xAxis[0].data = arr2

        risk_chart.setOption(risk_option);
    }

    function get() {
        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.newly_trend",
            type: "post",
            data:{days:30},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                consturct_newly_trend(ret.msg)
            }
        });

        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data:{query_condition:'warning_module'},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                construct_warning_module(ret.msg);
            }
        });

        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data:{query_condition:'warning_type'},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                consturct_warning(ret.msg);
            }
        });

        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data:{query_condition:'device_id'},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                consturct_attacked_top(ret.msg);
            }
        });
        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data:{query_condition:'risk'},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                construct_risk(ret.msg);
            }
        });
// uu=alarm.ShowAlarmTask
        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data:{query_condition:'group_id'},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                construct_task(ret.msg);
            }
        });
        
    }

var cascadeNodeCenterDevice = {
    'device_id':[]
};

</script>
<script src="js/stat.js"></script>

<script>
/* 判断是否从设备管理页跳转过来的，重载数据 */
$(function(){
    if(typeof(post_center_id) != "undefined"){
        setTimeout(function(){
            $('#showMore').click();
            $('#manage_center').selectpicker('val',post_center_id);
            switchDevice();
            searchData();
        },500)
    }
})
</script>
</body>
</html>

