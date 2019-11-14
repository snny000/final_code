/**
 * Created by Fernando on 2016/7/7.
 */

var p_size =10;//全局每页条数

var node ="A";//节点名

var contractorMap={'01':'中孚', '02':'蓝盾', '03':'天融信', '04':'鼎普', '05':'网安', '06':'信工所'};


//$("#p_size").text(p_size)
function selectPsize(){
    p_size = parseInt($("#p_size").val());
    $('#pagination .active a').text(1);
    refresh();
}

function HTMLEncode(html) {
    var temp = document.createElement("div");
    (temp.textContent != null) ? (temp.textContent = html) : (temp.innerText = html);
    var output = temp.innerHTML;
    temp = null;
    return output;
}

function HTMLDecode(text) {
    var temp = document.createElement("div");
    temp.innerHTML = text;
    var output = temp.innerText || temp.textContent;
    temp = null;
    return output;
}


function isSuccessFormat(status){
        console.log(status)
        var is_success_map = {0:'已忽略',1:'任务执行中',2:'任务执行成功',3:'任务执行失败',4:'任务错误'};
        var status_html = $('<span>'+is_success_map[status]+'</span>')
        switch(status){
            case 0:
                $(status_html).css('color','gray');
                break;
            case 1:
                $(status_html).css('color','orange');
                break;
            case 2:
                $(status_html).css('color','green');
                break;
            case 3:
                $(status_html).css({'color':'red','font-weight':'bold'});
                break;
            case 4:
                $(status_html).css('color','red');
                break;
        }
        return status_html;
    }


function getfinaltime(release_time,is_success){
    var final_time = ''
    if(is_success == 2){
        final_time = release_time
    }
    return final_time
}



function post(URL, PARAMS) {
    var temp = document.createElement("form");
    temp.action = URL;
    temp.method = "post";
    temp.style.display = "none";
    temp.target="_self";
    //temp_form.target = "_self";
    for (var x in PARAMS) {
        var opt = document.createElement("textarea");
        opt.name = x;
        opt.value = PARAMS[x];
        // alert(opt.name)
        temp.appendChild(opt);
    }
    document.body.appendChild(temp);
    temp.submit();
    return temp;
}


function post_blank(URL, PARAMS) {
    var temp = document.createElement("form");      
    temp.action = URL;      
    temp.method = "post";      
    temp.style.display = "none";
    temp.target="_blank";
    //temp_form.target = "_self";
    for (var x in PARAMS) {      
        var opt = document.createElement("textarea");      
        opt.name = x;      
        opt.value = PARAMS[x];      
        // alert(opt.name)      
        temp.appendChild(opt);      
    }      
    document.body.appendChild(temp);      
    temp.submit();      
    return temp;      
}      





// // 策略中查看任务组描述
// var currentTaskGroup = {};
// function showTaskGroup(that){
//     $('#showTaskGroupModal').modal('show');
//     var msgListObj = JSON.parse($(that).attr('data-bind'));
//     $("#show_task_group_id").val(msgListObj.task_id);
//     $("#show_task_group_name").val(msgListObj.task_group_name);
//     $("#show_task_group_type").val(ruleType[parseInt(msgListObj.task_type)][0]);
//     $.ajax({
//         url: '/ajax_action_detector.php?uu=command.query_taskgroup&p_size=10&pn=1',
//         data: {task_id:msgListObj.task_id},
//         success:function(data){
//             var res = JSON.parse(data)["msg"][0];
//             $('#show_task_group_create').val(res.create_person);
//             $('#show_task_group_create_time').val(res.create_time.replace('T',' '));
//             $('#show_task_group_remark').val(res.remarks);
//             currentTaskGroup = {
//                 url:ruleType[res.task_type][1],
//                 id: res.id,
//                 rule_id_list: res.rule_id_list,
//                 addIntoGroup: JSON.stringify({
//                     state:false,
//                     task_id: res.task_id,
//                     task_name: res.name,
//                     task_type: res.task_type
//                 })
//             };
//         }
//     })
// }

//调用方法 如      
//post('pages/statisticsJsp/excel.action', {html :prnhtml,cm1:'sdsddsd',cm2:'haha'});





/*    function mm(a)
 {
 return /(\x0f[^\x0f]+)\x0f[\s\S]*\1/.test("\x0f"+ a.join("\x0f\x0f") +"\x0f");
 }*/

