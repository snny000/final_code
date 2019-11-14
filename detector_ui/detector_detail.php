<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

$id = $_REQUEST["id"];

if(empty($id)){header('Location: error.php');}



?>

<!DOCTYPE html>
<html>
<head>
    <title>检测器详情</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

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
            /*background-color: #F5F6FA;*/
            background-color: #428bca;
            font-weight: bold;
            text-align: center;
            color: white;
        }

        .sub-title .text-muted{
            color: white;
        }
        #alarmCount{
            text-align: center;
        }

        a{
            cursor:pointer;
            font-weight: bold;
        }

        .highlightValue{
            color: orange;
            font-size: large;
            font-weight: bold;
        }

        #base-form td{
            border-top:0;
        }
        #base-form table td{
            border-top:1px solid #dddddd;
            border-bottom:1px solid #dddddd;
        }

        [alarmtype]{
            text-align: center;
        }

        #moduleTable td {
            line-height: 4.5;
            border: 1px solid #dddddd;
        }
        
        #moduleTable th{
            border-top: 0px;
            border: 1px solid #dddddd;
        }

        .container-left,.container-right{
            transition:width 1s;
        }

    </style>
</head>
<body>
<div class="modal fade" id="hintModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog" style="width:60%">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    ×
                </button>
                <h4 class="modal-title">
                    提示框
                </h4>
            </div>
            <div class="modal-body">
                
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="interfaceModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog" style="width:60%">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    ×
                </button>
                <h4 class="modal-title">
                    全部接口信息
                </h4>
            </div>
            <div class="modal-body">
                <div id="interfaceAlert"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="suspectedModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog" style="width:60%">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    ×
                </button>
                <h4 class="modal-title">
                    全部异常信息
                </h4>
            </div>
            <div class="modal-body">
                <div id="listSuspectedAlert"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="diskModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog" style="width:60%">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    ×
                </button>
                <h4 class="modal-title">
                    磁盘详细信息
                </h4>
            </div>
            <div class="modal-body">
                <table id="disk_info" class="table table-condensed">
                    <tbody>
                        <tr>
                            <td>磁盘序列号</td>
                            <td>磁盘大小</td>
                            <td style="text-align:center">磁盘整体可用空间</td>
                        </tr>
                     </tbody>
                </table>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div id="whole-wrapper">
    <div id="singleOpen" class="btn-group" data-toggle="buttons" style="margin:5px;left:50%; transform:translateX(-50%)">
        <button class="btn btn-primary" onclick="switchShow('left',this)"><i class="fa fa-info-circle">&nbsp;&nbsp;</i>基本信息</button>
        <!--<button class="btn btn-primary" data-toggle="modal" data-target="#hintModal"><i class="fa fa-sliders">&nbsp;&nbsp;</i>业务状态</button>-->
        <button class="btn btn-primary" onclick="switchShow('right',this)"><i class="fa fa-spinner">&nbsp;&nbsp;</i>模块信息</button>
