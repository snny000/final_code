<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

//$id = $_REQUEST["id"];

?>

<!DOCTYPE html>
<html>
<head>
    <title>插件命令管理</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

   <!-- <link href="default/css/new.css" rel="stylesheet">
         <link href="default/css/charts-graphs.css" rel="stylesheet">
   -->

     <!-- Datepicker CSS -->
    <!--
    <link rel="stylesheet" type="text/css" href="default/css/datepicker.css">
    <link href="default/fonts/font-awesome.min.css" rel="stylesheet">
    -->

    <!-- HTML5 shiv and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
    <script src="default/js/html5shiv.js"></script>
    <script src="default/js/respond.min.js"></script>
    <![endif]-->

    <link href="css/server.css" rel="stylesheet">
    <link href="css/detector.css" rel="stylesheet">
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="css/frame.css" rel="stylesheet">
    <link href="css/product.css" rel="stylesheet">
   <!-- <link href="css/fileinput.min.css" rel="stylesheet">-->
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">

    <style>
        body {
            background-color: white;
        }

        .widget-center .dropdown{
            margin: 0 auto;
            /*margin-top:20px;*/
            margin-top:10px;
            margin-bottom:5px;
        }

        .widget-center{
            /*margin-top: 20px;*/
        }

        .widget-group-center{
            margin: 0 auto;
            margin-top:5px;
            margin-bottom: 5px;

        }

        .widget-border{
            border: solid 1px #E3E3E3
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
    </style>
</head>
<body>
<div id="whole-wrapper">
    <div class="row nav_margin">


    <div class="row btn-banner upper-line"></div>
    <div class="row">
        <div  class="pull-left margin_ddos1">
            <h4><span class="tab_color">|</span>&nbsp;&nbsp;插件命令管理</h4>
        </div>

    </div>



    <div class="container-whole">
        <!--   <div class="container-left"> -->
            <div class="row">
                <div class="col-lg-12 col-md-12" style="width: 98%;">
                    <div class="widget no-margin widget-border"  style="height: 150px;margin-bottom: 20px;">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                插件
                            </div>
                        </div>
                        <div class="widget-center" >
                            <div class="row" style="margin-left: 10px"> <!-- style="text-align: center"-->
                                <div class="" style="margin-top: 10px">
                                    <input id="plug_id" type="text" class="form-control search-input btn-interval" placeholder="插件ID">

                                    <div class="dropdown btn-interval dropdown-inline"style="margin-left: 9px">
                                        <button type="button" data-toggle="dropdown"
                                                class="btn dropdown-btn dropdown-menu-width"
                                                aria-haspopup="true"
                                                aria-expanded="false">
                                            <span id="cmd" class="pull-left" value="-1">未选择</span>
                                            <i class="fa fa-sort-down pull-right"></i>
                                        </button>
                                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                            <li onclick="selectProtoFwd(this);" value="-1">未选择</li>
                                            <li onclick="selectProtoFwd(this);" value="1">启动</li>
                                            <li onclick="selectProtoFwd(this);" value="2">停止</li>
                                            <li onclick="selectProtoFwd(this);" value="3">删除</li>
                                        </ul>
                                    </div>
                                </div>

<!--                                <div class="" style="margin-top: 10px">-->
<!--                                </div>-->
                            </div>
                        </div>
                    </div>

                </div>

            </div> <!-- row -->
            <!--  </div>  --> <!-- container-left -->
        <div class="container-right">

        </div>
    </div>

    <div class="clearfix"></div>

        <?php
        require_once(dirname(__FILE__) . '/require_detector_filter_for_cmd_page.php');
        ?>

        <?php
        require_once(dirname(__FILE__) . '/require_detector_list_for_cmd_page.php');
        ?>


    <div  class="container-whole" style="text-align: center" >
        <div style="color:red;margin-bottom: 10px">请先选择插件命令，再选择检测器，才能进行命令下发</div>
        <button id="issuedButton" type="button" class="btn btn-lg btn-primary" disabled><i class="fa fa-sign-out">&nbsp;&nbsp;</i>下发</button>
        <!--  data-toggle="modal" data-target="#hintModal" -->
    </div>

</div>

<div class="modal fade" id="hintModal" tabindex="-1" role="dialog" aria-labelledby="hintLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    命令下发确认
                </h4>
            </div>
            <div class="modal-body" style="text-align: center">
                <p style="color: red">请确认是否下发命令</p>
                <p></p>
                <p></p>
            </div>
            <div class="modal-footer">
                <button id="issueSubmit" type="button" class="btn btn-primary">确定</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
    </div><!-- /.modal -->
</div>


<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>

    <script src="js/common.js"></script>
<!--<script src="js/fileinput.min.js"></script>-->
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="js/cmd_common.js"></script>

<script type="text/javascript">
    buildFrame("menu-plug2");
    $(function () {
        console.log("执行js");

        //隐藏所有的命令
        //$(".order_hide").hide();
    });

    var globalSearchParam = {random:1}

    var globalSelectedDetetors = {}

/*    $(".cmdsingle").click(function(){

        $('.cmdsingle').removeClass("active");
        $(this).addClass("active");
        $("#cmd").attr("value",$(this).attr("value"))
        //清除所有已选得项
        firstSelect("cmd_module");
        firstSelect("version_check_method");

        //////////////////// 将上传组件的所有东西清空
        $("#upJQuery").removeAttr('disabled');
        $("#upJQuery").parent().next().html("");
        $("#upfile").val("");
        $("#param").attr("value","");
        /////////////////////

        var id  = $("#cmd").attr("value")
        console.log("****id:"+id)
        if(id == "3" || id == "4"){
            $(".order_hide").hide();
            $(".order_hide:eq(0)").show();
        }else if(id == "7"){
            $(".order_hide").hide();
            $(".order_hide:eq(1)").show();
        }else if(id == "6" || id=="8"){
            $(".order_hide").hide();
            $(".order_hide:eq(2)").show();
        }else{
            $(".order_hide").hide();
        }
    })*/



    $('button.condition-btn.singlechoose').click(function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
        console.log($(this).attr("value"))

    })



