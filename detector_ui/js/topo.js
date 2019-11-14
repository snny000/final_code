/* 设备管理拓扑图操作
 * 2017/10/13
 * brucefuqiming
 */
// 初始化层级拓扑数据
var DIR = "../images/ui/";
var EDGE_LENGTH_MAIN = 150; //主节点之间间距
var EDGE_LENGTH_SUB = 50; //叶子节点与父节点之间间距
var currentPage = "topological_graph"; //默认页面层级拓扑
var allnodes = [
        {id: 1,  shape: 'image', image: DIR + 'direct.png',label:"指挥中心",type:"director",pid:0,subids:[2,3,4,13]},
        {id: 2,  shape: 'image', image: DIR + 'direct_node.png',label:"上海", type:"director_node",pid:1,subids:[5,6]},
        {id: 3,  shape: 'image', image: DIR + 'direct_node.png',label:"北京", type:"director_node",pid:1,subids:[12]},
        {id: 4,  shape: 'image', image: DIR + 'direct_node.png',label:"广东", type:"director_node",pid:1},
        {id: 5,  shape: 'image', image: DIR + 'manage.png',label:"上海管理中心", type:"manage",pid:2,subids:[7,8,9]},
        {id: 6,  shape: 'image', image: DIR + 'manage.png',label:"上海浦东管理中心", type:"manage",pid:2,subids:[10,11]},
        {id: 7,  shape: 'image', image: DIR + 'detector.png',label:"上海检测器1", type:"detector",pid:5},
        {id: 8,  shape: 'image', image: DIR + 'detector.png',label:"上海检测器2", type:"detector",pid:5},
        {id: 9,  shape: 'image', image: DIR + 'detector.png',label:"上海检测器3", type:"detector",pid:5},
        {id: 10, shape: 'image', image: DIR + 'detector.png',label:"浦东检测器4", type:"detector",pid:6},
        {id: 11, shape: 'image', image: DIR + 'detector.png',label:"浦东检测器5", type:"detector",pid:6},
        {id: 12, shape: 'image', image: DIR + 'manage.png',label:"北京管理中心", type:"manage",pid:3},
        {id: 13, shape: 'image', image: DIR + 'manage.png',label:"广州管理中心", type:"manage",pid:1,subids:[14,15]},
        {id: 14, shape: 'image', image: DIR + 'detector.png',label:"广州检测器6", type:"detector",pid:13},
        {id: 15, shape: 'image', image: DIR + 'detector.png',label:"广州检测器7", type:"detector",pid:13}
      ],
      alledges=[
          {id:'1_2',from: 1, to: 2, length: EDGE_LENGTH_MAIN},
          {id:'1_3',from: 1, to: 3, length: EDGE_LENGTH_MAIN},
          {id:'1_4',from: 1, to: 4, length: EDGE_LENGTH_MAIN},
          {id:'1_13',from: 1, to: 13, length: EDGE_LENGTH_MAIN},
          {id:'2_5',from: 2, to: 5, length: EDGE_LENGTH_MAIN},
          {id:'2_6',from: 2, to: 6, length: EDGE_LENGTH_MAIN},
          {id:'3_12',from: 3, to: 12, length: EDGE_LENGTH_MAIN},
          {id:'5_7',from: 5, to: 7, length: EDGE_LENGTH_SUB},
          {id:'5_8',from: 5, to: 8, length: EDGE_LENGTH_SUB},
          {id:'5_9',from: 5, to: 9, length: EDGE_LENGTH_SUB},
          {id:'6_10',from: 6, to: 10, length: EDGE_LENGTH_SUB},
          {id:'6_11',from: 6, to: 11, length: EDGE_LENGTH_SUB},
          {id:'13_14',from: 13, to: 14, length: EDGE_LENGTH_SUB},
          {id:'13_15',from: 13, to: 15, length: EDGE_LENGTH_SUB},
      ];
var dataMap = {}; // 根据类型将数据分组用于创建各搜索框
var createDataMap = function (allnodes) {
    for (var i = 0, l = allnodes.length; i < l; i++) {
        var key = allnodes[i]['type'];
        dataMap[key] = dataMap[key] || (dataMap[key] = []);
        dataMap[key].push(allnodes[i]);
    }
    var director_node_option = "";
    if(dataMap[0]!=undefined){
        dataMap[0].map(function(v){
            director_node_option += `<option type=0 value=${v.id}>${v.label}</option>`;
        });
    }

    if(dataMap[1]!=undefined){
        dataMap[1].map(function(v){
            director_node_option += `<option type=1 value=${v.id}>${v.label}</option>`;
        });
    }

    if(dataMap[2]!=undefined){
        dataMap[2].map(function(v){
            director_node_option += `<option type=2 value=${v.id}>${v.label}</option>`;
        });
    }
    if(dataMap[3]!=undefined){
        dataMap[3].map(function(v){
            director_node_option += `<option type=3 value=${v.id}>${v.label}</option>`;
        });
    }
    $('#director_node').html(director_node_option);
    $('#director_node').selectpicker('refresh');
    if(dataMap.manage!=undefined){
        var manage_center_option = "";
        dataMap.manage.map(function(v){
            manage_center_option += `<option value=${v.id}>${v.label}</option>`;
        });
        $('#manage_center').html(manage_center_option);
        $('#manage_center').selectpicker('refresh');
    }
    if(dataMap.detector!=undefined){
        var detector_id_option = "";
        dataMap.detector.map(function(v){
            detector_id_option += `<option value=${v.id}>${v.label}</option>`;
        });
        $('#detector_id').html(detector_id_option);
        $('#detector_id').selectpicker('refresh');
    }
}

