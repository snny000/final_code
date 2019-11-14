var FRAME = ["<nav class=\"navbar navbar-blue navbar-fixed-top\" role=\"navigation\">",
"        <!-- Brand and toggle get grouped for better mobile display -->",
"        <div class=\"navbar-header navbar-header-fix-height\">",
"          <img class = \"navbar-header-img\" src=\"images/ruizheng.png\">",
"        </div>",
"        <!-- Collect the nav links, forms, and other content for toggling -->",
"        <div class=\"collapse navbar-collapse navbar-ex1-collapse\">",
"          <ul class=\"nav navbar-nav side-nav\">",
"			<li><a id=\"summary\" href=\"summary_spark.php\"> &nbsp&nbsp&nbsp&nbsp概览</a></li>",
"			",
"			<li class=\"dropdown open\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp产品与服务 </a>",
"              <ul class=\"dropdown-menu\">",
//" 				 <li><a id=\"menu-summary\" href=\"summary_spark.php\">&nbsp<i class=\"fa fa-users\"></i>&nbsp概览</a></li>",
"                <li><a id=\"menu-sql\" href=\"sqlforlog.php\">&nbsp<i class=\"fa fa-users\"></i>&nbspSparkSQL服务</a></li>",
"                <li><a id=\"menu-es\" href=\"es_search.php\">&nbsp<i class=\"fa fa-users\"></i>&nbspES查询服务</a></li>",
"                <li><a id=\"menu-stream\" href=\"#\">&nbsp<i class=\"fa fa-minus-square\"></i>&nbsp流计算</a></li>",
"                <li><a id=\"menu-ml\" href=\"#\">&nbsp<i class=\"fa fa-minus-square\"></i>&nbsp机器学习</a></li>",
"                <li><a id=\"menu-graph\" href=\"#\">&nbsp<i class=\"fa fa-sitemap\"></i>&nbsp图计算</a></li>",



"              </ul>",
"            </li>",
"			",
"			<li class=\"dropdown open\">",
"              <a class=\"for-open\" href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" data-stopPropagation=\"true\"><b class=\"caret\"></b> &nbsp用户中心 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li><a id=\"menu-account\" href=\"#\">&nbsp<i class=\"fa fa-user\"></i>&nbsp账号管理</a></li>",
"				<li><a id=\"menu-messages\" href=\"message.php\">&nbsp<i class=\"fa fa-volume-up\"></i>&nbsp消息中心</a></li>",
"				<li><a id=\"menu-worksheet\" href=\"#\">&nbsp<i class=\"fa fa-clipboard\"></i>&nbsp工单管理</a></li>",
"				<li><a id=\"menu-orders\" href=\"#\">&nbsp<i class=\"fa fa-truck\"></i>&nbsp订单中心</a></li>",
"              </ul>",
"            </li>",
"          </ul>",
"          <ul class=\"nav navbar-nav navbar-right navbar-user\">",
"			<li class=\"dropdown search-dropdown\">",
"              <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\"><i class=\"fa fa-search\"></i> &nbsp搜索 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li>",
"					<div class=\"input-group\">",
"						<input type=\"text\" class=\"form-control\" placeholder=\"输入关键字\">",
"						<span class=\"input-group-btn\">",
"							<button class=\"btn btn-default\" type=\"button\"><i class=\"fa fa-search\"></i></button>",
"						</span>",
"					</div>",
"				</li>",
"              </ul>",
"            </li>",
"			",
"			<li class=\"dropdown qrcode-dropdown\">",
"              <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\"><i class=\"fa fa-mobile-phone\"></i> &nbsp手机版 </a>",
"              <ul class=\"dropdown-menu\">",
"                <li>",
"					<div class=\"thumbnail\">",
"					  <img src=\"images/qrcode.png\" alt=\"扫码下载手机版\">",
"					  <p>扫码下载手机大数据云</p>",
"					</div>",
"				</li>",
"              </ul>",
"            </li>",
"            <li class=\"dropdown messages-dropdown\">",
"              <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\"><i class=\"fa fa-envelope\"></i> &nbsp通知 <span class=\"badge\">7</span> <b class=\"caret\"></b></a>",
"              <ul class=\"dropdown-menu\">",
"                <li class=\"dropdown-header\">消息通知</li>",
"				<li id = \"msg-divider\" class=\"divider\"></li>",
"                <li><a href=\"message.php\"><p class=\"check-more\">查看更多</p></a></li>",
"              </ul>",
"            </li>",
"			",
"            <li class=\"dropdown worksheet-dropdown\">",
"              <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\"><i class=\"fa fa-clipboard\"></i> &nbsp工单服务 <b class=\"caret\"></b></a>",
"              <ul class=\"dropdown-menu\">",
"                <li><a href=\"#\">我的工单</a></li>",
"				<li class=\"divider\"></li>",
"                <li><a href=\"#\">提交工单</a></li>               ",
"              </ul>",
"            </li>",
"			",
"			<li class=\"dropdown help-dropdown\">",
"              <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\"><i class=\"fa fa-info\"></i> &nbsp帮助 </a>",
"            </li>",
"			",
"            <li class=\"dropdown user-dropdown\">",
"              <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\"><i class=\"fa fa-user\"></i> <span></span> <b class=\"caret\"></b></a>",
"              <ul class=\"dropdown-menu\">",
"                <li><a href=\"#\"><i class=\"fa fa-user\"></i> 个人信息</a></li>",
"                <li class=\"divider\"></li>",
"                <li><a href=\"login.php\"><i class=\"fa fa-power-off\"></i> 注销</a></li>",
"              </ul>",
"            </li>",
"          </ul>",
"        </div><!-- /.navbar-collapse -->",
"      </nav>"].join("");

