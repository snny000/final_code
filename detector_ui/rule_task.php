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

    <title>策略任务</title>

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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;策略任务
                    <div class="btn-group" data-toggle="buttons">
                        <button type="button" href='rule_task.php' class="btn btn-default btn-primary">管理中心本地</button>
                        <button type="button" href='rule_task_director.php' class="btn btn-default">指挥节点下发</button>
                    </div>
                </h4>
            </div>

        </div>

        <div class="row btn-banner">
                <input id="task_id" type="text" class="form-control search-input" placeholder="任务编号(模糊搜索)">
                <input id="user" type="text" class="form-control search-input btn-interval" placeholder="操作用户名(模糊搜索)">
                <input id="policy_version" type="text" class="form-control search-input btn-interval" placeholder="策略版本号(模糊搜索)">
                <input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器编号(精确搜索)">

            <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="task_module" class="pull-left" value="0">所有策略种类</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="0">所有策略种类</li>
                    <li onclick="selectProtoFwd(this);" value="1">木马攻击检测策略</li>
                    <li onclick="selectProtoFwd(this);" value="2">漏洞利用检测策略</li>
                    <li onclick="selectProtoFwd(this);" value="3">恶意程序检测策略</li>
                    <li onclick="selectProtoFwd(this);" value="4">未知攻击窃密检测上报</li>
                    <li onclick="selectProtoFwd(this);" value="5">关键字检测策略</li>
                    <li onclick="selectProtoFwd(this);" value="6">加密文件筛选策略</li>
                    <li onclick="selectProtoFwd(this);" value="7">压缩文件检测策略</li>
                    <li onclick="selectProtoFwd(this);" value="8">图片筛选回传策略</li>
                    <li onclick="selectProtoFwd(this);" value="9">IP审计策略</li>
                    <li onclick="selectProtoFwd(this);" value="10">域名审计策略</li>
                    <li onclick="selectProtoFwd(this);" value="11">URL审计策略</li>
                    <li onclick="selectProtoFwd(this);" value="12">账号审计检测策略</li>
                    <li onclick="selectProtoFwd(this);" value="13">通联关系上报策略</li>
                    <li onclick="selectProtoFwd(this);" value="14">应用行为上报策略</li>
                    <li onclick="selectProtoFwd(this);" value="15">应用行为web过滤策略</li>
                    <li onclick="selectProtoFwd(this);" value="16">应用行为DNS过滤策略</li>
                    <li onclick="selectProtoFwd(this);" value="17">IP白名单过滤策略</li>
                    <li onclick="selectProtoFwd(this);" value="18">通信阻断策略</li>

                </ul>
            </div>

            <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="task_cmd" class="pull-left" value="0">所有任务操作</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="0">所有任务操作</li>
                    <li onclick="selectProtoFwd(this);" value="1">增加</li>
                    <li onclick="selectProtoFwd(this);" value="2">删除</li>
                    <li onclick="selectProtoFwd(this);" value="3">全量</li>
                </ul>
            </div>
        </div>
        <div class="row btn-banner">
            <div class="input-group date form_datetime date_div" style="width: 160px">
                <input id="time_min" class="form-control" size="16" type="text" value="" readonly placeholder="开始时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>

            <div class="input-group date form_datetime date_div btn-interval2" style="width: 160px">
                <input id="time_max" class="form-control" size="16" type="text" value="" readonly placeholder="截止时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
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
                </ul>
            </div>

            <button id="searchButton" type="button" class="btn btn-primary btn-interval2"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>

        </div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="4%">任务编号</th>
                    <th width="5%">操作用户名</th>
                    <th width="5%">策略种类</th>
                    <th width="4%">任务操作</th>                   
                    <th width="6%">下发检测器</th>
                    <th width="7%">策略版本号</th>
                    <th width="7%">任务包含规则数量</th> 
                    <th width="7%">任务下发时间</th> 
                    <th width="7%">任务完成时间</th> 
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

                            <!--  <nav id="paginationbox">
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
    buildFrame("menu-rule1");
//    $(function(){
        var globalSearchParam = {random:1}
        //第一次加载分页
        LoadPage(1,globalSearchParam)