var initTopoData = function (url,postData) {
    url = "/ajax_action_detector.php?uu=command."+url;
    if (url == undefined)
        url = "/ajax_action_detector.php?uu=command.topological_graph"
    $.ajax({
        url: url,
        type: "post",
        data: postData,
        success: function (data) {
            //console.log(data)
            var res = JSON.parse(data);
            initTopoGraph(res);
            /*if(currentPage == "topological_graph")
                showHideAllDetector();*/
            //changeGraph('UD');
            //searchThenSelect();
        }
    })
}

var intersectArray = function(arr1, arr2) {
  if(Object.prototype.toString.call(arr1) === "[object Array]" && Object.prototype.toString.call(arr2) === "[object Array]") {
    return arr1.filter(function(v){ 
     return arr2.indexOf(v)!==-1 
    })
  }
}
// 搜索时选中节点
var searchThenSelect = function () {
    var currentId = [];
    for (var key in nodes._data) {
        currentId.push(key);
    }
    var vals = [];
    $.each($('.selectpicker'), function () {
        if ($(this).val() != "") {
            vals.push($(this).val())
        }
    })
    network.selectNodes(intersectArray(currentId,vals));
}


var topoData = {}; //拓扑数据
/*var graphOptions = { //默认布局
    interaction: { hover: true },
    nodes: {
        //borderWidth:4,
        size:50,
        color: {
            //border: '#406897',
            //background: '#6AAFFF'
        },
        font:{color:'#428bca',size:'30'},
        shapeProperties: {
            //useBorderWithImage:true
        }
    },
    edges: {
        color: 'lightgray'
    },
    layout: {
            hierarchical: {
                direction: 'UD',
                sortMethod: "directed"
            }
        },
    interaction: { dragNodes: false },
    physics: {
        enabled: false
    },
};*/


var graphOptions = {
        layout: {
            hierarchical: {
                direction: 'UD',
                sortMethod: "directed"
            }
        },
        nodes: {
        //borderWidth:4,
            size:40,
            color: {
                //border: '#406897',
                //background: '#6AAFFF'
            },
            font:{color:'#428bca',size:25},
            shapeProperties: {
                //useBorderWithImage:true
            }
        },
        interaction: { dragNodes: false },
        physics: {
            enabled: false
        }
    };