function unique(arr){
// 遍历arr，把元素分别放入tmp数组(不存在才放)
    var tmp = new Array();
    for(var i in arr){
//该元素在tmp内部不存在才允许追加
        if(tmp.indexOf(arr[i])==-1){
            tmp.push(arr[i]);
        }
    }
    return tmp;
}

/*

$("#refresh").click(function(){
    var currentPage = $('#pagination .active a').text()
    LoadPage(currentPage,globalSearchParam)
})
*/

function refresh(){
    var currentPage = $('#pagination .active a').text();
    LoadPage(currentPage,globalSearchParam)
}

$("#refresh").click(function(){
    refresh()
})


$('h4 .btn-group').on('click','button',function(){
    window.location.replace($(this).attr('href'));
})

$("#gotopn").click(function() {
    var currentPage = $("input#pn").val();
    $("input#pn").val("")
    var totalcount = $("#totalcount").text()

    //alert(totalcount)
    ///判断currentPage是不是数字
    function isNum(num){
        var reNum=/^\d*$/;
        return(reNum.test(num));
    }
    if (currentPage=="")
    {
        alert("页码不能为空");
        return;
    }
    if(!isNum(currentPage)){
        alert("输入错误")
        return;
    }

    ///判断currentPage是不是>=1  <=totalcount/p_size  不是alert
    if(!(currentPage >= 1 && currentPage <= Math.ceil(totalcount/p_size )))
    {
        alert("页码不存在");
        return ;
    }
    LoadPage(currentPage,globalSearchParam)


    //alert(currentPage)

})

//暂时不用了
function scroll(upJQuery) {


    console.log("html():"+$(upJQuery).parent().next().text())

    //console.log($(upJQuery).parent().next().text() == "上传中...")
    //console.log($(upJQuery).parent().next().text() == "上传中......")


    if ($(upJQuery).parent().next().text() == "上传中...") {

        $(upJQuery).parent().next().html("上传中......")

    }else if ($(upJQuery).parent().next().text() == "上传中......") {

        $(upJQuery).parent().next().html("上传中...")

    }else{


    }



}


function bytesToSize(bytes) {
    if (bytes === 0) return '0 B';
    var k = 1000, // or 1024
        sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        i = Math.floor(Math.log(bytes) / Math.log(k));
    return (bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i];
}

function uploadProgress(evt, upJQuery) {
    var loaded = evt.loaded;                  //已经上传大小情况
    var tot = evt.total;                      //附件总大小
    var per = Math.floor(100*loaded/tot);     //已经上传的百分比
    if(per == 100){
        $(upJQuery).parent().next().html("上传结束，等待响应，将马上完成");
    }else{
        $(upJQuery).parent().next().html("上传中，大小："+bytesToSize(tot)+"，已完成："+ per +"%");
    }


    //$("#son").css("width" , per +"%");
}


function upload(uu_url, upJQuery, upfile, param, upName){
    console.log("upJQuery:"+upJQuery);
    console.log("upfile:"+upfile);
    console.log("param:"+param);
    console.log("upName:"+upName);

    $(upJQuery).on('click', function() {

        if($(upfile).get(0).files[0]==undefined){
            $(upJQuery).parent().next().html("请选择文件!");
            return;
        }

        //var timer = setInterval('scroll(upJQuery);', 1000);

        var fd = new FormData();
        //fd.append("count", 1);
        fd.append("upfile", $(upfile).get(0).files[0]);
        console.log("$(upfile).get(0).files[0]:"+$(upfile).get(0).files[0])
        var file_name = $(upfile).get(0).files[0]['name'];
        $.ajax({
            url: "ajax_action_upload.php?uu=" + uu_url,
//                url: "test",
//            url: "http://192.168.120.234/file/upload",

            type: "POST",
//            processData: false,
//            contentType: "multipart/form-data",
            cache: false,
            contentType: false,
            processData: false,
            data: fd,
            //这里我们先拿到jQuery产生的 XMLHttpRequest对象，为其增加 progress 事件绑定，然后再返回交给ajax使用
            xhr: function(){
                var xhr = $.ajaxSettings.xhr();
                if(uploadProgress && xhr.upload) {
                    xhr.upload.addEventListener("progress" , function () { uploadProgress(event,upJQuery) }, false);
                    return xhr;
                }
            },
            success: function(d) {
                //    var data = "{\"msg\":[{\"file_path\":\"/media/test/20161019103825_126367.php\"}],\"code\":200}";
                console.log(d)
                var ret = JSON.parse(d);

                $(param).attr("value", ret.msg[0].file_path)

                if($(upName)) {
                    $(upName).attr("value", file_name)

                    $(upName).val(file_name);//修改文件可见
                }

                if(ret.code == 200){
                    $(upJQuery).parent().next().html("上传成功!")
                }else{
                    $(upJQuery).parent().next().html("服务器错误!")
                }

                $(upJQuery).prop('disabled',"true");
            },
            beforeSend: function () {
                $(upJQuery).parent().next().html("上传中...")
            },
            error: function () {
                $(upJQuery).parent().next().html("")
                alert("无法连接服务器");
            },
            complete: function () {
                //console.log("clearInterval"+timer)
                //clearInterval(timer);
            }

        });
    });

    $(upfile).change(function() {
        $(upJQuery).removeAttr('disabled')
        $(upJQuery).parent().next().html("")
        $(param).attr("value","");
        if(($(upName))) {
            $(upName).attr("value","");
            $(upName).val(''); //修改文件可见
        }
    })
}

