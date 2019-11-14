//自定义时间隐藏显示
function otherTime(){
	$('.otherTime').toggle();
    $('.time_switch').toggleClass('fa-chevron-down');
}
function switchRuleTask(){
    $('.ruleTask').toggle();
    $('.rule_switch').toggleClass('fa-chevron-down');
}
function switchDevice(){
    $('.device').toggle();
    $('.device_switch').toggleClass('fa-chevron-down');
}
function switchAlarmType(){
    $('.alarmType').toggle();
    $('.type_switch').toggleClass('fa-chevron-down');
}

// 告警级别统计
var initRiskCount = function(){
    var yData = ['无风险', '一般级', '关注级', '严重级', '紧急级'];
    var xData = [0,0,0,0,0];
    var option = {
    title: {
        text: '告警级别'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: null // 默认为直线，可选为：'line' | 'shadow'
        },
        formatter: '<div style="text-align: center;">告警级别</div>{b} : {c}'
    },
    grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
    xAxis: [{
        type: 'value',
        axisLabel: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLine: {
            show: false
        },
        splitLine: {
            show: false
        }

    }],
    yAxis: [{
        type: 'category',
        boundaryGap: true,
        axisTick: {
            show: true
        },
        axisLabel: {
            interval: null
        },
        data: yData,
        splitLine: {
            show: false
        }
    }],
    series: [{
        name: '',
        type: 'bar',
        barWidth: 25,
        label: {
            normal: {
                show: true,
                position: 'right'
            }

        },
        data: xData
    }]
}; 

riskChart = echarts.init($('#riskCount')[0]);
riskChart.setOption(option);
window.addEventListener('resize',function(){
    riskChart.resize();
})
}

