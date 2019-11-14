<?php

//require_once(dirname(__FILE__) . '/data/get.json.from.server.php');
//require_once(dirname(__FILE__) . '/service/service.php');

//putLog('1111111');
//if (isset($_POST['upfile'])) {

/*    putLog($_FILES['upfile']['tmp_name']);
    var_dump($_FILES);
    move_uploaded_file($_FILES['upfile']['tmp_name'], 'up_tmp/'.time().'.dat');
    //header('location: test.php');
    exit;*/
//}
?>
<!doctype html>
<html lang="zh">
<head>
    <meta charset="utf-8">
    <title>HTML5 Ajax Uploader</title>
    <script src="js/jquery-1.10.2.js"></script>
</head>

<body>
<p><input type="file" id="upfile"></p>
<p><input type="button" id="upJQuery" value="用jQuery上传"></p>
<script>
     /* jQuery 版 */
    $('#upJQuery').on('click', function() {
        var fd = new FormData();
        //fd.append("count", 1);
        fd.append("upfile", $("#upfile").get(0).files[0]);
        $.ajax({
            url: "ajax_action_upload.php?uu=file.upload",
            //url: "http://192.168.120.234/file/upload",
            
            type: "POST",
//            processData: false,
//            contentType: "multipart/form-data",
            cache: false,
            contentType: false,
            processData: false,
            data: fd,
            success: function(d) {
                console.log("####"+d);
            }
        });
    });
</script>
</body>
</html>