function upload_rule(upJQuery, upfile, param){
    console.log("upJQuery:"+upJQuery)
    console.log("upfile:"+upfile)
    console.log("param:"+param)

    $(upJQuery).on('click', function() {

        if($(upfile).get(0).files[0]==undefined){
            $(upJQuery).parent().next().html("请选择文件!")
            return;
        }

        //var timer = setInterval('scroll(upJQuery);', 1000);

        var fd = new FormData();
        //fd.append("count", 1);
        fd.append("upfile", $(upfile).get(0).files[0]);
        console.log("$(upfile).get(0).files[0]:"+$(upfile).get(0).files[0])
        $.ajax({
            url: "ajax_action_upload.php?uu=rule.fileupload",
//                url: "test",
//            url: "http://192.168.120.234/file/upload",

            type: "POST",
//            processData: false,
//            contentType: "multipart/form-data",
            cache: false,
            contentType: false,
            processData: false,
            data: fd,
            //这里我们先拿到jQuery产生的 XMLHttpRequest对象，为其增加 progress 事件绑定，然后再返回交给ajax使用
            xhr: function(){
                var xhr = $.ajaxSettings.xhr();
                if(uploadProgress && xhr.upload) {
                    xhr.upload.addEventListener("progress" , function () { uploadProgress(event,upJQuery) }, false);
                    return xhr;
                }
            },
            success: function(d) {
                //    var data = "{\"msg\":[{\"file_path\":\"/media/test/20161019103825_126367.php\"}],\"code\":200}";
                // console.log(d)
                var ret = JSON.parse(d);

                $(param).attr("value", ret.msg[0].file_path)

                if(ret.code == 200){
                    $(upJQuery).parent().next().html("上传成功!")
                }else{
                    $(upJQuery).parent().next().html("服务器错误!")
                }

                $(upJQuery).prop('disabled',"true");
            },
            beforeSend: function () {
                $(upJQuery).parent().next().html("上传中...")
            },
            error: function () {
                $(upJQuery).parent().next().html("")
                alert("无法连接服务器");
            },
            complete: function () {
                //console.log("clearInterval"+timer)
                //clearInterval(timer);
            }

        });
    });

    $(upfile).change(function() {
        $(upJQuery).removeAttr('disabled')
        $(upJQuery).parent().next().html("")
        $(param).attr("value","");
    })
}

