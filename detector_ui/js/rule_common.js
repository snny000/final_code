/**
 * Created by Fernando on 2016/7/7.
 */


$("#fullCenter").click(function(){
    $('#hintModal').find(".modal-title").html("上报管理中心策略集")
    var content =
        // "<span>上报插件个数:<span style='color: red;font-size: large'></span></span>"+
        "<p >上报策略个数:<span style='color: red;font-size: large'>"+$("#full span").text()+"</span></p>"+
        "<p >将会上报至指挥节点</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='fullSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#fullSubmit").click(function(){
        // console.log(document.referrer);
        policy_type = 0
        switch(window.location.pathname)
        {
            case "/rule_trojan.php":
                policy_type = 1
                break;
            case "/rule_attack.php":
                policy_type = 2
                break;
            case "/rule_pefile.php":
                policy_type = 3
                break;
            case "/rule_abnormal.php":
                policy_type = 4
                break;
            case "/rule_keyword_file.php":
                policy_type = 5
                break;
            case "/rule_encryption_file.php":
                policy_type = 6
                break;
            case "/rule_compress_file.php":
                policy_type = 7
                break;
            case "/rule_picture_file.php":
                policy_type = 8
                break;
            case "/rule_ip_listen.php":
                policy_type = 9
                break;
            case "/rule_domain_listen.php":
                policy_type = 10
                break;
            case "/rule_url_listen.php":
                policy_type = 11
                break;
            case "/rule_account_listen.php":
                policy_type = 12
                break;
            case "/rule_net_log.php":
                policy_type = 13
                break;
            case "/rule_app_behavior.php":
                policy_type = 14
                break;
            case "/rule_web_filter.php":
                policy_type = 15
                break;
            case "/rule_dns_filter.php":
                policy_type = 16
                break;
            case "/rule_ip_whitelist.php":
                policy_type = 17
                break;
            case "/rule_comm_block.php":
                policy_type = 18
                break;
        }    
        console.log(policy_type)
        var carray =new Array();
        pickCenterForward(carray,[],888,policy_type)
        $('#hintModal').modal('hide')
    })
    $('#hintModal').modal('show')
})


function pickCenterForward(id, device_id_list, type,policy_type) {
    var param = { cacheRef: "plug.php" } //当前页面
    var currentPage = $('#pagination .active a').text()
    param["policy_type"] = policy_type
    // param["cachePage"] = currentPage
    // param["cacheDevice_id_list"] = JSON.stringify(eval(device_id_list));
    // param["cacheCmd_type"] = type;
    // param["cacheSearchParam"] = JSON.stringify(globalSearchParam)
    // param["cacheMenu"] = "menu-plug1";
    // param["cacheType"] = 1;
    // param["cachePolicy_type"] = 0; // 当前插件类型
    // if (id instanceof Array) {
    //     param["cacheId"] = JSON.stringify(id);
    // } else {
    //     var carray = new Array()
    //     carray.push(parseInt(id))
    //     param["cacheId"] = JSON.stringify(carray)
    // }
    // post('plugin.fulldose_report', param);
    $.ajax({
        url: "/ajax_action_detector.php?uu=rule.fulldose_report",
        data:param,
        success: function (data) {
            var res = JSON.parse(data);
            // if (res.code == 200) {
            //     console.log("1212")
            // }
            alert(res["msg"]);
        }
    })
}


/**
 * 加载策略数据
 * @param currentPage  第几页
 * @param searchParam  请求参数
 * @param is_director  标识查询管理中心本地还是指挥下发策略， 1：指挥下发， 0：管理中心本地
 * @constructor
 */