<!--        <button class="btn btn-primary" data-toggle="modal" data-target="#hintModal"><i class="fa fa-plug">&nbsp;&nbsp;</i>插件状态</button>-->
    </div>

    <div class="container-whole">
        <div class="container-left">
            <div class="row">
                <div class="col-lg-12 col-md-12">
                    <div class="widget no-margin">
                        <!--<div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                检测器基本信息
                            </div>
                        </div>-->
                        <div class="widget-body">
                            <table class="table no-margin" style="margin-top:8px">
                                <tbody id="base-form">
                                    <tr class="sub-title">
                                        <td colspan=2>
                                            <span class="text-muted">概要信息</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted">检测器编号:</span>
                                            <span id="device_id"></span>
                                        </td>
                                        <td>
                                            <span class="text-muted">客户单位:</span>
                                            <span id="organs"></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted">部署地址:</span>
                                            <span id="address"></span>
                                        </td>
                                        <td>
                                            <span class="text-muted">行政区域:</span>
                                            <span id="address_code"></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted">审核时间:</span>
                                            <span id="op_time"></span>
                                        </td>
                                        <td>
                                            <span class="text-muted">审核人:</span>
                                            <span id="op_person"></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted">认证时间:</span>
                                            <span id="auth_time"></span>
                                        </td>
                                        <td>
                                            <span class="text-muted">认证结果:</span>
                                            <span id="message"></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan=2>
                                            <span class="text-muted"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>接口信息:</span>
                                            <a data-toggle="modal" data-target="#interfaceModal">查看全部</a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td id="list_interface" colspan=2>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted" style="font-weight:bold"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>告警统计</span>
                                        </td></tr>
                                    <tr>
                                        <td colspan=2>
                                            <table id="alarmCount" class="table table-condensed">
                                                <tbody>
                                                <tr>
                                                    <td>告警总数</td>
                                                    <td>攻击窃密告警</td>
                                                    <td>未知攻击告警</td>
                                                    <td>传输涉密告警</td>
                                                    <td>目标审计告警</td>
                                                    <td>通信阻断告警</td>
                                                    <td>其他</td>
                                                </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted">下发策略总数:</span>
                                            <span id="center_rule_count" class="highlightValue">0</span>
                                        </td>
                                        <td>
                                            <span class="text-muted">下发插件总数:</span>
                                            <span id="center_plug_count" class="highlightValue">0</span>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td>
                                            <span class="text-muted"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>最新异常状态:</span>
                                            <a data-toggle="modal" data-target="#suspectedModal">查看全部</a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td id="newSuspected" colspan=2>
                                        </td>
                                    </tr>
                                    <tr class="sub-title">
                                        <td colspan=2>
                                            <span class="text-muted">状态信息</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted" style="font-weight:bold"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>CPU状态</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan=2>
                                            <table id="cpu_info" class="table table-condensed">
                                                <tbody>
                                                    <tr><td>物理编号</td>
                                                    <td>核心数量</td>
                                                    <td>频率</td>
                                                    <td>CPU使用率</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted" style="font-weight:bold"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>内存状态</span>
                                        </td></tr>
                                    <tr>
                                        <td colspan=2>
                                            <table class="table table-condensed">
                                                <tbody>
                                                <tr><td>内存大小</td>
                                                <td>内存利用率</td>
                                                </tr>
                                                <tr><td id="memNum"></td>
                                                <td id="memUse"></td>
                                                </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted" style="font-weight:bold"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>磁盘状态</span>
                                            <a data-toggle="modal" data-target="#diskModal">查看明细</a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan=2>
                                            <table id="disk_count" class="table table-condensed">
                                                <tbody>
                                                <tr>
                                                    <td>磁盘个数</td>
                                                    <td>磁盘总量</td>
                                                    <td style="text-align:center">磁盘整体可用空间</td>
                                                </tr>
                                                <tr>
                                                    <td></td>
                                                    <td></td>
                                                    <td style="text-align:center"></td>
                                                </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted" style="font-weight:bold"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>网卡状态</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td id='list_networkcard' colspan=2></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted" style="font-weight:bold"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>插件状态</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted">最新插件下发时间:</span>
                                            <span id="newPlugSync"></span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <span class="text-muted">插件告警总数:</span>
                                            <span id="plugAlarmCount"></span>
                                        </td>
                                    </tr>
                                    <!--<tr>
                                        <td>
                                            <table id="plug_status" class="table table-condensed">
                                                <tbody>
                                                    <tr >
                                                        <td width="5%">插件ID</td>
                                                        <td width="10%">CPU资源限制值</td>
                                                        <td width="10%">CPU资源使用值</td>
                                                        <td width="10%">内存限制值</td>
                                                        <td width="10%">内存使用值</td>
                                                        <td width="10%">磁盘剩余空间</td>
                                                        <td width="10%">状态</td>
                                                        <td width="10%">插件版本</td>
                                                        <td width="10%">插件策略版本</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>-->
                                    <!--<tr class="sub-title">
                                        <td>
                                            <span class="text-muted">注册信息</span>
                                        </td>
                                    </tr>-->
                                    <tr>
                                        <td>
                                            <span class="text-muted"><i class="fa fa-arrow-circle-down">&nbsp;&nbsp;</i>联系人:</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td id="contact_info" colspan=2>
                                        </td>
                                    </tr>
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
                        <!--<div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                检测器模块信息
                            </div>
                        </div>-->
                        <div class="widget-body">
                            <div id="business-form">
                            <table class="table no-margin" style="margin-top:8px;margin-bottom:0px">
                                <tbody >
                                    <tr class="sub-title">
                                        <td colspan=2 style="border-top:0px">
                                            <span class="text-muted">模块信息</span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                                           <!-- <table id="moduleTable" class="table table-condensed">
                                                <thead>
                                                        <th>
                                                            功能模块
                                                        </th>
                                                        <th>
                                                            模块状态
                                                        </th>
                                                        <th>
                                                            子模块名
                                                        </th>
                                                        <th>
                                                            子模块状态
                                                        </th>
                                                        <th>
                                                            策略总数
                                                        </th>
                                                        <th>
                                                            产生告警总数
                                                        </th>
                                                </thead>
                                                <tbody>
                                                    
                                                    <tr modulename="alarm">
                                                        <td rowspan="4">
                                                            攻击窃密检测
                                                        </td>
                                                        <td rowspan="4">
                                                        </td>
                                                        <td submodulename="trojan">
                                                            木马攻击
                                                        </td>
                                                        <td>
                                                            
                                                        </td>
                                                        <td ruletype=1>
                                                            <a onclick="postRule('director',1)"></a><br/>
                                                            <a onclick="postRule('center',1)"></a>
                                                        </td>
                                                        <td alarmtype=8>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="attack">
                                                            漏洞利用
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=2>
                                                            <a onclick="postRule('director',2)"></a><br/>
                                                            <a onclick="postRule('center',2)"></a>
                                                        </td>
                                                        <td alarmtype=9>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="malware">
                                                            恶意程序
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=3>
                                                            <a onclick="postRule('director',3)"></a><br/>
                                                            <a onclick="postRule('center',3)"></a>
                                                        </td>
                                                        <td alarmtype=10>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="other">
                                                            其他攻击
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td>
                                                            
                                                        </td>
                                                        <td alarmtype=11>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr modulename="abnormal">
                                                        <td>
                                                            未知攻击检测
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td submodulename="abnormal">
                                                            未知攻击
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=4>
                                                            <a onclick="postRule('director',4)"></a><br/>
                                                            <a onclick="postRule('center',4)"></a>
                                                        </td>
                                                        <td alarmtype=12>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr modulename="sensitive">
                                                        <td rowspan="7">
                                                            传输涉密检测
                                                        </td>
                                                        <td rowspan="7">
                                                            开启
                                                        </td>
                                                        <td submodulename="finger_file">
                                                            密标文件
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td>
                                                            
                                                        </td>
                                                        <td alarmtype=1>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="sensitive_file">
                                                            标密文件
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td>
                                                            
                                                        </td>
                                                        <td alarmtype=2>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="keyword_file">
                                                            关键词
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=5>
                                                            <a onclick="postRule('director',5)"></a><br/>
                                                            <a onclick="postRule('center',5)"></a>
                                                        </td>
                                                        <td alarmtype=3>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="encryption_file">
                                                            加密文件
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=6>
                                                            <a onclick="postRule('director',6)"></a><br/>
                                                            <a onclick="postRule('center',6)"></a>
                                                        </td>
                                                        <td alarmtype=4>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="compress_file">
                                                            压缩文件
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=7>
                                                            <a onclick="postRule('director',7)"></a><br/>
                                                            <a onclick="postRule('center',7)"></a>
                                                        </td>
                                                        <td alarmtype=5>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="picture_file">
                                                            图片筛选
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=8>
                                                            <a onclick="postRule('director',8)"></a><br/>
                                                            <a onclick="postRule('center',8)"></a>
                                                        </td>
                                                        <td alarmtype=6>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="style_file">
                                                            版式检测
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td>
                                                            
                                                        </td>
                                                        <td alarmtype=7>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr modulename="object_listen">
                                                        <td rowspan="4">
                                                            目标审计检测
                                                        </td>
                                                        <td rowspan="4">
                                                            开启
                                                        </td>
                                                        <td submodulename="ip_listen">
                                                            IP审计
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=9>
                                                            <a onclick="postRule('director',9)"></a><br/>
                                                            <a onclick="postRule('center',9)"></a>
                                                        </td>
                                                        <td alarmtype=13>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="domain_listen">
                                                            域名审计
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=10>
                                                            <a onclick="postRule('director',10)"></a><br/>
                                                            <a onclick="postRule('center',10)"></a>
                                                        </td>
                                                        <td alarmtype=14>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="url_listen">
                                                            URL审计
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=11>
                                                            <a onclick="postRule('director',11)"></a><br/>
                                                            <a onclick="postRule('center',11)"></a>
                                                        </td>
                                                        <td alarmtype=15>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="account_listen">
                                                            帐号审计
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=12>
                                                            <a onclick="postRule('director',12)"></a><br/>
                                                            <a onclick="postRule('center',12)"></a>
                                                        </td>
                                                        <td alarmtype=16>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr modulename="block">
                                                        <td>
                                                            通信阻断
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td submodulename="block">
                                                            通信阻断
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=18>
                                                            <a onclick="postRule('director',18)"></a><br/>
                                                            <a onclick="postRule('center',18)"></a>
                                                        </td>
                                                        <td alarmtype=17>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr modulename="net_audit">
                                                        <td rowspan="4">
                                                            网络行为审计
                                                        </td>
                                                        <td rowspan="4">
                                                            开启
                                                        </td>
                                                        <td submodulename="net_log">
                                                            通联关系审计
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=13>
                                                            <a onclick="postRule('director',13)"></a><br/>
                                                            <a onclick="postRule('center',13)"></a>
                                                        </td>
                                                        <td alarmtype>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="app_behavior">
                                                            应用行为上报
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=14>
                                                            <a onclick="postRule('director',14)"></a><br/>
                                                            <a onclick="postRule('center',14)"></a>
                                                        </td>
                                                        <td alarmtype>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="app_behavior">
                                                            应用行为web过滤
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=15>
                                                            <a onclick="postRule('director',15)"></a><br/>
                                                            <a onclick="postRule('center',15)"></a>
                                                        </td>
                                                        <td alarmtype>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td submodulename="app_behavior">
                                                            应用行为DNS过滤
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=16>
                                                            <a onclick="postRule('director',16)"></a><br/>
                                                            <a onclick="postRule('center',16)"></a>
                                                        </td>
                                                        <td alarmtype>
                                                            
                                                        </td>
                                                    </tr>
                                                    <tr modulename="ip_whitelist">
                                                        <td>
                                                            白名单过滤
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td submodulename="ip_whitelist">
                                                            IP白名单过滤
                                                        </td>
                                                        <td>
                                                            开启
                                                        </td>
                                                        <td ruletype=17>
                                                            <a onclick="postRule('director',17)"></a><br/>
                                                            <a onclick="postRule('center',17)"></a>
                                                        </td>
                                                        <td alarmtype>
                                                            
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>-->
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
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>

