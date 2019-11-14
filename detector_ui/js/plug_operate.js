$("#clean").click(function(){

    $('#hintModal').find(".modal-title").html("清空提示框")

    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");

    if(checkboxs.size() == 0){
        alert("请选择清空数据");
        return;
    }

    var carray =new Array();
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status != '(删除)待同步'){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length==0){
        alert('当前插件已删除，不能变更生效范围!');
        return;
    }

    var content = "<p >将清空<span style='color: red;font-size: large'>"+carray.length+"</span>条数据，请确认，此操作为批量将选择的插件设置为无检测器生效</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='delSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#delSubmit").click(function(){
        var carray =new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            carray.push(parseInt($(this).attr("id")))
        })
        console.log("carray:"+carray)
        var issuedParam = {}

        issuedParam["id"] = JSON.stringify(carray);
        issuedParam["detector_id_list"] = "[0]"
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin.change_plug",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret["code"] == 200){
                    alert("检测器生效范围还原成功");
                    //$("#issuedButton").prop('disabled',"true");
                    refresh()
                }else{
                    alert("检测器生效范围还原失败");
                }

            }
        })

        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})



$("#recover").click(function(){
    //$('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("还原提示框")

    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");

    if(checkboxs.size() == 0){
        alert("请选择还原数据");
        return;
    }

    var carray =new Array();
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status != '(删除)待同步'){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length==0){
        alert('当前插件已删除，不能变更生效范围!');
        return;
    }


    // var carray1 =new Array()
    // checkboxs.each(function(){
    //     carray1.push($(this).attr("value"))
    //})

    //var unique_carray= unique(carray1)

    // if(unique_carray.length>1){

    //     alert("还原数据原范围不一致，请重新选择");
    //    return;

    //}


    var content = "<p >将还原<span style='color: red;font-size: large'>"+carray.length+"</span>条数据，请确认，此操作为批量将选择的插件设置为全部检测器生效</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='delSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#delSubmit").click(function(){
        var carray =new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            carray.push(parseInt($(this).attr("id")))
        })
        console.log("carray:"+carray)
        var issuedParam = {}

        issuedParam["id"] = JSON.stringify(carray);
        issuedParam["detector_id_list"] = "[]"
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin.change_plug",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret["code"] == 200){
                    alert("检测器生效范围还原成功");
                    //$("#issuedButton").prop('disabled',"true");
                    refresh()
                }else{
                    alert("检测器生效范围还原失败");
                }

            }
        })

        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})

$("#append").click(function(){
    // $('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("追加提示框")

    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");

    if(checkboxs.size() == 0){
        alert("请选择变更数据");
        return;
    }

    var carray =new Array();
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status != '(删除)待同步'){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length==0){
        alert('当前插件已删除，不能变更生效范围!');
        return;
    }


    /*        var carray1 =new Array()
     checkboxs.each(function(){
     carray1.push($(this).attr("value"))
     })



     var unique_carray = unique(carray1)

     //alert("###"+carray1+"--------"+unique_carray+"--------")

     if(unique_carray.length>1){

     alert("变更数据原范围不一致，请重新选择");
     return;

     }*/


    var content = "<p >将变更<span style='color: red;font-size: large'>"+carray.length+"</span>条数据，请确认，此操作为批量对选择的插件设置追加一定数量的生效检测器</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='delSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#delSubmit").click(function(){
        var carray =new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            carray.push(parseInt($(this).attr("id")))
        })
        //console.log("carray:"+carray)

        pickDetectorForward(carray,[],2)


        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})

$("#alter").click(function(){

    //$('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("变更提示框")

    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");

    if(checkboxs.size() == 0){
        alert("请选择变更数据");
        return;
    }

    var carray =new Array();
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status != '(删除)待同步'){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length==0){
        alert('当前插件已删除，不能变更生效范围!');
        return;
    }


    var carray1 =new Array()
    checkboxs.each(function(){
        carray1.push($(this).attr("value"))
    })



    var unique_carray = unique(carray1)

    //alert("###"+carray1+"--------"+unique_carray+"--------")

    if(unique_carray.length>1){

        alert("变更数据原范围不一致，请重新选择");
        return;

    }


    var content = "<p >将变更<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，此操作为批量对选择的插件设置检测器生效范围</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='delSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#delSubmit").click(function(){
        var carray =new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            carray.push(parseInt($(this).attr("id")))
        })
        //console.log("carray:"+carray)

        pickDetectorForward(carray,unique_carray[0],1)


        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})