var COPYRIGHT = ["<div class=\"copyright\">",
"                <p>COPYRIGHT@2016 ##############公司版权所有 </p>",
"                <p>公司地址:#################### 24小时电话服务热线：4009-####-##</p>",
//"                <p>备案号：京ICP备*******号</p>",
"            </div>"].join("");

$(function() {	
	//sidebar-closable
	$('.side-nav .dropdown').each(function(){			
		this.closable = false;
	});
	$('.side-nav .for-open').click(function(){			
		this.parentNode.closable = true;
	});
	$('.side-nav .dropdown').on({
		"shown.bs.dropdown": function() { this.closable = false; },
		"hide.bs.dropdown":  function() { return this.closable; }
	});
	//active-blue
	//$('#menu-ddos').css("background","#09C");
	//$('#menu-ddos').css("color","#fff");
	//search-closable
	$('.search-dropdown input').focus(function(){		
		this.parentNode.parentNode.parentNode.parentNode.closable = false;
	});
	$('.search-dropdown button').focus(function(){			
		this.parentNode.parentNode.parentNode.parentNode.parentNode.closable = false;
	});
	$('.search-dropdown input').blur(function(){		
		this.parentNode.parentNode.parentNode.parentNode.closable = true;
	});
	$('.search-dropdown button').blur(function(){			
		this.parentNode.parentNode.parentNode.parentNode.parentNode.closable = true;
	});
	$('.search-dropdown').on({
		"hide.bs.dropdown":  function() { return this.closable; }
	});
	
	$('.search-dropdown button').blur(function(){
		this.parentNode.parentNode.parentNode.parentNode.parentNode.closable = true;
	});

});

function buildFrame(activeElement){
	$('#whole-wrapper').prepend(FRAME);
	if(activeElement.length){
		$('#'+activeElement).css("background","#09C");
		$('#'+activeElement).css("color","#fff");
	}
}

function setFrameValue(msgList, uuid, sealMsgNum, visibleNum){
	$('.user-dropdown a span').html(uuid);
	var msgHtml = "";
	var count = 0;
	for (var i in msgList){
		msgHtml += "<li class=\"message-preview\"><a href=\"message_detail.php?id="+msgList[i].id+"\"><span class=\"name\">"+msgList[i].title+"</span><span class=\"message\">"+cutMessage(msgList[i].content)+"</span><span class=\"time\"><i class=\"fa fa-clock-o\"></i>"+msgList[i].create_time+"</span></a></li>";
		msgHtml += "<li class=\"divider\"></li>";
		count++;
		if(count>=visibleNum){
			break;
		}
	}
	$('#msg-divider').after(msgHtml);
	$('li.messages-dropdown > a > span').html(sealMsgNum);

}

function setNewsValue(newsList){
	var newsHtml = "";
	for (var i in newsList){
		var headNews = "";
		if(newsList[i].is_top = 1){
			headNews = "<span class=\"head-news\">头条</span>";
		}
		newsHtml += "<li><a href=\""+newsList[i].url+"\">"+headNews+"  &nbsp"+newsList[i].title+"</a></li>";
	}
	$('.work-news ul').html(newsHtml);
}

function cutMessage(msg){
	if(msg.length<50){
		return msg;
	} else {
		return msg.substring(0,49) + "......";
	}
}