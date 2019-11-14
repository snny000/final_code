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
    <title>命令下发</title>
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


        .checkbox {
            display: inline
        }

        #cmdPanel{
            margin-right: 15px;
        }
        #cmdPanel .panel-primary, #cmdPanel .panel-heading {
            border-radius: 0;
            margin-bottom: 0;
        }
        .step{
            display: inline-block;
            min-width: 10px;
            padding: 5px;
            font-size: 12px;
            font-weight: bold;
            line-height: 1;
            color: #ffffff;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            background-color: orange;
            border-radius: 10px;
        }
        .step:hover{
            color:#000;
            text-decoration:none;
        }

        .step2 .panel-body{
            display: flex;
            justify-content: space-around;
        }

        .step2 .panel-body>div{
            width: 49%;
            border: 1px solid #dddddd;
            
        }
        .step2 li{
            list-style: none;
            margin: 10px;
        }
    </style>
</head>
<body>
<div id="whole-wrapper">
    <div class="row nav_margin">
    <div class="row btn-banner upper-line"></div>
    <div class="row">
        <div  class="pull-left margin_ddos1">
            <h4><span class="tab_color">|</span>&nbsp;&nbsp;命令下发</h4>
        </div>

    </div>


    <div class="container-whole" id="cmdPanel">
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title" style="text-align:center">
                    <a data-toggle="collapse" data-parent="#accordion" class="" >①选择检测器</a>
                    <a class="step pull-right" onclick="showStep(1)">
                        下一步&nbsp;&nbsp;<i class="fa fa-arrow-circle-right"></i></a>
                </h3>
            </div>
            <div id="basePanel" class="panel-collapse in" style="height: auto;">
                <div class="panel-body">
                    <div>
                        <div class="dropdown dropdown-inline btn-interval2">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="contractor" class="pull-left" value="00">所有厂商</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                        <?php
                                        require_once(dirname(__FILE__) . '/require_contractor_list_for_all_page.php');
                                        ?>
                                    </ul>
                                </div>

                                <div class="dropdown btn-interval dropdown-inline">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="address_code" class="pull-left" value="0">所有位置</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                        <li onclick="selectProtoFwd(this);" value="0">所有位置</li>
                                        <li onclick="selectProtoFwd(this);" value="100000">北京</li>
                                        <li onclick="selectProtoFwd(this);" value="200000">上海</li>
                                        <li onclick="selectProtoFwd(this);" value="510000">广州</li>
                                    </ul>
                                </div>                  
                                <div class="dropdown dropdown-inline btn-interval">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="start_module" class="pull-left" value="0">所有开启模块</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                        <li onclick="selectProtoFwd(this);" value="0">所有开启模块</li>
                                        <li onclick="selectProtoFwd(this);" value="1">攻击窃密</li>
                                        <li onclick="selectProtoFwd(this);" value="2">未知攻击</li>
                                        <li onclick="selectProtoFwd(this);" value="3">违规泄密</li>
                                        <li onclick="selectProtoFwd(this);" value="4">目标侦听</li>
                                        <li onclick="selectProtoFwd(this);" value="5">网络行为审计</li>
                                        <li onclick="selectProtoFwd(this);" value="6">通信阻断</li>
                                    </ul>
                                </div>

                                <div class="dropdown btn-interval dropdown-inline">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="stop_module" class="pull-left" value="0">所有关闭模块</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                        <li onclick="selectProtoFwd(this);" value="0">所有关闭模块</li>
                                        <li onclick="selectProtoFwd(this);" value="1">攻击窃密</li>
                                        <li onclick="selectProtoFwd(this);" value="2">未知攻击</li>
                                        <li onclick="selectProtoFwd(this);" value="3">违规泄密</li>
                                        <li onclick="selectProtoFwd(this);" value="4">目标侦听</li>
                                        <li onclick="selectProtoFwd(this);" value="5">网络行为审计</li>
                                         <li onclick="selectProtoFwd(this);" value="6">通信阻断</li>
                                    </ul>
                                </div>
                                <input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器ID(模糊搜索)">
                                <button id="searchButton" type="button" class="btn btn-primary btn-interval2"><i class="fa fa-search">&nbsp;&nbsp;</i>查询</button>
                                <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>
                    </div>
                    <div>
                        <?php
                            require_once(dirname(__FILE__) . '/require_detector_list_for_cmd_page.php');
                            ?>
                    </div> 
                </div>
            </div>
        </div>

        <div class="panel panel-primary" style="display:none">
                    <div class="panel-heading">
                        <h3 class="panel-title" style="text-align:center">
                            <a class="step pull-left" style="background-color:orange;" onclick="showStep(0)">
                                <i class="fa fa-arrow-circle-left">&nbsp;&nbsp;</i>上一步</a>
                            <a data-toggle="collapse" data-parent="#accordion" class="">②命令配置</a>
                            <a resourceid='409' id="issuedButton" class="step pull-right" style="background-color:orange;">
                                <i class="fa fa-check">&nbsp;&nbsp;</i>下发</a>
                        </h3>
                    </div>
                    <div class="panel-collapse in step2" style="height: auto;">
                        <div class="panel-body">
                            <div>
                                <ul>
                                    <li>
                                        <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="1">关机</button>
                                    </li>
                                    <li>
                                        <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="2">重启</button>
                                    </li>
                                    <li>
                                    <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="3">模块启动</button>
                                    </li>
                                    <li>
                                    <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="4">模块关闭</button>                                    
                                    </li>
                                    <li>
                                    <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="5">时间同步</button>
                                    </li>
                                    <li>
                                    <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="6">固件升级</button>
                                    </li>
                                    <li>
                                    <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="7">版本一致性检查</button>
                                    </li>
                                    <li>
                                    <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="8">内置策略更新</button>
                                    </li>
                                    <li>
                                    <button id="" type="button" class="btn btn-primary nav_interval nav-btn cmdsingle" value="9">本地WEB管理用户密码重置</button>
                                    </li>
                                </ul>
                                <span id="cmd" value="0"></span>
                            </div>
                            <div>
                                <div class="dropdown dropdown-menu-width order_hide" hidden style="margin:0 auto;margin-top:10px">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width "
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="cmd_module" class="pull-left" value="0">请选择模块</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                        <li onclick="selectProtoFwd(this);alterChkItem(0);" value="0">请选择模块</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem(1);" value="1">攻击窃密</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem(2);" value="2">未知攻击</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem(3);" value="3">违规泄密</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem(4);" value="4">目标侦听</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem(5);" value="5">网络行为审计</li>
                                    </ul>
                                </div>
                                
                                <div class="dropdown dropdown-menu-width order_hide" hidden style="margin:0 auto;margin-top:10px">
                                    <button type="button" data-toggle="dropdown"
                                            class="btn dropdown-btn dropdown-menu-width "
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                        <span id="version_check_method" class="pull-left" value="0">请选择检查方法</span>
                                        <i class="fa fa-sort-down pull-right"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                        <li onclick="selectProtoFwd(this);alterChkItem1(0);" value="0">请选择检查方法</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem1(1);" value="1">读取文件</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem1(2);" value="2">读取目录</li>
                                        <li onclick="selectProtoFwd(this);alterChkItem1(3);" value="3">MD5值检测</li>
                                    </ul>
                                </div>

                            <div class="widget-group-center order_hide" style="width: 270px" hidden>
                                <p style="border:solid 1px #E3E3E3"><input type="file" id="upfile" ></p>
                                <p style="text-align:center">
                                    <input type="button" id="upJQuery" value="上传文件" class="btn btn-primary" >
                                </p>
                                <div style='color:red;margin-top: 4px;text-align:center'></div>
                                <input id="param" hidden>
                                <input id="file_name" hidden>
                            </div>
                            <div class="row" style="text-align: center">
                                <div class="order_hide" style="margin-top: 10px;" hidden>


                                    <input name="chkItem" type="checkbox" class='checkbox' id="s1" value="1"/><label
                                        for="s1">木马攻击检测</label>
                                    <input name="chkItem" type="checkbox" class='checkbox' id="s2" value="2"/><label
                                        for="s2">漏洞利用检测</label>

                                    <input name="chkItem" type="checkbox" class='checkbox' id="s3" value="3"/><label
                                        for="s3">恶意程序检测</label>
                                    <input name="chkItem" type="checkbox" class='checkbox' id="s4" value="4"/><label
                                        for="s4">其他攻击窃密检测</label>


                                </div>
                            </div>


                            <div class="row" style="text-align: center">
                                <div class="order_hide" style="margin-top: 10px;" hidden>

                                    <input name="chkItem" type="checkbox" class='checkbox' id="s5" value="5"/><label
                                        for="s5">未知攻击</label>
                                </div>
                            </div>
                            <div class="row" style="text-align: center">
                                <div class="order_hide" style="margin-top: 10px;" hidden>
                                    <div>
                                        <input name="chkItem" type="checkbox" class='checkbox' id="s6" value="6"/><label
                                            for="s6">密标文件检测</label>
                                        <input name="chkItem" type="checkbox" class='checkbox' id="s7" value="7"/><label
                                            for="s7">标密文件检测</label>
                                        <input name="chkItem" type="checkbox" class='checkbox' id="s8" value="8"/><label
                                            for="s8">关键字检测</label>
                                    </div>
                                    <div>
                                        <input name="chkItem" type="checkbox" class='checkbox' id="s9" value="9"/><label
                                            for="s9">加密文件检测</label>
                                        <input name="chkItem" type="checkbox" class='checkbox' id="s10" value="10"/><label
                                            for="s10">压缩文件检测</label>
                                        <input name="chkItem" type="checkbox" class='checkbox' id="s11" value="11"/><label
                                            for="s11">图片筛选</label>
                                        <input name="chkItem" type="checkbox" class='checkbox' id="s12" value="12"/><label
                                            for="s12">版式检测</label>
                                    </div>
                                </div>
                            </div>

                            <div class="row" style="text-align: center">
                                <div class="order_hide" style="margin-top: 10px;" hidden>

                                    <input name="chkItem" type="checkbox" class='checkbox' id="s13" value="13"/><label
                                        for="s13">IP审计</label>
                                    <input name="chkItem" type="checkbox" class='checkbox' id="s14" value="14"/><label
                                        for="s14">域名审计</label>

                                    <input name="chkItem" type="checkbox" class='checkbox' id="s15" value="15"/><label
                                        for="s15">URL审计</label>
                                    <input name="chkItem" type="checkbox" class='checkbox' id="s16" value="16"/><label
                                        for="s16">账号审计</label>
                                </div>
                            </div>
                            <div class="row" style="text-align: center">
                                <div class="order_hide" style="margin-top: 10px;" hidden>
                                    <input name="chkItem" type="checkbox" class='checkbox' id="s17" value="17"/><label
                                        for="s17">通联关系审计</label>
                                    <input name="chkItem" type="checkbox" class='checkbox' id="s18" value="18"/><label
                                        for="s18">应用行为审计</label>
                                </div>
                            </div>

                            <div class="row" style="text-align: center">
                                <div class="order_hide" style="margin-top: 10px;" hidden>
                                    <input id="user" type="text" class="form-control search-input btn-interval" placeholder="需要重置的用户名">
                                    <input id="passwd" type="password" class="form-control search-input btn-interval" placeholder="重置的新密码">
                                </div>

                                <div class="row" style="text-align: center">
                                    <div class="order_hide" style="margin-top: 10px;" hidden>
                                        <input name="new" id="filename" type="text" class="form-control search-input btn-interval" placeholder="检查文件名">
                                        <input name="new" id="offset" type="text" class="form-control search-input btn-interval" placeholder="读取的开始偏移">
                                        <input name="new" id="length" type="text" class="form-control search-input btn-interval" placeholder="读取长度">
                                    </div>
                                </div>
                                <div class="row" style="text-align: center">
                                    <div class="order_hide" style="margin-top: 10px;" hidden>
                                        <input name="new" id="path" type="text" class="form-control search-input btn-interval" placeholder="检查文件完整路径">
                                        <input name="new" id="result" type="text" class="form-control search-input btn-interval" placeholder="正确结果">

                                    </div>
                                </div>
                            </div>
                                
                            </div>
                        </div>
                    </div>
                </div>
        
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
    buildFrame("menu-order1");
    $(function () {
        console.log("执行js");

        //隐藏所有的命令
        //$(".order_hide").hide();
    });

    var globalSearchParam = {random:1,device_status:1}
    LoadPage(1,globalSearchParam)

    var globalSelectedDetetors = {}


    function clearChkItem(){

        $("[name = chkItem]:checkbox").prop("checked", false);

    }





    function alterChkItem(id){

        clearChkItem();

        $(".order_hide").hide();
        $(".order_hide:eq(0)").show();
        //////分类可见
        if(id ==0) {

        }else if(id ==1){
          //  $(".order_hide").hide();
        //    $(".order_hide:eq(0)").show();
            $(".order_hide:eq(3)").show();

        }
        else if(id ==2){
         //   $(".order_hide").hide();
         //   $(".order_hide:eq(0)").show();
            $(".order_hide:eq(4)").show();

        }
        else if(id ==3){
         //   $(".order_hide").hide();
        //    $(".order_hide:eq(0)").show();
            $(".order_hide:eq(5)").show();

        }
        else if(id ==4){
        //    $(".order_hide").hide();
         //   $(".order_hide:eq(0)").show();
            $(".order_hide:eq(6)").show();

        }
        else if(id ==5){
          //  $(".order_hide").hide();
          //  $(".order_hide:eq(0)").show();
            $(".order_hide:eq(7)").show();
/*            $("[id = 5]:checkbox").show()
            $("[id = 5]:checkbox").next().show()*/
        }

    }
    function alterChkItem1(id){

        $("#filename").val("");
        $("#offset").val("");
        $("#length").val("");
        $("#path").val("");
        $("#result").val("");
        $(".order_hide").hide();
        $(".order_hide:eq(1)").show();
        //////分类可见
        if(id ==0) {

        }else if(id ==1){
            $(".order_hide:eq(9)").show();
            $(".order_hide:eq(2)").show();

        }
        else if(id ==2){
            $(".order_hide:eq(10)").show();
        }
        else if(id ==3){
            $(".order_hide:eq(9)").show();
            $(".order_hide:eq(2)").show();

        }

    }



    $(".cmdsingle").click(function(){

        $('.cmdsingle').removeClass("active");
        $(this).addClass("active");
        $("#cmd").attr("value",$(this).attr("value"))
        //清除所有已选得项
        firstSelect("cmd_module");
        firstSelect("version_check_method");
        $("#user").val("");
        $("#passwd").val("");

        $("#filename").val("");
        $("#offset").val("");
        $("#length").val("");
        $("#path").val("");
        $("#result").val("");
        clearChkItem();

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

        }else if(id == "6" || id=="8") {
            $(".order_hide").hide();
            $(".order_hide:eq(2)").show();
        }
        else if(id == "9"){
                $(".order_hide").hide();
                $(".order_hide:eq(8)").show();
        }else{
            $(".order_hide").hide();
        }
    })