// 分类统计，包括大类和小类
var initTypeCount = function(){
    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{b} :{d}%",
            textStyle: {
                fontSize: 14
            }
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['违规泄密', '攻击窃密', '异常行为', '目标帧听', '通信阻断']
            // ['攻击窃密', '异常行为', '违规泄密', '目标帧听', '通信阻断'] //异常行为就是未知攻击，乱七八糟的分类
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: { readOnly: false },
                restore: {},
                saveAsImage: {}
            }
        },
        grid: [
            { x: '7.5%', y: '62%', width: '88%', height: '30%' },
        ],
        xAxis: [
            {
                gridIndex: 0,
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
                data: ['违规泄密', '攻击窃密', '异常行为', '目标帧听', '通信阻断']
            },
        ],
        yAxis: [
            {
                gridIndex: 0, name: '数量', show: false
            },
        ],
        series: [
            {
                name: '告警大类',
                type: 'pie',
                //roseType:'radius',
                radius: '48%',
                center: ['50%', '33%'],
                data: [
                    { value: 0, name: '违规泄密' },
                    { value: 0, name: '攻击窃密' },
                    { value: 0, name: '异常行为' },
                    { value: 0, name: '目标帧听' },
                    { value: 0, name: '通信阻断' }
                ],
                label: {
                    normal: {
                        position: 'outside',
                        formatter: '{b} {c}',
                        textStyle: {
                            color: '',
                            fontSize: 14
                        }
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            },
            {
                name: '违规泄密',
                type: 'pie',
                //roseType:'radius',
                radius: '23%',
                center: ['16%', '80.2%'],
                data: [
                    { value: 0, name: 'Email泄密' },
                    { value: 0, name: 'Im涉密' },
                    { value: 0, name: 'FTP涉密' },
                    { value: 0, name: 'HTTP涉密' },
                    { value: 0, name: 'Netdisk涉密' },
                    { value: 0, name: '其他涉密' }
                ],
                label: {
                    normal: {
                        position: 'inner',
                        formatter: '{c}',
                        textStyle: {
                            color: '#ffffff',
                            fontSize: 14
                        }
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            },
            {
                name: '攻击窃密',
                type: 'pie',
                //roseType:'radius',
                radius: '23%',
                center: ['34%', '80.2%'],
                data: [
                    { value: 0, name: '木马攻击' },
                    { value: 0, name: '漏洞利用' },
                    { value: 0, name: '恶意程序' },
                    { value: 0, name: '其他攻击' }
                ],
                label: {
                    normal: {
                        position: 'inner',
                        formatter: '{c}',
                        textStyle: {
                            color: '#ffffff',
                            fontSize: 14
                        }
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            },
            {
                name: '异常行为',
                type: 'pie',
                //roseType:'radius',
                radius: '23%',
                center: ['51%', '80.2%'],
                data: [
                    { value: 1, name: '异常行为' },
                ],
                label: {
                    normal: {
                        position: 'inner',
                        formatter: '{c}',
                        textStyle: {
                            color: '#ffffff',
                            fontSize: 14
                        }
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            },
			
            {
                name: '目标审计',
                type: 'pie',
                radius: '23%',
                center: ['69%', '80.2%'],
                data: [
                    { value: 0, name: 'IP审计' },
                    { value: 0, name: '域名审计' },
                    { value: 0, name: 'URL审计' },
                    { value: 0, name: '帐号审计' },
                ],
                label: {
                    normal: {
                        position: 'inner',
                        formatter: '{c}',
                        offset: [, 100],
                        textStyle: {
                            color: '#ffffff',
                            fontSize: 14
                        }
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            },
            {
                name: '通信阻断',
                type: 'pie',
                //roseType:'radius',
                radius: '23%',
                center: ['87%', '80.2%'],
                data: [
                    { value: 0, name: '通信阻断' }
                ],
                label: {
                    normal: {
                        position: 'inner',
                        formatter: '{c}',
                        textStyle: {
                            color: '#ffffff',
                            fontSize: 14
                        }
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    typeChart = echarts.init($('#typeCount')[0]);
    typeChart.setOption(option);
    window.addEventListener('resize',function(){
        typeChart.resize();
    })
}

// 地区统计
// var initNodeNum = function(){
//     var option = {
//         title : {
//             textStyle: {
//             },
//             text: '地区告警数',
//         },
//         color: ['#3058DB'],
//         tooltip: {
//             trigger: 'axis',
//             axisPointer: {
//                 type: 'shadow'
//             }
//         },


//         toolbox: {
//             show: true,
//             feature: {
//                 dataView: {
//                     show: true,
//                     readOnly: true
//                 },
//                 magicType: {
//                     show: true,
//                     type: ['line', 'bar']
//                 },
//                 restore: {
//                     show: true
//                 },
//                 saveAsImage: {
//                     show: true
//                 }
//             }
//         },
//         calculable: false,
//         xAxis: [{
//             type: 'category',
//             axisLabel: {
//                 interval: 0,
//                 rotate: 15
//             },
//             data: ['济南', '山东', '北京', '朝阳']
//         }],
//         yAxis: [{
//             type: 'value'
//         }],
//         series: [{
//                 name: '告警数',
//                 type: 'bar',
//                 data: [0, 0, 0, 0],
//                 markPoint: {
//                     data: [{
//                         type: 'max',
//                         name: '最大值'
//                     }, {
//                         type: 'min',
//                         name: '最小值'
//                     }]
//                 },
//                 /*markLine: {
//                     data: [{
//                         type: 'average',
//                         name: '平均值'
//                     }]
//                 }*/
//             }
//         ]
//     };
//     nodeNumChart = echarts.init($('#nodeNum')[0]);
//     nodeNumChart.setOption(option);
//     window.addEventListener('resize',function(){
//         nodeNumChart.resize();
//     })
// }

// // 管理中心统计
// var initCenterNum = function(){
//     var option = {
//         title : {
//             textStyle: {
//             },
//             text: '中心告警数',
//         },
//         color: ['#3398DB'],
//         tooltip: {
//             trigger: 'axis',
//             axisPointer: {
//                 type: 'shadow'
//             }
//         },


//         toolbox: {
//             show: true,
//             feature: {
//                 dataView: {
//                     show: true,
//                     readOnly: true
//                 },
//                 magicType: {
//                     show: true,
//                     type: ['line', 'bar']
//                 },
//                 restore: {
//                     show: true
//                 },
//                 saveAsImage: {
//                     show: true
//                 }
//             }
//         },
//         calculable: false,
//         xAxis: [{
//             type: 'category',
//             axisLabel: {
//                 interval: 0,
//                 rotate: 15
//             },
//             data: ['D001', '170901020001', '170901020002', '170901020003']
//         }],
//         yAxis: [{
//             type: 'value'
//         }],
//         series: [{
//                 name: '告警数',
//                 type: 'bar',
//                 data: [0, 0, 0, 0],
//                 markPoint: {
//                     data: [{
//                         type: 'max',
//                         name: '最大值'
//                     }, {
//                         type: 'min',
//                         name: '最小值'
//                     }]
//                 },
//                 /*markLine: {
//                     data: [{
//                         type: 'average',
//                         name: '平均值'
//                     }]
//                 }*/
//             }
//         ]
//     };
//     centerNumChart = echarts.init($('#centerNum')[0]);
//     centerNumChart.setOption(option);
//     window.addEventListener('resize',function(){
//         centerNumChart.resize();
//     })
// }

// 检测器统计
var initDeviceNum = function(){
    var option = {
        title : {
            textStyle: {
            },
            text: '检测器告警数',
        },
        color: ['#ffd285'],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },

        grid:{
            x: 60,
            y: 30,
            x2: 30,
            y2: 30
        },
        toolbox: {
            show: false,
            feature: {
                dataView: {
                    show: true,
                    readOnly: true
                },
                magicType: {
                    show: true,
                    type: ['line', 'bar']
                },
                restore: {
                    show: true
                },
                saveAsImage: {
                    show: true
                }
            }
        },
        calculable: false,
        xAxis: [{
            type: 'category',
            axisLabel: {
                interval: 0,
                rotate: 10
            },
            data: ['170301020001', '170301020006', '170307020001', '170307020002', '171007010007']
        }],
        yAxis: [{
            type: 'value'
        }],
        series: [{
                name: '告警数',
                type: 'bar',
                data: [0, 0, 0, 0, 0],
                markPoint: {
                    data: [{
                        type: 'max',
                        name: '最大值'
                    }, {
                        type: 'min',
                        name: '最小值'
                    }]
                },
                /*markLine: {
                    data: [{
                        type: 'average',
                        name: '平均值'
                    }]
                }*/
            }
        ]
    };
    deviceNumChart = echarts.init($('#deviceNum')[0]);
    deviceNumChart.setOption(option);
    window.addEventListener('resize',function(){
        deviceNumChart.resize();
    })
}

// 产生告警的策略、任务组数
var initRuleTaskCount = function () {
    var option = {
        color: ['#ffd285', '#ff733f', '#ec4863'],
        title: [{
            text: '策略/任务组分类告警数',
            left: '1%',
            top: '6%',
            textStyle: {
                //color: '#fff'
            }
        }, {
            text: '策略/任务组总数',
            left: '83%',
            top: '6%',
            textAlign: 'center',
            textStyle: {
                //color: '#fff'
            }
        }],
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            x: 300,
            top: '7%',
            textStyle: {
                color: '#ffd285',
            },
            data: ['任务组', '策略']
        },
        /*grid: {
            left: '1%',
            right: '35%',
            top: '16%',
            bottom: '6%',
            containLabel: true
        },*/
        grid: [{
            left: 50,
            right: 50,
            top: '20%',
            height: '30%',
            width: '60%'
        }, {
            left: 50,
            right: 50,
            top: '65%',
            bottom: '6%',
            height: '29%',
            width: '60%'
        }],
        toolbox: {
            "show": false,
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: [
            {
                type : 'category',
                //boundaryGap : false,
                axisLine: {onZero: true},
                data: ['0', '0', '0', '0', '0', '0']
            },
            {
                gridIndex: 1,
                type : 'category',
                //boundaryGap : false,
                axisLine: {onZero: true},
                data: ['0', '0', '0', '0'],
                position: 'bottom'
            }
        ],
        yAxis: [
            {
            name : '任务组',
            type : 'value',
        },
        {
            gridIndex: 1,
            name : '策略',
            type : 'value',
            //inverse: true
        }
        ],
        series: [{
            name:'任务组',
            type:'bar',
            symbolSize: 8,
            barWidth : 10,//柱图宽度
            hoverAnimation: false,
            data:[0, 0, 0, 0, 0, 0]
        },
        {
            name:'策略',
            type:'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            symbolSize: 8,
            barWidth : 10,//柱图宽度
            hoverAnimation: false,
            data: [0, 0, 0, 0]
        },
        {
            type: 'pie',
            center: ['83%', '35%'],
            radius: ['30%', '38%'],
            label: {
                normal: {
                    position: 'center'
                }
            },
            data: [{
                value: 0,
                name: '总数情况',
                itemStyle: {
                    normal: {
                        color: '#ffd285'
                    }
                },
                label: {
                    normal: {
                        formatter: '{c}',
                        textStyle: {
                            color: '#ffd285',
                            fontSize: 20

                        }
                    }
                }
            }, {
                name: '占位',
                tooltip: {
                    show: false
                },
                itemStyle: {
                    normal: {
                        color: '#87CEFA'
                    }
                },
                label: {
                    normal: {
                        textStyle: {
                            color: '#ffd285',
                        },
                        formatter: '\n告警任务组总数'
                    }
                }
            }]
        },


        {
            type: 'pie',
            center: ['83%', '76%'],
            radius: ['30%', '38%'],
            label: {
                normal: {
                    position: 'center'
                }
            },
            data: [{
                value: 0,
                name: '用户来源分析',
                itemStyle: {
                    normal: {
                        color: '#ff733f'
                    }
                },
                label: {
                    normal: {
                        formatter: '{c}',
                        textStyle: {
                            color: '#ff733f',
                            fontSize: 20

                        }
                    }
                }
            }, {
                name: '占位',
                tooltip: {
                    show: false
                },
                itemStyle: {
                    normal: {
                        color: '#87CEFA'
                    }
                },
                label: {
                    normal: {
                        textStyle: {
                            color: '#FF4500',
                        },
                        formatter: '\n告警策略总数'
                    }
                }
            }]
        }]
    };
    ruleTaskChart = echarts.init($('#ruleTask')[0]);
    ruleTaskChart.setOption(option);
    window.addEventListener('resize',function(){
        ruleTaskChart.resize();
    })
}

initRiskCount();
initTypeCount();
initDeviceNum();
initRuleTaskCount();
$('#showMore').on('click',function(){
    setTimeout(function(){
        riskChart.resize();
        typeChart.resize();
        ruleTaskChart.resize();
        deviceNumChart.resize();
        trendAlarm.resize();
    },200);

    if( $('#collapseSearch').css('display') == 'none'){
        $('.container-left,.container-right').fadeOut();
        $('#collapseSearch').fadeIn();
        $('#showMore').html('<i class="fa fa-angle-double-left"></i>返回');
        clearAll();
    }else{
        $('.container-left,.container-right').fadeIn();
        $('#collapseSearch').fadeOut();
        $('#showMore').html('<i class="fa fa-angle-double-right"></i>高级')
    }
})

function clearAll(){
    $('.selectpicker').selectpicker('val','');
    $('input').val('');
    firstSelect("warning_module");
    firstSelect("warning_type");
    $('#searchCondition').html('');
    for(var key in searchParam){
        searchParam[key] = '';
    }
    switchTime('30days');
    if(is_contain_sub == 1){
        $('#director_node').parent().next('label').find('input[type=checkbox]').click();
        is_contain_sub = 0;
    }
}
function searchData(){
    var searchCondition = "【当前查询条件:】";
    if($('#time_min').val()!=''){
        if($('#time_max').val() == ''){
            $('#time_max').val(new Date().toLocaleDateString().replace(/\//g,'-'))
        }
        searchParam['time'] = $('#time_min').val()+'——'+$('#time_max').val();
    }
    if($('#device_id').val()!=''){
        searchParam['device_id'] = $('#device_id').val();
    }else{
        searchParam['device_id'] = '';
    }
    if($('#rule_id').val()!=''){
        searchParam['rule_id'] = $('#rule_id').val();
    }else{
        searchParam['rule_id'] = '';
    }
    if($('#task_group_id').val()!=''){
        searchParam['group_id'] = $('#task_group_id').find('option:selected').text();
    }else{
        searchParam['group_id'] = '';
    }
    console.log(searchParam)
    if($('#warning_module').attr('value')!="0"){
        //searchParam['business_type'] = $('#warning_module').attr('value');
        searchParam['warning_module'] = $('#warning_module_list li[value='+$('#warning_module').attr('value')+']').text();
    }else{
        searchParam['warning_module'] = '';
    }
    if($('#warning_type').attr('value')!="0"){
        //searchParam['alarm_type'] = $('#warning_type').attr('value');
        searchParam['warning_type'] = $('#warning_type_list li[value='+$('#warning_type').attr('value')+']').text();
    }else{
        searchParam['warning_type'] = '';
    }
    for(var key in searchParam){
        if(searchParam[key]!=''){
            searchCondition += "<span style='color:#999999'>"+searchCh[key]+":</span>"+searchParam[key]+','
        }
    }
    $('#searchCondition').html(searchCondition);

    /* 时间通用 */
    param= {};
    if(searchParam['time'] != '' && $('#time_min').val()==""){
        var days = 7;
        if(searchParam['time'] == '近30天')
            days = 30;
        param['days'] = days;
        delete param['time_min'];
        delete param['time_max'];
    }else{
        param['time_min'] = $('#time_min').val();
        param['time_max'] = $('#time_max').val();
        delete param['days']
    }
    if($('#device_id').val()!=""){
        param['device_id'] = $('#device_id').val();
    }
    if($('#rule_id').val()!=""){
        param['rule_id'] = $('#rule_id').val();
    }
    if($('#task_group_id').val()!=""){
        param['group_id'] = $('#task_group_id').val();
    }
    if($('#warning_module').attr('value')!="0"){
        param["warning_module"] = $('#warning_module').attr('value');
    }
    if($('#warning_type').attr('value')!="0"){
        param["warning_type"] = $('#warning_type').attr('value');
    }
    if(is_contain_sub == 1){
        param["is_contain_sub"] = is_contain_sub;
    }
    console.log(param)
    getRisk(param);
    getTrendAlarm(param);
    getDevice(param);
    getBusinessType(param);
    getAlarmType(param);
    getRuleTask(param);
}

// 态势统计
var getTrendAlarm = function(param){
    if(searchParam['time'] != '' && $('#time_min').val()==""){
        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.newly_trend",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                consturct_newly_trend(ret.msg)
            }
        });
    }else{
        $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.show_alarm_between_days",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                consturct_newly_trend(ret.msg)
            }
        });
    }
}
// 级别统计
var riskMap = {
            '-1':'未知',
            0:'无风险',
            1:'一般级',
            2:'关注级',
            3:'严重级',
            4:'紧急级'
        }
var getRisk = function(param){
    param['query_condition'] = 'risk'
    $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                var arrX = [],arrY = [];
                var count = 0;
                for(var i=0;i<ret['msg'].length;i++){
                    if(ret['msg'][i].risk!='-1'){
                        arrY.push(riskMap[ret['msg'][i].risk]);
                        arrX.push(ret['msg'][i].amount);
                        count += parseInt(ret['msg'][i].amount);
                    }
                }
                var option = riskChart.getOption();
                option.series[0].data = arrX;
                option.yAxis[0].data = arrY;
                riskChart.setOption(option);
                $('#alarmCount').text(count);
            }
    });
}
// 地区
// var getNode = function(param){
//     param['query_condition'] = "node_id"
//     $.ajax({
//             url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
//             type: "post",
//             data: param,
//             cache: false,
//             success: function(data){
//                 var ret = JSON.parse(data);
//                 var arrX = [],seriesData = [];
//                 for(var i=0;i<ret['msg'].length;i++){
//                     if(ret['msg'][i].risk!='-1'){
//                         seriesData.push(ret['msg'][i].amount);
//                         arrX.push(ret['msg'][i].name);
//                     }
//                 }
//                 var option = nodeNumChart.getOption();
//                 option.series[0].data = seriesData;
//                 option.xAxis[0].data = arrX;
//                 nodeNumChart.setOption(option);
//             }
//     });
// }

// 管理中心
// var getCenter = function(param){
//     param['query_condition'] = "center_id";
//     $.ajax({
//             url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
//             type: "post",
//             data: param,
//             cache: false,
//             success: function(data){
//                 var ret = JSON.parse(data);
//                 var arrX = [],seriesData = [];
//                 for(var i=0;i<ret['msg'].length;i++){
//                     if(ret['msg'][i].risk!='-1'){
//                         seriesData.push(ret['msg'][i].amount);
//                         arrX.push(ret['msg'][i].center_id);
//                     }
//                 }
//                 var option = centerNumChart.getOption();
//                 option.series[0].data = seriesData;
//                 option.xAxis[0].data = arrX;
//                 centerNumChart.setOption(option);
//                 $('#centerCount').text(ret['msg'].length);
//             }
//     });
// }
//检测器
var getDevice = function(param){
    param['query_condition'] = "device_id";
    $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                var arrX = [],seriesData = [];
                for(var i=0;i<ret['msg'].length;i++){
                    if(ret['msg'][i].risk!='-1'){
                        seriesData.push(ret['msg'][i].amount);
                        arrX.push(ret['msg'][i].device_id);
                    }
                }
                var option = deviceNumChart.getOption();
                option.series[0].data = seriesData;
                option.xAxis[0].data = arrX;
                deviceNumChart.setOption(option);
                console.log(ret['msg'].length)
                $('#deviceCount').text(ret['msg'].length);
            }
    });
}
// 告警类型（大类）
var warning_moduleMap =
    {
        1:'攻击窃密',
        2:'异常行为',
        3:'违规泄密',
        4:'目标帧听',
        5:'通信阻断',
        //6:'插件告警'
    }
var warning_typeMap=
    {   
        // 0:'未知告警',
        // 1:'密标文件',
        // 2:'标密文件',
        // 3:'关键词',
        // 4:'加密文件',
        // 5:'压缩文件',
        // 6:'图片筛选',
        // 7:'版式检测',
        // 8:'木马攻击',
        // 9:'漏洞利用',
        // 10:'恶意程序',
        // 11:'其他攻击',
        // 12:'未知攻击',
        // 13:'IP审计',
        // 14:'域名审计',
        // 15:'URL审计',
        // 16:'账号审计',
        // 17:'通信阻断'
        // 1:'木马攻击',
        1:'木马攻击',
        2:'漏洞利用',
        3:'恶意程序',
        4:'其他攻击',
        5:'异常行为',
        6:'Email涉密',
        7:'Im涉密',
        8:'FTP涉密',
        9:'HTTP涉密',
        10:'Netdisk涉密',
        11:'其他涉密',
        12:'IP审计',
        13:'域名审计',
        14:'URL审计',
        15:'账号审计',
        16:'通信阻断',
    }
var getBusinessType = function(param){
    param['query_condition'] = "warning_module";
    $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                var option = typeChart.getOption();
                var warning_module_data = option.series[0].data;
                warning_module_data.map(function(v){
                    v.value = 0;
                })
                for(var i=0;i<ret['msg'].length;i++){
                    for(var j=0;j<warning_module_data.length;j++){
                        if(warning_moduleMap[ret['msg'][i].warning_module] == warning_module_data[j].name){
                            warning_module_data[j].value = ret['msg'][i].amount;
                        }
                    }
                }
                option.series[0].data = warning_module_data;
                typeChart.setOption(option);
            }
    });
}
// 告警类型（小类）
var getAlarmType = function(param){
    param['query_condition'] = "warning_type";
    $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                var option = typeChart.getOption();
                for(var i=1;i<6;i++){
                    option.series[i].data.map(function(v){
                        v.value = 0;
                    })
                    for(var j=0;j<option.series[i].data.length;j++){
                        for(var k=0;k<ret['msg'].length;k++){
                            if(option.series[i].data[j].name == warning_typeMap[ret['msg'][k].warning_type]){
                                option.series[i].data[j].value = ret['msg'][k].amount;
                            }
                        }
                    }
                    
                }
                typeChart.setOption(option);
            }
    });
}
// 策略/任务组
var getRuleTask = function(param){
    param['query_condition'] = "rule_id";
    $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                var option = ruleTaskChart.getOption();
                option.xAxis[1].data = [];
                option.series[1].data = [];
                option.series[3].data[0].value = 0;
                var msg = ret['msg'];
                var xAxis = [],yAxis = [];
                for(var i=0;i<msg.length;i++){
                    xAxis.push(msg[i].rule_id);
                    yAxis.push(msg[i].amount);
                }
                option.xAxis[1].data = xAxis;
                option.series[1].data = yAxis;
                option.series[3].data[0].value = msg.length;
                ruleTaskChart.setOption(option);
            }
    });

    param['query_condition'] = "group_id";
    $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data: param,
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                var option = ruleTaskChart.getOption();
                option.xAxis[0].data = [];
                option.series[0].data = [];
                option.series[2].data[0].value = 0;
                var msg = ret['msg'];
                var xAxis = [],yAxis = [];
                for(var i=0;i<msg.length;i++){
                    xAxis.push(msg[i].name);
                    yAxis.push(msg[i].amount);
                }
                option.xAxis[0].data = xAxis;
                option.series[0].data = yAxis;
                option.series[2].data[0].value = msg.length;
                ruleTaskChart.setOption(option);
            }
    });
}

