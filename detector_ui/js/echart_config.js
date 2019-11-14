/**
 * Created by wangwenan on 2017/6/12.
 */

// var default_chart_color = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3'];
var default_chart_color = ["#3693CF", "#CF233C", '#91c7ae', '#2f4554'];
var default_chart_padding = [[15, 0, 0, 0], [0, 0, 15, 0]];
var yAxis_padding = [0, 5, 10, 15];

//Result1=[{name:XXX,value:XXX},{name:XXX,value:XXX}, ...]
//Result2=[{name:XXX,group:XXX,value:XXX},{name:XXX,group:XXX,value:XXX}, ...]
var chartDataFormate = {

    formateNoGroupData: function (data) {//data的格式如上的Result1，这种格式的数据，多用于饼图、单一的柱形图的数据源
        var categories = [];
        var datas = [];
        for (var i = 0; i < data.length; i++) {
            categories.push(data[i].name || "");
            datas.push({name: data[i].name, value: data[i].value || 0});
        }
        return {category: categories, data: datas};
    },

    formateGroupData: function (data, type, is_stack, _markline) {//data的格式如上的Result2，type为要渲染的图表类型：可以为line，bar，is_stack表示为是否是堆积图，这种格式的数据多用于展示多条折线图、分组的柱图
        var chart_type = 'line';
        if (type)
            chart_type = type || 'line';
        var xAxis = [];
        var group = [];
        var series = [];
        for (var i = 0; i < data.length; i++) {
            if (!this.contains(data[i]["name"], xAxis))
                xAxis.push(data[i]["name"]);
            if (!this.contains(data[i]["group"], group))
                group.push(data[i]["group"]);
        }

        for (var i = 0; i < group.length; i++) {
            var temp = [];
            for (var j = 0; j < data.length; j++) {
                if (group[i] == data[j].group) {
                    if (chart_type == "map")
                        temp.push({name: data[j].name, value: data[i].value});
                    else
                        temp.push(data[j].value);

                }
            }
            switch (chart_type) {
                case 'bar':
                    var series_temp = {
                        name: group[i],
                        data: temp,
                        type: chart_type,
                    };
                    if (is_stack)
                        series_temp = $.extend({}, {stack: 'stack'}, series_temp);
                    break;
                case 'map':
                    var series_temp = {
                        name: group[i], type: chart_type, mapType: 'china', selectedMode: 'single',
                        itemStyle: {
                            normal: {label: {show: true}},
                            emphasis: {label: {show: true}}
                        },
                        data: temp
                    };
                    break;
                case 'line':
                    console.log("#########################################");
                    var series_temp = {
                        name: group[i],
                        data: temp,
                        type: chart_type,
                        smooth: true,
                        symbolSize: 12,
                        lineStyle: {
                            normal: {
                                width: 4,
                                color: default_chart_color[i]
                            }
                        },
                        label: {
                            normal: {
                                show: true,
                                color: default_chart_color[i],
                                textBorderColor: '#FFF',
                                textBorderWidth: 2,
                                padding: default_chart_padding[i]
                            }
                        },
                        markPoint: {
                            symbolSize: 15,
                            symbolOffset: [0, '10%'],
                            label: {
                                normal: {
                                    // formatter: '{a|{a}\n}{b|{b} }{c|{c}}',
                                    formatter: '{b|{b} }{c|{c}}',
                                    backgroundColor: 'rgb(242,242,242)',
                                    borderColor: default_chart_color[i],
                                    borderWidth: 3,
                                    borderRadius: 4,
                                    padding: [4, 10],
                                    lineHeight: 25,
                                    // shadowBlur: 5,
                                    // shadowColor: '#000',
                                    // shadowOffsetX: 0,
                                    // shadowOffsetY: 1,
                                    position: 'right',
                                    distance: 20,
                                    rich: {
                                        // a: {
                                        //     align: 'center',
                                        //     color: default_chart_color[i],
                                        //     fontSize: 18,
                                        //     textShadowBlur: 2,
                                        //     textShadowColor: '#FFF',
                                        //     textShadowOffsetX: 0,
                                        //     textShadowOffsetY: 1,
                                        //     textBorderColor: '#FFF',
                                        //     textBorderWidth: 2
                                        // },
                                        b: {
                                            color: default_chart_color[i]
                                        },
                                        c: {
                                            color: '#ff8811',
                                            textBorderColor: '#FFF',
                                            textBorderWidth: 1,
                                            fontSize: 22
                                        }
                                    }
                                }
                            },
                            data: [
                                {type: 'max', name: '最大值: '},
                                {type: 'min', name: '最小值: '}
                            ]
                        }
                    };
                    if (is_stack)
                        series_temp = $.extend({}, {stack: 'stack'}, series_temp);
                    break;
                default:
                    var series_temp = {name: group[i], data: temp, type: chart_type};
            }
            series.push(series_temp);
        }
        if(_markline && _markline.length > 0) {
            //var mark_data = [];
            //for(var i = 0; i < parseInt(data.length/group.length); i++) {
            //    mark_data.push(_markline);
            //}
            //group.push('临界值');
            //var series_temp = {name: '临界值', data: mark_data, type: 'line', markLine: {data: [{type: 'average', name: '平均值'}]}};
            //series.push(series_temp);
            var m_data = [];
            for(var j = 0; j < _markline.length; j++) {
                if(_markline[j] > 0) {
                    var tmp = {
                        yAxis: _markline[j],
                        name: '临界值' + j
                    };
                    m_data.push(tmp);
                }
            }
            var mark_line = {
                markLine: {
                    data: m_data
                }
            };
            var v_pieces = [];
            if(_markline[0] > 0) {
                v_pieces.push({
                    lt: _markline[0],
                    color: '#F00',
                    label: '<' + _markline[0] + '：指标不合格'
                });
                v_pieces.push({
                    gte: _markline[0],
                    lte: _markline[1],
                    //color: default_chart_color[Math.ceil((11*Math.random()) - 1)]
                });
                v_pieces.push({
                    gt: _markline[1],
                    color: '#F00',
                    label: '>' + _markline[1] + '：指标不合格'
                });
            }
            else {
                v_pieces.push({
                    lte: _markline[1]
                    //color: default_chart_color[Math.ceil((11*Math.random()) - 1)]
                });
                v_pieces.push({
                    gt: _markline[1],
                    color: '#F00',
                    label: '>' + _markline[1] + '：指标不合格'
                });
            }
            var visual_Map =  {
                show: true,
                top: 10,
                right: 10,
                type: 'piecewise',
                pieces: [{
                    lt: _markline[0],
                    color: '#F00',
                    label: '<' + _markline[0] + '：指标不合格'
                },{
                    gte: _markline[0],
                    lte: _markline[1],
                    label: _markline[0] + " - " + _markline[1],
                    color: "#003bb3"
                    //color: default_chart_color[Math.ceil((11*Math.random()) - 1)]
                }, {
                    gt: _markline[1],
                    color: '#F00',
                    label: '>' + _markline[1] + '：指标不合格'
                }],
                outOfRange: {
                    color: '#999'
                }
            };

            series[0] = $.extend({}, series[0], mark_line);
            return {category: group, xAxis: xAxis, _visualMap: visual_Map, series: series};
        }
        else {
            return {category: group, xAxis: xAxis, series: series};
        }

    },

    formateMixData: function (data, type, y_unit, _markline) {//data的格式如上的Result2，type为要渲染的图表类型：可以为line，bar，is_stack表示为是否是堆积图，这种格式的数据多用于展示多条折线图、分组的柱图
        var chart_type = 'line';
        var xAxis = [];
        var yAxis = [];
        var group = [];
        var series = [];
        for (var i = 0; i < data.length; i++) {
            if (!this.contains(data[i]["name"], xAxis))
                xAxis.push(data[i]["name"]);
            if (!this.contains(data[i]["group"], group))
                group.push(data[i]["group"]);
        }

        for (var i = 0; i < group.length; i++) {
            var temp = [];
            var y_tmp = {
                name: y_unit[i] || '',
                type: 'value',
                splitArea: { show: true },
            };
            yAxis.push(y_tmp);
            for (var j = 0; j < data.length; j++) {
                if (group[i] == data[j].group) {
                    temp.push(data[j].value);
                }
            }

            var series_temp = {
                name: group[i],
                xAxisIndex: 0,
                yAxisIndex: i,
                data: temp,
                type: type[i],
                smooth: true,
                symbolSize: 12,
                lineStyle: {
                    normal: {
                        width: 4,
                        color: default_chart_color[i]
                    }
                },
                label: {
                    normal: {
                        show: true,
                        color: default_chart_color[i],
                        textBorderColor: '#FFF',
                        textBorderWidth: 2,
                        padding: default_chart_padding[i]
                    }
                },
                markPoint: {
                    symbolSize: 15,
                    symbolOffset: [0, '10%'],
                    label: {
                        normal: {
                            formatter: '{b|{b} }{c|{c}}',
                            backgroundColor: 'rgb(242,242,242)',
                            borderColor: default_chart_color[i],
                            borderWidth: 3,
                            borderRadius: 4,
                            padding: [4, 10],
                            lineHeight: 25,
                            // shadowBlur: 5,
                            // shadowColor: '#000',
                            // shadowOffsetX: 0,
                            // shadowOffsetY: 1,
                            position: 'right',
                            distance: 20,
                            rich: {
                                b: {
                                    color: default_chart_color[i]
                                },
                                c: {
                                    color: '#ff8811',
                                    textBorderColor: '#FFF',
                                    textBorderWidth: 1,
                                    fontSize: 22
                                }
                            }
                        }
                    },
                    data: [
                        {type: 'max', name: '最大值: '},
                        {type: 'min', name: '最小值: '}
                    ]
                }
            };

            series.push(series_temp);
        }
        for(var i = 0; _markline && i < _markline.length; i++) {
            var mark_line = {
                markLine: {
                    data: [{
                        yAxis: _markline[i],
                        name: '临界值'
                    }]
                }
            };
            series[i] = $.extend({}, series[i], mark_line);
        }
        return {category: group, xAxis: xAxis, yAxis: yAxis, series: series};
    },

    contains: function (obj, coll) {
        for(var index in coll) {
            if(obj === coll[index]) {
                return true;
            }
        }
        return false;
    }
};

