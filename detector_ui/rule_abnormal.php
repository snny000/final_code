<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
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

    <title>未知攻击窃密检测策略</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

    <!-- Add custom CSS here -->
    <link href="css/frame.css" rel="stylesheet">
    <link href="css/product.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <link href="css/detector.css" rel="stylesheet">
    <link href="css/rule.css" rel="stylesheet">
    <link href="bootstrap-datetimepicker-master/css/bootstrap-datetimepicker.min.css" rel="stylesheet" media="screen">

    <style>


    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;未知攻击窃密检测策略
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
            <div class="upper-btn-group margin_ddos1 pull-right">
                <?php
                require_once(dirname(__FILE__) . '/require_top_button_for_rule_page.php');
                ?>
            </div>
        </div>
        <div class="row btn-banner upper-line"></div>
        <div class="row btn-banner">
            
            <input id="file_size_limit" type="text" class="form-control search-input" placeholder="文件大小">
			<input id="file_num_hour" type="text" class="form-control search-input btn-interval" placeholder="每小时上传文件">
			<input id="rate_limit" type="text" class="form-control search-input btn-interval" placeholder="最大带宽速率">
            <input id="label" type="text" class="form-control search-input btn-interval" placeholder="备注标签（模糊搜索）">
            <input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器ID(精确搜索)">
            
		</div>
		<div class="row btn-banner">
        <?php
                    require_once(dirname(__FILE__) . '/require_common_search_for_rule_page.php');
                ?>
                <div class="dropdown btn-interval dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="abn_type" class="pull-left" value="-1">所有窃密类型</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="-1">所有窃密类型</li>
                    <li onclick="selectProtoFwd(this);" value="0">0</li>
                    <li onclick="selectProtoFwd(this);" value="1">1</li>
                    <li onclick="selectProtoFwd(this);" value="2">2</li>
                    <li onclick="selectProtoFwd(this);" value="3">3</li>
                    <li onclick="selectProtoFwd(this);" value="4">4</li>
                    <li onclick="selectProtoFwd(this);" value="5">5</li>
                    <li onclick="selectProtoFwd(this);" value="6">6</li>
                    <li onclick="selectProtoFwd(this);" value="7">7</li>
                    <li onclick="selectProtoFwd(this);" value="8">8</li>
                    
                </ul>
            </div>
            &nbsp;
		      <div class="dropdown dropdown-inline">
                <button type="button" data-toggle="dropdown"
                        class="btn dropdown-btn dropdown-menu-width"
                        aria-haspopup="true"
                        aria-expanded="false">
                    <span id="risk_min" class="pull-left" value="-1">所有告警级别</span>
                    <i class="fa fa-sort-down pull-right"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
                    <li onclick="selectProtoFwd(this);" value="-1">所有告警级别</li>
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
                    <th width="6%">规则编号</th>
                    <th width="7%">未知攻击窃密类型</th>
                    <th width="7%">是否允许文件上传</th>
                    <th width="6%">文件大小</th>
                    <th width="7%">每小时上传文件</th>
					<th width="8%">最大带宽速率</th>
					<th width="8%">最低风险级别</th>
					<th width="8%">规则状态</th>
                    <th width="8%">标签</th>
                    <th width="8%">创建时间</th>
                    <th width="9%">生效范围</th>
                    <th width="9%">操作</th>
                    <th width="10%">任务组</th>
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
                    添加策略
                </h4>
            </div>
            <div class="modal-body">
			
			    <div class="dropdown-inline">
                    <span> 未知攻击窃密类型:</span>
                    <div class="dropdown">
                        <button type="button" data-toggle="dropdown"
                                class="btn dropdown-btn dropdown-menu-width"
                                aria-haspopup="true"
                                aria-expanded="false">
							<span id="add_abn_type" class="pull-left" value="-1">未选择</span>
                            <i class="fa fa-sort-down pull-right"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
						    <li onclick="selectProtoFwd(this);" value="-1">未选择</li>
							<li onclick="selectProtoFwd(this);" value="0">0</li>
                            <li onclick="selectProtoFwd(this);" value="1">1</li>
                            <li onclick="selectProtoFwd(this);" value="2">2</li>
                            <li onclick="selectProtoFwd(this);" value="3">3</li>
                            <li onclick="selectProtoFwd(this);" value="4">4</li>
							<li onclick="selectProtoFwd(this);" value="5">5</li>
							<li onclick="selectProtoFwd(this);" value="6">6</li>
							<li onclick="selectProtoFwd(this);" value="7">7</li>
							<li onclick="selectProtoFwd(this);" value="8">8</li>
                        </ul>
                    </div>
					<div style="color:red"></div>
                </div>
				
				<div class="dropdown-inline">
                    <span> 是否允许文件上传:</span>
                    <div class="dropdown">
                        <button type="button" data-toggle="dropdown"
                                class="btn dropdown-btn dropdown-menu-width"
                                aria-haspopup="true"
                                aria-expanded="false">
                            <span id="add_allow_file" class="pull-left" value="-1">未选择</span>
                            <i class="fa fa-sort-down pull-right"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
						    <li onclick="selectProtoFwd(this);" value="-1">未选择</li>
                            <li onclick="selectProtoFwd(this);" value="0">不允许</li>
                            <li onclick="selectProtoFwd(this);" value="1">允许</li>
                        </ul>
                    </div>
					<div style="color:red"></div>
                </div>


                <div>
                    <span>文件大小限制（KB，取值区间是[0,102400]，数值型，允许文件上传时填写）：</span> <input id="add_file_size_limit" type="number" min="0"  class="form-control";>
                    <div style="color:red"></div>
                    <span>每小时上传文件限制（取值区间是[0,1000]，数值型）：</span> <input id="add_file_num_hour" type="number" min="0"  class="form-control";>
                    <div style="color:red"></div>
                    <span>文件上传的最大带宽速率限制（Kbps，取值区间是[0,102400]，数值型）:</span> <input id="add_rate_limit" type="number" min="0"  class="form-control";>
                    <div style="color:red"></div>
                </div>

                
				<div class="dropdown-inline">
                    <span> 最低风险级别:</span>
                    <div class="dropdown">
                        <button type="button" data-toggle="dropdown"
                                class="btn dropdown-btn dropdown-menu-width"
                                aria-haspopup="true"
                                aria-expanded="false">
                            <span id="add_risk_min" class="pull-left" value="-1">未选择</span>
                            <i class="fa fa-sort-down pull-right"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
						    <li onclick="selectProtoFwd(this);" value="-1">未选择</li>
                            <li onclick="selectProtoFwd(this);" value="0">无风险</li>
                            <li onclick="selectProtoFwd(this);" value="1">一般级</li>
                            <li onclick="selectProtoFwd(this);" value="2">关注级</li>
                            <li onclick="selectProtoFwd(this);" value="3">严重级</li>
                            <li onclick="selectProtoFwd(this);" value="4">紧急级</li>
                        </ul>
                    </div>
					<div style="color:red"></div>
                </div>
                <div>
                    <div> 选择任务组:</div>
                    <select id="task_group" class="selectpicker task_group_select" data-live-search="true" title="请选择任务组 ..." style="width:100%;">
                    </select>
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
<link href="css/bootstrap-select.css" rel="stylesheet">
<script type="text/javascript" src="js/bootstrap-select.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script src="js/rule_common.js"></script>

