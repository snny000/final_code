<?php
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');
require_once(dirname(__FILE__) . '/require_get_parameter_for_rule_page.php');
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>插件部署管理</title>

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

        .upper-btn-group{
            position: relative;
            display: inline-block;
        }

        .upper-line{
            border-bottom: solid 1px #DDDDDD;
            margin-bottom: 20px;
        }

        .uploadDiv {
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }

    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;插件部署管理
                    <div class="btn-group" data-toggle="buttons">
                        <button type="button" href='plug.php' class="btn btn-default btn-primary">管理中心本地</button>
                        <button type="button" href='plug_director.php' class="btn btn-default">指挥节点下发</button>
                    </div>
                </h4>
            </div>
            <div class="upper-btn-group margin_ddos1 pull-right">
                <button resourceid='396' id="addButton" type="button" class="btn btn-interval btn-primary" data-toggle="modal" data-target="#addModal"><i class="fa fa-plus">&nbsp;&nbsp;</i>添加</button>
                <div class="btn-group btn-interval">
                    <button resourceid='396' type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown"><i class="fa fa-hourglass">&nbsp;&nbsp;</i>同步
                        <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu" role="menu">
                        <li><a id="full" href="#">刷新检测器插件集<span hidden=""></span></a></li>
                        <li class="divider"></li>
                        <li><a id="fullCenter" href="#">上报管理中心插件</a></li>
                    </ul>
                </div>
                <button resourceid='396' id="increment" type="button" class="btn btn-primary btn-interval" disabled=""><i class="fa fa-hourglass-half">&nbsp;&nbsp;</i>增量&nbsp;<span class="badge" style="background-color:orange"></span></button>
            </div>
        </div>

        <div class="row btn-banner upper-line"></div>
        <div class="row btn-banner"> <!--指挥中心相关查询-->
            <div class="input-group date form_datetime date_div">
                <input id="time_min" class="form-control" size="16" type="text" value="" readonly placeholder="开始时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>

            <div class="input-group date form_datetime date_div btn-interval2">
                <input id="time_max" class="form-control" size="16" type="text" value="" readonly placeholder="截止时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>

            <input id="plug_id" type="text" class="form-control search-input btn-interval2" placeholder="插件ID（模糊搜索）">
            <input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器ID(精确搜索)">
            <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="rule_status" class="pull-left" value="-1">是否同步</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="-1">所有同步状态</li>
                    <li onclick="selectProtoFwd(this);" value="1">待同步</li>
                    <li onclick="selectProtoFwd(this);" value="0">已同步</li>
                </ul>
            </div>

            <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>
        </div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="6%">插件ID</th>
                    <th width="6%">插件版本</th>
                    <th width="7%">插件文件</th>
                    <th width="8%">插件策略版本</th>
                    <th width="7%">CPU资源要求(%)</th>
                    <th width="8%">内存资源要求(MB)</th>
                    <th width="8%">磁盘资源要求(MB)</th>
                    <th width="8%">插件配置文件</th>
                    <th width="5%">插件状态</th>
                    <th width="9%">创建时间</th>
                    <th width="7%">生效范围</th>
                    <th width="7%">操作</th>
                    <th width="9%">检测器操作</th>
                </tr>
                </thead>
                    <!--<tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="7%">1</th>
                    <th width="7%">11</th>
                    <th width="7%">111</th>
                    <th width="8%">1</th>
                    <th width="7%">25</th>
                    <th width="8%">20</th>
                    <th width="8%">30</th>
                    <th width="8%">24</th>
                    <th width="8%">24</th>
                    <th width="8%">24</th>
                    <th width="7%">查看生效范围</th>
                    <th width="7%">变更生效范围</th>
                    <th width="9%">查看检测器</th>
                </tr>-->
                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
                    <td>
                        <div class="pull-left">
                            <button resourceid='396' class="btn btn-default btn-sm" id="delete">删除</button>
                            <button resourceid='396' class="btn btn-default btn-sm" id="alter">批量变更生效范围</button>
                            <button resourceid='396' class="btn btn-default btn-sm" id="append">批量追加生效范围</button>
                            <button resourceid='396' class="btn btn-default btn-sm" id="recover">批量全部生效</button>
                            <button resourceid='396' class="btn btn-default btn-sm" id="clean">批量清空生效范围</button>
                            <button resourceid='396' class="btn btn-primary btn-sm" onclick="updatePlug('plug')">更新插件</button>
                            <button resourceid='396' class="btn btn-primary btn-sm" onclick="updatePlug('plug_config')">更新插件配置</button>
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
                    添加插件
                </h4>
            </div>
            <div class="modal-body">

                <div>
                    <span>插件ID:</span> <input id="add_plug_id" class="form-control">
                    <div style="color:red"></div>
                    <span>插件版本:</span> <input id="add_plug_version" class="form-control">
                    <div style="color:red"></div>
                    
                    <span>上传插件文件:</span>
                    <div class="uploadDiv"><!-- widget-group-center -->
                        <p style="border:solid 1px #E3E3E3"><input type="file" id="upfile1" ></p>
                        <p style="text-align:center">
                            <input type="button" id="upJQuery1" value="上传文件" class="btn btn-primary" >
                        </p>
                        <div style='color:red;margin-top: 4px;text-align:center'></div>
                        <input id="add_plug_path" hidden>
                        <input id="add_plug_name" hidden>
                        <div style="color:red"></div>
                    </div>

                    <span>插件策略版本:</span> <input id="add_plug_config_version" class="form-control">
                    <div style="color:red"></div>
                    <span>CPU资源要求(%):</span> <input id="add_plug_config_cpu" class="form-control">
                    <span>内存资源要求(MB):</span> <input id="add_plug_config_mem" class="form-control">
                    <span>磁盘资源要求(MB):</span> <input id="add_plug_config_disk" class="form-control">
                    
                    <span>上传插件配置文件:</span>
                    <div class="uploadDiv"><!-- widget-group-center -->
                        <p style="border:solid 1px #E3E3E3"><input type="file" id="upfile2" ></p>
                        <p style="text-align:center">
                            <input type="button" id="upJQuery2" value="上传文件" class="btn btn-primary" >
                        </p>
                        <div style='color:red;margin-top: 4px;text-align:center'></div>
                        <input id="add_plug_config_path" hidden>
                        <input id="add_plug_config_name" hidden>
                        <div style="color:red"></div>
                    </div>
                </div>

                <!--<div>
                    <span>备注标签（可用于查询）：</span> <input id="add_label"  class="form-control";>
                    <div style="color:red"></div>
                </div>-->

            </div>
            <div class="modal-footer">
                <button id="add-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<!-- 模态框（Modal） -->
