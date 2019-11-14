<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__).'/data/get.json.from.server.php');
require_once(dirname(__FILE__).'/service/service.php');

//$user = new User();
//$user = checkLogin(1, 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);
//$msgList = getCommonById("getSealMsgListByUserId", "user_id", $user->getId());
//$msgCount = getCommonById("getSealMsgCountByUserId", "user_id", $user->getId());
//$newsList = getCommon("getFreshNewsByTop");
//$FileNum=getCommonPlus("getHDFSFileNum.log",null);
//$FileSysStatus=getCommonPlus("getHDFSFileSysStatus.log",null);

?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>概览</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

    <!-- Add custom CSS here -->
    <link href="css/frame.css" rel="stylesheet">
	<link href="css/entrance.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
	<style>

	</style>
  </head>

  <body>

    <div id="whole-wrapper">

      <div class="page-wrapper">
		<div class="page-wrapper-left">
			<div class="user-padding">
				<div class="user-wrapper row clearfix">
					<div class="col-xs-2 img-middle">
						<span>
							<img src="images/ruiduncloud.png" style="width:55%; min-width:70px;">
							<!--<h5><strong>######<script src="/ajax_action.php?uu=getHDFSFileSysStatus.log"></script></strong></h5>-->
							<!--<h5><strong>######</strong></h5>-->
							<!--<h5><small>#########</small></h5>-->
						</span>
					</div>

					<div class="col-xs-3">
						<div class="reminder-title"><h5><small>大数据平台概览：</small></h5></div>
						<div class="reminder-content" id = 'reminder-content1'></div>
						<div class="reminder-content" id = 'reminder-content2'></div>
						<!--<div class="reminder-entrance"><a href="#">点击查看</a></div>-->
					</div>
					<div class="col-xs-5">
						<div class="reminder-title"><h5><small>集群状态概览：</small></h5></div>
						<div class="reminder-content" id = 'reminder-content3'>3</div>
						<div class="reminder-content" id = 'reminder-content4'>4</div>
					</div>
				</div>
			</div>
			<div class="product-padding">
				<div class="product-wrapper row">
					<div class="product-head">
						<span style="font-size: large">集群运行状态</span>
					</div>

					<div id="cluster-state" style="margin:0px 20px">
						<div class="col-lg-4 col-sm-4 price-wrapper">
							<div class="pricing-table most-popular">
								<div class="pricing-head">
									<h1>主机名:master</h1>

								</div>
								<ul class="list-unstyled">
									<li>状态：运行中</li>
									<li>已用内存：2048MB</li>
									<li>剩余内存：6144MB</li>
									<li>已用核数：1</li>
									<li>未用核数：7</li>
								</ul>
								<div class="price-actions">
									<a href="javascript:;" class="btn">点击查看</a>
								</div>
							</div>
						</div>

						<div class="col-lg-4 col-sm-4 price-wrapper">
							<div class="pricing-table">
								<div class="pricing-head">
									<h1>#######</h1>
								</div>
								<ul class="list-unstyled">
									<li>#############</li>
									<li>#############</li>
									<li>#############</li>
									<li>#############</li>
								</ul>
								<div class="price-actions">
									<a href="javascript:;" class="btn">立即开启</a>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="product-padding">
				<div class="product-wrapper row">
					<div class="product-head">
						<span style="font-size: large">任务运行状态</span>
					</div>

					<div id="job-state" style="margin:0px 20px">

					</div>
				</div>
			</div>
		</div>
		<div class="page-wrapper-right">
			<div class="ads-padding">
				<div class="ads-wrapper">
					<div id="ad-one" class="ad-wrapper">
						<a href="#"><img src="images/ad1.jpg" style="height:90px;"></a>
					</div>
					<div id="ad-two" class="ad-wrapper">
						<a href="#"><img src="images/ad2.jpg" style="height:90px;"></a>
					</div>
				</div>
			</div>
			<div class="time-line-padding">
				<div class="time-line-wrapper row">
					<div class="product-head">
						<span>最新消息</span>
					</div>
					<div class="timeline-note user-news">
						<ul>
						  <li><a href="#"><span>[2016-5-4]</span>  &nbsp产品到期提醒</a></li>
						  <li><a href="#"><span>[2016-5-3]</span>  &nbsp产品到期提醒</a></li>
						  <li><a href="#"><span>[2016-5-3]</span>  &nbsp产品到期提醒</a></li>
						  <li><a href="#"><span>[2016-5-3]</span>  &nbsp产品到期提醒</a></li>
						  <li><a href="#"><span>[2016-5-3]</span>  &nbsp产品到期提醒</a></li>
						  <li><a href="#"><span>[2016-5-2]</span>  &nbsp产品到期提醒</a></li>
						</ul>
						<div><a href="#">更多</a></div>
					</div>
					<div class="product-head">
						<span>公司动态</span>
					</div>
					<div class="timeline-note work-news">
						<ul>
						  <li><a href="#"><span class="head-news">头条</span>  &nbsp身边的网络专家</a></li>
						  <li><a href="#"><span class="hot-news">热点</span>  &nbsp身边的网络专家</a></li>
						  <li><a href="#"><span class="hot-news">热点</span>  &nbsp身边的网络专家</a></li>
						  <li><a href="#"><span class="hot-news">热点</span>  &nbsp身边的网络专家</a></li>
						  <li><a href="#"><span></span>  &nbsp身边的网络专家</a></li>
						  <li><a href="#"><span></span>  &nbsp身边的网络专家</a></li>
						</ul>
						<div><a href="#">更多</a></div>
					</div>
				</div>
			</div>
		</div>
		<div class="summary-copyright">
		</div>
      </div><!-- /#page-wrapper -->

    </div><!-- /#wrapper -->

    <!-- JavaScript -->
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.js"></script>

	<script>
	$(function() {
		buildFrame("summary");

		$('.summary-copyright').html(COPYRIGHT);

		

		//$('.reminder-content').html("<span>"+FileNum["filenum"]+"</span>个文件<br/>硬盘空间<span>"+FileSysStatus["capacity"]+"</span>GB<br/>可用空间<span>"+FileSysStatus["remaining"]+"</span>GB");
	});

	$.ajax({
		//url: "http://192.168.120.175/doSqlForLog.log",
		url: "/ajax_action.php?uu=getHDFSFileNum.log",
		type: "post",
		data: null,
		//sqlvalue
		success:function(data) {

			//console.log(data)
			var ret = JSON.parse(data);

			$('#reminder-content1').html("<span>"+ret["filenum"]+"</span>个文件");
			//var ret = JSON.parse(data);
		},
	});

	$.ajax({
		//url: "http://192.168.120.175/doSqlForLog.log",
		url: "/ajax_action.php?uu=getHDFSFileSysStatus.log",
		type: "post",
		data: null,
		//sqlvalue
		success:function(data) {

			//console.log(data)
			var ret = JSON.parse(data);

			$('#reminder-content2').html("硬盘空间<span>"+ret["capacity"]+"</span>GB<br/>可用空间<span>"+ret["remaining"]+"</span>GB");
			//var ret = JSON.parse(data);
		},
	});

	$.ajax({
		//url: "http://192.168.120.175/doSqlForLog.log",
		url: "/ajax_action_spark.php?uu=ws/v1/cluster/nodes",
		type: "post",
		data: null,
		//sqlvalue
		success:function(data) {

			//console.log(data);
			var ret = JSON.parse(data);
			var str = ""

			$('#reminder-content3').html("集群节点总共有<span>"+ret.nodes.node.length+"</span>个");

			for(var i=0;i<ret.nodes.node.length;i++){
				var _state = ret.nodes.node[i].state=="RUNNING"?"most-popular":"";
				str = str +
					"<div class='col-lg-4 col-sm-4 price-wrapper'>"+
						"<div class='pricing-table "+_state+"'>"+
							"<div class='pricing-head'>"+
								"<h1> <span style='color:black'>主机名:"+ret.nodes.node[i].nodeHostName+"</span></h1>"+
							"</div>"+
							"<ul class='list-unstyled'>"+
								"<li>状态："+ret.nodes.node[i].state+"</li>"+
								"<li>已用内存："+ret.nodes.node[i].usedMemoryMB+"MB</li>"+
								"<li>剩余内存："+ret.nodes.node[i].availMemoryMB+"MB</li>"+
								"<li>已用核数："+ret.nodes.node[i].usedVirtualCores+"</li>"+
								"<li>未用核数："+ret.nodes.node[i].availableVirtualCores+"</li>"+
							"</ul>"+
							"<div class='price-actions'>"+
								"<a href='javascript:;' class='btn'>点击查看</a>"+
							"</div>"+
						"</div>"+
					"</div>";
			}
			$("#cluster-state").html(str)
			//$('#reminder-content2').html("硬盘空间<span>"+ret["capacity"]+"</span>GB<br/>可用空间<span>"+ret["remaining"]+"</span>GB");
			//var ret = JSON.parse(data);
		},
	});


	$.ajax({
		//url: "http://192.168.120.175/doSqlForLog.log",
		url: "/ajax_action_spark.php?uu=ws/v1/cluster/apps",
		type: "post",
		data: null,
		//sqlvalue
		success:function(data) {

			console.log(data)
			var ret = JSON.parse(data);

			var running_num = 0;
			var str = ""
			for(var i=0;i<ret.apps.app.length;i++){
			    var _state = ret.apps.app[i].state=="RUNNING"?"most-popular":"";
				if(ret.apps.app[i].state=="RUNNING"){
					running_num +=1;
				}

				str = str +
						"<div class='col-lg-4 col-sm-4 price-wrapper'>"+
						"<div class='pricing-table "+_state+"'>"+
						"<div class='pricing-head'>"+
						"<h1><span style='color:black'>任务id:"+ret.apps.app[i].id.split('_')[2]+"</span></h1>"+
						"</div>"+
						"<ul class='list-unstyled'>"+
						"<!--<li>id："+ret.apps.app[i].id+"</li>-->"+
						"<li>任务名："+ret.apps.app[i].name+"</li>"+
						"<li>状态："+ret.apps.app[i].state+"</li>"+
						"<li>进度："+ret.apps.app[i].progress+"%</li>"+
						"<li>开始时间："+getLocalTime(ret.apps.app[i].startedTime)+"</li>"+
						"<li>结束时间："+(ret.apps.app[i].finishedTime==0?"未结束":getLocalTime(ret.apps.app[i].finishedTime))+"</li>"+
						"</ul>"+
						"<div class='price-actions'>"+
						"<a href='javascript:;' class='btn'>点击查看</a>"+
						"</div>"+
						"</div>"+
						"</div>";
			}

			$('#reminder-content4').html("正在运行任务有<span>"+running_num+"</span>个");

			$("#job-state").html(str);
		},
	});

	function getLocalTime(nS) {
		return new Date(parseInt(nS)).format("yyyy-MM-dd hh:mm:ss");//
	//	return new Date(parseInt(nS)).toLocaleString().replace(/:\d{1,2}$/,' ');
//		var now = new Date(parseInt(nS));
//		var nowStr = now.format("yyyy-MM-dd hh:mm:ss");
//		return nowStr;

	}

	Date.prototype.format = function(format){
		var o = {
			"M+" : this.getMonth()+1, //month
			"d+" : this.getDate(), //day
			"h+" : this.getHours(), //hour
			"m+" : this.getMinutes(), //minute
			"s+" : this.getSeconds(), //second
			"q+" : Math.floor((this.getMonth()+3)/3), //quarter
			"S" : this.getMilliseconds() //millisecond
		}

		if(/(y+)/.test(format)) {
			format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
		}

		for(var k in o) {
			if(new RegExp("("+ k +")").test(format)) {
				format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
			}
		}
		return format;
	}
	</script>
	<script src="js/frame.js"></script>
  </body>
</html>