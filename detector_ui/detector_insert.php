<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

//$id = $_REQUEST["id"];


$id = getRequest("id");

$is_r= getRequest("is_r");


?>

<script type="text/javascript">

    var id = "<?php echo $id?>";
    var is_r = "<?php echo $is_r?>";

    if(id==''){

        id=0;

    }
    if(is_r==''){

        is_r=0;
    }

    console.log("id:"+id)

    console.log("is_r:"+is_r)

</script>


<!DOCTYPE html>
<html>
<head>
    <title>检测器信息录入</title>
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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;检测器信息录入</h4>
            </div>

        </div>


        <div class="container-whole">
            <!--   <div class="container-left"> -->
            <div class="row">
                <div class="col-lg-12 col-md-12" style="width: 98%;">
                    <div class="widget no-margin widget-border"  style="height:  auto;margin-bottom: 20px;">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title"></div>
                        </div>
                        <div class="widget-center" >

                            <div id="first" class="row" style="margin-left: 15px"> <!-- style="text-align: center"-->
                                <div  class="" style="margin-top: 10px">
                                    <div class="dropdown-inline">
                                        <span>检测器编号:</span>
                                        <input id="device_id" type="text" class="form-control search-input" placeholder="检测器编号">
                                        <div style="color:red"></div>
                                    </div>

                                    <div class="dropdown-inline">
                                        <span>检测器CA证书序列号:</span>
                                        <input id="device_ca" type="text" class="form-control search-input btn-interval" placeholder="检测器CA证书序列号">
                                        <div style="color:red"></div>
                                    </div>
                                    <div class="dropdown-inline">
                                        <span>内存大小（MB）:</span>
                                        <input id="mem_total" type="text" class="form-control search-input btn-interval" placeholder="内存大小（MB）">
                                        <div style="color:red"></div>
                                    </div>
                                    <div class="dropdown-inline">
                                        <span>软件版本号:</span>
                                        <input id="soft_version" type="text" class="form-control search-input btn-interval" placeholder="软件版本号">
                                        <div style="color:red"></div>
                                    </div>
                                    <div>&nbsp;</div>
                                    <div>
                                        <div class="dropdown btn-interval dropdown-inline">
                                            <button type="button" data-toggle="dropdown"
                                                    class="btn dropdown-btn dropdown-menu-width"
                                                    aria-haspopup="true"
                                                    aria-expanded="false">
                                                <span id="contractor" class="pull-left" value="0">检测器生产产商</span>
                                                <i class="fa fa-sort-down pull-right"></i>
                                            </button>
                                            <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                                <li onclick="selectProtoFwd(this);" value="1">中孚</li>
                                                <li onclick="selectProtoFwd(this);" value="2">蓝盾</li>
                                                <li onclick="selectProtoFwd(this);" value="3">天融信</li>
                                                <li onclick="selectProtoFwd(this);" value="4">鼎普</li>
                                                <li onclick="selectProtoFwd(this);" value="5">网安</li>
                                                <li onclick="selectProtoFwd(this);" value="6">信工所</li>
                                                <li onclick="selectProtoFwd(this);" value="7">网神360</li>
                                                <li onclick="selectProtoFwd(this);" value="8">金城</li>
                                            </ul>
                                        </div>
                                        <div class="dropdown-inline">
                                            <span>检测器部属单位:</span>
                                            <input id="organs" type="text" class="form-control search-input btn-interval" placeholder="检测器部属单位">
                                            <div style="color:red"></div>
                                        </div>
                                        <div class="dropdown-inline">
                                            <span>检测器部署地址:</span>
                                            <input id="address" type="text" class="form-control search-input btn-interval" placeholder="检测器部署地址">
                                            <div style="color:red"></div>
                                        </div>
                                        <div class="dropdown-inline">
                                            <span>行政区域编码:</span>
                                            <input id="address_code" type="text" class="form-control search-input btn-interval" placeholder="行政区域编码">
                                            <div style="color:red"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>


                    <div class="widget no-margin widget-border"  style="height: auto;margin-bottom: 20px;">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                接口信息
                            </div>
                        </div>

                        <div class="widget-center" >
                            <div id="interface" class="row" style="margin-left: 15px"> <!-- style="text-align: center"-->
                                <div  class="" style="margin-top: 10px">
                                    <div class="dropdown-inline">
                                        <span>IP地址:</span>
                                        <input id="ip" type="text" class="form-control search-input" placeholder="IP地址">
                                        <div style="color:red"></div>
                                    </div>

                                    <div class="dropdown-inline">
                                        <span>MAC地址:</span>
                                        <input id="mac" type="text" class="form-control search-input btn-interval" placeholder="MAC地址">
                                        <div style="color:red"></div>
                                    </div>
                                    <div class="dropdown-inline">
                                        <span>子网掩码:</span>
                                        <input id="netmask" type="text" class="form-control search-input btn-interval" placeholder="子网掩码">
                                        <div style="color:red"></div>
                                    </div>

                                    <div class="dropdown-inline">
                                        <span>网关地址:</span>
                                        <input id="gateway" type="text" class="form-control search-input btn-interval" placeholder="网关地址">
                                        <div style="color:red"></div>
                                    </div>
                                    <div class="dropdown btn-interval dropdown-inline">
                                        <button type="button" data-toggle="dropdown"
                                                class="btn dropdown-btn dropdown-menu-width"
                                                aria-haspopup="true"
                                                aria-expanded="false">
                                            <span id="manage" class="pull-left" value="-1">是否为管理口</span>
                                            <i class="fa fa-sort-down pull-right"></i>
                                        </button>
                                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                                            <li onclick="selectProtoFwd(this);" value="-1">是否为管理口</li>
                                            <li onclick="selectProtoFwd(this);" value="1">Ture</li>
                                            <li onclick="selectProtoFwd(this);" value="2">False</li>

                                        </ul>

                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>


                    <div class="widget no-margin widget-border"  style="height:  auto;margin-bottom: 20px;">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                CPU信息
                            </div>
                        </div>

                        <div id="cpuInfoTemplet" hidden>
                            <div name="cpuCell" class="row" style="margin-left: 15px"> <!-- style="text-align: center"-->
                                <div  style="margin-top: 10px">
                                    <div class="dropdown-inline">
                                        <span>CPU编号:</span>
                                        <input name="physical_id" type="text" class="form-control search-input" placeholder="CPU编号">
                                        <div style="color:red"></div>
                                    </div>

                                    <div class="dropdown-inline">
                                        <span>CPU核心数:</span>
                                        <input name="core" type="text" class="form-control search-input btn-interval" placeholder="CPU核心数">
                                        <div style="color:red"></div>
                                    </div>
                                    <div class="dropdown-inline">
                                        <span>CPU主频:</span>
                                        <input name="clock" type="text" class="form-control search-input btn-interval" placeholder="CPU主频">
                                        <div style="color:red"></div>
                                    </div>
                                    <button class="btn btn-link padding_zero" name="delete" onclick="delCpuCell(this)">
                                        <li class="fa fa-cut">&nbsp;</li>删除</button>
                                </div>

                            </div>
                        </div>

                        <div id="cpuInfo" class="widget-center" >

                            <!--  ////动态添加内容-->


                        </div>
                        <div  class="add_div_border">
                            <button class="btn btn-link btn-sm " id="add_div1">
                                <img width="20px" height="20px" src="images/add.png">
                                添加
                            </button>
                        </div>

                    </div>

                    <div class="widget no-margin widget-border"  style="height:  auto;margin-bottom: 20px;">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                磁盘信息
                            </div>
                        </div>
                        <div id="diskInfoTemplet" class="widget-center" hidden >
                            <div name="diskCell" class="row" style="margin-left: 15px"> <!-- style="text-align: center"-->
                                <div class="" style="margin-top: 10px">
                                    <div class="dropdown-inline">
                                        <span>磁盘序列号:</span>
                                        <input name ="serial" type="text" class="form-control search-input" placeholder="磁盘序列号">
                                        <div style="color:red"></div>
                                    </div>

                                    <div class="dropdown-inline">
                                        <span>磁盘大小(GB):</span>
                                        <input name ="size" type="text" class="form-control search-input btn-interval" placeholder="磁盘大小(GB)">
                                        <div style="color:red"></div>
                                    </div>

                                    <button class="btn btn-link padding_zero" name="delete" onclick="delCpuCell(this)">
                                        <li class="fa fa-cut">&nbsp;</li>删除</button>

                                </div>
                            </div>

                        </div>

                        <div id="diskInfo" class="widget-center" >

                            <!--  ////动态添加内容-->


                        </div>
                        <div  class="add_div_border">
                            <button class="btn btn-link btn-sm " id="add_div2">
                                <img width="20px" height="20px" src="images/add.png">
                                添加
                            </button>
                        </div>
                    </div>

                    <div class="widget no-margin widget-border"  style="height:  auto;margin-bottom: 20px;">
                        <div class="widget-header widget-header-index">
                            <div class="title widget-header-index-title">
                                客户单位联系人信息
                            </div>
                        </div>
                        <div id="contactTemplet" class="widget-center" hidden >
                            <div name="contactCell" class="row" style="margin-left: 15px"> <!-- style="text-align: center"-->
                                <div class="" style="margin-top: 10px">
                                    <div class="dropdown-inline">
                                        <span>姓名:</span>
                                        <input name="name" type="text" class="form-control search-input" placeholder="姓名">
                                        <div style="color:red"></div>
                                    </div>

                                    <div class="dropdown-inline">
                                        <span>工作:</span>
                                        <input name="position" type="text" class="form-control search-input btn-interval" placeholder="工作">
                                        <div style="color:red"></div>
                                    </div>
                                    <div class="dropdown-inline">
                                        <span>电话:</span>
                                        <input name="phone" type="text" class="form-control search-input btn-interval" placeholder="电话">
                                        <div style="color:red"></div>
                                    </div>
                                    <div class="dropdown-inline">
                                        <span>邮箱:</span>
                                        <input name="email" type="text" class="form-control search-input btn-interval" placeholder="邮箱">
                                        <div style="color:red"></div>
                                    </div>

                                    <button class="btn btn-link padding_zero" name="delete" onclick="delCpuCell(this)">
                                        <li class="fa fa-cut">&nbsp;</li>删除</button>

                                </div>
                            </div>
                        </div>

                        <div id="contactInfo" class="widget-center" >

                            <!--  ////动态添加内容-->


                        </div>
                        <div  class="add_div_border">
                            <button class="btn btn-link btn-sm " id="add_div3">
                                <img width="20px" height="20px" src="images/add.png">
                                添加
                            </button>
                        </div>


                    </div>

                </div>

            </div> <!-- row -->

            <div >
                <button id="issuedButton" type="button" class="btn btn-primary">提交</button>
                <button id="clearButton" type="button" class="btn btn-default">清除</button>
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
                            检测器信息录入确认
                        </h4>
                    </div>
                    <div class="modal-body" style="text-align: center">
                        <p style="color: red">请确认是否录入信息</p>
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
            //buildFrame("menu-detector_insert");
            buildFrame("menu-detector_info");
            $(function () {
                console.log("执行js");

            });

            var globalSearchParam = {random:1}

            var globalSelectedDetetors = {}

            if(id==0){

                addCpuCell();
                addDiskCell();
                addContactCell();
            }

