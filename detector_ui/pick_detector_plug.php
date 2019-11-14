<?php
//require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
//require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_get_parameter_for_pick_plug_page.php');

?>


<!DOCTYPE html>
<html>
<head>
	<title>检测器生效范围</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<meta name="author" content="">

	<!-- Bootstrap core CSS -->
	<link href="css/bootstrap.css" rel="stylesheet">
	<link href="css/bootstrap-switch.css" rel="stylesheet">

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

	</style>
</head>
<body>
<div id="whole-wrapper">
	<div>
			<div class="row">
				<div class="pull-left margin_ddos1">
					<h4><span class="tab_color">|</span>&nbsp;&nbsp;检测器生效范围</h4>
				</div>

			</div>


		<div id="searchDiv" class="row btn-banner">
			<div class="dropdown dropdown-inline">
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

			<div class="dropdown btn-interval dropdown-inline">
				<button type="button" data-toggle="dropdown"
						class="btn dropdown-btn dropdown-menu-width"
						aria-haspopup="true"
						aria-expanded="false">
					<span id="device_status" class="pull-left" value="1">正常运行</span>
					<i class="fa fa-sort-down pull-right"></i>
				</button>
				<ul class="dropdown-menu dropdown-menu-width dropdown-list-style" id="ipslist">
					<li onclick="selectProtoFwd(this);" value="1">正常运行</li>
					<li onclick="selectProtoFwd(this);" value="0">所有状态</li>
					<li onclick="selectProtoFwd(this);" value="2">暂未审核</li>
					<li onclick="selectProtoFwd(this);" value="3">审核失败</li>
					<li onclick="selectProtoFwd(this);" value="4">认证失败</li>
					<li onclick="selectProtoFwd(this);" value="5">流量异常</li>
					<li onclick="selectProtoFwd(this);" value="6">系统异常</li>
					<li onclick="selectProtoFwd(this);" value="7">资源异常</li>
					<li onclick="selectProtoFwd(this);" value="8">策略异常</li>
				</ul>
			</div>

			<input id="device_id" type="text" class="form-control search-input btn-interval" placeholder="检测器ID(模糊搜索)">
			<input id="user" type="text" class="form-control search-input btn-interval" placeholder="部署单位(模糊搜索)">
			<button id="searchButton" type="button" class="btn btn-primary btn-interval"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
			<button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>


				<!-- value用于标记是否已经点击查询的逻辑 -->
			数量：<span id="totalcount" value="0" style="color: red;font-size: large;font-weight: bold">？</span>

		</div>


		<div class="clearfix"></div>
		<div id = "selected_detetors_original" class="row common_margin">

		</div>
		<div class="clearfix"></div>

		<div class="clearfix"></div>
		<div id = "selected_detetors" class="row common_margin">

		</div>
		<div class="clearfix"></div>




		<div class="row common_margin">
			<table id="maintable" class="table table-hover tbl_font_size "
				   style="border: 1px solid lightgray;border-collapse: inherit">
				<thead class="thead">
				<tr >
					<th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
					<!--<th width="2%"></th>-->
					<th width="10%">检测器编号</th>
					<th width="10%">生产厂商</th>
					<th width="10%">部署位置</th>
					<th width="10%">部署单位</th>
					<th width="10%">是否在线</th>
					<th width="10%">最后告警产生时间</th>
					<th width="10%">开启/关闭</th>
				</tr>
				</thead>

				<tbody>
				</tbody>

				<tfoot>
				<tr>
					<td><input type="checkbox" class="checkbox" id="chk_all2"></td>
					<td colspan="9">
						<div class="pull-left">

							<button class="btn btn-default btn-sm" id="refresh">刷新</button>
						</div>
						<div class="pull-right">

							<?php
							require_once(dirname(__FILE__) . '/require_page_bar_for_all_page.php');
							?>

