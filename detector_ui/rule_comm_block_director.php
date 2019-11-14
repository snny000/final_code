<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');

require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

require_once(dirname(__FILE__) . '/require_get_parameter_for_rule_page.php');
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

    <title>通信阻断策略</title>

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

    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;通信阻断策略
                    <div class="btn-group" data-toggle="buttons">
                        <!--<label class="btn btn-primary active" href="rule_trojan.php">
                            管理中心本地
                        </label>
                        <label class="btn btn-primary" href="rule_trojan_director.php">
                            指挥节点下发
                        </label>-->
                    </div>
                </h4>
            </div>
        </div>
        <div class="row btn-banner upper-line"></div>
        <div class="row btn-banner">
            <input id="rule_id" type="text" class="form-control search-input" placeholder="规则编号（模糊搜索）">
			<input id="sip" type="text" class="form-control search-input btn-interval" placeholder="源IP地址">
            <input id="dip" type="text" class="form-control search-input btn-interval" placeholder="目的IP地址">
            &nbsp;
            <?php
                require_once(dirname(__FILE__) . '/require_common_search_for_rule_page.php');
            ?>
            <button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>
        </div>
       
        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr >
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="11%">规则编号</th>
                    <th width="11%">源IP地址</th>
                    <th width="11%">源端口范围</th>
                    <th width="12%">目的IP地址</th>
					<th width="11%">目的端口范围</th>
                    <th width="11%">通信协议</th>
                    <th width="11%">生效范围</th>
                    <th width="12%">任务组</th>
                </tr>
                </thead>

                <tbody>
                </tbody>

                <tfoot>
                <tr>
                    <td><input type="checkbox" class="checkbox" id="chk_all2"></td>
                    <td>
                        <div class="pull-left">
                            <?php
                            require_once(dirname(__FILE__) . '/require_batch_button_for_rule_page.php');
                            ?>
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
<!-- 模态框（Modal） -->
<div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="detailLabel" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    添加策略
                </h4>
            </div>
            <div class="modal-body">


                <div>
                     <span>源IP地址（IP子网类型，未标注子网掩码表示单个IP地址）:</span> <input id="add_sip"  class="form-control";>
                    <div style="color:red"></div>
                    <span>源端口范围（输入单个XX端口或者XX-XX的端口范围）:</span> <input id="add_sport"  class="form-control";>
                    <div style="color:red"></div>
                    <span>目的IP地址（IP子网类型，未标注子网掩码表示单个IP地址）:</span> <input id="add_dip"  class="form-control";>
                    <div style="color:red"></div>
                    <span>目的端口范围（输入单个XX端口或者XX-XX的端口范围）:</span> <input id="add_dport"  class="form-control";>
                    <div style="color:red"></div>
                    <span>通信协议:</span> <input id="add_protocol"  class="form-control" placeholder="TCP" readOnly="true" >
                    <div>
                    <div> 选择任务组:</div>
                    <select id="task_group" class="selectpicker task_group_select" data-live-search="true" title="请选择任务组 ..." style="width:100%;">
                    </select>
                    </div>
                    <div style="color:red"></div>
                    <span>备注标签:</span> <input id="add_label"  class="form-control";>
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

<?php
require_once(dirname(__FILE__) . '/require_hint_modal_for_rule_page.php');
?>

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

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>
<script src="js/rule_common.js"></script>
<script>
    buildFrame("menu-rule8");
    var global_policy_type=18;

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

        var param = {

            "sip":$("#add_sip").val(),
            "label":$("#add_label").val(),
            "sport":$("#add_sport").val(),
            "dip":$("#add_dip").val(),
            "dport":$("#add_dport").val(),
            "protocol":6,
            "group_id":$("#task_group").val()==""? 0: $("#task_group").val()
        };


            var ischeck = true
            var add_sip = $("#add_sip").val()
            var add_label = $("#add_label").val()
            var add_sport = $("#add_sport").val()
            var add_dip = $("#add_dip").val()
            var add_dport = $("#add_dport").val()
            var add_protocol=$("#add_protocol").val()
            if(add_sip == ""){
                $("#add_sip").next("div").html("源IP不能为空")
                ischeck = false
            }else{
                $("#add_sip").next("div").html("")
            }

        if(add_sport == ""){
            $("#add_sport").next("div").html("源端口范围不能为空")
            ischeck = false
        }else{
            $("#add_sport").next("div").html("")
        }


        if(add_dip == ""){
            $("#add_dip").next("div").html("目的IP地址不能为空")
            ischeck = false
        }else{
            $("#add_dip").next("div").html("")
        }

        if(add_dport == ""){
            $("#add_dport").next("div").html("目的端口范围不能为空")
            ischeck = false
        }else{
            $("#add_dport").next("div").html("")
        }

        if(!ischeck){
                return;
            }


            //console.log(param)
            $.ajax({
                url: "/ajax_action_detector.php?uu=rule.insert&policy_type=" + global_policy_type,
                type: "post",
                data: {json:JSON.stringify(param)},
                success:function(data) {
                    //  var ret = JSON.parse(data);
                    console.log(data)
                    refresh();
                }
            })
            $("#addModal").modal('hide');

        }
    )
    

    /*
     var msgListObj = eval(msgList);
     List(msgListObj); //默认列表
     */

    function List(msgListObj){
        var protocolMap = {6:'TCP'}
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
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();row.attr("id",msgListObj[i].id)
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+ " value="+msgListObj[i].device_id_list.replace(/\s/g, "")+">")
            row.find("td:eq(1)").html(msgListObj[i].rule_id);
            row.find("td:eq(2)").html(msgListObj[i].sip);
            row.find("td:eq(3)").html(msgListObj[i].sport);
            row.find("td:eq(4)").html(msgListObj[i].dip);
            row.find("td:eq(5)").html(msgListObj[i].dport);
            row.find("td:eq(6)").html(protocolMap[msgListObj[i].protocol]);
            var operateviewhtml=generateoperateviewhtml(msgListObj[i].id,msgListObj[i].device_id_list)