<script>
    buildFrame("menu-rule3");
    var global_policy_type=4;

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
			                       
            "file_size_limit":$("#add_file_size_limit").val() == '' ? -1 : parseInt($("#add_file_size_limit").val()),
            "file_num_hour":parseInt($("#add_file_num_hour").val()),
			"rate_limit":parseInt($("#add_rate_limit").val()),
			"abn_type": parseInt($("#add_abn_type").attr("value")),
			"allow_file": parseInt($("#add_allow_file").attr("value")),
			"risk_min": parseInt($("#add_risk_min").attr("value")),
            "label":$("#add_label").val(),
            "group_id":$("#task_group").val()==""? 0: $("#task_group").val()
        };


            var ischeck = true
            var add_file_size_limit = $("#add_file_size_limit").val()
            var add_file_num_hour= $("#add_file_num_hour").val()
			var add_rate_limit = $("#add_rate_limit").val()
			var add_abn_type = $("#add_abn_type").attr("value")
			var add_allow_file = $("#add_allow_file").attr("value")
			var add_risk_min = $("#add_risk_min").attr("value")
            
			
            if(add_file_size_limit == "" && add_allow_file == 1){    ///文件大小这个输入框，只有当是否允许文件上传“allow_file”值为1的时候有效
                $("#add_file_size_limit").next("div").html("文件大小不能为空")
                ischeck = false
            }else{
                $("#add_file_size_limit").next("div").html("")
            }
			if(add_file_num_hour == ""){
                $("#add_file_num_hour").next("div").html("每小时上传文件不能为空")
                ischeck = false
            }else{
                $("#add_file_num_hour").next("div").html("")
            }

            if(add_rate_limit == ""){
                $("#add_rate_limit").next("div").html("最大带宽速率不能为空")
                ischeck = false
            }else{
                $("#add_rate_limit").next("div").html("")
            }
			
			if(add_allow_file == -1){
			    $("#add_allow_file").parent().parent().next("div").html("请选择是否允许文件上传")
				ischeck = false
			}else{
				$("#add_allow_file").parent().parent().next("div").html("")
			}
			if(add_abn_type == -1){
			    $("#add_abn_type").parent().parent().next("div").html("请选择未知攻击窃密类型")
				ischeck = false
			}else{
				$("#add_abn_type").parent().parent().next("div").html("")
			}
			if(add_risk_min == -1){
			    $("#add_risk_min").parent().parent().next("div").html("请选择最低风险级别")
				ischeck = false
			}else{
				$("#add_risk_min").parent().parent().next("div").html("")
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
        var abnMap = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8'}
        var riskMap = {0:'无风险',1:'一般级',2:'关注级',3:'严重级',4:'紧急级'}
        var statusMap = {0:'已下发',1:'未下发'}
		var allowMap={0:'不允许',1:'允许'}
        var operateMap = {1:'增加',2:'删除',3:'变更范围'}

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
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "<td style='color:#999999'></td>" +
            "</tr>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();row.attr("id",msgListObj[i].id)
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+ " value="+msgListObj[i].device_id_list.replace(/\s/g, "")+">")
            row.find("td:eq(1)").html(msgListObj[i].rule_id);
			row.find("td:eq(2)").html(abnMap[msgListObj[i].abn_type]);
			row.find("td:eq(3)").html(allowMap[msgListObj[i].allow_file]);
			if (msgListObj[i].allow_file === 1) {
                row.find("td:eq(4)").html(msgListObj[i].file_size_limit);
            } else {
                row.find("td:eq(4)").html('');
            }
			row.find("td:eq(5)").html(msgListObj[i].file_num_hour);
			row.find("td:eq(6)").html(msgListObj[i].rate_limit);
			row.find("td:eq(7)").html(riskMap[msgListObj[i].risk_min]);
			// row.find("td:eq(7)").html(statusMap[msgListObj[i].rule_status]+"("+operateMap[msgListObj[i].operate]+")");
            row.find("td:eq(8)").html(ruleStatusFormat(msgListObj[i]));
            row.find("td:eq(9)").html(msgListObj[i].label);
            row.find("td:eq(10)").html(msgListObj[i].create_t);