var searchCh =  {
    time:'时间',
    device_id:'检测器',
    rule_id:'策略ID',
    group_id:'任务组',
    warning_module:'告警大类',
    warning_type:'告警小类',
    risk:'告警级别'
}
var param = {};
var searchParam = {
    time: '',
    device_id:'',
    rule_id:'',
    group_id:'',
    warning_module:'',
    warning_type:''
}

function switchTime(type){
    $('#time_min,#time_max').val('');
    if(type=='30days'){
        searchParam['time'] = '近30天';
        searchData();
    }
    if(type=='week'){
        searchParam['time'] = '近7天';
        searchData();
    }
}

// 导出当前查询
function export_search(type) {
    var query_param = ""
    if(type!='time'){
        query_param += "?query_condition="+type;
        for(var key in param){
            if(key!='query_condition')
                query_param += "&"+key+"="+param[key];
        }        
        var uu = "/alarm/export_alarm_report" + query_param +"&rename="+searchCh[type]+".xlsx";
        window.location.href = "/ajax_action_download_stat_rename.php?uu="+ uu ;
    }else{
        // 按时间段导出
        if(param['time_min']!=undefined){
            query_param += "?time_min="+param['time_min'];
            for(var key in param){
                if(key!='time_min' && key!='query_condition')
                    query_param += "&"+key+"="+param[key];
            }
            window.location.href = "/ajax_action_download_stat_rename.php?uu=/alarm/export_time_alarm_report" + query_param +"&rename="+param['time_min']+"-"+param['time_max']+"告警.xlsx";
        }else if(param['days']!=undefined){
            // 按固定时间导出
            query_param += "?days="+param['days'];
            for(var key in param){
                if(key!='days'&&key!='query_condition')
                    query_param += "&"+key+"="+param[key];
            }
            window.location.href = "/ajax_action_download_stat_rename.php?uu=/alarm/export_last_days_report" + query_param +"&rename="+searchParam['time']+"告警.xlsx";
        }
    }
    

    console.log(param)
    var file_path = "/alarm/ExportAlarmReport";
    var file_name = "告警统计报表（按条件）.xlsx";
    //var param = "?query_condition=risk&days=30"


    //window.location.href = "/ajax_action_download_rename.php?uu=/alarm/ExportAlarmReport" + param + "&rename=daochu.xlsx";

    //window.location.href ="/ajax_action_download_rename.php?uu="+file_path +"&rename="+file_name+param;
}