var nodes = null,edges = null;
// 创建拓扑图
var initTopoGraph = function (data) {
    allnodes = data["msg"]["allnodes"];
    alledges = data["msg"]["alledges"];
    if (allnodes.length > 500) { //节点数目大于500时设置位置，自动计算位置耗时很长
        //delete graphOptions['layout'];
        function getNumberInNormalDistribution(mean, std_dev) {
            return mean + (randomNormalDistribution() * std_dev);
        }
        function randomNormalDistribution() {
            var u = 0.0, v = 0.0, w = 0.0, c = 0.0;
            do {
                //获得两个（-1,1）的独立随机变量
                u = Math.random() * 2 - 1.0;
                v = Math.random() * 2 - 1.0;
                w = u * u + v * v;
            } while (w == 0.0 || w >= 1.0)
            //这里就是 Box-Muller转换
            c = Math.sqrt((-2 * Math.log(w)) / w);
            //返回2个标准正态分布的随机数，封装进一个数组返回
            //当然，因为这个函数运行较快，也可以扔掉一个
            //return [u*c,v*c];
            return u * c;
        }
        allnodes.map(function (v) {
            switch (v.type) {
                case "director":
                    v.image = DIR + 'direct.png';
                    break;
                case "director_node":
                    v.image = DIR + 'direct_node.png';
                    break;
                case 0:
                    v.image = DIR + 'direct.png';
                    v.x = 1000;
                    v.y = 0;
                    break;
                case 1:
                    v.image = DIR + 'province.png';
                    v.x = getNumberInNormalDistribution(allnodes.filter(function(i){return i.id==v.pid})[0]['x'], 1000);
                    v.y = 100;

                    break;
                case 2:
                    v.image = DIR + 'city.png';
                    v.x = getNumberInNormalDistribution(allnodes.filter(function(i){return i.id==v.pid})[0]['x'], 1000);
                    v.y = 200;
                    break;
                case 3:
                    v.image = DIR + 'county.png';
                    v.x = getNumberInNormalDistribution(allnodes.filter(function(i){return i.id==v.pid})[0]['x'], 1000);
                    v.y = 300;
                    break;
                case "manage":
                    v.image = DIR + 'manage.png';
                    v.x = getNumberInNormalDistribution(allnodes.filter(function(i){return i.id==v.pid})[0]['x'], 1000);
                    v.y = 400;
                    break;
                case "detector":
                    v.image = DIR + 'detector.png';
                    v.x = getNumberInNormalDistribution(allnodes.filter(function(i){return i.id==v.pid})[0]['x'], 1000);
                    v.y = 500;
                    break;
                default:
                    break;
            }
        })
    }
    else {
        allnodes.map(function (v) {
            switch (v.type) {
                case "director":
                    v.image = DIR + 'direct.png';
                    break;
                case "director_node":
                    v.image = DIR + 'direct_node.png';
                    break;
                case 0:
                    v.image = DIR + 'direct.png';
                    break;
                case 1:
                    v.image = DIR + 'province.png';
                    break;
                case 2:
                    v.image = DIR + 'city.png';
                    break;
                case 3:
                    v.image = DIR + 'county.png';
                    break;
                case "manage":
                    v.image = DIR + 'manage.png';
                    if(v.is_audit == 0){
                        /*v.shadow = {
                            enabled: true,
                            color:'#ff0000'
                        }
                        v.color = {
                            border: '#ff0000',
                            background: '#ff0000'
                        }
                        v.shapeProperties = {
                            borderDashes: true, 
                            interpolation: false,  
                        }*/
                        v.image = DIR + 'manage_audit.png';
                    }
                    break;
                case "detector":
                    v.image = DIR + 'detector.png';
                    break;
                default:
                    break;
            }

        })
    }
    
    alledges.map(function(v){
        if(v.length=="EDGE_LENGTH_MAIN")
            v.length = EDGE_LENGTH_MAIN
        else
            v.length = EDGE_LENGTH_SUB
    })
    
    
    var container = document.getElementById('chart-container');
    nodes = new vis.DataSet(allnodes); // 创建节点对象
    edges = new vis.DataSet(alledges); // 创建连线对象
    topoData = {
        nodes: nodes,
        edges: edges
    };
    
    network = new vis.Network(container, topoData, graphOptions);
    //绑定事件
    bindEvent(network);
    if(dataMap.manage == undefined)
        createDataMap(allnodes);
    if(allnodes.length<500){
        showHideAllDetector();
        changeGraph('UD');
    }else{
        network.moveTo({
            position: {x:1000, y:0},
            scale: 1,
            offset: {x:0, y:0}
        })
    }
}
var graphType = undefined;
// 改变布局
var changeGraph = function (type) {
    graphType = type;
    var container = document.getElementById('chart-container');
    var nodeSpacing = 120;
    var levelSeparation = 150;
    if(type=="UD"){
        nodeSpacing = 150;
    }else{
        levelSeparation = 200;
    }
    graphOptions = {
        layout: {
            hierarchical: {
                direction: type,
                sortMethod: "directed",
                nodeSpacing:nodeSpacing,
                levelSeparation:levelSeparation
            }
        },
        nodes: {
            borderWidth:4,
            borderWidthSelected:4,
            size:40,
            color: {
                border: 'rgba(0,255,255,0)',
                background: 'rgba(255,255,255,0)',
                highlight:{
                    border:'rgb(255,127,0)',
                    background: 'rgba(0,255,255,0)',
                }
            },
            font:{color:'#428bca',size:20},
            shapeProperties: {
                useBorderWithImage:true
            },
            shadow:{
                enabled: false,
                color: '#3dd4de',
                size: 30
            }
        },
        edges:{
            smooth: true,//曲线
            shadow:true,
            color: {
                color:'#428bca',
                highlight:'#428bca'

            },
            width: 2,
        },
        interaction: { dragNodes: false },
        physics: {
            enabled: false
        }
        
        /*configure: {
            filter: function (option, path) {
                if (path.indexOf('hierarchical') !== -1) {
                    return true;
                }
                return false;
            },
            showButton: false
        }*/
    };
    if (type == undefined) {
        graphOptions = {
            nodes: {
            borderWidth:4,
            borderWidthSelected:4,
            size:40,
            color: {
                border: 'rgba(0,255,255,0)',
                background: 'rgba(255,255,255,0)',
                highlight:{
                    border:'rgb(255,127,0)',
                    background: 'rgba(0,255,255,0)',
                }
            },
            font:{color:'#428bca',size:20},
            shapeProperties: {
                useBorderWithImage:true
            }
        },
        edges:{
            shadow:true,
            color: {
                color:'#428bca',
                highlight:'#428bca'

            },
            width: 2
        },
        physics: {
            enabled: true
        }
        };
    }
    network = new vis.Network(container, topoData, graphOptions);
    bindEvent(network)
}
// 绑定事件
var bindEvent = function (network) {
    /*network.on("doubleClick", function (params) {//双击事件
        if (params.nodes.length != 0) {//确定为节点双击事件
            var click_node_id = params.nodes[0];
            remove_all_sub_nodes(click_node_id);
        }
    });*/
    network.on("hoverNode",function(params){
        //console.log(params)
        /*var tooltip=document.getElementById('topo_tooltip');      //获取菜单对象
        tooltip.style.cssText='display:block;position:absolute;top:'+event.clientY+'px;'+'left:'+event.clientX+'px;'
        $(document).click(function(e){
            e = window.event || e; // 兼容IE7
            obj = $(e.srcElement || e.target);
            if (!$(obj).is("#topo_tooltip") ) {
                tooltip.style.display = "none";
            } 
        });*/
    })
    network.on("selectNode",function(params){
        var node = allnodes.filter(function(value){
            return value.id == params.nodes[0]
        })
        showNodeDetail(node[0],params.event);
        
    })
    network.on("click",function(){
        if(network.getSelectedNodes().length == 0){
            $('.device-detail').hide();
        }
    })
}

