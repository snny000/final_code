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

    <title>任务组管理</title>

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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;任务组管理</h4>
            </div>
            <div class="upper-btn-group margin_ddos1 pull-right">
                <button id="addButton" type="button" class="btn btn-interval btn-primary" data-toggle="modal" data-target="#addModal"><i class="fa fa-plus">&nbsp;&nbsp;</i>添加</button>
                <!--<button id="full" type="button" class="btn btn-primary btn-interval"><i class="fa fa-hourglass">&nbsp;&nbsp;</i>全量&nbsp;<span hidden="">2</span></button>
                <button id="increment" type="button" class="btn btn-primary btn-interval" disabled=""><i class="fa fa-hourglass-half">&nbsp;&nbsp;</i>增量&nbsp;<span class="badge" style="background-color:orange"></span></button>-->
            </div>
        </div>

        <div class="row btn-banner">
                <input id="group_id" type="text" class="form-control search-input" placeholder="任务组编号(模糊搜索)">
                <input id="user" type="text" class="form-control search-input btn-interval" placeholder="创建者(模糊搜索)">
                <input id="task_name" type="text" class="form-control search-input btn-interval" placeholder="任务组名称(模糊搜索)">
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

            <div class="dropdown btn-interval2 dropdown-inline">
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
                    <li onclick="selectProtoFwd(this);" value="4">未知攻击检测策略</li>
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

            <button id="searchButton" type="button" class="btn btn-primary btn-interval2"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>

        </div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="10%">任务组编号</th>
                    <th width="10%">任务组名称</th>
                    <th width="20%">策略种类</th>
                    <th width="10%">创建者</th>
                    <th width="10%">创建时间</th>
                    <th width="20%">备注</th>
                    <th width="30%">操作</th>
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
                    <td colspan="11">
                        <div class="pull-left">
                            <button class="btn btn-default btn-sm" id="delete">删除</button>
                            <!--<button class="btn btn-default btn-sm" id="rewrite_label">批量修改任务组</button>-->
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

<!-- 模态框（Modal） -->
<div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    添加任务组
                </h4>
            </div>
            <div class="modal-body">


                <div class="dropdown-inline">
                    <span> 策略种类:</span>
                    <div class="dropdown">
                        <button type="button" data-toggle="dropdown"
                                class="btn dropdown-btn dropdown-menu-width"
                                aria-haspopup="true"
                                aria-expanded="false">
							<span id="task_type_select" value="-1">未选择</span>
                            <i class="fa fa-sort-down pull-right"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
						    <li onclick="selectProtoFwd(this);" value="-1">未选择</li>
                            <li onclick="selectProtoFwd(this);" value="1">木马攻击检测策略</li>
                            <li onclick="selectProtoFwd(this);" value="2">漏洞利用检测策略</li>
                            <li onclick="selectProtoFwd(this);" value="3">恶意程序检测策略</li>
                            <li onclick="selectProtoFwd(this);" value="4">未知攻击检测策略</li>
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
					<div style="color:red"></div>
                </div>
				
                <div>
                    <!--<span>任务组编号（数值型必填）:</span> <input id="task_id_input" type="number" maxlength="128" class="form-control";>
                    <div style="color:red"></div>-->
                    <span>任务组名称（必填）:</span> <input id="task_name_input"  maxlength="128" class="form-control";>
                    <div style="color:red"></div>
                    <span>创建者（必填）:</span> <input id="create_person_input" maxlength="128" class="form-control";>
                    <div style="color:red"></div>
                    <span>备注：</span> <input id="add_label"  class="form-control";>
                    <div style="color:red"></div>
                </div>
            </div>
            <div class="modal-footer">
                <button id="add-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<!-- 模态框（Modal） -->
