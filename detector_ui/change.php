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

    <title>修改密码</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

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

        /*修改密码页面详情*/
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
                <h4><span class="tab_color">|</span>&nbsp;&nbsp;密码修改</h4>
            </div>

        </div>


         <div class="container" >
             <div class="row row_margin"  >
                <div>
                    <div id="login_module" class="login_module" style="width:30%;margin:0 auto">
                        <!--<hr class="hr"/>-->
                        <form name="login_form" id="login_form" method="post" >
                            <div class="form-group margin1">
                                <label class="control-label">输入旧密码:</label>

                                <div class="input-group">
                                    <div class="input-group-addon"><i class="fa fa-lock"></i></div>
                                    <input type="password" class="form-control" id="oldpasswd" placeholder="旧密码">
                                </div>
                            </div>
                            <div class="form-group margin2">
                                <label class="control-label">输入新密码:</label>
                                <label id="pwd_Medium" class="control-label" style="color: red"></label>
                                <div class="input-group">
                                    <div class="input-group-addon"><i class="fa fa-lock"></i></div>
                                    <input type="password" class="form-control" id="newpasswd" placeholder="新密码" onKeyUp="CheckIntensity(this.value)">

                                </div>
                            </div>

                            <div class="form-group margin2">
                                <label class="control-label">确认新密码:</label>

                                <div class="input-group">
                                    <div class="input-group-addon"><i class="fa fa-lock"></i></div>
                                    <input type="password" class="form-control" id="assertpasswd" placeholder="新密码" onKeyUp="CheckIntensity(this.value)">
                                </div>
                            </div>

                            <div class="form-group margin3" align="center">
                                <button id="submitButton" type="button" class="btn btn-primary btn-interval"><i class="search"></i>提交</button>
                                <button id="clearButton" type="button" class="btn btn-primary btn-interval"><i class="eraser"></i>清除</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

        </div>




    </div>
</div>


<!-- JavaScript -->
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame_detector.js"></script>
<script src="js/common.js"></script>
<script src="js/jquery.twbsPagination.min.js"></script>
<script src="js/md5.min.js"></script>
<script>
    buildFrame("menu-passwd");



    function CheckIntensity(pwd){
        var Mcolor,Wcolor,Scolor,Color_Html;
        var m=0;
        var Modes=0;
        for(i=0; i<pwd.length; i++){
            var charType=0;
            var t=pwd.charCodeAt(i);
            if(t>=48 && t <=57){charType=1;}
            else if(t>=65 && t <=90){charType=2;}
            else if(t>=97 && t <=122){charType=4;}
            else{charType=4;}
            Modes |= charType;
        }
        for(i=0;i<4;i++){
            if(Modes & 1){m++;}
            Modes>>>=1;
        }
        if(pwd.length<=4){m=1;}
        if(pwd.length<=0){m=0;}
        switch(m){
            case 1 :
                Color_Html="弱";
                break;
            case 2 :
                Color_Html="中";
                break;
            case 3 :
                Color_Html="强";
                break;
            default :
                Color_Html="";
                break;
        }
        document.getElementById('pwd_Medium').innerHTML=Color_Html;
    }






    //密码本地校验
    $("#submitButton").click(function(){


        var username= localStorage.loginid;
        //alert('uuid'+uuid)
        if(username==undefined){

            alert('请在登录状态下修改密码')
            return;

        }



        var oldpasswd=$("input#oldpasswd").val();
        var newpasswd=$("input#newpasswd").val();
        var assertpasswd=$("input#assertpasswd").val();
        var regex=/^[/s]+$/;

        // var regex_pass=/^(?=.*\d)(?=.*[a-zA-Z])(?=.*[~!@#$%^&*])[\da-zA-Z~!@#$%^&*]{6,}$/;

        var regex_pass=/^(?=.*\d)(?=.*[a-zA-Z])(?=.*[`~!@#$%^&*()_\-+=<>?:"{}|,.\/;'\\[\]·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘’，。、])[\da-zA-Z`~!@#$%^&*()_\-+=<>?:"{}|,.\/;'\\[\]·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘’，。、]{6,}$/;

        if(regex.test(oldpasswd)||oldpasswd.length==0){
            alert("密码格式不对");
            return;
        }
        if(regex.test(newpasswd)||newpasswd.length==0) {
            alert("新密码格式不对");
            return;
        }
        if (assertpasswd != newpasswd||assertpasswd==0) {
            alert("两次密码输入不一致");
            return;
        }

/*        if(newpasswd.length<6) {
            alert("新密码最短要求6位");
            return;
        }*/

        if(!regex_pass.test(newpasswd) || newpasswd.length<6) {
            alert("新密码必须包含数字、英文字母、特殊符号且大于等于6位");
            return;
        }

        var oldpasswd_md5 = md5(oldpasswd).toUpperCase();
        var newpasswd_md5 = md5(newpasswd).toUpperCase();


        $.ajax({
            url: "/ajax_action_detector.php?uu=login.change_password",
            type: "post",
            data: { username: username, old_password: oldpasswd_md5, new_password:newpasswd_md5},
            success:function(data) {
                var res = JSON.parse(data);
                if(res["code"]==200){

                    alert('密码修改成功！')
                } else {
                    alert(res["msg"]);

                }
            },
            error: function () {
                alert("无法连接服务器");
            },
            beforeSend: function () {

            }

        });




    })
//重置
    $("#clearButton").click(function(){
        $("#oldpasswd").val("");
        $("#newpasswd").val("");
        $("#assertpasswd").val("");
    })


</script>
</body>
</html>