<?php
ini_set("display_errors", "On");
ini_set("log_errors", "On");
error_reporting(E_ALL | E_STRICT);
require_once(dirname(__FILE__).'/data/get.json.from.server.php');
require_once(dirname(__FILE__).'/service/service.php');

//$ref = getGet("ref");
//if(empty($ref)){
//    $ref = "summary.php";
//}checkLoginForLoginPage($ref);

?>

<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>登录</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">
    <link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">
    <link href="css/frame.css" rel="stylesheet">
    <link href="css/entrance.css" rel="stylesheet">

    <style>
        body {
            background: white;
        }
    </style>
</head>
<body>
<div>
    <nav class="navbar navbar-blue navbar-fixed-top" role="navigation">
        <div class="nav-margin">
            <div class="navbar-header">
                <div>
                    <img class="navbar-header-img" src="images/ruizheng.png">
                </div>
            </div>

            <ul class="nav navbar-nav navbar-right">
                <!--<li><p class="navbar-text">关于我们</p></li>-->
                <li><a href="#"><i class="fa fa-users"></i>&nbsp关于我们 </a></li>
                <li><a href="#"><i class="fa fa-info"></i>&nbsp帮助 </a></li>
            </ul>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container-fluid -->
    </nav>
</div>
<div class="container">
    <div class="row row_margin">
        <div class="col-sm-6 col-md-5 col-md-offset-1 ">
            <img src="images/login_bg1.png" width="450px" height="350px;">
        </div>
        <div class="col-sm-5 col-md-4 col-md-offset-2">
            <div id="login_module" class="login_module">
                <label class="label_welcome">欢迎登录</label>
                <hr class="hr"/>
                <form name="login_form" id="login_form" method="post">
                    <div class="form-group margin1">
                        <label class="control-label">账号:</label>

                        <div class="input-group">
                            <div class="input-group-addon"><i class="fa fa-user"></i></div>
                            <input type="text" class="form-control" id="inputSuccess1" placeholder="用户名">
                        </div>
                    </div>
                    <div class="form-group margin2">
                        <label class="control-label">密码:</label>
                        <a href="#">
                            <small style="float: right;">忘记密码?</small>
                        </a>

                        <div class="input-group">
                            <div class="input-group-addon"><i class="fa fa-lock"></i></div>
                            <input type="password" class="form-control" id="inputSuccess2" placeholder="密码">
                        </div>
                    </div>
                    <div class="checkbox margin2">
                        <label>
                            <input type="checkbox">
                            <small>记住密码</small>
                        </label>
                    </div>
                    <div class="form-group margin3">
                        <label class="control-label sr-only">登录</label>
                        <input type="button" class="form-control btn btn-primary" id = "inputSuccess3" value="登录"">
                    </div>
                    <div class="form-group info">
                        温馨提示：建议您使用谷歌Chrome浏览器，其他浏览器对本系统兼容性不完善！
                    </div>
                    <div class="loading-pic hidden">
                        <img src="images/loading.gif" style="width:100%;">
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div>
        <nav class="navbar navbar-default navbar-fixed-bottom">
        </nav>
    </div>
</div>
<script src="js/jquery-1.10.2.js"></script>
<script src="js/bootstrap.js"></script>
<script src="js/frame.js"></script>
<script src="js/md5.min.js"></script>
<script>
    $(function () {
        $('nav.navbar-fixed-bottom').html(COPYRIGHT);
        $("input#inputSuccess3").click(function(){
            var loginid = $("input#inputSuccess1").val();
            var password = $("input#inputSuccess2").val();
            var password_md5 = md5(password).toUpperCase();
           $.ajax({
                //url: "/ajax_action_detector.php?uu=login.check",/////本地验证
               url: "/ajax_action_login.php",/////SESSION验证
               type: "post",
                data: { username: loginid, password: password_md5},
                success:function(data) {
                    var res = JSON.parse(data);
					var res1 = res;
                    if(res["code"]==200){
                        localStorage.loginid=loginid;
                        localStorage.timestamp=new Date().toLocaleString();
						localStorage.level=0;
                        $.ajax({
                            //url: "/ajax_action_detector.php?uu=login.check",/////本地验证
                            url: "/ajax_action_detector_before_login.php?uu=login.user_expire",/////SESSION验证
                            type: "post",
                            data: { username: loginid},
                            success:function(data) {
                                var res = JSON.parse(data);
                                
                                if(res["code"]==200){
                                    var msg = res["msg"]
                                    if(msg==0){
                                        console.log(msg)
                                        //window.location.href="summary.php";
										login_data(res1);
                                    }else if(msg==1){
                                        alert("密码已经过期，请修改密码！");
                                        window.location.href="change.php";
                                    }else{
                                        alert("过期校验出错");
                                    }
                                } else {
                                    alert(res["msg"]);
                                    $(".loading-pic").addClass("hidden");
                                }
                            },
                            error: function () {
                                alert("无法连接服务器");
                            },
                            beforeSend: function () {
                                $(".loading-pic").removeClass("hidden");
                            }
                        });
                    } else {
                        alert(res["msg"]);
                        $(".loading-pic").addClass("hidden");
                    }
                },
                error: function () {
                    alert("无法连接服务器");
                },
                beforeSend: function () {
                    $(".loading-pic").removeClass("hidden");
                }

            });
        });

        $(document).keyup(function(event){
            if(event.keyCode ==13){
                $("input#inputSuccess3").click();
            }
         });
        
    });
	
	
	    function login_data(res){
        
        localStorage.roles = JSON.stringify(res["msg"]["role"]);
        var keycount = 0;
        for(var key in res["msg"]["role"]){
            keycount++;
        }
        if(keycount == 1){
            for(var key in res["msg"]["role"]){
                localStorage.roleResourceIds = JSON.stringify(res["msg"]["role"][key]);
                localStorage.currentRole = key;
            }
            window.location.href="summary.php";
        }
        else{
            $('body').append(switchRoleModal);
            var radio = ""
            for(var key in res["msg"]["role"]){
                radio += '<label><input type="radio" name="switch_role" value='+JSON.stringify(res["msg"]["role"][key])+'>'+key+'</label>'
            }
            $('#switchRole .modal-body div').append(radio);
            $('#switchRole').modal('show');
        }
        
    }

    var switchRoleModal = `<div class="modal fade" id="switchRole" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog" style="width: 390px">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                    &times;
                </button>
                <h4 class="modal-title">
                    选择角色
                </h4>
            </div>
            <div class="modal-body">
                <div>
                </div>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-interval btn-primary" onclick="switchSubmit()">确定</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div>
    </div>
</div>`

function switchSubmit(){
    var roleResourceIds = $('input[name=switch_role]:checked').attr('value');
    if(roleResourceIds == undefined){
        alert('请选择角色');
        return;
    }
    localStorage.roleResourceIds = roleResourceIds;
    localStorage.currentRole = $('input[name=switch_role]:checked').parent().text();
    window.location.href="summary.php";
}
</script>


</body>
</html>