// 点击显示详情
var showNodeDetail = function(node,event){
    $('.device-detail').hide();
    if(node.type == "detector"){
        getDeviceDetail(node.id);
        $('#device-detail').show();

        $('#device-detail').css('right','unset');
        $('#device-detail').css("left", document.body.scrollLeft + event.center.x + 1);
        $('#device-detail').css("top", document.body.scrollLeft + event.center.y-$('#device-detail').height());
        //$('#device-detail').scrollTop(0);
        if(parseInt($('#device-detail').css('right'))<0){
            $('#device-detail').css('transform','translateX('+$('#device-detail').css('right')+')')
        }
        if(parseInt($('#device-detail').css('left'))<100){
            $('#device-detail').css('transform','translateX(0px)')
        }
    }else if(node.type=="0" || node.type=="1" || node.type=="2" || node.type=="3"){
        getDirectorDetail(node.id);
        $('#director-detail').show();

        $('#director-detail').css({'height':'auto','right':'unset'})
        $('#director-detail').css("left", document.body.scrollLeft + event.center.x + 1);
        $('#director-detail').css("top", document.body.scrollLeft + event.center.y-$('#director-detail').height());

        if(parseInt($('#director-detail').css('right'))<0){
            $('#director-detail').css('transform','translateX('+$('#director-detail').css('right')+')')
        }
        if(parseInt($('#director-detail').css('left'))<100){
            $('#director-detail').css('transform','translateX(0px)')
        }
    }else if(node.type=="manage"){
        getManageDetail(node.id);
        $('#manage-detail').show();

        $('#manage-detail').css({'height':'auto','right':'unset'})
        $('#manage-detail').css("left", document.body.scrollLeft + event.center.x + 1);
        $('#manage-detail').css("top", document.body.scrollLeft + event.center.y-$('#manage-detail').height());

        if(parseInt($('#manage-detail').css('right'))<0){
            $('#manage-detail').css('transform','translateX('+$('#manage-detail').css('right')+')')
        }
        if(parseInt($('#manage-detail').css('left'))<100){
            $('#manage-detail').css('transform','translateX(0px)')
        }
    }
        
        

    
}

// 关闭详情
$('.device-detail button.close').on('click',function(){
    $('.device-detail').hide();
    network.unselectAll();
})

//删除下级所有节点
function remove_all_sub_nodes(node_id) {
    var sub_nodes = get_directly_sub_nodes(node_id);
    if (sub_nodes.length == 0) {//当前点击的为叶子节点
        //判断是否有下级节点
        var currentNode = {};
        for (var i = 0; i < allnodes.length; i++) {
            if (allnodes[i].id == node_id) {
                currentNode = allnodes[i];
                break;
            }
        }
        if (typeof (currentNode['subids']) != 'undefined' && currentNode['subids'].length!=0) {
            $.each(currentNode['subids'], function (index, item) {
                allnodes.map(function(v){
                    if(v.id == item){
                        nodes.add(v);
                        edges.add({ id: node_id + '_' + item, from: node_id, to: item });
                    }
                })
            });
        } else if(typeof (currentNode['subids']) != 'undefined' && currentNode['subids'].length==0){
            //alert('无下级节点')
        } else if(typeof (currentNode['subids']) == 'undefined') {
            alert('当前为叶子节点');
        }
    } else {
        $.each(sub_nodes, function (index, item) {
            var sub_sub_nodes = get_directly_sub_nodes(item);
            if (sub_sub_nodes.length == 0) {
                nodes.remove({ id: item });
                edges.remove({ id: node_id + '_' + item });
            } else {
                remove_all_sub_nodes(item);
            }
            nodes.remove({ id: item });
            edges.remove({ id: node_id + '_' + item });
        });
    }
}


//获取某节点直属下级节点
function get_directly_sub_nodes(node_id) {
    var return_nodes = [];
    var connectedNodes = network.getConnectedNodes(node_id,'to');//获取所有连接子节点
    $.each(connectedNodes, function (index, item) {
        //if (item != allnodes[node_id - 1]['pid']) {//当前节点的父节点 ，不操作
            return_nodes.push(item);
        //}
    });
    return return_nodes;
}

// 隐藏显示全部检测器
var showHideAllDetector = function () {
    allnodes.map(function (v) {
        if (v.type == "manage") {
            //if(network.getConnectedNodes(v.id,'to').length!=0){
                remove_all_sub_nodes(v.id)
            //}
        }
    });
    if(graphType!=undefined)
        changeGraph(graphType);
}


// 切换层级拓扑和虚拟组拓扑
var switchTopo = function(type){
    currentPage = type;
    // 隐藏层级拓扑相关查询
    if(currentPage == "get_virtual_group"){
        // 虚拟组管理跳转
        window.location.replace('topo_virtual.php');
        /*initVirtualList();
        $('#director_node').selectpicker('val','');
        $('#manage_center').selectpicker('val','');
        $('#detector_id').selectpicker('val','');

        $('#director_node').parent().parent().hide();
        $('#manage_center').parent().parent().hide();
        $('#detector_id').parent().parent().hide();
        $('#virtual_group').parent().parent().show();*/
    }else{
        initTopoData(type,{0:0});
        $('#virtual_group').selectpicker('val','');

        $('#virtual_group').parent().parent().hide();
        $('#director_node').parent().parent().show();
        $('#manage_center').parent().parent().show();
        $('#detector_id').parent().parent().show();
    }
}
switchTopo("topological_graph");

