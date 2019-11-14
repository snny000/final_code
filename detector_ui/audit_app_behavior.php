<?php
//ini_set("display_errors", "On");
//ini_set("log_errors", "On");
//error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
require_once(dirname(__FILE__) . '/service/service.php');
require_once(dirname(__FILE__) . '/require_login_check_for_all_page.php');
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

    <title>应用行为审计</title>

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

        .date_label{
            float: left;
            margin-top: 5px;
            margin-right: 4px;
        }
        .date_div{
            width: 400px;
            float: left;
        }
    </style>
</head>

<body>

<div id="whole-wrapper">

    <div>
        <div class="row">
            <div class="pull-left margin_ddos1">
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;应用行为审计</h4>
            </div>

        </div>

        <div class="row btn-banner">
            <input id="sip" type="text" class="form-control search-input" placeholder="源IP地址(支持通配符)">
            <input id="sport" type="number" class="form-control search-input btn-interval" placeholder="源端口号">
            <input id="smac" type="text" class="form-control search-input btn-interval" placeholder="源MAC地址">
            <input id="dip" type="text" class="form-control search-input btn-interval" placeholder="目的IP地址(支持通配符)">
            <input id="dport" type="number" class="form-control search-input btn-interval" placeholder="目的端口号">
            <input id="dmac" type="text" class="form-control search-input btn-interval" placeholder="目的MAC地址">
        </div>
        <div class="row btn-banner">

            <div class="date_div" style="width: 165px">
                <input id="protocol" type="text" class="form-control search-input" placeholder="传输层协议">
            </div>

            <div class="date_div" style="width: 165px">
                <input id="app" type="text" class="form-control search-input btn-interval" placeholder="应用协议">
            </div>

            <div class="input-group date form_datetime date_div" style="width: 160px; margin-left: 20px">
                <input id="start_time" class="form-control" size="16" type="text" value="" readonly placeholder="开始时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>

            <div class="input-group date form_datetime date_div btn-interval2" style="width: 160px">
                <input id="end_time" class="form-control" size="16" type="text" value="" readonly placeholder="截止时间">
                <span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
            </div>

            <button id="searchButton" type="button" class="btn btn-primary btn-interval2"><i class="fa fa-search">&nbsp;&nbsp;</i>搜索</button>
            <button id="clearButton" type="button" class="btn btn-default"><i class="fa fa-eraser">&nbsp;&nbsp;</i>清除</button>

        </div>


        <div class="row common_margin">
            <table id="maintable" class="table table-hover tbl_font_size "
                   style="border: 1px solid lightgray;border-collapse: inherit">
                <thead class="thead">
                <tr>
                    <th width="2%"><input type="checkbox" class="checkbox" id="chk_all1"></th>
                    <th width="10%" >源IP地址:端口号</th>
                    <th width="10%">源MAC地址</th>
                    <th width="10%">目的IP地址:端口号</th>
                    <th width="10%">目的MAC地址</th>
                    <th width="10%">传输层协议</th>
                    <th width="10%">应用协议</th>
                    <th width="10%">事件时间</th>
                    <th width="2%">私有字段</th>
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

 <!--                           <nav id="paginationbox">
                                <span style="vertical-align:10px;">共有<strong id="totalcount"></strong>条，每页显示：<strong>10</strong>条</span>
                                <ul id="pagination" class="pagination pagination-sm" style="margin: 0%;"> </ul>
                            </nav>-->
                            <?php
                            require_once(dirname(__FILE__) . '/require_page_bar_for_all_page.php');
                            ?>


                        </div>
                    </td>
                </tr>

                </tfoot>
            </table>

        </div>

    </div>

</div>
<!-- /#page-wrapper -->


<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>

<script src="bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.min.js" charset="UTF-8"></script>
<script src="bootstrap-datetimepicker-master/js/locales/bootstrap-datetimepicker.zh-CN.js" charset="UTF-8"></script>