function LoadPage(currentPage,searchParam,is_director){
    is_director = is_director || 0;
    $.ajax({
        url: "/ajax_action_detector.php?uu=rule.count&policy_type=" + global_policy_type + "&is_director=" + is_director,
        type: "post",
        data: searchParam,
        success:function(data) {
            var ret = JSON.parse(data);
            if (ret["code"] == 200)
                ret = ret["msg"]["count"]
            else {
                ret = 0;
            }
            $("#totalcount").text(ret);
            $('#pagination').empty();
            $('#pagination').removeData("twbs-pagination");
            $('#pagination').unbind("page");
            pagination(ret,"/ajax_action_detector.php?uu=rule.show&p_size="+p_size+"&policy_type=" + global_policy_type + "&is_director=" + is_director, parseInt(currentPage),searchParam)
        },
        beforeSend: function () {
            $(".loading-pic").removeClass("hidden");
        },
        error: function () {
            alert("无法连接服务器");
        }
    })

    /*
     <button id="full" type="button" class="btn btn-primary btn-interval">全量&nbsp;<span class="badge" style="background-color: orange">0</span></button>
     <button id="increment" type="button" class="btn btn-primary btn-interval">增量&nbsp;<span class="badge" style="background-color: orange">0</span></button>
     */
    if (is_director == 0) {
        $.ajax({ //全量
            url: "/ajax_action_detector.php?uu=rule.is_changed&policy_type=" + global_policy_type + "&type=1",
            success:function(data) {
                var ret = JSON.parse(data);

                if(ret.msg==0){
                    $("#full span").text("");
                    $("#full").prop('disabled',"true");
                }else{
                    $("#full span").text(ret.msg);
                    $("#full").removeAttr('disabled')
                }
            }
        })

        $.ajax({ //增量
            url: "/ajax_action_detector.php?uu=rule.is_changed&policy_type=" + global_policy_type + "&type=0",
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.msg==0){
                    $("#increment span").text("");
                    $("#increment").prop('disabled',"true");
                }else{
                    $("#increment span").text(ret.msg);
                    $("#increment").removeAttr('disabled')
                }
            }
        })
    }
}


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

/*$("#chk_all1,#chk_all2").click(function(){
    if(this.checked){
        $("table :checkbox").prop("checked", true);
    }else{
        $("table :checkbox").prop("checked", false);
    }
});*/

var cascadeNodeCenterDevice = {
    'node_id':[],
    'center_id':[],
    'device_id':[]
};


// 获取检测器构建下拉框
var initDeviceId = function(){
    $.ajax({
        url: "/ajax_action_detector.php?uu=detector.count",
        success: function (data) {
            var res = JSON.parse(data);
            if (res.code == "200") {
                var count = res["msg"]["count"];
                $.ajax({
                    url:"/ajax_action_detector.php?uu=detector.show&p_size="+count+"&pn=1",
                    success:function(data){
                        var res = JSON.parse(data);
                        if(res.code == "200"){
                            var deviceData = res["msg"];
                            var option = "";
                            deviceData.map(function(v,i){
                                option += `<option value=${v.device_id}>${v.organs}${v.device_id}</option>`;
                                var deviceObj = {'value':v.device_id,'name':v.organs+v.device_id};
                                cascadeNodeCenterDevice['device_id'].push(deviceObj);
                            })
                            $('#device_id').append(option);
                            $('#device_id').selectpicker('refresh');
                        }
                    }
                })
            }
        }
    })
}
initDeviceId();

$('#clearButton').on('click',function(){
    $('#device_id').selectpicker('val','');

    var deviceOpt = '<option value="">全部检测器</option>';
    cascadeNodeCenterDevice['device_id'].map(function(v){
        deviceOpt += '<option value='+v.value+'>'+v.name+'</option>';
    });
    $('#device_id').html(deviceOpt);
    $('#device_id').selectpicker('refresh');
})

