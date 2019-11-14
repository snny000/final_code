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

    <title>系统审计</title>

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
           /*width: 400px;*/
            float: left;
        }
    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;系统审计</h4>
            </div>

        </div>

        <div class="row btn-banner">

           	<input id="log_id" type="text" class="form-control search-input date_div" placeholder="日志编号(模糊搜索)">
			<input id="user" type="text" class="form-control search-input date_div btn-interval" placeholder="操作用户名(模糊搜索)">
            <input id="opt_type" type="text" class="form-control search-input date_div btn-interval" placeholder="操作类型(模糊搜索)">
            <input id="message" type="text" class="form-control search-input date_div btn-interval" placeholder="日志详情(模糊搜索)">

        </div>
		<div class="row btn-banner">
            

            <div class="input-group date form_datetime date_div" style="width: 160px">
                <input id="time" class="form-control" size="16" type="text" value="" readonly placeholder="产生时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>

            <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>
        </div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit;border-collapse: inherit;word-wrap:break-word;word-break:break-all;">
                <thead class="thead">
                <tr >
                    <th width="1%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <!--<th width="9%">检测器编号</th>-->
                    <th width="10%">日志编号</th>
					<th width="10%">操作用户名</th>
					<th width="10%">操作类型</th>
					<th width="10%">审计日志类型</th>
					<th width="10%">日志详情</th>
					<th width="10%">产生时间</th>
					
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
                    <td colspan="7">
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


<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script>
    buildFrame("menu-detector3");
    $(function(){
        var globalSearchParam = {random:1}
        //第一次加载分页
        LoadPage(1,globalSearchParam)
    })


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
                    $("#maintable tbody").append("<tr><td colspan='8'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
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

    function List(msgListObj){
        console.log(msgListObj);

        $("#maintable tbody tr").remove();
        var _row = $("<tr>" +
            "<td></td>" +
            /*"<td style='color:#999999'></td>" +*/
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();
            // var operatehtml = getStrManipulation(msgListObj[i].warning_type, msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>")
           /* row.find("td:eq(1)").text(msgListObj[i].device_id);*/
			row.find("td:eq(1)").text(msgListObj[i].log_id);
			row.find("td:eq(2)").text(msgListObj[i].user);
			row.find("td:eq(3)").text(msgListObj[i].opt_type);
            row.find("td:eq(4)").html(msgListObj[i].event_type);
            row.find("td:eq(5)").html(msgListObj[i].message);
			row.find("td:eq(6)").html(msgListObj[i].time);
            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }

    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=audit_local.count",
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
                pagination(ret,"/ajax_action_detector.php?uu=audit_local.show&p_size="+p_size,parseInt(currentPage),searchParam)
            },
            beforeSend: function () {
                $(".loading-pic").removeClass("hidden");
            },
            error: function () {
                alert("无法连接服务器");
            }
        })
    }

    $("#searchButton").click(function(){
        /*var device_id =  $("#device_id").val();*/
		var log_id =  $("#log_id").val();

		var user =  $("#user").val();
        var opt_type =  $("#opt_type").val();

        var message = $("#message").val()
        var time =$("#time").val()

        globalSearchParam = {random:1}

/*        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
        }*/
		if(log_id!=""){
            globalSearchParam["log_id"] = log_id
        }

		if(user!=""){
            globalSearchParam["user"] = user
        }
        if(opt_type!=""){
            globalSearchParam["opt_type"] = opt_type
        }
        if(message!=""){
            globalSearchParam["message"] = message
        }
        if(time!=""){
            globalSearchParam["time"] = time
        }

        LoadPage(1,globalSearchParam)
    })

    $("#clearButton").click(function(){

       /* $("#device_id").val("");*/
		$("#log_id").val("");
        $("#opt_type").val("");
		$("#user").val("");
        $("#message").val("");
        $("#time").val("");
    })


</script>

</body>
</html>