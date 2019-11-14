<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
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

    <title>账号管理</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

    <!-- Add custom CSS here -->
    <link href="css/frame.css" rel="stylesheet">
    <link href="css/product.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <link href="css/detector.css" rel="stylesheet">
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

        #addModal .bootstrap-select.node-id-select,#changeModal .bootstrap-select.node-id-select{
            width: 100% !important;
        }


    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;账号管理</h4>
            </div>
            <div class="upper-btn-group margin_ddos1 pull-right">
                <button resourceid="282" id="addButton" type="button" class="btn btn-interval btn-primary" data-toggle="modal" data-target="#addModal"><i class="fa fa-plus">&nbsp;&nbsp;</i>添加</button>
            </div>
        </div>
        <div class="row btn-banner upper-line"></div>
        <div class="row btn-banner">

            <input id="loginid" type="text" class="form-control search-input" placeholder="用户名（模糊搜索）">
            <select id="select_level" class="selectpicker node-id-select" data-live-search="true" title="请选择角色" style="{width:100px;}">
            </select>
            
           <!--  <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="level" class="pull-left" value="-1">所有权限类型</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="-1">所有权限类型</li>
                    <li onclick="selectProtoFwd(this);" value="1">系统管理员</li>
                    <li onclick="selectProtoFwd(this);" value="2">安全保密管理员</li>
                    <li onclick="selectProtoFwd(this);" value="3">策略配置人员</li>
                    <li onclick="selectProtoFwd(this);" value="4">传输涉密配置人员</li>
                    <li onclick="selectProtoFwd(this);" value="5">策略审计人员</li>
                    <li onclick="selectProtoFwd(this);" value="6">普通运维用户</li>
					
                </ul> 
            </div>-->

            <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button resourceid="282" id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>
		</div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="20%">用户名</th>
                    <th width="20%">角色</th>
                    <th width="20%">操作</th>
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
                    <td colspan="3">
                        <div class="pull-left">
                            <button resourceid="282" class="btn btn-default btn-sm" id="delete">删除</button>
                          <!--  <button class="btn btn-default btn-sm" id="clean">批量重置密码</button>-->
                            <button resourceid="399" class="btn btn-default btn-sm" id="change">修改权限</button>
                            <button resourceid="403" class="btn btn-default btn-sm" id="clean">重置密码</button>
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
<!-- 模态框（Modal） -->
<div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    添加用户
                </h4>
            </div>
           <div class="modal-body">
                <span>用户名：</span> <input id="add_loginid"  class="form-control">
                <div style="color:red"></div>
                
            </div>
            <div class="modal-footer">
                <button id="add-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="changeModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    修改用户
                </h4>
            </div>
            <div class="modal-body">
                <span>用户名：</span> <input id="change_loginid"  class="form-control" disabled="disabled";>
                <div style="color:red"></div>
                <span>用户角色：</span>
                <select id="change_level" class="selectpicker node-id-select" data-live-search="true" title="请选择角色" multiple=true>
                </select>
            </div>
            <div class="modal-footer">
                <button id="change-submit" type="button" class="btn btn-primary">提交</button>
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
            <div id="new_label_div" style="display: none;text-align: center;">
                <span>新备注标签1：</span> <input id="new_label" type="text" class="form-control" style="width: 250px !important;display: inline-block !important;">
                <div style="color:red"></div>
            </div>


            <!--       class="modal-footer"-->

            <div class="modal-footer">
                <button id="delSubmit" type="button" class="btn btn-primary">确定</button>

                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>

                <!--  <button id="cancelSubmit" type="button" class="btn btn-primary">关闭</button>-->


                <!-- data-dismiss="modal"-->
                <!-- <button id="cancelSubmit1" type="button" class="btn btn-default">关闭</button>-->


            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

</div>

<!-- /#wrapper -->