<script type="text/javascript">
    buildFrame('menu-detector');
    var php_id = <?php echo $id;?>;
    var device_id = "";
    $(function () {
        get(); // 检测器基本信息
    });

    /*基本信息*/
    function get() {
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.detail&id="+php_id, //ajax请求
            //url:'detector_detail.json',
            type: "post",
            data:null,
            cache: false,
            success: function(data){
                buildTbody(data);
            }
        });

        function buildTbody(data){
            var server = JSON.parse(data);
            //var server = data;
            var msg = server.msg;
            device_id = msg.device_id;
            $("#device_id").text(msg.device_id);
            $("#organs").text(msg.organs);
            $("#address").text(msg.address);
            $("#address_code").text(msg.address_code);
            $("#op_time").text(msg.op_time);
            $("#op_person").text(msg.op_person);
            $("#auth_time").text(msg.auth_time);
            $("#message").text(msg.message);
            $("#center_plug_count").text(msg.plug.plug_count); //插件数目
            $("#plugAlarmCount").html("<a onclick=postAlarm(6,\""+msg.device_id+"\")>"+msg.plug.plug_alarm+"</a>"); //插件告警数目
            $("#newPlugSync").html("<a onclick=postPlug(\""+msg.device_id+"\")>"+msg.plug.time+"</a>"); //最新插件下发时间
            $('#center_rule_count').text(msg.rule_count.all); //策略总数
            var _row = `<tr><td><a onclick="postAlarm('',${msg.device_id})" class="highlightValue">${msg.alarm_count.all}</a></td>
                    <td><a onclick="postAlarm(1,${msg.device_id})">${msg.alarm_count.alarm}</a></td>
                    <td><a onclick="postAlarm(2,${msg.device_id})">${msg.alarm_count.abnormal}</a></td>
                    <td><a onclick="postAlarm(3,${msg.device_id})">${msg.alarm_count.sensitive}</a></td>
                    <td><a onclick="postAlarm(4,${msg.device_id})">${msg.alarm_count.object_listen}</a></td>
                    <td><a onclick="postAlarm(5,${msg.device_id})">${msg.alarm_count.block}</a></td>
                    <td><a style="color:#999">${msg.alarm_count.other}</a>
                    </tr>`
            $('#alarmCount').append(_row);
            

            
            
            $("#memNum").text(msg.mem_total+" MB");
            

            list_name(msg.contact);
            list_cpu(msg.cpu_info);
            list_diskid(msg.disk_info);
            list_interface(msg.interface);
            //getAllAlarm();
           
            //getRuleCount();

            getRunStatus(msg);
            getBusinessStatus(msg);
            
        }

        function list_name(contact){
            var str = "<table class='table table-condensed'><tr><td>姓名</td><td>工作</td><td>电话</td><td>邮箱</td></tr>"
            for(var i=0;i<contact.length;i++){
                str  = str  + "<tr><td>"+ contact[i].name + "</td><td>"+
                    contact[i].position+ "</td><td>"+
                    contact[i].phone + "</td><td>"+
                    contact[i].email + "</td></tr>"
            }
            str += "</table>";
            $('#contact_info').html(str);
        }

        
        function list_diskid(disk_info){
            var str = "";
            var diskCount = disk_info.length || 0;
            var diskMem = 0;
            for(var i=0;i<disk_info.length;i++){
                str  = str  + "<tr><td>"+ disk_info[i].serial + "</td><td>"+disk_info[i].size + " GB</td></tr>"
                diskMem += parseInt(disk_info[i].size);
            }

            $('#disk_count tbody tr:eq(1) td:eq(0)').text(diskCount);
            $('#disk_count tbody tr:eq(1) td:eq(1)').text(diskMem +" GB");

            $('#disk_info tbody').append(str);
        }

        function list_interface(interface){
            var trueFalse = {'true':'是','false':'否'};
            var str = "<table class='table table-condensed'><tr><td>IP地址</td><td>MAC地址</td><td>是否为管理端口</td><td>子网掩码</td><td>网关接口</td></tr>"
            var str2 = "<table class='table table-condensed'><tr><td>IP地址</td><td>MAC地址</td><td>是否为管理端口</td><td>子网掩码</td><td>网关接口</td></tr>"
            for(var i=0;i<interface.length;i++){
                if(interface[i].manage==true)
                    str  = str  + "<tr><td>"+ interface[i].ip + "</td><td>"+interface[i].mac + "</td><td>"+trueFalse[interface[i].manage] + "</td><td>"+interface[i].netmask + "</td><td>"+interface[i].gateway + "</td></tr>"
                str2 = str2  + "<tr><td>"+ interface[i].ip + "</td><td>"+interface[i].mac + "</td><td>"+trueFalse[interface[i].manage] + "</td><td>"+interface[i].netmask + "</td><td>"+interface[i].gateway + "</td></tr>"
            }
            str += "</table>";
            str2 += "</table>";
            //return str;
            $('#list_interface').html(str);
            $('#interfaceAlert').html(str2);
        }

        function list_cpu(info){
            var str="";
            for(var i=0;i<info.length;i++){
                str  += "<tr physical_id="+info[i].physical_id+"><td>"+ info[i].physical_id + "</td><td>"+
                    info[i].core + "</td><td>"+
                    info[i].clock + "GHz</td><td>"+
                    "</td></tr>"
            }
            $("#cpu_info tbody").append(str);
        }
        /*获取告警统计数*/
        function getAllAlarm(){
            $.ajax({
                url:'/ajax_action_detector.php?uu=alarm.warning_type_histogram',
                data:{
                    device_id:php_id,
                    query_condition:'business_type'
                },
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var _row = "";
                    var alarmCount = 0;
                    var businessObj = {};
                    for(var i=1;i<7;i++){
                        businessObj[i] = 0;
                    }
                    for(var i=0;i<msg.length;i++){
                        alarmCount+=parseInt(msg[i]['amount']);
                        businessObj[msg[i].business_type] = msg[i].amount;
                    }
                    var other = businessObj[0]+businessObj[6];
                    _row = `<tr><td><a onclick="postAlarm('',${php_id})" class="highlightValue">${alarmCount}</a></td>
                    <td><a onclick="postAlarm(1,${php_id})">${businessObj[1]}</a></td>
                    <td><a onclick="postAlarm(2,${php_id})">${businessObj[2]}</a></td>
                    <td><a onclick="postAlarm(3,${php_id})">${businessObj[3]}</a></td>
                    <td><a onclick="postAlarm(4,${php_id})">${businessObj[4]}</a></td>
                    <td><a onclick="postAlarm(5,${php_id})">${businessObj[5]}</a></td>
                    <td><a style="color:#999">${other}</a>
                    </tr>`
                    $('#alarmCount').append(_row);

                    $('#plugAlarmCount').html("<a onclick=postStat(6,\""+php_id+"\")>"+businessObj[6]+"</a>");

                    $.ajax({
                        url:'/ajax_action_detector.php?uu=alarm.warning_type_histogram',
                        data:{
                            device_id:php_id,
                            query_condition:'alarm_type'
                        },
                        success:function(data){
                            var msg = JSON.parse(data)["msg"];
                            var alarmtype = {};
                            for(var i=0;i<msg.length;i++){
                                alarmtype[msg[i].alarm_type] = msg[i].amount;
                            }
                            // 模块告警（告警小类）
                            $("#moduleTable td[alarmtype]").html("<a>0</a>")
                            for(var key in alarmtype){
                                var aTag = "";
                                if(alarmtype[key]!=0)
                                alarmtype[key] == ""||"undefined" ? 0: alarmtype[key];
                                aTag = `<a onclick="postAlarm('',${php_id},${key})">${alarmtype[key]}</a>`;
                                $("#moduleTable td[alarmtype="+key+"]").html(aTag);
                            }
                        }
                    })
                    
                }
            })
        }
        /*获取指挥中心下发插件总数*/
        function getDirectorPlug(){
            $.ajax({
                url:'/ajax_action_detector.php?uu=plugin.show_plug_count&device_id='+php_id,
                success:function(data){
                    var msg = JSON.parse(data);
                    $('#director_plug_count').text(msg["msg"]["count"]);
                }
            })
        }

        /*获取所有策略*/
        function getRuleCount(){
            // 上行策略总数
            $.ajax({
                url:'/ajax_action_detector.php?uu=rule.get_rule_count&device_id='+php_id,
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var count = 0;
                    for(var key in msg){
                        $("#moduleTable td[ruletype="+key+"] a:eq(0)").html("管理中心下发"+msg[key]+"条");
                        count += parseInt(msg[key]);
                    }
                    $('#center_rule_count').text(count);
                }
            })
            $.ajax({
                url:'/ajax_action_detector.php?uu=rule.get_director_rule_count&device_id='+php_id,
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var count = 0;
                    for(var key in msg){
                        $("#moduleTable td[ruletype="+key+"] a:eq(1)").html("本地下发"+msg[key]+"条");
                        count += parseInt(msg[key]);
                    }
                    $('#director_rule_count').text(count);
                }
            })
        }


        
        
    }

    /*运行状态*/
    function getRunStatus(msg){
        if(msg.run_resource.mem) {
            $("#memUse").html("<span class='highlightValue'>"+msg.run_resource.mem+"%</span>");
        }
        var _rowspan = $('#disk_info tbody tr').length-1;
        if(msg.run_resource.disk) {
            $('#disk_info tbody tr:eq(1)').append("<td class='highlightValue' style='text-align:center' rowspan="+_rowspan+">"+msg.run_resource.disk+" GB</td>");

            $('#disk_count tbody tr:eq(1) td:eq(2)').html("<span class='highlightValue' style='text-align:center'>"+msg.run_resource.disk+" GB</span>")
        }
        if(msg.run_resource.cpu)
            list_cpu2(msg.run_resource.cpu);
        if(msg.run_resource.plug_stat)
            list_plug(msg.run_resource.plug_stat)

        function list_cpu2(data){
            info = data;
            for(var i=0;i<info.length;i++){
                $('#cpu_info tbody tr[physical_id='+info[i]["physical_id"]+'] td:eq(3)').html("<span class='highlightValue'>"+info[i]["cpu_usage"]+"%</span>")
            }
        }

        function list_plug(data){
            plug_stat = data;
            var str = ""
            for(var i=0;i< plug_stat.length;i++){
                str  = str  + "<tr plug_id='"+plug_stat[i].plug_id+"'><td>"+  plug_stat[i].plug_id + "</td><td>"+
                    plug_stat[i].cpu_range+ "%</td><td>"+
                    plug_stat[i].cpu_usage + "%</td><td>"+
                    plug_stat[i].mem_range + " MB</td><td>"+
                    plug_stat[i].mem_usage + " MB</td><td>"+
                    plug_stat[i].disk_usage + " GB</td><td>"+
                    moduleStatus[plug_stat[i].status] + "</td>"+
                    "<td></td><td></td></tr>"
            }
            $("#plug_status tbody").append(str);
        }
    }

    /*检测器业务状态*/
    function getBusinessStatus(msg){

        buildBusinessTbody(msg);

        function buildBusinessTbody(msg){
        /*网卡连通性信息*/
        function listNetworkCard(msg){
            var networkcard = msg.networkcard;
            var interface_stat_map= {1:'网卡启用',2:'网卡停用',3:'网线掉落',4:'网卡故障',99:'未知故障'}
                var str = "<table class='table table-condensed'>"+
                    "<tr><td>网卡序列号</td><td>网卡状态</td><td>数据流量</td><td>无法处理的报文数</td><td>丢包个数</td><td>采集时长</td></tr>";
                for(var i=0;i<networkcard.length;i++) {
                    /*str = str +
                    "<span class='text-muted'> 网卡序列号:</span>" + networkcard[i].interface_seq +
                    "<table class='table table-condensed'>"+
                    "<tr><td><span class='text-muted'> 网卡状态:</span>" + interface_stat_map[networkcard[i].interface_stat] + "</td></tr>" +
                    "<tr><td><span class='text-muted'> 数据流量:</span>" + networkcard[i].interface_flow + "</td></tr>" +
                    "<tr><td><span class='text-muted'> 无法处理的报文数:</span>" + networkcard[i].interface_error + "</td></tr>" +
                    "<tr><td><span class='text-muted'> 丢包个数:</span>" + networkcard[i].interface_drop + "</td></tr>" +
                    "<tr><td><span class='text-muted'> 采集时长:</span>" + networkcard[i].duration_time + "</td></tr>" +
                    "</table>";*/
                    str += "<tr><td>"+networkcard[i].interface_seq+"</td>"+
                        "<td>"+interface_stat_map[networkcard[i].interface_stat]+"</td>"+
                        "<td>"+networkcard[i].interface_flow+" MB</td>"+
                        "<td>"+networkcard[i].interface_error+"</td>"+
                        "<td>"+networkcard[i].interface_drop+"</td>"+
                        "<td>"+networkcard[i].duration_time+" 秒</td></tr>";
                }
                //return str;
                $('#list_networkcard').html(str);
        }
        

        



        function list_module(msg){
            var str = "<table id='moduleTable' class='table table-condensed'>" +
                "<tr><th>功能模块</th><th>模块状态</th><th>子模块名</th><th>子模块状态</th><th>策略总数</th><th>策略版本</th></tr>"+
                "<tr><td rowspan ='4'>攻击窃密检测</td><td rowspan ='4'>"+moduleStatus[msg.alarm_status]+"</td><td>木马攻击</td><td>"+moduleStatus[msg.trojan_status]+"</td><td><a onclick='postRule(1)'>共"+msg.rule_count.trojan+"条</a></td><td>"+msg.trojan_version+"</td></tr>"+
                "<tr><td>漏洞利用</td><td>"+moduleStatus[msg.attack_status]+"</td><td><a onclick='postRule(2)'>共"+msg.rule_count.attack+"条</a></td><td>"+msg.attack_version+"</td></tr>"+
                "<tr><td>恶意程序</td><td>"+moduleStatus[msg.malware_status]+"</td><td><a onclick='postRule(3)'>共"+msg.rule_count.malware+"条</a></td><td>"+msg.malware_version+"</td></tr>"+
                "<tr><td>其他攻击</td><td>"+moduleStatus[msg.other_status]+"</td><td><a>共"+0+"条</a></td><td>"+msg.other_version+"</td></tr>"+
                "<tr><td>未知攻击检测</td><td>"+moduleStatus[msg.abnormal_status]+"</td><td>未知攻击</td><td>"+moduleStatus[msg.abnormal_status]+"</td><td><a onclick='postRule(4)'>共"+msg.rule_count.abnormal+"条</a></td><td>"+msg.abnormal_version+"</td></tr>"+
                "<tr><td rowspan ='7'>违规泄密检测</td><td rowspan ='7'>"+moduleStatus[msg.sensitive_status]+"</td><td>密标文件</td><td>"+moduleStatus[msg.finger_file_status]+"</td><td><a>共"+0+"条</a></td><td>"+msg.finger_file_version+"</td></tr>"+
                "<tr><td>标密文件</td><td>"+moduleStatus[msg.sensitive_file_status]+"</td><td><a>共"+0+"条</a></td><td>"+msg.sensitive_file_version+"</td></tr>"+
                "<tr><td>关键字</td><td>"+moduleStatus[msg.keyword_file_status]+"</td><td><a onclick='postRule(5)'>共"+msg.rule_count.keyword_file+"条</a></td><td>"+msg.keyword_file_version+"</td></tr>"+
                "<tr><td>加密文件</td><td>"+moduleStatus[msg.encryption_file_status]+"</td><td><a onclick='postRule(6)'>共"+msg.rule_count.encryption_file+"条</a></td><td>"+msg.encryption_file_version+"</td></tr>"+
                "<tr><td>压缩文件</td><td>"+moduleStatus[msg.compress_file_status]+"</td><td><a onclick='postRule(7)'>共"+msg.rule_count.compress_file+"条</a></td><td>"+msg.compress_file_version+"</td></tr>"+
                "<tr><td>图片筛选</td><td>"+moduleStatus[msg.picture_file_status]+"</td><td><a onclick='postRule(8)'>共"+msg.rule_count.picture_file+"条</a></td><td>"+msg.picture_file_version+"</td></tr>"+
                "<tr><td>版式检测</td><td>"+moduleStatus[msg.style_file_status]+"</td><td><a>共"+0+"条</a></td><td>"+msg.style_file_version+"</td></tr>"+
                "<tr><td rowspan ='4'>目标审计检测</td><td rowspan ='4'>"+moduleStatus[msg.object_listen_status]+"</td><td>IP审计</td><td>"+moduleStatus[msg.ip_listen_status]+"</td><td><a onclick='postRule(9)'>共"+msg.rule_count.ip_listen+"条</a></td><td>"+msg.ip_listen_version+"</td></tr>"+
                "<tr><td>域名审计</td><td>"+moduleStatus[msg.domain_listen_status]+"</td><td><a onclick='postRule(10)'>共"+msg.rule_count.domain_listen+"条</a></td><td>"+msg.domain_listen_version+"</td></tr>"+
                "<tr><td>URL审计</td><td>"+moduleStatus[msg.url_listen_status]+"</td><td><a onclick='postRule(11)'>共"+msg.rule_count.url_listen+"条</a></td><td>"+msg.url_listen_version+"</td></tr>"+
                "<tr><td>帐号审计</td><td>"+moduleStatus[msg.account_listen_status]+"</td><td><a onclick='postRule(12)'>共"+msg.rule_count.account_listen+"条</a></td><td>"+msg.account_listen_version+"</td></tr>"+
                "<tr><td>通信阻断</td><td>"+moduleStatus[msg.block_status]+"</td><td>通信阻断</td><td>"+moduleStatus[msg.block_status]+"</td><td><a onclick='postRule(18)'>共"+msg.rule_count.block+"条</a></td><td>"+msg.block_version+"</td></tr>"+
                "<tr><td rowspan ='4'>网络行为审计</td><td rowspan ='4'>"+moduleStatus[msg.net_log_status]+"</td><td>通联关系审计</td><td>"+moduleStatus[msg.net_log_status]+"</td><td><a onclick='postRule(13)'>共"+msg.rule_count.net_log+"条</a></td><td>"+msg.net_log_version+"</td></tr>"+
                "<tr><td>应用行为上报</td><td>"+moduleStatus[msg.app_behavior_status]+"</td><td><a onclick='postRule(14)'>共"+msg.rule_count.app_behavior+"条</a></td><td>"+msg.app_behavior_version+"</td></tr>"+
                "<tr><td>应用行为web过滤</td><td>"+moduleStatus[msg.app_behavior_status]+"</td><td><a onclick='postRule(15)'>共"+msg.rule_count.web_filter+"条</a></td><td>"+msg.web_filter_version+"</td></tr>"+
                "<tr><td>应用行为dns过滤</td><td>"+moduleStatus[msg.app_behavior_status]+"</td><td><a onclick='postRule(16)'>共"+msg.rule_count.dns_filter+"条</a></td><td>"+msg.dns_filter_version+"</td></tr>"+
                "<tr><td>IP白名单过滤</td><td>开启</td><td>IP白名单过滤</td><td>开启</td><td><a onclick='postRule(17)'>共"+msg.rule_count.ip_whitelist+"条</a></td><td>"+msg.ip_whitelist_version+"</td></tr>"

            str += "</table>";
            $('#business-form').append(str);
        }

        /*异常状态*/
        function listSuspected(msg){
            var info = msg.suspected_status;
            if(info.length == 0)
                return;
            info.sort(function (a, b) { 
                    var time1 = new Date(a.time).getTime();
                    var time2 = new Date(b.time).getTime();
                    return time2 - time1;
                });
            var str = "<table class='table table-condensed'><tr><td>异常类型</td><td>异常产生时间</td><td>告警级别</td><td>事件描述</td></tr>"
                var str2 = "<table class='table table-condensed'><tr><td>设备编号</td><td>异常类型</td><td>异常产生时间</td><td>告警级别</td><td>事件描述</td></tr>"
                var riskType = {
                    0:'无风险',
                    1:'一般级',
                    2:'关注级',
                    3:'严重级',
                    4:'紧急级'
                }
                var eventType = {
                    1:'系统异常',
                    2:'软件异常',
                    3:'插件异常',
                    4:'策略运行异常'
                }
                for(var i=0;i<info.length;i++){
                    str2  = str2  + "<tr><td>"+ msg.device_id + "</td><td>"+
                        info[i].event_type + "</td><td>"+
                        info[i].time + "</td><td>"+
                        riskType[info[i].risk] + "</td><td>"+
                        info[i].msg + "</td></tr>"
                }
                str2 += "</table>";
                str  = str  + "<tr><td>"+ info[0].event_type + "</td><td>"+
                        info[0].time + "</td><td>"+
                        riskType[info[0].risk] + "</td><td>"+
                        info[0].msg + "</td></tr>"
                str += "</table>";
                $('#listSuspectedAlert').html(str2);
                //var str = "<a onclick='postSuspected(\""+php_id+"\")'>"+info[0].msg+" ("+info[0].time+")</a>"
                $('#newSuspected').html(str);

        }

        

        /*插件运行状态*/
        function listPluginStatus(msg){
            var info = msg.plug_status;
            for(var i=0;i<info.length;i++){
                     $('#plug_status tbody tr[plug_id='+info[i].plug_id+'] td:eq(7)').html(info[i].plug_version);
                     $('#plug_status tbody tr[plug_id='+info[i].plug_id+'] td:eq(8)').html(info[i].plug_policy_version);
                }
        }

        

        /*策略列表*/
        function list_rule(msg){
            var _row = $("<tr>" +
            "<td></td>" +
            "<td></td>" +
            "<td></td>" +
            "</tr>");
            for (var key in ruleType) {
                var row = _row.clone();
                row.find("td:eq(0)").text(ruleType[key][0]);
                row.find("td:eq(1)").html("<a policy_type="+key+" url="+ruleType[key][1]+".php onclick='postRule(this)'>共-条</a>");
                row.find("td:eq(2)").html("<a policy_type="+key+" url="+ruleType[key][1]+"_manage.php onclick='postRule(this)'>共-条</a>");
                row.show();
                row.appendTo($('#ruleCount'));

                //getRuleCount(key,row);
            }
        }
        

        /*模块信息*/
        function listModuleStatus(msg){
            var dataMap = {}; //按照类型重新分类数据，以方便处理
                for (var i = 0, l = msg.length; i < l; i++) {
                    var key = msg[i]['name'];
                    dataMap[key] = dataMap[key] || (dataMap[key] = []);
                    dataMap[key].push(msg[i]);
                }

                for(var key in msg){
                    var msg = dataMap[key][0];
                    var submodule = eval(dataMap[key][0]["submodule"]);
                    var rowspan = submodule.length;

                    $("#moduleTable tr[modulename="+msg.name+"] td:eq(1)").html(moduleStatus[msg.status]);
                    for(var i=0;i<submodule.length;i++){
                        $("#moduleTable td[submodulename="+submodule[i].name+"]").next().html(moduleStatus[submodule[i].status]);
                    }
                }
        }

        
        listNetworkCard(msg);
        //listModuleStatus(msg);
        listSuspected(msg);
        listPluginStatus(msg);
        //list_rule();
        list_module(msg);
    }
  }

