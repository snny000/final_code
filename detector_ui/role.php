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
    <title>角色管理</title>

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

        #leftMenuPanel,#rightButtonPanel{
            width:48%;
            height:100%;
            padding:2px;
            border:1px solid #e5e5e5;
            overflow:auto;
        }

        #leftMenuPanel i{
            color: #ff892a;
        }
        #leftMenuPanel span{
            cursor: pointer;
        }

        #leftMenuPanel button{
            border: none;
            color: white;
            background:#428bca;
        }
        #leftMenuPanel div p{
            margin-left: 20px;
        }

    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;角色管理</h4>
            </div>
            <div class="upper-btn-group margin_ddos1 pull-right">
                <button resourceid='278' id="addButton" type="button" class="btn btn-interval btn-primary" data-toggle="modal" data-target="#addModal"><i class="fa fa-plus">&nbsp;&nbsp;</i>添加角色</button>
                <!--<button id="editButton" type="button" class="btn btn-interval btn-primary" data-toggle="modal" data-target="#editModal"><i class="fa fa-edit">&nbsp;&nbsp;</i>修改</button>
                <button id="removeButton" type="button" class="btn btn-interval btn-primary" data-toggle="modal"><i class="fa fa-trash-o">&nbsp;&nbsp;</i>删除</button>
                <button id="resourceButton" type="button" class="btn btn-interval btn-primary"><i class="fa fa-gear">&nbsp;&nbsp;</i>权限设置</button>-->
            </div>
        </div>
        <div class="row btn-banner upper-line"></div>
        <div class="row btn-banner">
            <input id="roleName" type="text" class="form-control search-input" placeholder="角色名（模糊搜索）">
            <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>
		</div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"></th>
                    <th width="20%">角色名称</th>
                    <th width="20%">角色描述</th>
                    <th width="20%">角色状态</th>
                    <th width="20%">操作</th>
                    <th width="10%">查看用户</th>
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <!--<td><input type="checkbox" class="checkbox" id="chk_all2"></td>-->
                    <td colspan="6">
                        <div class="pull-left">
                            <button resourceid='278' class="btn btn-default btn-sm" id="delete">删除</button>
                            <!--<button class="btn btn-default btn-sm" id="change">修改权限</button>-->
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
                    添加角色
                </h4>
            </div>
            <div class="modal-body">
                <span>角色名称：</span> <input id="add_rolename"  class="form-control";>
                <div style="color:red"></div>
                    <!--<span>状态：</span>
                    <label>
                        <input type="checkbox" checked="checked" disabled="disabled">
                        启用角色
                    </label>
					<div style="color:red"></div>-->
                <span>角色描述：</span> <input  class="form-control";>

            </div>
            <div class="modal-footer">
                <button id="add-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="editModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    修改角色
                </h4>
            </div>
            <div class="modal-body">
                <span>角色名称：</span> <input id="edit_rolename"  class="form-control";>
                <div style="color:red"></div>
                    <!--<span>状态：</span>
                    <label>
                        <input type="checkbox" checked="checked" disabled="disabled">
                        启用角色
                    </label>
					<div style="color:red"></div>-->
                <span>角色描述：</span> <input id="edit_remark"  class="form-control";>

            </div>
            <div class="modal-footer">
                <button id="change-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="resourceModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog" style="width:80%">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    权限配置
                </h4>
            </div>
            <div class="modal-body" style="text-align: center">
                <div style="color:red">配置提示：左侧配置页面，右侧配置页面对应的菜单按钮！</div>
                <div class="menuResource" style="height:300px;overflow:auto;text-align:left">
                    <div id="leftMenuPanel" class="pull-left">
                        <!--<div>
                            <input type="checkbox" id="checkAllMenu">
                            全选
                        </div>-->
                        <div>
                            <input type="checkbox" id="checkAttack">
                            攻击窃密检测策略
                        </div>
                        <div>
                            <input type="checkbox" id="checkAbnormal">
                            未知攻击检测策略
                        </div>
                        <div>
                            <input type="checkbox" id="checkTrans">
                            传输涉密检测策略
                        </div>
                        <div>
                            <input type="checkbox" id="checkObject">
                            目标审计策略
                        </div>
                        <div>
                            <input type="checkbox" id="checkNetwork">
                            网络行为审计策略
                        </div>
                        <div>
                            <input type="checkbox" id="checkIpWhite">
                            IP白名单策略
                        </div>
                        <div>
                            <input type="checkbox" id="checkBlock">
                            通信阻断策略
                        </div>
                    </div>
                    <div id="rightButtonPanel" class="pull-right">
                    </div>
                </div>
            </div>


            <!--       class="modal-footer"-->

            <div class="modal-footer">
                <button id="resourceSubmit" type="button" class="btn btn-primary">确定</button>
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

            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<div class="modal fade" id="userModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    查看用户
                </h4>
            </div>
            <div class="modal-body" style="text-align: center">
                <table class="table table-hover tbl_font_size " style="border: 1px solid lightgray;border-collapse: inherit">
                    <thead class="thead">
                        <tr>
                            <th width="20%">编号</th>
                            <th width="20%">用户名</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
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