// 插件上传
function upload2(upJQuery, upfile, upPath, upName){
    console.log("upJQuery:"+upJQuery)
    console.log("upfile:"+upfile)
    console.log("upPath:"+upPath)
    console.log("upName:"+upName)

    $(upJQuery).on('click', function() {

        if($(upfile).get(0).files[0]==undefined){
            $(upJQuery).parent().next().html("请选择文件!")
            return;
        }

        //var timer = setInterval('scroll(upJQuery);', 1000);

        var fd = new FormData();
        //fd.append("count", 1);
        fd.append("upfile", $(upfile).get(0).files[0]);
        console.log("$(upfile).get(0).files[0]:"+$(upfile).get(0).files[0]['name'])
        var file_name = $(upfile).get(0).files[0]['name'];
        $.ajax({
            url: "ajax_action_upload.php?uu=plugin.fileupload",
//                url: "test",
//            url: "http://192.168.120.234/file/upload",

            type: "POST",
//            processData: false,
//            contentType: "multipart/form-data",
            cache: false,
            contentType: false,
            processData: false,
            data: fd,
            //这里我们先拿到jQuery产生的 XMLHttpRequest对象，为其增加 progress 事件绑定，然后再返回交给ajax使用
            xhr: function(){
                var xhr = $.ajaxSettings.xhr();
                if(uploadProgress && xhr.upload) {
                    xhr.upload.addEventListener("progress" , function () { uploadProgress(event,upJQuery) }, false);
                    return xhr;
                }
            },
            success: function(d) {
                //    var data = "{\"msg\":[{\"file_path\":\"/media/test/20161019103825_126367.php\"}],\"code\":200}";
                console.log(d)
                var ret = JSON.parse(d);

                $(upPath).attr("value", ret.msg[0].file_path)
                $(upName).attr("value", file_name)

                $(upName).val(file_name);//修改文件可见

                if(ret.code == 200){
                    $(upJQuery).parent().next().html("上传成功!")
                }else{
                    $(upJQuery).parent().next().html("服务器错误!")
                }

                $(upJQuery).prop('disabled',"true");
            },
            beforeSend: function () {
                $(upJQuery).parent().next().html("上传中...")
            },
            error: function () {
                $(upJQuery).parent().next().html("")
                alert("无法连接服务器");
            },
            complete: function () {
                //console.log("clearInterval"+timer)
                //clearInterval(timer);
            }

        });
    });

    $(upfile).change(function() {
        $(upJQuery).removeAttr('disabled')
        $(upJQuery).parent().next().html("")
        $(upPath).attr("value","");
        $(upName).attr("value","");
        $(upName).val(''); //修改文件可见
    })
}

// 管理中心备案信息上传
function uploadCenter(upJQuery, upfile, param){
    $(upJQuery).on('click', function() {
        if($(upfile).get(0).files[0]==undefined){
            $(upJQuery).parent().next().html("请选择文件!")
            return;
        }
        var fd = new FormData();
        fd.append("upfile", $(upfile).get(0).files[0]);
        $.ajax({
            url: "ajax_action_upload.php?uu=detector_info.fileupload",
            type: "POST",
            cache: false,
            contentType: false,
            processData: false,
            data: fd,
            //这里我们先拿到jQuery产生的 XMLHttpRequest对象，为其增加 progress 事件绑定，然后再返回交给ajax使用
            xhr: function(){
                var xhr = $.ajaxSettings.xhr();
                if(uploadProgress && xhr.upload) {
                    xhr.upload.addEventListener("progress" , function () { uploadProgress(event,upJQuery) }, false);
                    return xhr;
                }
            },
            success: function(d) {
                var ret = JSON.parse(d);

                $(param).attr("value", ret.msg[0].file_path)

                if(ret.code == 200){
                    $(upJQuery).parent().next().html("上传成功!")
                }else{
                    $(upJQuery).parent().next().html("服务器错误!")
                }

                $(upJQuery).prop('disabled',"true");
            },
            beforeSend: function () {
                $(upJQuery).parent().next().html("上传中...")
            },
            error: function () {
                $(upJQuery).parent().next().html("")
                alert("无法连接服务器");
            },
            complete: function () {
            }

        });
    });

    $(upfile).change(function() {
        $(upJQuery).removeAttr('disabled')
        $(upJQuery).parent().next().html("")
        $(param).attr("value","");
    })
}


function firstSelect(id){
    var module = $("#"+id).parent().parent()
    var first_text = module.find("li:first").text()
    var first_value = module.find("li:first").attr("value")
    module.find("span:first").attr("value",first_value)
    module.find("span:first").text(first_text);
}


function setSelect(id,v){
    var module = $("#"+id).parent().parent()

    var elem = module.find("li");

    var first_text = module.find("li:first").text()
    var first_value = module.find("li:first").attr("value")
/*    console.log('v:'+v)
    console.log('first_text:'+first_text)
    console.log('first_value:'+first_value)*/

    elem.each(function(){
        //carray.push(parseInt($(this).attr("id")))
        if($(this).attr("value")==v){
            first_text = $(this).text()
            first_value = $(this).attr("value")
/*            console.log('first_text:'+first_text)
            console.log('first_value:'+first_value)*/
        }

    })

    module.find("span:first").attr("value",first_value)
    module.find("span:first").text(first_text);
}
/*
$("#searchButton").focus(function() {
    $(this).parent().parent().find("input[type='text']").each(function(){
        var value = $(this).val(); //这里的value就是每一个input的value值~

        if(!value.match(/^[\u4E00-\u9FA5a-zA-Z0-9_]{0,}$/)){


            var label = $(this).attr('placeholder')

            var error_str =label+"存在非法字符\n";

            alert(error_str)

        }

    });

})*/




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
}