/*跳转异常信息列表页面*/
function postSuspected(deviceId){
    
}
function postAlarm(type,deviceId,alarmtype){
    
    var param = {
        device_id: deviceId,
        warning_module: type==""?"-1":type,
        warning_type: alarmtype==undefined?"-1":alarmtype
    }
    if(type == 6){
        post_blank("plug_alarm.php",param);
    }else{
        post_blank("alarm.php",param);
    }
}
function postSubscribe(deviceId){
    post_blank("data_subscribe.php",{device_id:deviceId});
}
function postPlug(deviceId){
    post_blank("plug.php",{device_id:deviceId})
}
function postCenter(centerId){
    post_blank("topo_detail.php",{id:centerId})
}
</script>

<script>
var ruleType = {
                1:['木马攻击检测策略','rule_trojan'],
                2:['漏洞利用检测策略','rule_attack'],
                3:['恶意程序检测策略','rule_pefile'],
                4:['未知攻击窃密检测上报策略','rule_abnormal'],
                5:['关键字检测策略','rule_keyword_file'],
                6:['加密文件筛选策略','rule_encryption_file'],
                7:['压缩文件检测策略','rule_compress_file'],
                8:['图片文件筛选策略','rule_picture_file'],
                9:['IP审计策略','rule_ip_listen'],
                10:['域名审计策略','rule_domain_listen'],
                11:['URL审计策略','rule_url_listen'],
                12:['账号审计检测策略','rule_account_listen'],
                13:['通联关系上报策略','rule_net_log'],
                14:['应用行为上报策略','rule_app_behavior'],
                15:['应用行为web过滤策略','rule_web_filter'],
                16:['应用行为DNS过滤策略','rule_dns_filter'],
                17:['IP白名单过滤策略','rule_ip_whitelist'],
                18:['通信阻断策略','rule_comm_block']
        }