var chartOptionTemplates = {
    commonOption: {//通用的图表基本配置
        backgroundColor: "#FFFFFF",
        tooltip: {
            trigger: 'item'//tooltip触发方式:axis以X轴线触发,item以每一个数据项触发
        },
        grid: {
            x: 20,
            y: 10,
            x2: 20,
            y2: 10
        },
        color: default_chart_color,
        toolbox: {
            top: 25,
            right:10,
            orient: 'vertical',
            show: true,
            feature: {
                // dataZoom: {
                //     yAxisIndex: 'none'
                // },
                // dataView: {readOnly: false},
                magicType: {type: ['line', 'bar']},
                // restore: {},
                // saveAsImage: {}
            }
        },
    },
    commonLineOption: {//通用的折线图表的基本配置
        backgroundColor: "#FFFFFF",
        // tooltip: {
        //     trigger: 'axis'
        // },
        grid: {
            x: 50,
            y: 50,
            x2: 75,
            y2: 40
        },
        color: default_chart_color,
        /*toolbox: {
            top: 15,
            // left: 5,
            right:5,
            orient: 'vertical',
            show: false,
            feature: {
                // dataZoom: {
                //     yAxisIndex: 'none'
                // },
                // dataView: { readOnly: false }, //数据预览
                magicType: {type: ['line', 'bar']},
                // restore: {},
                // saveAsImage: {}
            }
        },*/
        // dataZoom: [
        //     {
        //         show: false,
        //         type: 'slider',
        //         xAxisIndex: 0
        //     },
        //     {
        //         show: false,
        //         type: 'inside',
        //         xAxisIndex: 0
        //     },
        //     {
        //         show: false,
        //         type: 'slider',
        //         yAxisIndex: 0
        //     },
        //     {
        //         show: false,
        //         type: 'inside',
        //         yAxisIndex: 0
        //     }
        // ],
    },

    pie: function (data, name) {//data:数据格式：{name：xxx,value:xxx}...
        var pie_datas = chartDataFormate.formateNoGroupData(data);
        var option = {
            tooltip: {
                trigger: 'item',
                formatter: '{b} : {c} ({d}/%)',
                show: true
            },
            legend: {
                top: 15,
                orient: 'vertical',
                x: 'left',
                data: name
            },
            series: [
                {
                    name: name || "",
                    type: 'pie',
                    radius: '65%',
                    center: ['50%', '50%'],
                    data: pie_datas.data
                }
            ]
        };
        return $.extend({}, chartOptionTemplates.commonOption, option);
    },

    lines: function (title, data, name, is_stack, _markline) { //data:数据格式：{name：xxx,group:xxx,value:xxx}...
        var stackline_datas = chartDataFormate.formateGroupData(data, 'line', is_stack, _markline);
        var option = {
            title: {
                text: title,
                textStyle:{
                    show: false,
                    color:"#3693CF",
                    fontSize:18
                }

            },
            legend: {
                top: 15,
                data: stackline_datas.category,
                // textStyle: {    //图例文字的样式
                //     color: default_chart_color,
                //     fontSize:14
                // }
            },
            xAxis: [{
                type: 'category', //X轴均为category，Y轴均为value
                data: stackline_datas.xAxis,
                boundaryGap: [0.2, 0.2],//数值轴两端的空白策略
                axisLabel: {
                    show: true,
                    interval: 'auto',
                    rotate: 0,
                    margin: 8
                }
            }],
            yAxis: [{
                name: name || '',
                type: 'value',
                splitArea: { show: true },
                boundaryGap: [0.2, 0.2],//数值轴两端的空白策略
            }],
            series: stackline_datas.series
        };
        if(stackline_datas._visualMap) {
            return $.extend({}, chartOptionTemplates.commonLineOption, {visualMap: stackline_datas._visualMap}, option);
        }
        else {
            return $.extend({}, chartOptionTemplates.commonLineOption, option);
        }
    },

    bars: function (title, data, name, is_stack, _markline) {//data:数据格式：{name：xxx,group:xxx,value:xxx}...
        var bars_dates = chartDataFormate.formateGroupData(data, 'bar', is_stack, _markline);
        var option = {
            title: {
                text: title
            },
            legend: {
                top: 15,
                data: bars_dates.category
            },
            xAxis: [{
                type: 'category',
                data: bars_dates.xAxis,
                axisLabel: {
                    show: true,
                    interval: 'auto',
                    rotate: 0,
                    margin: 8
                }

            }],
            yAxis: [{
                type: 'value',
                name: name || '',
                splitArea: { show: true }
            }],
            series: bars_dates.series
        };
        if(bars_dates._visualMap) {
            return $.extend({}, chartOptionTemplates.commonLineOption, {visualMap: bars_dates._visualMap}, option);
        }
        else {
            return $.extend({}, chartOptionTemplates.commonLineOption, option);
        }
    },

    //其他的图表配置，如柱图+折线
    /**
     * generate mix(line line , bar bar, bar line) chart(which hava different yAxis) option
     * @param title: chart title text
     * @param data: [{name: time, value:..., group: meaning of variable}, {...}] data of xAxis and series
     * @param l_type: [] charts type
     * @param l_name: [] chart yAxis name
     * @param _markline: [] markLine
     */
    mix: function(title, data, l_type, l_name, _markline) {
        var mix_datas = chartDataFormate.formateMixData(data, l_type, l_name, _markline);
        var option = {
            title: {
                text: title,
                textStyle:{
                    show: false,
                    color:"#3693CF",
                    fontSize:18
                }

            },
            legend: {
                top: 15,
                data: mix_datas.category
                // textStyle: {    //图例文字的样式
                //     color: default_chart_color,
                //     fontSize:14
                // }
            },
            xAxis: [{
                type: 'category', //X轴均为category，Y轴均为value
                data: mix_datas.xAxis,
                boundaryGap: [0.2, 0.2],//数值轴两端的空白策略
                axisLabel: {
                    show: true,
                    interval: 'auto',
                    rotate: 0,
                    margin: 8
                }
            }],
            yAxis: mix_datas.yAxis,
            series: mix_datas.series
        };
        return $.extend({}, chartOptionTemplates.commonLineOption, option);
    }
}

var ChartInit = {
    addChartLoading:　function(charts) {
        for(var i = 0; i < charts.length; i++) {
            charts[i].showLoading();
        }
    },
    hideChartLoading: function(charts) {
        for(var i = 0; i < charts.length; i++) {
            charts[i].hideLoading();
        }
    },
    init: function(charts) {
        this.addChartLoading(charts);
    }
}



