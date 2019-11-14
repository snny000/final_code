/**
 * Created by Fernando on 2016/7/7.
 */

/////////////////Global variables//////////
var ddosValues;
var ORDER_ID;
var ISP_LIST;//[{"type":1,id:11},{"type":2,id:23}]
/////////////////Global variables//////////
function displayConfig(type, step) {

    var product_arr = getHandlerMap(type);
    var curFirstPro = product_arr[0];
    if (curFirstPro == "ddos") {
        $.ajax({
            url: "service/get.ddos.orderid.php",
            type: "get",
            success: function (data) {
                var ret = JSON.parse(data);
                ORDER_ID = ret;
            }
        });
    } else if (curFirstPro == "waf") {

    } else if (curFirstPro == "cdn") {

    }

    /*画出对应的状态栏目*/
    $('#wizardDiv').html(wizardStatus(type, step));
    //ddos      -2
    //waf       -2
    //cdn       -3
    //finish    -1

    var stepsAll = product_arr.length;
    var content = new Array();
    var isContainCDN = false;
    for (var i = 0; i < stepsAll; i++) {
        if (product_arr[i] == "ddos") {
            content[i] = getConfigDDos();
        } else if (product_arr[i] == "finish") {
            content[i] = getConfigFinish();
        } else if (product_arr[i] == "cdn") {
            content[i] = getConfigCDN();
            isContainCDN = true;
        } else if (product_arr[i] == "waf") {
            content[i] = getConfigWaf();
        }
    }
    var result = content.join(" ");
    content = null;
    $("#tbl_config_all>tbody").append(result);

    if (isContainCDN) {
        $('#_ModalContent').html(getCdnModal());
    }
    $('input[data-size=mini]').bootstrapToggle();
    var curProduct = product_arr[step];
    //$("#tbl_config_all>tbody>tr").addClass("hidden");
    $("#tbl_config_all>tbody>tr[id='" + curProduct + "1']").removeClass("hidden");

    if (step == 0) {
        $('#btn_previous').addClass("hidden");
        $('#btn_next').click(function () {
            btn_next(product_arr, step, 1, type)
        });
    } else if ((step + 1) == stepsAll) {
        $('#btn_next').addClass("hidden");
        $('#btn_previous').click(function () {
            btn_previous(product_arr, step, 1, type);
        });
        $('#btn_save').removeClass("hidden");
        $('#btn_submit').removeClass("hidden");
    } else {
        $('#btn_next').click(function () {
            btn_next(product_arr, step, 1, type)
        });
        $('#btn_previous').click(function () {
            btn_previous(product_arr, step, 1, type);
        });
    }
}
function btn_next(product_arr, step, prestage, type) {

    var curStep = step;
    var curProduct = product_arr[step];
    var curStage = prestage + 1;
    var allSteps = product_arr.length;
    var allStages = getAllStages(curProduct);


    if (curStage > allStages) {
        curStep++;
        curProduct = product_arr[curStep];
        curStage = 1;

        if (curProduct == "ddos") {
            $.ajax({
                url: "service/get.ddos.orderid.php",
                type: "get",
                success: function (data) {
                    var ret = JSON.parse(data);
                    ORDER_ID = ret;
                }
            });
        } else if (curProduct == "waf") {

        } else if (curProduct == "cdn") {

        }
    }
    //选择不同页面的校验功能
    if (!changeVerifyEntrance(step, prestage)) return;


    if (curProduct == "ddos" && prestage == 1) {


        for (var item in ddosValues) {
            ddosValues[item].order_id = ORDER_ID;
        }
        $.ajax({
            url: "service/save.ddos.php",
            type: "post",
            data: {ddosValues: ddosValues},
            success: function (data) {
                var ret = JSON.parse(data);
                if (ret["code"] == 0) {
                    //todo
                    ISP_LIST = ret["msg"];
                    successCallBack(product_arr, curProduct, curStep, allSteps, curStage, allStages, type);
                } else {
                    alert(ret["msg"]);
                    return;
                }
            }
        });
    } else if (curProduct == "ddos" && prestage == 2) {

    } else if (curProduct == "waf" && prestage == 1) {

    } else if (curProduct == "waf" && prestage == 2) {

    } else if (curProduct == "cdn" && prestage == 1) {

    } else if (curProduct == "cdn" && prestage == 2) {

    } else if (curProduct == "cdn" && prestage == 3) {

    }

    ///调试用的,
    successCallBack(product_arr, curProduct, curStep, allSteps, curStage, allStages, type);
}
function successCallBack(product_arr, curProduct, curStep, allSteps, curStage, allStages, type) {
    if (curProduct == "ddos" && curStage == 2) {
        initStageOfStep(curStep, curStage);
    }
    $('#btn_next').removeClass("hidden");
    if (curStep == allSteps - 1) {
        $('#btn_next').addClass("hidden");
        $('#btn_save').removeClass("hidden");
        $('#btn_submit').removeClass("hidden");
    } else {

    }
    $('#btn_previous').removeClass("hidden");

    $("#tbl_config_all>tbody>tr").addClass("hidden");
    if (curStage > allStages) {//转到下一个step
        $("#tbl_config_all>tbody>tr[id='" + product_arr[curStep] + curStage + "']").removeClass("hidden");
    } else {
        $("#tbl_config_all>tbody>tr[id='" + curProduct + curStage + "']").removeClass("hidden");
    }
    $('#btn_next').unbind('click');
    $('#btn_next').click(function () {
        btn_next(product_arr, curStep, curStage, type);
    });

    $('#btn_previous').unbind('click');
    $('#btn_previous').click(function () {
        btn_previous(product_arr, curStep, curStage, type);
    });

    $('#wizardDiv').html(wizardStatus(type, curStep));
}


