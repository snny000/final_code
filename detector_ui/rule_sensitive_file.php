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

    <title>涉密内容检测策略</title>

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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;涉密内容检测策略</h4>
            </div>
            <div class="upper-btn-group margin_ddos1 pull-right">
                <?php
                require_once(dirname(__FILE__) . '/require_top_button_for_rule_page.php');
                ?>
            </div>
        </div>
        <div class="row btn-banner upper-line"></div>
        <div class="row btn-banner">
                <input id="rule_id" type="text" class="form-control search-input" placeholder="规则编号（模糊搜索）">
                <input id="rule_content" type="text" class="form-control search-input btn-interval" placeholder="规则内容（模糊搜索）">

                <div class="dropdown btn-interval dropdown-inline">
                    <button type="button" data-toggle="dropdown"
                            class="btn dropdown-btn dropdown-menu-width"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <span id="risk" class="pull-left" value="-1">所有警报风险级别</span>
                        <i class="fa fa-sort-down pull-right"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                        <li onclick="selectProtoFwd(this);" value="-1">所有警报风险级别</li>
                        <li onclick="selectProtoFwd(this);" value="0">无风险</li>
                        <li onclick="selectProtoFwd(this);" value="1">一般级</li>
                        <li onclick="selectProtoFwd(this);" value="2">关注级</li>
                        <li onclick="selectProtoFwd(this);" value="3">严重级</li>
                        <li onclick="selectProtoFwd(this);" value="4">紧急级</li>
                    </ul>
                </div>

                <div class="dropdown btn-interval dropdown-inline">
                    <button type="button" data-toggle="dropdown"
                            class="btn dropdown-btn dropdown-menu-width"
                            aria-haspopup="true"
                            aria-expanded="false">
                        <span id="rule_status" class="pull-left" value="-1">所有规则状态</span>
                        <i class="fa fa-sort-down pull-right"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                        <li onclick="selectProtoFwd(this);" value="-1">所有规则状态</li>
                        <li onclick="selectProtoFwd(this);" value="0">已下发</li>
                        <li onclick="selectProtoFwd(this);" value="1">未下发</li>
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
                    <th width="9%">规则编号</th>
                    <th width="9%">规则类型</th>
                    <th width="9%">最少命中次数</th>
                    <th width="9%">规则内容</th>
                    <th width="9%">告警级别</th>
                    <th width="9%">规则状态</th>
					<th width="9%">标签</th>
                    <th width="9%">创建时间</th>
                    <th width="9%">生效范围</th>
                    <th width="8%">操作</th>
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
                            <button class="btn btn-default btn-sm" id="refresh">刷新</button>
                        </div>
                        <div class="pull-right">


                            <?php
                            require_once(dirname(__FILE__) . '/require_page_bar_for_all_page.php');
                            ?>

                            <!-- <nav id="paginationbox">
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

                <div class="dropdown-inline">
                    <span> 规则类型:</span>
                    <div class="dropdown">
                        <button type="button" data-toggle="dropdown"
                                class="btn dropdown-btn dropdown-menu-width"
                                aria-haspopup="true"
                                aria-expanded="false">
                            <span id="add_rule_type" class="pull-left" value="keyword">关键词</span>
                            <i class="fa fa-sort-down pull-right"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                            <li onclick="selectProtoFwd(this);" value="keyword">关键词</li>
                            <li onclick="selectProtoFwd(this);" value="regex">正则表达式</li>
                        </ul>
                    </div>
                </div>

                <div class="dropdown-inline">
                    <span> 告警级别:</span>
                    <div class="dropdown">
                        <button type="button" data-toggle="dropdown"
                                class="btn dropdown-btn dropdown-menu-width"
                                aria-haspopup="true"
                                aria-expanded="false">
                            <span id="add_risk" class="pull-left" value="0">无风险</span>
                            <i class="fa fa-sort-down pull-right"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                            <li onclick="selectProtoFwd(this);" value="0">无风险</li>
                            <li onclick="selectProtoFwd(this);" value="1">一般级</li>
                            <li onclick="selectProtoFwd(this);" value="2">关注级</li>
                            <li onclick="selectProtoFwd(this);" value="3">严重级</li>
                            <li onclick="selectProtoFwd(this);" value="4">紧急级</li>
                        </ul>
                    </div>
                </div>

                <div>
                    <span> 最少命中次数:</span> <input id="add_min_match_count" type="number" class="form-control" value=1 min="1" max="20" ;>
                    <div style="color:red"></div>
                    <span> 规则内容:</span>
                    <textarea id="add_rule_content" style="width:100%;height:80px;resize: vertical;" class="form-control"></textarea>
                    <div style="color:red"></div>
                </div>
				<div>
                    <span>备注标签（可用于查询）：</span> <input id="add_label"  class="form-control";>
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
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script>
    buildFrame("policy_type5");
    var global_policy_type=5;

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
                        $("<tr><td colspan='11' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
                    }else if (ret["code"] == 9001){
                        window.location.href = "login.php?ref="+window.location.href;
                    }else{
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
        //console.log(option)
        $('#pagination').twbsPagination(option);
    }




    $("#add-submit").click(function(){

            var ischeck = true
            var add_min_match_count = $("#add_min_match_count").val()
            var add_rule_content = $("#add_rule_content").val()
            var re = /^-?\\d+$/;
            if( !(/^(\+|-)?\d+$/.test(add_min_match_count))&&add_min_match_count>0 ||
                (add_min_match_count<=0 || add_min_match_count>20) ){
                $("#add_min_match_count").next("div").html("请输入在1~20间的整数")
                ischeck = false
            }else{
                $("#add_min_match_count").next("div").html("")
            }

            if(add_rule_content == ""){
                $("#add_rule_content").next("div").html("规则内容不能为空")
                ischeck = false
            }else{
                $("#add_rule_content").next("div").html("")
            }

            if(!ischeck){
                return;
            }


            var param = {
                "rule_type": $("#add_rule_type").attr("value"),
                "risk":parseInt($("#add_risk").attr("value")),
                "min_match_count": parseInt($("#add_min_match_count").val()),
                "rule_content": $("#add_rule_content").val(),
				"label":$("#add_label").val(),
            };
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
        var riskMap = {0:'无风险',1:'一般级',2:'关注级',3:'严重级',4:'紧急级'}
        var statusMap = {0:'已下发',1:'未下发'}
		var operateMap = {1:'增加',2:'删除',3:'变更范围'}
        var rule_typeMap = {0:'关键词',1:'正则表达式'}

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
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();row.attr("id",msgListObj[i].id)
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+ " value="+msgListObj[i].device_id_list.replace(/\s/g, "")+">")
            row.find("td:eq(1)").text(msgListObj[i].rule_id);
            row.find("td:eq(2)").html(rule_typeMap[msgListObj[i].rule_type]);
            row.find("td:eq(3)").text(msgListObj[i].min_match_count);
            row.find("td:eq(4)").html(msgListObj[i].rule_content);
            row.find("td:eq(5)").html(riskMap[msgListObj[i].risk]);
            row.find("td:eq(6)").html(statusMap[msgListObj[i].rule_status]+"("+operateMap[msgListObj[i].operate]+")");
            row.find("td:eq(7)").html(msgListObj[i].label);
            row.find("td:eq(8)").html(msgListObj[i].create_t);

          /*  var num =eval(msgListObj[i].device_id_list).length
            if(num>0){
                var operateviewhtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + msgListObj[i].id + ","+msgListObj[i].device_id_list+",3)\">生效检测器数量"+eval(msgListObj[i].device_id_list).length+"（查看）</a>"
            }else{
                var operateviewhtml = "全部检测器生效"
            }*/
            var operateviewhtml=generateoperateviewhtml(msgListObj[i].id,msgListObj[i].device_id_list)
            var operatehtml=generateoperatehtml(msgListObj[i].id,msgListObj[i].device_id_list)
            row.find("td:eq(9)").html(operateviewhtml);
         /*   var operatehtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + msgListObj[i].id + ","+msgListObj[i].device_id_list+",1)\">变更生效范围</a>"
           */ row.find("td:eq(10)").html(operatehtml);
            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }

    var globalSearchParam = {random:1}

    //第一次加载分页
    //LoadPage(1,globalSearchParam)
    globalSearchParam = cacheSearchParam;
    LoadPage(cachePage,globalSearchParam);
    alterSearchForm()


    $("#searchButton").click(function(){
        var rule_id =  $("#rule_id").val();
        var rule_content =  $("#rule_content").val();
		var label =  $("#label").val();
        var device_id = $("#device_id").val();
        var risk = $("#risk").attr("value").toString()
        var rule_status = $("#rule_status").attr("value").toString()

       // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        globalSearchParam = {random:1}
        if(risk!="-1"){
            globalSearchParam["risk"] = risk
        }
        if(rule_status!="-1"){
            globalSearchParam["rule_status"] = rule_status
        }

        if(rule_id!=""){
            globalSearchParam["rule_id"] = rule_id
        }
        if(rule_content!=""){
            globalSearchParam["rule_content"] = rule_content
        }
        if(device_id!=""){
            globalSearchParam["device_id"] = device_id
        }


        if(label!=""){
            globalSearchParam["label"] = label
        }
        LoadPage(1,globalSearchParam)
    })

    $("#clearButton").click(function(){
        firstSelect("risk");
        firstSelect("rule_status");
        $("#rule_id").val("");
        $("#rule_content").val("");
		$("#label").val("");
		$("#device_id").val("");
    })
	
	function alterSearchForm (){

        oneSelect("risk");
        oneSelect("rule_status");

        oneInput("rule_id");
        oneInput("rule_content");
        oneInput("label");
		oneInput("device_id");



    }

 /*   $("#cancelSubmit").click(function() {
        alert('1111111111')
        $('#new_label_div').hide()
        $('#hintModal').modal('hide')
    })*/


    $("#delete").click(function(){
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
                url: "/ajax_action_detector.php?uu=rule.del&policy_type=" + global_policy_type.toString(),
                type: "post",
                data: {id:JSON.stringify(carray)},
                success:function(data) {
                    //  var ret = JSON.parse(data);
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
            "<p >下发规则个数:<span style='color: red;font-size: large'>"+$("#full span").text()+"</span></p>"
        $('#hintModal').find(".modal-body").html(content)

        var footer = "<button id='fullSubmit' type='button' class='btn btn-primary'>确定</button>"+
            "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
        $('#hintModal').find(".modal-footer").html(footer)

        $("#fullSubmit").click(function(){
            $.ajax({
                url: "/ajax_action_detector.php?uu=rule.sync&policy_type=" + global_policy_type.toString() + "&type=1",
                type: "post",
                data:null,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if(ret.code == 200){
                        alert("全量下发成功");
                    }else{
                        alert("全量下发失败");
                    }
                    refresh()
                }
            })
            //  $(this).prop('disabled',"true");

            $('#hintModal').modal('hide')
        })

        $('#hintModal').modal('show')
    })


    $("#increment").click(function(){
        $('#hintModal').find(".modal-title").html("增量下发提示框")

        var content =
            "<span>下发方式:<span style='color: red;font-size: large'>增量下发</span></span>"+
            "<p >下发规则个数:<span style='color: red;font-size: large'>"+$("#increment span").text()+"</span></p>"
        $('#hintModal').find(".modal-body").html(content)

        var footer = "<button id='incrementSubmit' type='button' class='btn btn-primary'>确定</button>"+
            "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
        $('#hintModal').find(".modal-footer").html(footer)

        $("#incrementSubmit").click(function(){
            $.ajax({
                url: "/ajax_action_detector.php?uu=rule.sync&policy_type=" + global_policy_type.toString() + "&type=0",
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

    /*
    $("#full").click(function(){
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.sync&policy_type=" + global_policy_type.toString() + "&type=1",
            type: "post",
            data:null,
            success:function(data) {
                //  var ret = JSON.parse(data);
                console.log(data)
            }
        })
      //  $(this).prop('disabled',"true");
        refresh()
    })


    $("#increment").click(function(){
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.sync&policy_type=" + global_policy_type.toString() + "&type=0",
            type: "post",
            data:null,
            success:function(data) {
                //  var ret = JSON.parse(data);
                console.log(data)
            }
        })
      //  $(this).prop('disabled',"true");
        refresh()
    })
    */
</script>
<script>

    function pickDetectorForward(id,device_id_list,type){

        //var
        //alert('1111')

        //console.log(000)
        var param= {cacheRef:'rule_sensitive_file.php'}///////!!!!!!!!!
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

        param["cacheMenu"] = "policy_type5";///////!!!!!!!!!
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