$("#chk_all1,#chk_all2").click(function(){
    if(this.checked){
        $("table :checkbox").prop("checked", true);
    }else{
        $("table :checkbox").prop("checked", false);
    }
});

///绑定复选框选择事件
function rebindChkAll(){

    $("#maintable tbody tr :checkbox").click(function(){

        alterChkAll();

    });

    alterChkAll();
}







//第五种方法
var idTmr;
function  getExplorer() {
    var explorer = window.navigator.userAgent ;
    //ie
    if (explorer.indexOf("MSIE") >= 0) {
        return 'ie';
    }
    //firefox
    else if (explorer.indexOf("Firefox") >= 0) {
        return 'Firefox';
    }
    //Chrome
    else if(explorer.indexOf("Chrome") >= 0){
        return 'Chrome';
    }
    //Opera
    else if(explorer.indexOf("Opera") >= 0){
        return 'Opera';
    }
    //Safari
    else if(explorer.indexOf("Safari") >= 0){
        return 'Safari';
    }
}
function method5(tableid) {
    $("#export_div").hide();

    $("#export_div").html($("#maintable").clone());

    $("#export_div #maintable").attr('id','export_maintable');

    $("#export_div #export_maintable tfoot").remove();

    //$("#export_div #export_maintable tr th:eq(0)").remove();
    $("#export_div #export_maintable tr :first-child").remove();
    $("#export_div #export_maintable tr :last-child").remove();

    $("#export_div #export_maintable tbody tr td").each(function(){
        if($(this).text().match(/^[0-9]{0,}$/)){
            $(this).text("["+$(this).text()+"]");
        }

    });

    tableid = export_maintable;


    if(getExplorer()=='ie')
    {
        alert('请使用Chrome浏览器');

    }
    else
    {
        tableToExcel(tableid)
    }
}
function Cleanup() {
    window.clearInterval(idTmr);
    CollectGarbage();
}
var tableToExcel = (function() {
    var uri = 'data:application/vnd.ms-excel;base64,',
        template = '<html><head><meta charset="UTF-8"></head><body><table border="1">{table}</table></body></html>',
        base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) },
        format = function(s, c) {
            return s.replace(/{(\w+)}/g,
                function(m, p) { return c[p]; }) }
    return function(table, name) {
        if (!table.nodeType) table = document.getElementById(table)
        var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
        window.location.href = uri + base64(format(template, ctx))
    }
})()



$("#addModal input textarea").blur(function(){
    var value = $(this).val(); //这里的value就是每一个input的value值~

    //re= /select|update|delete|exec|count|script|'|"|=|;|>|<|%/i;
    re= /select|update|delete|exec|count|script|>|<|%/i;
    if ( re.test(value) ){

        //error_str+=label+"存在非法字符\n";
        alert("请您不要在参数中输入脚本字符和SQL关键字！");
        $("#add-submit").attr("disabled", true);
    }else{

        $("#add-submit").removeAttr("disabled");

    }

});



var helper_ele = "&nbsp;<i class=\"fa fa-question-circle hint-helper\" onmouseenter=\"showHint(this);\" onmouseleave=\"hideHint(this);\" style=\"color: darkgrey; \"></i>";


