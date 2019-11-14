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

    <title>检测器备案管理</title>

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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;检测器备案管理</h4>
            </div>
            <div class="upper-btn-group margin_ddos1 pull-right">
                <button class="btn btn-interval btn-primary" id="export" onclick="export_file()">导入模板下载</button>
                <button resourceid='352' id="x3" type="button" class="btn btn-primary btn-interval"  data-toggle="modal" data-target="#addModal"><i class="fa fa-file">&nbsp;&nbsp;</i>导入文件</button>
                <button resourceid='352' id="addButton" type="button" class="btn btn-interval btn-primary" onClick="location='detector_insert.php'"><i class="fa fa-plus">&nbsp;&nbsp;</i>新增检查器</button>

            </div>
        </div>

        <div class="row btn-banner">
            <input id="device_id" type="text" class="form-control search-input" placeholder="检测器编号(模糊搜索)">
            <input id="device_ca" type="text" class="form-control search-input btn-interval" placeholder="检测器CA证书序列号(模糊搜索)">
            <input id="adderss" type="text" class="form-control search-input btn-interval" placeholder="部署位置(模糊搜索)">
            <input id="organs" type="text" class="form-control search-input btn-interval" placeholder="部属单位(模糊搜索)">


            <button id="searchButton" type="button" class="btn btn-primary btn-interval2"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>



        </div>

        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="1%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="15%">检测器编号</th>
                    <th width="15%">生产厂商</th>
                    <th width="15%">部署位置</th>
                    <th width="15%">部属单位</th>
                    <th width="15%">操作</th>
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
                    <td colspan="6">
                        <div class="pull-left">

                            <button class="btn btn-default btn-sm" id="refresh">刷新</button>
                            <button resourceid="413" class="btn btn-default btn-sm" id="delete">删除</button>
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
                    导入文件
                </h4>
            </div>
            <div class="modal-body">

                <div>
                    <p style="border:solid 1px #E3E3E3"><input type="file" id="upfile" ></p>
                    <p style="text-align:center">
                        <input type="button" id="upJQuery" value="上传文件" class="btn btn-primary" >
                    </p>
                    <div style='color:red;margin-top: 4px;text-align:center'></div>
                    <input id="param" hidden>
                    <input id="file_name" hidden>
                </div>

            </div>

            <div class="modal-footer">
                <button id="add-submit" type="button" class="btn btn-primary">提交</button>
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

<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script>
    buildFrame("menu-detector_info");

    var globalSearchParam = {random:1}
    $(function(){
        globalSearchParam = {random:1}
        //第一次加载分页
        LoadPage(1,globalSearchParam)
    })


    function export_file() {
        //  window.location.href = "detector_detail.php?id=" + id;
        var file_path = "/detector_info/template";
        var file_name = "检测器备案信息导入模板下载.xlsx";

        //window.open("/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+"");

        window.location.href ="/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+"";
        //post('detector_detail.php',{id:id});
    }


    $("#maintable tfoot").on('click', '#delete', function(){
        $('#hintModal').find(".modal-title").html("删除提示框")

        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");

        if(checkboxs.size() == 0){
            alert("请选择删除数据");
            return;
        }

        var content = "<p >将删除<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，请确认</p>"
        $('#hintModal').find(".modal-body").html(content);

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
            console.log("carray:"+carray);
            $.ajax({
                url: "/ajax_action_detector.php?uu=detector_info.delete",
                type: "post",
                data: {id:JSON.stringify(carray)},
                success:function(data) {
                    var ret = JSON.parse(data);
                    alert(ret['msg']);
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
    });*/
    function fail(status,id){
        console.log("status:"+status)
        console.log("id:"+id)
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector.detail&id="+id, //ajax请求
            type: "post",
            data:null,
            cache: false,
            success: function(data){
                console.log(data)
                var server = JSON.parse(data);
                var msg = server.msg;
                if (status == 3){
                    $("#fail-reason").html("审核未通过:"+msg.register_message)
                }else if(status == 4){
                    $("#fail-reason").html("认证未通过:"+msg.message)
                }
            }
        });
        //
    }
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
            var row = _row.clone();
            row.attr("id",msgListObj[i].id);
            // var operatehtml = getStrManipulation(msgListObj[i].warning_type, msgListObj[i].id);
            var operatehtml = getStrManipulation(msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+ ">")
            row.find("td:eq(1)").text(msgListObj[i].device_id);
            row.find("td:eq(2)").text(contractorMap[msgListObj[i].device_id.substring(4, 6)]);
            row.find("td:eq(3)").text(msgListObj[i].address);
            row.find("td:eq(4)").text(msgListObj[i].organs);
            row.find("td:eq(5)").html(operatehtml);
            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }
    function getStrManipulation(id) {
              return "<a href=\"javascript:void(0);\" class=\"fa fa-bars\" onclick=\"detail(" + id + ")\"> 详情</a>"+" <label>|</label>"+"<a href=\"javascript:void(0);\"class=\"fa fa-refresh\" onclick=\"modify(" + id + ")\">修改</a>"

    }
    function detail(id) {//查看详情
        //  window.location.href = "detector_detail.php?id=" + id;
        window.open("detector_insert.php?id=" + id+"&is_r=1");
        //post('detector_detail.php',{id:id});
    }

    function modify(id) {//查看详情
        //  window.location.href = "detector_detail.php?id=" + id;
        window.open("detector_insert.php?id=" + id);

        //post('detector_detail.php',{id:id});
    }

    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/ajax_action_detector.php?uu=detector_info.count",
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
                pagination(ret,"/ajax_action_detector.php?uu=detector_info.show&p_size="+p_size,parseInt(currentPage),searchParam)
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
        var device_id =  $("#device_id").val();
        var device_ca =  $("#device_ca").val();
        var adderss =  $("#adderss").val();
        var organs =  $("#organs").val();





        globalSearchParam = {random:1}

        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
        }
        if(device_ca!=""){
            globalSearchParam["device_ca"] = device_ca
        }
        if(adderss!=""){
            globalSearchParam["adderss"] = adderss
        }
        if(organs!=""){
            globalSearchParam["organs"] = organs
        }

        LoadPage(1,globalSearchParam)
    })

    $("#clearButton").click(function(){

        $("#device_id").val("");
        $("#device_ca").val("");
        $("#adderss").val("");
        $("#organs").val("");
    })

    upload("detector_info.fileupload", "#upJQuery","#upfile","#param","#file_name");



    $("#add-submit").click(function(){

        var param =  $("#param").attr("value")

        var issuedParam = {random:1}

        if(param!=undefined && param!=""){
            issuedParam["param"] = param
        }else{
                alert("请选择上传文件并点上传按钮")
                return;

        }




        $.ajax({
            url: "/ajax_action_detector.php?uu=detector_info.import",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert(ret.msg);
                    // alert("导入成功");
                    //$("#issuedButton").prop('disabled',"true");
                    refresh()
                }else{
                    alert("导入失败：" + ret.msg);
                }
            },
            error: function () {
                alert("无法连接服务器");
            }
        })



        $("#addModal").modal('hide');
    })











</script>

</body>
</html>