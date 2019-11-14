var handler_map = [
					   ["ddos", "finish"]
					  ,["waf", "finish"]
					  ,["cdn", "finish"]
					  ,["ddos", "waf", "finish"]
					  ,["ddos", "cdn", "finish"]
					  ,["waf", "cdn", "finish"]
					  ,["ddos", "waf", "cdn", "finish"]
					  ];

function wizardStatus(type, active)
{
	var text = "<ul id='wizardStatus'>" +
			"<li><i class='fa fa-users'></i>&nbspDDOS配置</li>" +
			"<li><i class='fa fa-minus-square'></i>&nbspWAF配置</li>" +
			"<li><i class='fa fa-sitemap'></i>&nbspCDN配置</li>" +
			"<li><i class='fa fa-check-circle-o'></i>&nbsp完成</li>" +
			"</ul>"
	var u = $(text);

	var flag;
	switch(type){
		case 0:
			u.children('li:eq(1),li:eq(2)').remove();
			activeli(u,active);
			flag = 1;
			break;
		case 1:
			u.children('li:eq(0),li:eq(2)').remove();
			activeli(u,active);
			flag = 1;
			break;
		case 2:
			u.children('li:eq(0),li:eq(1)').remove();
			activeli(u,active);
			flag = 1;
			break;	
		case 3:
			u.children('li:eq(2)').remove();
			activeli(u,active);
			flag = 2;
			break;
		case 4:
			u.children('li:eq(1)').remove();
			activeli(u,active);
			flag = 2;
			break;
		case 5:
			u.children('li:eq(0)').remove();
			activeli(u,active);
			flag = 2;
			break;
		default:
			activeli(u,active);
			flag = 3;
	}
	
	if(flag<active){
		alert("active的个数多于type的个数");
	}
	
    return u;
}

/**
 * 设置li的class为current
 * @param u jq对象
 * @param active 前active个li设置为current
 */
function activeli(u,active){
	switch(active){
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


function buildConfigFrame(type, index){
	var action = handler_map[type][index];
	if(action=="ddos"){
		return "ddos";
	} else if(action=="waf"){
		return "waf";
	} else if(action=="cdn"){
		return "cdn";
	} else if(action=="finish"){
		return "finish";
	} else {
		return "";
	}
}

function registerActions(type,index){
	
}
//$(document).ready(function() {
//	$('body').append(wizardStatus(5,1));
//})