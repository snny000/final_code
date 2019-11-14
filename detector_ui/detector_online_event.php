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

    <title>检测器在线事件</title>

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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;检测器在线事件</h4>
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

                <input id="device_id" type="text" class="form-control search-input btn-interva2" placeholder="检测器ID(模糊搜索)">

                <div class="dropdown btn-interval2 dropdown-inline">
                    <button type="button" data-toggle="dropdown"
                            class="btn dropdown-btn dropdown-menu-width"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <span id="event" class="pull-left" value="-1">所有事件</span>
                        <i class="fa fa-sort-down pull-right"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                        <li onclick="selectProtoFwd(this);" value="-1">所有事件</li>
                        <li onclick="selectProtoFwd(this);" value="上线">上线</li>
                        <li onclick="selectProtoFwd(this);" value="离线">离线</li>
                    </ul>
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
                    <th width="10%">ID</th>
                    <th width="10%">检测器ID</th>
                    <th width="10%">事件</th>
                    <th width="10%">时间</th>
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td>
                        <div class="pull-left">

                            <button class="btn btn-default btn-sm" id="refresh">刷新</button>
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
    buildFrame("menu-detector1");


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
        $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"));
        $(obj).parent().parent().find("span:first").text($(obj).text());
        //$("#"+id).attr("value",$(obj).attr("value"));
       // $("#"+id).text($(obj).text());
    }

    $('button.condition-btn.singlechoose').click(function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
    });

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

    /*
    var msgListObj = eval(msgList);
    List(msgListObj); //默认列表
    */

    function List(msgListObj){

        $("#maintable tbody tr").remove();
        var _row = $("<tr>" +
            "<td ></td>"+
            "<td ></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();
            row.attr("id",msgListObj[i].id)
            row.find("td:eq(0)").html(msgListObj[i].id);
            row.find("td:eq(1)").text(msgListObj[i].device_id);
            event_td = row.find("td:eq(2)");
            if (msgListObj[i].event=='上线') {
                var event = '<span style="color: green">' + msgListObj[i].event + '</span>';
            } else{
                var event = '<span style="color: red">' + msgListObj[i].event + '</span>';
            }
            event_td.html(event);
            row.find("td:eq(3)").text(msgListObj[i].time);

            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }


    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.online_event_count",
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
                pagination(ret,"/ajax_action_detector.php?uu=detector.online_event_show&p_size="+p_size,parseInt(currentPage),searchParam)
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