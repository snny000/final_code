<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__).'/data/get.json.from.server.php');
require_once(dirname(__FILE__).'/service/service.php');


//$msgList = getCommonById("getSealMsgListByUserId", "user_id", $user->getId());
//$msgCount = getCommonById("getSealMsgCountByUserId", "user_id", $user->getId());
//$newsList = getCommon("getFreshNewsByTop");


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
    <!--<link href="css/entrance.css" rel="stylesheet">-->
    <link href="css/product.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <style>
        body {
          background-color: white;
        }
    </style>
  </head>

  <body>

    <div id="whole-wrapper">
      <div>

        <div class="row row_margin"  >
          <div class="pull-left margin_ddos1">
            <h4><span class="tab_color">|</span>&nbsp;&nbsp;ES查询</h4>
          </div>
        </div>

<!--
        <div class="row">
          <div class="col-lg-4" style="margin: 0 15px;width: 80%;" >
            <div class="input-group">
              <input id="sql_t" type="text" class="form-control" placeholder="请输入Sparksql语句">

              <div class="input-group-btn">
                <button id="sql_b" type="button" class="btn btn-primary"><i class="fa fa-search">&nbsp;&nbsp;</i>提交
                </button>
              </div>
            </div>
          </div>
        </div>
    -->

        <div align="center" >
          <div class="input-group" style="margin: 0 15px;width: 80%;">
            <input id="sql_t" type="text" class="form-control" placeholder="请输入ES查询参数" style="font-size: 20px;height: 40px;">

            <div class="input-group-btn">
              <button id="sql_b" type="button" class="btn btn-primary" style="height: 40px;"><i class="fa fa-search">&nbsp;&nbsp;</i>提交
              </button>
            </div>
          </div>


            <div>
              <div id="content" style="font:initial;font-size: 20px;margin-top: 20px"></div>
            </div>
<!--
            <div class="summary-copyright" style="width: 100%;position: fixed;left: 0;bottom: 0;">
            </div>
   -->
        </div><!-- /#page-wrapper -->
      </div>
    </div><!-- /#wrapper -->

    <!-- JavaScript -->
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.js"></script>

	<script>
	$(function() {
      buildFrame("menu-es");
      //$("#content").text("hahahaha");
      //"SELECT * FROM log where test_type=3"
      $("#sql_b").click(function(){
        $("#sql_b").prop('disabled',"true");
        var sqlvalue = $("#sql_t").prop("value")
        //console.log("sqlvalue："+sqlvalue)
        $.ajax({
          //url: "http://192.168.120.175/doSqlForLog.log",
          url: "/es_action.php",
          type: "post",
          data: sqlvalue,
          //sqlvalue
          success:function(data) {
            $("#content tr").remove();
            console.log(data)
            var ret = JSON.parse(data);
            var array = ret.data;
            var total = ret.total;
            var took = ret.took;
            var result_str = "总数量:"+total+"&nbsp查询时间:"+took+"ms<br/>";
            for(var i = 0;i < array.length; i++) {
              result_str+=JSON.stringify(array[i])+"<br/>";
            }
            //console.log(JSON.stringify(ret.data))
            $("#content").html(result_str)
            $("#sql_b").removeAttr('disabled')
            //var ret = JSON.parse(data);
          },
          beforeSend: function () {
            $("#content").html("");
            $("#content").append("<tr><td colspan='5'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
          },
        })
      })
      $('.summary-copyright').html(COPYRIGHT);
	});
	</script>
	<script src="js/frame.js"></script>
  </body>
</html>