// 搜索
$('#searchButton').on('click',function(){
    var postData = {};
    var direct_node = $('#director_node').val();
    var manage_center = $('#manage_center').val();
    var detector_id = $('#detector_id').val();
    var virtual_group = $('#virtual_group').val();
    if(direct_node!=""){
        var director_node = $(`#director_node option[value=${direct_node}]`).attr('type');
        postData[director_node] = direct_node;
    }else{
        postData[0] = 0;
    }
        
    if(manage_center!=""){
        delete postData[0];
        postData.manage = manage_center;
    }
    if(detector_id!=""){
        delete postData[0];
        postData.detector = detector_id;
    }
    if(currentPage=="get_virtual_group"){ //查询虚拟组
        if(virtual_group!=""){
            postData.virtual_group_id = virtual_group;
            initTopoData("get_virtual_group",postData);
        }else{
            initVirtualList();
        }
    }else{
        initTopoData("topological_graph",postData);
    }

    $('.topoStyle,.showHideDevice').removeClass('btn-primary');
    $('.topoStyle:eq(0)').addClass('btn-primary');
    $('.showHideDevice').text('显示检测器');
})
// 清除搜索条件
$('#clearButton').on('click',function(){
    $('#director_node').selectpicker('val','');
    $('#manage_center').selectpicker('val','');
    $('#detector_id').selectpicker('val','');
    $('#virtual_group').selectpicker('val','');
    //$('#searchButton').click();
})

// 虚拟组初始化
var initVirtualList = function(){
    $.ajax({
        url: '/ajax_action_detector.php?uu=command.get_virtual_group_info',
        success: function (data) {
            var res = JSON.parse(data);
            var virtualGroupData = res["msg"]["virtual_group"];
            createAllVirtualGroup(virtualGroupData);
        }
    })
}
// 初始化全部虚拟组
var createAllVirtualGroup = function (virtualGroupData) {
    $('#virtual_group').children('').remove();
    $('#virtual_group').append('<option value="">全部虚拟组</option>');
    $('#chart-container').children('').remove();
    virtualGroupData.map(function (v) {
        var virtual_group_option = `<option value=${v.virtual_group_id}>${v.virtual_group_name}</option>`;
        $('#virtual_group').append(virtual_group_option);
        $('#virtual_group').selectpicker('refresh');

        var virtual_group_div = `<div virtual_id=${v.virtual_group_id} class="virtual_group_cls" onclick="clickShowVirtualGroup(this)">${v.virtual_group_name}</div>`;
        $('#chart-container').append(virtual_group_div)
    })
}
// 点击查看虚拟组拓扑
var clickShowVirtualGroup = function(that){
    var virtual_group_id = $(that).attr('virtual_id');
    var postData = {"virtual_group_id":virtual_group_id};
    $('#virtual_group').selectpicker('val',virtual_group_id);
    $('#virtual_group').selectpicker('refresh');
    initTopoData("get_virtual_group",postData);
}

var ruleType = {
        1:['木马攻击检测策略','rule_trojan'],
        2:['漏洞利用检测策略','rule_attack'],
        3:['恶意程序检测策略','rule_pefile'],
        4:['未知攻击窃密检测上报策略','rule_abnormal'],
        5:['关键字检测策略','rule_keyword_file'],
        6:['加密文件筛选策略','rule_encryption_file'],
        7:['压缩文件检测策略','rule_compress_file'],
        8:['图片文件筛选策略','rule_picture_file'],
        9:['IP审计策略','rule_ip_listen'],
        10:['域名审计策略','rule_domain_listen'],
        11:['URL审计策略','rule_url_listen'],
        12:['账号审计检测策略','rule_account_listen'],
        13:['通联关系上报策略','rule_net_log'],
        14:['应用行为上报策略','rule_app_behavior'],
        15:['应用行为web过滤策略','rule_web_filter'],
        16:['应用行为DNS过滤策略','rule_dns_filter'],
        17:['IP白名单过滤策略','rule_ip_whitelist'],
        18:['通信阻断策略','rule_comm_block']
}