var rule_keyword_helper_text = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;规则内容分为正则表达式和关键词表达式，正则表达式参考正则规则；关键词表达式支持\"与\"、\"非\"和距离（说明：或关系由后台拆分为多个关键词表达式），定义如下：<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(a)\t使用英文字符\" &\"表示\"与\"关系，如：\"word1\"&\"word2\"，表示同时存在\"word1\"和\"word2\"；<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b)\t使用英文字符\" !\"表示\"非\"关系，如：!\" word3\"，表示不存在\"word3\"；<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(c)\t使用成对大括号\" {\"、\" }\"和文字符\",\"，表示相对于上一个关键词的距离范围，单位为字节，如{6,10}，表示距离在6到10字节之间；{0,6}，表示距离小于等于6；{10,0}，表示距离大于等于10，0表示无穷大；位于上一个关键词之后，如\"word1\"{6,10}&\"word2\"，表示同时存在\"word1\"和\"word2\"，并\"word2\"的开始位置位于\"word1\"后6到10个字节内；{0, 0}可以省略不写，如\"word1\"{0, 0}&\"word2\" 表示\"word2\"在\"word1\"任意位置，省略{0, 0}后关键词表达式为 \"word1\"&\"word2\"；表示同时存在\"word1\"和\"word2\"(\"word2\"可能在\"word1\"前)。<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(d)\t当对关键词表达式中关键词存在特殊字符(含:\"&\"、\"!\"、\"{\"、\" }\"、\",\" 、\"\\\"、 \"\"\"、 \" \")时, 使用英文字符\"\\\"进行转义；如 \\&\\&&\\\\\\\\，表示同时存在\" &&\"和\"\\\\\"两个关键词；<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(e)\t关键词表达中关键词顺序：距离、\"与\"关系、\"非\"关系，如：" +
    "\"word1\"{3,9}&\"word2\"{6,12}&\"word3\"&\"word4\"! \"word5\"! \"word6\"；<br/>";
var rule_encryption_helper_text = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\"文件最小值\"和\"文件最大值\"设置了加密文件筛选的大小区间，如\"文件最小值\"设为10，\"文件最大值\"设为100，则大小在10KB-100KB之间的文件回传";
var rule_compress_helper_text = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\"压缩层数\"只有0和1两种取值，\"0\"表示对压缩层数没有要求，\"1\"表示压缩层数超过1层的压缩文件回传<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\"回传压缩文件大小\"表示需要检测压缩文件大小限制，\"丢弃压缩文件大小\"表示需要丢弃压缩文件大小限制，注意：<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(a)\t当压缩文件大小大于\"丢弃压缩文件大小\"所设值时，检测器丢弃该压缩文件；<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(b)\t当压缩文件大小介于\"回传压缩文件大小\"和\"丢弃压缩文件大小\"所设值之间时，回传压缩文件到检测器管理系统；<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(c)\t当压缩文件小大小于\"回传压缩文件大小\"时，需检测器解压并进行压缩深度判断；<br/>" +
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(d)\t\"丢弃压缩文件大小\"需要大于\"回传压缩文件大小\"<br/>";
var rule_picture_helper_text = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;图片大小在\"图片最小值\"和\"图片最大值\"所设值的区间内的图片回传到检测器管理系统，如，\"图片最小值\"设为10，\"图片最大值\"设为100，则大小在10KB-100KB之间的图片回传";

var director_config_ip_whitelist_helper_text = "该字段用于设置管理中心接收指挥节点下行数据的IP白名单";
var director_config_reset_helper_text = "管理中心主动断开与指挥节点的连接，断开后可重新配置连接或连接其他指挥节点";

var detector_audit_mode = '人工模式: 检测器需先提交备案信息，在检测器提交注册信息之后，人工在界面完成审核<br/>' +
                            '自动模式: 检测器同样需要提交备案信息，在检测器提交注册信息时会直接进行后台自动审核';

var longTextHintHelper = {
    self_textarea: "",

    init: function () {
        console.log("helper.init()");
        this.self_textarea = $("<span class=\"hidden\" style=\"font-size: 14px; text-align: justify; z-index: 100; width: 500px; height: fit-content; padding: 8px; border: 4px solid lightgray; background-color: white; border-radius: 4px;\">文字解释</span>");
        this.self_textarea.appendTo($("body"));
    },

    show: function (parent_ele, _hint_text) {
        if(_hint_text != "") {
            $(this.self_textarea).html(_hint_text);
        }
        var parent_y = $(parent_ele).offset().top;
        var parent_x = $(parent_ele).offset().left;
        var self_y = parent_y + $(parent_ele).height();
        var self_x = parent_x + $(parent_ele).width();
        // console.log("HintHelper：", self_x, self_y, _hint_text);
        $(this.self_textarea).appendTo($(parent_ele).parent());
        $(this.self_textarea).css("position", "absolute");
        $(this.self_textarea).css("margin-top", $(parent_ele).height());
        $(this.self_textarea).offset().top = self_y;
        $(this.self_textarea).offset().left = self_x;
        $(this.self_textarea).removeClass("hidden");
    },

    hide: function () {
        this.self_textarea.addClass("hidden");
        $(this.self_textarea).css("position", "relative");
    }

};