<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<link href="css/bootstrap-select.css" rel="stylesheet">
<script type="text/javascript" src="js/bootstrap-select.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script>
    buildFrame("menu-account");
    // if(localStorage.level==0){



    // }else if(localStorage.level==1){
    //      //$("#change").hide()
    //      $("#change").attr("disabled", true);
    //      setSelect('add_level',6)
    //      $("#add_level").parent().attr("disabled", true);
    //      $("#addButton").attr("disabled", true);

    //  }else if(localStorage.level==2){
    //      $("#delete").attr("disabled", true);
    //      $("#addButton").attr("disabled", true);
    //  }else{
    //      $("#change").attr("disabled", true);
    //      $("#delete").attr("disabled", true);
    //      $("#addButton").attr("disabled", true);
    //  }
    //  
     function selectProtoFwd(obj) {
        $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
        $(obj).parent().parent().find("span:first").text($(obj).text());
    }

    $('button.condition-btn.singlechoose').click(function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
    })


    // function selectProtoFwd(obj) {
    //     $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
    //     $(obj).parent().parent().find("span:first").text($(obj).text());
    //     //$("#"+id).attr("value",$(obj).attr("value"));
    //     // $("#"+id).text($(obj).text());
    // }

    // $('button.condition-btn.singlechoose').click(function () {
    //     $(this).siblings().removeClass("active");
    //     $(this).addClass("active");
    // })

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

                        List(ret["msg"]["user_query"]);
                    } else if (ret["code"] == 20000) {
                        $("#maintable tbody tr").remove();
                        $("<tr><td colspan='3' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
                    }else if (ret["code"] == 9001){
                        window.location.href = "login.php?ref="+window.location.href;
                    }else{
                        alert(ret["msg"]);
                    }
                },
                beforeSend: function () {
                    $("#maintable tbody tr").remove();
                    $("#maintable tbody").append("<tr><td colspan='3'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
                },
                error: function () {
                    alert("无法连接服务器");
                }
            });

        }
    }



    // 角色下拉列表初始化
    $.ajax({
            url: 'ajax_action_detector.php?uu=login.get_role_number',
            success: function (res) {
                var ret = JSON.parse(res);
                if(ret.code == 200){
                    var rolecount = ret['msg']['role_count'];
                    $.ajax({
                        url: 'ajax_action_detector.php?uu=login.role_query_all&p_size='+rolecount+'&pn=1',
                        success: function (res) {
                            var roleData = JSON.parse(res).msg.query_role;
                            roleData.map(function(v,i){
                                var li =  `<li onclick="selectProtoFwd(this);" value=${v.id}>${v.name}</li>`;
                                $('.roleList').append(li);
                                var option =  `<option value=${v.id}>${v.name}</option>`;
                                $('#add_level,#change_level,#select_level').append(option);
                                $('#add_level,#change_level,#select_level').selectpicker('refresh');
                            })
                        }
                    })
                }
            }
        })


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