//    $('.cmdsingle').click(function () {
////        $(this).siblings().removeClass("active");
//        $('.cmdsingle').removeClass("active");
//        $(this).addClass("active");
//        $("#cmd").attr("value",$(this).attr("value"))
//    })


    $("#searchButton").click(function(){

/*        if(($("#start_module").attr("value") == $("#stop_module").attr("value"))&&
            $("#start_module").attr("value")!=0 && $("#stop_module").attr("value")!=0){
            alert("开启模块和关闭模块不能相同");
            return;
        }*/

        // 取消下发按钮的disable
        $("#issuedButton").removeAttr("disabled");

        var device_id =  $("#device_id").val();
        var organs =  $("#organs").val();
        // var rct = $("#select_verify").attr("value")
        // var ison = $("#select_isonline").attr("value")
        var contractor = $("#contractor").attr("value").toString()
        var address_code = $("#address_code").attr("value").toString()
        var device_status = $("#device_status").attr("value").toString()

        //alert(device_status)

        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        globalSearchParam = {random:1}
        if(contractor!="00"){
            globalSearchParam["contractor"] = contractor
        }
        if(address_code!="0"){
            globalSearchParam["address_code"] = address_code
        }
        if(device_status!="0"){
            globalSearchParam["device_status"] = device_status
        }

        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
        }
        if(organs!=""){
            globalSearchParam["organs"] = organs
        }
        LoadPage(1,globalSearchParam)
    })



    $("#clearButton").click(function(){
        firstSelect("contractor");
        firstSelect("address_code");
        firstSelect("device_status");
        $("#device_id").val("");
        $("#user").val("");
    })