longTextHintHelper.init();

//    $('i.hint-helper').click(function () {
//        showHint(this);
//    }).mouseenter(function () {
//        showHint(this);
//    }).mouseleave(function () {
//        console.log("mouseleave");
//        longTextHintHelper.hide();
//    });
function showHint(obj) {
    $(obj).css("color", "darkgrey");
    longTextHintHelper.show(obj, $(obj).attr("value"));
}
function hideHint(obj) {
    $(obj).css("color", "gray");
    longTextHintHelper.hide();
}


var col_size = $("#maintable").find("th").length;//表格列数
console.log('col_size:'+col_size);
if($("#maintable tfoot>tr>td>input.checkbox").length > 0) {
    $("#maintable tfoot td:eq(1)").attr("colspan", col_size - 1);
} else {
    $("#maintable tfoot td:eq(0)").attr("colspan", col_size);
}


var CityHelper = {

    $citypicker: null,
    $node_index_serial_prefix_map: {0: '001', 1: '010', 2: '011', 3: '100'},
    $serial_suffix: '01100',

    init: function(citypicker){
        this.$citypicker = citypicker;
        this.$citypicker.citypicker();
    },

    reset: function () {
        $('#add_serial').val("");   // 清空序列号
        this.$citypicker.citypicker('reset');
    },

    setCityPickerLevel: function (obj) {
        var type = parseInt($(obj).attr("value"));
        var placeholder = "";
        var data_level = "district";
        var city_str = "<input id=\"city-picker\" class=\"form-control\" style=\"width:365px;\" readonly type=\"text\" placeholder=\"请选择对应的省/地市/县区\"\n" +
            "                                           data-toggle=\"city-picker\">";
        var city_picker_div = $("#distpicker div div");
        if(type == 0) {
            console.log('type==0');
            placeholder = "选择了国家节点";
        } else if(type == 1) {
            placeholder = "请选择对应的省";
            data_level = "province";
        } else if(type == 2) {
            placeholder = "请选择对应的省/地市";
            data_level = "city";
        } else if(type == 3) {
            placeholder = "请选择对应的省/地市/县区";
        } else {
            placeholder = "请选择节点类型";
        }
        city_picker_div.html(city_str);
        this.$citypicker = $('#city-picker');
        this.$citypicker.attr("placeholder", placeholder);
        this.$citypicker.attr("data-level", data_level);
        this.$citypicker.citypicker();
        if(type != 1 && type != 2 && type != 3) {
            this.$citypicker.citypicker('destroy');
        }
    },

    generateNodeSerial: function(index, serial_node) {
        var code = "000000";
        // console.log("##########" + code);
        if(index != 0) {
            code = this.$citypicker.data('citypicker').getCode();
            var code_list = code.split('/');
            code = code_list[code_list.length - 1]
        }
        var middle = this.appendPrefixZeroToFixedLength(parseInt(code.substring(0, 2)).toString(2)) + this.appendPrefixZeroToFixedLength(parseInt(code.substring(2, 4)).toString(2)) + this.appendPrefixZeroToFixedLength(parseInt(code.substring(4, 6)).toString(2));
        console.log("code: " + code + " binary_middle: " + middle);
        // var serial = parseInt(this.$node_index_serial_prefix_map[index] + middle + this.$serial_suffix + this.generateZeroStr(), 2);
        var serial_str = this.$node_index_serial_prefix_map[index] + middle + this.$serial_suffix;
        console.log("serial: " + serial_str);
        $(serial_node).val(parseInt(serial_str, 2).toString());
        return parseInt(serial_str, 2);
    },

    generateZeroStr: function (length) {
        var zeroStr = "";
        length = length || 32;
        for(var i = 0; i < length; i++) {
            zeroStr += '0';
        }
        return zeroStr
    },

    appendPrefixZeroToFixedLength: function (str, length) {
        str = str.toString().trim();
        length = length || 8;
        if(str.length >= length) {
            return str.substring(0, length);
        } else {
            for(var i = str.length; i < length; i++) {
                str = '0' + str;
            }
            return str;
        }
    }
};

function isonlineFormat_new(status){
    var is_onlineMap={1:'在线',0:'离线'};
    var status_html = $('<span>'+is_onlineMap[status]+'</span>')
    switch(status){
        case 0:
            $(status_html).css('color','red');
            break;
        case 1:
            $(status_html).css('color','green');
            break;
    }
    return status_html;
}