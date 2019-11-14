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

    <title>指挥中心接入配置</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

    <!-- Add custom CSS here -->
    <link href="css/frame.css" rel="stylesheet">
    <link href="css/product.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <link href="css/detector.css" rel="stylesheet">
    <link href="bootstrap-datetimepicker-master/css/bootstrap-datetimepicker.min.css" rel="stylesheet" media="screen">
    <link href="css/city-picker.css" rel="stylesheet">

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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;指挥中心接入配置</h4>
            </div>

        </div>

        <div class="hidden">
            <div class="operate_config" style="display:inline-flex;">
                <button id="configButton" type="button" class="btn btn-primary hidden"><i class="fa fa-edit">&nbsp;&nbsp;</i>配置指挥参数</button>
                <button id="registerButton" type="button" class="btn btn-primary hidden"><i class="fa fa-link">&nbsp;&nbsp;</i>注册</button>
                <button id="resetButton" type="button" class="btn btn-primary btn-interval2 hidden"><i class="fa fa-unlink">&nbsp;&nbsp;</i>重置指挥配置</button>
                <button id="authButton" type="button" class="btn btn-primary btn-interval2 hidden"><i class="fa fa-link">&nbsp;&nbsp;</i>认证</button>
            </div>
        </div>

        <div id="export_div">

        </div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr>
                    <th width="10%">管理中心ID</th>
                    <th width="10%">管理中心IP</th>
                    <th width="10%">管理中心序列号</th>
                    <th width="10%">指挥节点ID</th>
                    <th width="10%">指挥节点IP</th>
                    <th width="10%">下行IP白名单</th>
                    <th width="8%">接入状态</th>
                    <th width="8%">注册时间</th>
                    <th width="8%">认证时间</th>
                    <th width="20%">操作</th>
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td>
                        <div class="pull-left">

                            <button class="btn btn-default btn-sm" id="refresh">刷新</button>
                            <button class="btn btn-default btn-sm btn-interval2" id="add_whitelist">修改IP白名单</button>
                        </div>

                    </td>
                </tr>

                </tfoot>
            </table>

        </div>

        <div class="row" style="text-align: center;">
            <img id='center_status_img' src="images/no_director_mode.jpg">
        </div>
    </div>

</div>
<!-- /#page-wrapper -->