<script>
    buildFrame("menu-role");
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
                    console.log(ret)
                    if (ret["msg"]["role_count"].length != 0) {
                        List(ret["msg"]["query_role"]);
                    } else if (ret["msg"]["role_count"].length == 0) {
                        $("#maintable tbody tr").remove();
                        $("<tr><td colspan='6' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
                    }else if (ret["code"] == 9001){
                        window.location.href = "login.php?ref="+window.location.href;
                    }else{
                        alert(ret["msg"]);
                    }
                },
                beforeSend: function () {
                    $("#maintable tbody tr").remove();
                    $("#maintable tbody").append("<tr><td colspan='6'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
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


    $("#add-submit").click(function(){
        var param = {
            "rolename":$("#add_rolename").val(),
        };
        var ischeck = true
        var add_rolename = $("#add_rolename").val()
        if(add_rolename == ""){
            $("#add_rolename").next("div").html("角色名不能为空")
            ischeck = false
        }else{
            $("#add_rolename").next("div").html("")
        }
        if(!ischeck){
            return;
        }
            $.ajax({
                url: "/ajax_action_detector.php?uu=login.role_create",
                type: "post",
                data: param,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if(ret["msg"] == "success"){
                        refresh();
                        $("#addModal").modal('hide');
                    }else{
                        alert(ret['msg']);
                    }
                }
            })
        }
    )

    function List(msgListObj){
        $("#maintable tbody tr").remove();
        var _row = $("<tr>" +
            "<td></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();row.attr("id",msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+ ">")
            row.find("td:eq(1)").text(msgListObj[i].name);
			row.find("td:eq(2)").html(msgListObj[i].name);
             row.find("td:eq(3)").html(formatterRoleType(msgListObj[i].name,row));
            // row.find("td:eq(4)").html(msgListObj[i].name);
            // row.find("td:eq(3)").html(formatterRoleType(msgListObj[i].name,row));
            row.find("td:eq(4)").html(getStrManipulation(msgListObj[i]));
            row.find("td:eq(5)").html("<a onclick='showUsers("+msgListObj[i].id+",\""+msgListObj[i].name+"\")'>查看用户</a>");
            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }
    function formatterRoleType(name,row){
        var html = "自定义";
        if(name=="用户管理员"||name=="权限管理员"||name=="系统管理员"||name=="默认角色"){
            html = "<span style='color:red'>系统内置</span>";
            row.find("td:eq(0) input").attr('disabled','disabled')
        }
        return html;
    }

    function getStrManipulation(msgListObj) {
        var permission = JSON.parse(localStorage.roleResourceIds);
        if(permission.indexOf(278)==-1){
            return ''
        }
        return `<a class="fa fa-edit" data-bind='${JSON.stringify(msgListObj)}' onclick="editRole(this)" data-toggle="modal"  data-target="#editModal">修改</a>
         <label>|</label>
         <a class="fa fa-gear" data-bind='${JSON.stringify(msgListObj)}' onclick="resourceSet(this)" data-toggle="modal"  data-target="#resourceModal">权限设置</a>`
    }

    function showUsers(roleid,rolename){
        $('#userModal').modal('show');
        $('#userModal .modal-title').text('查看用户('+rolename+')')
        $('#userModal table tbody').html('');
        $.ajax({
            url:'/ajax_action_detector.php?uu=login.user_query_all&p_size=10000&pn=1',
            data:{role_id:roleid},
            success:function(data){
                var msg = JSON.parse(data);
                if(msg["msg"]["user_count"]!=0){
                    var tr = "";
                    for(var i=0;i<msg["msg"]["user_count"];i++){
                        tr += "<tr style='text-align:left'><td>"+msg["msg"]["user_query"][i]["id"]+"</td><td>"+msg["msg"]["user_query"][i]["username"]+"</td></tr>"
                    }
                    $('#userModal table tbody').html(tr);
                }else{
                    $('#userModal table tbody').html("<tr><td colspan=3>没有用户</td></tr>");
                }
            }
        })
    }

    
    // 修改角色
    var modifyParam = {};
    function editRole(that){
        var msgListObj = JSON.parse($(that).attr('data-bind'))
        $('#edit_rolename').val(msgListObj.name);
        $('#edit_remark').val(msgListObj.name);
        modifyParam = {
            "role_id":msgListObj.id,           
        }
    }
    $("#change-submit").click(function(){
            modifyParam["rolename"] = $("#edit_rolename").val();
            var ischeck = true;
            var change_rolename = $("#edit_rolename").val();
            if(change_rolename == ""){
                $("#edit_rolename").next("div").html("角色名称不能为空")
                ischeck = false
            }else{
                $("#edit_rolename").next("div").html("")
            }
            if(!ischeck){
                return;
            }
            console.log(modifyParam)
            $.ajax({
                url: "/ajax_action_detector.php?uu=login.change_role_info",
                type: "post",
                data: modifyParam,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if(ret["msg"] == "角色信息修改成功"){
                        $("#editModal").modal('hide');
                        refresh();
                    }else{
                        alert(ret["msg"]);
                    }
                },
                error: function () {
                    alert("无法连接服务器");
                }
            })
        })
    // 角色授权
    var resourceParam = {}
    function resourceSet(that){
        var currentData = JSON.parse($(that).attr('data-bind'));
        var role_id = currentData.id;
        resourceParam["role_id"] = role_id;
        $('#rightButtonPanel p').show();
        $('#rightButtonPanel').find('input[type=checkbox]').prop('checked',false);
        $('#leftMenuPanel').find('input[type=checkbox]').prop('checked',false);
        $('#leftMenuPanel p').css('background','');
        // 获取当前角色的权限
        $.ajax({
            url:'/ajax_action_detector.php?uu=login.role_query_permission',
            type: "post",
            data:{role_id:role_id},
            success:function(data){
                console.log(data)
                var ret = JSON.parse(data);
                // 匹配权限，已有的打勾
                if(ret["msg"]["permission_id_list"]!=undefined){
                    var _roleResourcce = ret["msg"]["permission_id_list"]
                    $('#leftMenuPanel p input[type=checkbox]').each(function(){
                        if(_roleResourcce.indexOf(parseInt($(this).attr("id"))) != -1)
                            $(this).prop('checked',true);
                    });
                    $('#rightButtonPanel p input[type=checkbox]').each(function(){
                        if(_roleResourcce.indexOf(parseInt($(this).attr("id"))) != -1)
                            $(this).prop('checked',true);
                    })
                }else{
                    
                }
                var divchk = $('#leftMenuPanel div');
                $.each(divchk,function(i){
                    if($(divchk[i]).find('p input').not("input:checked").length == 0){
                        $(divchk[i]).find('input:eq(0)').prop('checked',true);
                    }else{
                        $(divchk[i]).find('input:eq(0)').prop('checked',false);
                    }
                })
            }
        })
    }
    $('#resourceSubmit').on('click',function(){
        var permission_id_list = [];
        // 处理4个策略大菜单
        if($('#checkAttack').parent().find('p input:checked').length!=0){
            permission_id_list.push(404); // 攻击窃密检测策略大菜单权限id为404，根据数据库修改，下同
        }
        if($('#checkTrans').parent().find('p input:checked').length!=0){
            permission_id_list.push(405); // 传输涉密检测策略大菜单权限id
        }
        if($('#checkObject').parent().find('p input:checked').length!=0){
            permission_id_list.push(406); // 目标审计策略大菜单权限id
        }
        if($('#checkNetwork').parent().find('p input:checked').length!=0){
            permission_id_list.push(407); // 网络行为审计策略大菜单权限id
        }
        $('#leftMenuPanel p input[type=checkbox]:checked').each(function(){
            permission_id_list.push(parseInt($(this).attr('id')));
        });
        $('#rightButtonPanel p input[type=checkbox]:checked').each(function(){
            permission_id_list.push(parseInt($(this).attr('id')));
        });
        resourceParam["permission_id_list"] = JSON.stringify(permission_id_list);
        $.ajax({
            url:'/ajax_action_detector.php?uu=login.role_add_permission',
            type: "post",
            data: resourceParam,
            success:function(data){
                var ret = JSON.parse(data)
                if(ret["msg"] == "success"){
                    $("#resourceModal").modal('hide');
                }else if(ret["msg"] == "failure"){
                    alert('权限已清空！');
                    $("#resourceModal").modal('hide');
                }else{
                    alert(ret["msg"]);
                }
            }
        })
    })

    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=login.role_query_all&p_size="+p_size,
            type: "post",
            data: searchParam,
            success:function(data) {
                var ret = JSON.parse(data);
                console.log(ret)
                if (ret["role_count"] != 0)
                    ret = ret["msg"]["role_count"]
                else {
                    ret = 0;
                }
                $("#totalcount").text(ret);
                $('#pagination').empty();
                $('#pagination').removeData("twbs-pagination");
                $('#pagination').unbind("page");
                pagination(ret,"/ajax_action_detector.php?uu=login.role_query_all&p_size="+p_size,parseInt(currentPage),searchParam)
            },
            beforeSend: function () {
                $(".loading-pic").removeClass("hidden");
            },
            error: function () {
                alert("无法连接服务器");
            }
        })
    }


    var globalSearchParam = {random:1}

    //第一次加载分页
    LoadPage(1,globalSearchParam)
    $("#searchButton").click(function(){
        var rolename =  $("#roleName").val();
        globalSearchParam = {random:1}
        if(rolename!=""){
            globalSearchParam["rolename"] = rolename
        }
        LoadPage(1,globalSearchParam)
    })

    $("#clearButton").click(function(){
        $("#roleName").val("");
        $('#searchButton').click();
    })

   $("#delete,#removeButton").click(function(){
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
            console.log("carray:"+carray)
            $.ajax({
                url: "/ajax_action_detector.php?uu=login.role_delete",
                type: "post",
                data: {role_id_list:JSON.stringify(carray)},
                success:function(data) {
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
</script>
<script>
    // 控制权限选择
    var checkControl = function(){
        var allSelected = $('#checkAllMenu');
       var menuCheckbox = $('#leftMenuPanel').find('p input[type=checkbox]'); //所有菜单项
       var menuCount = menuCheckbox.length; // 菜单数目
       // 全选
       allSelected.click(function() {
           var $this = $(this);
           menuCheckbox.click(); // 出发菜单及按钮选中
           if( $this.prop('checked') ) {
               menuCheckbox.each(function() {
                   $(this).prop('checked', true);
               });
           } else {
               menuCheckbox.each(function() {
                   $(this).prop('checked', false);
               });
           }
       });
       menuCheckbox.click(function(){
           $('#leftMenuPanel p').css('background','');
           $(this).parent().css('background','yellow');
           var checkedLength = $('#leftMenuPanel').find('p input[type=checkbox]').filter(':checked').length;
           if(checkedLength == menuCount){
               allSelected.prop('checked',true)
           }else{
               allSelected.prop('checked',false)
           }
           var divchk = $('#leftMenuPanel div');
           $.each(divchk,function(i){
               if($(divchk[i]).find('p input').not("input:checked").length == 0){
                   $(divchk[i]).find('input:eq(0)').prop('checked',true);
               }else{
                   $(divchk[i]).find('input:eq(0)').prop('checked',false);
               }
           })
       })
    // 点击菜单查看对应按钮，隐藏其他按钮
    $('#leftMenuPanel p span,#leftMenuPanel p button').on('click',function(){
        $('#leftMenuPanel p').css('background','');
        $(this).parent().css('background','yellow');
        var showMenuButton = $(this).attr('content_type_id');
        $('#rightButtonPanel p').show();
        $('#rightButtonPanel p').each(function(){
            if($(this).attr('content_type_id') != showMenuButton){
                $(this).hide();
            }
        })
    })
    // 勾选菜单，默认对应按钮全选
    $('#leftMenuPanel p input[type=checkbox]').on('click',function(){
        var showMenuButton = $(this).attr('content_type_id');
        var isChecked = $(this).prop("checked");
        $('#rightButtonPanel p').show();
        $('#rightButtonPanel p').each(function(){
            if($(this).attr('content_type_id') != showMenuButton){
                $(this).hide();
            }
        })
        $('#rightButtonPanel p input[type=checkbox]').each(function(){
            if($(this).attr('content_type_id') == showMenuButton){
                isChecked==true ? $(this).prop('checked',true) : $(this).prop('checked',false);
            }
        })
    })
    // 勾选按钮，确保菜单选中
    $('#rightButtonPanel p input[type=checkbox]').on('click',function(){
        var showButton = $(this).attr('content_type_id');
        var isChecked = $(this).prop("checked");
        $('#leftMenuPanel p input[type=checkbox]').each(function(){
            if($(this).attr('content_type_id') == showButton){
                if(isChecked==true && $(this).prop('checked')==false)
                    $(this).prop('checked',true)
            }
        })
    })

    // 策略大类选择
    $('#checkAttack,#checkTrans,#checkObject,#checkNetwork,#checkAbnormal,#checkIpWhite,#checkBlock').on('click',function(){
        if($(this).prop('checked')){
            $(this).nextAll().find('input').prop('checked',false)
            $(this).nextAll().find('input').click();
        }else{
            $(this).nextAll().find('input').prop('checked',true)
            $(this).nextAll().find('input').click();
        }
    })

    }
    $(function(){
       // 初始化所有权限列表
       $.ajax({
            url:'/ajax_action_detector.php?uu=login.query_all_permissions',
            type: "post",
            success:function(data){
                var ret = JSON.parse(data);
                var allResource = ret["msg"]["all_permissions"];
                //console.log(allResource)
                allResource.map(function(item,key){
                     var menu = `<p>
                            <input id=${item["menu"]["id"]} content_type_id=${item["menu"]["content_type_id"]} type="checkbox">
                            <span content_type_id=${item["menu"]["content_type_id"]}>
                                <i class="fa fa-folder-open-o"></i>
                                ${item["menu"]["name"]}(${item["menu"]["id"]})
                            </span>
                            <button content_type_id=${item["menu"]["content_type_id"]} class="pull-right">详细配置</button>
                        </p>`
                    if (item["menu"]["name"]=="木马攻击检测策略" ||
                        item["menu"]["name"]=="漏洞利用检测策略" ||
                        item["menu"]["name"]=="恶意程序检测策略"){
                            $('#checkAttack').parent().append(menu)
                        }
                    else if(item["menu"]["name"]=="关键字检测策略" ||
                        item["menu"]["name"]=="加密文件检测策略" ||
                        item["menu"]["name"]=="多层压缩检测策略" ||
                        item["menu"]["name"]=="图片筛选策略" ){
                            $('#checkTrans').parent().append(menu)
                        }
                    else if(item["menu"]["name"]=="IP审计检测策略" ||
                        item["menu"]["name"]=="域名审计检测策略" ||
                        item["menu"]["name"]=="URL审计检测策略" ||
                        item["menu"]["name"]=="账号审计检测策略" ){
                            $('#checkObject').parent().append(menu)
                        }
                    else if(item["menu"]["name"]=="通联关系上报策略" ||
                        item["menu"]["name"]=="应用行为上报策略" ||
                        item["menu"]["name"]=="应用行为WEB过滤策略" ||
                        item["menu"]["name"]=="应用行为DNS过滤策略" ){
                            $('#checkNetwork').parent().append(menu)
                        }
                    else if(item["menu"]["name"]=="未知攻击检测策略"){
                            $('#checkAbnormal').parent().append(menu)
                        }
                    else if(item["menu"]["name"]=="IP白名单策略"){
                            $('#checkIpWhite').parent().append(menu)
                        }
                    else if(item["menu"]["name"]=="通信阻断策略"){
                            $('#checkBlock').parent().append(menu)
                        }
                    else
                        $('#leftMenuPanel').append(menu);
                    var buttonList = item["button"];
                    if(buttonList!=undefined){
                        buttonList.map(function(v,i){
                        var button = `
                            <p content_type_id=${v["content_type_id"]}>
                                    <label>
                                        <input id=${v["id"]} content_type_id=${v["content_type_id"]} type="checkbox">
                                        ${v["name"]}(${v["id"]})
                                    </label>
                                </p>
                            `
                        $('#rightButtonPanel').append(button);
                       })
                    }      
                })
                checkControl();
            }
        })
   })
    
</script>
</body>
</html>