<div class="modal fade" id="updatePlugModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    更新插件
                </h4>
            </div>
            <div class="modal-body">

                <div>
                    <span>插件ID:</span> <input id="edit_plug_id" class="form-control" disabled>
                    <div style="color:red"></div>
                    <span>插件版本:</span> <input id="edit_plug_version" class="form-control">
                    <div style="color:red"></div>
                    
                    <span>上传插件文件:</span>
                    <div class="uploadDiv"><!-- widget-group-center -->
                        <p style="border:solid 1px #E3E3E3"><input type="file" id="upfile3" ></p>
                        <p style="text-align:center">
                            <input type="button" id="upJQuery3" value="上传文件" class="btn btn-primary" >
                        </p>
                        <div style='color:red;margin-top: 4px;text-align:center'></div>
                        <input id="edit_plug_path" hidden>
                        <div style="color:red"></div>
                        <span>当前文件:</span>
                        <input id="edit_plug_name" class="form-control" disabled>
                    </div>

                    <span>插件策略版本:</span> <input id="edit_plug_config_version" class="form-control">
                    <div style="color:red"></div>
                    <span>CPU资源要求(%):</span> <input id="edit_plug_config_cpu" class="form-control">
                    <span>内存资源要求(MB):</span> <input id="edit_plug_config_mem" class="form-control">
                    <span>磁盘资源要求(MB):</span> <input id="edit_plug_config_disk" class="form-control">
                    
                    <span>上传插件配置文件:</span>
                    <div class="uploadDiv"><!-- widget-group-center -->
                        <p style="border:solid 1px #E3E3E3"><input type="file" id="upfile4" ></p>
                        <p style="text-align:center">
                            <input type="button" id="upJQuery4" value="上传文件" class="btn btn-primary" >
                        </p>
                        <div style='color:red;margin-top: 4px;text-align:center'></div>
                        <input id="edit_plug_config_path" hidden>
                        <div style="color:red"></div>
                        <span>当前文件:</span>
                        <input id="edit_plug_config_name" class="form-control" disabled>
                    </div>
                </div>

                <!--<div>
                    <span>备注标签（可用于查询）：</span> <input id="edit_label"  class="form-control";>
                    <div style="color:red"></div>
                </div>-->

            </div>
            <div class="modal-footer">
               <!--  <button id="edit-submit" type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button> -->
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>

