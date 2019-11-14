
        // 告警级别
        var createAlarmLevel = function (data) {
            var dataAxis = [];
            var seriesData = [];
            var alarmLevelType = {
                '-1':'未知',
                0:'无风险',
                1:'一般级',
                2:'关注级',
                3:'严重级',
                4:'紧急级',
            }
            /*for(var item in data){
                dataAxis.push(alarmLevelType[item]);
                seriesData.push(data[item]);
            }*/
            for(var i=0;i<data.length;i++){
                if(data[i].risk!=-1){
                    dataAxis.push(alarmLevelType[data[i].risk])
                    seriesData.push(data[i].amount);
                } 
            }
            var yMax = seriesData.sort()[seriesData.length-1];
            var dataShadow = [];

            for (var i = 0; i < seriesData.length; i++) {
                dataShadow.push(yMax);
            }

            var alarmLevelOption = {
                title: {
                    //text: '告警级别',
                    textStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    //trigger: 'axis'
                },
                grid: {
                    left: '-10%',
                    right: '10%',
                    top: '10%',
                    height: '89%', //设置grid高度
                    containLabel: true
                },
                xAxis: {
                    data: dataAxis,
                    axisLabel: {
                        //inside: true,
                        textStyle: {
                            color: '#fff'
                        },
                        interval:0
                    },
                    axisTick: {
                        show: false
                    },
                    axisLine: {
                        show: false
                    },
                    z: 10
                },
                yAxis: {
                    axisLine: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        show: false,
                        textStyle: {
                            color: '#fff'
                        }
                    }
                },
                dataZoom: [
                    {
                        type: 'inside'
                    }
                ],
                series: [
                    { // For shadow
                        type: 'bar',
                        itemStyle: {
                            normal: { color: 'rgba(0,0,0,0.05)' }
                        },
                        barWidth: 36,
                        barGap: '-100%',
                        barCategoryGap: '40%',
                        data: dataShadow,
                        animation: false
                    },
                    {
                        type: 'bar',
                        barWidth: 36,
                        itemStyle: {
                            normal: {
                                color: /*new echarts.graphic.LinearGradient(
                                    0, 0, 0, 1,
                                    [
                                        { offset: 0, color: '#83bff6' },
                                        { offset: 0.5, color: '#188df0' },
                                        { offset: 1, color: '#188df0' }
                                    ]
                                )*/function(param){
                                    var color = 'rgb(145,199,174)';
                                    switch(param.name){
                                        case '一般级':
                                            color = 'rgb(97,160,168)';
                                            break;
                                        case '关注级':
                                            color = 'rgb(255,115,63)';
                                            break;
                                        case '紧急级':
                                            color = 'rgb(255,210,133)';
                                            break;
                                        case '严重级':
                                            color = 'rgb(236,72,99)';
                                            break;
                                    }
                                    return color;
                                },
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle: {
                                        color: '#fff'
                                    }
                                }
                            },
                            /*emphasis: {
                                color: new echarts.graphic.LinearGradient(
                                    0, 0, 0, 1,
                                    [
                                        { offset: 0, color: '#2378f7' },
                                        { offset: 0.7, color: '#2378f7' },
                                        { offset: 1, color: '#83bff6' }
                                    ]
                                )
                            }*/
                        },
                        data: seriesData
                    }
                ]
            };

            // Enable data zoom when user click bar.
            var alarmLevelChart = echarts.init($('.modalBody')[0]);
            alarmLevelChart.setOption(alarmLevelOption);
            echartsResize(alarmLevelChart);
            var zoomSize = 6;
            alarmLevelChart.on('click', function (params) {
                alarmLevelChart.dispatchAction({
                    type: 'dataZoom',
                    startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
                    endValue: dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
                });
            });
        }

        // 告警态势
        var createAlarmTrend = function (data) {
            alarmTrendChart = echarts.init($('.modalBody')[1]);
            var xAxisData = [],seriesData=[];
            data.map(function(v){
                xAxisData.push(v.date);
                seriesData.push(v.amount);
            })
            echartsResize(alarmTrendChart);
                alarmTrendChart.setOption({
                    title: {
                        //text: '告警态势',
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    grid: {
                        left: '3%',
                        //right: '10%',
                        top: '10%',
                        height: '89%', //设置grid高度
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    xAxis: {
                        data: xAxisData,
                        axisLine: {
                            lineStyle: {
                                color: "#fff"
                            }
                        },
                        axisLabel: {
                            textStyle: {
                                color: '#fff'
                            },
                            //interval:0
                        },
                    },
                    yAxis: {
                        splitLine: {
                            show: false
                        },
                        axisLine: {
                            lineStyle: {
                                color: "#fff"
                            }
                        },
                        axisLabel: {
                            textStyle: {
                                color: '#fff'
                            },
                        },
                    },
                    series: {
                        name:'数量',
                        type: 'line',
                        data: seriesData,
                        smooth: true,
                        symbolSize: 12,
                        lineStyle: {
                            normal: {
                                width: 5,
                            },
                        },
                        markLine: {
                            silent: true,
                            /*data: [{
                                yAxis: 20
                            }, {
                                yAxis: 40
                            }, {
                                yAxis: 60
                            }, {
                                yAxis: 80
                            }, {
                                yAxis: 100
                            }]*/
                            data: [
                                {type: 'average', name: '平均值'}
                            ]
                        }
                    }
                });

        }

        // 任务组告警
        var createTaskGroup = function (data) {
            alarmTaskGroupChart = echarts.init($('.modalBody')[4]);
            var xAxisData = [],seriesData=[];
            data.map(function(v){
                xAxisData.push(v.name);
                seriesData.push(v.amount);
            })
            echartsResize(alarmTaskGroupChart);
                alarmTaskGroupChart.setOption({
                    title: {
                        //text: '告警态势',
                        textStyle: {
                            color: '#fff'
                        }
                    },
                    grid: {
                        left: '3%',
                        //right: '10%',
                        top: '10%',
                        height: '89%', //设置grid高度
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    xAxis: {
                        data: xAxisData,
                        axisLine: {
                            lineStyle: {
                                color: "#fff"
                            }
                        },
                        axisLabel: {
                            textStyle: {
                                color: '#fff',
                                //fontSize: 8
                            },
                            //interval:0,
                            //rotate: 10
                            formatter:''
                        },
                    },
                    yAxis: {
                        splitLine: {
                            show: false
                        },
                        axisLine: {
                            lineStyle: {
                                color: "#fff"
                            }
                        },
                        axisLabel: {
                            textStyle: {
                                color: '#fff'
                            },
                        },
                    },
                    series: {
                        name:'数量',
                        type: 'bar',
                        data: seriesData,
                        smooth: true,
                        symbolSize: 12,
                        barWidth: 30,
                        lineStyle: {
                            normal: {
                                width: 5,
                            },
                        },
                        itemStyle:{
                            normal:{
                                label: {
                                    show: true,
                                    position: 'top',
                                    textStyle: {
                                        color: '#fff'
                                    },
                                    formatter: '{b}'
                                }
                            }
                        }
                    }
                });

        }

        // 告警类型
        var createAlarmType = function (data) {
            var warning_typeMap={
                /*0:'未知告警',
                1:'密标文件',
                2:'标密文件',
                3:'关键词',
                4:'加密文件',
                5:'压缩文件',
                6:'图片文件',
                7:'版式文件',
                8:'木马攻击',
                9:'漏洞利用',
                10:'恶意文件',
                11:'其他攻击',
                12:'未知攻击',
                13:'IP审计',
                14:'域名审计',
                15:'URL审计',
                16:'账号审计',
                17:'通信阻断'*/
                1: '传输涉密',
                2: '攻击窃密',
                3: '未知攻击',
                4: '目标审计',
                5: '通信阻断',
            }
            var amountData = [],seriesData = [];
            data.map(function(v){
                if(v.warning_module!=0 && v.warning_module!=6){
                    var item = {};
                    item.value = v.amount;
                    item.name = warning_typeMap[v.warning_module];
                    seriesData.push(item);
                }
                
            })
            var alarmTypeOption = {
                title: {
                    //text: '告警类型',
                    textStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {},
                /*grid: [
                    { x: '20%', y: '62%', width: '88%', height: '30%' },
                ],*/
                grid: {
                        left: '3%',
                        //right: '10%',
                        top: '10%',
                        height: '89%', //设置grid高度
                        containLabel: true
                    },
                color:["#72CAE7", "#1693A5", "#D9544F","#1693A5", "#FFC100", "#D9544F"],
                series: [
                    {
                        name: '告警类型',
                        type: 'pie',
                        radius: ['0%', '70%'],
                        label: {
                            normal: {
                                //formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                                backgroundColor: 'transparent',
                                //borderColor: '#aaa',
                                borderWidth: 1,
                                borderRadius: 4,
                                //position:'inner',
                                // shadowBlur:3,
                                // shadowOffsetX: 2,
                                // shadowOffsetY: 2,
                                // shadowColor: '#999',
                                // padding: [0, 7],
                                formatter: '{b}',
                                textStyle: {
                                    color: '#fff',
                                    fontSize: 14
                                },
                                rich: {
                                    a: {
                                        color: '#999',
                                        lineHeight: 22,
                                        align: 'center'
                                    },
                                    // abg: {
                                    //     backgroundColor: '#333',
                                    //     width: '100%',
                                    //     align: 'right',
                                    //     height: 22,
                                    //     borderRadius: [4, 4, 0, 0]
                                    // },
                                    hr: {
                                        borderColor: '#aaa',
                                        width: '100%',
                                        borderWidth: 0.5,
                                        height: 0
                                    },
                                    b: {
                                        fontSize: 16,
                                        lineHeight: 33
                                    },
                                    per: {
                                        color: '#eee',
                                        backgroundColor: '#334455',
                                        padding: [2, 4],
                                        borderRadius: 2
                                    }
                                }
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        data: seriesData
                    }
                ]
            };

            var alarmTypeChart = echarts.init($('.modalBody')[2]);
            alarmTypeChart.setOption(alarmTypeOption);
            echartsResize(alarmTypeChart);

            var app = {};
            app.currentIndex = -1;
        }

        // 告警单位top10
        var createAlarmUnit = function (pieData) {
            var alarmUnitChart = echarts.init($('.modalBody')[3]);
            pieData.map(function(v,i){
                pieData[i].value = v.amount;
                pieData[i].name = v.device_id == ""?"未知":v.device_id;
            })
            var yAxisData = [],dataAll = [];
            pieData.sort(function (a, b) { return a.value - b.value; })
            pieData.map(function(v){
                yAxisData.push(v.name);
                dataAll.push(v.value);
            })
            var alarmUnitOption = {
                title: {
                    //text: '中心告警TOP10',
                    textStyle: {
                        color: '#fff'
                    }
                },
                grid: {
                    left: '3%',
                    right: '10%',
                    top: '10%',
                    height: '89%', //设置grid高度
                    containLabel: true
                },
                tooltip: {
                    trigger: 'item'
                },
                xAxis: [
                    {gridIndex: 0, axisTick: {show:false},axisLabel: {show:false},splitLine: {show:false},axisLine: {show:false }},
                ],
                yAxis: [
                    {  gridIndex: 0, interval:0,data:yAxisData,
                        axisTick: {show:false}, axisLabel: {show:true},splitLine: {show:false},
                        axisLine: {show:true,lineStyle:{color:"#fff"}},
                    }
                ],
                series: [{
                    name: '检测器告警',
                    type: 'bar',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    barWidth:'10',
                    itemStyle:{normal:
                        {color:'#66FF33'}
                    },
	                label:{
                        normal:{
                            show:true, 
                            position:"right",
                            textStyle:{
                                color:"#fff"
                            }
                        }
                    },
                    data: dataAll,
                }]
            };

            alarmUnitChart.setOption(alarmUnitOption);
            echartsResize(alarmUnitChart);
        }

        // 检测器使用状态
        var createDeviceStatus = function (data) {
            var warning_typeMap={
                1: '',
                2: '',
                3: '',
                4: '',
                5: '',
                6: '',
            }
            var amountData = [],seriesData = [];
            data.map(function(v){
                var item = {};
                item.value = v.amount;
                item.name = v.status;
                seriesData.push(item);
            })
            var deviceStatusOption = {
                title: {
                    //text: '告警类型',
                    textStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {},
                grid: {
                        left: '3%',
                        //right: '10%',
                        top: '10%',
                        height: '89%', //设置grid高度
                        containLabel: true
                    },
                color:["#72CAE7","#FFC100", "#1693A5", "#D9544F","#1693A5", "#D9544F"],
                series: [
                    {
                        name: '检测器状态',
                        type: 'pie',
                        radius: ['0%', '60%'],
                        label: {
                            normal: {
                                //formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                                backgroundColor: 'transparent',
                                borderColor: '#aaa',
                                borderWidth: 1,
                                borderRadius: 4,
                                //position:'inner',
                                shadowBlur:3,
                                shadowOffsetX: 2,
                                shadowOffsetY: 2,
                                shadowColor: '#999',
                                padding: [3, 7],
                                formatter: '{b}:{c}',
                                textStyle: {
                                    color: '#fff',
                                    fontSize: 14
                                },
                                rich: {
                                    a: {
                                        color: '#999',
                                        lineHeight: 22,
                                        align: 'center'
                                    },
                                    // abg: {
                                    //     backgroundColor: '#333',
                                    //     width: '100%',
                                    //     align: 'right',
                                    //     height: 22,
                                    //     borderRadius: [4, 4, 0, 0]
                                    // },
                                    hr: {
                                        borderColor: '#aaa',
                                        width: '100%',
                                        borderWidth: 0.5,
                                        height: 0
                                    },
                                    b: {
                                        fontSize: 16,
                                        lineHeight: 33
                                    },
                                    per: {
                                        color: '#eee',
                                        backgroundColor: '#334455',
                                        padding: [2, 4],
                                        borderRadius: 2
                                    }
                                }
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        data: seriesData
                    }
                ]
            };

            var deviceStatusChart = echarts.init($('.modalBody')[5]);
            deviceStatusChart.setOption(deviceStatusOption);
            echartsResize(deviceStatusChart);
        }
       // 统计数量
        var initCountChart = function (mainData) {
            var countChart = echarts.init($(".countData>div")[0]);
            function createSeries(mainData) {
                var result = [];
                var insideLabel = {
                    normal: {
                        position: 'center',
                        formatter: function (params) {
                            if(params.name=="告警数")
                                return '{b|'+params.name+ '}' + '\n' + '{a|'+params.value+'}';
                            return params.name + '\n' + '{a|'+params.value+'}';
                        },
                        rich:{
                            a:{
                                fontSize:22,
                                fontWeight: 'bold',
                                color:'orange'
                            },
                            b:{
                                fontSize:18,
                                fontWeight: 'bold',
                                color:'rgb(194,53,49)'
                            }
                        },
                        textStyle: {
                            color:'yellow',
                            fontStyle: 'normal',
                            fontWeight: 'bold',
                            fontSize: 16
                        }
                    }
                };
                var outsideLabel = {
                    normal: {
                        show: false
                    }
                };
                for (var i = 0; i < mainData.length; i++) {
                    var data = [];
                    var obj = {
                        name: mainData[i].name,
                        value: mainData[i].value,
                        itemStyle: {
                            normal: {
                                color: '#3dd4de',
                                shadowColor: '#3dd4de',
                                shadowBlur: 20
                            }
                        }
                    }
                    if(mainData[i].name=="告警数"){
                       obj.itemStyle = {
                                normal: {
                                    color: '#3dd4de',
                                    shadowColor: '#3dd4de',
                                    shadowBlur: 20
                                }
                            }
                    }
                    data.push(obj);
                    result.push({
                        type: 'pie',
                        center: [i * 25 + 12+ '%', '50%'],
                        radius: ['74%', '80%'],
                        label: insideLabel,
                        data: data
                    });
                }
                return result;
            }
            var countChartOption = {
                series: createSeries(mainData)
            }
            countChart.setOption(countChartOption);
            window.addEventListener("resize", function () {
                countChart.resize();
            })
        }


    //创建three星星背景
        var createCanvas = function () {
            t = document.getElementsByClassName('product-wrapper')[0],
                e = THREE,
                r = window.innerWidth,
                i = window.innerHeight - 50,
                c = 0,
                p = r / 2,
                d = i / 2,
                s = document.createElement("div"),
                s.id = "weaponCanvas",
                s.style.position = 'absolute',
                s.style.top = 0,
                t.prepend(s),
                a = new e.PerspectiveCamera(75, r / i, 1, 1e4),
                a.position.z = 1500,
                f = new e.Scene,
                f.add(a),
                l = new e.CanvasRenderer,
                l.setSize(r, i - 10),
                //x(),
                s.appendChild(l.domElement),
                document.addEventListener('mousemove', b, false);
                document.addEventListener('touchstart', w, false);
                document.addEventListener('touchmove', E, false);

            u = setInterval(S, 1e3 / 30)

            function b(e) {
                e.clientX > p / 2 && e.clientX < p / 2 + p && (c = e.clientX - p)
            }
            function w(e) { }
            function E(e) {
                e.touches.length === 1 && (e.preventDefault(), c = e.touches[0].pageX - p, h = e.touches[0].pageY - d)
            }
            function S() {
                a.position.x += (c - a.position.x) * .05,
                    a.lookAt(f.position),
                    l.render(f, a)
            }
            m = new Image,
                m.src = "images/ui/star-ignore.png";

            var n = 0,
                r = 0,
                v = [],
                i = new e.ParticleBasicMaterial({
                    map: new e.Texture(m)
                });
            for (var s = 0; s < 400; s++) o = new THREE.Particle(i),
                n = T(- 3.5, 3.5),
                r = N(n, 0, 2),
                o.position.y = T(- r, r) * 1400,
                o.position.x = n * 500,
                o.position.z = Math.random() * 800 - 400,
                o.scale.x = o.scale.y = 1,
                f.add(o),
                v.push(o);
            for (var s = 0; s < 20; s++) o = new THREE.Particle(i),
                o.position.x = Math.random() * 2e3 - 2e3,
                o.position.y = Math.random() * 2e3 - 1e3,
                o.position.z = Math.random() * 500 + 200,
                o.scale.x = o.scale.y = 1.5,
                f.add(o),
                v.push(o);
            for (var s = 0; s < 20; s++) o = new THREE.Particle(i),
                o.position.x = Math.random() * 2e3,
                o.position.y = Math.random() * 2e3 - 1e3,
                o.position.z = Math.random() * 500 + 200,
                o.scale.x = o.scale.y = 1.5,
                f.add(o),
                v.push(o)

            function T(e, t) {
                return Math.random() * (t - e) + e
            }
            function N(e, t, n) {
                var t = t || 0,
                    n = n || 1;
                return 1 / (Math.sqrt(n) * Math.sqrt(2 * Math.PI)) * Math.pow(Math.E, -(e * e + 0 - t) / (2 * n))
            }
        }
    
        var createAllChart = function(){
            
            // 告警类别
            $.ajax({
                url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
                //url:'alarm_warning_module.txt',
                type: "post",
                data: {query_condition:'warning_module'},
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200){
                        createAlarmType(ret.msg);
                    }
                }
            })
            // 告警检测器TOP10
            $.ajax({
                url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
                // url:'alarm_device.txt',
                type: "post",
                data:{query_condition:'device_id',num:10},
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200){
                        createAlarmUnit(ret.msg);
                    }
                }
            })
            // 告警级别
            $.ajax({
                url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
                //url:'alarm_risk.txt',
                type: "post",
                data:{query_condition:'risk'},
                success:function(data) {
                    var ret = JSON.parse(data);
                    createAlarmLevel(ret.msg);
                }
            })

            // 任务组告警
            $.ajax({
                url: "/ajax_action_detector.php?uu=alarm.warning_type_histogram",
                //url:'alarm_task.txt',
                type: "post",
                data:{query_condition:'group_id'},
                success:function(data) {
                    var ret = JSON.parse(data);
                    createTaskGroup(ret.msg);
                }
            })
            
            
            // 告警态势
            $.ajax({
                url: "/ajax_action_detector.php?uu=alarm.newly_trend",
                //url:"alarm_trend.txt",
                type: "post",
                data: {days:30},
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200){
                        createAlarmTrend(ret.msg);
                    }
                }
            })

            // 检测器使用状态
            $.ajax({
                url: "/ajax_action_detector.php?uu=detector.statistic_status",//这里的url暂时没有
                // url:"alarm_device_status.txt",
                type: "post",
                data: {days:30},
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200){
                        createDeviceStatus(ret.msg);
                        for(i=0;i<ret.msg.length;i++){
                            if(ret.msg[i].status == "禁用"){
                                $("#bad-detector").text(ret.msg[i].amount)
                            }
                            if(ret.msg[i].status == "注册待审核"){
                                $("#detector-audit-num").text(ret.msg[i].amount)
                            }
                        }
                    }
                }
            })

            // 统计
            //①告警数量
            $.ajax({
                url: "/ajax_action_detector.php?uu=alarm.count",
                type: "post",
                data: null,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200)
                        ret = ret["msg"]["count"]
                    else {
                        ret = 0;
                    }
                    $("#alarm-num").text(ret);
                }
            })
            // 今日新增
            $.ajax({
                url: "/ajax_action_detector.php?uu=alarm.count",
                type: "post",
                data: {time_min:new Date().toLocaleDateString().replace(/\//g,'-')},
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200)
                        ret = ret["msg"]["count"]
                    else {
                        ret = 0;
                    }
                    $("#today-alarm-num").text(ret);
                }
            })

            // 检测器总数
            $.ajax({
                url: "/ajax_action_detector.php?uu=detector.count",
                type: "post",
                data: null,
                success:function(data) {
                    var ret = JSON.parse(data);
                    if (ret["code"] == 200)
                        ret = ret["msg"]["count"]
                    else {
                        ret = 0;
                    }
                    $("#detector-num").text(ret);
                }
            })

            //策略数目
            $.ajax({
                url: "/ajax_action_detector.php?uu=rule.count_all",
                type: "post",
                data: null,
                success:function(data) {
                    var ret = JSON.parse(data);
                    console.log(ret)
                    $("#class-num").text(ret.msg.class);
                    $("#rule-num").text(ret.msg.count);
                }
            })
        }

	$(function() {
		buildFrame("summary");
        
        $("#map-div").height($(window).height()-50);
        window.addEventListener('resize',function(){
            $("#map-div").height($(window).height()-50);
        })
        createCanvas();
        createAllChart(); //创建所有图表
        
		//$('.summary-copyright').html(COPYRIGHT);
	});

// 图表自适应
var echartsResize = function(chart){
    window.addEventListener('resize',function(){
        chart.resize();
    })
}