function changeVerifyEntrance(step, stages) {//stage 从1开始，step从0
    switch (step) {
        case 0:           //ddos页面校验
            if (stages == 1) {             //ddos第一页
                if (ddosPage1Verify()) {
                    changeLinkData();
                    $('#btn_proto_forward').unbind();
                    $('#btn_proto_forward').click(function () {
                        btn_proto_add(ddos_link);
                    });
                    $('#btn_website_defend_add').unbind();
                    $('#btn_website_defend_add').click(function () {
                        btn_website_defend_add(ddos_link);
                    });
                    ddosValues = getDDosPage1UpLoadData();
                    return true;
                }
                else return false;
            }
            else {                        //ddos第二页

                if (ddosPage2Verify()) {
                    return true;
                }
                else return true;
            }
            break;
        case 1:           //waf页面校验
            //if (stages == 1) {
            //    if (wafPage1Verify()) {
            //        return true;
            //    }
            //    else {
            //        return false;
            //    }
            //}
            return true;

        case 2:           //cdn页面校验
            //if (stages == 1) {
            //    if (cdnPage1Verify()) {
            //        return true;
            //    }
            //    else {
            //        return false;
            //    }
            //}
            return true;
        default :
            break;
    }
    return true;
}

//ddo verify
function wizardStatus(type, active) {
    var text = "<ul id='wizardStatus'>" +
        "<li><i class='fa fa-users'></i>&nbspDDOS配置</li>" +
        "<li><i class='fa fa-minus-square'></i>&nbspWAF配置</li>" +
        "<li><i class='fa fa-sitemap'></i>&nbspCDN配置</li>" +
        "<li><i class='fa fa-check-circle-o'></i>&nbsp完成</li>" +
        "</ul>"
    var u = $(text);

    var flag;
    switch (type) {
        case 0:
            u.children('li:eq(1),li:eq(2)').remove();
            activeli(u, active);
            flag = 1;
            break;
        case 1:
            u.children('li:eq(0),li:eq(2)').remove();
            activeli(u, active);
            flag = 1;
            break;
        case 2:
            u.children('li:eq(0),li:eq(1)').remove();
            activeli(u, active);
            flag = 1;
            break;
        case 3:
            u.children('li:eq(2)').remove();
            activeli(u, active);
            flag = 2;
            break;
        case 4:
            u.children('li:eq(1)').remove();
            activeli(u, active);
            flag = 2;
            break;
        case 5:
            u.children('li:eq(0)').remove();
            activeli(u, active);
            flag = 2;
            break;
        default:
            activeli(u, active);
            flag = 3;
    }
    //
    //if (flag < active) {
    //    alert("active的个数多于type的个数");
    //}
    return u;
}

/**
 * 设置li的class为current
 * @param u jq对象
 * @param active 前active个li设置为current
 */
function activeli(u, active) {
    switch (active) {
        case 0:
            u.children('li:eq(0)').addClass('current')
            break;
        case 1:
            u.children('li:eq(0),li:eq(1)').addClass('current')
            break;
        case 2:
            u.children('li:eq(0),li:eq(1),li:eq(2)').addClass('current')
            break;
        case 3:
            u.children('li:eq(0),li:eq(1),li:eq(2),li:eq(3)').addClass('current')
            break;
    }
}


function initStageOfStep(step, stage) {
    switch (step) {
        case 0:
            if (stage == 1) {             //ddos第一页

            }
            else if (stage == 2) {                        //ddos第二页
                ddosPage2Validate.init();
                return;
            }
            break;
        case 1:           //waf页面校验


            break;
        case 2:           //cdn页面校验

            break;
        default :
            break;
    }
}