<?php
require_once(dirname(__FILE__) . '/require_hint_modal_for_rule_page.php');
?>






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
<script src="js/plug_operate.js"></script>
<script>
    buildFrame("menu-plug1");
    $('h4 .btn-group').on('click','button',function(){
        window.location.replace($(this).attr('href'));
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




    $("#add-submit").click(function(){
        var id = 0
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        id = $(checkboxs).attr("id")
        var param = {
            "id": id,
            "plug_id":$("#add_plug_id").val(),
            "plug_type":"detect",
            "plug_version":$("#add_plug_version").val(),
            "plug_path": $("#add_plug_path").attr("value"),
            "plug_name": $("#add_plug_name").attr("value"),
            "plug_config_version": $("#add_plug_config_version").val(),
            "cpu": $("#add_plug_config_cpu").val() == ""? 0: $("#add_plug_config_cpu").val(),
            "mem": $("#add_plug_config_mem").val() == ""? 0:$("#add_plug_config_mem").val(),
            "disk": $("#add_plug_config_disk").val() == ""? 0:$("#add_plug_config_disk").val(),
            "plug_config_path": $("#add_plug_config_path").attr("value"),
            "plug_config_name": $("#add_plug_config_name").attr("value"),
        };


            var ischeck = true
            var plug_id = $("#add_plug_id").val()
            var plug_version = $("#add_plug_version").val()
            var plug_path = $("#add_plug_path").attr("value")
            var plug_config_version = $("#add_plug_config_version").val()
            var plug_config_path = $("#add_plug_config_path").attr("value")
    

            if(plug_id == ""){
                $("#add_plug_id").next("div").html("插件ID不能为空")
                ischeck = false
            }else{
                $("#add_plug_id").next("div").html("")
            }
            if(plug_version == ""){
                $("#add_plug_version").next("div").html("插件版本不能为空")
                ischeck = false
            }else{
                $("#add_plug_version").next("div").html("")
            }
            if(plug_config_version == ""){
                $("#add_plug_config_version").next("div").html("插件配置策略版本不能为空")
                ischeck = false
            }else{
                $("#add_plug_config_version").next("div").html("")
            }
            if(plug_path == undefined || plug_path == ""){
                $("#add_plug_name").next("div").html("请上传插件文件！")
                ischeck = false
            }else{
                $("#add_plug_name").next("div").html("")
            }
            if(plug_config_path == undefined || plug_config_path == ""){
                $("#add_plug_config_name").next("div").html("请上传插件配置文件！")
                ischeck = false
            }else{
                $("#add_plug_config_name").next("div").html("")
            }

            if(!ischeck){
                return;
            }

            $.ajax({
                url: "/ajax_action_detector.php?uu=plugin.add_update_plugin",
                type: "post",
                data: {cmd:0,json:JSON.stringify(param)},
                success:function(data) {
                    var ret = JSON.parse(data);
                    if(ret.code!=200){
                        alert(ret.msg);
                        return;
                    }
                    $("#addModal").modal('hide');
                    console.log(data)
                    refresh();
                }
            })

        }
    )
    //上传插件--文件上传
    upload("plugin.fileupload", "#upJQuery1","#upfile1","#add_plug_path","#add_plug_name");
    upload("plugin.fileupload", "#upJQuery2","#upfile2","#add_plug_config_path","#add_plug_config_name");
    //更新插件--文件上传
    upload("plugin.fileupload", "#upJQuery3","#upfile3","#edit_plug_path","#edit_plug_name");
    upload("plugin.fileupload", "#upJQuery4","#upfile4","#edit_plug_config_path","#edit_plug_config_name");

    function List(msgListObj){
        var trojan_typeMap = {1:'特种木马',2:'普通木马',3:'远控',4:'其他'}
        var prevalenceMap= {1:'高',2:'中',3:'低'}
        var riskMap = {0:'无风险',1:'一般级',2:'关注级',3:'严重级',4:'紧急级'}
        var statusMap = {0:'已同步',1:'待同步'}
        var store_pcapMap = {1:'保留',2:'不保留'}
        var operateMap = {1:'增加',2:'删除',3:'变更范围'}

        $("#maintable tbody tr").remove();
        // var nodetd = node_type==2 ? "<td style='color:#999999'></td>" : "<td style='color:#999999;display:none'></td>"
        // var operatetd = node_type==2 ? "<td style='color:#999999;display:none'></td>" : "<td style='color:#999999'></td>"
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
            "<td style='color:#999999'></td>"+
            // operatetd +
            // nodetd +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();row.attr("id",msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' plug_id="+msgListObj[i].plug_id+" id="+msgListObj[i].id+ " value="+msgListObj[i].device_id_list.replace(/\s/g, "")+">")
            row.find("td:eq(1)").text(msgListObj[i].plug_id);
            row.find("td:eq(2)").html(msgListObj[i].plug_version);
            // row.find("td:eq(3)").html(msgListObj[i].plug_path);
            row.find("td:eq(3)").html("<a url="+msgListObj[i].plug_path+" href=ajax_action_download_rename_common.php?uu=download&path="+msgListObj[i].plug_path+"&rename="+msgListObj[i].plug_name+">"+msgListObj[i].plug_name+"</a>");
            row.find("td:eq(4)").html(msgListObj[i].plug_config_version);
           // row.find("td:eq(5)").html(prevalenceMap[msgListObj[i].prevalence]);
            row.find("td:eq(5)").html(msgListObj[i].cpu);
            row.find("td:eq(6)").html(msgListObj[i].mem);
            row.find("td:eq(7)").html(msgListObj[i].disk);
            // row.find("td:eq(8)").html(msgListObj[i].plug_config_path);
            row.find("td:eq(8)").html("<a url="+msgListObj[i].plug_config_path+" href=ajax_action_download_rename_common.php?uu=download&path="+msgListObj[i].plug_config_path+"&rename="+msgListObj[i].plug_config_name+">"+msgListObj[i].plug_config_name+"</a>");
            row.find("td:eq(9)").html(plugStatusFormat(msgListObj[i]));
            row.find("td:eq(10)").html(msgListObj[i].generate_time);
            
            var operateviewhtml=generateoperateviewhtml(msgListObj[i].id,msgListObj[i].device_id_list)
            var operatehtml=generateoperatehtml(msgListObj[i].id,msgListObj[i].device_id_list)
            var operateviewhtml_new = generateoperateviewhtml_new(msgListObj[i].id,msgListObj[i].device_id_list,msgListObj[i].plug_on_device_status,msgListObj[i].plug_status)
            row.find("td:eq(11)").html(operateviewhtml);
            row.find("td:eq(12)").html(operatehtml);
            row.find("td:eq(13)").html(operateviewhtml_new);
            
            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }

    // 插件状态格式化
    function plugStatusFormat(msgListObj){
        var statusMap = {0:'已同步',1:'待同步'};
        var operateMap = {0:'新增',1:'删除',2:'变更生效范围',3:'插件变更',4:'插件配置变更',5:''};
        var add_update_plug_cmd_map = {0: 'add', 1: 'update_plug', 2: 'update_config'}

        var cmdStr = [];
        var plugCmd = JSON.parse(msgListObj.cmd);
        if(msgListObj.plug_status == 1){
            for(var i=0,l=plugCmd.length;i<l;i++){
                cmdStr.push(operateMap[plugCmd[i]])
            }
            cmdStr = cmdStr.join("+");
            return `<span style="color:orange">(${cmdStr})${statusMap[msgListObj.plug_status]}</span>`;
        }
        return `${statusMap[msgListObj.plug_status]}`
    }

    /*更新插件，含更新插件配置*/
    var updatePlug = function(type){
        $('#upJQuery3,#upJQuery4').attr('disabled','disabled');
        if(type=="plug"){
            $('#updatePlugModal').find(".modal-title").html("更新插件");

            $('#edit_plug_version').show();
            $('#edit_plug_version').prev().show();
            $($('#updatePlugModal .uploadDiv')[0]).show();
            $($('#updatePlugModal .uploadDiv')[0]).prev().show();
            
        }else{
            $('#updatePlugModal').find(".modal-title").html("更新插件配置");

            $('#edit_plug_version').hide();
            $('#edit_plug_version').prev().hide();
            $($('#updatePlugModal .uploadDiv')[0]).hide();
            $($('#updatePlugModal .uploadDiv')[0]).prev().hide();
        }
        

        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");

        if(checkboxs.size() == 0){
            alert("请选择要更新的数据");
            return;
        }else if(checkboxs.size()>1){
            alert("每次只允许更新一条插件信息");
            return;
        }

        var carray =new Array();
        checkboxs.each(function(){
            var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
            if(status != '(删除)待同步'){
                carray.push(parseInt($(this).attr("id")))
            }
        })
        if(carray.length==0){
            alert('当前插件已删除，不能修改!');
            return;
        }
        var checkbox = checkboxs[0];
        var td = $(checkbox).parent().nextAll();
        var plug_id = $(checkbox).attr('plug_id');
        var plug_version = $(td[1]).html();
        var plug_path = $(td[2]).find('a').attr('url');
        var plug_config_version = $(td[3]).html();
        var plug_config_cpu = $(td[4]).html();
        var plug_config_mem = $(td[5]).html();
        var plug_config_disk = $(td[6]).html();
        var plug_config_path = $(td[7]).find('a').attr('url');

        var plug_name = $(td[2]).text();
        var plug_config_name = $(td[7]).text();
        $('#edit_plug_id').val(plug_id);
        $('#edit_plug_version').val(plug_version);
        $('#edit_plug_path').attr('value',plug_path);
        $('#edit_plug_config_version').val(plug_config_version);
        $('#edit_plug_config_cpu').val(plug_config_cpu);
        $('#edit_plug_config_mem').val(plug_config_mem);
        $('#edit_plug_config_disk').val(plug_config_disk);
        $('#edit_plug_config_path').attr('value',plug_config_path);

        $('#edit_plug_name').val(plug_name);
        $('#edit_plug_config_name').val(plug_config_name);
        

        var footer = '<div class="modal-footer">'+
                '<button id="edit-submit" type="button" class="btn btn-primary">提交</button>'+
                '<button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>'+
            '</div>'
        $('#updatePlugModal').find(".modal-footer").html(footer)

        $("#edit-submit").click(function(){
            var id = 0
            var lines = $("#maintable tbody tr");
            var checkboxs = lines.find("input:eq(0):checkbox:checked");
            id = $(checkboxs).attr("id")
            var param = {
                "id": id,
                "plug_id": plug_id,
                "plug_type": "detect",
                "plug_version": $("#edit_plug_version").val(),
                "plug_path": $('#edit_plug_path').attr('value'),
                "plug_name": $('#edit_plug_name').attr('value'),
                "plug_config_version": $('#edit_plug_config_version').val(),
                "cpu": $('#edit_plug_config_cpu').val() ==""?0:$('#edit_plug_config_cpu').val(),
                "mem": $('#edit_plug_config_mem').val() ==""?0:$('#edit_plug_config_mem').val(),
                "disk": $('#edit_plug_config_disk').val() ==""?0:$('#edit_plug_config_disk').val(),
                "plug_config_path": $('#edit_plug_config_path').attr('value'),
                "plug_config_name": $('#edit_plug_config_name').attr('value'),
            };
            var ischeck = true;
            if($('#edit_plug_version').val() == ""){
                $("#edit_plug_version").next("div").html("插件版本不能为空")
                ischeck = false
            }else{
                $("#edit_plug_version").next("div").html("");
            }
            if($('#edit_plug_config_version').val() == ""){
                $("#edit_plug_config_version").next("div").html("插件配置策略版本不能为空")
                ischeck = false
            }else{
                $("#edit_plug_config_version").next("div").html("")
            }
            if($('#edit_plug_path').attr('value') == undefined || $('#edit_plug_path').attr('value')==""){
                $("#edit_plug_path").next("div").html("请上传插件文件！")
                ischeck = false
            }else{
                $("#edit_plug_path").next("div").html("");
            }
            if($('#edit_plug_config_path').attr('value') == undefined || $('#edit_plug_config_path').attr('value')==""){
                $("#edit_plug_config_path").next("div").html("请上传插件配置文件！")
                ischeck = false
            }else{
                $("#edit_plug_config_path").next("div").html("")
            }

            if(!ischeck){
                return;
            }

            var plugCmd = 2; //更新插件or更新插件配置
            if(type=="plug"){
                plugCmd = 1
            }

            $.ajax({
                url: "/ajax_action_detector.php?uu=plugin.add_update_plugin",
                type: "post",
                data: {cmd:plugCmd,plug_id:plug_id,id:id,json:JSON.stringify(param)},
                success:function(data) {
                    var ret = JSON.parse(data);
                    console.log(data)
                    if(ret.code!=200){
                        alert(ret.msg);
                        return;
                    }
                    refresh();
                }
            })
            $("#updatePlugModal").modal('hide');

        })
        $('#updatePlugModal').modal('show')
    }

    function LoadPage(currentPage,searchParam,is_director){
        is_director = is_director || 0;
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin.show_plug_count&is_director=" + is_director,
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
                pagination(ret,"/ajax_action_detector.php?uu=plugin.show_all_plug&p_size="+p_size + "&is_director=" + is_director,parseInt(currentPage),searchParam)
            },
            beforeSend: function () {
                $(".loading-pic").removeClass("hidden");
            },
            error: function () {
                alert("无法连接服务器");
            }
        })

        if (is_director == 0) {
            $.ajax({ //全量
                url: "/ajax_action_detector.php?uu=plugin.is_changed&policy_type=1&type=1",
                success:function(data) {
                    var ret = JSON.parse(data);

                    if(ret.msg==0){
                        $("#full span").text("");
                        $("#full").prop('disabled',"true");
                    }else{
                        $("#full span").text(ret.msg);
                        $("#full").removeAttr('disabled')
                    }
                }
            })

            $.ajax({ //增量
                url: "/ajax_action_detector.php?uu=plugin.is_changed&type=0",
                success:function(data) {
                    var ret = JSON.parse(data);
                    if(ret.msg==0){
                        $("#increment span").text("");
                        $("#increment").prop('disabled',"true");
                    }else{
                        $("#increment span").text(ret.msg);
                        $("#increment").removeAttr('disabled')
                    }
                }
            })
        }
    }

     var globalSearchParam = {random:1}

    //第一次加载分页
    //LoadPage(1,globalSearchParam)
    globalSearchParam = cacheSearchParam;
    // if(node_type == undefined)
    LoadPage(cachePage,globalSearchParam);



    $("#searchButton").click(function(){
        var plug_id =  $("#plug_id").val();
        var device_id = $("#device_id").val();
        var plug_status = $("#rule_status").attr("value").toString();
        // var director_node = $("#director_node").val(); //指挥节点
        // var manage_center = $("#manage_center").val(); //管理中心
        // var virtual_group = $("#virtual_group").val(); //虚拟组
        var time_min = $("#time_min").val();
        var time_max =$("#time_max").val();

        globalSearchParam = {random:1}
        if(plug_id!=""){
            globalSearchParam["plug_id"] = plug_id
        }
        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
        }
        // if(director_node!=""){
        //     globalSearchParam["node_id"] = director_node
        // }
        // if(manage_center!=""){
        //     globalSearchParam["center_id"] = manage_center
        // }
        // if(virtual_group!=""){
        //     globalSearchParam["virtual_group_id"] = virtual_group
        // }
        if(time_min!=""){
            globalSearchParam["time_min"] = time_min
        }
        if(time_max!=""){
            globalSearchParam["time_max"] = time_max
        }
        if(plug_status!="-1"){
            globalSearchParam["plug_status"] = plug_status
        }
        // if(node_type!=undefined){
        //     globalSearchParam['type'] = node_type;
        // }
        // if(is_contain_sub == 1){
        //     globalSearchParam['is_contain_sub'] = is_contain_sub;
        // }

        LoadPage(1,globalSearchParam)
    })

    $("#clearButton").click(function(){
        $("#plug_id").val("");
        $("#device_id").val("");
        
        $("#time_min").val("");
        $("#time_max").val("");
        // $('#director_node').selectpicker("val","");
        // $('#manage_center').selectpicker("val","");
        // $('#virtual_group').selectpicker("val","");
        // $("#task_group_id").selectpicker("val","");
        firstSelect("rule_status");
    })

 
