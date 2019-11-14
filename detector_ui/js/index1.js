



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

var risk_option = {
    title: {
        // text: '告警统计图',
        textStyle:{
            color:"#3693CF",
            fontSize:18,
        },
        left:'47%'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    grid:{
        x: 60,
        y: 30,
        x2: 30,
        y2: 30
    },
    color:[ '#328FCA'],
    
    series : [
        {
            name: '告警级别',
            type: 'pie',
            radius : '80%',
            center: ['50%', '50%'],
            data:[
                
            ],
            itemStyle: {
                normal:{
                    borderWidth: 3,
                    borderColor: '#235894'
                }
            }
        }
    ]
};

//告警级别统计表
function construct_risk(data){
    var riskMap = {
        '-1':'未知',
        0:'无风险',
        1:'一般级',
        2:'关注级',
        3:'严重级',
        4:'紧急级'
    }
    var arr1 = new Array();
    var arr2 = new Array();

    for(var i=0;i<data.length;i++){
        //arr1[i] = data[i].amount
        //arr2[i] = riskMap[data[i].risk]
        if(data[i].risk!=-1){
            var obj = {'name':riskMap[data[i].risk],'value':data[i].amount};
            risk_option.series[0].data.push(obj);
        }
    }

    risk_chart.setOption(risk_option);
}
    var risk_chart = echarts.init(document.getElementById('attacked-risk-div'));

    $(function () {
        console.log("执行js");
        get();
        window.onresize = function(){
            risk_chart.resize();
        }

    });

    function get() {
        // 告警级别
            $.ajax({
            url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
            type: "post",
            data:{query_condition:'risk'},
            cache: false,
            success: function(data){
                var ret = JSON.parse(data);
                construct_risk(ret.msg);
                }
            });
    }
    $(function() {
        buildFrame("summary");
        
        $("#map-div").height($(window).height()-50);
        window.addEventListener('resize',function(){
            $("#map-div").height($(window).height()-50);
        })
        
        // createMapView(); 
        // createCanvas();
        // createAllChart(); //创建所有图表
        
        //$('.summary-copyright').html(COPYRIGHT);
    });