var moduleType = {
    'alarm': '攻击窃密检测',
    'abnormal': '未知攻击检测',
    'sensitive': '传输涉密检测', 
    'object_listen': '目标审计检测', 
    'net_audit': '网络行为审计', 
    'block': '通信阻断',
    'ip_whitelist':'IP白名单过滤'
}
var submoduleType = {
    'trojan': '木马攻击', 
    'attack': '漏洞利用', 
    'malware': '恶意程序', 
    'other': '其他攻击', 
    'abnormal': '未知攻击', 
    'finger_file': '密标文件', 
    'sensitive_file': '标密文件',
    'keyword_file': '关键字', 
    'encryption_file': '加密文件', 
    'compress_file': '压缩文件', 
    'picture_file': '图片筛选', 
    'style_file': '版式检测',
    'ip_listen': 'IP审计', 
    'domain_listen': '域名审计', 
    'url_listen': 'URL审计', 
    'account_listen': '帐号审计', 
    'net_log': '通联关系审计', 
    'app_behavior': '应用行为审计',
    'block': '通信阻断',
    'ip_whitelist':'IP白名单过滤'
}
var moduleStatus = {
    'on':'开启',
    'off':'<span style="color:red">关闭</span>',
    '':'<span style="color:red">关闭</span>'
}