$("#delete").click(function () {
    $('#hintModal').find(".modal-title").html("删除提示框")

    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");

    if (checkboxs.size() == 0) {
        alert("请选择删除数据");
        return;
    }
    // 判断是否有未同步数据
    var carray =new Array();
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status != '(删除)待同步' && status !="已同步"){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length!=0){
        var r = confirm('当前有未同步数据，是否坚持删除这些数据？');
        if(!r)
            return;
    }

    var content = "<p >将删除<span style='color: red;font-size: large'>" + checkboxs.size() + "</span>条数据，请确认</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='delSubmit' type='button' class='btn btn-primary'>确定</button>" +
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#delSubmit").click(function () {
        var carray = new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function () {
            carray.push(parseInt($(this).attr("id")))
        })
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin/delete_plug",
            type: "post",
            data: { id: JSON.stringify(carray) },
            success: function (data) {
                //  var ret = JSON.parse(data);
                console.log(data)
                refresh()
            }
        })

        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})


function selectProtoFwd(obj) {
    $(obj).parent().parent().find("span:first").attr("value",$(obj).attr("value"))
    $(obj).parent().parent().find("span:first").text($(obj).text());
}


$("#full").click(function(){
    //  $('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("刷新检测器插件集")

    var content =
        "<span>下发方式:<span style='color: red;font-size: large'>刷新检测器插件集</span></span>"+
        "<p >下发规则个数:<span style='color: red;font-size: large'>"+$("#full span").text()+"</span></p>"+
        "<p >将在下一步选择下发的检测器</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='fullSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#fullSubmit").click(function(){
        var carray =new Array()
        pickDetectorForward(carray,[],4)
        //  $(this).prop('disabled',"true");

        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})

// 刷新管理中心插件集
$("#fullCenter").click(function(){
    $('#hintModal').find(".modal-title").html("上报管理中心插件")
    var content =
        // "<span>上报插件个数:<span style='color: red;font-size: large'></span></span>"+
        "<p >上报插件个数:<span style='color: red;font-size: large'>"+$("#full span").text()+"</span></p>"+
        "<p >将会上报至指挥节点</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='fullSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#fullSubmit").click(function(){
        var carray =new Array();
        pickCenterForward(carray,[],888)
        $('#hintModal').modal('hide')
    })
    $('#hintModal').modal('show')
})


$("#increment").click(function(){
    //  $('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("增量下发提示框")

    var content =
        "<span>下发方式:<span style='color: red;font-size: large'>增量下发</span></span>"+
        "<p >下发规则个数:<span style='color: red;font-size: large'>"+$("#increment span").text()+"</span></p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='incrementSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#incrementSubmit").click(function(){
        $.ajax({
            url: "/ajax_action_detector.php?uu=plugin.plug_synchronization&type=0",
            type: "post",
            data:null,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert("增量下发成功");
                }else{
                    alert("增量下发失败");
                }
                refresh()
            }
        })
        //  $(this).prop('disabled',"true");

        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})





function generateoperateviewhtml(id,device_id_list){
    var num =eval(device_id_list).length
    var operateviewhtml=""

    if(device_id_list=='[0]'){
        operateviewhtml = "未设置生效范围"
    }else if(device_id_list=='[]'){
        operateviewhtml = "全部检测器生效"
    }else if(num>0){
        operateviewhtml = "<a href=\"javascript:void(0);\" onclick=\'pickDetectorForward(" + id + ","+device_id_list+",3)\'>生效检测器数量"+eval(device_id_list).length+"（查看）</a>"

    }else{
        operateviewhtml="生效范围解析错误"
    }
     return operateviewhtml
}


