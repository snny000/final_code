/**
 * Created by Fernando on 2016/7/7.
 */
function selectProtoFwd(obj) {
    $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
    $(obj).parent().parent().find("span:first").text($(obj).text());
    //$("#"+id).attr("value",$(obj).attr("value"));
    // $("#"+id).text($(obj).text());
}

var option = {
    //  totalPages: totalPages,
    visiblePages: 3,
    first: "<<",
    prev: "<",
    next: ">",
    last: ">>",
    onPageClick: function (event, page){
        $.ajax({
            url: option.myurl+"&pn="+page,
            type: "post",
            data: option.searchParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 200) {

                    List(ret["msg"]);
                } else if (ret["code"] == 20000) {
                    $("#maintable tbody tr").remove();
                    $("<tr><td colspan='8' style='text-align: center'><h4>没有消息</h4></td></tr>").appendTo("#maintable tbody");
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



/////全选逻辑
$("#chk_all1,#chk_all2").click(function(){
    if(this.checked){
        $("table :checkbox").prop("checked", true);


        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            var device_id=$(this).parent().parent().find("td:eq(1)").text();
            globalSelectedDetetors[$(this).attr("id")] = device_id;

        })


    }else{


        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox");
        // var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            delete globalSelectedDetetors[$(this).attr("id")];

        })


        $("table :checkbox").prop("checked", false);

    }

    selectedDetetorsRefresh();
});





function List(msgListObj){

    var address_codeMap={'100000':'北京','200000':'上海','510000':'广州'};
    var device_statusMap={1:'正常运行',2:'暂未审核',3:'审核失败',4:'认证失败',5:'流量异常',7:'系统异常',8:'资源异常',9:'策略异常'};
/*    var contractorMap={'01':'厂商1', '02':'厂商2', '03':'厂商3'};*/



    var imgMap = {
        1: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
        2: "<i class='fa fa-circle' style='color:#5BC0DE; font-size:xx-small ' />",
        3: "&nbsp;&nbsp;<span style='background: #FF9900;padding: 3px;border-radius: 5px; color: white'>置顶</span>"
    }

    var device_status_imgMap = {
        1: "<i class='fa fa-circle' style='color:#5BC0DE; font-size:xx-small ' />",
        2: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
        3: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
        4: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
        5: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
        6: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
        7: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>",
        8: "<strong style='color:red;font-size:18px'>!&nbsp;&nbsp;</strong>"

    }



    //var _row = $("#content").clone();
    //$("#content").remove();
    $("#maintable tbody tr").remove();

    var _row = $("<tr><td></td><td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td><td style='color:#999999'></td></tr>");

    for (var i = 0; i < msgListObj.length; i++) {
        var row = _row.clone();
        var imghtml = '';
        var titlehtml = "<a target= _blank href = 'detector_detail.php?id="+msgListObj[i].id+"' style='color:#000000'>"+msgListObj[i].device_id+"</a>";

        //row.attr("id",msgListObj[i].id)
        // row.find("td:eq(0)").html("<input type='checkbox' class='checkbox'>")
        //  row.find("td:eq(1)").text(msgListObj[i].id);
//            row.find("td:eq(1)").html(device_status_imgMap[msgListObj[i].device_status]+titlehtml);
        //var row = _row.clone();row.attr("id",msgListObj[i].id)
        if(globalSelectedDetetors[msgListObj[i].id]==undefined){
            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' id="+msgListObj[i].id+">");
        }else{

            row.find("td:eq(0)").html("<input type='checkbox' class='checkbox' checked='checked' id="+msgListObj[i].id+">");
        }


        row.find("td:eq(1)").html(msgListObj[i].device_id);
        row.find("td:eq(2)").text(contractorMap[msgListObj[i].contractor]);
        row.find("td:eq(3)").html(address_codeMap[msgListObj[i].address_code]?address_codeMap[msgListObj[i].address_code]:"未知地区");
        row.find("td:eq(4)").html(msgListObj[i].organs);
        row.find("td:eq(5)").html(isonlineFormat_new(msgListObj[i].is_online));
        row.find("td:eq(6)").text(msgListObj[i].last_warning_time);

        row.show();
        row.appendTo("#maintable tbody");


    }




///绑定复选框选择事件
    $("#maintable tbody tr :checkbox").click(function(){
        //alert("333333333333333");

        if(this.checked){
            //$("table :checkbox").prop("checked", true);
            // selected_detetors
            //$("#selected_detetors").remove();

            //this.id
            var id=$(this).attr('id');
            var device_id=$(this).parent().parent().find("td:eq(1)").text();
            //device_id.appendTo("#selected_detetors");
            //alert(device_id);
            globalSelectedDetetors[id] = device_id;
            //console.log(globalSelectedDetetors);
            //$("#selected_detetors").append(device_id+" ");

            // $("#selected_detetors").refresh();
        }else{

            var id=$(this).attr('id');
            delete globalSelectedDetetors[id];
            //console.log(globalSelectedDetetors);
            //globalSelectedDetetors
            //$("table :checkbox").prop("checked", false);
        }

        selectedDetetorsRefresh();
        ///处理复选框全选
        alterChkAll();
    });

///处理复选框全选
    alterChkAll();

    alterChkList();

    /*
     $("tbody tr a").click(function () {
     console.log("test")
     window.location.href = "message_detail.php?id="+$(this).parent().parent().attr("id");
     })
     */
}


////刷新选中列表
function selectedDetetorsRefresh(){



    $("#selected_detetors").empty();

    $("#selected_detetors").append("<strong>选择检测器"+Object.keys(globalSelectedDetetors).length+"：</strong> ")

    for (var key in globalSelectedDetetors){
        // console.log("属性：" + key + ",值："+ globalSelectedDetetors[key]);
        $("#selected_detetors").append("<img src='images/del.gif' onclick='delId(" + key + ")'>"+globalSelectedDetetors[key]+" ");
    }
    //alert("333333333333333");

}



///处理复选框列表
function alterChkList(){
    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox");
    checkboxs.each(function(id){

        if(globalSelectedDetetors[$(this).attr("id")]==undefined){
            $("#"+id).prop("checked", false);
        }else{
            $("#"+id).prop("checked", true);
        }




        //carray.push(parseInt($(this).attr("id")))
    })



}


///删除小图片事件
function delId(id){
    //var id=$(this).attr('id');
    delete globalSelectedDetetors[id];

    /// $("#maintable tbody tr");

    $("#"+id).prop("checked", false);


    selectedDetetorsRefresh();
    alterChkAll();
}


function LoadPage(currentPage,searchParam){
    $.ajax({
        url: "/ajax_action_detector.php?uu=detector.count",
        type: "post",
        data: searchParam,
        success:function(data) {
            var ret = JSON.parse(data);
            if (ret["code"] == 200)
                ret = ret["msg"]["count"]
            else {
                ret = 0;
            }
            $("#totalcount2").text(ret);
            $("#totalcount2").attr("value",1);
            $("#totalcount").text(ret);
            $('#pagination').empty();
            $('#pagination').removeData("twbs-pagination");
            $('#pagination').unbind("page");
            pagination(ret,"/ajax_action_detector.php?uu=detector.show&p_size="+p_size,parseInt(currentPage),searchParam)
        },
/*        beforeSend: function () {
         $(".loading-pic").removeClass("hidden");
         },*/
        beforeSend: function () {
            $("#maintable tbody tr").remove();
            $("#maintable tbody").append("<tr><td colspan='7'  style='text-align: center'><img src='images/loading.gif'></td></tr>")
        },
        error: function () {
            alert("无法连接服务器");
        }
    })
}
