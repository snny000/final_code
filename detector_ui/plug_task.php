<?php
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>插件任务</title>

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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;插件任务
                    <div class="btn-group" data-toggle="buttons">
                        <button type="button" href='plug_task.php' class="btn btn-default btn-primary">管理中心本地</button>
                        <button type="button" href='plug_task_director.php' class="btn btn-default">指挥节点下发</button>
                    </div>
                </h4>
            </div>
        </div>

        <div class="row btn-banner">
                <!--<input id="task_id" type="text" class="form-control search-input" placeholder="任务编号(模糊搜索)">-->

            <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="task_cmd" class="pull-left" value="">所有任务操作</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="">所有任务操作</li>
                    <li onclick="selectProtoFwd(this);" value="0">增量下发</li>
                    <li onclick="selectProtoFwd(this);" value="1">全量下发</li>
                    <li onclick="selectProtoFwd(this);" value="2">开启插件</li>
                    <li onclick="selectProtoFwd(this);" value="3">停止插件</li>
                </ul>
            </div>

            <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="is_valid" class="pull-left" value="-1">所有任务状态</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="-1">所有任务状态</li>
                    <li onclick="selectProtoFwd(this);" value='1'>任务执行中</li>
                    <li onclick="selectProtoFwd(this);" value='2'>任务执行成功</li>
                    <li onclick="selectProtoFwd(this);" value='3'>任务执行失败</li>
                    <li onclick="selectProtoFwd(this);" value='4'>任务错误</li>
                    <li onclick="selectProtoFwd(this);" value='0'>已忽略</li>
                    <!--<li onclick="selectProtoFwd(this);" value="not_get">未下发</li>-->
                </ul>
            </div>  

            <div class="input-group date form_datetime date_div " style="width: 160px">
                <input id="time_min" class="form-control" size="16" type="text" value="" readonly placeholder="开始时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>

            <div class="input-group date form_datetime date_div btn-interval" style="width: 160px">
                <input id="time_max" class="form-control" size="16" type="text" value="" readonly placeholder="截止时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>
            
            <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default btn-interval"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>

        </div>
        <!--<div class="row btn-banner">
            
            <div class="dropdown-inline btn-interval2">
                <select id="director_node" class="selectpicker form-control search-input" data-live-search="true" title="指挥节点">
                    <option value="">全部指挥节点</option>
                </select>
            </div>
            <input id="center_id" type="text" class="form-control search-input btn-interval" placeholder="管理中心(模糊搜索)">
        </div>-->

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="4%">任务编号</th>
                    <th width="4%">任务版本号</th>
                    <th width="5%">操作用户名</th>
                    <th width="4%">任务操作</th>
                    <th width="6%">下发检测器</th>
                    <th width="7%">任务发起时间</th>
                    <th width="7%">任务完成时间</th>
                    <th width="7%">任务包含规则数量</th>
                    <th width="5%">任务状态</th>
                    <th width="6%">操作</th>
                    <th width="14%">内容</th>
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
                        </div>
                        <div class="pull-right">
                            <?php
                            require_once(dirname(__FILE__) . '/require_page_bar_for_all_page.php');
                            ?>
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

