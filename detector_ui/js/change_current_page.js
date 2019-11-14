/**
 * Created by wangwenan on 2016/7/19.
 */

var p_size = 10;
var current_page;
var total_page;
var length = 3;    //可见页码数
var old_select_index = -1;
function initCurrentPage(total, page) {
    current_page = page;
    total_page = total;
    if (total < page) {
        console.log("当前页数大于总页数！");
        retrun;
    }
    switch (total) {
        case 1:
            $('.pagination').find('li:eq(3)').remove();
            $('.pagination').find('li:eq(3)').remove();
            break;
        case 2:
            $('.pagination').find('li:eq(4)').remove();
            break;
        default:
            break;
    }
    var num;
    var index;
    if (total < 3) {
        length = total;
    }
    if (page == 1) {   //当前页为第一页
        jumpToHead();
    } else if (page == total) {   //当前页为最后一页
        jumpToTail();
    } else {    //当前页为中间一页，并且total>=3
        old_select_index = 3;
        $('.pagination li:eq(3)>a').addClass("active");
        num = page - 1;
        for (var i = 2; i < 5; i++) {
            $('.pagination li:eq(' + i + ')>a').text(num++);
        }
    }
}

function jumpToHead() {
    alert("jumpTohead--->page:" + current_page + " index:" + old_select_index + " total:" + total_page);
    old_select_index = 2;
    $('.pagination li:eq(2)>a').addClass("active");
    addHeadDisabled();
    var num = 1;
    var index;
    for (var i = 0; i < length; i++) {
        index = 2 + i;
        $('.pagination li:eq(' + index + ')>a').text(num++);
    }
}

function jumpToTail() {
    alert("jumpToTail--->page:" + current_page + " index:" + old_select_index + " total:" + total_page);
    var selected_index = 2 + length - 1;
    old_select_index = selected_index;
    $('.pagination li:eq(' + selected_index + ')>a').addClass("active");
    addTailDisabled();
    var num = total_page;
    var index;
    for (var i = 0; i < length; i++) {
        index = 1 + length - i;
        $('.pagination li:eq(' + index + ')>a').text(num--);
    }
}

function jumpToHeadOrTail(tag) {  //tag:1->前跳, 2->后跳
    switch (tag) {
        case 1:
            if (current_page == 1) return;
            $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
            jumpToHead();
            removeTailDisabled();
            current_page = 1;
            break;
        case 2:
            if (current_page == total_page) return;
            $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
            jumpToTail();
            removeHeadDisabled();
            current_page = total_page;
            break;
        default:
            break;
    }
}

function addHeadDisabled() {
    $('.pagination').find('li:eq(0)').addClass("disabled");
    //$('.pagination').find('li:eq(0)').unbind("click", jumpToHeadOrTail);
    $('.pagination').find('li:eq(1)').addClass("disabled");
    //$('.pagination').find('li:eq(1)').unbind("click", jumpOnePage);
}
function addTailDisabled() {
    $('.pagination').find('li:last').addClass("disabled");
    //$('.pagination').find('li:last').unbind("click", jumpToHeadOrTail);
    $('.pagination').find('li:nth-last-child(2)').addClass("disabled");
    //$('.pagination').find('li:nth-last-child(2)').unbind("click", jumpOnePage);
}
function removeTailDisabled() {
    $('.pagination').find('li:last').removeClass("disabled");
    //$('.pagination').find('li:last').click(function () {
    //    jumpToHeadOrTail(2);
    //});
    $('.pagination').find('li:nth-last-child(2)').removeClass("disabled");
    //$('.pagination').find('li:nth-last-child(2)').click(function () {
    //    jumpOnePage(2);
    //});
}
function removeHeadDisabled() {
    $('.pagination').find('li:eq(0)').removeClass("disabled");
    //$('.pagination').find('li:eq(0)').click(function () {
    //    jumpToHeadOrTail(1);
    //});
    $('.pagination').find('li:eq(1)').removeClass("disabled");
    //$('.pagination').find('li:eq(1)').click(function () {
    //    jumpOnePage(1);
    //});
}
function jumpOnePage(tag) {    //tag:1->previous, 2->next
    alert("jumpOnePage:--->page:" + current_page + " index:" + old_select_index + " total:" + total_page);
    switch (tag) {
        case 1:
            if (current_page == 1) return;
            if (current_page == 2) { //当前为第二页
                $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
                var selected_index = --old_select_index;
                $('.pagination li:eq(' + selected_index + ')>a').addClass("active");
                addHeadDisabled();
                if (current_page-- == total_page) {
                    removeTailDisabled();
                }
                return;
            }
            if (old_select_index == 4) {          //当前页为可见页的最右边页
                $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
                var selected_index = --old_select_index;
                $('.pagination li:eq(' + selected_index + ')>a').addClass("active");
                removeTailDisabled();
            }
            var num = current_page - 2;
            var index;
            for (var i = 0; i < length; i++) {
                index = 2 + i;
                $('.pagination li:eq(' + index + ')>a').text(num++);
            }
            current_page--;
            break;
        case 2:
            if (current_page == total_page) return;
            if (current_page == total_page - 1) {
                $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
                var selected_index = ++old_select_index;
                $('.pagination li:eq(' + selected_index + ')>a').addClass("active");
                addTailDisabled();
                if (current_page++ == 1) {
                    removeHeadDisabled();
                }
                return;
            }
            if (old_select_index == 2) {          //当前页为可见页的最左边页
                $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
                var selected_index = ++old_select_index;
                $('.pagination li:eq(' + selected_index + ')>a').addClass("active");
                removeHeadDisabled();
            }
            var num = current_page + 2;
            var index;
            for (var i = 0; i < length; i++) {
                index = 1 + length - i;
                $('.pagination li:eq(' + index + ')>a').text(num--);
            }
            current_page++;
            break;
        default:
            break;
    }
}

function selectOtherPage(obj) {
    alert("selectPage--->current_page:" + current_page + " current_index:" + old_select_index + " total_page:" + total_page);
    var page = $(obj).find('a').text();
    var index = $(obj).prevAll().length;
    if (page == 1) {
        $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
        $('.pagination li:eq(' + index + ')>a').addClass("active");
        jumpToHead();
    }
    else if (page == total_page) {
        $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
        $('.pagination li:eq(' + index + ')>a').addClass("active");
        jumpToTail();
    }
    else if ((page >= 2 && index == 2) || (page <= total_page - 1 && index == 4)) {  //当前可见页码有三条并且选中页码在中间
        var num;
        num = page - 1;
        var index = 2;
        for (var i = 0; i < length; i++) {
            $('.pagination li:eq(' + index + ')>a').text(num++);
            index++;
        }
        if(Math.abs(index - old_select_index) == 2) {
            $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
            $('.pagination li:eq(3)>a').addClass("active");
            old_select_index = 3;
        }
    } else {
        $('.pagination li:eq(' + old_select_index + ')>a').removeClass("active");
        $('.pagination li:eq(' + index + ')>a').addClass("active");
        if (current_page == 1) {
            removeHeadDisabled();
        }
        else if (current_page == total_page) {
            removeTailDisabled();
        }
        old_select_index = index;
    }
    current_page = page;
}