// 批量更新任务组，含清空
$("#add_taskGroup").click(function(){
    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");
    if(checkboxs.size() == 0){
        alert("请选择添加的数据");
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
        alert('当前插件已删除，不能进行任务组操作!');
        return;
    }


    var carray1 =new Array()
    console.log(checkboxs)
    checkboxs.each(function(){
        var task_group_id = JSON.parse($(this).parent().parent().find('td').eq(-1).find('a').attr('data-bind')).group_id;
        console.log(task_group_id)
        carray1.push(task_group_id)
    })
    var unique_carray = unique(carray1);
    if(unique_carray.length>1){
        alert('变更数据原任务组不一致，请重新选择');
        return ;
    }
    // 判断是否已删除，已删除待同步的策略不能再变更生效范围和任务组，只能下发
    var carray =new Array()
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status == '（删除）待同步'){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length!=0){
        alert('当前操作包含已删除策略，不能变更任务组!');
        return;
    }
    var originTaskGroup = unique_carray.toString() == 0 ?"--":$(checkboxs[0]).parent().parent().find('td').eq(-1).find('a').html();
    $('.operateTooltip').html("<p>将修改<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据的任务组，请确认</p>原始任务组："+
    "<span style='color: red;font-size: large'>"+originTaskGroup+"</span>")

    $("#taskGroupSubmit").click(function(){
        var carray =new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            carray.push($(this).parent().parent().find("td:eq(1)").html())
        })
        console.log("carray:"+carray)
        var issuedParam = {};
        issuedParam["policy_type"] = policy_type;
        issuedParam["rule_id"] = JSON.stringify(carray); //用rule_id做的操作
        
        if($('#lunch').val()==""){
            var r = confirm("确认要清空当前策略的任务组吗？");
            issuedParam["group_id"] = "0";
            if(!r)
                return;
        }else if($('#lunch').val() == unique_carray.toString()){
            alert('当前选择任务组与原任务组相同，请重新选择');
            return;
        }else{
            issuedParam["group_id"] = $('#lunch').val();
        }
        
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.update_group",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret["code"] == 200){
                    refresh();
                }else{
                    alert("添加失败");
                }
                $('.selectpicker').val('');
                $('.selectpicker').selectpicker('refresh');
            }
        })
        $('#taskGroupModal').modal('hide')
        $("#taskGroupSubmit").unbind('click')
    })
    $('#taskGroupModal').modal('show')
})