</script>
<script>

    function pickDetectorForward(id,device_id_list,type,plug_on_device_status){
        var param= {cacheRef:'plug.php'}
        var currentPage = $('#pagination .active a').text()
        param["cachePage"] = currentPage

        param["cacheDevice_id_list"]=JSON.stringify(eval(device_id_list));

        param["cacheCmd_type"] = type;

        param["cachePlug_on_device_status"] = JSON.stringify(plug_on_device_status);

        param["cacheSearchParam"] = JSON.stringify(globalSearchParam)

        param["cacheMenu"] = "menu-plug1";
        param["cacheType"]=1
        param["cachePolicy_type"] = 1

        if(id instanceof Array){
            console.log("@@@@@@@@", param['cacheId'])
            param["cacheId"] = JSON.stringify(id)

        }else{
            var carray =new Array()
            carray.push(parseInt(id))
            param["cacheId"] = JSON.stringify(carray)
            console.log("########", param['cacheId'])
        }
        // 判断是否已删除，已删除待同步的插件不能再变更生效范围和修改，只能下发
        var ids = JSON.parse(param["cacheId"]);
        var newIds = new Array();
        for(var i=0;i<ids.length;i++){
            var status = $('#maintable tbody tr[id='+ids[i]+'] td span').text();
            if(status != '(删除)待同步'){
                newIds.push(ids[i]);
            }
        }
        // if(newIds.length==0){
        //     alert('当前插件已删除，不能变更生效范围!');
        //     return;
        // }
        param["cacheId"] = JSON.stringify(newIds);
        console.log("$$$$$$$$", param['cacheId'])
        if(type==3){
            post_blank('pick_detector_plug.php',param);

        }else{
            post('pick_detector_plug.php',param);
        }
    }

/* 判断是否包含post_device_id,如果有则是从设备管理页跳转过来的，重载数据 */
$(function(){
    if(typeof(post_device_id) != "undefined"){
        $('#device_id').val(post_device_id);
        $('#searchButton').click();
    }
})

</script>

</body>
</html>