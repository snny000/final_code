var helper_ele = "&nbsp;<i class=\"fa fa-question-circle hint-helper\" onmouseenter=\"showHint(this);\" onmouseleave=\"hideHint(this);\" style=\"color: darkgrey; \"></i>";


var tcp_connect_helper_text = "TCP(建立)连接数";
var memory_helper_text = " 内存使用情况(使用/总量)";
var net_traffic_help_text = "网卡流量<br/>实时和当天总流量(入->出)";
var request_times_help_text = "请求次数(入->出)<br/>(异常/失败/慢)";
var node_queue_help_text = "节点消息队列<br/>(待处理->消息优先级:正常/高/低)<br/>(待发送->消息优先级:正常/高/低)";

var longTextHintHelper = {
    self_textarea: "",

    init: function () {
        console.log("helper.init()");
        this.self_textarea = $("<span class=\"hidden\" style=\"z-index: 100; width: fit-content; height: fit-content; padding: 8px; border: 4px solid lightgray; background-color: white; border-radius: 4px;\">文字解释</span>");
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
        console.log("HintHelper：", self_x, self_y, _hint_text);
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




function checkNodeQueue(obj) {
    if(parseInt(obj["task_local_count"]) > 200 || parseInt(obj["task_local_hi_count"]) > 200 || parseInt(obj["task_local_lo_count"]) > 200
        || parseInt(obj["task_send_count"]) > 200 || parseInt(obj["task_send_hi_count"]) > 200 || parseInt(obj["task_send_lo_count"]) > 200) {
        return true;
    }
    else {
        return false;
    }
}

//str: format('[float]G: [float]G')
function calDiskUseRatio(str) {
    if(str == null || str.length == 0) {
        return 0.0;
    } else {
        var used = str.substring(0, str.indexOf("G"));
        var total_str = str.substring(str.indexOf(":") + 2);
        var total = total_str.substring(0, total_str.length - 1);
//            console.log(used + " " + total_str + " " + total);
        return parseFloat(used) / parseFloat(total);
    }
}


function formatTime2BriefText(str_time, allow_time_error_minute) {
    var pre_date = new Date(str_time);  //开始时间
    var curr_date = new Date();    //结束时间
    var diff_stamp = curr_date.getTime() - pre_date.getTime();
    if(diff_stamp < 0) {
        var t = Math.ceil(diff_stamp * -1 / (60 * 1000));
        if(t > allow_time_error_minute) {
            return "时间错误";
        } else {
            return "刚刚";
        }
    }

    var time_per_unit_diffs = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]];
    for(var i = time_per_unit_diffs.length - 1; i >= 0; i--) {
        var diff = 0;
        if(i < time_per_unit_diffs.length - 2 && time_per_unit_diffs[i+1][1] < 0) {
            diff -= 1;
        }
        switch (i) {
            case 5:
                diff += curr_date.getSeconds() - pre_date.getSeconds();
                time_per_unit_diffs[i][1] = diff >= 0 ? 0 : -1;
                time_per_unit_diffs[i][0] = diff >= 0 ? diff : diff + 60;
                break;
            case 4:
                diff += curr_date.getMinutes() - pre_date.getMinutes();
                time_per_unit_diffs[i][1] = diff >= 0 ? 0 : -1;
                time_per_unit_diffs[i][0] = diff >= 0 ? diff : diff + 60;
                break;
            case 3:
                diff += curr_date.getHours() - pre_date.getHours();
                time_per_unit_diffs[i][1] = diff >= 0 ? 0 : -1;
                time_per_unit_diffs[i][0] = diff >= 0 ? diff : diff + 24;
                break;
            case 2:
                diff += curr_date.getDate() - pre_date.getDate();
                time_per_unit_diffs[i][1] = diff >= 0 ? 0 : -1;
                time_per_unit_diffs[i][0] = diff >= 0 ? diff : diff + 30;
                break;
            case 1:
                diff += curr_date.getMonth() - pre_date.getMonth();
                time_per_unit_diffs[i][1] = diff >= 0 ? 0 : -1;
                time_per_unit_diffs[i][0] = diff >= 0 ? diff : diff + 12;
                break;
            case 0:
                diff += curr_date.getFullYear() - pre_date.getFullYear();
                time_per_unit_diffs[i][0] = diff;
                break;
            default: break;
        }
    }

    if(time_per_unit_diffs[0][0] < 0) return "时间错误";
    for(var j = 0; j < time_per_unit_diffs.length; j++) {
//            console.log("i=" + j + ": " + time_per_unit_diffs[j][0]);
        if (time_per_unit_diffs[j][0] > 0) {
            switch (j) {
                case 0:
                    return time_per_unit_diffs[j][0] + "年前";
                case 1:
                    return time_per_unit_diffs[j][0] + "个月前";
                case 2:
                    return time_per_unit_diffs[j][0] + "天前";
                case 3:
                    return time_per_unit_diffs[j][0] + "小时前";
                case 4:
                    return time_per_unit_diffs[j][0] + "分钟前";
                case 5:
                    return time_per_unit_diffs[j][0] + "秒前";
            }
        }
    }
}