<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__).'/data/get.json.from.server.php');
require_once(dirname(__FILE__).'/service/service.php');

require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');

//$user = new User();
//$user = checkLogin(1, 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);
//$msgList = getCommonById("getSealMsgListByUserId", "user_id", $user->getId());
//$msgCount = getCommonById("getSealMsgCountByUserId", "user_id", $user->getId());
//$newsList = getCommon("getFreshNewsByTop");
//$FileNum=getCommonPlus("getHDFSFileNum","log",null);
//$FileSysStatus=getCommonPlus("getHDFSFileSysStatus","log",null);

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
    <!-- <link href="css/server.css" rel="stylesheet"> -->
    <link href="css/frame.css" rel="stylesheet">
	<link href="css/entrance.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
	<style>
        .chart-row{
            border:solid 1px #E1E6EB;
            margin-left: 15px;
            margin-right: 0px;
            margin-bottom: 15px;
        }

        .chart-size{
            width: auto;height: 200px; /* width: 1080px;height:270px; */
        }

        .sub-title{
            background-color: #F5F6FA;
            font-weight: bold;
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
        .mainCountPanel{
            height: 768px;
            overflow: auto;
            text-align: left;
            display: flex;
            justify-content: space-around;
        }
        .mainCountPanel>div{
            border: 1px solid gray;
        }
        .mainCountPanel>div:nth-child(1){
            width:40%;
            height:100%;

        }
        .mainCountPanel>div:nth-child(2){
            width:55%;
            height:100%;
            
        }
        .countPanelTitle{
            font-size: 16px;
            font-weight: bold;
            color: #428bca;
            text-align: center;
            padding: 5px;
        }
        #riskCount,#trendAlarm,#deviceNum{
            width:100%;
            height: 30%;
            
        }
        .highlightValue{
            font-size: 24px;
            font-weight: bold;
            color: orange;
        }
        .countLabel{
            text-align: center;
        }
        .countLabel>span{
            margin-right: 10px;
        }
        #typeCount,#ruleTask{
            width:100%;
            height: 48%;
            
        }

        .devicePanel{
            height:300px;
            display: flex;
            justify-content: space-around;
            margin-left: 15px;
            margin-right: 15px;
            margin-top: 15px;
            border: 1px solid gray;
        }
        #nodeNum, #centerNum{
            width: 30%;
            height: 100%;   
        }
        .container-left,.container-right{
        	width:100%;
        	height:150px;
        }
        .table{
        	margin-left: 50px;
        	margin-top:0px;
        	width: 300px; 
        	background-color: white;
        }
	</style>
  </head>

  <body>

    <div id="whole-wrapper">

      <div class="page-wrapper">

			<div class="user-padding">

				<div class="user-wrapper row clearfix">
					<div style="height: 50px;line-height: 50px;margin: 0 20px;border-bottom: 1px solid #eaedf1;font-weight: bold;">系统总览</div>
					<div style="padding: 0 10px;">
						<div class="col-xs-3">
							<div class="reminder-title"><h5>检测器概览：</h5></div>
							<div class="reminder-content">共<span id="detector-num">60</span>台检测器，<span>3</span>台运行异常</div>
							<div class="reminder-entrance"><a href="detector.php">点击查看</a></div>
						</div>
						<div class="col-xs-3">
							<div class="reminder-title"><h5>告警概览：</h5></div>
							<div class="reminder-content">共有告警<span id="alarm-num">40</span>条，今日新增<span>3</span>条</div>
							<div class="reminder-entrance"><a href="alarm.php">点击查看</a></div>
						</div>
						<div class="col-xs-3">
							<div class="reminder-title"><h5>策略概览：</h5></div>
							<div class="reminder-content">共有<span>17</span>类，共计<span>40</span>条策略</div>
							<div class="reminder-entrance"><a href="rule_task.php">点击查看</a></div>
						</div>
						<div class="col-xs-3">
							<div class="reminder-title"><h5>审核概览：</h5></div>
							<div class="reminder-content">共有未审核<span id="alarm-num">40</span>条，今日新增<span>3</span>条</div>
							<div class="reminder-entrance"><a href="detector.php">点击查看</a></div>
						</div>
					</div>
				</div>
			</div><!-- user-padding -->
			<div class="product-padding">
                <div class="table">
                    <div class="widget-header widget-header-index">
                        <div class="title widget-header-index-title">
                            告警级别统计
                        </div>
                    </div>
                    <div class="widget-body">
                        <div style=" border: 1px solid #e1e6eb;">
                            <div id = "attacked-risk-div" class="chart-size"></div>
                            <div align="center">
                                <p class="img-text">告警级别统计图</p>
                                <p class="img-text2">(amount/risk)</p>
                            </div>
                        </div>
                    </div>
                </div>
			</div><!-- product-padding -->
		<div class="summary-copyright"></div>
      </div><!-- /#page-wrapper -->

    </div><!-- /#whole-wrapper -->

    <!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/libs/echarts.min.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<link href="css/bootstrap-select.css" rel="stylesheet">