//    })


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
                        $("<tr><td colspan=" + col_size + " style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
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


    function formatterOperate(msgListObj){
        var dom = "";
        if(msgListObj.is_valid == 1 || msgListObj.is_valid == 3 || msgListObj.is_valid == 4 ){
            dom = "<a onclick='resendJob(\""+msgListObj.task_id+"\")'><i class='fa fa-share-square-o'></i>重发</a>";
            dom += "| <a onclick='ignoreJob(\""+msgListObj.task_id+"\")'><i class='fa fa-undo'></i>忽略</a>";
        }
        return dom;
    }

    function formatterReSend(msgListObj){
        var dom = ""
        if(msgListObj.is_valid == 3 || msgListObj.is_valid == 4 ){
            dom = "<a onclick='resendJob(\""+msgListObj.task_id+"\")'>失败重发</a>";
        }
        return dom;
    }
    function formatterIgnore(msgListObj){
        var dom = ""
        if(msgListObj.is_valid == 4 || msgListObj.is_valid == 4 ){
            dom = "<a onclick='ignoreJob(\""+msgListObj.task_id+"\")'>失败忽略</a>";
        }
        return dom;
    }

    // 任务重发
    function resendJob(id){
        var r = confirm('确认重新发送本次任务吗?');
        if(!r)
            return;
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule_task.send_again",
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
            url: "/ajax_action_detector.php?uu=rule_task.ignore_task",
            type: "post",
            data: {id: id},
            success:function(data) {
                console.log(data)
                refresh();
            }
        })
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
        var task_module_map={1:'木马攻击检测策略',2:'漏洞利用检测策略',3:'恶意程序检测策略',4:'未知攻击窃密检测上报策略',5:'关键字检测策略',6:'加密文件筛选策略',7:'压缩文件检测策略',
        8:'图片文件筛选策略',9:'IP审计策略',10:'域名审计策略',11:'URL审计策略',12:'账号审计检测策略',13:'通联关系上报策略',14:'应用行为上报策略',15:'应用行为web过滤策略',
            16:'应用行为DNS过滤策略',17:'IP白名单过滤策略',18:'通信阻断策略'}
        var task_cmd_map = {1:'增加',2:'删除',3:'全量'}
		
		// var is_success_map = {0:'已忽略',1:'任务执行中',2:'任务执行成功',3:'任务执行失败',4:'任务错误'};
        
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
            "<td style='color:#999999'></td>" +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();

            var is_valids = isSuccessFormat(msgListObj[i].is_valid)


           // var operatehtml = getStrManipulation(msgListObj[i].warning_type, msgListObj[i].id);
            row.attr("id",msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>");
            row.find("td:eq(1)").text(msgListObj[i].task_id);
            row.find("td:eq(2)").text(msgListObj[i].user);
            row.find("td:eq(3)").html(task_module_map[msgListObj[i].task_module]);
            row.find("td:eq(4)").text(task_cmd_map[msgListObj[i].task_cmd]);
            row.find("td:eq(5)").html(msgListObj[i].device_id);
            var final_time = getfinaltime(msgListObj[i].task_release_time,msgListObj[i].is_valid)
            row.find("td:eq(6)").html(msgListObj[i].policy_version);
            row.find("td:eq(7)").html(msgListObj[i].task_num);
            row.find("td:eq(8)").html(msgListObj[i].task_generate_time);
            row.find("td:eq(9)").html(final_time);
            row.find("td:eq(10)").html(is_valids);
            row.find("td:eq(11)").html(formatterOperate(msgListObj[i]));
            row.find("td:eq(12)").text(msgListObj[i].config);
            // row.find("td:eq(10)").html(HTMLEncode(msgListObj[i].config));

            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }

    function LoadPage(currentPage,searchParam, is_director){
        s_director = is_director || 0;
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule_task.count&is_director=" + is_director,
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
                pagination(ret,"/ajax_action_detector.php?uu=rule_task.show&p_size="+p_size + "&is_director=" + is_director,parseInt(currentPage),searchParam)
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
        var task_id =  $("#task_id").val();
        var user =  $("#user").val();
        var policy_version =  $("#policy_version").val();
        var device_id =  $("#device_id").val();
        var task_module = $("#task_module").attr("value").toString()
        var task_cmd = $("#task_cmd").attr("value").toString()
        var is_valid = $("#is_valid").attr("value").toString()
        var time_min = $("#time_min").val()
        var time_max =$("#time_max").val()

        globalSearchParam = {random:1}

        if(user!=""){
            globalSearchParam["user"] = user
        }

        if(task_module!="0"){
            globalSearchParam["task_module"] = task_module
        }
        if(task_cmd!="0"){
            globalSearchParam["task_cmd"] = task_cmd
        }
        if(is_valid!="-1"){
            globalSearchParam["is_valid"] = is_valid
        }
        if(task_id!=""){
            globalSearchParam["task_id"] = task_id
        }
        if(policy_version!=""){
            globalSearchParam["policy_version"] = policy_version
        }
        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
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
        $("#task_id").val("");
        $("#user").val("");
        $("#policy_version").val("");
        $("#device_id").val("");
        $("#time_min").val("");
        $("#time_max").val("");
    })

</script>

</body>
</html>