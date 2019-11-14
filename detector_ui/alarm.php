<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');
require_once(dirname(__FILE__) . '/require_get_parameter_for_post.php');
//require_once( 'data/get.json.from.server.php');
//require_once( 'service/service.php');
//$user = new User();
//$user = checkLogin(1, 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);

?>

<!DOCTYPE HTML>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>告警列表</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

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

        .date_label{
            float: left;
            margin-top: 5px;
            margin-right: 4px;
        }
        .date_div{
            width: 400px;
            float: left;
        }
    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;告警列表</h4>
            </div>

        </div>

        <div class="row btn-banner">
                <input id="alarm_id" type="text" class="form-control search-input" placeholder="告警ID(模糊搜索)">
                <input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器ID(模糊搜索)">
                <input id="organs" type="text" class="form-control search-input btn-interval" placeholder="部署单位(模糊搜索)">
                <input id="rule_id" type="text" class="form-control search-input btn-interval" placeholder="规则编号(模糊搜索)">
                <input id="group_id" type="text" class="form-control search-input btn-interval" placeholder="任务组(模糊搜索)">
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
                </div>

                <div class="dropdown btn-interval dropdown-inline">
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

        </div>
        <div class="row btn-banner">
            <div class="form-group">
                <!-- <label for="dtp_input1" class="col-md-2 control-label">DateTime Picking</label> date_label date_div-->
                <!-- col-md-5-->
                <div class="input-group date form_datetime date_div" style="width: 160px">
                    <input id="time_min" class="form-control" size="16" type="text" value="" readonly placeholder="开始时间">
                    <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                </div>

                <div class="input-group date form_datetime date_div btn-interval2" style="width: 160px">
                    <input id="time_max" class="form-control" size="16" type="text" value="" readonly placeholder="截止时间">
                    <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
                </div>

                <button id="searchButton" type="button" class="btn btn-primary btn-interval2"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
                <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>
            </div>
        </div>

        <div id="export_div">

        </div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="10%">告警ID</th>
                    <th width="10%">检测器ID</th>
                    <th width="5%">检测器厂商</th>
                    <th width="5%">部署单位</th>
                    <th width="8%">告警类型</th>
                    <th width="8%">源IP</th>
                    <th width="8%">目的IP</th>
                    <th width="5%">风险级别</th>
                    <th width="10%">规则编号</th>
                    <th width="10%">任务组</th>
                    <th width="10%">告警时间</th>
                    <th width="8%">操作</th>
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
<!--                            <button class="btn btn-default btn-sm" id="export" onclick="method5('maintable')">导出</button>-->
                            <button class="btn btn-default btn-sm" id="export" onclick="export_file()">导出报表</button>
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

<!-- 模态框（Modal） -->
<div class="modal fade" id="checkModal" tabindex="-1" role="dialog" aria-labelledby="checkLabel" aria-hidden="true">
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
                   <span> 审核人:</span> <input id="op_person" type="text" class="search-input form-control" style="width:100%";>
                </div>
                <div style="margin-top: 10px">
                     <span>未通过原因:</span>
                     <textarea id="register_message" style="width:100%;height:80px;" class="form-control"></textarea>
                </div>

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭
                </button>
                <button id="check-submit" type="button" class="btn btn-primary">
                    提交
                </button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>



<div class="modal fade" id="detailModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    告警详情
                </h4>
            </div>
            <div class="modal-body">
                <table class="table no-margin modal-form">
                <tbody id="detail-form">

                </tbody>
                </table>
                <!--
                <div class="widget no-margin">
                    <div class="widget-header widget-header-index">
                        <div class="title widget-header-index-title">
                            IP侦听告警
                        </div>
                    </div>
                    <div>
                        <table class="table no-margin modal-form">
                            <tbody id="detail-form">

                            </tbody>
                        </table>
                    </div>
                </div>
                -->
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

</div>
<!-- /#wrapper -->

<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script>
    buildFrame("menu-alert1");