/*    $("#chk_all1,#chk_all2").click(function(){
        if(this.checked){
            $("table :checkbox").prop("checked", true);
        }else{
            $("table :checkbox").prop("checked", false);
        }
    });*/



    $("#add-submit").click(function(){
        var param = {
            "username":$("#add_loginid").val(),
			"level": JSON.stringify($("#change_level").val()),

        };
        var ischeck = true
        var add_loginid = $("#add_loginid").val()
		var add_level = $("#add_level").attr("value")

        if(add_loginid == ""){
            $("#add_loginid").next("div").html("用户名不能为空")
            ischeck = false
        }else{
            $("#add_loginid").next("div").html("")
        }


        $("#addModal input").each(function(){
            var value = $(this).val(); //这里的value就是每一个input的value值~
            if(!value.match(/^[\u4E00-\u9FA5a-zA-Z0-9_]{0,}$/)){
                var label = $(this).prev("span").text()
                //error_str+=label+"存在非法字符\n";
                $(this).next("div").html("存在非法字符\n")
                ischeck = false
            }
        });

        if(!ischeck){
            return;
        }
        $.ajax({
            url: "/ajax_action_detector.php?uu=login.user_registration",
            type: "post",
            data: param,
            success:function(data) {
                var ret = JSON.parse(data);
                 if(ret["msg"] == "success"){
                     refresh();
                     $("#addModal").modal('hide');
                 }else{
                     alert(ret["msg"]);
                 }
//                 refresh();
            }
        });
        $("#addModal").modal('hide');

    }
    )

     $("#change-submit").click(function(){
            modifyParam["username"] = $("#change_loginid").val();
            modifyParam["role_id"] = JSON.stringify($("#change_level").val());
            // modifyParam["node_id"] = $('#change_node_id').val();
            var ischeck = true;
            var change_loginid = $("#change_loginid").val();
            var change_level = $("#change_level").val();
            if(change_loginid == ""){
                $("#change_loginid").next("div").html("用户名不能为空")
                ischeck = false
            }else{
                $("#change_loginid").next("div").html("")
            }
            if(change_level == null){
                alert('请选择角色！')
                ischeck = false
            }else{
                $("#change_level").next("div").html("")
            }
            /*if(change_level == -1){
                $("#change_level").parent().parent().next("div").html("请选择角色")
                ischeck = false
            }else{
                $("#change_level").parent().parent().next("div").html("")
            }*/

            $("#changeModal input").each(function(){
                var value = $(this).val(); //这里的value就是每一个input的value值~
                if(!value.match(/^[\u4E00-\u9FA5a-zA-Z0-9_]{0,}$/)){
                    var label = $(this).prev("span").text()
                    $(this).next("div").html("存在非法字符\n")
                    ischeck = false
                }
            });
            if(!ischeck){
                return;
            }
            $.ajax({
                url: "/ajax_action_detector.php?uu=login.change_user_info",
                type: "post",
                data: modifyParam,
                success:function(data) {
                    refresh();
                },
                error: function () {
                    alert("无法连接服务器");
                }
            })
            $("#changeModal").modal('hide');
        })
    
    /*
     var msgListObj = eval(msgList);
     List(msgListObj); //默认列表
     */

    function List(msgListObj){
        var levelMap = {1:'系统管理员',2:'安全保密管理员',3:'策略配置人员',4:'传输涉密配置人员',5:'策略审核人员',6:'普通运维人员'}

        $("#maintable tbody tr").remove();
        var _row = $("<tr>" +
            "<td></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();row.attr("id",msgListObj[i].id)
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' roleid="+msgListObj[i].role_id+" id="+msgListObj[i].id+ ">")
            row.find("td:eq(1)").text(msgListObj[i].username);
            var GetRole = getrolename(msgListObj[i].role_name)
            row.find("td:eq(2)").html(GetRole);
            // row.find("td:eq(2)").html(msgListObj[i].role_name.join(','));
            row.find("td:eq(3)").html(getStrManipulation(msgListObj[i]));
            row.show();
            row.appendTo("#maintable tbody");
        }

        rebindChkAll();
    }
    function getrolename(role_name){
        if(role_name){
            return role_name.join(',')
        }else{
            return role_name
        }
    }
     function getStrManipulation(msgListObj) {
        return `<a class="fa fa-gear" data-bind='${JSON.stringify(msgListObj)}' onclick="editUser(this)" data-toggle="modal"  data-target="#changeModal">修改</a>`
    }

     // 修改用户
    var modifyParam = {};
    function editUser(that){
        var oldObj = JSON.parse($(that).attr('data-bind'));
        $("#change_loginid").val(oldObj.username);
        //$("#change_level").attr('value',oldObj.role_id);
        //$("#change_level").text(oldObj.role_name);
        $('#change_level').selectpicker('val',oldObj.role_id);
        // $('#change_node_id').selectpicker('val',oldObj.node_id);
        modifyParam.user_id = oldObj.id;

    }

    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=login.get_user_number",
            type: "post",
            data: searchParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 200)
                    ret = ret["msg"]["user_count"]
                else {
                    ret = 0;
                }
                $("#totalcount").text(ret);
                $('#pagination').empty();
                $('#pagination').removeData("twbs-pagination");
                $('#pagination').unbind("page");
                pagination(ret,"/ajax_action_detector.php?uu=login.user_query_all&p_size="+p_size,parseInt(currentPage),searchParam)
            },
            beforeSend: function () {
                $(".loading-pic").removeClass("hidden");
            },
            error: function () {
                alert("无法连接服务器");
            }
        })

        /*
         <button id="full" type="button" class="btn btn-primary btn-interval">全量&nbsp;<span class="badge" style="background-color: orange">0</span></button>
         <button id="increment" type="button" class="btn btn-primary btn-interval">增量&nbsp;<span class="badge" style="background-color: orange">0</span></button>
         */


    }


    var globalSearchParam = {random:1}

    //第一次加载分页
    LoadPage(1,globalSearchParam)