// 跳转策略页面
function postRule(that){
    var url = $(that).attr('url');
    var param = {
        device_id: $(that).attr('id')
    }
    post_blank(url,param);
}
// 显示检测器各项信息详情
function getDeviceDetail(deviceId) {
    $.ajax({
        url: "/ajax_action_detector.php?uu=command.get_detector_info&device_id=" + deviceId, //ajax请求
        type: "post",
        cache: false,
        success: function (data) {
            buildTbody(data);
        }
    });

    function buildTbody(data) {
        var server = JSON.parse(data);
        var msg = server.msg[0];
        var base_form =
            "<tr><td><span class='text-muted'> 设备编号:</span>" + msg.device_id + "</td>" +
            "<td><button class='pull-right btn btn-primary' onclick='postDetail(\"device\"," + deviceId + ")'>查看详情</button></td>" +
            "</tr>" +
            "<tr><td><span class='text-muted'> 所属管理中心:</span>" + msg.center_id + "</td></tr>" +
            "<tr><td><span class='text-muted'> 所属指挥节点:</span>" + msg.node_name + "</td></tr>" +
            "<tr><td><span class='text-muted'> 部署单位:</span>" + msg.organs + "</td></tr>" 
        $("tbody#base-form").html(base_form);

    }

    $.ajax({
        url: "/ajax_action_detector.php?uu=command.get_plugin_status_info&device_id=" + deviceId, //ajax请求
        type: "post",
        cache: false,
        success: function (data) {
            var res = JSON.parse(data);
            if (res.code == 200)
                buildBusinessTbody(res["msg"]);
        }
    });

    function buildBusinessTbody(msg) {
        var business_form =
            "<tr class='sub-title'><td><span class='text-muted'>策略统计</td></tr>" +
            "<tr><td><table id='ruleCount' class='table table-condensed'></table></td></tr>"
        //$("tbody#business-form").html(business_form);
        getAllAlarm();
        getRuleCount();
        getDirectorPlug();
        getSubscribe();
    }

    /*获取告警统计数*/
        function getAllAlarm(){
            /*$.ajax({
                url:'/ajax_action_detector.php?uu=V1.alarm.get_statistics_count&device_id='+deviceId,
                success:function(data){
                    var res = JSON.parse(data)["msg"];
                    var msg = res["business_type"];
                    var alarmCount = 0;
                    for(var key in msg){
                        alarmCount+=parseInt(msg[key]);
                    }
                    $('#alarm_count').html('<a onclick="postAlarm(\''+deviceId+'\')">'+alarmCount+'</a>');
                }
            })*/
            $.ajax({
                url:'/ajax_action_detector.php?uu=alarm.warning_type_histogram',
                data:{
                    device_id:deviceId,
                    query_condition:'business_type'
                },
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var alarmCount = 0;
                    for(var i=0;i<msg.length;i++){
                        alarmCount+=parseInt(msg[i]['amount']);
                    }
                    $('#alarm_count').html('<a onclick="postAlarm(\''+deviceId+'\')">'+alarmCount+'</a>');
                }
            })
        }

        /*获取所有策略*/
        function getRuleCount(){
            // 上行策略总数
            $.ajax({
                url:'/ajax_action_detector.php?uu=rule.get_rule_count&device_id='+deviceId,
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var count = 0;
                    for(var key in msg){
                        //$("#moduleTable td[ruletype="+key+"] a:eq(0)").html("上行"+msg[key]+"条");
                        count += parseInt(msg[key]);
                    }
                    $('#center_rule_count').text(count);
                }
            })
            $.ajax({
                url:'/ajax_action_detector.php?uu=rule.get_director_rule_count&device_id='+deviceId,
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var count = 0;
                    for(var key in msg){
                        //$("#moduleTable td[ruletype="+key+"] a:eq(1)").html("下行"+msg[key]+"条");
                        count += parseInt(msg[key]);
                    }
                    $('#director_rule_count').text(count);
                }
            })
        }

        /*获取指挥中心下发插件总数*/
        function getDirectorPlug(){
            $.ajax({
                url:'/ajax_action_detector.php?uu=plugin.show_plug_count&device_id='+deviceId,
                success:function(data){
                    var msg = JSON.parse(data);
                    $('#director_plug_count').html('<a onclick="postPlug(\''+deviceId+'\')">'+msg["msg"]["count"]+'</a>');
                }
            })
        }
        /*获取订阅情况*/
        function getSubscribe(){
            $.ajax({
                url:'/ajax_action_detector.php?uu=command.get_subscribe_num&device_id='+deviceId,
                success:function(data){
                    var msg = JSON.parse(data);
                    $('#subscribe_status').html("<a onclick=postSubscribe(\""+deviceId+"\")>共"+msg["msg"]["count"]+"条订阅</a>");
                }
            })
        }

}

function postSubscribe(deviceId,type){
    if(type==undefined)
        post_blank("data_subscribe.php",{device_id:deviceId});
    else
        post_blank("data_subscribe.php",{center_id:deviceId});
}

function postAlarm(deviceId){
    var param = {
        device_id: deviceId,
    }
    post_blank("alarm_list.php",param);
}
function postPlug(deviceId){
    post_blank("plug.php",{device_id:deviceId})
}
function postStat(type,centerId,alarmtype){
    var param = {
        center_id: centerId,
        warning_module: type==""?"-1":type,
    }
    post_blank("stat.php",param);
}