<link href="css/bootstrap-select.css" rel="stylesheet">
<script type="text/javascript" src="js/bootstrap-select.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>
<script src="js/plug_operate.js"></script>
<script>
    buildFrame("menu-plug2");
    var globalSearchParam = {random:1}
    $(function(){
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
                    if (ret["code"] == 200 && ret["msg"].length>0) {

                        List(ret["msg"]);
                    } else if (ret["code"] == 20000 || ret["msg"].length == 0) {
                        $("#maintable tbody tr").remove();
                        $("<tr><td colspan=" + col_size + " style='text-align: center'><h4>没有记录</h4></td></tr>").appendTo("#maintable tbody");
                    }else if (ret["code"] == 9001){
                        window.location.href = "login.php?ref="+window.location.href;
                    }else{
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
        var task_cmd_map = {0:'增量下发',1:'全量下发',2:'开启插件',3:'停止插件'}
		
		var is_success_map = {0:'已忽略',1:'任务执行中',2:'任务执行成功',3:'任务执行失败',4:'任务错误'};

        $("#maintable tbody tr").remove();
        var _row = $("<tr>" +
            "<td></td>" +
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
            "<td style='color:#999999'></td>" +
            /*"<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +*/

            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();
           // var operatehtml = getStrManipulation(msgListObj[i].warning_type, msgListObj[i].id);
            row.attr("id",msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>");
            row.find("td:eq(1)").text(msgListObj[i].id);
            // row.find("td:eq(2)").text(task_cmd_map[msgListObj[i].cmd]);
            row.find("td:eq(2)").text(msgListObj[i].version);
            row.find("td:eq(3)").html(msgListObj[i].user);
            row.find("td:eq(4)").text(task_cmd_map[msgListObj[i].cmd]);
            row.find("td:eq(5)").html(msgListObj[i].device_id);
            row.find("td:eq(6)").html(msgListObj[i].generate_time);
            var final_time = getfinaltime(msgListObj[i].release_time,msgListObj[i].is_valid)
            row.find("td:eq(7)").html(final_time);
            row.find("td:eq(8)").html(msgListObj[i].num); 
            row.find("td:eq(9)").html(isSuccessFormat(msgListObj[i].is_valid));
            /*row.find("td:eq(8)").html(formatterReSend(msgListObj[i]));
            row.find("td:eq(9)").html(formatterIgnore(msgListObj[i]));*/
            row.find("td:eq(10)").html(formatterOperate(msgListObj[i]));
            row.find("td:eq(11)").html(msgListObj[i].config);
//            row.find("td:eq(11)").html(JSON.stringify(JSON.parse(msgListObj[i].config)));


            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }

    function formatterOperate(msgListObj){
        var dom = "";
        if(msgListObj.is_valid == 1 || msgListObj.is_valid == 3 || msgListObj.is_valid == 4 ){
            dom = "<a onclick='resendJob(\""+msgListObj.id+"\")'><i class='fa fa-share-square-o'></i>重发</a>";
            dom += "| <a onclick='ignoreJob(\""+msgListObj.id+"\")'><i class='fa fa-undo'></i>忽略</a>";
        }
        return dom;
    }

    function formatterReSend(msgListObj){
        var dom = ""
        if(msgListObj.is_valid == 3 || msgListObj.is_valid == 4 ){
            dom = "<a onclick='resendJob(\""+msgListObj.id+"\")'>失败重发</a>";
        }
        return dom;
    }
    function formatterIgnore(msgListObj){
        var dom = ""
        if(msgListObj.is_valid == 4 || msgListObj.is_valid == 4 ){
            dom = "<a onclick='ignoreJob(\""+msgListObj.id+"\")'>失败忽略</a>";
        }
        return dom;
    }
    // 任务重发
    function resendJob(id){
        var r = confirm('确认重新发送本次任务吗?');
        if(!r)
            return;
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin.send_again",
            type: "post",
            data: {id: id},
            success:function(data) {
                console.log(data)
                refresh();
            }
        })
    }
    // 失败忽略
    function ignoreJob(id){
        var r = confirm('确认忽略本次失败或错误的任务吗?');
        if(!r)
            return;
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin.update_task_plug",
            type: "post",
            data: {id: id},
            success:function(data) {
                console.log(data)
                refresh();
            }
        })
    }

    function LoadPage(currentPage,searchParam, is_director){
        is_director = is_director || 0;
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin.count&is_director=" + is_director,
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
                pagination(ret,"/ajax_action_detector.php?uu=plugin.show&p_size="+p_size + "&is_director=" + is_director,parseInt(currentPage),searchParam)
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
        // var task_id =  $("#task_id").val();
        var task_cmd = $("#task_cmd").attr("value").toString()
        var is_valid = $("#is_valid").attr("value").toString()
        var time_min = $("#time_min").val()
        var time_max =$("#time_max").val()
        
        globalSearchParam = {random:1}


        if(task_cmd!=""){
            globalSearchParam["cmd"] = task_cmd
        }
        if(is_valid!="-1"){
            globalSearchParam["is_valid"] = is_valid
        }
        if(time_min!=""){
            globalSearchParam["time_min"] = time_min
        }
        if(time_max!=""){
            globalSearchParam["time_max"] = time_max
        }
        LoadPage(1,globalSearchParam)

    })

    $("#clearButton").click(function(){
        firstSelect("task_module");
        firstSelect("task_cmd");
        firstSelect("is_valid");
        $("#user").val("");
        $("#policy_version").val("");
        $("#time_min").val("");
        $("#time_max").val("");
    })
</script>
</body>
</html>