// 批量复制到任务组，如果所选策略没有任务组，则只更新不复制
$("#copy_taskGroup").click(function(){
    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");
    if(checkboxs.size() == 0){
        alert("请选择复制的数据");
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
        alert('当前插件已删除，不能进行任务组操作!');
        return;
    }


    // 判断是否已删除，已删除待同步的策略不能再变更生效范围和任务组，只能下发
    var carray =new Array()
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status == '（删除）待同步'){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length!=0){
        alert('当前操作包含已删除策略，不能复制任务组!');
        return;
    }

    $('.operateTooltip').html('操作提示：该操作将复制当前选择的策略到新的任务组中<br/>如果所选策略无任务组，则更新该策略的任务组。')

    $("#taskGroupSubmit").click(function(){
        var carray =new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        var copyId = [],updateId = []; //复制的和更新的分别处理
        checkboxs.each(function(){
            //carray.push(parseInt($(this).attr("id")))
            if($(this).parent().parent().find('td').eq(-2).find('a').html() == ""){
                updateId.push($(this).parent().parent().find("td:eq(1)").html())
            }else
                copyId.push($(this).parent().parent().find("td:eq(1)").html())
        })
        var issuedParam = {};
        issuedParam["policy_type"] = policy_type;
        issuedParam["rule_id"] = JSON.stringify(copyId); //用rule_id做的操作
        
        if($('#lunch').val()==""){
            var r = confirm("确认要清空当前策略的任务组吗？");
            issuedParam["group_id"] = "0";
            if(!r)
                return;
        }else{
            issuedParam["group_id"] = $('#lunch').val();
        }
        if (copyId.length != 0) {
            $.ajax({
                url: "/ajax_action_detector.php?uu=rule.copy_rule_group",
                type: "post",
                data: issuedParam,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if(ret["code"] == 200){
                        refresh();
                    }else{
                        alert("添加失败");
                    }
                    $('.selectpicker').val('');
                    $('.selectpicker').selectpicker('refresh');
                }
            })
        }
        if (updateId.length != 0) {
            issuedParam["rule_id"] = JSON.stringify(updateId);
            $.ajax({
                url: "/ajax_action_detector.php?uu=rule.update_group",
                type: "post",
                data: issuedParam,
                success: function (data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200) {
                        refresh();
                    } else {
                        alert("添加失败");
                    }
                    $('.selectpicker').val('');
                    $('.selectpicker').selectpicker('refresh');
                }
            })
        }
        $('#taskGroupModal').modal('hide')
        $("#taskGroupSubmit").unbind('click')
    })
    $('#taskGroupModal').modal('show')
})
// 清空策略的任务组
$('#clear_taskGroup').click(function(){
    $('#hintModal').find(".modal-title").html("移除策略的任务组")
    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");
    if(checkboxs.size() == 0){
        alert("请选择数据");
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
        alert('当前插件已删除，不能进行任务组操作!');
        return;
    }


    // 判断是否已删除，已删除待同步的策略不能再变更生效范围和任务组，只能下发
    var carray =new Array()
    checkboxs.each(function(){
        var status = $('#maintable tbody tr[id='+$(this).attr("id")+'] td span').text();
        if(status == '（删除）待同步'){
            carray.push(parseInt($(this).attr("id")))
        }
    })
    if(carray.length!=0){
        alert('当前操作包含已删除策略，不能清空任务组!');
        return;
    }

    var content = "<p >将移除<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据的任务组，请确认</p>"
    $('#hintModal').find(".modal-body").html(content)

    var footer = "<button id='clearTaskGroupSubmit' type='button' class='btn btn-primary'>确定</button>"+
        "<button type='button' class='btn btn-default' data-dismiss='modal'>关闭</button>"
    $('#hintModal').find(".modal-footer").html(footer)

    $("#clearTaskGroupSubmit").click(function(){
        var carray =new Array()
        var lines = $("#maintable tbody tr");
        var checkboxs = lines.find("input:eq(0):checkbox:checked");
        checkboxs.each(function(){
            carray.push(parseInt($(this).parent().parent().find("td:eq(1)").html()))
        })
        var issuedParam = {};
        issuedParam["policy_type"] = policy_type;
        issuedParam["rule_id"] = JSON.stringify(carray); //用rule_id做的操作
        issuedParam["group_id"] = "0";
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.update_group",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret["code"] == 200){
                    refresh();
                }else{
                    alert("清空失败");
                }
            }
        })
        $('#hintModal').modal('hide')
        $("#clearTaskGroupSubmit").unbind('click')
    })
    $('#hintModal').modal('show')
})

// 关闭任务组窗口时解除点击事件绑定
$(function () {
    $('#taskGroupModal').on('hide.bs.modal', function () {
        $("#taskGroupSubmit").unbind('click');
        $('.operateTooltip').html('');
    })
});



// 判断是否是从任务组查看策略页面跳转的，屏蔽相关操作功能
if(typeof(addIntoGroup)!="undefined" && addIntoGroup.state!=undefined){
    $('.nav_margin').next().hide();
    $('.nav_margin').nextAll('.btn-banner').hide();
    $('.upper-btn-group.margin_ddos1.pull-right').hide();
    $('.row.btn-banner').hide();
    $('.nav_margin h4 label').hide();
    $('h4 .btn-group').hide();
    $(function(){
        $('#add_taskGroup').hide();
        $('#copy_taskGroup').hide();
        setTimeout(function(){
            LoadPage(1,{group_id:addIntoGroup.group_id});
        },500)
        // console.log(group_name)
        var name = `当前策略所属任务组：<span style="color: red;font-size: large;font-weight: bold;">${addIntoGroup.group_name}</span>`;
        $('.nav_margin .pull-left').append(name);
    }) 
}