/*        var first_text = module.find("li:first").text()
        var first_value = module.find("li:first").attr("value")*/




    $("#searchButton").click(function(){

        var loginid =  $("#loginid").val();
		var level = $("#select_level").val();

        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        globalSearchParam = {random:1}


        if(level!="-1"){
            globalSearchParam["role_id"] = level
        }
        if(loginid!=""){
            globalSearchParam["username"] = loginid
        }
        LoadPage(1,globalSearchParam)
    })


    $("#clearButton").click(function(){

        // firstSelect("select_level");
        $('#select_level').selectpicker('val','')
        $("#loginid").val("");

    })


    function alterSearchForm (){

        oneSelect("level");


        oneInput("loginid");



    }


   $("#delete").click(function(){
        //$('#new_label_div').hide()

        $('#hintModal').find(".modal-title").html("删除提示框")

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
            $.ajax({
                url: "/ajax_action_detector.php?uu=login.delete_user",
                type: "post",
                data: {user_id_list:JSON.stringify(carray)},
                success:function(data) {
                    //  var ret = JSON.parse(data);
                    var server = JSON.parse(data);
                    var msg = server.msg;
                    alert(msg);
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
	
	$('#clean').click(function(){
        $('#hintModal').find(".modal-title").html("重置密码提示框")
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        if(checkboxs.size() == 0){
            alert("请选择数据");
            return;
        }else if(checkboxs.size()>1){
            alert("一次只能操作一条数据");
            return;
        }

        var content = "<p>将重置<span style='color: red;font-size: large'>"+checkboxs.parent().next().text()+"</span>的密码，请确认</p>"
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
            $.ajax({
                url: "/ajax_action_detector.php?uu=login.reset_user_password",
                type: "post",
                //data: {user_id_list:JSON.stringify(carray)},
                data: {id: carray[0]},
                success:function(data) {
                    alert("密码重置成功");
                    //refresh();
                },
                error: function () {
                    alert("无法连接服务器");
                }
            })
            $('#hintModal').modal('hide')
        })

        $('#hintModal').modal('show')
    })

    $("#change").click(function(){
        //$('#new_label_div').hide()

        ///$('#hintModal').find(".modal-title").html("修改提示框")

        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");

        if(checkboxs.size() == 0){
            alert("请选择修改数据");
            return;
        }

        if(checkboxs.size() > 1){
            alert("每次只能修改一条");
            return;
        }
        var id = checkboxs.eq(0).attr('id')
        $.ajax({
            url: "/ajax_action_detector.php?uu=user.detail",
            type: "post",
            data: {id:id},
            success:function(data) {
                //  var ret = JSON.parse(data);
                var ret = JSON.parse(data);
                var loginid = ret["msg"]["loginid"];
                var level = ret["msg"]["level"];

                $('#change_loginid').val(loginid);

                setSelect('change_level',level)

                $('#changeModal').modal('show');
            },
            error: function () {
                alert("无法连接服务器");
            }
        })



    

/*        var carray1 =new Array()
        checkboxs.each(function(){
            carray1.push($(this).attr("value"))
        })
        var unique_carray = unique(carray1)*/
        //alert("###"+carray1+"--------"+unique_carray+"--------")


/*        var content = "<p >是否要修改账户</p>"
        $('#hintModal').find(".modal-body").html(content)

        var footer = "<button id='changeButton' type='button' class='btn btn-primary' data-toggle='modal' data-target='#changeModal'>确定</button>"+
            "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
        $('#hintModal').find(".modal-footer").html(footer)

        $("#changeButton").click(function(){
            var carray =new Array()
            var carray1 =new Array()
            var lines = $("#maintable tbody tr");
            var checkboxs = lines.find("input:eq(0):checkbox:checked");
            checkboxs.each(function(){
                carray.push(parseInt($(this).attr("id")))
            })
            $('#hintModal').modal('hide')
        })


        $('#hintModal').modal('show')*/
    })




</script>




</body>
</html>