var directorType = {0:"国家",1:"省部","2":"城市","3":"县城"}
// 获取指挥节点详情
function getDirectorDetail(directorId){
    $.ajax({
        url:'/ajax_action_detector.php?uu=command.get_detector_node_info',
        data:{node_id:directorId},
        success:function(data){
            var msg = JSON.parse(data)["msg"];
            var base_form =
                "<tr><td><span class='text-muted'> 节点编号:</span>"+msg.node_id+"</td></tr>" +
                "<tr><td><span class='text-muted'> 节点名称:</span>"+msg.name+"</td></tr>" +
                "<tr><td><span class='text-muted'> 节点类型:</span>"+directorType[msg.type]+"</td></tr>" +
                "<tr><td><span class='text-muted'> 上级节点:</span>"+(msg.f_node_name==undefined?"--":msg.f_node_name)+"</td></tr>" +
                "<tr><td><span class='text-muted'> 创建时间:</span>"+msg.create_time.replace('T',' ')+"</td></tr>"
            $('#director-detail tbody').html(base_form);
        }
    })
}
// 获取管理中心详情
function getManageDetail(centerId){
    $.ajax({
        url:'/ajax_action_detector.php?uu=command.get_manage_info',
        data:{center_id:centerId},
        success:function(data){
            var msg = JSON.parse(data)["msg"][0];
            var audit = "";
            if(msg.is_audit == 0)
                audit = "<button class='btn btn-success' onclick='auditCenter(\""+centerId+"\",\""+msg.node_id+"\")'><i class='fa fa-files-o'>&nbsp;&nbsp;</i>审核&nbsp;&nbsp;</button>"
            var base_form = 
                "<tr><td><button class='btn btn-primary' onclick='postDetail(\"center\",\""+centerId+"\")'>查看详情</button></td>"+
                "<td>"+audit+"</td></tr>"+
                "<tr><td><span class='text-muted'> 编号:</span></td><td>"+msg.center_id+"</td></tr>" +
                "<tr><td><span class='text-muted'> 所属节点（编号）:</span></td><td>"+msg.node_name+"("+msg.node_id+")</td></tr>" +
                "<tr><td><span class='text-muted'> 从属单位:</span></td><td>"+msg.organs+"</td></tr>" 
            $('#manage-detail #collapseManageOne tbody').html(base_form);
        }
    })

    getAllAlarm();
    getRuleCount();
    getDirectorPlug();
    getSubscribe();

    /*获取告警统计数*/
        function getAllAlarm(){
            /*$.ajax({
                url:'/ajax_action_detector.php?uu=V1.alarm.get_statistics_count&center_id='+centerId,
                success:function(data){
                    var res = JSON.parse(data)["msg"];
                    var msg = res["business_type"];
                    var alarmCount = 0;
                    for(var key in msg){
                        alarmCount+=parseInt(msg[key]);
                    }
                    $('#alarm_count2').html('<a onclick="postStat(\'\',\''+centerId+'\')">'+alarmCount+'</a>');
                }
            })*/
            $.ajax({
                url:'/ajax_action_detector.php?uu=alarm.warning_type_histogram',
                data:{
                    center_id:centerId,
                    query_condition:'business_type'
                },
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var alarmCount = 0;
                    for(var i=0;i<msg.length;i++){
                        alarmCount+=parseInt(msg[i]['amount']);
                    }
                    $('#alarm_count2').html('<a onclick="postStat(\'\',\''+centerId+'\')">'+alarmCount+'</a>');
                }
            })
        }

        /*获取所有策略*/
        function getRuleCount(){
            // 上行策略总数
            $.ajax({
                url:'/ajax_action_detector.php?uu=rule.get_rule_count&center_id='+centerId,
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var count = 0;
                    for(var key in msg){
                        count += parseInt(msg[key]);
                    }
                    $('#center_rule_count2').text(count);
                }
            })
            $.ajax({
                url:'/ajax_action_detector.php?uu=rule.get_director_rule_count&center_id='+centerId,
                success:function(data){
                    var msg = JSON.parse(data)["msg"];
                    var count = 0;
                    for(var key in msg){
                        count += parseInt(msg[key]);
                    }
                    $('#director_rule_count2').text(count);
                }
            })
        }

        /*获取指挥中心下发插件总数*/
        function getDirectorPlug(){
            $.ajax({
                url:'/ajax_action_detector.php?uu=plugin.show_plug_count&center_id='+centerId,
                success:function(data){
                    var msg = JSON.parse(data);
                    $('#center_plug_count2').html(msg["msg"]["count"]);
                }
            })
        }
        /*获取订阅情况*/
        function getSubscribe(){
            $.ajax({
                url:'/ajax_action_detector.php?uu=command.get_subscribe_num&center_id='+centerId,
                success:function(data){
                    var msg = JSON.parse(data);
                    $('#subscribe_status2').html("<a onclick=postSubscribe(\""+centerId+"\",2)>共"+msg["msg"]["count"]+"条订阅</a>");
                }
            })
        }
}


// 跳转详情页面
function postDetail(type,id){
    id = "'"+id+"'";
    if(type == "center"){
        post_blank("topo_detail.php",{id:id});
    }else{
        post_blank("detector_detail.php",{id:id});
    }
}

// 审核管理中心
function auditCenter(center_id,node_id){
    $('#auditNodeId').val('');
    $('#is_audit').val('0');
    $('#audit_detail').val('');
    showStep(0);
    $('#auditCenterId').val(center_id);
    $('#auditNodeId').val(node_id);
    // 上传的管理中心的信息
    $.ajax({
            url:'/ajax_action_detector.php?uu=command.ShowCenterInfoDetail&center_id='+center_id,
            success:function(data){
                var msg = JSON.parse(data)['msg'];
                initAuditPart(msg,0);
            }
    })
    // 备案管理中心信息
    $.ajax({
            url:'/ajax_action_detector.php?uu=command.ShowCenterAuditDetail&center_id='+center_id,
            success:function(data){
                var ret = JSON.parse(data);
                if(ret.code!=200){
                    alert('管理中心备案信息不存在，不能审核！');
                    $('#auditModal').modal('hide');
                }
                var msg = JSON.parse(data)['msg'];
                initAuditPart(msg,1);
            }
    })

    $('#auditModal').modal('show');
}
function showStep(step){
    $('#auditModal .panel').hide();
    $('#auditModal .panel').eq(step).show();
}
function initAuditPart(msg,type){
    $('#basePanel table:eq('+type+') span[key=node_name]').html($('#director_node option[value='+msg['node_id']+']').text());
    for(var key in msg){
        $('#basePanel table:eq('+type+') span[key='+key+']').html(msg[key])
    }

    var interface = msg['interface'][0];
    for(var key in interface){
        if(interface['manage'] == true){
            $('#interfacePanel table:eq('+type+') span[key=manage]').html('是');
        }
        if(interface['manage'] == false){
            $('#interfacePanel table:eq('+type+') span[key=manage]').html('否');
        }
        $('#interfacePanel table:eq('+type+') span[key='+key+']').html(interface[key])
    }

    var cpu = msg['cpu_info'];
    var tr = "";
    for(var i=0;i<cpu.length;i++){
        tr += "<tr>"+
            "<td>"+ cpu[i]['physical_id']+ "</td>"+
            "<td>"+ cpu[i]['core']+ "</td>"+
            "<td>"+ cpu[i]['clock']+ "</td>"+
            "</tr>"
    }
    $('#cpuPanel table:eq('+type+') tbody').html(tr);

    var disk = msg['disk_info'];
    var tr = "";
    for(var i=0;i<disk.length;i++){
        tr += "<tr>"+
            "<td>"+ disk[i]['serial']+ "</td>"+
            "<td>"+ disk[i]['size']+ "</td>"+
            "</tr>"
    }
    $('#diskPanel table:eq('+type+') tbody').html(tr);

    var contact = msg['contact'];
    var tr = "";
    for(var i=0;i<contact.length;i++){
        tr += "<tr>"+
            "<td>"+ contact[i]['name']+ "</td>"+
            "<td>"+ contact[i]['position']+ "</td>"+
            "<td>"+ contact[i]['phone']+ "</td>"+
            "<td>"+ contact[i]['email']+ "</td>"+
            "</tr>"
    }
    $('#contactPanel table:eq('+type+') tbody').html(tr);
}
function submitAuditCenter(){
    var centerId = $('#auditCenterId').val();
    var nodeId = $('#auditNodeId').val();
    var isAudit = $('#is_audit').val();
    var auditDetail = $('#audit_detail').val();
    $.ajax({
        url:'/ajax_action_detector.php?uu=command.CenterAudit',
        data:{
            node_id: nodeId,
            center_id: centerId,
            is_audit: isAudit,
            audit_detail: auditDetail
        },
        success:function(data){
            console.log(data);
            var ret = JSON.parse(data);
            if(ret.code == 200){
                alert('审核成功!');
                $('#auditModal').modal('hide');
            }else{
                alert("审核失败:"+ret.msg);
            }
            $('#manage-detail').hide();
            $('#searchButton').click();
        },
        error:function(){
            alert('审核失败')
        }
    })
}