// 根据策略类型初始化任务组下拉框数据
var ruleType = {
        1:['木马攻击检测策略','rule_trojan.php'],
        2:['漏洞利用检测策略','rule_attack.php'],
        3:['恶意程序检测策略','rule_pefile.php'],
        4:['未知攻击窃密检测上报策略','rule_abnormal.php'],
        5:['关键字检测策略','rule_keyword_file.php'],
        6:['加密文件筛选策略','rule_encryption_file.php'],
        7:['压缩文件检测策略','rule_compress_file.php'],
        8:['图片文件筛选策略','rule_picture_file.php'],
        9:['IP审计策略','rule_ip_listen.php'],
        10:['域名审计策略','rule_domain_listen.php'],
        11:['URL审计策略','rule_url_listen.php'],
        12:['账号审计检测策略','rule_account_listen.php'],
        13:['通联关系上报策略','rule_net_log.php'],
        14:['应用行为上报策略','rule_app_behavior.php'],
        15:['应用行为web过滤策略','rule_web_filter.php'],
        16:['应用行为DNS过滤策略','rule_dns_filter.php'],
        17:['IP白名单过滤策略','rule_ip_whitelist.php'],
        18:['通信阻断策略','rule_comm_block.php']
}
var currentPagePath = document.location.pathname.substring(1);
$('h4 .btn-group').on('click','button',function(){
    window.location.replace($(this).attr('href'));
})
$(function(){
    $('h4 .btn-group').addClass('btn-group-sm');
    var switchSub = "";
    if(currentPagePath.indexOf('director') == -1){
        switchSub =
            '<button type="button" href='+currentPagePath+' class="btn btn-default">管理中心本地</button>'+
            '<button type="button" href='+currentPagePath.split('.')[0]+'_director.php class="btn btn-default">指挥节点下发</button>'
    }else{
        switchSub =
            '<button type="button" href='+currentPagePath.substring(0,currentPagePath.indexOf('_director'))+'.php class="btn btn-default" >管理中心本地</button>'+
            '<button type="button" href='+currentPagePath+' class="btn btn-default">指挥节点下发</button>'
        $('.upper-btn-group.margin_ddos1.pull-right').hide();
        $('#maintable tfoot .pull-left button').not(':last').hide();
    }

    $('h4 .btn-group').html(switchSub);
    // 管理中心本地
    if(currentPagePath.indexOf('director') == -1){
        $('h4 .btn-group button:eq(0)').addClass('btn-primary');
    }else{  // 指挥节点下发
        $('h4 .btn-group button:eq(1)').addClass('btn-primary');
    }
})

var policy_type = 0;
for(let i in ruleType){
    if(ruleType[i][1]==currentPagePath){
        policy_type = i;
        $.ajax({
            url: 'ajax_action_detector.php?uu=task_group.show&p_size=10000&pn=1&rule_type='+i,
            success: function (res) {
                var taskgroup = JSON.parse(res).msg;
                console.log(taskgroup)
                taskgroup.map(function(v,i){
                    var option =  `<option value=${v.group_id}>${v.name}</option>`;
                    $('.selectpicker.task_group_select').append(option);
                    $('.selectpicker.task_group_select').selectpicker('refresh');
                })
            }
        })
        break;
    }
}





// 策略中查看任务组描述
var currentTaskGroup = {};
function showTaskGroup(that){
    $('#showTaskGroupModal').modal('show');
    var msgListObj = JSON.parse($(that).attr('data-bind'));
    $("#show_task_group_id").val(msgListObj.group_id);
    $("#show_task_group_name").val(msgListObj.name);
    $("#show_task_group_type").val(ruleType[parseInt(msgListObj.rule_type)][0]);
    $.ajax({
        url: '/ajax_action_detector.php?uu=task_group.show&p_size=10&pn=1',
        data: {group_id:msgListObj.group_id},
        success:function(data){
            var res = JSON.parse(data)["msg"][0];
            $('#show_task_group_create').val(res.create_person);
            $('#show_task_group_create_time').val(res.create_time.replace('T',' '));
            $('#show_task_group_remark').val(res.remarks);
        }
    })
}