/*            var num =eval(msgListObj[i].device_id_list).length
            if(num>0){
                var operateviewhtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + msgListObj[i].id + ","+msgListObj[i].device_id_list+",3)\">生效检测器数量"+eval(msgListObj[i].device_id_list).length+"（查看）</a>"
            }else{
                var operateviewhtml = "全部检测器生效"
            }*/
            var operateviewhtml=generateoperateviewhtml(msgListObj[i].id,msgListObj[i].device_id_list)
            var operatehtml=generateoperatehtml(msgListObj[i].id,msgListObj[i].device_id_list)

            row.find("td:eq(11)").html(operateviewhtml);
            //var operatehtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + msgListObj[i].id + ","+msgListObj[i].device_id_list+",1)\">变更生效范围</a>"
            row.find("td:eq(12)").html(operatehtml);
           // 任务组绑定
            var task_group_data = {
                "group_id": msgListObj[i].group_id,
                "rule_type": global_policy_type,
                "name": msgListObj[i].group_name
,
            }
            var task_group_dom = `<a data-bind=${JSON.stringify(task_group_data)} onclick="showTaskGroup(this)">${msgListObj[i].group_name}</a>`
            if(msgListObj[i].group_id != null && msgListObj[i].group_id != 0){
                row.find("td:eq(13)").addClass('hasTaskGroup');
            }
            row.find("td:eq(13)").html(task_group_dom);
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
        var file_size_limit =  $("#file_size_limit").val();
        var file_num_hour =  $("#file_num_hour").val();
		var rate_limit =  $("#rate_limit").val();
        var label =  $("#label").val();
        var device_id = $("#device_id").val();

		var abn_type = $("#abn_type").attr("value").toString();
        var risk_min = $("#risk_min").attr("value").toString();
        var rule_status = $("#rule_status").attr("value").toString();
        var group_id = $("#task_group_id").val(); //任务组

        // globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
        globalSearchParam = {random:1}
        
        if(risk_min!="-1"){
            globalSearchParam["risk_min"] = risk_min
        }
        if(rule_status!="-1"){
            globalSearchParam["rule_status"] = rule_status
        }
        if(abn_type!="-1"){
            globalSearchParam["abn_type"] = abn_type
        }
         if(group_id!=""){
            globalSearchParam["group_id"] = group_id
        }

        if(file_size_limit != ""){
            globalSearchParam["file_size_limit"] = file_size_limit
        }
        if(file_num_hour!=""){
            globalSearchParam["file_num_hour"] = file_num_hour
        }
		if(rate_limit!=""){
            globalSearchParam["rate_limit"] = rate_limit
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
        
        firstSelect("risk_min");
        firstSelect("rule_status");
        firstSelect("abn_type");
        $("#file_size_limit").val("");
        $("#file_num_hour").val("");
		$("#rate_limit").val("");
        $("#label").val("");
        $("#device_id").val("");
        $("#task_group_id").selectpicker("val","");

    })







    function alterSearchForm (){

        oneSelect("risk_min");
        oneSelect("rule_status");
        oneSelect("abn_type");

        oneInput("file_size_limit");
        oneInput("file_num_hour");
        oneInput("rate_limit");
        oneInput("label");
        oneInput("device_id");



    }

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

        param["cacheMenu"] = "menu-rule3";///////!!!!!!!!!
        param["cacheType"]=1
        param["cachePolicy_type"] = policy_type///////!!!!!!!!!
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