<script type="text/javascript" src="js/bootstrap-select.js"></script>


<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>
	<script>
	// 告警级别统计
var initRiskCount = function(){
    var yData = ['无风险', '一般级', '关注级', '严重级', '紧急级'];
    var xData = [0,0,0,0,0];
    var option = {
    title: {
        text: '告警级别'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: null // 默认为直线，可选为：'line' | 'shadow'
        },
        formatter: '<div style="text-align: center;">告警级别</div>{b} : {c}'
    },
    grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
    xAxis: [{
        type: 'value',
        axisLabel: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLine: {
            show: false
        },
        splitLine: {
            show: false
        }

    }],
    yAxis: [{
        type: 'category',
        boundaryGap: true,
        axisTick: {
            show: true
        },
        axisLabel: {
            interval: null
        },
        data: yData,
        splitLine: {
            show: false
        }
    }],
    series: [{
        name: '',
        type: 'bar',
        barWidth: 25,
        label: {
            normal: {
                show: true,
                position: 'right'
            }

        },
        data: xData
    }]
}; 

// riskChart = echarts.init($('#riskCount')[0]);
// riskChart.setOption(option);
window.addEventListener('resize',function(){
    riskChart.resize();
})
}


//告警级别统计表
function construct_risk(data){
    var riskMap = {
        '-1':'未知',
        0:'无风险',
        1:'一般级',
        2:'关注级',
        3:'严重级',
        4:'紧急级'
    }
    var arr1 = new Array();
    var arr2 = new Array();

    for(var i=0;i<data.length;i++){
        //arr1[i] = data[i].amount
        //arr2[i] = riskMap[data[i].risk]
        if(data[i].risk!=-1){
            var obj = {'name':riskMap[data[i].risk],'value':data[i].amount};
            risk_option.series[0].data.push(obj);
        }
    }

    risk_chart.setOption(risk_option);
}



	initRiskCount();
	var risk_chart = echarts.init(document.getElementById('attacked-risk-div'));
	function get() {
        // 告警级别
            $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data:{query_condition:'risk'},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                construct_risk(ret.msg);
                }
            });
    }


	$.ajax({
		url: "/ajax_action_detector.php?uu=alarm.count",
		type: "post",
		data: null,
		success:function(data) {
			var ret = JSON.parse(data);
			if (ret["code"] == 200)
				ret = ret["msg"]["count"]
			else {
				ret = 0;
			}
			$("#alarm-num").text(ret);
		}
	})

	$.ajax({
		url: "/ajax_action_detector.php?uu=detector.count",
		type: "post",
		data: null,
		success:function(data) {
			var ret = JSON.parse(data);
			if (ret["code"] == 200)
				ret = ret["msg"]["count"]
			else {
				ret = 0;
			}
			$("#detector-num").text(ret);
		}
	})


	// $(function() {
	// 	buildFrame("summary");

	// 	var map_chart = echarts.init(document.getElementById("map-div"));
	// 	map_chart.setOption(map_option);
	// 	window.onresize = function(){
	// 		map_chart.resize();
	// 	}
	// 	$('.summary-copyright').html(COPYRIGHT);
	// });
	</script>
	<script src="js/frame_detector.js"></script>
	<script src="js/index.js"></script>
  </body>
</html>