function generateoperateviewhtml_new(id,device_id_list,plug_on_device_status,plug_status){
    var num =eval(device_id_list).length
    var operateviewhtml=""
    var plug_status = plug_status

    if(device_id_list=='[0]'){
        operateviewhtml = "没有检测器生效"
    }else if(device_id_list=='[]'){
        operateviewhtml = "全部检测器生效"
    }else if(num>0){
        if(plug_status == 0)
            operateviewhtml = "<a href=\"javascript:void(0);\" onclick=\'pickDetectorForward(" + id + ","+device_id_list+",999,"+plug_on_device_status+")\'>开启/关闭</a>"
    }else{
        operateviewhtml="生效范围解析错误"
    }
     return operateviewhtml
}



function generateoperatehtml(id,device_id_list){

    var num =eval(device_id_list).length
    var operatehtml=""
    if(device_id_list=='[0]'){
        operatehtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + id + ","+"[0]"+",1)\">变更生效范围</a>"
    }else if(device_id_list=='[]'){
        operatehtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + id + ","+"[]"+",1)\">变更生效范围</a>"
    }else if(num>0){
        operatehtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + id + ","+device_id_list+",1)\">变更生效范围</a>"
    }else{
        operatehtml="生效范围解析错误"
    }

    // if(node_type==2){
    //     operatehtml = '';
    // }
    // operatehtml = '';
    // 判断是否有编辑权限
    // var permission = JSON.parse(localStorage.roleResourceIds);
    // if(permission.indexOf(396)==-1){
    //     operatehtml = '';
    // }

    return operatehtml

}





upload("#upJQuery","#upfile","#param");


/* 2017/9/26 */
// 点击table行选中
$('#maintable').on('click','tbody tr td:not(:first-child)',function(){
    var currentCheckbox = $(this).parent().find('td').eq(0).find('input[type=checkbox]');
    if(currentCheckbox.prop('checked')){
        currentCheckbox.prop('checked',false)
    }else{
        currentCheckbox.prop("checked",true)
    }
})


$('.form_datetime').datetimepicker({
        language:  'zh-CN',
        minView: "month",
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayBtn: true
    });

// // 判断策略是本级添加还是下级上传的，隐藏相关操作
// var node_type = undefined; // 用于判断是本级添加还是下级添加，屏蔽相关操作
// if(document.location.href.indexOf('node_type=2')!=-1){
//     node_type = 2;
// }
// var is_contain_sub = 0; //查询的时候是否包含下级
// $(function(){
//     $('h4 .btn-group').addClass('btn-group-sm');
//     var is_contain_sub_html = '<label style="display:none;font-weight:normal;font-size:12px"><input onclick="isContainSub()" type="checkbox" >是否包含下级地区</label>';
//     var switchSub = 
//             '<button type="button" href="plug.php" class="btn btn-default"  >本级添加</button>'+
//          '<button type="button" href="plug.php?node_type=2" class="btn btn-default" node_type=2  >下级指挥添加</button>'
//             //'<button type="button" href="plug_manage.php" class="btn btn-default">管理中心上报</button>'
    
//     $('h4 .btn-group').html(switchSub);
//     // 下级指挥添加
//     if(node_type == 2){
//         $('h4 .btn-group button:eq(1)').addClass('btn-primary');
//         $('.upper-btn-group.margin_ddos1.pull-right').hide();
//         $('#maintable tfoot .pull-left button').not(':last').hide();
//         $('#searchButton').click();
//         $('#maintable th').eq(-2).hide();
//         $('#director_node').after(is_contain_sub_html)
//     // 本级添加
//     }else if(document.location.href.indexOf('manage') == -1){
//         $('h4 .btn-group button:eq(0)').addClass('btn-primary');
//         //var _colspan = parseInt($('#maintable tfoot td:eq(1)').attr('colspan'))
//         //$('#maintable tfoot td:eq(1)').attr('colspan',_colspan+1)
//         $('#maintable th').eq(-1).hide();
//     // 管理中心上传
//     }else{
//         $('h4 .btn-group button:eq(2)').addClass('btn-primary');
//         $('.upper-btn-group.margin_ddos1.pull-right').hide();
//         $('#maintable tfoot .pull-left button').not(':last').hide();
//         $('#director_node').after(is_contain_sub_html)
//     }
//     $('#virtual_group').parent().hide();
// })
// $('h4 .btn-group').on('click','button',function(){
//     window.location.replace($(this).attr('href'));
// })
// $('#director_node').change(function(){
//  $('#director_node').parent().next('label').css('display','table-footer-group');
// })
// function isContainSub(){
//     is_contain_sub = is_contain_sub == 0 ? 1 : 0;
// }
// 清除搜索取消勾选
$('#clearButton').on('click',function(){
    // if(is_contain_sub == 1){
    $('#director_node').parent().next('label').find('input[type=checkbox]').click();
        // is_contain_sub = 0;
    // }
})