// 初始化相关数据
$(function(){
    /*$.ajax({
        url: "/ajax_action_detector.php?uu=command.get_detector_node",
        success: function (data) {
            var res = JSON.parse(data);
            if (res.code == "200") {
                var nodeData = res["msg"]["node_list"];
                var nodeoption = "";
                nodeData.map(function(v,i){
                    nodeoption+=`<option value=${v.node_id}>${v.name}</option>`
                })
                $('#node_id').append(nodeoption);
                $('#node_id').selectpicker('refresh');
            }
        }
    })

    $.ajax({
        url: "/ajax_action_detector.php?uu=command.get_manage_num",
        success: function (data) {
            var res = JSON.parse(data);
            if (res.code == "200") {
                var count = res["msg"]["count"];
                $.ajax({
                    url:"/ajax_action_detector.php?uu=command.get_manage_info&p_size="+count+"&pn=1",
                    success:function(data){
                        var res = JSON.parse(data);
                        if(res.code == "200"){
                            var centerData = res["msg"];
                            var centeroption = "";
                            centerData.map(function(v,i){
                                centeroption+=`<option value=${v.center_id}>${v.center_id}</option>`
                            })
                            $('#center_id').append(centeroption);
                            $('#center_id').selectpicker('refresh');
                        }
                    }
                })
            }
        }
    })*/

    $.ajax({
        url: "/ajax_action_detector.php?uu=task_group.count",
        success: function (data) {
            var res = JSON.parse(data);
            if (res.code == "200") {
                var count = res["msg"]["count"];
                $.ajax({
                    url:"/ajax_action_detector.php?uu=task_group.show&p_size="+count+"&pn=1",
                    success:function(data){
                        var res = JSON.parse(data);
                        if(res.code == "200"){
                            var taskData = res["msg"];
                            var option = "";
                            taskData.map(function(v,i){
                                option += `<option value=${v.group_id}>${v.name}</option>`;
                            })
                            $('#task_group_id').append(option);
                            $('#task_group_id').selectpicker('refresh');
                        }
                    }
                })
            }
        }
    })

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
})
/* 是否包含下级复选框 */
var is_contain_sub_html = '<label style="display:none;font-weight:normal;font-size:12px"><input onclick="isContainSub()" type="checkbox" >是否包含下级地区</label>';
    $('#director_node').after(is_contain_sub_html);
var is_contain_sub = 0;
$('#director_node').change(function(){
	$('#director_node').parent().next('label').css('display','table-footer-group');
})
// function isContainSub(){
//     is_contain_sub = is_contain_sub == 0 ? 1 : 0;
//     $('#director_node').change();
// }

// 地区、管理中心、检测器联动
// 搜索项联动
$('#clearButton').on('click',function(){
    var deviceOpt = '<option value="">全部检测器</option>';
    cascadeNodeCenterDevice['device_id'].map(function(v){
        deviceOpt += '<option value='+v.value+'>'+v.name+'</option>';
    });
    $('#device_id').html(deviceOpt);
    $('#device_id').selectpicker('refresh');
})