// 搜索项联动
$('#clearButton').on('click',function(){
    var director_node_option = "";
    if(dataMap[0]!=undefined){
        dataMap[0].map(function(v){
            director_node_option += `<option type=0 value=${v.id}>${v.label}</option>`;
        });
    }

    if(dataMap[1]!=undefined){
        dataMap[1].map(function(v){
            director_node_option += `<option type=1 value=${v.id}>${v.label}</option>`;
        });
    }

    if(dataMap[2]!=undefined){
        dataMap[2].map(function(v){
            director_node_option += `<option type=2 value=${v.id}>${v.label}</option>`;
        });
    }
    if(dataMap[3]!=undefined){
        dataMap[3].map(function(v){
            director_node_option += `<option type=3 value=${v.id}>${v.label}</option>`;
        });
    }
    $('#director_node').html(director_node_option);
    $('#director_node').selectpicker('refresh');
    if(dataMap.manage!=undefined){
        var manage_center_option = "";
        dataMap.manage.map(function(v){
            manage_center_option += `<option value=${v.id}>${v.label}</option>`;
        });
        $('#manage_center').html(manage_center_option);
        $('#manage_center').selectpicker('refresh');
    }
    if(dataMap.detector!=undefined){
        var detector_id_option = "";
        dataMap.detector.map(function(v){
            detector_id_option += `<option value=${v.id}>${v.label}</option>`;
        });
        $('#detector_id').html(detector_id_option);
        $('#detector_id').selectpicker('refresh');
    }
})

$('#director_node').on('change',function(){
    $('#manage_center').selectpicker('val','');
    $('#detector_id').selectpicker('val','');
    var currentId = $(this).val();
    var newmanage = dataMap['manage'].filter(function(v){
        return v.pid == currentId;
    });
    var manageOpt = "";
    for(var i=0;i<newmanage.length;i++){
        manageOpt+='<option value="'+newmanage[i].id+'">'+newmanage[i].label+'</option>';
    }
    $('#manage_center').html(manageOpt);
    $('#manage_center').selectpicker('refresh');

    var detectorOpt = "";
    for(var i=0;i<dataMap.detector.length;i++){
        for(var j=0;j<newmanage.length;j++){
            if(dataMap.detector[i].pid == newmanage[j].id){
                detectorOpt += '<option value="'+dataMap.detector[i].id+'">'+dataMap.detector[i].label+'</option>';
            }
        }
    }
    $('#detector_id').html(detectorOpt);
    $('#detector_id').selectpicker('refresh');
})

$('#manage_center').on('change',function(){
    $('#detector_id').selectpicker('val','');
    var currentId = $(this).val();
    var newdetector = dataMap['detector'].filter(function(v){
        return v.pid == currentId;
    });
    var detectorOpt = "";
    for(var i=0;i<newdetector.length;i++){
        detectorOpt+='<option value="'+newdetector[i].id+'">'+newdetector[i].label+'</option>';
    }

    $('#detector_id').html(detectorOpt);
    $('#detector_id').selectpicker('refresh');

    /*var pid = dataMap['manage'].filter(function(v){
        return v.id == currentId;
    })[0].pid;
    $('#director_node').selectpicker('val',pid);*/
})

/* 拓扑图操作提示 */
$('.topoStyle').on('click',function(){
    $('.topoStyle').removeClass('btn-primary');
    $(this).addClass('btn-primary');
})

$('.showHideDevice').on('click',function(){
    if($(this).text() == "显示检测器"){
        $(this).text('隐藏检测器');
        $(this).addClass('btn-primary');
    }else{
        $(this).text('显示检测器');
        $(this).removeClass('btn-primary');
    }
})