/*function switchShow(panel){
    if(panel=="left"){
        $('.container-left').fadeIn();
        $('.container-right').fadeOut();
        $('.container-left').css('width','100%')
    }else{
        $('.container-right').fadeIn();
        $('.container-left').fadeOut();
        $('.container-right').css('width','100%');
    }
    
}*/
function switchShow(panel,that){
    var _this = $(that);
    if(panel=="left"){
        if(_this.hasClass('btn-primary')){
            if($('.container-right').css('display')=='none'){
                return;
            }
            _this.removeClass('btn-primary');
            $('.container-left').hide();
            if($('.container-right').css('display')!='none'){
                $('.container-right').css('width','100%');
            }
        }else{
            _this.addClass('btn-primary');
            
            if($('.container-right').css('display')!='none'){
                $('.container-right').removeAttr("style");
            }else{
                $('.container-left').css('width','100%');
            }
            setTimeout(function(){
                $('.container-left').show();
            },1000)
        }
    }else{
        if(_this.hasClass('btn-primary')){
            if($('.container-left').css('display')=='none'){
                return;
            }
            _this.removeClass('btn-primary');
            $('.container-right').hide();
            if($('.container-left').css('display')!='none'){
                $('.container-left').css('width','100%');
            }
        }else{
            _this.addClass('btn-primary');
            $('.container-right').show();
            if($('.container-left').css('display')!='none'){
                $('.container-left').removeAttr("style")
            }else{
                $('.container-right').css('width','100%');
            }
        }
    }
    
}
$('#hintModal').on('hide.bs.modal', function () {
    $('#hintModal').scrollTop(0);
})

// 跳转策略页面
function postRule(policy_type){
    var param = {
        device_id: device_id
    }
    var url = ruleType[policy_type][1]+".php";
    post_blank(url,param);
}
</script>
</body>
</html>