//    $("#upJQuery1").on('click', function() {
//
//        if($("#upfile1").get(0).files[0]==undefined){
//            $("#upJQuery1").parent().next().html("请选择文件!")
//            return;
//        }
//
//        var fd = new FormData();
//        //fd.append("count", 1);
//        fd.append("upfile", $("#upfile1").get(0).files[0]);
//        console.log("$(#upfile1).get(0).files[0]:"+$("#upfile1").get(0).files[0])
//        $.ajax({
//            url: "ajax_action_upload.php?uu=file.upload",
////                url: "test",
////            url: "http://192.168.120.234/file/upload",
//
//            type: "POST",
////            processData: false,
////            contentType: "multipart/form-data",
//            cache: false,
//            contentType: false,
//            processData: false,
//            data: fd,
//            success: function(d) {
//                //    var data = "{\"msg\":[{\"file_path\":\"/media/test/20161019103825_126367.php\"}],\"code\":200}";
//                console.log("ddddddddd:"+d)
//                var ret = JSON.parse(d);
//                //console.log(ret.msg[0].file_path);
//                //console.log(d);
//                $("#plug_path").attr("value", ret.msg[0].file_path)
//                $("#upJQuery1").parent().next().html("上传成功!")
//                $("#upJQuery1").prop('disabled',"true");
//            }
//        });
//    });
//
//    $("#upfile1").change(function() {
//        $("#upJQuery1").removeAttr('disabled')
//        $("#upJQuery1").parent().next().html("")
//        $("#plug_path").attr("value","");
//    })


 /*   function upload(upJQuery, upfile, param){
        console.log("upJQuery:"+upJQuery)
        console.log("upfile:"+upfile)
        console.log("param:"+param)

        $(upJQuery).on('click', function() {

            if($(upfile).get(0).files[0]==undefined){
                $(upJQuery).parent().next().html("请选择文件!")
                return;
            }

            var fd = new FormData();
            //fd.append("count", 1);
            fd.append("upfile", $(upfile).get(0).files[0]);
            console.log("$(upfile).get(0).files[0]:"+$(upfile).get(0).files[0])
            $.ajax({
                url: "ajax_action_upload.php?uu=file.upload",
//                url: "test",
//            url: "http://192.168.120.234/file/upload",

                type: "POST",
//            processData: false,
//            contentType: "multipart/form-data",
                cache: false,
                contentType: false,
                processData: false,
                data: fd,
                success: function(d) {
                    //    var data = "{\"msg\":[{\"file_path\":\"/media/test/20161019103825_126367.php\"}],\"code\":200}";
                    console.log(d)
                    var ret = JSON.parse(d);

                    $(param).attr("value", ret.msg[0].file_path)

                    if(ret.code == 200){
                        $(upJQuery).parent().next().html("上传成功!")
                    }else{
                        $(upJQuery).parent().next().html("服务器错误!")
                    }

                    $(upJQuery).prop('disabled',"true");
                },
                beforeSend: function () {
                    $(upJQuery).parent().next().html("上传中......")
                },
                error: function () {
                    $(upJQuery).parent().next().html("")
                    alert("无法连接服务器");
                }
            });
        });

        $(upfile).change(function() {
            $(upJQuery).removeAttr('disabled')
            $(upJQuery).parent().next().html("")
            $(param).attr("value","");
        })
    }*/





    $("#issuedButton").click(function(){
        var plug_id =  $("#plug_id").val();
        var output_path =  $("#output_path").val();;
        var cmd =  $("#cmd").attr("value").toString();
        var plug_path =  $("#plug_path").attr("value")
        var plug_config_path =  $("#plug_config_path").attr("value")


        console.log("plug_path:"+plug_path)
        console.log("plug_config_path:"+plug_config_path)


        //校验判断
        var error_str = ""
/*        if( $("#totalcount").attr("value") == 0){
         error_str+="请先查询检测器\n";
         }*/
        if(cmd==-1){
            error_str+="请选择命令类型\n";
        }
        if(plug_id==""){
            error_str+="请输入插件ID\n";
        }


        //构造id_list
        var carray =new Array()
        for (var key in globalSelectedDetetors){
            carray.push(parseInt(key))
        }
        console.log(carray.length)

        if(carray.length==0){

            error_str+="下发的检测器数量不能为0\n";

        }


        if(error_str!=""){
            alert(error_str);
        }else{
//            $('#hintModal p:eq(1)').html("选择的命令是："+cmd_type_map[cmd]);
            //$('#hintModal p:eq(2)').html("下发的检测器个数："+$("#totalcount").text());
            $('#hintModal p:eq(2)').html("下发的检测器个数："+carray.length);


            $('#hintModal').modal('show')
        }
    })

    $("#issueSubmit").click(function(){
        var plug_id =  $("#plug_id").val();
        var output_path =  $("#output_path").val();
        var cmd = parseInt($("#cmd").attr("value"));
        var plug_path =  $("#plug_path").attr("value");
        var plug_config_path =  $("#plug_config_path").attr("value");

        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        issuedParam = {random:1}
        if(plug_id!=""){
            issuedParam["plug_id"] = plug_id
        }
        if(output_path!=""){
            issuedParam["output_path"] = output_path
        }


        if(cmd!="-1"){
            issuedParam["cmd"] = cmd
        }


        if(plug_path!=""){
            issuedParam["plug_path"] = plug_path
        }
        if(plug_config_path!=""){
            issuedParam["plug_config_path"] = plug_config_path
        }

//        if(param!=undefined && param!=""){
//            issuedParam["param"] = param
//        }

        ///构造id_list
        var carray =new Array()
        for (var key in globalSelectedDetetors){
            carray.push(parseInt(key))
        }
        issuedParam["detector_id_list"] = JSON.stringify(carray)




        $.ajax({
            url: "/ajax_action_detector.php?uu=plug_cmd.sync",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert("命令下发成功");
                    $("#issuedButton").prop('disabled',"true");
                }else{
                    alert("命令下发失败");
                }
            },
            error: function () {
                alert("无法连接服务器");
            }
        })

        $("#hintModal").modal('hide');
    })
    /*
    // issueSubmit
    $("#issuedButton").click(function(){

        var device_id =  $("#device_id").val();
        var contractor = $("#contractor").attr("value").toString()
        var address_code = $("#address_code").attr("value").toString()
        var start_module = $("#start_module").attr("value").toString()
        var stop_module = $("#stop_module").attr("value").toString()
        var cmd_module =  $("#cmd_module").attr("value").toString()
        var version_check_method =  $("#version_check_method").attr("value").toString()
        var param =  $("#param").attr("value")
        var cmd =  $("#cmd").attr("value").toString()






        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        issuedParam = {random:1}
        if(cmd!="0"){
            issuedParam["cmd"] = cmd
        }
        if(contractor!="00"){
            issuedParam["contractor"] = contractor
        }
        if(address_code!="0"){
            issuedParam["address_code"] = address_code
        }
        if(device_id!=""){
            issuedParam["device_id"] = device_id
        }
        if(start_module!="0"){
            issuedParam["start_module"] = start_module
        }
        if(stop_module!="0"){
            issuedParam["stop_module"] = stop_module
        }
        if(cmd_module!="0"){
            issuedParam["cmd_module"] = cmd_module
        }
        if(version_check_method!="0"){
            issuedParam["version_check_method"] = version_check_method
        }
        if(param!=undefined && param!=""){
            issuedParam["param"] = param
        }

        $.ajax({
            url: "/ajax_action_detector.php?uu=cmd.sync",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert("命令下发成功");
                }else{
                    alert("命令下发失败");
                }
            }
        })

    })
    */

</script>
</body>
</html>

