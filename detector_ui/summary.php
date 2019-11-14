<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__).'/data/get.json.from.server.php');
require_once(dirname(__FILE__).'/service/service.php');

require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');
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
        .charts {
            position: absolute;
            padding: 5px;
            /*border-radius: 10px;*/
            border: 1px dotted rgba(255,255,255,0.3);
            box-shadow: rgba(255,255,255,0.2) 1px 1px 5px;
            animation: glow 1000ms ease-out infinite alternate;
        }
        .modalTitle {
            text-decoration-style: none;
            font: 14px bold;
            cursor: pointer;
            background: url(./images/ui/modalHead.png);
            background-size: 100% 100%;
            height: 26px;
            padding: 3px 10px;
            margin-bottom: 4px;
            width: 100%;
            color: yellow;
        }

        .modalBorder {
            height: calc(100% - 26px);
            color: white;
            font-size: 14px;
            padding: 2px;
            /*border: 1px solid rgb(24, 185, 255);
            box-shadow: rgb(0,255,255) 1px 1px 5px;
            animation: glow 1000ms ease-out infinite alternate;*/
        }

        .modalBody {
            height: 100%;
            background-color: rgba(1, 25, 35, 0.3) !important;
        }
        @-webkit-keyframes glow {
            0% {
                /*border-color: rgba(0, 229, 255, 0.73);*/
                /*box-shadow: 0 0 5px rgb(0,80,136);*/
                box-shadow: 0 0 5px rgba(255,255,255,0.1);
            }
            100% {
                /*border-color: #00ffff;*/
                box-shadow: 0 0 20px rgba(255,255,255,0.3);
            }
        }
        /*.countData{
            position: absolute;
            width: 40.5%;
            height: 20%;
            top: 0;
            line-height: 60px;
            text-align: center;
            color: white;
            font-size: 16px;
            right: 20px;
            margin-top: 5px;
            border: 1px solid rgb(0,255,255);
            box-shadow: rgb(0,255,255) 1px 1px 5px;
        }*/
        .map {
            position: absolute;
            width: 53.5%;
            height: 75%;
            top:10px;
            left:50%;
            transform:translateX(-50%);
            border: 1px dotted rgba(255,255,255,0.3);
            /*background: rgba(1, 25, 35, 0.3);*/
            box-shadow: rgba(255,255,255,0.2) 1px 1px 5px;
        }
        .countData{
            position: absolute;
            width: calc(100% - 40px);
            height: 20%;
            top: 10px;
            text-align: center;
            color: white;
            font-size: 16px;
            left: 50%;
            transform: translateX(-50%);
            /*border: 1px solid rgba(255,255,255,0.3);
            box-shadow: rgba(255,255,255,0.2) 1px 1px 5px;*/
			border: 1px dotted rgba(255,255,255,0.3);
			background: rgba(1, 25, 35, 0.3) !important;
        }
        .countData span.row,
        .countData span.col,
        .map span.row,
        .map span.col{
            position: absolute;
            padding: 5px;
            border-style: solid;
            border-color: rgba(0,255,255,0.8);
        }
        .countData div{
            /*height: 100%;
            width: 100%;*/
            padding: 2px;
            /*background: rgba(1, 25, 35, 0.3) !important;*/
        }


		.reminder-entrance>a{
			color: rgb(0,255,255);
		}
		.reminder-title small{
			color: yellow;
		}


        .row1 {
            border-width: 3px 0 0 3px;
            top: -3px;
            left: 11px;
        }

        .row2 {
            border-width: 3px 3px 0 0;
            top: -3px;
            right: 11px;
        }

        .col1 {
            border-width: 0 0 3px 3px;
            bottom: -3px;
            left: -4px;
        }

        .col2 {
            border-width: 0 3px 3px 0;
            bottom: -3px;
            right: -4px;
        }
        .countData ul {
            margin-top: 0;
            margin-left: 10px;
        }
        .countData li {
            list-style: none;
            display: inline;
            margin-right: 20px;
            /*border: 2px solid rgb(0,153,204);*/
        }

        .countData li span{
            padding: 2px;
        }
        

        .countData li span:nth-child(1) {
            color:yellow;
            font-weight: bold;        
        }

        .countData li span:nth-child(2){
            color: orange;
            font-size: 24px;
            font-weight: bold;
            text-decoration: underline;
        }

        .realTimeData{
            position: absolute;
            left: 5px;
            bottom: 20px;
            color: white;
        }

        .realTimeData a {
            text-decoration: none;
            color: yellow;
        }
        .realTimeData a:hover{
            color: yellow;
        }

		#countFlex{
			display:flex;
			justify-content: space-around;
		}

		#countFlex>div{
			width: 25%;
		}
		.reminder-title{
			margin-top: 0px;
		}

		.reminder-title h5{
			margin: 0;
		}

	</style>
  </head>

  <body style="overflow:hidden">

    <div id="whole-wrapper">
		<div class="product-wrapper row">
        
			<!--<div style="padding: 0px;background:rgba(0,72,129,.9)">-->
            <div style="padding: 0px;background:#09C">
                <div id="map-div" style="width: 100%;height: 60%;margin:0 auto;transform: translateY(-12%);">
                </div>
                
                <div class="countData">
                    <span class="row row1"></span>
					<span class="row row2"></span>
					<span class="col col2"></span>
					<span class="col col1"></span>

                    <div class="user-padding">
						<div class="user-wrapper clearfix">
							<div style="height: 30px;line-height: 30px;border-bottom: 1px solid rgba(255,255,255,0.3);font-weight: bold;">系统总览</div>
							<div style="padding: 0 5px;" id="countFlex">
								<div class="col-xs-4">
									<div class="reminder-title"><h5><small>检测器概览：</small></h5></div>
									<div class="reminder-content">共<span id="detector-num"></span>台检测器，<span id="bad-detector"></span>台禁用</div>
									<div class="reminder-entrance"><a href="detector.php">点击查看</a></div>
								</div>
								<div class="col-xs-4">
									<div class="reminder-title"><h5><small>告警概览：</small></h5></div>
									<div class="reminder-content">共有告警<span id="alarm-num">40</span>条，今日新增<span id="today-alarm-num">3</span>条</div>
									<div class="reminder-entrance"><a href="alarm.php">点击查看</a></div>
								</div>
								<div class="col-xs-4">
									<div class="reminder-title"><h5><small>策略概览：</small></h5></div>
									<div class="reminder-content">共有<span id="class-num"></span>类，共计<span id="rule-num">40</span>条策略</div>
									<div class="reminder-entrance"><a href="rule_task.php">点击查看</a></div>
								</div>
								<div class="col-xs-4">
									<div class="reminder-title"><h5><small>检测器审核概览：</small></h5></div>
									<div class="reminder-content">共<span id="detector-audit-num">0</span>台检测器待审核</div>
									<div class="reminder-entrance"><a href="detector.php">点击查看</a></div>
								</div>
							</div>
						</div>
					</div>
                </div>
                <div class="charts" style="width: 32%;height:37%;left:20px;top:calc(20% + 15px)">
                    <div class="modalTitle">
                        <span>告警级别</span>
                    </div>
                    <div class="modalBorder">
                        <div class="modalBody">
                        </div>
                    </div>
                </div>
                <div class="charts" style="width: 32%;height:37%;right:20px;top:calc(20% + 15px);">
                    <div class="modalTitle">
                        <span>告警态势(近30天)</span>
                    </div>
                    <div class="modalBorder">
                        <div class="modalBody">
                        </div>
                    </div>
                </div>
                
                <div class="charts" style="width: 32%;height:37%;left:50%;transform:translateX(-50%);top:calc(20% + 15px)">
                    <div class="modalTitle">
                        <span>告警类型统计</span>
                    </div>
                    <div class="modalBorder">
                        <div class="modalBody">
                        </div>
                    </div>
                </div>
                <div class="charts" style="width: 32%;height:38%;left:20px;bottom:10px">
                    <div class="modalTitle">
                        <span>检测器告警TOP10</span>
                    </div>
                    <div class="modalBorder">
                        <div class="modalBody">
                        </div>
                    </div>
                </div>

                <div class="charts" style="width: 32%;height:38%;left:50%;transform:translateX(-50%);bottom:10px">
                    <div class="modalTitle" >
                        <span>任务组告警TOP10</span>
                    </div>
                    <div class="modalBorder">
                        <div class="modalBody">
                        </div>
                    </div>
                </div>

                <div class="charts" style="width: 32%;height:38%;right:20px;bottom:10px;">
                    <div class="modalTitle" >
                        <span>检测器接入情况</span>
                    </div>
                    <div class="modalBorder">
                        <div class="modalBody">
                        </div>
                    </div>
                </div>
			</div>
		</div>
		<div class="summary-copyright">
      </div><!-- /#page-wrapper -->

    </div><!-- /#wrapper -->

    <!-- JavaScript -->
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.js"></script>
	<script src="js/libs/echarts.min.js"></script>
    <script src="js/libs/three.min.js"></script>
	<script>
	/*$.ajax({
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
	})*/
	</script>
	<script src="js/frame_detector.js"></script>
    <script src="js/index.js"></script>
  </body>
</html>