// 状态格式化
    function ruleStatusFormat(msgListObj){
        var statusMap = {0:'已同步',1:'待同步'};
        var operateMap = {0:'新增',1:'删除',2:'变更生效范围',3:'变更任务组',4:''};
        var cmdStr = [];
        var plugCmd = JSON.parse(msgListObj.operate);
        console.log(plugCmd)
        if(msgListObj.rule_status == 1){
            for(var i=0,l=plugCmd.length;i<l;i++){
                cmdStr.push(operateMap[plugCmd[i]])
            }
            cmdStr = cmdStr.join("+");
            return `<span style="color:orange">(${cmdStr})${statusMap[msgListObj.rule_status]}</span>`;
        }
        return `${statusMap[msgListObj.rule_status]}`
    }

function getTaskGroupRules(){
    //post_blank(currentTaskGroup["url"],currentTaskGroup); //打开单独的页面查看，没必要
    $('#showTaskGroupModal').modal('hide');
    $('#task_group_id').selectpicker('val',$('#show_task_group_id').val()); //下拉框选中，触发查询
    $('#searchButton').click();
}

function oneSelect(id){
    if(globalSearchParam[id]!=undefined) {
        var key=globalSearchParam[id]
        var module = $("#risk_min").parent().parent();
        var select_obj = module.find("li[value="+key+"]");
        selectProtoFwd(select_obj);
    }
}

function oneSelect(id){
    if(globalSearchParam[id]!=undefined) {
        var key=globalSearchParam[id]
        var module = $("#risk_min").parent().parent();
        var select_obj = module.find("li[value="+key+"]");
        selectProtoFwd(select_obj);
    }
}

function oneInput(id){
    if(globalSearchParam[id]!=undefined) {
        var key=globalSearchParam[id]
        $("#"+id).val(key);
    }
}

$(function() {
    $('#hintModal').on('hide.bs.modal',
        function() {
            //alert('1111111111')
            $('#new_label_div').hide()
            //$('#hintModal').modal('hide')
        })
});

$("#rewrite_label").click(function(){

    // $('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("修改提示框")

    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");

    if(checkboxs.size() == 0){
        alert("请选择修改数据");
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

        $("#new_label").next("div").html("当前生效范围不一致，请谨慎操作")
        //alert("变更数据原范围不一致，请重新选择");
        // return;

    }else{
        $("#new_label").next("div").html("")
    }




    var content = "<p >将修改<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，请确认，此操作为批量修改策略标签</p>"
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

        issuedParam["policy_type"] = global_policy_type;

        //var ids =new Array()
        //ids.push(parseInt(cacheId))
        issuedParam["id"] = JSON.stringify(carray);
        //issuedParam["detector_id_list"] = "[]"



        var ischeck = true
        var new_label = $("#new_label").val()
        if(new_label == ""){
            $("#new_label").next("div").html("新标签不能为空")
            ischeck = false
        }else{
            $("#new_label").next("div").html("")
        }
        if(!ischeck){
            return;
        }





        issuedParam["new_label"] = new_label

        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.rewrite_label",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret["code"] == 200){
                    alert("策略标签修改成功");
                    //$("#issuedButton").prop('disabled',"true");
                    refresh()
                }else{
                    alert("策略标签修改失败");
                }

            }
        })

        $('#new_label_div').hide()
        $('#hintModal').modal('hide')
    })



    $('#new_label_div').show()
    $('#hintModal').modal('show')
})