/*    function getStrDownload(file_path, id) {

        return "<a href='/ajax_action_download.php?uu="+file_path +"'>&nbsp;下载告警文件</a>";


    }*/
    function export_file() {
        //  window.location.href = "detector_detail.php?id=" + id;

        var file_path = "/alarm/export";
        var file_name = "告警统计报表.xlsx";
        var warning_type = $("#warning_type").attr("value").toString();
        if(warning_type == '0'){
            alert("请选择告警类型，也可设置其他查询字段");
            return;
        }
        var params = {};
        params = getSearchParam(params);
        var param_str = '';
        for(var key in params) {
            param_str += "&" + key + "=" + params[key]
        }
//        console.log(params, "#########" + param_str);
        //window.open("/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+"");
        window.location.href ="/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+param_str;

        //post('detector_detail.php',{id:id});
    }


    $('.form_datetime').datetimepicker({
        language:  'zh-CN',
        minView: "month",
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayBtn: true,
        /*
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        forceParse: 0,
        showMeridian: 1
         */
    });

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
                        $("<tr><td colspan='10' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
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




    function check(id){
        $.ajax({
            url: "/ajax_action_detector.php?uu=detail&id="+id, //ajax请求
            cache: false,
            success: function(data){
                console.log(data)
                var server = JSON.parse(data);

                var msg = server.msg;
                var base_form = "<tr><td><span class='text-muted'> ID：</span><span id='check_id'>"+msg.id+"</span></td></tr>" +
                    "<tr><td><span class='text-muted'> 设备厂商:</span>"+msg.contractor+"</td></tr>"
                // $("tbody#base-form").html(base_form);
                $("tbody#base-form").html(base_form);
            }
        });
    }


    $("#check-submit").click(function(){
            $.ajax({
                url: "/ajax_action_detector.php?uu=detector.permit",
                type: "post",
                data: {id:$("#check_id").text(),type:$("#ischeck .active").prop("value"),op_person:$("#op_person").val(),register_message:$("#register_message").val()},
                success:function(data) {
                    var ret = JSON.parse(data);
                    console.log(ret)
                }
            })
            $("#checkModal").modal('hide');
        }
    )

    function detail(status,id){

        var map = {
            1: [ //木马告警详情
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "攻击IP"], ["sport", "攻击端口"],
                ["smac", "攻击MAC地址"], ["dip", "被攻击IP"], ["dport", "被攻击端口"], ["dmac", "被攻击MAC地址"],
                ["time", "告警时间"], ["risk", "风险级别"], ["trojan_id", "木马分类编号"],  ["os", "攻击适用的操作系统"],
                ["trojan_name", "木马名称"], ["trojan_type", "木马类型"], ["desc", "攻击描述"], ["device_id", "告警上报检测器"],
                ["report_time", "中心接收告警时间"]
            ],

            2: [ //漏洞攻击告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "攻击IP"], ["sport", "攻击端口"],
                ["smac", "攻击MAC地址"], ["dip", "被攻击IP"], ["dport", "被攻击端口"], ["dmac", "被攻击MAC地址"],
                ["time", "告警时间"], ["risk", "风险级别"], ["attack_type", "攻击类型"], ["application", "攻击适用的应用程序"],
                ["os", "攻击适用的操作系统"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            3: [ //恶意程序告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["time", "告警产生时间"], ["risk", "风险级别"], ["malware_type", "恶意程序种类"], ["malware_name", "恶意程序名称"],
                ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"], ["protocol", "协议名"],
                ["sender", "发送者"], ["recver", "接收者"], ["cc", "邮件抄送者"],
                ["bcc", "邮件密送者"], ["subject", "邮件主题"], ["mail_from", "MAIL FROM命令提交的邮件发送者"],
                ["rcpt_to", "RCPT TO命令提交的邮件接收者"],["ehlo", "EHLO命令提交的IP信息"]
            ],

            4: [ //其他攻击窃密告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "攻击方IP"],["sport", "攻击方端口"],
                ["smac", "攻击方MAC地址"], ["dip", "被攻击IP"], ["dport", "被攻击端口"], ["dmac", "被攻击MAC地址"],
                ["time", "告警时间"], ["risk", "风险级别"], ["desc", "攻击窃密告警描述"], ["device_id", "告警上报检测器"],
                ["report_time", "中心接收告警时间"]
            ],

            5: [ //未知攻击窃密告警
                ["alarm_id", "告警编号"], ["sip", "攻击方IP"], ["sport", "攻击方端口"],
                ["smac", "攻击方MAC地址"], ["dip", "被攻击IP"], ["dport", "被攻击端口"], ["dmac", "被攻击MAC地址"],
                ["alert_type", "异常类型"], ["alert_policy", "异常判断依据"], ["alert_desc", "异常判断描述及上下文"], ["time", "告警时间"],
                ["risk", "风险级别"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            6: [ //邮件涉密告警
                ["alarm_id", "告警编号"], ["alert_type", "告警类型"], ["rule_id", "规则编号"],
                ["risk", "风险级别"], ["time", "告警数据采集时间"], ["sm_inpath", "实际告警文件内嵌路径"],
                ["sm_summary", "涉密数据摘要"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["xm_dir", "数据传输方向"], ["app_pro", "协议类型"], ["sender", "发件人邮箱"], ["receiver", "收件人邮箱"],
                ["cc", "抄送"], ["bcc", "密送"], ["subject", "邮件主题"], ["domain", "邮件提供商名"], ["protocol", "最上层协议类型"],
                ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            7: [ //即时通讯涉密告警
                ["alarm_id", "告警编号"], ["alert_type", "告警类型"], ["rule_id", "规则编号"],
                ["risk", "风险级别"], ["time", "告警数据采集时间"], ["sm_inpath", "实际告警文件内嵌路径"],
                ["sm_summary", "涉密数据摘要"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["xm_dir", "数据传输方向"], ["app_pro", "协议类型"], ["protocol", "消息的协议类型"], ["sender", "发件人"],
                ["receiver", "收件人"], ["account", "即时通讯账户"], ["msg_content", "聊天内容"], ["device_id", "告警上报检测器"],
                ["report_time", "中心接收告警时间"]
            ],

            8: [ //文件传输涉密告警
                ["alarm_id", "告警编号"], ["alert_type", "告警类型"], ["rule_id", "规则编号"],
                ["risk", "风险级别"], ["time", "告警数据采集时间"], ["sm_inpath", "实际告警文件内嵌路径"],
                ["sm_summary", "涉密数据摘要"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["xm_dir", "数据传输方向"], ["app_pro", "协议类型"], ["protocol", "消息的协议类型"], ["account", "FTP账号"],
                ["pwd", "FTP密码"], ["trans_dir", "文件传输方向"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            9: [ //HTTP涉密告警
                ["alarm_id", "告警编号"], ["alert_type", "告警类型"], ["rule_id", "规则编号"],
                ["risk", "风险级别"], ["time", "告警数据采集时间"], ["sm_inpath", "实际告警文件内嵌路径"],
                ["sm_summary", "涉密数据摘要"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["xm_dir", "数据传输方向"], ["app_pro", "协议类型"], ["protocol", "消息的协议类型"], ["domain", "访问域"],
                ["url", "访问url"], ["method", "HTTP请求方法"], ["ret_code", "HTTP返回码"], ["user-agent", "请求user-agent"],
                ["cookie", "请求的cookie信息"], ["server", "服务端的server信息"], ["refer", "引用页"],
                ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            10: [ //网盘涉密告警
                ["alarm_id", "告警编号"], ["alert_type", "告警类型"], ["rule_id", "规则编号"],
                ["risk", "风险级别"], ["time", "告警数据采集时间"], ["sm_inpath", "实际告警文件内嵌路径"],
                ["sm_summary", "涉密数据摘要"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["xm_dir", "数据传输方向"], ["app_pro", "协议类型"], ["protocol", "消息的协议类型"], ["account", "网盘账户"],
                ["domain", "网盘类型"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            11: [ //其他协议告警
                ["alarm_id", "告警编号"], ["alert_type", "告警类型"], ["rule_id", "规则编号"], ["risk", "风险级别"],
                ["time", "告警数据采集时间"], ["sm_inpath", "实际告警文件内嵌路径"], ["sm_summary", "涉密数据摘要"],
                ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"],["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["xm_dir", "数据传输方向"], ["app_pro", "协议类型"]
            ],

            12: [ //IP审计告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["time", "告警产生时间"], ["risk", "风险级别"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            13: [ //域名审计告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["time", "告警时间"], ["risk", "风险级别"], ["dns", "域名信息"], ["domain_ip", "域名解析IP"],
                ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            14: [ //URL审计告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["time", "告警时间"], ["risk", "风险级别"], ["url", "URL"], ["method", "请求方法"], ["ret_code", "返回码"],
                ["user-agent", "请求user-agent"], ["cookie", "请求的cookie信息"], ["server", "服务端的server信息"],
                ["refer", "引用页"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            15: [ //帐号审计告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["time", "告警时间"], ["risk", "风险级别"], ["sender", "发件人邮箱"], ["receiver", "收件人邮箱"],
                ["cc", "抄送"], ["bcc", "密送"], ["subject", "邮件主题"], ["mail_content", "邮件内容"],
                ["attachment", "附件名列表"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ],

            16: [ //阻断告警
                ["alarm_id", "告警编号"], ["rule_id", "规则编号"], ["sip", "源主机IP"], ["sport", "源主机端口"],
                ["smac", "源主机MAC地址"], ["dip", "目的主机IP"], ["dport", "目的端口"], ["dmac", "目的主机MAC地址"],
                ["time", "告警时间"], ["device_id", "告警上报检测器"], ["report_time", "中心接收告警时间"]
            ]
        }
        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.detail", //ajax请求
            type: "post",
            data: {id:id,warning_type:status},
            cache: false,
            success: function(data){
                console.log("数据："+data)
                var server = JSON.parse(data);
                var msg = server.msg;

                $("tbody#detail-form tr").remove();

                var _row = $("<tr><td><span class='text-muted'></span><span></span></td></tr>")
                var id_arrays = map[status]

                console.log(id_arrays)

                for (var i = 0; i < id_arrays.length; i++) {
                    var row = _row.clone();



                     if(status==5 && id_arrays[i][0]=='alert_policy')
                    {
                        var alert_policy_map= {1:'可疑心跳保活行为',2:'远程控制行为',3:'异常私有协议',4:'异常通用代理行为'}
                        row.find("span:eq(0)").html(id_arrays[i][1]+":")
                        row.find("span:eq(1)").html(alert_policy_map[msg[id_arrays[i][0]]])
                    }
                    else if(status>=6 && status<=11 && id_arrays[i][0]=='alert_type')
                    {
                        var alert_type_map= {1:'电子密标文件告警',2:'标密文件告警',3:'关键词告警',4:'加密文件告警',
                            5:'压缩文件告警',6:'图片文件告警',7:'含图片的文档告警',8:'版式文件告警'}
                        row.find("span:eq(0)").html(id_arrays[i][1]+":")
                        row.find("span:eq(1)").html(alert_type_map[msg[id_arrays[i][0]]])
                    }
                    else if(status>=1 && status<=15 && id_arrays[i][0]=='risk')
                    {
                        var riskMap = {0:'无风险',1:'一般级',2:'关注级',3:'严重级',4:'紧急级'}
                        row.find("span:eq(0)").html(id_arrays[i][1]+":")
                        row.find("span:eq(1)").html(riskMap[msg[id_arrays[i][0]]])

                    }


                    else if(status==15 && id_arrays[i][0]=='attachment')
                    {
                        var attachment_map= {1:'木马攻击窃密告警',2:'漏洞攻击窃密告警',3:'恶意程序窃密告警',4:'其他攻击窃密告警',
                            5:'未知攻击窃密告警',6:'邮件涉密告警',7:'即时通讯涉密告警',8:'文件传输涉密告警',
                            9:'HTTP涉密告警',10:'网盘涉密告警',11:'其他协议告警',12:'IP审计告警',
                            13:'域名审计告警',14:'URL审计告警',15:'账号审计告警',16:'通信阻断告警'}
                        row.find("span:eq(0)").html(id_arrays[i][1]+":")
                        row.find("span:eq(1)").html(attachment_map[msg[id_arrays[i][0]]])
                    }

                    else{
                        row.find("span:eq(0)").html(id_arrays[i][1]+":")
                        row.find("span:eq(1)").html(HTMLEncode(msg[id_arrays[i][0]]))
/*                         if(id_arrays[i][0]=='sender'){
                             console.log(id_arrays[i][0]+':'+id_arrays[i][1]+':'+msg[id_arrays[i][0]])
                         }*/
                    }
                    row.show();
                    row.appendTo("tbody#detail-form");
                }
                /*
                var detail_form = "<tr><td><span class='text-muted'>"+map[10][1][1]+"：</span><span id='check_id'>"+msg[map[10][1][0]]+"</span></td></tr>" +
                    "<tr><td><span class='text-muted'> 规则编号:</span>"+msg.rule_id+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 源主机IP:</span>"+msg.sip+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 源主机端口:</span>"+msg.sport+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 源主机MAC地址:</span>"+msg.smac+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 目的主机IP:</span>"+msg.dip+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 目的端口:</span>"+msg.dport+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 目的主机MAC地址:</span>"+msg.dmac+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 告警产生时间:</span>"+msg.time+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 风险级别:</span>"+msg.risk+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 告警上报检测器:</span>"+msg.device_id+"</td></tr>"+
                    "<tr><td><span class='text-muted'> 中心接收告警时间:</span>"+msg.report_time+"</td></tr>"
                    $("tbody#detail-form").html(detail_form);
                 */
            }
        });
        //
    }

    /**
     *
     * @param status 1-待提交,2-配置中,3-失效
     * @param id
     * @returns {*}
     */
    function getStrDownload(file_path, id,file_name) {
        //return "<a href='http://192.168.120.234/"+file_path +"'>&nbsp;下载报文</a>";
//        var str = "<a href='/ajax_action_download_rename.php?uu=/alarm/media/"+file_path +"&rename="+file_name+"'>&nbsp;下载报文</a>";
        var str = "<a href='/ajax_action_download_rename_common.php?uu=download&path="+file_path +"&rename="+file_name+"'>&nbsp;下载报文</a>";
        if(file_path == ''){

            str = "&nbsp;没有报文";
        }else{



        }
        return str;




        /* download='预算表.pdf'
        switch (status) {
            default
                return "<a href=\"javascript:void(0);\" data-toggle=\"modal\" data-target=\"#failModal\" onclick=\"fail("+ status +"," + id + ")\">查看</a>";
        }
        */
    }

    function getStrManipulation(status, id) {
        return "<a href=\"javascript:void(0);\" data-toggle=\"modal\" data-target=\"#detailModal\" onclick=\"detail("+ status +",'" + id.toString() + "')\">查看</a>";
        /*
         switch (status) {<a>&nbsp;研判</a>
         default
         return "<a href=\"javascript:void(0);\" data-toggle=\"modal\" data-target=\"#failModal\" onclick=\"fail("+ status +"," + id + ")\">查看</a>";
         }
         */
    }



    /*
    var msgListObj = eval(msgList);
    List(msgListObj); //默认列表
    */

    function List(msgListObj){
        //var contractorMap={'01':'厂商1', '02':'厂商2', '03':'厂商3'};
        var warning_typeMap={1:'木马攻击窃密告警',2:'漏洞攻击窃密告警',3:'恶意程序窃密告警',4:'其他攻击窃密告警',
            5:'未知攻击窃密告警',6:'邮件涉密告警',7:'即时通讯涉密告警',8:'文件传输涉密告警',
            9:'HTTP涉密告警',10:'网盘涉密告警',11:'其他协议告警',12:'IP审计告警',
            13:'域名审计告警',14:'URL审计告警',15:'账号审计告警',16:'通信阻断告警'}


        ///{1:'木马攻击',2:'漏洞攻击',3:'恶意程序',4:'未知攻击',5:'邮件涉密',6:'通讯涉密',7:'文件涉密',
       /// 8:'HTTP涉密',9:'网盘涉密',10:'IP侦听',11:'域名侦听',12:'URL侦听',13:'账号侦听'}
        var riskMap = {0:'无风险',1:'一般级',2:'关注级',3:'严重级',4:'紧急级'}

        $("#maintable tbody tr").remove();
        var _row = $("<tr>" +
            "<td><input type='checkbox' class='checkbox'></td>" +
            "<td ></td>"+
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
            var operatehtml = getStrManipulation(msgListObj[i].warning_type, msgListObj[i].id.toString())+getStrDownload(msgListObj[i].file_path, msgListObj[i].id,msgListObj[i].file_name);
            row.attr("id",msgListObj[i].id)
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>");
            row.find("td:eq(1)").text(msgListObj[i].alarm_id);
            row.find("td:eq(2)").html(msgListObj[i].device_id);
            row.find("td:eq(3)").text(contractorMap[msgListObj[i].contractor]);
            row.find("td:eq(4)").html(msgListObj[i].organs);
            row.find("td:eq(5)").html(warning_typeMap[msgListObj[i].warning_type]);
            row.find("td:eq(6)").html(msgListObj[i].sip);
            row.find("td:eq(7)").html(msgListObj[i].dip);
            row.find("td:eq(8)").text(riskMap[msgListObj[i].risk]);
            row.find("td:eq(9)").text(msgListObj[i].rule_id);
            row.find("td:eq(10)").text(msgListObj[i].group_id);
            row.find("td:eq(11)").text(msgListObj[i].time);
            row.find("td:eq(12)").html(operatehtml);

            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
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

    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.count",
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
                pagination(ret,"/ajax_action_detector.php?uu=alarm.show&p_size="+p_size,parseInt(currentPage),searchParam)
            },
 /*           beforeSend: function () {
                $(".loading-pic").removeClass("hidden");
            },*/
            beforeSend: function () {
                $("#maintable tbody tr").remove();
                $("#maintable tbody").append("<tr><td colspan='10'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
            },
            error: function () {
                alert("无法连接服务器");
            }
        })
    }

    var globalSearchParam = {random:1}
    //第一次加载分页
    LoadPage(1,globalSearchParam);


    $("#searchButton").click(function(){
        globalSearchParam = {random:1};
        globalSearchParam = getSearchParam(globalSearchParam);
        LoadPage(1,globalSearchParam)
    })

    function getSearchParam(params) {
        var alarm_id =  $("#alarm_id").val();
        var device_id =  $("#device_id").val();
        var organs =  $("#organs").val();
        var rule_id =  $("#rule_id").val();
        var group_id =  $("#group_id").val();
        var contractor = $("#contractor").attr("value").toString()
        var risk = $("#risk").attr("value").toString()
        var warning_module = $("#warning_module").attr("value").toString()
        var warning_type = $("#warning_type").attr("value").toString()
        var time_min = $("#time_min").val()
        var time_max =$("#time_max").val()

        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        if(contractor!="00"){
            params["contractor"] = contractor
        }
        if(risk!="-1"){
            params["risk"] = risk
        }
        if(warning_module!="0"){
            params["warning_module"] = warning_module
        }
        if(warning_type!="0"){
            params["warning_type"] = warning_type
        }

        if(device_id!=""){
            params["device_id"] = device_id
        }
        if(organs!=""){
            params["organs"] = organs
        }
        if(device_id!=""){
            params["device_id"] = device_id
        }
        if(alarm_id!=""){
            params["alarm_id"] = alarm_id
        }
        if(time_min!=""){
            params["time_min"] = time_min
        }
        if(time_max!="") {
            params["time_max"] = time_max
        }
        if(rule_id!="") {
            params['rule_id'] = rule_id
        }
        if(group_id!="") {
            params['group_id'] = group_id
        }

        return params
    }

    $("#clearButton").click(function(){
        firstSelect("contractor");
        firstSelect("risk");
        firstSelect("warning_module");
        firstSelect("warning_type");
        $("#device_id").val("");
        $("#organs").val("");
        $("#alarm_id").val("");
        $("#rule_id").val("");
        $("#group_id").val("");
        $("#time_min").val("");
        $("#time_max").val("");
    })

    /* 判断是否包含post_device_id,如果有则是从设备管理页跳转过来的，重载数据 */
$(function(){
    if(typeof(post_device_id) != "undefined"){
        setTimeout(function(){
            $('#device_id').val(post_device_id);
            $('#warning_module_list li[value='+post_warning_module+']').click();
            $('#warning_type_list li[value='+post_warning_type+']').click();
            $('#searchButton').click();
        },1000)
    }
})

</script>

</body>
</html>