/*            $('button.condition-btn.singlechoose').click(function () {
                $(this).siblings().removeClass("active");
                $(this).addClass("active");
                console.log($(this).attr("value"))
                $("#type_plug").attr("value",$(this).attr("value"));


            })*/

            if(id>0){

                fillFormById()
            }

            //console.log('disabled'+is_r)
            if(is_r==1){

                setReadOnly()
            }

            function setReadOnly() {
               /////表单都变成不能编辑
                console.log('disabled')
                $(":input").attr("disabled",true)
                }


            function buildTbody(data) {
                var server = JSON.parse(data);
                var msg = server.msg;

/*                if(msg.interface.manage==1)
                {
                        var module = $("#manage").parent().parent()
                        module.find("span:first").attr("value",1)
                        module.find("span:first").text("True");
                }
                if(msg.interface.manage==2)
                {
                    var module = $("#manage").parent().parent()
                    module.find("span:first").attr("value",2)
                    module.find("span:first").text("False");
                }*/

                setSelect('manage',msg.interface.manage)
                setSelect('contractor',msg.contractor)

                
                $("#device_ca").val(msg.device_ca);
                $("#device_id").val(msg.device_id);
                $("#mem_total").val(msg.mem_total);
                $("#soft_version").val(msg.soft_version);
                $("#address").val(msg.address);
                $("#organs").val(msg.organs);
                $("#address_code").val(msg.address_code);
                $("#ip").val(msg.interface.ip);
                $("#mac").val(msg.interface.mac);
                $("#netmask").val(msg.interface.netmask);
                $("#gateway").val(msg.interface.gateway);



                for(i=0;i<msg.cpu_info.length;i++)
                {
                    addCpuCell()
                    $("#cpuInfo [name='cpuCell']").each(function() {
                        $(this).find("[name='physical_id']").val(msg.cpu_info[i].physical_id);
                        $(this).find("[name='core']").val(msg.cpu_info[i].core);
                        $(this).find("[name='clock']").val(msg.cpu_info[i].clock);
                    });
                }

                for(i=0;i<msg.disk_info.length;i++)
                {

                    addDiskCell()
                    $("#diskInfo [name='diskCell']").each(function() {

                        $(this).find("[name='serial']").val(msg.disk_info[i].serial);
                        $(this).find("[name='size']").val(msg.disk_info[i].size);
                    });

                }
                for(i=0;i<msg.contact.length;i++)
                {
                    addContactCell()
                    $("#contactInfo [name='contactCell']").each(function() {

                        $(this).find("[name='name']").val(msg.contact[i].name);
                        $(this).find("[name='position']").val(msg.contact[i].position);
                        $(this).find("[name='phone']").val(msg.contact[i].phone);
                        $(this).find("[name='email']").val(msg.contact[i].email);
                    });
                }




                //////填充表单

            }

            function fillFormById() {

                $.ajax({
                    url: "/ajax_action_detector.php?uu=detector_info.detail",
                    type: "post",
                    data: {id:id},
                    success:function(data) {
                        var ret = JSON.parse(data);
                        if(ret.code == 200){
                            console.log(data);
                            buildTbody(data);
                        }else{
                            alert("后台错误:"+ret.msg);
                        }
                    },
                    error: function () {
                         alert("无法连接服务器");
                    }
                })


            }

            $("#clearButton").click(function(){
                firstSelect("manage");
                firstSelect("contractor");
                $("#device_ca").val("");
                $("#device_id").val("");
                $("#mem_total").val("");
                $("#soft_version").val("");
                $("#address").val("");
                $("#organs").val("");
                $("#address_code").val("");
                $("#ip").val("");
                $("#mac").val("");
                $("#netmask").val("");
                $("#gateway").val("");


                $("#cpuInfo [name='cpuCell']").each(function() {

                    $(this).find("[name='physical_id']").val("");
                    $(this).find("[name='core']").val("");
                    $(this).find("[name='clock']").val("");
                });
                $("#diskInfo [name='diskCell']").each(function() {

                    $(this).find("[name='serial']").val("");
                    $(this).find("[name='size']").val("");
                    });
                $("#contactInfo [name='contactCell']").each(function() {

                    $(this).find("[name='name']").val("");
                    $(this).find("[name='position']").val("");
                    $(this).find("[name='phone']").val("");
                    $(this).find("[name='email']").val("");
                    });

            })




            function delCpuCell(obj) {
                $(obj).parent().parent().remove()

            }

            function addCpuCell() {
                $("#cpuInfo").append($("#cpuInfoTemplet [name='cpuCell']").clone());

            }
            function addDiskCell() {
                $("#diskInfo").append($("#diskInfoTemplet [name='diskCell']").clone());
            }
            function addContactCell() {
                $("#contactInfo").append($("#contactTemplet [name='contactCell']").clone());
            }

            $("#add_div1").click(function(){
                addCpuCell();
            });
            $("#add_div2").click(function(){
                addDiskCell();
            });
            $("#add_div3").click(function(){
                addContactCell();
            });

            $("#issuedButton").click(function(){

                var device_ca =  $("#device_ca").val();
                var device_id =  $("#device_id").val();;
                var mem_total =  $("#mem_total").val();;
                var soft_version =  $("#soft_version").val();;
                // var organs =  $("#organs").val();
                var contractor =  $("#contractor").attr("value").toString();
                var address =  $("#address").val();
                var organs =  $("#organs").val();
                var address_code =  $("#address_code").val();
                var ip =  $("#ip").val();
                var mac =  $("#mac").val();
                var manage =  $("#manage").attr("value").toString();
                var netmask=  $("#netmask").val();
                var gateway =  $("#gateway").val();


                //校验判断
                var error_str = ""

                if(device_ca==""){
                    error_str+="请输入检测器CA证书序列号\n";
                }

                if(soft_version==""){
                    error_str+="请输入检测器软件版本号\n";
                }

                if(organs==""){
                    error_str+="请输入检测器部署单位\n";
                }

                if(device_id==""){
                    error_str+="请输入检测器编号\n";
                }
                if(mem_total==""){
                    error_str+="请输入内存大小（MB）\n";
                }
                if(organs==""){
                    error_str+="请输入检测器部属单位\n";
                }

                if(address==""){
                    error_str+="请输入检测器部署地址\n";
                }
                if(address_code==""){
                    error_str+="请输入行政区域编码\n";
                }

                if(ip==""){
                    error_str+="请输入IP地址\n";
                }
                if(mac==""){
                    error_str+="请输入MAC地址\n";
                }
                if(manage=="-1"){
                    error_str+="请选择是否为管理口\n";
                }

                if(netmask==""){
                    error_str+="请输入子网掩码\n";
                }
                if(gateway==""){
                    error_str+="请输入网关地址\n";
                }


                $("#cpuInfo [name='cpuCell']").each(function() {

                    var physical_id =$(this).find("[name='physical_id']").val();
                    var core =$(this).find("[name='core']").val();
                    var clock =$(this).find("[name='clock']").val();

                    if(physical_id==""){
                        error_str+="请输入CPU编号\n";
                    }

                    if(core==""){
                        error_str+="请输入CPU核心数\n";
                    }
                    if(clock==""){
                        error_str+="请输入CPU主频\n";
                    }


                });

                $("#diskInfo [name='diskCell']").each(function() {
                    var serial =$(this).find("[name='serial']").val();
                    var size =$(this).find("[name='size']").val();
                    if(serial==""){
                        error_str+="请输入磁盘序列号\n";
                    }

                    if(size==""){
                        error_str+="请输入磁盘大小\n";
                    }


                });


                $("#contactInfo [name='contactCell']").each(function() {
                    var name =$(this).find("[name='name']").val();
                    var position =$(this).find("[name='position']").val();
                    var phone =$(this).find("[name='phone']").val();
                    var email =$(this).find("[name='email']").val();

                    if(name==""){
                        error_str+="请输入姓名\n";
                    }
                    if(position==""){
                        error_str+="请输入工作\n";
                    }

                    if(phone==""){
                        error_str+="请输入电话\n";
                    }
                    if(email==""){
                        error_str+="请输入邮箱\n";
                    }

                });




                $("input").each(function(){
                    var value = $(this).val(); //这里的value就是每一个input的value值~

                    if(!value.match(/^[\u4E00-\u9FA5a-zA-Z0-9_\.]{0,}$/)){


                        var label = $(this).prev("span").text()

                        error_str+=label+"存在非法字符\n";

                    }

                });


                if(error_str!=""){
                    alert(error_str);
                }else{
                    $('#hintModal').modal('show')
                }
            })

            $("#issueSubmit").click(function(){
                var device_ca =  $("#device_ca").val();
                var device_id =  $("#device_id").val();;
                var mem_total =  $("#mem_total").val();;
                var contractor =  $("#contractor").attr("value").toString();
                var soft_version =  $("#soft_version").val();
                var address =  $("#address").val();
                var organs =  $("#organs").val();
                var address_code =  $("#address_code").val();
                var ip =  $("#ip").val();
                var mac =  $("#mac").val();
                var manage =  $("#manage").attr("value").toString();
                var netmask=  $("#netmask").val();
                var gateway =  $("#gateway").val();



                issuedParam = {random:1}

                var interface={}

                interface["ip"] = ip
                interface["mac"] = mac
                interface["manage"] = manage
                interface["netmask"] = netmask
                interface["gateway"] = gateway

                issuedParam["interface"] = interface


                if(device_ca!=""){
                    issuedParam["device_ca"] = device_ca
                }



                if(device_id!=""){
                    issuedParam["device_id"] = device_id
                }
                if(mem_total!=""){
                    issuedParam["mem_total"] = parseInt(mem_total)
                }
                if(organs!=""){
                    issuedParam["organs"] = organs
                }
                if(contractor!=""){
                    issuedParam["contractor"] = contractor
                }
                if(soft_version!=""){
                    issuedParam["soft_version"] = soft_version
                }
                if(address!=""){
                    issuedParam["address"] = address
                }

                if(address_code!=""){
                    issuedParam["address_code"] = address_code
                }




                var cpuInfo=new Array()
                $("#cpuInfo [name='cpuCell']").each(function() {

                    var physical_id =$(this).find("[name='physical_id']").val();
                    var core =$(this).find("[name='core']").val();
                    var clock =$(this).find("[name='clock']").val();
                    var cpuCell = {

                        "physical_id":parseInt(physical_id),
                        "core":parseInt(core),
                        //"clock":parseInt(clock),
                        "clock":clock,

                    };
                    cpuInfo.push(cpuCell)
                    //alert(JSON.stringify(cpuCell))
                });
                ///alert(JSON.stringify(cpuInfo))
                if(cpuInfo.length>0){
                    issuedParam["cpu_info"] = cpuInfo
                }



                var diskInfo=new Array()
                $("#diskInfo [name='diskCell']").each(function() {

                    var serial =$(this).find("[name='serial']").val();
                    var size =$(this).find("[name='size']").val();
                    var diskCell = {
                        "serial":serial,
                        "size":parseInt(size),
                    };
                    diskInfo.push(diskCell)
                    //alert(JSON.stringify(cpuCell))
                });
                if(diskInfo.length>0){
                    issuedParam["disk_info"] = diskInfo
                }

                var contactInfo=new Array()
                $("#contactInfo [name='contactCell']").each(function() {

                    var name =$(this).find("[name='name']").val();
                    var position =$(this).find("[name='position']").val();
                    var phone =$(this).find("[name='phone']").val();
                    var email =$(this).find("[name='email']").val();
                    var contactCell = {

                        "name":name,
                        "position":position,
                        "phone":phone,
                        "email":email,

                    };
                    contactInfo.push(contactCell)

                });

                if(contactInfo.length>0){
                    issuedParam["contact"] = contactInfo
                }


                issuedParam["id"] = id

              //  alert(JSON.stringify(issuedParam))

                $.ajax({
                    url: "/ajax_action_detector.php?uu=detector_info.save",
                    type: "post",
                    data: {json:JSON.stringify(issuedParam)},
                    success:function(data) {
                        var ret = JSON.parse(data);
                        if(ret.code == 200){
                            alert("信息录入成功");
                            //$("#issuedButton").prop('disabled',"true");
                            window.open("detector_info.php");

                        }else{
                            alert("信息录入失败");
                        }
                    }
                })

                $("#hintModal").modal('hide');
            })
        </script>
</body>
</html>