$("#clean").click(function(){
    //$('#new_label_div').hide()

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
    // var carray1 =new Array()
    // checkboxs.each(function(){
    //     carray1.push($(this).attr("value"))
    //})

    //var unique_carray= unique(carray1)

    // if(unique_carray.length>1){

    //     alert("还原数据原范围不一致，请重新选择");
    //    return;

    //}


    var content = "<p >将清空<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，请确认，此操作为批量将选择的策略设置为无检测器生效</p>"
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

        issuedParam["policy_type"] = global_policy_type;

        //var ids =new Array()
        //ids.push(parseInt(cacheId))
        issuedParam["id"] = JSON.stringify(carray);
        issuedParam["detector_id_list"] = "[0]"
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.range",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret["code"] == 200){
                    alert("检查器生效范围还原成功");
                    //$("#issuedButton").prop('disabled',"true");
                    refresh()
                }else{
                    alert("检查器生效范围还原失败");
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


    var content = "<p >将还原<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，请确认，此操作为批量将选择的策略设置为全部检测器生效</p>"
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

        issuedParam["policy_type"] = global_policy_type;

        //var ids =new Array()
        //ids.push(parseInt(cacheId))
        issuedParam["id"] = JSON.stringify(carray);
        issuedParam["detector_id_list"] = "[]"
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.range",
            type: "post",
            data: issuedParam,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret["code"] == 200){
                    alert("检查器生效范围还原成功");
                    //$("#issuedButton").prop('disabled',"true");
                    refresh()
                }else{
                    alert("检查器生效范围还原失败");
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


    var content = "<p >将变更<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，请确认，此操作为批量对选择的策略设置追加一定数量的生效检测器</p>"
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


    var content = "<p >将变更<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，此操作为批量对选择的策略设置检测器生效范围</p>"
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

$("#delete").click(function(){
    //$('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("删除提示框")

    var lines = $("#maintable tbody tr");
    var checkboxs = lines.find("input:eq(0):checkbox:checked");

    if(checkboxs.size() == 0){
        alert("请选择删除数据");
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
        alert('当前插件已删除，重复删除!');
        return;
    }


    var content = "<p >将删除<span style='color: red;font-size: large'>"+checkboxs.size()+"</span>条数据，请确认</p>"
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
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.del&policy_type="+global_policy_type,
            type: "post",
            data: {id:JSON.stringify(carray)},
            success:function(data) {
                //  var ret = JSON.parse(data);
                console.log(data)
                refresh()
            }
        })

        $('#hintModal').modal('hide')
    })

    $('#hintModal').modal('show')
})





$("#full").click(function(){
    //  $('#new_label_div').hide()

    $('#hintModal').find(".modal-title").html("全量下发提示框")

    var content =
        "<span>下发方式:<span style='color: red;font-size: large'>全量下发</span></span>"+
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


/*    $("#fullSubmit").click(function(){
        $.ajax({
            url: "/ajax_action_detector.php?uu=rule.sync&policy_type="+global_policy_type+"&type=1",
            type: "post",
            data:null,
            success:function(data) {
                var ret = JSON.parse(data);
                if(ret.code == 200){
                    alert("全量下发成功");
                }else{
                    alert("全量下发失败");
                }
                refresh()
            }
        })
        //  $(this).prop('disabled',"true");

        $('#hintModal').modal('hide')
    })*/

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
            url: "/ajax_action_detector.php?uu=rule.sync&policy_type="+global_policy_type+"&type=0",
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
        operateviewhtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + id + ","+device_id_list+",3)\">生效检测器数量"+eval(device_id_list).length+"（查看）</a>"

    }else{
        operateviewhtml="生效范围解析错误"
    }
     return operateviewhtml
}

function generateoperatehtml(id,device_id_list){

    var num =eval(device_id_list).length
    var operatehtml=""
    if(device_id_list=='[0]' ||device_id_list=='[]'){
        operatehtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + id + ","+"[]"+",1)\">变更生效范围</a>"
    }else if(num>0){
        operatehtml = "<a href=\"javascript:void(0);\" onclick=\"pickDetectorForward(" + id + ","+device_id_list+",1)\">变更生效范围</a>"
    }else{
        operatehtml="生效范围解析错误"
    }

    return operatehtml

}


