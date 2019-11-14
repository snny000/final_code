/**
 * Created by Fernando on 2016/7/7.
 */

function getHandlerMap(type) {
    var handler_map = [
        ["ddos", "finish"]
        , ["waf", "finish"]
        , ["cdn", "finish"]
        , ["ddos", "waf", "finish"]
        , ["ddos", "cdn", "finish"]
        , ["waf", "cdn", "finish"]
        , ["ddos", "waf", "cdn", "finish"]
    ];
    return handler_map[type];
}
function getPrefix(tag) {
    var tmpId = '';
    if (tag == 1) {//
        tmpId = "_forward";
    } else if (tag == 2) {//
        tmpId = "_defend";
    } else if (tag == 3) {
        tmpId = "_waf";
    } else if (tag == 4) {
        tmpId = "cdn";
    }
    return tmpId;
}

function getAllStages(curProduct) {
    var allStages = 0;
    if (curProduct == "ddos" || curProduct == "waf") {
        allStages = 2;
    } else if (curProduct == "cdn") {
        allStages = 3;
    } else if (curProduct == "finish") {
        allStages = 1;
    }
    return allStages;
}
//ddos1 一级表


function getStrISP2Int(ispStr) {
    if (ispStr == "中国电信") {
        return 1;
    } else if (ispStr == "中国联通") {
        return 2;
    } else if (ispStr == "中国移动") {
        return 3;
    }
}

function getStrPro2Int(proStr) {
    if (proStr == "tcp") {
        return 1;
    } else if (proStr == "udp") {
        return 2;
    }
}

function getStrLoadBalance2Int(loadStr) {
    if (loadStr == "轮询") {
        return 1;
    } else if (loadStr == "一致性哈希") {
        return 2;
    } else if (loadStr == "随机") {
        return 3;
    }
}
function getIntLoadBalance2Str(loadInt) {
    if (loadInt == 1) {
        return "轮询";
    } else if (loadInt == 2) {
        return "一致性哈希";
    } else if (loadInt == 3) {
        return "随机";
    }
}


function selectProtoFwd(obj) {
    var btn = $(obj).parent().parent();
    btn.find("button>span:first").text($(obj).text());
}


function StringBuilder() {
    this.data = Array("");
}
StringBuilder.prototype.append = function () {
    this.data.push(arguments[0]);
    return this;
}
StringBuilder.prototype.toString = function () {
    return this.data.join("");
}

function getStrISP(i) {
    switch (i) {
        case 1:
            return '中国电信';
        case 2:
            return '中国联通';
        case 3:
            return '中国移动';
        case 4:
            return '教育网';
        default :
            return "";
    }
}