<!--							<nav id="paginationbox">
								<span style="vertical-align:10px;">共有<strong id="totalcount2"></strong>条，每页显示：<strong>10</strong>条</span>
								<ul id="pagination" class="pagination pagination-sm" style="margin: 0%;"> </ul>
							</nav>-->
						</div>
					</td>
				</tr>

				</tfoot>
			</table>
		</div>


		<div id="issuedDiv" class="container-whole" style="text-align: center" >
			<div style="color:red;margin-bottom: 10px">请先选择检测器，才能进行提交</div>
			<button id="issuedButton" type="button" class="btn btn-lg btn-primary"><i class="fa fa-sign-out">&nbsp;&nbsp;</i>保存</button>
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
						检查器生效范围确认
					</h4>
				</div>
				<div class="modal-body" style="text-align: center">
					<p style="color: red">请确认是否提交生效范围变更</p>
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
	<script src="js/bootstrap-switch.js"></script>
	<script src="js/frame_detector.js"></script>
	<!--<script src="js/fileinput.min.js"></script>-->
	<script src="js/jquery.twbsPagination.min.js"></script>
	<script src="js/common.js"></script>

	<script type="text/javascript">
		buildFrame(cacheMenu);
		$(function () {
			console.log("执行js");

			//隐藏所有的命令
			//$(".order_hide").hide();
		});

		var globalSearchParam = {random:1,device_status:1}




		var globalSelectedDetetors = {}

		var globalSelectedDetetorsOriginal = {}

		//LoadPage(1,globalSearchParam)

		//alert(cacheDevice_id_list+' '+cacheDevice_id_list.length)

		if(cacheCmd_type ==3 || cacheCmd_type==999){

			globalSearchParam={random:1,device_status:1,device_ids:JSON.stringify(cacheDevice_id_list)}
			$("#searchDiv").hide();
			$("#issuedDiv").hide();
			$("#selected_detetors").hide();
			$("#chk_all1,#chk_all2").hide();
		}

		if(cacheCmd_type ==4){

			//globalSearchParam={random:1,device_status:1}

			$("#selected_detetors_original").hide();


		}
		if(cacheCmd_type!=999){
			$('#maintable thead tr th:last').hide();
		}
		if(cacheCmd_type==999){
			$('#maintable tfoot tr td:first').hide();
			$('#maintable thead tr th:first').hide();
		}

		if(cacheDevice_id_list.length>0){

			$.ajax({
				url: "/ajax_action_detector.php?uu=detector.show",
				type: "post",
				data: {device_ids:JSON.stringify(cacheDevice_id_list),pn:1,p_size:1000},
				success:function(data) {
					var ret = JSON.parse(data);

					if (ret["code"] == 200) {
						//alert("检查器生效范围变更成功");
						//$("#issuedButton").prop('disabled',"true");
						//pickDetectorBack();
						for (var i = 0; i < ret["msg"].length; i++) {
							globalSelectedDetetors[ ret["msg"][i].id] =  ret["msg"][i].device_id;

							globalSelectedDetetorsOriginal[ ret["msg"][i].id] =  ret["msg"][i].device_id;
						}

						//globalSelectedDetetorsOriginal=globalSelectedDetetors;

////////////////先取生效数组，再刷列表
						LoadPage(1,globalSearchParam)
						//selectedDetetorsRefresh();
///处理复选框全选
						//alterChkAll();

						//alterChkList();
					}else{
						alert("检查器范围获取失败");
					}
				}
			})

		}else{

			////////////////先取生效数组，再刷列表
			LoadPage(1,globalSearchParam)
		}


		function selectProtoFwd(obj) {
			$(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
			$(obj).parent().parent().find("span:first").text($(obj).text());
			//$("#"+id).attr("value",$(obj).attr("value"));
			// $("#"+id).text($(obj).text());
		}

		//    $('.cmdsingle').click(function () {
		////        $(this).siblings().removeClass("active");
		//        $('.cmdsingle').removeClass("active");
		//        $(this).addClass("active");
		//        $("#cmd").attr("value",$(this).attr("value"))
		//    })


		$("#searchButton").click(function(){


			// 取消下发按钮的disable
			//$("#issuedButton").removeAttr("disabled");

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
							$("<tr><td colspan='8' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
						}else if (ret["code"] == 9001){
							window.location.href = "login.php?ref="+window.location.href;
						}else{
							alert(ret["msg"]);
						}
					},
					beforeSend: function () {
						$("#maintable tbody tr").remove();
						$("#maintable tbody").append("<tr><td colspan='9'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
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



		$("#chk_all1,#chk_all2").click(function(){
			if(this.checked){
				$("table :checkbox").prop("checked", true);


				var lines = $("#maintable tbody tr");
				var checkboxs = lines.find("input:eq(0):checkbox:checked");
				checkboxs.each(function(){
					var device_id=$(this).parent().parent().find("td:eq(1)").text();
					globalSelectedDetetors[$(this).attr("id")] = device_id;

				})


			}else{


				var lines = $("#maintable tbody tr");
				var checkboxs = lines.find("input:eq(0):checkbox");
				checkboxs.each(function(){
					delete globalSelectedDetetors[$(this).attr("id")];

				})


				$("table :checkbox").prop("checked", false);

			}

			selectedDetetorsRefresh();


			alterChkList();
			///处理复选框全选
//			alterChkAll();
		});




		function List(msgListObj){

			var address_codeMap={'100000':'北京','200000':'上海','510000':'广州'};
			var device_statusMap={1:'正常运行',2:'暂未审核',3:'审核失败',4:'认证失败',5:'流量异常',7:'系统异常',8:'资源异常',9:'策略异常'};
			//var contractorMap={'01':'厂商1', '02':'厂商2', '03':'厂商3'};
			var imgMap = {
				1: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
				2: "<i class='fa fa-circle' style='color:#5BC0DE; font-size:xx-small ' />",
				3: "&nbsp;&nbsp;<span style='background: #FF9900;padding: 3px;border-radius: 5px; color: white'>置顶</span>"
			}

			var device_status_imgMap = {
				1: "<i class='fa fa-circle' style='color:#5BC0DE; font-size:xx-small ' />",
				2: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
				3: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
				4: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
				5: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
				6: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
				7: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
				8: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>"

			}



			//var _row = $("#content").clone();
			//$("#content").remove();
			$("#maintable tbody tr").remove();
			var plug_on_status_td = cacheCmd_type == 999?"<td></td>":"<td style='display:none'></td>";
			var chk = cacheCmd_type == 999?"<td style='display:none'></td>":"<td></td>";
			var _row = $("<tr>"+chk+"<td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td>"+plug_on_status_td+"</tr>");

			for (var i = 0; i < msgListObj.length; i++) {
				var row = _row.clone();
				$.fn.bootstrapSwitch.defaults.size = 'mini';
            	$.fn.bootstrapSwitch.defaults.onText = '开启';
            	$.fn.bootstrapSwitch.defaults.offText = '关闭';
				var imghtml = '';
				var titlehtml = "<a target= _blank href = 'detector_detail.php?id="+msgListObj[i].id+"' style='color:#000000'>"+msgListObj[i].device_id+"</a>";
				var switchhtml = "";
				if(cacheCmd_type == 999){
					var checked = cachePlug_on_device_status[msgListObj[i].id] == "1" ? "checked" : "";
				    switchhtml = "<div><input name='my-checkbox' type='checkbox' id="+msgListObj[i].id+"  "+checked+" /></div>";
				}
				

				//row.attr("id",msgListObj[i].id)
				// row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>")
				//  row.find("td:eq(1)").text(msgListObj[i].id);
//            row.find("td:eq(1)").html(device_status_imgMap[msgListObj[i].device_status]+titlehtml);
				//var row = _row.clone();row.attr("id",msgListObj[i].id)
				//if(globalSelectedDetetors[msgListObj[i].id]==undefined){
				// row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+">");
				//}else{

					row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' checked='checked' id="+msgListObj[i].id+">");
				//}


				row.find("td:eq(1)").html(msgListObj[i].device_id);
				row.find("td:eq(2)").text(contractorMap[msgListObj[i].contractor]);
				row.find("td:eq(3)").html(address_codeMap[msgListObj[i].address_code]?address_codeMap[msgListObj[i].address_code]:"未知地区");
				row.find("td:eq(4)").html(msgListObj[i].organs);
                row.find("td:eq(5)").html(isonlineFormat_new(msgListObj[i].is_online));
				row.find("td:eq(6)").text(msgListObj[i].last_warning_time);
				row.find("td:eq(7)").html(switchhtml);

				row.show();
				row.appendTo("#maintable tbody");


			}

			$("[name='my-checkbox']").bootstrapSwitch({
				onText:"开启",
				offText:"关闭",
				onColor:"success",
				offColor:"info",
				size:"mini",
				onSwitchChange:function(event,state){
					var type=0
					var module = $(this).parent();
					var select_obj = module.find("[name='my-checkbox']");
					
					var id = select_obj.attr("id")

					/*if(state==true){
						//$(this).val("1");
						alert('检查器将开启')
						var comment=prompt("请输入备注","");
						if(comment==null)
						{
							type=0
							refresh()
						}
						else {
							type=1
							$.ajax({
								url: "/ajax_action_detector.php?uu=detector.alert",
								type: "post",
								data: {id:id,type:type,comment:comment},
								success:function(data) {
									var ret = JSON.parse(data);
									if(ret.code == 200){
										alert("状态切换成功");

									}else{
										alert("状态切换失败");
									}
								}
							})
						}
					}else{
						alert('检查器将禁用')
						var comment=prompt("请输入备注","");
						if(comment==null)
						{
							type=1
							refresh()
						}
						else {
							type=0
							$.ajax({
								url: "/ajax_action_detector.php?uu=detector.alert",
								type: "post",
								data: {id:id,type:type,comment:comment},
								success:function(data) {
									var ret = JSON.parse(data);
									if(ret.code == 200){
										alert("状态切换成功");

									}else{
										alert("状态切换失败");
									}
								}
							})
						}
					}*/

					if(state==true){
						var r = confirm('是否对该检测器开启当前插件？');
						if(r){
							submitPlugOnDeviceStatus(id);
						}else{
							return false;
						}
					}else{
						var r = confirm('是否对该检测器关闭当前插件？');
						if(r){
							submitPlugOnDeviceStatus(id);
						}else{
							return false;
						}
					}
				}

        })

// 提交检测器开关
function submitPlugOnDeviceStatus(id){
	/*
	传参:
		id-当前插件id，直接获取
		detector_id_list-当前检测器列表，直接获取
		plug_on_device_status-修改后的开启/关闭列表
	*/
	issuedParam = {random:1}
//	issuedParam["id"] = JSON.stringify(cacheId)[1];
	issuedParam["id"] = cacheId[0];
	//issuedParam["detector_id_list"] = JSON.stringify(cacheDevice_id_list);
	console.log(cachePlug_on_device_status)
	var currentPlugOnDeviceStatus = cachePlug_on_device_status;
	var deviceCheck = $('#maintable tbody tr input[name=my-checkbox]');
	// 这里有问题，应该是只拿当前操作的那个检测器的id的值，现在循环以后值会被改
	// $.each(deviceCheck,function(){
	// 	if($(this).prop('checked')){
	// 		currentPlugOnDeviceStatus[$(this).attr('id')] = "1";
	// 		issuedParam["operate"] = "1";
	// 	}else{
	// 		currentPlugOnDeviceStatus[$(this).attr('id')] = "0";
	// 		issuedParam["operate"] = "0";
	// 	}
	// })
	// 
	if($('#maintable tbody tr input[name=my-checkbox][id='+id+']').prop('checked')){
		issuedParam["operate"] = "1";
	}else{
		issuedParam["operate"] = "0";
	}
	console.log(currentPlugOnDeviceStatus)
	// issuedParam["plug_on_device_status"] = JSON.stringify(currentPlugOnDeviceStatus);
	issuedParam["detector_id"] = id
	console.log(issuedParam)
	$.ajax({
		url: "/ajax_action_detector.php?uu=plugin.plug_start_stop", //这里改成对应的后台的url
		type: "post",
		data: issuedParam,
		success: function (data) {
			var ret = JSON.parse(data);
			if (ret["code"] == 200) {
				var r=confirm('是否返回插件部署页?');
				if(r)
					pickDetectorBack();
			}else{
				alert("关闭失败");
				cachePlug_on_device_status[id]=="1"?cachePlug_on_device_status[id] = "0":cachePlug_on_device_status[id] = "1";
				refresh();
			}
		}
	})
}


///绑定复选框选择事件
			$("#maintable tbody tr :checkbox").click(function(){
				//alert("333333333333333");
				if(cacheCmd_type == 999){
					return;
				}

				if(this.checked){
					//$("table :checkbox").prop("checked", true);
					// selected_detetors
					//$("#selected_detetors").remove();

					//this.id
					var id=$(this).attr('id');
					var device_id=$(this).parent().parent().find("td:eq(1)").text();
					//device_id.appendTo("#selected_detetors");
					//alert(device_id);
					globalSelectedDetetors[id] = device_id;
					//console.log(globalSelectedDetetors);
					//$("#selected_detetors").append(device_id+" ");

					// $("#selected_detetors").refresh();
				}else{

					var id=$(this).attr('id');
					delete globalSelectedDetetors[id];
					//console.log(globalSelectedDetetors);
					//globalSelectedDetetors
					//$("table :checkbox").prop("checked", false);
				}

				selectedDetetorsRefresh();


//				alterChkList();
// /处理复选框全选
				alterChkAll();
			});


			selectedDetetorsRefresh();


			alterChkList();
///处理复选框全选
			alterChkAll();
			/*
			 $("tbody tr a").click(function () {
			 console.log("test")
			 window.location.href = "message_detail.php?id="+$(this).parent().parent().attr("id");
			 })
			 */
		}


		////刷新选中列表
		function selectedDetetorsRefresh(){

			//globalSelectedDetetorsOriginal

			$("#selected_detetors").empty();

			$("#selected_detetors_original").empty();


			$("#selected_detetors_original").append("<strong>当前生效检测器"+Object.keys(globalSelectedDetetorsOriginal).length+"：</strong> ")
			$("#selected_detetors").append("<strong>变更生效检测器"+Object.keys(globalSelectedDetetors).length+"：</strong> ")

			for (var key in globalSelectedDetetorsOriginal){
				// console.log("属性：" + key + ",值："+ globalSelectedDetetors[key]);
				//$("#selected_detetors").append("<img src='images/del.gif' onclick='delId(" + key + ")'>"+key+" "+globalSelectedDetetors[key]+" ");


				if(globalSelectedDetetors[key]==undefined){
					$("#selected_detetors_original").append("<span style='color:red'><s>"+globalSelectedDetetorsOriginal[key]+"</s></span>");
					$("#selected_detetors_original").append("<span style='color:red'>删除</span>&nbsp;&nbsp;&nbsp;&nbsp;")
				}else{
					$("#selected_detetors_original").append(""+globalSelectedDetetorsOriginal[key]+"");
					$("#selected_detetors_original").append("原有&nbsp;&nbsp;&nbsp;&nbsp;")
				}


			}



			for (var key in globalSelectedDetetors){
				// console.log("属性：" + key + ",值："+ globalSelectedDetetors[key]);
				//$("#selected_detetors").append("<img src='images/del.gif' onclick='delId(" + key + ")'>"+key+" "+globalSelectedDetetors[key]+" ");

				$("#selected_detetors").append("<img src='images/del.gif' onclick='delId(" + key + ")'>"+globalSelectedDetetors[key]+"");
				if(globalSelectedDetetorsOriginal[key]==undefined){

					$("#selected_detetors").append("<span style='color:blue'>新增</span>&nbsp;&nbsp;&nbsp;&nbsp;")
				}else{
					$("#selected_detetors").append("原有&nbsp;&nbsp;&nbsp;&nbsp;")
				}


			}
			//alert("333333333333333");

		}
/*
		///处理复选框全选
		function alterChkAll(){
			var lines = $("#maintable tbody tr");
			var uncheckboxs = lines.find("input:eq(0):checkbox:not(:checked)");

			//console.log(uncheckboxs.size())
			if(uncheckboxs.size() == 0){

				$("#chk_all1,#chk_all2").prop("checked", true);
			}else{

				$("#chk_all1,#chk_all2").prop("checked", false);

			}
		}*/


		///处理复选框列表
		function alterChkList(){
			var lines = $("#maintable tbody tr");
			var checkboxs = lines.find("input:eq(0):checkbox");

			//if(checkboxs.size()>0)
			checkboxs.each(function(){
				//if($("#"+id).length){
					if(globalSelectedDetetors[$(this).attr("id")]==undefined){
						$(this).prop("checked", false);
						//$("#"+id).prop("checked", false);
					}else{
						$(this).prop("checked", true);
						//$("#"+id).prop("checked", true);
					}
				//}
				//carray.push(parseInt($(this).attr("id")))
			})

			if(cacheCmd_type ==3){

				//$(":checkbox").hide();
				//checkboxs.hide();
				checkboxs.attr('disabled',true)
			}

		}


		///删除小图片事件
		function delId(id){
			//var id=$(this).attr('id');
			delete globalSelectedDetetors[id];

			/// $("#maintable tbody tr");

			$("#"+id).prop("checked", false);


			selectedDetetorsRefresh();


			alterChkList();
			///处理复选框全选
			alterChkAll();
		}


		function LoadPage(currentPage,searchParam){
			$.ajax({
				url: "/ajax_action_detector.php?uu=detector.count",
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
					$("#totalcount").attr("value",1);
					$("#totalcount2").text(ret);
					$('#pagination').empty();
					$('#pagination').removeData("twbs-pagination");
					$('#pagination').unbind("page");
					pagination(ret,"/ajax_action_detector.php?uu=detector.show&p_size="+p_size,parseInt(currentPage),searchParam)



				},
				beforeSend: function () {
					$(".loading-pic").removeClass("hidden");
				},
				error: function () {
					alert("无法连接服务器");
				}
			})
		}

		$("#clearButton").click(function(){
			firstSelect("contractor");
			firstSelect("address_code");
			firstSelect("device_status");
			$("#device_id").val("");
			$("#user").val("");
		})

		$("#issuedButton").click(function(){


			//校验判断
			var error_str = ""
			/*        if( $("#totalcount").attr("value") == 0){
			 error_str+="请先查询检测器\n";
			 }*/


			/*        if($("#totalcount").text() == "0"){
			 error_str+="下发的检测器数量不能为0\n";
			 }
			 if(($("#start_module").attr("value") == $("#stop_module").attr("value"))&&
			 $("#start_module").attr("value")!=0 && $("#stop_module").attr("value")!=0){
			 error_str+="开启模块和关闭模块不能相同\n";
			 }*/


			///构造id_list
			var carray =new Array()
			for (var key in globalSelectedDetetors){
//				carray.push(parseInt(key))
				carray.push(parseInt(globalSelectedDetetors[key]))
			}
			console.log(carray.length)

			if(carray.length==0){

				error_str+="选择的检测器数量不能为0\n";

			}


			if(error_str!=""){
				alert(error_str);
			}else{
				//$('#hintModal p:eq(1)').html("选择的命令是："+cmd_type_map[cmd]);
				//$('#hintModal p:eq(2)').html("下发的检测器个数："+$("#totalcount").text());
				$('#hintModal p:eq(2)').html("选择的检测器个数："+carray.length);


				$('#hintModal').modal('show')
			}
		})

		$("#issueSubmit").click(function(){


			// globalSearchParam = {random:1,register_ce_type:rct,is_online:ison}
			issuedParam = {random:1}

			// issuedParam["policy_type"] = cachePolicy_type;

			//var ids =new Array()
			//ids.push(parseInt(cacheId))
			issuedParam["id"] = JSON.stringify(cacheId);


			///构造id_list
			var carray =new Array()
			for (var key in globalSelectedDetetors){
//				carray.push(parseInt(key))
                carray.push(parseInt(globalSelectedDetetors[key]))
			}
			issuedParam["detector_id_list"] = JSON.stringify(carray)


			//alert("cacheCmd_type:"+cacheCmd_type)

			var cmd_str=1;
			if(cacheCmd_type ==1){

				cmd_str="change_plug"

			}else if(cacheCmd_type ==2){

				cmd_str="append_plug"

			}else if(cacheCmd_type ==3){

				cmd_str="change_view"

			}else if(cacheCmd_type ==4){

				cmd_str="plug_synchronization"


				issuedParam["type"] = 1

				delete issuedParam["id"]
			}




            //alert(cmd_str)

			if(cacheCmd_type ==1 || cacheCmd_type ==2 || cacheCmd_type ==4) {
				$.ajax({
					url: "/ajax_action_detector.php?uu=plugin." + cmd_str,
					type: "post",
					data: issuedParam,
					success: function (data) {
						var ret = JSON.parse(data);

						if (ret["code"] == 200) {
							if(cacheCmd_type ==4){
								
								alert("全量下发成功");
							}else{
								alert("检查器生效范围变更成功");
							}
							
							
							//$("#issuedButton").prop('disabled',"true");
							pickDetectorBack();
						} else {
							
							if(cacheCmd_type ==4){
								
								alert("全量下发失败");
							}else{
								
								alert("检查器生效范围变更失败");
							}
							
						}
					}
				})
			}




			$("#hintModal").modal('hide');
		})


	</script>
</body>
</html>


<!--<div id="page" style="border-style:dashed;border-color:#e4e4e4;line-height:30px;background:url(sorry.png) no-repeat right;">
	<h1>抱歉，找不到此页面~</h1>
	<h2>Sorry, the site now can not be accessed. </h2>
	<font color="#666666">你请求访问的页面，暂时找不到，我们建议你返回首页进行浏览，谢谢！</font><br /><br />
	<div class="button">
		<a href="javascript:void(0);" title="进入首页"  onclick="pickDetectorBack()" target="_blank">进入首页</a>
	</div>
</div>-->



<script>

	function pickDetectorBack(){

		//var

		var param= {}
		param["cachePage"] = cachePage
		param["cacheSearchParam"] = JSON.stringify(cacheSearchParam)



		post(cacheRef,param);

	}

</script>




</body>
</html>