function export_file() {
    //  window.location.href = "detector_detail.php?id=" + id;
    var file_path = "/rule/template";
    var file_name = "策略导入模板下载.rar";

    //window.open("/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+"");

    window.location.href ="/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+"";
    //post('detector_detail.php',{id:id});
}


$("#imp-submit").click(function(){

    var param =  $("#param").attr("value")

    var issuedParam = {random:1}

    if(param!=undefined && param!=""){
        issuedParam["param"] = param
    }else{
        alert("请选择上传文件并点上传按钮")
        return;

    }

    issuedParam["policy_type"] = global_policy_type




    $.ajax({
        url: "/ajax_action_detector.php?uu=rule.import",
        type: "post",
        data: issuedParam,
        success:function(data) {
            var ret = JSON.parse(data);
            if(ret.code == 200){
                alert("导入成功");
                //$("#issuedButton").prop('disabled',"true");
                refresh()
            }else{
                alert(ret['msg']);
            }
        },
        error: function () {
            alert("无法连接服务器");
        }
    })



    $("#impModal").modal('hide');
})


upload("rule.fileupload", "#upJQuery","#upfile", "#param", "");

/* 判断是否包含post_device_id,如果有则是从设备管理页跳转过来的，重载数据 */
$(function(){
    if(typeof(post_device_id) != "undefined"){
        setTimeout(function(){
            $('#device_id').val(post_device_id);
            $('#searchButton').click();
        },1000)
    }
})



/* 定义策略复用按钮的权限id，与数据库定义的id保持一致 */
var policy_buttonid = {
    1: 360, //编辑木马攻击检测策略
    2: 362, //编辑漏洞利用检测策略
    3: 364, //编辑恶意程序检测策略
    4: 366, //编辑未知攻击检测策略
    5: 368, //编辑关键字检测策略
    6: 370, //编辑加密文件检测策略
    7: 372, //编辑多层压缩检测策略
    8: 374, //编辑图片筛选策略
    9: 376, //编辑IP审计检测策略
    10: 378, //编辑域名审计检测策略
    11: 380, //编辑URL审计检测策略
    12: 382, //编辑账号审计检测策略
    13: 384, //编辑通联关系上报策略
    14: 386, //编辑应用行为上报策略
    15: 388, //编辑应用行为WEB过滤策略
    16: 390, //编辑应用行为DNS过滤策略
    17: 392, //编辑IP白名单策略
    18: 394 //编辑通信阻断策略
}
$('.upper-btn-group.margin_ddos1.pull-right button').attr('resourceid',policy_buttonid[policy_type]);
$('#maintable tfoot .pull-left button').not(':last').attr('resourceid',policy_buttonid[policy_type]);

var policy_pageid = {
    1: 359, //木马攻击检测策略
    2: 361, //漏洞利用检测策略
    3: 363, //恶意程序检测策略
    4: 365, //未知攻击检测策略
    5: 367, //关键字检测策略
    6: 369, //加密文件检测策略
    7: 371, //多层压缩检测策略
    8: 373, //图片筛选策略
    9: 375, //IP审计检测策略
    10: 377, //域名审计检测策略
    11: 379, //URL审计检测策略
    12: 381, //账号审计检测策略
    13: 383, //通联关系上报策略
    14: 385, //应用行为上报策略
    15: 387, //应用行为WEB过滤策略
    16: 389, //应用行为DNS过滤策略
    17: 391, //IP白名单策略
    18: 393 //通信阻断策略
}
// 判断是否有当前策略页权限
var permission = JSON.parse(localStorage.roleResourceIds);
if(permission.indexOf(policy_pageid[policy_type])==-1 && currentPagePath.indexOf('_director')==-1){
    alert('没有权限!');
    window.location.href = 'login.php';
}