function btn_previous(product_arr, step, prestage, type) {


    var curStep = step;
    var curProduct = product_arr[step];
    var curStage = prestage - 1;
    var allSteps = product_arr.length;

    if (step == allSteps - 1) {
        $('#btn_save').addClass("hidden");
        $('#btn_submit').addClass("hidden");
    }

    var allStages = 0;
    if (curStage == 0) {
        curStep--;
        curProduct = product_arr[curStep];
        allStages = getAllStages(curProduct);
    }
    $('#btn_previous').removeClass("hidden");

    $('#btn_next').removeClass("hidden");
    if (curStep == 0 && curStage == 1) {
        $('#btn_previous').addClass("hidden");
    }

    $("#tbl_config_all>tbody>tr").addClass("hidden");
    if (curStage == 0) {//转到上一个step
        curStage = allStages;
        $("#tbl_config_all>tbody>tr[id='" + product_arr[curStep] + curStage + "']").removeClass("hidden");
    } else {
        $("#tbl_config_all>tbody>tr[id='" + curProduct + curStage + "']").removeClass("hidden");
    }
    $('#btn_next').unbind('click');
    $('#btn_next').click(function () {
        btn_next(product_arr, curStep, curStage, type);
    });

    $('#btn_previous').unbind('click');
    $('#btn_previous').click(function () {
        btn_previous(product_arr, curStep, curStage, type);
    });
    $('#wizardDiv').html(wizardStatus(type, curStep));
}

var range;
function isLoadNoSlider(isContainNoUiSlider) {
    if (!isContainNoUiSlider) {
        return;
    }
    range = document.getElementById('bandwidth-range');

    if (typeof (noUiSlider) == "undefined") {
        return;
    }
    noUiSlider.create(range, {
        start: 0, // Handle start position
        step: 1, // Slider moves in increments of '10'
        //margin: 20, // Handles must be more than '20' apart
        connect: 'lower', // Display a colored bar between the handles
        direction: 'ltr', // Put '0' at the bottom of the slider
        //tooltips: [ true ],
        //orientation: 'vertical', // Orient the slider vertically
        //behaviour: 'tap-drag', // Move handle on tap, bar is draggable
        range: { // Slider can select '0' to '100'
            'min': 0,
            'max': 300
        },
        format: {
            to: function (value) {
                return Math.round(value);
            },
            from: function (value) {
                return value + ".00";
            }
        },
        pips: { // Show a scale with the slider
            mode: 'count',
            values: 6,
            density: 15,
            format: {
                to: function (value) {
                    return value + "Gbps";
                },
                from: function (value) {
                }
            }
        }
    });

    var inputNumber = document.getElementById('input-bandwidth');

    range.noUiSlider.on('update', function (values, handle) {

        var value = values[handle];
        inputNumber.value = value;
    });

    inputNumber.addEventListener('change', function () {
        range.noUiSlider.set(this.value);
    });
}

function config_btn_event() {

    $('button.config-btn').click(function () {
        var index = $(this).prevAll().length;
        if ($(this).hasClass("active")) {
            $(this).removeClass("active");
            ddos_link[index] = false;
        }
        else {
            $(this).addClass("active");
            ddos_link[index] = true;
        }
        console.log("config.js-->" + JSON.stringify(ddos_link));
    });

    $('button.config-times').click(function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
        var index = $(this).prevAll().length;
        for (var i = 0; i < 12; i++) {
            if (i != index) {
                ddos_purchase_time[i] = false;
            }
            else {
                ddos_purchase_time[i] = true;
            }
        }
    });
    $('button.config-btn-band').click(function () {  //waf-defend-ability event
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
        var index = $(this).prevAll().length;
        for (var i = 0; i < 12; i++) {
            if (i != index) {
                waf_defend_ability[i] = false;
            }
            else {
                waf_defend_ability[i] = true;
            }
        }
    });
    $('button.config-btn-business-type').click(function () {   //cdn business event
        var index = $(this).prevAll().length;
        if ($(this).hasClass("active")) {
            $(this).removeClass("active");
            cdn_business_type[index] = false;
        }
        else {
            $(this).addClass("active");
            cdn_business_type[index] = true;
        }
    });
}

function checkLink(obj, product_ISP) {
    var flag = false;
    //alert(JSON.stringify(obj));
    for (var i = 0; i < obj.length; i++) {
        if (obj[i]) {
            flag = true;
            product_ISP = i + 1;
            //alert("==>" + product_ISP);
            //alert("==>" + DDOS_ISP);
        }
    }
    if (!flag) {
        alert("请选择线路种类！");
        return false;
    }
    else {
        return true;
    }
}

function checkPurchaseTime(obj) {
    var flag = false;
    for (var i = 0; i < obj.length; i++) {
        if (obj[i]) {
            flag = true;
        }
    }
    if (!flag) {
        alert("请选择购买时长！");
        return false;
    }
    else {
        return true;
    }
}
function getDDosLinkLi(obj) {
    var html = '';
    if (obj == null) return;
    for (var i = 0; i < obj.length; i++) {
        if (obj[i]) {
            html += '<li onclick=\"selectProtoFwd(this);\">' + genLinkTextByIndex(i) + '</li>';
        }
    }
    return html;
}

function getCheckedLink() {
    if (ddos_link[0]) {
        return '中国电信';
    } else if (ddos_link[1]) {
        return '中国联通';
    } else {
        return '中国移动';
    }
}