//获取指挥节点并初始化下拉框
// var initDirectorNode = function () {
//     $.ajax({
//         url: "/ajax_action_detector.php?uu=command.get_detector_node",
//         success: function (data) {
//             var res = JSON.parse(data);
//             if (res.code == "200") {
//                 var nodeData = res["msg"]["node_list"];
//                 var nodeoption = "";
//                 nodeData.map(function(v,i){
//                     nodeoption+=`<option value=${v.node_id}>${v.name}</option>`
//                 })
//                 $('#director_node').append(nodeoption);
//                 $('#director_node').selectpicker('refresh');
//             }
//         }
//     })
// }
// initDirectorNode();

//获取管理中心并初始化table，根据指挥节点联动
// var initManageCenter = function(node_id){
//     var param = {};
//     if(node_id){
//         param["node_id"] = node_id;
//     }
//     $.ajax({
//         url: "/ajax_action_detector.php?uu=command.get_manage_num",
//         data:param,
//         success: function (data) {
//             var res = JSON.parse(data);
//             if (res.code == "200") {
//                 var count = res["msg"]["count"];
//                 $.ajax({
//                     url:"/ajax_action_detector.php?uu=command.get_manage_info&p_size="+count+"&pn=1",
//                     data:param,
//                     success:function(data){
//                         var res = JSON.parse(data);
//                         if(res.code == "200"){
//                             var centerData = res["msg"];
//                             var centeroption = "";
//                             centerData.map(function(v,i){
//                                 centeroption+=`<option value=${v.center_id}>${v.organs}${v.center_id}</option>`
//                             })
//                             $('#manage_center').append(centeroption);
//                             $('#manage_center').selectpicker('refresh');
//                         }
//                     }
//                 })
//             }
//         }
//     })
// }
// initManageCenter();

//上报管理中心插件集跳转
function pickCenterForward(id, device_id_list, type) {
    var param = { cacheRef: "plug.php" } //当前页面
    var currentPage = $('#pagination .active a').text()
    param["cachePage"] = currentPage
    param["cacheDevice_id_list"] = JSON.stringify(eval(device_id_list));
    param["cacheCmd_type"] = type;
    param["cacheSearchParam"] = JSON.stringify(globalSearchParam)
    param["cacheMenu"] = "menu-plug1";
    param["cacheType"] = 1;
    param["cachePolicy_type"] = 0; // 当前插件类型
    if (id instanceof Array) {
        param["cacheId"] = JSON.stringify(id);
    } else {
        var carray = new Array()
        carray.push(parseInt(id))
        param["cacheId"] = JSON.stringify(carray)
    }
    // post('plugin.fulldose_report', param);
    $.ajax({
        url: "/ajax_action_detector.php?uu=plugin.fulldose_report",
        // data:param,
        success: function (data) {
            var res = JSON.parse(data);
            if (res.code == "200") {
                console.log("1212")
            }
        }
    })
}



/* 判断是否包含post_device_id,如果有则是从设备管理页跳转过来的，重载数据 */
$(function(){
    if(typeof(post_device_id) != "undefined"){
        $('#device_id').val(post_device_id);
        $('#searchButton').click();
    }
})

$('.upper-btn-group.margin_ddos1.pull-right button').attr('resourceid','396');
$('#maintable tfoot .pull-left button').not(':last').attr('resourceid','396');