//    $('.cmdsingle').click(function () {
////        $(this).siblings().removeClass("active");
//        $('.cmdsingle').removeClass("active");
//        $(this).addClass("active");
//        $("#cmd").attr("value",$(this).attr("value"))
//    })


    $("#searchButton").click(function(){

        if(($("#start_module").attr("value") == $("#stop_module").attr("value"))&&
            $("#start_module").attr("value")!=0 && $("#stop_module").attr("value")!=0){
            alert("开启模块和关闭模块不能相同");
            return;
        }

        // 取消下发按钮的disable
        //$("#issuedButton").removeAttr("disabled");

        var device_id =  $("#device_id").val();
        var contractor = $("#contractor").attr("value").toString()
        var address_code = $("#address_code").attr("value").toString()
        var start_module = $("#start_module").attr("value").toString()
        var stop_module = $("#stop_module").attr("value").toString()

        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        //globalSearchParam = {random:1,device_status:1}
        globalSearchParam = {random:1,device_status:1}
        if(contractor!="00"){
            globalSearchParam["contractor"] = contractor
        }
        if(address_code!="0"){
            globalSearchParam["address_code"] = address_code
        }
        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
        }
        if(start_module!="0"){
            globalSearchParam["start_module"] = start_module
        }
        if(stop_module!="0"){
            globalSearchParam["stop_module"] = stop_module
        }
        LoadPage(1,globalSearchParam)
    })



    $("#clearButton").click(function(){
        firstSelect("contractor");
        firstSelect("address_code");
        firstSelect("start_module");
        firstSelect("stop_module");
        $("#device_id").val("");
    })

        upload("cmd.fileupload", "#upJQuery","#upfile","#param","#file_name");

    $("#issuedButton").click(function(){
        var cmd_type_map={1:'关机',2:'重启',3:'模块启动',4:'模块关闭',5:'时间同步',
            6:'固件升级',7:'版本一致性检查',8:'内置策略更新',9:'本地WEB管理用户密码重置'}

        var cmd_module =  $("#cmd_module").attr("value").toString()
        var version_check_method =  $("#version_check_method").attr("value").toString()
        var param =  $("#param").attr("value")
        var cmd =  $("#cmd").attr("value").toString()
        var user =  $("#user").val();
        var passwd =  $("#passwd").val();

        //校验判断
        var error_str = ""

        var checkboxs =$("[name = chkItem]:checkbox:checked")
      //alert(checkboxs.size());

        if(cmd=="0"){
            error_str+="请选择命令\n";
        }else if((cmd=="3"&&cmd_module=="0")||(cmd=="4"&&cmd_module=="0")){
            error_str+="请选择模块\n";
        }else if((cmd=="3"&&checkboxs.size()==0)||(cmd=="4"&&checkboxs.size()==0)){
            error_str+="请选择子模块\n";
        }else if(cmd=="7"&&version_check_method=="0"){
            error_str+="请选择检查方法\n";
        }
        else if(cmd=="7"&&version_check_method=="1"){
        if ((($("#filename").val()=="" ||$("#offset").val()=="" )|| $("#length").val()=="" )||(param==undefined || param==""))
        {
            if(($("#filename").val()=="" ||$("#offset").val()=="" )|| $("#length").val()==""){
            error_str+="请填写相应的参数\n";
        }
           else if(param==undefined || param=="")
            {
                error_str+="请上传文件\n";
            }

        }
        }
        else if(cmd=="7"&&version_check_method=="2"){
            if ( $("#path").val()=="" )
            {
                error_str+="请填写相应的参数\n";
            }
            if ( $("#result").val()=="" )
            {
                error_str+="请填写相应的参数\n";
            }
        }
        else if(cmd=="7"&&version_check_method=="3"){
            if ((($("#filename").val()=="" ||$("#offset").val()=="" )|| $("#length").val()=="" )||(param==undefined || param==""))
            {
                if(($("#filename").val()=="" ||$("#offset").val()=="" )|| $("#length").val()==""){
                    error_str+="请填写相应的参数\n";
                }
                else if(param==undefined || param=="")
                {
                    error_str+="请上传文件\n";
                }

            }
        }
        else if((cmd=="6"||cmd=="8")&&(param==undefined || param=="")){
            //console.log("请上传文件")
            error_str+="请上传文件\n";
        }
        else if ((cmd=="9"&&user=="")||(cmd=="9"&&passwd=="")) {
            error_str += "请输入用户名和新密码\n";
        }

/*        if($("#totalcount").text() == "0"){
            error_str+="下发的检测器数量不能为0\n";
        }
        if(($("#start_module").attr("value") == $("#stop_module").attr("value"))&&
            $("#start_module").attr("value")!=0 && $("#stop_module").attr("value")!=0){
            error_str+="开启模块和关闭模块不能相同\n";
        }*/
        //input.container-right[placeholder]

        $(".container-right input[placeholder]").each(function(){
            var value = $(this).val(); //这里的value就是每一个input的value值~

            if(!value.match(/^[\u4E00-\u9FA5a-zA-Z0-9_\.\/]{0,}$/)){


                var label = $(this).attr('placeholder')



                //var label = $(this).prev("span").text()

                error_str+=label+"存在非法字符\n";


            }

        });




        ///构造id_list
        var carray =new Array()
        for (var key in globalSelectedDetetors){
//            carray.push(parseInt(key))
            carray.push(parseInt(globalSelectedDetetors[key]))
        }
        console.log(carray.length)

        if(carray.length==0){

            error_str+="下发的检测器数量不能为0\n";

        }







        if(error_str!=""){
            alert(error_str);
        }else{
            $('#hintModal p:eq(1)').html("选择的命令是："+cmd_type_map[cmd]);
            //$('#hintModal p:eq(2)').html("下发的检测器个数："+$("#totalcount").text());
            $('#hintModal p:eq(2)').html("下发的检测器个数："+carray.length);


            $('#hintModal').modal('show')
        }
    })

    $("#issueSubmit").click(function(){

        var cmd_module =  $("#cmd_module").attr("value").toString()
        var version_check_method =  $("#version_check_method").attr("value").toString()
        var param =  $("#param").attr("value")
        var cmd =  $("#cmd").attr("value").toString()
        var user =  $("#user").val();
        var passwd =  $("#passwd").val();

        var input_filename =  $("#filename").val(); //版本一致性检查时人工输入的绝对路径文件
        var filename =  $("#file_name").attr('value'); //上传的文件的原始文件名
        var offset =  $("#offset").val();
        var length =  $("#length").val();
        var path =  $("#path").val();
        var result =  $("#result").val();
        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        issuedParam = {random:1}
        if(cmd!="0"){
            issuedParam["cmd"] = cmd
        }
        if(cmd_module!="0"){
            issuedParam["cmd_module"] = cmd_module
        }

        var checkboxs =$("[name = chkItem]:checkbox:checked")
        if(cmd_module!="0" && checkboxs.size()>0){
            var carray_submodule =new Array()
            checkboxs.each(function(){
                carray_submodule.push(parseInt($(this).attr("value")))
            })

            issuedParam["submodule"] = JSON.stringify(carray_submodule);
        }

        if(version_check_method!="0"){
            if(version_check_method=="1"){
                issuedParam["input_filename"] = input_filename
                issuedParam["offset"] = offset
                issuedParam["length"] = length
            }
            if(version_check_method=="2"){

                issuedParam["path"] = path
                issuedParam["result"] = result
            }
            if(version_check_method=="3"){
                issuedParam["input_filename"] =input_filename
                issuedParam["offset"] = offset
                issuedParam["length"] = length
            }
            issuedParam["version_check_method"] = version_check_method
        }
        if(param!=undefined && param!=""){
            issuedParam["param"] = param
            issuedParam["filename"] = filename
        }
        if(user!=""){
            issuedParam["user"] = user
        }
        if(passwd!=""){
            issuedParam["passwd"] = passwd
        }

        ///构造id_list
        var carray =new Array()
        for (var key in globalSelectedDetetors){
//            carray.push(parseInt(key))
            carray.push(parseInt(globalSelectedDetetors[key]))
        }
        issuedParam["id_list"] = JSON.stringify(carray)






        $.ajax({
            url: "/ajax_action_detector.php?uu=cmd.sync",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert("命令下发成功");
                    refresh();
                    //$("#issuedButton").prop('disabled',"true");
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

    function showStep(step){
        if(step == 1){
            ///构造id_list
            var carray =new Array()
            for (var key in globalSelectedDetetors){
                carray.push(parseInt(key))
            }
            console.log(carray.length)

            if(carray.length==0){

                alert("下发的检测器数量不能为0");
                return;
            }
        }
        $('#cmdPanel .panel').hide();
        $('#cmdPanel .panel').eq(step).show();

        
    }

</script>
</body>
</html>