//            var operatehtml=generateoperatehtml(msgListObj[i].id,msgListObj[i].device_id_list)
            row.find("td:eq(7)").html(operateviewhtml);
//            row.find("td:eq(8)").html(operatehtml);
            // 任务组绑定
//            var task_group_data = {
//                "group_id": msgListObj[i].group_id,
//                "rule_type": global_policy_type,
//                "name": msgListObj[i].group_name
//            }
//            var task_group_dom = `<a data-bind=${JSON.stringify(task_group_data)} onclick="showTaskGroup(this)">${msgListObj[i].group_name}</a>`
//            if(msgListObj[i].group_id != null && msgListObj[i].group_id != 0){
//                row.find("td:eq(9)").addClass('hasTaskGroup');
//
//            }
//            row.find("td:eq(9)").html(task_group_dom);
            row.find("td:eq(8)").html(msgListObj[i].task_id != 0 ? msgListObj[i].task_id : '');
            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }

    var globalSearchParam = {random:1}

    //第一次加载分页
    //LoadPage(1,globalSearchParam,1)
    globalSearchParam = cacheSearchParam;
    LoadPage(cachePage,globalSearchParam,1);
    alterSearchForm()


    $("#searchButton").click(function(){
        var rule_id =  $("#rule_id").val();
		var sip =  $("#sip").val();
        var dip = $("#dip").val();
        var group_id = $("#task_group_id").val(); //任务组



        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        globalSearchParam = {random:1}
        


        if(rule_id!=""){
            globalSearchParam["rule_id"] = rule_id
        }
        if(group_id!=""){
            globalSearchParam["group_id"] = group_id
        }

		if(sip!=""){
            globalSearchParam["sip"] = sip
        }
		if(dip!=""){
            globalSearchParam["dip"] = dip
        }


        

        LoadPage(1,globalSearchParam,1)
    })


    $("#clearButton").click(function(){
        
        firstSelect("rule_status");
        $("#rule_id").val("");
		$("#sip").val("");
		$("#dip").val("");
        $("#task_group_id").selectpicker("val","");
    })
	 function alterSearchForm (){

        oneSelect("rule_status");

        oneInput("rule_id");
        oneInput("sip");
		oneInput("dip");
    }

    $('#refresh').click(function () {
        var currentPage = $('#pagination .active a').text();
        LoadPage(currentPage,globalSearchParam,1)
    });

 /*   $("#cancelSubmit").click(function() {
        alert('1111111111')
        $('#new_label_div').hide()
        $('#hintModal').modal('hide')
    })*/

</script>

<script>

    function pickDetectorForward(id,device_id_list,type){

        //var
        //alert('1111')

        //console.log(000)
        var param= {cacheRef:currentPagePath}///////!!!!!!!!!
        var currentPage = $('#pagination .active a').text()
        param["cachePage"] = currentPage

        //console.log(111)

       // var carray_device =device_id_list.replace("[","").replace("]","").split(",")

        param["cacheDevice_id_list"]=JSON.stringify(eval(device_id_list));
        //param["cacheDevice_id_list"]=[1,2];
        param["cacheCmd_type"] = type;

 /*       if(type==3){

            globalSearchParam

        }*/
        param["cacheSearchParam"] = JSON.stringify(globalSearchParam)

        param["cacheMenu"] = "menu-rule8";///////!!!!!!!!!
        param["cacheType"]=1
        param["cachePolicy_type"] = global_policy_type///////!!!!!!!!!
        //console.log(222)
        if(id instanceof Array){
            param["cacheId"] = JSON.stringify(id)

        }else{

            var carray =new Array()
            carray.push(parseInt(id))
            param["cacheId"] = JSON.stringify(carray)
        }
        //console.log(333)

        if(type==3){

            post_blank('pick_detector.php',param);

        }else{

            post('pick_detector.php',param);

        }





    }

</script>

</body>
</html>