<script>
    buildFrame("menu-audit2");
    $(function(){
        var globalSearchParam = {random:1}
        //第一次加载分页
        LoadPage(1,globalSearchParam)
    })


    $('.form_datetime').datetimepicker({
        language:  'zh-CN',
        minView: "hour",
        format: 'yyyy-mm-dd hh:ii:ss',
        autoclose: true,
        todayBtn: true,
    });

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
            console.log("page:"+page)
            $.ajax({
                url: option.myurl+"&pn="+page,
                type: "post",
                data: option.searchParam,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 0) {

                        List(ret["data"]);
                    } else if (ret["code"] == 20000) {
                        $("#maintable tbody tr").remove();
                        $("<tr><td colspan='9' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
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
/*


    $("#chk_all1,#chk_all2").click(function(){
        if(this.checked){
            $("table :checkbox").prop("checked", true);
        }else{
            $("table :checkbox").prop("checked", false);
        }
    });
*/



    function format(txt,compress/*是否为压缩模式*/){/* 格式化JSON源码(对象转换为JSON文本) */
        var indentChar = '    ';
        if(/^\s*$/.test(txt)){
            alert('数据为空,无法格式化! ');
            return;
        }
        try{var data=eval('('+txt+')');}
        catch(e){
            alert('数据源语法错误,格式化失败! 错误信息: '+e.description,'err');
            return;
        };
        var draw=[],last=false,This=this,line=compress?'':'\n',nodeCount=0,maxDepth=0;

        var notify=function(name,value,isLast,indent/*缩进*/,formObj){
            nodeCount++;/*节点计数*/
            for (var i=0,tab='';i<indent;i++ )tab+=indentChar;/* 缩进HTML */
            tab=compress?'':tab;/*压缩模式忽略缩进*/
            maxDepth=++indent;/*缩进递增并记录*/
            if(value&&value.constructor==Array){/*处理数组*/
                draw.push(tab+(formObj?('"'+name+'":'):'')+'['+line);/*缩进'[' 然后换行*/
                for (var i=0;i<value.length;i++)
                    notify(i,value[i],i==value.length-1,indent,false);
                draw.push(tab+']'+(isLast?line:(','+line)));/*缩进']'换行,若非尾元素则添加逗号*/
            }else   if(value&&typeof value=='object'){/*处理对象*/
                draw.push(tab+(formObj?('"'+name+'":'):'')+'{'+line);/*缩进'{' 然后换行*/
                var len=0,i=0;
                for(var key in value)len++;
                for(var key in value)notify(key,value[key],++i==len,indent,true);
                draw.push(tab+'}'+(isLast?line:(','+line)));/*缩进'}'换行,若非尾元素则添加逗号*/
            }else{
                if(typeof value=='string')value='"'+value+'"';
                draw.push(tab+(formObj?('"'+name+'":'):'')+value+(isLast?'':',')+line);
            };
        };
        var isLast=true,indent=0;
        notify('',data,isLast,indent,false);
        return draw.join('');
    }


    function List(msgListObj){
        $("#maintable tbody tr").remove();
        var _row = $("<tr><td><input type='checkbox' class='checkbox'></td>"+
            "<td></td><td></td><td ></td><td></td><td></td><td></td><td></td><td></td></tr>");

        var _area = $("<textarea readonly disabled style=\"width:300px;background-color:#f9f9f9;font-size:10px;line-height:15px;height:49px;BORDER-BOTTOM: 0px solid; BORDER-LEFT: 0px solid; BORDER-RIGHT: 0px solid; BORDER-TOP: 0px solid\"></textarea>");

        for (var i = 0; i < msgListObj.length; i++) {
            var row = _row.clone();
            // var operatehtml = getStrManipulation(msgListObj[i].warning_type, msgListObj[i].id);
            row.attr("id",msgListObj[i].id);
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>");
            row.find("td:eq(1)").text(msgListObj[i].sip+":"+msgListObj[i].sport);
            row.find("td:eq(2)").html(msgListObj[i].smac);
            row.find("td:eq(3)").text(msgListObj[i].dip+":"+msgListObj[i].dport);
            row.find("td:eq(4)").html(msgListObj[i].dmac);
            row.find("td:eq(5)").html("&nbsp&nbsp&nbsp&nbsp"+msgListObj[i].protocol+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp");
            row.find("td:eq(6)").html("&nbsp&nbsp&nbsp"+msgListObj[i].app+"&nbsp&nbsp&nbsp&nbsp");
            row.find("td:eq(7)").html(msgListObj[i].time);

            var area =_area.clone();

            row.find("td:eq(8)").html(area.text(format(JSON.stringify(msgListObj[i]).replace(/[\r\n]/g, ""))));
            row.show();
            row.appendTo("#maintable tbody");
        }
        rebindChkAll();
    }



    function LoadPage(currentPage,searchParam){
        $.ajax({
            url: "/app_behavior_show.php",
            type: "post",
            data: searchParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 0)
                    ret = ret["total"]
                else {
                    ret = 0;
                }
                $("#totalcount").text(ret);
                $('#pagination').empty();
                $('#pagination').removeData("twbs-pagination");
                $('#pagination').unbind("page");
                pagination(ret,"/app_behavior_show.php?size="+p_size+"",parseInt(currentPage),searchParam)
            },
            beforeSend: function () {
                $(".loading-pic").removeClass("hidden");
            },
            error: function () {
                alert("无法连接服务器");
            }
        })
    }

    var globalSearchParam = {random:1}

    $("#searchButton").click(function(){
        var sip =  $("#sip").val();
        var sport =  $("#sport").val();
        var smac =  $("#smac").val();
        var dip =  $("#dip").val();
        var dport =  $("#dport").val();
        var dmac =  $("#dmac").val();
        var protocol =  $("#protocol").val();
        var app =  $("#app").val();
        var start_time = $("#start_time").val()
        var end_time =$("#end_time").val()

        globalSearchParam = {random:1}


        if(sip!=""){
            globalSearchParam["sip"] = sip
        }
        if(sport!=""){
            globalSearchParam["sport"] = sport
        }
        if(smac!=""){
            globalSearchParam["smac"] = smac
        }
        if(dip!=""){
            globalSearchParam["dip"] = dip
        }
        if(dport!=""){
            globalSearchParam["dport"] = dport
        }
        if(dmac!=""){
            globalSearchParam["dmac"] = dmac
        }
        if(protocol!=""){
            globalSearchParam["protocol"] = protocol
        }
        if(app!=""){
            globalSearchParam["app"] = app
        }
        if(start_time!=""){
            globalSearchParam["start_time"] = start_time
        }
        if(end_time!=""){
            globalSearchParam["end_time"] = end_time
        }

        LoadPage(1,globalSearchParam)
    })

    $("#clearButton").click(function(){
        $("#sip").val("");
        $("#sport").val("");
        $("#smac").val("");
        $("#dip").val("");
        $("#dport").val("");
        $("#dmac").val("");
        $("#protocol").val("");
        $("#app").val("");
        $("#start_time").val("");
        $("#end_time").val("");
    })


</script>

</body>
</html>