<div class="modal fade" id="modifyModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    修改任务组
                </h4>
            </div>
            <div class="modal-body">
                <div>
                    <div style="color:red"></div>
                    <span>任务组名称（必填）:</span> <input id="task_name_modify"  maxlength="128" class="form-control";>
                    <div style="color:red"></div>
                    <!--<span>创建者（必填）:</span> <input id="create_person_modify" maxlength="128" class="form-control";>
                    <div style="color:red"></div>-->
                    <span>备注：</span> <input id="add_label_modify"  class="form-control";>
                    <div style="color:red"></div>
                </div>
            </div>
            <div class="modal-footer">
                <button id="modify-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
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


            <!-- class="modal-footer"-->
            <div class="modal-footer">
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>


<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script>
    buildFrame("menu-rule9");
    var globalSearchParam = {random:1};
    // 定义查看策略和添加策略的url链接，用于跳转不同的页面处理
    var ruleType = {
        1:['木马攻击检测策略','rule_trojan.php'],
        2:['漏洞利用检测策略','rule_attack.php'],
        3:['恶意程序检测策略','rule_pefile.php'],
        4:['未知攻击检测策略','rule_abnormal.php'],
        5:['关键字检测策略','rule_keyword_file.php'],
        6:['加密文件筛选策略','rule_encryption_file.php'],
        7:['压缩文件检测策略','rule_compress_file.php'],
        8:['图片文件筛选策略','rule_picture_file.php'],
        9:['IP审计策略','rule_ip_listen.php'],
        10:['域名审计策略','rule_domain_listen.php'],
        11:['URL审计策略','rule_url_listen.php'],
        12:['账号审计检测策略','rule_account_listen.php'],
        13:['通联关系上报策略','rule_net_log.php'],
        14:['应用行为上报策略','rule_app_behavior.php'],
        15:['应用行为web过滤策略','rule_web_filter.php'],
        16:['应用行为DNS过滤策略','rule_dns_filter.php'],
        17:['IP白名单过滤策略','rule_ip_whitelist.php'],
        18:['通信阻断策略','rule_comm_block.php']
        }
    $(function(){
        //第一次加载分页
        LoadPage(1,globalSearchParam)
    })


    $('.form_datetime').datetimepicker({
        language:  'zh-CN',
        minView: "month",
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayBtn: true
    });

    function selectProtoFwd(obj) {
        $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
        $(obj).parent().parent().find("span:first").text($(obj).text());
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
                        $("<tr><td colspan='11' style='text-align: center'><h4>没有记录</h4></td></tr>").appendTo("#maintable tbody");
                    }else if (ret["code"] == 9001){
                        window.location.href = "login.php?ref="+window.location.href;
                    }else{
                        // console.log(ret["msg"])
                        alert(ret["msg"]);
                    }
                },
                beforeSend: function () {
                    $("#maintable tbody tr").remove();
                    $("#maintable tbody").append("<tr><td colspan='11'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
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
        $('#pagination').twbsPagination(option);
    }

    function List(msgListObj){
        var task_module_map={
            1:'木马攻击检测策略',
            2:'漏洞利用检测策略',
            3:'恶意程序检测策略',
            4:'未知攻击检测策略',
            5:'关键字检测策略',
            6:'加密文件筛选策略',
            7:'压缩文件检测策略',
            8:'图片文件筛选策略',
            9:'IP审计策略',
            10:'域名审计策略',
            11:'URL审计策略',
            12:'账号审计检测策略',
            13:'通联关系上报策略',
            14:'应用行为上报策略',
            15:'应用行为web过滤策略',
            16:'应用行为DNS过滤策略',
            17:'IP白名单过滤策略',
            18:'通信阻断策略'}
        var task_cmd_map = {1:'增加',2:'删除',3:'全量'}
		
		var is_success_map = {'true':'已完成','false':'未完成','not_get':'未下发'}

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
            "</tr>");
        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();
            var operatehtml = getStrManipulation(msgListObj[i]);
            row.attr("id",msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>");
            row.find("td:eq(1)").text(msgListObj[i].group_id);
            row.find("td:eq(2)").text(msgListObj[i].name);
            row.find("td:eq(3)").html(task_module_map[msgListObj[i].rule_type]);
            row.find("td:eq(4)").text(msgListObj[i].create_person);
            row.find("td:eq(5)").html(msgListObj[i].create_time.replace('T',' '));
            row.find("td:eq(6)").html(msgListObj[i].remarks);
            row.find("td:eq(7)").html(operatehtml);
            row.show();
            row.appendTo("#maintable tbody");

            getRuleCount(msgListObj[i],row);
        }
        rebindChkAll();
    }
    // 异步获取任务组对应策略条数
    function getRuleCount(msgListObj,row){
        $.ajax({
                url:'ajax_action_detector.php?uu=task_group.policy_count&policy_type='+msgListObj.rule_type,
                type: "post",
                async:true,
                data: {group_id:msgListObj.group_id},
                success:function(data) {
                    var ruleCount = JSON.parse(data)['msg']['count'];
                    if(ruleCount !=0){
                        var setShowTag = "<a href=\"javascript:void(0);\" class=\"fa fa-bars\" data-bind="+ JSON.stringify(msgListObj) +" onclick=\"showRule(this)\">查看策略(共"+ruleCount+"条)</a>"
                        $(row.find("td:eq(7)")).find('span').replaceWith(setShowTag);
                    }
                }
            })
    }

    function getStrManipulation(msgListObj) {
        var showtag = "<span class=\"fa fa-exclamation\">没有策略</span>";
        /*if(msgListObj.rule_id_list){
            var rule_id_list = msgListObj.rule_id_list.replace(/#/g,'&'); //#报错
            var ruleCount = rule_id_list.split("&").length;
            showtag = showtag = "<a href=\"javascript:void(0);\" class=\"fa fa-bars\" data-bind="+ JSON.stringify(msgListObj) +" onclick=\"showRule(this)\">查看策略(共"+ruleCount+"条)</a>"
        }*/
        return showtag + "<label>|</label>"+"<a href=\"javascript:void(0);\"class=\"fa fa-refresh\" data-bind="+ JSON.stringify(msgListObj) +" onclick=\"modifyGroup(this)\" data-toggle=\"modal\" data-target=\"#modifyModal\">修改任务组</a>"
    }

    function showRule(that){
        var msgListObj = JSON.parse($(that).attr('data-bind'))
        var param = {
            id: msgListObj.id,
            rule_id_list: msgListObj.rule_id_list,
            addIntoGroup: JSON.stringify({
                state:false,
                group_id: msgListObj.group_id,
                group_name: msgListObj.name,
                rule_type: msgListObj.rule_type
            })
        };
        post_blank(ruleType[msgListObj.rule_type][1],param);
    }
    var modifyParam = {};
    // 修改任务组
    function modifyGroup(that){
        var msgListObj = JSON.parse($(that).attr('data-bind'))
        $('#task_name_modify').val(msgListObj.name);
        //$('#create_person_modify').val(msgListObj.create_person);
        $('#add_label_modify').val(msgListObj.remarks);
        console.log(msgListObj)
        modifyParam = {
            "id":msgListObj.id,           
            "rule_type":msgListObj.rule_type,
            /*"task_id": msgListObj.task_id*/
        }
    }

    $('#modify-submit').on('click',function(){
            modifyParam.name = $("#task_name_modify").val();
            //modifyParam.create_person = $("#create_person_modify").val();
            modifyParam.remarks = $("#add_label_modify").val();
            var ischeck = true; 
			if(modifyParam.name == ""){
			    $("#task_name_modify").next("div").html("请输入任务组名称")
				ischeck = false
			}else{
				$("#task_name_modify").next("div").html("")
			}
/*            if(modifyParam.create_person == ""){
                $("#create_person_modify").next("div").html("请输入创建者")
                ischeck = false
            }else{
                $("#create_person_modify").next("div").html("")
            }*/
            if(!ischeck){
                return;
            }
            $.ajax({
                url: "/ajax_action_detector.php?uu=task_group.batch_update",
                type: "post",
                data: {id:"["+modifyParam.id+"]",name:modifyParam.name,remarks:modifyParam.remarks},
                success:function(data) {
                    refresh();
                }
            })
            $("#modifyModal").modal('hide');
        })

    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=task_group.count",
            type: "post",
            data: searchParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 200)
                    ret = ret['msg']['count'];
                else {
                    ret = 0;
                }
                $("#totalcount").text(ret);
                $('#pagination').empty();
                $('#pagination').removeData("twbs-pagination");
                $('#pagination').unbind("page");
                pagination(ret,"/ajax_action_detector.php?uu=task_group.show&p_size="+p_size,parseInt(currentPage),searchParam)
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
        var group_id =  $("#group_id").val();
        var user =  $("#user").val();
        var task_name =  $("#task_name").val();
        var task_module = $("#task_module").attr("value").toString()
        var time_min = $("#time_min").val()
        var time_max =$("#time_max").val()

        globalSearchParam = {random:1}

        if(user!=""){
            globalSearchParam["create_person"] = user
        }

        if(task_module!="0"){
            globalSearchParam["rule_type"] = task_module
        }
        if(group_id!=""){
            globalSearchParam["group_id"] = group_id
        }
        if(task_name!=""){
            globalSearchParam["name"] = task_name
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
        $("#group_id").val("");
        $("#user").val("");
        $("#task_name").val("");
        $("#time_min").val("");
        $("#time_max").val("");
        //$("#searchButton").click();
    })

    $("#add-submit").click(function(){
        var param = {
            "id":0,
            "rule_type":parseInt($("#task_type_select").attr("value")),
            //"group_id": parseInt($("#group_id").val()),
            "name": $("#task_name_input").val(),
            "create_person": $("#create_person_input").val(),
            "remarks": $("#add_label").val(),
        };
        var ischeck = true; 
			if(param.rule_type == -1){
				$("#task_type_select").parent().parent().next("div").html("请选择策略类型")
				ischeck = false
			}else{
				$("#task_type_select").parent().parent().next("div").html("")
			}
/*			if(param.group_id == ""){
				$("#task_id_input").next("div").html("请输入任务组编号")
				ischeck = false
			}else{
				$("#task_id_input").next("div").html("")
			}*/
			if(param.name == ""){
			    $("#task_name_input").next("div").html("请输入任务组名称")
				ischeck = false
			}else{
				$("#task_name_input").next("div").html("")
			}
            if(param.create_person == ""){
                $("#create_person_input").next("div").html("请输入创建者")
            }else{
                $("#create_person_input").next("div").html("")
            }

            if(!ischeck){
                return;
            }
            console.log(param)
            $.ajax({
                url: "/ajax_action_detector.php?uu=task_group.add_update",
                type: "post",
                data: {json:JSON.stringify(param)},
                success:function(data) {
                    refresh();
                    firstSelect("task_type_select");
                    $.each($('#addModal input'),function(i,v){
                        $(v).val('');
                    })
                }
            })
            $("#addModal").modal('hide');
        }
    )

    // 批量修改任务组
    $("#rewrite_label").click(function(){
        $('#hintModal').find(".modal-title").html("批量修改任务组")
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        if(checkboxs.size() == 0){
            alert("请选择需要修改的数据");
            return;
        }
        var modifyContent = `
        <p >将修改<span style='color: red;font-size: large'>${checkboxs.size()}</span>条数据，请确认</p>
        <div id="new_label_div" style="text-align: center;">
            <span>任务组名称：</span> <input id="new_name" type="text" class="form-control" style="width: 250px !important;display: inline-block !important;">
                <div style="color:red"></div>
            <span>任务组备注：</span> <input id="new_remarks" type="text" class="form-control" style="width: 250px !important;display: inline-block !important;">
        </div>`
        $('#hintModal').find(".modal-body").html(modifyContent)

        var footer = "<button id='rewriteSubmit' type='button' class='btn btn-primary'>确定</button>"+
            "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
        $('#hintModal').find(".modal-footer").html(footer)

        $("#rewriteSubmit").click(function(){
            var carray =new Array()
            var lines = $("#maintable tbody tr");
            var checkboxs = lines.find("input:eq(0):checkbox:checked");
            checkboxs.each(function(){
                carray.push(parseInt($(this).parent().parent().attr('id')))
            });
            var newname = $('#new_name').val();
            var newremark = $('#new_remarks').val();
            var ischeck = true
            if(newname == ""){
			    $("#new_name").next("div").html("请输入任务组名称")
				ischeck = false
			}else{
				$("#task_name_input").next("div").html("")
			}
            if(!ischeck)
                return;
            console.log("carray:"+carray)
            $.ajax({
                url: "/ajax_action_detector.php?uu=task_group.batch_update",
                type: "post",
                data: {id:JSON.stringify(carray),name:newname,remarks:newremark},
                success:function(data) {
                    refresh();
                }
            })
            $('#hintModal').modal('hide')
        })
        $('#hintModal').modal('show')
    })

    $("#delete").click(function(){
        $('#hintModal').find(".modal-title").html("删除提示框")
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        if(checkboxs.size() == 0){
            alert("请选择删除数据");
            return;
        }
        for(var i=0;i<checkboxs.length;i++){
            if($($(checkboxs[i]).parent().parent().find('td:last')).find('a').length == 2){
                alert("任务组中包含策略，请先移除相关策略！");
                return ;
            }
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
                carray.push(parseInt($(this).parent().parent().attr('id')))
            })
            console.log("carray:"+carray)
            $.ajax({
                url: "/ajax_action_detector.php?uu=task_group.delete",
                type: "post",
                data: {id:JSON.stringify(carray)},
                success:function(data) {
                    console.log(data)
                    refresh()
                }
            })
            $('#hintModal').modal('hide')
        })
        $('#hintModal').modal('show')
    })

    $("#full").click(function(){
        $('#hintModal').find(".modal-title").html("全量下发提示框")
        var content =
            "<span>下发方式:<span style='color: red;font-size: large'>全量下发</span></span>"+
            "<p >下发任务组个数:<span style='color: red;font-size: large'>"+$("#full span").text()+"</span></p>"+
            "<p >下发规则个数:<span style='color: red;font-size: large'>"+$("#full span").text()+"</span></p>"
        $('#hintModal').find(".modal-body").html(content)

        var footer = "<button id='fullSubmit' type='button' class='btn btn-primary'>确定</button>"+
            "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
        $('#hintModal').find(".modal-footer").html(footer)

        $("#fullSubmit").click(function(){
            var carray =new Array()
            pickDetectorForward(carray,[],4)
            $('#hintModal').modal('hide')
        })
        $('#hintModal').modal('show')
    })


$("#increment").click(function(){
    $('#hintModal').find(".modal-title").html("增量下发提示框")

    var content =
        "<span>下发方式:<span style='color: red;font-size: large'>增量下发</span></span>"+
        "<p >下发任务组个数:<span style='color: red;font-size: large'>"+$("#full span").text()+"</span></p>"+
        "<p >下发规则个数:<span style='color: red;font-size: large'>"+$("#increment span").text()+"</span></p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='incrementSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#incrementSubmit").click(function(){
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.sync&policy_type="+global_policy_type+"&type=0",
            type: "post",
            data:null,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert("增量下发成功");
                }else{
                    alert("增量下发失败");
                }
                refresh()
            }
        })
        //  $(this).prop('disabled',"true");

        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})

</script>

</body>
</html>