<!-- 模态框（Modal） -->
<div class="modal fade" id="configModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 490px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    配置管理中心接入信息
                </h4>
            </div>
            <div class="modal-body">
                <div id="add_valid_msg" class="alert alert-danger hidden" role="alert"></div>
                <span id="add_id" class="hidden"></span>
                <div class="padding_top_5"><span>管理中心ID：</span> <input id="add_center_id" class="form-control"></div>
                <div class="padding_top_5"><span>管理中心IP：</span> <input id="add_center_ip" class="form-control"></div>
                <div class="padding_top_5"><span>管理中心序列号：</span> <input id="add_center_serial" class="form-control" disabled></div>
                <div class="dropdown-inline padding_top_5">
                    <span> 节点类型:</span>
                    <div class="dropdown">
                        <button type="button" data-toggle="dropdown"
                                class="btn dropdown-btn dropdown-menu-width"
                                aria-haspopup="true"
                                aria-expanded="false">
                            <span id="add_type" class="pull-left" value="-1">未选择</span>
                            <i class="fa fa-sort-down pull-right"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist" style="z-index: 1000000">
                            <li onclick="selectProtoFwd(this); setCityPickerLevel(this);" value="-1">所有类型</li>
                            <li onclick="selectProtoFwd(this); setCityPickerLevel(this);" value="0">国家</li>
                            <li onclick="selectProtoFwd(this); setCityPickerLevel(this);" value="1">省</li>
                            <li onclick="selectProtoFwd(this); setCityPickerLevel(this);" value="2">市</li>
                            <li onclick="selectProtoFwd(this); setCityPickerLevel(this);" value="3">县</li>
                        </ul>
                    </div>
                </div>
                <div class="docs-methods padding_top_5">
                    <form class="form-inline">
                        <div id="distpicker">
                            <div class="form-group">
                                <div style="position: relative;">
                                    <input id="city-picker" class="form-control" style="width:365px;" readonly type="text" placeholder="请选择节点类型"
                                           data-toggle="city-picker">
                                </div>
                            </div>
                            <div class="form-group">
                                <button class="btn btn-warning" id="reset" type="button" onclick="cityHelper.reset();">重置</button>
                                </button>
                            </div>
                        </div>
                    </form>
                </div>

                <div class="padding_top_5"><span>指挥节点名：</span> <input id="add_node_name" class="form-control"></div>
                <div class="padding_top_5"><span class="padding_top_5">指挥节点IP：</span> <input id="add_node_ip" class="form-control"></div>
                <div></div>

            </div>
            <div class="modal-footer">
                <button id="configSubmitButton" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="whitelistModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 490px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    修改下行IP白名单
                </h4>
            </div>
            <div class="modal-body">
                <div id="add_valid_msg" class="alert alert-danger hidden" role="alert"></div>
                <span id="add_id" class="hidden"></span>
                <div class="padding_top_5">
                    <span>IP：</span>
                    <textarea id="whitelist_ip" class="form-control search-input btn-interval" autofocus rows="4" cols="45"
                            placeholder="请输入需要的IP,多条可换行输入" style="min-height: 40px"></textarea>
                </div>
            </div>
            <div class="modal-footer">
                <button id="whitelistSubmitButton" type="button" class="btn btn-primary">提交</button>
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
<script src="js/city-picker.data.js"></script>
<script src="js/city-picker.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script>
    buildFrame("menu-director");

    function initTextHelper() {
        var table = $('#maintable');
        table.find("th:eq(5)").html(table.find("th:eq(5)").html() + helper_ele);
        table.find("th:eq(5) i.hint-helper").attr("value", director_config_ip_whitelist_helper_text);

//        $("#resetButton").html($("#resetButton").html() + helper_ele);
//        $("#resetButton i.hint-helper").attr("value", director_config_reset_helper_text);
    }

    initTextHelper();

    var citypicker = $('#city-picker');
    var cityHelper = CityHelper;
    cityHelper.init(citypicker);

    function setCityPickerLevel(obj) {
        if(parseInt($(obj).attr("value")) == 0) {
            cityHelper.generateNodeSerial(parseInt($(obj).attr("value")), $('#add_center_serial'));
        }
        cityHelper.setCityPickerLevel(obj);
    }

    $('div#distpicker').on("click", "div.city-picker-dropdown dl dd a", function () {
        cityHelper.generateNodeSerial(parseInt($('#add_type').attr('value')), $('#add_center_serial'));
    });

    function selectProtoFwd(obj) {
        $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"));
        $(obj).parent().parent().find("span:first").text($(obj).text());
        //$("#"+id).attr("value",$(obj).attr("value"));
       // $("#"+id).text($(obj).text());
    }

    $('button.condition-btn.singlechoose').click(function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
    });

    $("#add_whitelist").click(function () {
        if (center_info.length > 0 && center_info[0].center_status == 1) {
            setWhitelistModel();
        } else {
            alert("未接入指挥节点，不能修改IP白名单");
        }
    });
    
    function setWhitelistModel() {
        $("#add_valid_msg").addClass("hidden");
        $("#add_id").text("0");
        if (center_info.length > 0) {
            $("#whitelist_ip").val(convertIpWhitelist(center_info[0].ip_whitelist, '\n'));
        }
        $("#whitelistModal").modal("show");
    }

    $("#whitelistSubmitButton").click(function () {
        var result = validateWhitelistModel();
        if(!result["ischeck"]){
            return;
        } else {
            console.log(result["param"]);
//            return;
            $.ajax({
                url: "/ajax_action_detector.php?uu=center.update_ip_whitelist",
                type: "post",
                data: result["param"],
                success:function(data) {
                    console.log(data);
                    var ret = JSON.parse(data);
                    alert(ret["msg"]);
                    refresh();
                }
            });
            $("#whitelistModal").modal('hide');
        }
    });
    
    function validateWhitelistModel() {
        var add_ip = [];
        var ischeck = true;
        var error_text = "";
        var ip = $("#whitelist_ip").val().trim();
        if (ip == '') {
            error_text = error_text + "添加IP为空!";
            ischeck = false;
        }

        if (ip.indexOf("\n") < 0) {
            if (!isValidIP(ip)) {
                error_text = error_text + "<br/>添加的单IP不合法!";
                ischeck = false;
            } else {
                add_ip.push(ip);
            }
        } else {
            var ip_list = ip.split("\n");
            for (var i in ip_list) {
                if(!isValidIP(ip_list[i].trim())) {
                    error_text = error_text + "<br/>添加的多IP中有不合法IP!：" + ip_list[i];
                    ischeck = false;
                    break
                }
                add_ip.push(ip_list[i].trim());
            }
        }

        if(!ischeck) {
            console.debug("error_text: ", error_text.trim());
            if(error_text.indexOf("<br/>") == 0) {
                error_text = error_text.substring(5);
            }
            $("#add_valid_msg").html(error_text.trim());
            $("#add_valid_msg").removeClass("hidden");
            return {"ischeck": ischeck};
        } else {
            var param = {
                "center_id": center_info[0].center_id,
                "ip": JSON.stringify(add_ip)
            };
            return {"ischeck": ischeck, "param": param};
        }
    }
    

    $("#maintable").on("click", '#configButton', function () {
        console.debug("click config button");
        setConfigModel();
    });

    function setConfigModel() {
        $("#add_valid_msg").addClass("hidden");
        $("#add_id").text("0");
        if (center_info.length == 0) {
            $("#add_center_id").val('');
            $("#add_center_ip").val('');
            $("#add_node_name").val('');
            $("#add_node_ip").val('');
            $("#add_center_serial").val('');
        } else {
            $("#add_center_id").val(center_info[0].center_id);
            $("#add_center_ip").val(center_info[0].center_ip);
            $("#add_node_name").val(center_info[0].src_node);
            $("#add_node_ip").val(center_info[0].src_ip);
            $("#add_center_serial").val(center_info[0].center_serial);
        }

        firstSelect("add_type");

        cityHelper.$citypicker.attr("placeholder", "请选择节点类型");
        cityHelper.$citypicker.citypicker('destroy');

        $('#configModal').modal('show');
    }

    function isValidIP(ip) {
        var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
        return reg.test(ip);
    }

    function validateConfigModel() {
        console.debug("begin validate modal");
        var ischeck = true;
        var add_center_id = $("#add_center_id").val().trim();
        var add_center_ip = $("#add_center_ip").val().trim();
        var add_center_serial = $("#add_center_serial").val().trim();
        var add_node_name = $("#add_node_name").val().trim();
        var add_node_ip = $("#add_node_ip").val().trim();
        var add_type = parseInt($("#add_type").attr("value"));

        var error_text = "";
        if(add_center_id == ""){
            error_text = error_text + "管理中心ID不能为空!";
            ischeck = false;
        }
        if(add_center_ip == "") {
            error_text = error_text + "<br/>管理中心IP不能为空!";
            ischeck = false;
        } else if(!isValidIP(add_center_ip)) {
            error_text = error_text + "<br/>管理中心IP不合法!";
            ischeck = false;
        }
        if(add_center_serial == ""){
            error_text = error_text + "<br/>管理中心序列号不能为空!";
            ischeck = false;
        }
        if(add_node_name == ""){
            error_text = error_text + "<br/>指挥节点名不能为空!";
            ischeck = false;
        }
        if(add_node_ip == "") {
            error_text = error_text + "<br/>指挥节点IP不能为空!";
            ischeck = false;
        } else if(!isValidIP(add_node_ip)) {
            error_text = error_text + "<br/>指挥节点IP不合法!";
            ischeck = false;
        }


        $("#configModal input").each(function(){
            var value = $(this).val(); //这里的value就是每一个input的value值~

            if(!value.match(/^[\u4E00-\u9FA5a-zA-Z0-9_\/]{0,}$/) && $(this).attr("id") != "add_node_ip" && $(this).attr("id") != "add_center_ip"){

                error_text = error_text + "<br/>" + $(this).prev().text() + "存在非法字符!";

                ischeck = false
            }

        });

        if(!ischeck) {
            console.debug("error_text: ", error_text.trim());
            if(error_text.indexOf("<br/>") == 0) {
                error_text = error_text.substring(5);
            }
            $("#add_valid_msg").html(error_text.trim());
            $("#add_valid_msg").removeClass("hidden");
            return {"ischeck": ischeck};
        } else {
            var param = {
                "id": parseInt($("#add_id").text()),
                "center_id": add_center_id,
                "center_ip": add_center_ip,
                "center_serial": parseInt(add_center_serial),
                "src_node": add_node_name,
                "src_ip": add_node_ip
            };
            return {"ischeck": ischeck, "param": param};
        }
    }

    $("#configSubmitButton").click(function(){
        saveConfigData();
    });

    function saveConfigData() {
        var result = validateConfigModel();
        if(!result["ischeck"]){
            return;
        } else {
            console.log(result["param"]);
//            return;
            $.ajax({
                url: "/ajax_action_detector.php?uu=center.save_director_config",
                type: "post",
                data: result["param"],
                success:function(data) {
                    console.log(data);
                    var ret = JSON.parse(data);
                    alert(ret["msg"]);
                    refresh();
                }
            });
            $("#configModal").modal('hide');
        }
    }

    $("#maintable").on("click", '#registerButton', function () {
        $.ajax({
            url: "/ajax_action_detector.php?uu=center.register",
            type: "post",
            data: {'center_id': center_info[0].center_id},
            success:function(data) {
                console.log(data);
                var ret = JSON.parse(data);
                alert(ret["msg"]);
                refresh();
            }
        });
    });

    $("#maintable").on("click", '#resetButton', function () {
        var msg = "是否确定重置？";
        if (confirm(msg)==true){
            $.ajax({
                url: "/ajax_action_detector.php?uu=center.reset",
                type: "post",
                data: {'center_id': center_info[0].center_id},
                success:function(data) {
                    console.log(data);
                    var ret = JSON.parse(data);
                    alert(ret["msg"]);
                    refresh();
                }
            });
        } else {
            return false;
        }
    });

    $("#maintable").on("click", '#authButton', function () {
        $.ajax({
            url: "/ajax_action_detector.php?uu=center.auth",
            type: "post",
            data: {'center_id': center_info[0].center_id},
            success:function(data) {
                console.log(data);
                var ret = JSON.parse(data);
                alert(ret["msg"]);
                refresh();
            }
        });
    });

    var center_info = [];

    function List(msgListObj){

        $("#maintable tbody tr").remove();
        var _row = $("<tr>" +
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
            "</tr>");

        if (msgListObj.length == 0) {
            setStatusImages(0);
            var row = _row.clone();
            row.attr("id", '');
            row.find("td:eq(0)").html("<p style='color: #FF0000;'>未配置</p>");
            row.find("td:eq(1)").html("<p style='color: #FF0000;'>未配置</p>");
            row.find("td:eq(2)").html("<p style='color: #FF0000;'>未配置</p>");
            row.find("td:eq(3)").html("<p style='color: #FF0000;'>未配置</p>");
            row.find("td:eq(4)").html("<p style='color: #FF0000;'>未配置</p>");
            row.find("td:eq(5)").html("<p style='color: #FF0000;'>未配置</p>");
            row.find("td:eq(5)").html(isCenterAccess(0));
            row.find("td:eq(9)").html(operateFormat(0));

            row.show();
            row.appendTo("#maintable tbody");
        } else {
            setStatusImages(center_info[0].center_status);
            for (var i = 0; i < msgListObj.length; i++) {
                var row = _row.clone();
                row.attr("id",msgListObj[i].id);
                row.find("td:eq(0)").html(msgListObj[i].center_id);
                row.find("td:eq(1)").html(msgListObj[i].center_ip);
                row.find("td:eq(2)").html(msgListObj[i].center_serial);
                row.find("td:eq(3)").html(msgListObj[i].src_node);
                row.find("td:eq(4)").html(msgListObj[i].src_ip);
                row.find("td:eq(5)").html(convertIpWhitelist(msgListObj[i].ip_whitelist));
                row.find("td:eq(6)").html(isCenterAccess(msgListObj[i].center_status));
                if (msgListObj[i].center_status == 0 || msgListObj[i].center_status == 6) {
                    row.find("td:eq(7)").html('');
                    row.find("td:eq(8)").html('');
                } else if (msgListObj[i].center_status == 2 || msgListObj[i].center_status == 3 || msgListObj[i].center_status == 4) {
                    row.find("td:eq(7)").html(msgListObj[i].register_time);
                } else {
                    row.find("td:eq(7)").html(msgListObj[i].register_time);
                    row.find("td:eq(8)").html(msgListObj[i].auth_time);
                }

                row.find("td:eq(9)").html(operateFormat(msgListObj[i].center_status));

                row.show();
                row.appendTo("#maintable tbody");
            }
        }

    }

    function setStatusImages(status) {
        switch (status) {
            case 0:
                $("#center_status_img").attr('src', 'images/no_director_mode.png');
                break;
            case 1:
                $("#center_status_img").attr('src', 'images/director_mode.png');
                break;
            case 2:
                $("#center_status_img").attr('src', 'images/under_audit.png');
                break;
            case 3:
                $("#center_status_img").attr('src', 'images/under_register.png');
                break;
            case 4:
                $("#center_status_img").attr('src', 'images/under_auth.png');
                break;
            case 5:
                $("#center_status_img").attr('src', 'images/under_auth.png');
                break;
            case 6:
                $("#center_status_img").attr('src', 'images/under_register.png');
                break;
            default:
                break;
        }
    }

    function convertIpWhitelist(ip_whitelist, concat_str='<br/>') {
        console.log(ip_whitelist);
        ips = '';
        for(var ip in ip_whitelist) {
            ips = ips + concat_str + ip_whitelist[ip]
        }
        return ips.substring(concat_str.length)
    }

    function isCenterAccess(status){
        var device_statusMap={0: '未接入指挥中心', 1: '指挥模式', 2:'等待指挥审核', 3: '审核失败', 4 : '审核成功', 5 : '认证失败', 6 : '待注册'};
        var status_html = $('<span>'+device_statusMap[status]+'</span>');
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
            case 0:
                $(status_html).css({'color':'red','font-weight':'bold'});
                break;
            default:
                $(status_html).css('color', 'red');
                break;
        }
        return status_html;
    }

    function operateFormat(status) {
        var all_operate = $('.operate_config').clone();
        switch (status) {
            case 0:
                all_operate.find('#configButton').removeClass('hidden');
                break;
            case 6:
                all_operate.find('#registerButton').removeClass('hidden');
                break;
            case 1:
                all_operate.find('button').removeClass('hidden');
                all_operate.find('#configButton').addClass('hidden');
                all_operate.find('#registerButton').html("<i class=\"fa fa-edit\">&nbsp;&nbsp;</i>重新注册");
                all_operate.find('#authButton').html("<i class=\"fa fa-edit\">&nbsp;&nbsp;</i>重新认证");
                break;
            case 2:
//                all_operate.find('#configButton').removeClass('hidden');
                break;
            case 3:
                all_operate.find('#registerButton').removeClass('hidden');
                break;
            case 4:
                all_operate.find('#authButton').removeClass('hidden');
                break;
            case 5:
                all_operate.find('#authButton').removeClass('hidden');
                break;
            default:
                break;
        }
        return all_operate;
    }

    function LoadPage(currentPage, searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=center.show",
            type: "post",
            data: searchParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 200) {
                    center_info = ret["msg"];
                    List(ret["msg"]);
                }
                else {
                    alert(ret["msg"]);
                }
            },

            beforeSend: function () {
                $("#maintable tbody tr").remove();
                $("#maintable tbody").append("<tr><td colspan=" + col_size + " style='text-align: center'><img src='images/loading.gif'></td></tr>")
            },
            error: function () {
                alert("无法连接服务器");
            }
        })
    }

    var globalSearchParam = {random:1};
    //第一次加载分页
    LoadPage(globalSearchParam);

    $("#searchButton").click(function(){
        globalSearchParam = {random:1};
        globalSearchParam = getSearchParam(globalSearchParam);
        LoadPage(1,globalSearchParam)
    })

    function getSearchParam(params) {
        var device_id =  $("#device_id").val();
        var event = $("#event").attr("value").toString()
        var time_min = $("#time_min").val()
        var time_max =$("#time_max").val()

        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        if(event!="-1"){
            params["event"] = event
        }

        if(device_id!=""){
            params["device_id"] = device_id
        }

        if(time_min!=""){
            params["time_min"] = time_min
        }
        if(time_max!="") {
            params["time_max"] = time_max
        }
        return params
    }

    $("#clearButton").click(function(){
        firstSelect("event");
        $("#device_id").val("");
        $("#time_min").val("");
        $("#time_max").val("");
    })


</script>

</body>
</html>