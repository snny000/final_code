# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError, transaction, connection
from django.db.models import Q, F
from django.core.serializers import serialize
from policy_serializers import *
from DetectCenter import sender, common, config, date_util as du, file_util as fu, security_util as su, director_config as dc, queryset_util as qu, print_util as pu
from detector.models import Detector
from director.models import *
from plugin.models import PlugTask

from DetectCenter import common_center_2_director as ccd
from director.detect_center_reg_auth import check_global_director_connection
from director.data_processing import set_policy_job_finished, set_plugin_job_finished, set_command_job_finished

import traceback
import json
import time
import datetime
import os
import copy
import xlrd
import logging
import write_policy_data


rule_models = [
    TrojanRule, AttackRule, MalwareRule, AbnormalRule,
    KeywordRule, EncryptionRule, CompressRule, PictureRule,
    IPListenRule, DNSListenRule, URLListenRule, AccountListenRule,
    NetLogRule, AppBehaviorRule, WebFilterRule, DNSFilterRule,
    IPWhiteListRule, BlockRule
]  # 模型列表

rule_serializers = [
    TrojanRuleSerializer, AttackRuleSerializer, MalwareRuleSerializer,
    AbnormalRuleSerializer, KeywordRuleSerializer, EncryptionRuleSerializer,
    CompressRuleSerializer, PictureRuleSerializer, IPListenRuleSerializer,
    DNSListenRuleSerializer, URLListenRuleSerializer, AccountListenRuleSerializer,
    NetLogRuleSerializer, AppBehaviorRuleSerializer, WebFilterRuleSerializer,
    DNSFilterRuleSerializer, IPWhiteListRuleSerializer, BlockRuleSerializer
]  # 序列化类列表

director_rule_models = [
    DirectorTrojanRule, DirectorAttackRule, DirectorMalwareRule, DirectorAbnormalRule,
    DirectorKeywordRule, DirectorEncryptionRule, DirectorCompressRule, DirectorPictureRule,
    DirectorIPListenRule, DirectorDNSListenRule, DirectorURLListenRule, DirectorAccountListenRule,
    DirectorNetLogRule, DirectorAppBehaviorRule, DirectorWebFilterRule, DirectorDNSFilterRule,
    DirectorIPWhiteListRule, DirectorBlockRule
]  # 模型列表

# rule_type_list = [
#     'rule_trojan_list', 'rule_attack_list', 'rule_malware_list', 'rule_abnormal_list',
#     'rule_keyword_list', 'rule_encryption_list', 'rule_compress_list', 'rule_picture_list',
#     'rule_ip_list', 'rule_domain_list', 'rule_url_list', 'rule_account_list',
#     'rule_netlog_list', 'rule_appbehavior_list', 'rule_webfilter_list', 'rule_dnsfilter_list',
#     'rule_ipwhite_list'
# ]  # Detector model中检测器对应的规则列表


# **************************************** 处理界面请求 ****************************************


task_is_valid_map = {0: '已忽略', 1: '任务执行中', 2: '任务执行成功', 3: '任务执行失败', 4: '任务错误'}   # 现在默认任务随心跳下发后就当成任务执行成功，后续可能根据检测器的反馈确定实际执行成功状态

operate_map = {'add': 0, 'del': 1, 'change': 2, 'group': 3, '': 4}


################任务组相关#################
# 批量修改策略所属任务组，如果置为0：表示没有所属任务组
# 请求参数：policy_type
#         group_id
#         rule_id
def rule_update_group(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        policy_type = common.check_request_int_field(request_data, 'policy_type')
        if isinstance(policy_type, Response):
            return policy_type

        group_id = request_data.get('group_id')
        if group_id is not None:
            group_id = int(group_id)
        else:
            group_id = 0

        rule_list = common.check_request_list_or_dict_field(request_data, 'rule_id')   # rule_id列表
        if isinstance(rule_list, Response):
            return rule_list

        # rule_director_models[policy_type - 1].objects.filter(rule_id__in=rule_list).update(**update_terms)
        rule_info = rule_models[policy_type - 1].objects.filter(rule_id__in=rule_list)
        for info in rule_info:
            print info.rule_status, info.operate

            # rule_models[policy_type - 1].objects.filter(id=info.id).update(group_id=group_id)

            ### 目前任务组不考虑增量下发
            if info.rule_status == 1 and info.operate == 'add':
                rule_models[policy_type - 1].objects.filter(id=info.id).update(group_id=group_id, operate='add',
                                                                                        rule_status=1)
            else:
                rule_models[policy_type - 1].objects.filter(id=info.id).update(group_id=group_id,
                                                                                        operate='group' + '#' + info.operate,
                                                                                        rule_status=1)
        common.generate_system_log(request_data, u'策略操作', u'批量修改策略所属任务组',
                                   u'修改策略所属任务组类型：' + common.POLICY_TYPE[policy_type - 1] + u' 修改策略rule_id：' + json.dumps(rule_list) + u'所属任务组id修改为' + request_data.get('group_id', u'没有任务组') + u'修改成功')
        return common.ui_message_response(200, '修改成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'策略操作', u'批量修改策略所属任务组',
                                   u'修改策略所属任务组类型：' + common.POLICY_TYPE[policy_type - 1] + u'修改策略rule_id：' + json.dumps(rule_list) + u'所属任务组id修改为' + request_data.get('group_id', u'没有任务组') + u'模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 复制现有规则，产生新的规则
def copy_policy(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        policy_type = common.check_request_int_field(request_data, 'policy_type')
        if isinstance(policy_type, Response):
            return policy_type

        group_id = request_data.get('group_id')
        if group_id is not None:
            group_id = int(group_id)

        rule_list = common.check_request_list_or_dict_field(request_data, 'rule_id')  # rule_id列表
        if isinstance(rule_list, Response):
            return rule_list

        for rule_id in rule_list:
            rule = rule_models[policy_type - 1].objects.filter(rule_id=rule_id)
            serializer_data = serialize('json', rule)
            list_data = json.loads(serializer_data)

            with connection.cursor() as cursor:  # 运行mysql函数，生成规则id
                cursor.execute('select nextval(%s)', ('rule',))  # 参数是一个元组
                rule_id = common.get_rule_serial(cursor.fetchone()[0])
            rule_data = list_data[0].get('fields')
            rule_data['group_id'] = group_id
            if policy_type not in [4, 13, 14]:  # 未知攻击、通联关系、应用行为没有rule_id字段
                rule_data['rule_id'] = rule_id

            rule_data['operate_time'] = du.get_current_date_string()
            if 'label' in rule_data:
                rule_data['remark'] = rule_data.pop('label')

            if policy_type == 5:  # 关键词检测策略
                rule_data['rule_type'] = 0 if rule_data['rule_type'] == 'keyword' else 1

            if policy_type == 9:  # IP审计策略
                # 界面传输的值：0表示无限制，1表示TCP，2表示UDP；数据库存储的值：0表示无限制，6表示TCP，17表示UDP
                rule_data['protocol'] = [0, 6, 17][rule_data['protocol']]
            if policy_type == 18:  # 阻断策略
                rule_data['protocol'] = 6  # 固定为TCP
            rule_data['rule_status'] = 1
            rule_data['operate'] = 'add'
            rule_data['version'] = ''
            rule_data['operate_time'] = du.get_current_date_string()
            rule_data['device_id_list_run'] = ''
            rule_data['device_id_list'] = ''
            rule_data['is_del'] = 1
            # rule_data['command_node_id'] = None
            serializer = rule_serializers[policy_type - 1](data=rule_data)
            if serializer.is_valid():
                serializer.save()  # 存储数据库

        return common.ui_message_response(200, '修改成功', list_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)



# logger_record = logging.getLogger('project.record')

# ********** 策略 **********

# 构造策略查询页面参数
def get_rule_query_terms(request_data, policy_type):
    # 构造查询参数
    query_terms = {}
    
    rule_id = request_data.get('rule_id')            # 规则ID
    if rule_id is not None:
        query_terms['rule_id__contains'] = rule_id
    
    rule_status = request_data.get('rule_status')    # 规则状态
    if rule_status is not None:
        query_terms['rule_status'] = rule_status
    
    risk = request_data.get('risk')                  # 告警级别
    if risk is not None:
        query_terms['risk'] = risk
    
    label = request_data.get('label')                # 备注标签
    if label is not None:
        query_terms['remark__contains'] = label
    
    if policy_type == 1:                                        # 木马攻击检测
        trojan_id = request_data.get('trojan_id')               # 木马分类编号
        if trojan_id is not None:
            query_terms['trojan_id__contains'] = trojan_id
        
        trojan_name = request_data.get('trojan_name')           # 木马名称
        if trojan_name is not None:
            query_terms['trojan_name__contains'] = trojan_name
        
        trojan_type = request_data.get('trojan_type')           # 木马类型
        if trojan_type is not None:
            query_terms['trojan_type'] = trojan_type
            
        store_pcap = request_data.get('store_pcap')             # 是否保留报文（1保留，2不保留）
        if store_pcap is not None:
            query_terms['store_pcap'] = store_pcap

        print query_terms
    
    elif policy_type == 2:                                      # 漏洞利用检测
        rule = request_data.get('rule')                         # 规则内容
        if rule is not None:
            query_terms['rule__contains'] = rule
        
        attack_type = request_data.get('attack_type')           # 攻击类型
        if attack_type is not None:
            query_terms['attack_type'] = attack_type
            
    elif policy_type == 3:                                      # 恶意程序检测
        malware_type = request_data.get('malware_type')         # 恶意程序种类
        if malware_type is not None:
            query_terms['malware_type__contains'] = malware_type
        
        malware_name = request_data.get('malware_name')         # 恶意程序名称
        if malware_name is not None:
            query_terms['malware_name__contains'] = malware_name
            
    elif policy_type == 4:                                      # 未知攻击窃密检测文件上传策略
        abn_type = request_data.get('abn_type')                 # 未知攻击窃密类型
        if abn_type is not None:
            query_terms['abn_type'] = abn_type
        
        risk_min = request_data.get('risk_min')                 # 最低风险级别
        if risk_min is not None:
            query_terms['risk_min'] = risk_min
        
        file_size_limit = request_data.get('file_size_limit')   # 文件大小限制
        if file_size_limit is not None:
            query_terms['file_size_limit'] = file_size_limit
        
        file_num_hour = request_data.get('file_num_hour')       # 每小时上传文件限制
        if file_num_hour is not None:
            query_terms['file_num_hour'] = file_num_hour
        
        rate_limit = request_data.get('rate_limit')             # 上传文件最大带宽速率限制
        if rate_limit is not None:
            query_terms['rate_limit'] = rate_limit
            
    elif policy_type == 5:                                      # 关键词检测
        rule_content = request_data.get('rule_content')         # 规则内容
        if rule_content is not None:
            query_terms['rule_content__contains'] = rule_content
            
    elif policy_type == 6:                                      # 加密文件检测
        filesize_minsize = request_data.get('filesize_minsize') # 文件最小值
        if filesize_minsize is not None:
            query_terms['filesize_minsize'] = filesize_minsize
        
        filesize_maxsize = request_data.get('filesize_maxsize') # 文件最大值
        if filesize_maxsize is not None:
            query_terms['filesize_maxsize'] = filesize_maxsize
            
    elif policy_type == 7:                                      # 压缩文件检测
        depth = request_data.get('depth')                       # 压缩层数
        if depth is not None:
            query_terms['depth'] = depth
        
        backsize = request_data.get('backsize')                 # 回传文件大小
        if backsize is not None:
            query_terms['backsize'] = backsize
        
        dropsize = request_data.get('dropsize')                 # 丢弃文件大小
        if dropsize is not None:
            query_terms['dropsize'] = dropsize
            
    elif policy_type == 8:                                      # 图片文件筛选
        filesize_minsize = request_data.get('filesize_minsize') # 图片回传最小值
        if filesize_minsize is not None:
            query_terms['filesize_minsize'] = filesize_minsize
        
        filesize_maxsize = request_data.get('filesize_maxsize') # 图片回传最大值
        if filesize_maxsize is not None:
            query_terms['filesize_maxsize'] = filesize_maxsize
            
    elif policy_type == 9:                                      # IP侦听检测
        sip = request_data.get('sip')                           # 源IP
        if sip is not None:
            query_terms['sip__contains'] = sip
        sport = request_data.get('sport')                       # 源端口
        if sport is not None:
            query_terms['sport__contains'] = sport
        dip = request_data.get('dip')                           # 目的IP
        if dip is not None:
            query_terms['dip__contains'] = dip
        dport = request_data.get('dport')                       # 目的端口
        if dport is not None:
            query_terms['dport__contains'] = dport
        protocol = request_data.get('protocol')                 # 通信协议
        if protocol is not None:
            query_terms['protocol'] = protocol
            
    elif policy_type in [10, 11, 12, 15, 16]:
        if policy_type in [10, 16]:                            # 域名侦听检测/DNS过滤
            dns = request_data.get('dns')                       # DNS信息
            if dns is not None:
                query_terms['dns__contains'] = dns
        elif policy_type in [11, 15]:                           # URL侦听检测/WEB过滤
            url = request_data.get('url')                       # URL信息
            if url is not None:
                query_terms['url__contains'] = url
        else:                                                   # 账号侦听检测
            account = request_data.get('account')               # 账号信息
            if account is not None:
                query_terms['account__contains'] = account
            
            account_type = request_data.get('account_type')     # 账号类型
            if account_type is not None:
                query_terms['account_type__contains'] = account_type
        
        rule_type = request_data.get('rule_type')               # 规则类型
        if rule_type is not None:
            query_terms['rule_type'] = rule_type
        
        match_type = request_data.get('match_type')             # 匹配类型
        if match_type is not None:
            query_terms['match_type'] = match_type
        
    elif policy_type in [13, 14]:                               # 通联关系/应用行为上传
        interval = request_data.get('interval')                 # 每次上报的间隔
        if interval is not None:
            query_terms['interval'] = interval
        
        num = request_data.get('num')                           # 日志条数(缓存事件数)
        if num is not None:
            query_terms['num'] = num
            
    elif policy_type == 17:                                     # IP白名单策略
        ip = request_data.get('ip')                             # ip地址
        if ip is not None:
            query_terms['ip__contains'] = ip
        
        port = request_data.get('port')                         # 端口值
        if port is not None:
            query_terms['port'] = port
            
    elif policy_type == 18:                                     # 阻断策略
        sip = request_data.get('sip')                           # 源IP
        if sip is not None:
            query_terms['sip__contains'] = sip
        
        dip = request_data.get('dip')                           # 目的IP
        if dip is not None:
            query_terms['dip__contains'] = dip

    return query_terms
    

# 获取查询结果集
def get_result_set(policy_type):
    if policy_type == 1:                                     # 木马攻击检测
        result_set = ('rule_id', 'trojan_id', 'trojan_name', 'trojan_type', 'os', 'desc', 'rule', 'risk', 'store_pcap', 'group_id')
    elif policy_type == 2:                                   # 漏洞利用检测
        result_set = ('rule_id', 'store_pcap', 'rule', 'attack_type', 'application', 'os', 'risk', 'group_id')
    elif policy_type == 3:                                   # 恶意程序检测
        result_set = ('rule_id', 'malware_type', 'malware_name', 'md5', 'signature', 'risk', 'group_id')
    elif policy_type == 4:                                   # 未知攻击窃密检测文件上传策略
        result_set = ('rule_id', 'abn_type', 'allow_file', 'risk_min', 'file_size_limit', 'file_num_hour', 'rate_limit', 'group_id')
    elif policy_type == 5:                                   # 关键词检测
        result_set = ('rule_id', 'rule_type', 'min_match_count', 'rule_content', 'risk', 'group_id')
    elif policy_type == 6:                                   # 加密文件检测
        result_set = ('rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk', 'group_id')
    elif policy_type == 7:                                   # 压缩文件检测
        result_set = ('rule_id', 'depth', 'backsize', 'dropsize', 'risk', 'group_id')
    elif policy_type == 8:                                   # 图片文件筛选
        result_set = ('rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk', 'group_id')
    elif policy_type == 9:                                   # IP侦听检测
        result_set = ('rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'risk', 'group_id')
    elif policy_type == 10:                                  # 域名侦听检测
        result_set = ('rule_id', 'dns', 'rule_type', 'match_type', 'risk', 'group_id')
    elif policy_type == 11:                                  # URL侦听检测
        result_set = ('rule_id', 'url', 'rule_type', 'match_type', 'risk', 'group_id')
    elif policy_type == 12:                                  # 账号侦听检测
        result_set = ('rule_id', 'account_type', 'account', 'rule_type', 'match_type', 'risk', 'group_id')
    elif policy_type in [13, 14]:                            # 通联关系/应用行为上传
        result_set = ('rule_id', 'interval', 'num', 'group_id')
    elif policy_type == 15:                                  # web过滤
        result_set = ('rule_id', 'url', 'rule_type', 'match_type', 'group_id')
    elif policy_type == 16:                                  # dns过滤
        result_set = ('rule_id', 'dns', 'rule_type', 'match_type', 'group_id')
    elif policy_type == 17:                                  # IP白名单策略
        result_set = ('rule_id', 'ip', 'port', 'group_id')
    elif policy_type == 18:                                  # 阻断策略
        result_set = ('rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'group_id')
    else:
        result_set = ()
    
    return result_set + ('rule_status', 'operate', 'device_id_list_run', 'device_id_list', 'creat_time', 'remark')
    

# 获取规则页面查询结果
def get_rule_query_result(request_data):

    # 获取请求参数
    policy_type = common.check_request_int_field(request_data, 'policy_type')    # 策略模块
    if isinstance(policy_type, Response):
        return policy_type

    query_terms = get_rule_query_terms(request_data, policy_type)

    result_set = get_result_set(policy_type)  # 界面显示的结果集
    is_director = request_data.get('is_director')
    if is_director == '1':
        task_id = request_data.get('task_id')
        if task_id is not None:
            query_terms['task_id'] = task_id
        query_data = director_rule_models[policy_type - 1].objects.filter(**query_terms)

        result_list = list(result_set)
        result_list[result_set.index('group_id')] = 'task_id'
        result_set = tuple(result_list)
    else:
        group_id = request_data.get('group_id')
        if group_id is not None:
            query_terms['group_id'] = group_id
        query_data = rule_models[policy_type - 1].objects.filter(**query_terms)

    # 获取检测器查询条件
    device_id = request_data.get('device_id')  # 检测器编号，如'160901010001'
    if device_id:
        detector_info = Detector.objects.filter(device_id=device_id)
        if detector_info.exists():
            query_id = '#' + str(detector_info[0].device_id) + '#'
            query_data = query_data.filter(Q(device_id_list__contains=query_id) | Q(device_id_list='#'))
        else:
            query_data = query_data.filter(device_id_list='###')  # 查询不到任何数据

    # 界面不显示已经标记删除的
    query_data = query_data.exclude(is_del=0, rule_status=0)

    return query_data, result_set


# 查询某个监测模块的所有规则
def show_all_rules(request):
    try:
        request_data = common.print_header_data(request)                    # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_data, result_set = get_rule_query_result(request_data)        # 查询结果
        
        query_data = query_data.order_by('-id')[start_pos:end_pos]          # 排序

        serializer_data = serialize('json', query_data, fields=result_set)
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            # fields['operate'] = operate[fields['operate']]

            operate_list = []
            if fields['operate'].strip() in ['', 'add', 'del']:
                operate_list.append(operate_map[fields['operate'].strip()])
            else:
                operate_str = fields['operate'].strip().split('#')
                # print "#", operate_str
                for operate in operate_str:
                    if operate == '':
                        continue
                    operate_list.append(operate_map.get(operate, 3))
            # print "operate_list", operate_list
            new_operate_list = []
            for v in operate_list:
                if v not in new_operate_list:
                    new_operate_list.append(v)
            # print "operate_list", new_operate_list
            fields['operate'] = json.dumps(map(int, new_operate_list), separators=(',', ':'))


            fields['device_id_list_run'] = common.generate_device_ids_ui_str_from_model_str(fields['device_id_list_run'])   # 运行该规则的检测器

            fields['device_id_list'] = common.generate_device_ids_ui_str_from_model_str(fields['device_id_list'])  # 准备要下发的检测器

            fields['create_t'] = fields.pop('creat_time').replace('T', ' ')
            fields['label'] = fields.pop('remark')

            groups = TaskGroup.objects.filter(group_id=fields.get('group_id'))
            if groups.exists():
                fields['group_name'] = groups[0].name
            else:
                fields['group_name'] = ''
            if 'task_id' in fields and fields['task_id'] is not None:
                fields['task_id'] = str(fields.get('task_id'))
            if 'group_id' in fields and fields['group_id'] is not None:
                fields['group_id'] = str(fields.get('group_id'))
            fields['rule_id'] = str(fields['rule_id'])  # 由于前段js不支持long型，所以数据库中存的无符号整型传入前端由于精度问题会出现ID异常
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询某个监测模块的规则总数
def show_rules_count(request):
    try:
        request_data = common.print_header_data(request)        # 获取请求数据
        query_data = get_rule_query_result(request_data)[0]      # 获取查询结果
        if isinstance(query_data, Response):
            return query_data

        count = query_data.count()     # 查询数量（与查询接口对应）
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询所有监测模块的规则总数
def show_rules_count_all(request):
    try:
        request_data = common.print_header_data(request)        # 获取请求数据

        count = 0
        for model in rule_models:
            count += model.objects.all().count()
        show_data = {'class': len(rule_models), 'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 插入某个监测模块的一条规则
def insert_rule(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        policy_type = common.check_request_int_field(request_data, 'policy_type')    # 策略模块
        if isinstance(policy_type, Response):
            return policy_type

        rule_data = common.check_request_list_or_dict_field(request_data, 'json')
        if isinstance(rule_data, Response):
            return rule_data

        with connection.cursor() as cursor:     # 运行mysql函数，生成规则id
            cursor.execute('select nextval(%s)', ('rule', ))    # 参数是一个元组
            rule_id = common.get_rule_serial(cursor.fetchone()[0])

        # if policy_type not in [4, 13, 14]:  # 未知攻击、通联关系、应用行为没有rule_id字段  现在已经添加rule_id
        #     rule_data['rule_id'] = rule_id
        rule_data['rule_id'] = rule_id

        rule_data['operate'] = 'add'
        rule_data['operate_time'] = du.get_current_time()
        if 'label' in rule_data:
            rule_data['remark'] = rule_data.pop('label')

        if policy_type == 5:  # 关键词检测策略
            rule_data['rule_type'] = 0 if rule_data['rule_type'] == 'keyword' else 1

        if policy_type == 9:  # IP审计策略
            # 界面传输的值：0表示无限制，1表示TCP，2表示UDP；数据库存储的值：0表示无限制，6表示TCP，17表示UDP
            rule_data['protocol'] = [0, 6, 17][rule_data['protocol']]
        if policy_type == 18:   # 阻断策略
            rule_data['protocol'] = 6    # 固定为TCP

        from director.data_processing import director_rule_models
        # 获取指挥中心相同策略
        rule_data['map_rule_id_list'] = common.check_center_director_rule_is_equal(rule_data, policy_type, director_rule_models[policy_type-1])

        serializer = rule_serializers[policy_type - 1](data=rule_data)
        if serializer.is_valid():
            serializer.save()            # 存储数据库
        elif common.is_serial_id_overflow_errer(serializer.errors):    # 数据库存储的是无符号64位整型数据，django模型BigIntegerField不支持无符号64位，所以rest-framework序列化时对于比有符号最大值还大的数会报错，这是采用django model的原生create入库
            rule_models[policy_type - 1].objects.create(**rule_data)
        else:
            common.generate_system_log(request_data, u'策略操作', u'添加规则', u'插入' + common.POLICY_TYPE[policy_type - 1] + ':' + request_data.get('json') + u', 失败')
            return common.ui_message_response(400, json.dumps(serializer.errors), '数据缺失或字段不符合规定，序列化出错')
        common.generate_system_log(request_data, u'策略操作', u'添加规则',
                                   u'成功插入一条' + common.POLICY_TYPE[policy_type - 1] + ':' + request_data.get('json'))
        return common.ui_message_response(200, '数据存储成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'策略操作', u'添加规则', u'插入' + common.POLICY_TYPE[policy_type - 1] + u'程序出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 下载导入文件模板
def download_rule_template(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        file_name = 'rules.zip'
        relative_path = 'template/' + file_name
        file_path = common.MEDIA_ROOT + relative_path
        if not os.path.exists(file_path):
            return common.ui_message_response(400, '服务器上没有该文件:' + file_path.encode('utf-8'), '文件不存在')

        response = common.construct_download_file_header(file_path, relative_path, file_name)
        return response

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)
                                          

# 产生一条规则字典（数据类型判断）
def generate_rule_dict(policy_type, device_ids, **kw):
    rule_dict = {}
    # if policy_type not in [4, 13, 14]:  # 未知攻击、通联关系、应用行为没有rule_id字段 现在已添加
    with connection.cursor() as cursor:     # 运行mysql函数，生成规则id
        cursor.execute('select nextval(%s)', ('rule', ))    # 参数是一个元组
        rule_dict['rule_id'] = common.get_rule_serial(cursor.fetchone()[0])

    if policy_type == 1:  # 木马规则
        rule_dict['trojan_id'] = kw['trojan_id']
        if isinstance(kw['store_pcap'], float):
            rule_dict['store_pcap'] = int(kw['store_pcap'])
        elif kw['store_pcap'] == '':
            rule_dict['store_pcap'] = 1  # 默认留存(1表示留存，2表示不留存)
        else:
            return False
        rule_dict['os'] = kw['os']
        rule_dict['trojan_name'] = kw['trojan_name']
        if kw['trojan_type'] in [1.0, 2.0, 3.0, 4.0]:
            rule_dict['trojan_type'] = int(kw['trojan_type'])
        else:
            return False
        rule_dict['desc'] = kw['desc']
        rule_dict['rule'] = kw['rule']
        if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            rule_dict['risk'] = int(kw['risk'])
        else:
            return False
    elif policy_type == 2:  # 漏洞利用规则
        if isinstance(kw['store_pcap'], float):
            rule_dict['store_pcap'] = int(kw['store_pcap'])
        elif kw['store_pcap'] == '':
            rule_dict['store_pcap'] = 1  # 默认留存(1表示留存，2表示不留存)
        else:
            return False
        rule_dict['rule'] = kw['rule']
        attack_type_list = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw']
        if kw['attack_type'] in attack_type_list:
            rule_dict['attack_type'] = attack_type_list.index(kw['attack_type']) + 1
        else:
            return False
        rule_dict['application'] = kw['application']
        rule_dict['os'] = kw['os']
        if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            rule_dict['risk'] = int(kw['risk'])
        else:
            return False
    elif policy_type == 3:  # 恶意程序规则
        rule_dict['md5'] = kw['md5']
        rule_dict['signature'] = kw['signature']
        rule_dict['malware_type'] = kw['malware_type']
        rule_dict['malware_name'] = kw['malware_name']
        if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            rule_dict['risk'] = int(kw['risk'])
        else:
            return False
    elif policy_type == 4:  # 未知攻击规则
        if kw['abn_type'] in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]:
            rule_dict['abn_type'] = int(kw['abn_type'])
        else:
            return False
        if kw['allow_file'] in [0.0, 1.0]:
            rule_dict['allow_file'] = int(kw['allow_file'])
        if kw['risk_min'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            rule_dict['risk_min'] = int(kw['risk_min'])
        else:
            return False
        if isinstance(kw['file_size_limit'], float) and 0 <= kw['file_size_limit'] <= 102400:
            rule_dict['file_size_limit'] = int(kw['file_size_limit'])
        else:
            return False
        if isinstance(kw['file_num_hour'], float) and 0 <= kw['file_num_hour'] <= 1000:
            rule_dict['file_num_hour'] = int(kw['file_num_hour'])
        else:
            return False
        if isinstance(kw['rate_limit'], float) and 0 <= kw['rate_limit'] <= 102400:
            rule_dict['rate_limit'] = int(kw['rate_limit'])
        else:
            return False
    elif policy_type == 5:  # 关键词规则
        rule_type_list = ['keyword', 'regex']
        if kw['rule_type'] in rule_type_list:
            rule_dict['rule_type'] = rule_type_list.index(kw['rule_type'])
        else:
            return False
        if isinstance(kw['min_match_count'], float):
            rule_dict['min_match_count'] = int(kw['min_match_count'])
        elif kw['min_match_count'] == '':
            rule_dict['min_match_count'] = 1  # 默认值
        else:
            return False
        rule_dict['rule_content'] = kw['rule_content']
        if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            rule_dict['risk'] = int(kw['risk'])
        else:
            return False
    elif policy_type in [6, 8]:  # 加密文件筛选规则, 图文筛选规则
        if isinstance(kw['filesize_minsize'], float):
            rule_dict['filesize_minsize'] = int(kw['filesize_minsize'])
        else:
            return False
        if isinstance(kw['filesize_maxsize'], float):
            rule_dict['filesize_maxsize'] = int(kw['filesize_maxsize'])
        else:
            return False
        if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            rule_dict['risk'] = int(kw['risk'])
        else:
            return False
    elif policy_type == 7:  # 压缩文件规则
        if isinstance(kw['depth'], float):
            rule_dict['depth'] = int(kw['depth'])
        else:
            return False
        if isinstance(kw['backsize'], float):
            rule_dict['backsize'] = int(kw['backsize'])
        else:
            return False
        if isinstance(kw['dropsize'], float):
            rule_dict['dropsize'] = int(kw['dropsize'])
        else:
            return False
        if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
            rule_dict['risk'] = int(kw['risk'])
        else:
            return False
    elif policy_type in [9, 18]:  # IP审计规则, 阻断规则
        rule_dict['sip'] = kw['sip']
        rule_dict['sport'] = kw['sport']
        rule_dict['dip'] = kw['dip']
        rule_dict['dport'] = kw['dport']
        if policy_type == 9:
            if kw['protocol'] in [0.0, 6.0, 17.0]:  # 0表示无限制，6表示TCP，17表示UDP
                rule_dict['protocol'] = int(kw['protocol'])
            else:
                return False
        else:
            if kw['protocol'] == 6.0:    # 阻断规则固定为TCP
                rule_dict['protocol'] = int(kw['protocol'])
            else:
                return False
        
        if policy_type == 9:
            if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
                rule_dict['risk'] = int(kw['risk'])
            else:
                return False
    elif policy_type in [10, 11, 12, 15, 16]:
        if kw['rule_type'] in [0.0, 1.0]:   # 0表示无表达式，1表示正则表达式
            rule_dict['rule_type'] = int(kw['rule_type'])
        else:
            return False
        if kw['match_type'] in [0.0, 1.0, 2.0, 3.0]:  # 0表示子串匹配，1表示右匹配，2表示左匹配，3表示完全匹配
            rule_dict['match_type'] = int(kw['match_type'])
        else:
            return False
        
        if policy_type in [10, 11, 12]:
            if kw['risk'] in [0.0, 1.0, 2.0, 3.0, 4.0]:
                rule_dict['risk'] = int(kw['risk'])
            else:
                return False
        
        if policy_type in [10, 16]:  # DNS审计规则, DNS过滤规则
            rule_dict['dns'] = kw['dns']
        elif policy_type in [11, 15]:  # URL审计规则, Web过滤规则
            rule_dict['url'] = kw['url']
        else:   # 账号审计规则
            rule_dict['account_type'] = kw['account_type']
            rule_dict['account'] = kw['account']
    elif policy_type in [13, 14]:  # 通联关系上传规则， 应用行为上传规则
        if isinstance(kw['interval'], float) and isinstance(kw['num'], float):
            rule_dict['interval'] = kw['interval']
            rule_dict['num'] = kw['num']
        else:
            return False
    elif policy_type == 17:  # IP白名单规则
        rule_dict['ip'] = kw['ip']
        rule_dict['port'] = kw['port']

    rule_dict['version'] = ''
    # rule_dict['operate'] = 'change'
    rule_dict['operate'] = 'add'
    rule_dict['rule_status'] = 1
    rule_dict['creat_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rule_dict['operate_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rule_dict['device_id_list_run'] = ''
    rule_dict['device_id_list'] = device_ids
    rule_dict['remark'] = kw['remark']
    rule_dict['is_del'] = 1
    return rule_dict

                                          
# 根据规则文件构造规则列表
def generate_rule_list(policy_type, rule_file, device_ids=''):
    rule_config = [
        ['trojan_id', 'store_pcap', 'os', 'trojan_name', 'trojan_type', 'desc', 'rule', 'risk', 'remark'],   # 木马规则
        ['store_pcap', 'rule', 'attack_type', 'application', 'os', 'risk', 'remark'],                        # 漏洞利用规则
        ['md5', 'signature', 'malware_type', 'malware_name', 'risk', 'remark'],                              # 恶意文件规则
        ['abn_type', 'allow_file', 'risk_min', 'file_size_limit', 'file_num_hour', 'rate_limit', 'remark'],  # 未知攻击文件上传规则
        ['rule_type', 'min_match_count', 'rule_content', 'risk', 'remark'],                                  # 关键词规则
        ['filesize_minsize', 'filesize_maxsize', 'risk', 'remark'],                                          # 加密文件筛选规则
        ['depth', 'backsize', 'dropsize', 'risk', 'remark'],                                                 # 压缩文件规则
        ['filesize_minsize', 'filesize_maxsize', 'risk', 'remark'],                                          # 图文文件筛选规则
        ['sip', 'sport', 'dip', 'dport', 'protocol', 'risk', 'remark'],                                      # IP审计规则
        ['dns', 'rule_type', 'match_type', 'risk', 'remark'],                                                # DNS审计规则
        ['url', 'rule_type', 'match_type', 'risk', 'remark'],                                                # URL审计规则
        ['account_type', 'account', 'rule_type', 'match_type', 'risk', 'remark'],                            # 账号审计规则
        ['interval', 'num', 'remark'],                                                                       # 通联关系上传规则
        ['interval', 'num', 'remark'],                                                                       # 应用行为上传规则
        ['url', 'rule_type', 'match_type', 'remark'],                                                        # web过滤规则
        ['dns', 'rule_type', 'match_type', 'remark'],                                                        # DNS过滤规则
        ['ip', 'port', 'remark'],                                                                            # IP白名单过滤规则
        ['sip', 'sport', 'dip', 'dport', 'protocol', 'remark']                                               # 阻断规则
    ]
    book = xlrd.open_workbook(rule_file)
    sheet=book.sheet_by_index(0)
    first_row = sheet.row_values(0)
    if set(first_row) != set(rule_config[policy_type - 1]):
        print "规则参数不正确"
        return False
    rows_num = sheet.nrows
    cols_num = sheet.ncols
    rule_list = []
    for i in xrange(1, rows_num):
        config_dict = {}
        for j in range(cols_num):
            config_dict[first_row[j]] = sheet.cell_value(i, j)
        # print '************', config_dict
        rule_dict = generate_rule_dict(policy_type, device_ids, **config_dict)
        if rule_dict:
            rule_list.append(rule_dict)
        else:
            print '第%d行存在数据类型错误' % (i + 1,)
            return False
    return rule_list


# 批量插入某个监测模块的规则
def batch_insert_rules(request, sub_function_dir):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        policy_type = common.check_request_int_field(request_data, 'policy_type')  # 策略模块
        if isinstance(policy_type, Response):
            return policy_type
        file_path = request_data.get('param')        # 规则文件相对路径
        if file_path is None:
            return common.ui_message_response(400, '请求url中没有携带参数param', '请求参数没有param')
        file_path = common.MEDIA_ROOT + sub_function_dir + file_path
        if not os.path.exists(file_path):
            return common.ui_message_response(400, '服务器上没有该文件:' + file_path.encode('utf-8'),
                                              '规则文件不存在')
        # device_ids = request_data.get('device_id_list', '')        # 下发的检测器id列表，默认为空
        rule_list = generate_rule_list(policy_type, file_path)
        for rule in rule_list:
            from director.data_processing import director_rule_models
            # 获取指挥中心相同策略
            rule['map_rule_id_list'] = common.check_center_director_rule_is_equal(rule, policy_type, director_rule_models[policy_type - 1])

        if rule_list:
            serializer = rule_serializers[policy_type - 1](data=rule_list, many=True)
            if serializer.is_valid():
                serializer.save()            # 存储数据库
            elif common.is_serial_id_overflow_errer(serializer.errors):    # 数据库存储的是无符号64位整型数据，django模型的BigIntegerField不支持无符号64位，所以rest-framework序列化时对于比有符号最大值还大的数会报错，这是采用django model的原生create入库
                for data in rule_list:
                    rule_models[policy_type - 1].objects.create(**data)
            else:
                return common.ui_message_response(400, json.dumps(serializer.errors), '数据缺失或字段不符合规定，序列化出错')
            common.generate_system_log(request_data, u'策略操作', u'添加规则',
                                       u'成功插入多条' + common.POLICY_TYPE[policy_type - 1] + ':' + json.dumps(rule_list))
            return common.ui_message_response(200, '数据存储成功', 'success', status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '规则文件内容不符合规范', '规则文件内容不符合规范')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 删除某个监测模块的多条规则
def delete_rules(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        policy_type = common.check_request_int_field(request_data, 'policy_type')    # 策略模块
        if isinstance(policy_type, Response):
            return policy_type

        rule_id_list = common.check_request_list_or_dict_field(request_data, 'id')   # 规则id列表
        if isinstance(rule_id_list, Response):
            return rule_id_list

        delete_id_list = []   # 待删除的rule主键id列表
        update_id_list = []   # 待更新的rule主键id列表

        rule_list = rule_models[policy_type - 1].objects.filter(id__in=rule_id_list)
        if not rule_list.exists():
            return common.ui_message_response(400, '根据条件没有查询到需要删除的插件记录', '没有选择的插件')
        for rule in rule_list:
            if rule.device_id_list_run == '':   # 当前规则没有在任何检测器上存在
                delete_id_list.append(rule.id)   # 直接删除
            else:
                update_id_list.append(rule.id)   # 更新
        rule_models[policy_type - 1].objects.filter(id__in=delete_id_list).delete()  # 删除
        rule_models[policy_type - 1].objects.filter(id__in=update_id_list).update(
            version='', rule_status=1, operate_time=du.get_current_time(), operate='del',
            device_id_list='', is_del=0)  # 更新
        common.generate_system_log(request_data, u'策略操作', u'删除规则', u'删除' + str(len(rule_list)) + u'条' + common.POLICY_TYPE[policy_type - 1])
        return common.ui_message_response(200, '删除成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'策略操作', u'删除规则', u'删除' + common.POLICY_TYPE[policy_type - 1] + u'模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 接收规则id和检测器id，变更规则生效的检测器（此操作仅在选中规则生效的检测器范围一样才执行）
def change_rules_detectors(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        policy_type = common.check_request_int_field(request_data, 'policy_type')  # 策略模块
        if isinstance(policy_type, Response):
            return policy_type
        rule_id_list = common.check_request_list_or_dict_field(request_data, 'id')   # 规则id列表
        if isinstance(rule_id_list, Response):
            return rule_id_list
        device_id_list = request_data.get('detector_id_list')  # 检测器id列表
        rule_data = rule_models[policy_type-1].objects.filter(id__in=rule_id_list)
        if device_id_list is not None:
            if device_id_list == '[]':  # 表示全部生效
                for info in rule_data:
                    update_rule_operate_status_devices(policy_type, info, '#')

            elif device_id_list == '[0]':   # 表示清空生效范围
                for info in rule_data:
                    update_rule_operate_status_devices(policy_type, info, '')

            else:
                device_id_list = json.loads(device_id_list)
                update_detector_value = '#' + '#'.join(map(str, device_id_list)) + '#'
                for info in rule_data:
                    update_rule_operate_status_devices(policy_type, info, update_detector_value)

            common.generate_system_log(request_data, u'规则更新', u'更新规则适用范围', u'变更' + common.POLICY_TYPE[policy_type - 1] + u'中id列表为' + request_data.get('id') + u'的规则的生效检测器为' + request_data.get('detector_id_list'))
        else:    # 没有检测器id列表参数表示全部生效
            return common.ui_message_response(400, '参数detector_id_list不存在', '参数detector_id_list不存在')

        return common.ui_message_response(200, '变更成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'策略操作', u'更新规则适用范围', u'变更' + common.POLICY_TYPE[policy_type - 1] + u'生效检测器范围模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_rule_operate_status_devices(policy_type, rule, device_id_list):

    if rule.rule_status == 1 and rule.operate == 'add':
        print "set operate to add"
        rule_models[policy_type - 1].objects.filter(id=rule.id).update(
            device_id_list=device_id_list, operate='add', rule_status=1)
    else:
        print "append change to operate"
        rule_models[policy_type - 1].objects.filter(id=rule.id).update(
            device_id_list=device_id_list, operate='change' + '#' + rule.operate, rule_status=1)


# 接收规则id和检测器id，追加规则生效的检测器（此操作不限制选中的规则生效的检测器范围是否一样）
def append_rules_detector(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        policy_type = common.check_request_int_field(request_data, 'policy_type')  # 策略模块
        if isinstance(policy_type, Response):
            return policy_type

        rule_id_list = common.check_request_list_or_dict_field(request_data, 'id')  # 规则id列表
        if isinstance(rule_id_list, Response):
            return rule_id_list

        device_id_list = request_data.get('detector_id_list')  # 检测器id列表参数
        if device_id_list is not None:
            rule_info = rule_models[policy_type - 1].objects.filter(id__in=rule_id_list)
            if device_id_list == '[]':   # 追加全部检测器
                for info in rule_info:
                    update_rule_operate_status_devices(policy_type, info, '#')

            else:   # 追加部分检测器，求原先列表和现在列表的并集
                device_id_list = json.loads(device_id_list)
                for info in rule_info:
                    if info.device_id_list not in ['', '#']:  # 原先列表不是全部，也不为空
                        origin_list = map(int, info.device_id_list[1: -1].split('#'))
                        update_detector_value = '#' + '#'.join(map(
                            str, sorted(set(device_id_list) | set(origin_list)))) + '#'
                    elif info.device_id_list == '':   # 原来列表为空
                        update_detector_value = '#' + '#'.join(map(str, device_id_list)) + '#'
                    else:
                        continue
                    update_rule_operate_status_devices(policy_type, info, update_detector_value)

        return common.ui_message_response(200, '追加成功', 'success', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 批量修改标签（备注）
def modify_labels(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        policy_type = common.check_request_int_field(request_data, 'policy_type')  # 策略模块
        if isinstance(policy_type, Response):
            return policy_type

        rule_id_list = common.check_request_list_or_dict_field(request_data, 'id')  # 规则id列表
        if isinstance(rule_id_list, Response):
            return rule_id_list

        label = request_data.get('new_label', '')  # 新的标签

        rule_models[policy_type - 1].objects.filter(id__in=rule_id_list).update(remark=label)
        return common.ui_message_response(200, '修改成功', 'success', status.HTTP_200_OK)
    except Exception:
        print traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# 获取规则内容字段（根据policy_type）
def get_rule_fields(policy_type):

    result_set = ()     # 规则内容的集合

    if policy_type == 1:  # 木马攻击检测
        result_set = ('rule_id', 'trojan_id', 'store_pcap', 'os', 'trojan_name', 'trojan_type', 'desc', 'rule', 'risk')
    elif policy_type == 2:  # 漏洞利用检测
        result_set = ('rule_id', 'store_pcap', 'rule', 'attack_type', 'application', 'os', 'risk')
    elif policy_type == 3:  # 恶意程序检测
        result_set = ('rule_id', 'md5', 'signature', 'malware_type', 'malware_name', 'risk')
    elif policy_type == 4:  # 未知攻击窃密检测文件上传
        result_set = ('rule_id', 'abn_type', 'allow_file', 'risk_min', 'file_size_limit', 'file_num_hour', 'rate_limit')
    elif policy_type == 5:  # 关键词检测
        result_set = ('rule_id', 'rule_type', 'min_match_count', 'rule_content', 'risk')
    elif policy_type == 6:  # 加密文件筛选
        result_set = ('rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk')
    elif policy_type == 7:  # 压缩文件检测
        result_set = ('rule_id', 'depth', 'backsize', 'dropsize', 'risk')
    elif policy_type == 8:  # 图片筛选回传
        result_set = ('rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk')
    elif policy_type == 9:  # IP侦听检测
        result_set = ('rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'risk')
    elif policy_type == 10:  # 域名侦听检测
        result_set = ('rule_id', 'dns', 'rule_type', 'match_type', 'risk')
    elif policy_type == 11:  # URL侦听检测
        result_set = ('rule_id', 'url', 'rule_type', 'match_type', 'risk')
    elif policy_type == 12:  # 账号侦听检测
        result_set = ('rule_id', 'account_type', 'account', 'rule_type', 'match_type', 'risk')
    elif policy_type == 13:  # 通联关系上传
        result_set = ('rule_id', 'interval', 'num')
    elif policy_type == 14:  # 应用行为上传
        result_set = ('rule_id', 'interval', 'num')
    elif policy_type == 15:  # web过滤
        result_set = ('rule_id', 'url', 'rule_type', 'match_type')
    elif policy_type == 16:  # dns过滤
        result_set = ('rule_id', 'dns', 'rule_type', 'match_type')
    elif policy_type == 17:  # IP白名单策略
        result_set = ('rule_id', 'ip', 'port')
    elif policy_type == 18:  # 阻断策略
        result_set = ('rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol')
    else:
        pass

    return result_set


# 生成某个模块的策略
def generate_increment_policy(request):
    """
    增量生成规则
    :param request:
    :return:
    """
    try:
        pu.print_format_header('增量下发策略')

        request_data = common.print_header_data(request)  # 获取请求数据

        policy_type = common.check_request_int_field(request_data, 'policy_type')    # 策略模块
        if isinstance(policy_type, Response):
            return policy_type

        result_set = get_rule_fields(policy_type)   # 获取查询的规则集合

        task_list = []   # 任务

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}   # id与device_id的对应关系

        add_rule = {}     # 每个检测器需要添加的规则，key表示检测器主键id，value表示rule_id（主键id）列表
        del_rule = {}     # 每个检测器需要删除的规则，key表示检测器主键id，value表示rule_id（主键id）列表
        rule_device_add = []   # 增加的rule(主键id)与检测器（主键id）的对应关系，每一个元素都是一个元组(rule_id, device_id)
        rule_device_del = []   # 删除的rule(主键id)与检测器（主键id）的对应关系，每一个元素都是一个元组(rule_id, device_id)

        # 查询未生成任务的规则信息
        rule_data = rule_models[policy_type - 1].objects.filter(rule_status=1)
        # rule_data = rule_models[policy_type - 1].objects.filter(~Q(device_id_list_run=F('device_id_list')) | Q(operate__contains='group'), rule_status=1)   #这里认为 对于之前的生效范围和设置生效范围的一样的话就不进行增量操作
        if not rule_data.exists():
            return common.ui_message_response(200, '没有未下发的规则', '没有未下发的规则', status.HTTP_200_OK)

        rule_json = serialize('json', rule_data, fields=result_set + ('remark', ))  # 序列化成json
        rule_all = json.loads(rule_json)
        config_dict = {data['pk']: data['fields'] for data in rule_all}  # config {规则id: config}
        if policy_type == 2:  # 漏洞利用规则，修改数字对应的攻击类型
            for k, v in config_dict.iteritems():
                config_dict[k]['attack_type'] = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw'][
                    v['attack_type'] - 1]
        elif policy_type in [6, 8]:  # 加密规则或图片规则，修改config的组织方式
            for k, v in config_dict.iteritems():
                config_dict[k]['filesize'] = {"minsize": v.pop('filesize_minsize'),
                                              "maxsize": v.pop('filesize_maxsize')}
        elif policy_type == 7:  # 压缩规则，修改config的组织方式
            for k, v in config_dict.iteritems():
                config_dict[k]['filesize'] = {"backsize": v.pop('backsize'),
                                              "dropsize": v.pop('dropsize')}

        director_config = copy.deepcopy(config_dict)

        for k in config_dict:
            config_dict[k].pop('remark')
            director_config[k]['label'] = director_config[k].pop('remark')

        command_policy_add = []
        command_policy_update = []
        command_policy_del = []
        command_policy_update_group = []

        for rule in rule_data:  # 遍历所有规则

            # ********************* 指挥中心数据 *********************    新增任务组变更增量同步
            d_run = rule.device_id_list_run  # 正在运行的检测器范围
            d_will_run = rule.device_id_list  # 变更后的检测器范围

            if rule.operate.strip() == 'add':      # 新增
                command_rule_add = copy.deepcopy(
                    director_config[rule.id])  # 深拷贝，否则修改command_rule_add也会修改config_dict
                # if d_will_run != '#' and d_will_run != '':  # id更换为对应的device_id
                #     id_list_run = map(int, d_will_run[1:-1].split('#'))
                #     d_will_run_new = '#' + '#'.join([id_device_dict[i_run] for i_run in id_list_run]) + '#'
                # else:
                #     d_will_run_new = d_will_run
                d_will_run_new = d_will_run
                command_rule_add['device_id_list_run'] = d_will_run_new
                command_rule_add['create_time'] = rule.creat_time.strftime('%Y-%m-%d %H:%M:%S')
                command_rule_add['task_id'] = rule.group_id
                command_policy_add.append(command_rule_add)

                # ######## 新增任务组  (规则新增时任务组的值默认为0)
                # if rule.group_id is not None and rule.group_id > 0:
                #     command_policy_update_group.append({'rule_id': rule.rule_id, 'task_id': rule.group_id})
            elif rule.operate.strip() == 'del':      # 删除
                if d_run != '' and d_will_run == '':
                    command_policy_del.append(rule.rule_id)

                ####### 删除任务组
                # command_policy_update_group.append({'rule_id': rule.rule_id, 'task_id': rule.group_id})

            elif str(rule.operate).find('change') >= 0:  # 修改生效范围
                # if d_will_run != '#' and d_will_run != '':  # id更换为对应的device_id
                #     id_list_run = map(int, d_will_run[1:-1].split('#'))
                #     d_will_run_new = '#' + '#'.join([id_device_dict[i_run] for i_run in id_list_run]) + '#'
                # else:
                #     d_will_run_new = d_will_run
                d_will_run_new = d_will_run

                command_policy_update.append({
                    'rule_id': rule.rule_id,
                    'device_id_list_run': d_will_run_new
                })

                ####### 变更任务组
                if str(rule.operate).find('group') >= 0:
                    command_policy_update_group.append({'rule_id': rule.rule_id, 'task_id': rule.group_id})
            else:                                    # 只变更了任务组
                command_policy_update_group.append({'rule_id': rule.rule_id, 'task_id': rule.group_id})

            # ********************* 指挥中心数据 *********************

            if rule.device_id_list == rule.device_id_list_run == '':    # 新增同时没有设置生效范围
                continue

            # previous_device_list 表示该规则已经生成任务的检测器id列表
            previous_device_list = common.generate_device_ids_list_from_model_str(rule.device_id_list_run, id_device_dict.values())

            # now_device_list表示该规则变更之后的检测器id列表
            now_device_list = common.generate_device_ids_list_from_model_str(rule.device_id_list, id_device_dict.values())

            print 'previous_device_list:', previous_device_list
            print 'now_device_list:', now_device_list

            add_device_ids = set(now_device_list) - (set(previous_device_list) & set(now_device_list))
            for d_id in add_device_ids:  # 规则对应的部分检测器增加
                rule_device_add.append((rule.id, d_id))
            del_device_ids = set(previous_device_list) - (set(previous_device_list) & set(now_device_list))
            for d_id in del_device_ids:  # 规则对应的部分检测器删除
                rule_device_del.append((rule.id, d_id))
            print 'rule_device_add:', rule_device_add
            print 'rule_device_del:', rule_device_del

            ##### 处理变更任务组 #####

        for item in rule_device_add:
            add_rule.setdefault(item[1], []).append(item[0])
        for item in rule_device_del:
            del_rule.setdefault(item[1], []).append(item[0])

        print 'add_rule(device_id:rule_id list):', add_rule
        print 'del_rule(device_id:rule_id list):', del_rule

        # 筛选类规则（未知攻击、加密、压缩、图片、通联关系、应用行为）只选择一条 (还会删除其他本次未下发的同类规则中的本次会下发的检测器ID)
        if policy_type in [4, 6, 7, 8, 13, 14]:
            for k, v in add_rule.iteritems():
                add_rule[k] = [v[-1]]
                # rule_info = rule_models[policy_type - 1].objects.filter(
                #     device_id_list__contains='#' + str(k) + '#').exclude(
                #     id=v[-1])
                # if rule_info.exists():
                #     for r in rule_info:
                #         if r.device_id_list == '#' + str(k) + '#':
                #             update_data = ''
                #         else:
                #             update_data = r.device_id_list.replace(str(k) + '#', '')
                #         rule_info.filter(id=r.id).update(device_id_list=update_data, device_id_list_run=update_data)
            new_del_rule = copy.deepcopy(del_rule)
            for k, v in new_del_rule.iteritems():
                if k in add_rule:
                    del del_rule[k]

        print 'new_add_rule:', add_rule
        print 'new_del_rule:', del_rule

        generate_time = du.get_current_time()
        all_rule = {'add': add_rule, 'del': del_rule}
        for k, v in all_rule.iteritems():
            for d_id, r_id_list in v.iteritems():
                version_num = common.cal_task_version([Task, DirectorTask], d_id, 'policy', '1')
                try:
                    task_data = {
                        'module': policy_type,
                        'version': version_num,
                        'cmd': k,
                        'num': len(r_id_list),
                        'config': json.dumps([config_dict[rule_id] for rule_id in r_id_list], encoding='utf-8',
                                             ensure_ascii=False),
                        'generate_time': generate_time,
                        'device_id': d_id,
                        'user': request_data.get('uuid')
                    }
                    task_list.append(task_data)
                except:
                    print '任务生成失败'

        # 更新相应rule表的版本号、状态、操作时间，检测器运行列表更新为检测器变更列表
        # rule_data.update(version=version_num, rule_status=0, operate_time=generate_time, operate='', device_id_list_run=F('device_id_list'))
        rule_data.update(version='', rule_status=0, operate_time=generate_time, operate='', device_id_list_run=F('device_id_list'))

        # ********************* 指挥中心数据 *********************

        if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
            command_data = {}
            if len(command_policy_add) > 0:
                command_data['add'] = command_policy_add
            if len(command_policy_update) > 0:
                command_data['update'] = command_policy_update
            if len(command_policy_del) > 0:
                command_data['del'] = command_policy_del
            if len(command_policy_update_group) > 0:
                command_data['update_task_id'] = command_policy_update_group

            print "upload to director command data:", pu.pretty_print_format(command_data)
            command_data = json.dumps(command_data, ensure_ascii=False).encode('utf-8')

            common_header = ccd.get_common_command_header_of_center('CENTER_POLICY', common.COMMAND_POLICY_TYPE[policy_type - 1],
                                                                    task_type='0')
            ccd.upload_json_2_director_of_center(common_header, common.COMMAND_POLICY_TYPE[policy_type - 1], command_data, async_level=3)

        # ********************* 指挥中心数据 *********************

        if not task_list:
            return common.ui_message_response(200, '没有任务需要生成', '没有任务需要生成', status.HTTP_200_OK)
        else:
            serializer_task = TaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
            else:
                return common.ui_message_response(400, json.dumps(serializer_task.errors), 'task数据缺失或字段不符合规定，序列化出错')

        ####不再通过module_type来确定是否有策略任务需要下发，通过Task表中的is_valid==1字段确认是否有任务下发
        # 将detector_info表中对应检测器的这一模块标记为1，表示该模块有策略下发
        # update_fields = {common.module_fields[policy_type - 1]: 1}
        # operate_device_id_list = list(set(add_rule.keys()) | set(del_rule.keys()))
        # Detector.objects.filter(id__in=operate_device_id_list).update(**update_fields)

        common.generate_system_log(request_data, u'策略操作', u'策略增量下发',
                                   u'策略增量下发' + json.dumps(task_list, cls=qu.CJsonEncoder, encoding='utf-8', ensure_ascii=False))

        if config.const.UPLOAD_BUSINESS_DISPOSAL:
            write_policy_data.process_policy(common.module_names[policy_type-1])

        pu.print_format_tail('增量下发策略')
        return common.ui_message_response(200, '任务生成成功', '任务生成成功', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        common.generate_system_log(request_data, u'策略操作', u'策略增量下发', u'策略增量下发模块异常')
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_fulldose_policy(request):
    """
    全量方式生成策略任务
    :param request:
    :return:
    """
    try:
        pu.print_format_header('管理中心全量下发策略')

        request_data = common.print_header_data(request)  # 获取请求数据

        policy_type = common.check_request_int_field(request_data, 'policy_type')  # 策略模块
        if isinstance(policy_type, Response):
            return policy_type
        device_id_list = request_data.get('detector_id_list')  # 全量下发需选择检测器

        result_set = get_rule_fields(policy_type)  # 获取查询的规则集合

        task_list = []  # 任务

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}  # id与device_id的对应关系
        print '------------全量下发'
        if device_id_list is None:
            return common.ui_message_response(400, '请求url中没有携带参数device_id_list', '请求参数没有device_id_list')
        elif device_id_list == '[]':  # 表示全部检测器
            # device_id_list = id_device_dict.keys()
            device_id_list = id_device_dict.values()
        else:
            device_id_list = [str(d_id) for d_id in json.loads(device_id_list)]

        generate_time = du.get_current_time()
        # rule_data = rule_models[policy_type - 1].objects.filter(
        #     Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'))
        # rule_data = rule_models[policy_type - 1].objects.filter(is_del=1)

        is_device_has_policy = False  # 标识对所有的检测器，是否有策略可以下发
        # 筛选类规则（未知攻击、加密、压缩、图片、通联关系、应用行为）只选择一条
        if policy_type in [4, 6, 7, 8, 13, 14]:
            for d_id in device_id_list:
                if d_id == 0:
                    continue
                director_rule_data = director_rule_models[policy_type - 1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
                rule_data = rule_models[policy_type - 1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
                if not rule_data.exists() and not director_rule_data.exists():
                    print '对于检测器' + d_id + ',指挥中心和管理中心没有可全量下发的策略'
                    continue
                else:
                    is_device_has_policy = is_device_has_policy | True

                director_rule_json = serialize('json', director_rule_data, fields=result_set)
                director_rule_all = json.loads(director_rule_json)
                director_config_list = [director_rule_all[-1]['fields']] if director_rule_all else []

                rule_json = serialize('json', rule_data, fields=result_set)  # 序列化成json
                rule_all = json.loads(rule_json)
                config_list = [rule_all[-1]['fields']] if rule_all else []
                config_list.extend(director_config_list)
                config_list = [config_list[-1]]
                if policy_type in [6, 8]:  # 加密规则或图片规则，修改config的组织方式
                    for config in config_list:
                        config['filesize'] = {"minsize": config.pop('filesize_minsize'),
                                              "maxsize": config.pop('filesize_maxsize')}
                elif policy_type == 7:  # 压缩规则，修改config的组织方式
                    for config in config_list:
                        config['filesize'] = {"backsize": config.pop('backsize'),
                                              "dropsize": config.pop('dropsize')}

                version_num = common.cal_task_version([Task, DirectorTask], d_id, 'policy', '1')
                task_data = {
                    'module': policy_type,
                    'version': version_num,
                    'cmd': 'reset',
                    'num': len(config_list),
                    'config': json.dumps(config_list, encoding='utf-8', ensure_ascii=False),
                    'generate_time': generate_time,
                    'device_id': d_id,
                    'user': request_data.get('uuid'),
                    'is_valid': 1
                }
                task_list.append(task_data)
        else:  # 告警类规则（可以多条规则）
            for d_id in device_id_list:
                if d_id == 0:
                    continue
                director_rule_data = director_rule_models[policy_type - 1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
                rule_data = rule_models[policy_type - 1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
                if not rule_data.exists() and not director_rule_data.exists():
                    print '对于检测器' + d_id + ',指挥中心和管理中心没有可全量下发的策略'
                    continue
                else:
                    is_device_has_policy = is_device_has_policy | True

                director_rule_json = serialize('json', director_rule_data, fields=result_set)
                director_rule_all = json.loads(director_rule_json)
                director_config_list = [data['fields'] for data in director_rule_all] if director_rule_all else []

                rule_json = serialize('json', rule_data, fields=result_set)  # 序列化成json
                rule_all = json.loads(rule_json)
                config_list = [data['fields'] for data in rule_all] if rule_all else []  # config
                config_list.extend(director_config_list)
                if policy_type == 2:  # 漏洞利用规则，修改数字对应的攻击类型
                    for config in config_list:
                        config['attack_type'] = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw'
                                                 ][config['attack_type'] - 1]

                version_num = common.cal_task_version([Task, DirectorTask], d_id, 'policy', '1')
                task_data = {
                    'module': policy_type,
                    'version': version_num,
                    'cmd': 'reset',
                    'num': len(config_list),
                    'config': json.dumps(config_list, encoding='utf-8', ensure_ascii=False),
                    'generate_time': du.get_current_time(),
                    'device_id': d_id,
                    'user': request_data.get('uuid')
                }
                task_list.append(task_data)

        if not is_device_has_policy:
            return common.ui_message_response(200, '没有可全量下发的策略', '没有可全量下发的策略', status.HTTP_200_OK)

        if not task_list:
            return common.ui_message_response(200, '没有任务需要生成', '没有任务需要生成', status.HTTP_200_OK)
        else:
            serializer_task = TaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
                common.generate_system_log(request_data, u'策略操作', u'全量刷新检测器策略',
                                           u'全量刷新检测器策略' + json.dumps(task_list, cls=qu.CJsonEncoder, encoding='utf-8',
                                                                     ensure_ascii=False))
            else:
                common.generate_system_log(request_data, u'策略操作', u'全量刷新检测器策略', u'全量刷新检测器策略，task数据缺失或字段不符合规定，序列化出错')
                return common.ui_message_response(400, json.dumps(serializer_task.errors),
                                                  'task数据缺失或字段不符合规定，序列化出错')
        pu.print_format_tail('全量下发策略')
        return common.ui_message_response(200, 'task生成成功', '任务生成成功', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        common.generate_system_log(request_data, u'策略操作', u'全量刷新检测器策略', u'全量刷新检测器策略模块异常')
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def report_all_rule_to_direct_center(request):
    try:

        pu.print_format_header('全量上报管理中心策略')
        request_data = common.print_header_data(request)

        policy_type = common.check_request_int_field(request_data, 'policy_type')
        if isinstance(policy_type, Response):
            return policy_type

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}  # id与device_id的对应关系

        rule_data = rule_models[policy_type-1].objects.filter(is_del=1, rule_status=0)

        result_set = get_rule_fields(policy_type) + ('group_id', 'device_id_list_run', 'creat_time')
        rule_json = serialize('json', rule_data, fields=result_set + ('remark', ))
        rule_all = json.loads(rule_json)

        command_data_list = []
        for rule in rule_all:
            # print rule['fields']
            fields = rule['fields']
            if policy_type == 2:  # 漏洞利用规则，修改数字对应的攻击类型
                fields['attack_type'] = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw'][
                    fields['attack_type'] - 1]
            elif policy_type in [6, 8]:  # 加密规则或图片规则，修改config的组织方式
                fields['filesize'] = {"minsize": fields.pop('filesize_minsize'),
                                    "maxsize": fields.pop('filesize_maxsize')}
            elif policy_type == 7:  # 压缩规则，修改config的组织方式
                fields['filesize'] = {"backsize": fields.pop('backsize'),
                                    "dropsize": fields.pop('dropsize')}

            # device_id_list_run = fields['device_id_list_run']
            # if device_id_list_run != '#' and device_id_list_run != '':
            #     id_list = map(int, device_id_list_run[1:-1].split("#"))
            #     fields['device_id_list_run'] = '#' + '#'.join([id_device_dict[id] for id in id_list]) + '#'

            if 'creat_time' in fields and fields['creat_time'] is not None:
                fields['create_time'] = fields.pop('creat_time').replace('T', ' ')
            if 'group_id' in fields:
                fields['task_id'] = fields.pop('group_id')
            if 'remark' in fields:
                fields['label'] = fields.pop('remark')


            command_data_list.append(fields)

        command_data = {}
        if command_data_list:
            command_data['sync_director'] = command_data_list

        if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
            print "fulldose upload to director:", pu.pretty_print_format(command_data)

            common_header = ccd.get_common_command_header_of_center('CENTER_POLICY', common.COMMAND_POLICY_TYPE[policy_type - 1],
                                                                    task_type='0')
            ccd.upload_json_2_director_of_center(common_header, common.COMMAND_POLICY_TYPE[policy_type - 1], json.dumps(command_data), async_level=3)

            pu.print_format_tail('全量上报管理中心策略')
            return common.ui_message_response(200, '全量同步管理中心策略到指挥中心成功', '全量同步策略成功', status.HTTP_200_OK)
        else:
            pu.print_format_tail('全量上报管理中心策略')
            return common.ui_message_response(200, '未接入指挥版本', '未接入指挥版本', status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return common.ui_message_response(400, '服务器内部错误', '服务器内部错误')


# 构造任务页面查询条件，用于显示列表信息和总数
def get_task_query_terms(request_data):

    # 获取请求参数
    task_id = request_data.get('task_id')                # 任务ID
    task_module = request_data.get('task_module')        # 任务模块
    task_cmd = request_data.get('task_cmd')              # 任务变更命令
    policy_version = request_data.get('policy_version')  # 任务策略版本号
    device_id = request_data.get('device_id')            # 检测器ID
    # is_success = request_data.get('is_success')  # 实际任务随心跳下发后的任务执行成功状态
    is_valid = request_data.get('is_valid')   # 任务完成状态
    time_min = request_data.get('time_min')              # 任务生成起始时间
    time_max = request_data.get('time_max')              # 任务生成结束时间
    user = request_data.get('user')                      # 操作用户

    query_terms = {}  # 构造查询参数

    if task_id is not None:
        query_terms['id__contains'] = task_id      # 模糊查询
    if task_module is not None:
        query_terms['module'] = task_module
    if task_cmd is not None:                            # 界面与数据库数据转换
        if task_cmd == '1':
            query_terms['cmd'] = 'add'
        elif task_cmd == '2':
            query_terms['cmd'] = 'del'
        elif task_cmd == '3':
            query_terms['cmd'] = 'reset'
        else:
            return common.ui_message_response(400, '请求数据中的task_cmd不是1、2、3',
                                              '请求数据中的task_cmd不正确')
    if policy_version is not None:
        query_terms['version__contains'] = policy_version   # 模糊查询
    if device_id is not None:
        query_terms['device_id__contains'] = device_id  # 模糊查询

    if time_min is not None:   # 生成任务的时间段筛选
        query_terms['generate_time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        query_terms['generate_time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)
    if user is not None:
        query_terms['user__contains'] = user

    is_director = request_data.get('is_director')
    if is_director == '1':
        query_data = DirectorTask.objects.filter(**query_terms)
    else:
        query_data = Task.objects.filter(**query_terms)

    # if is_success is not None:
    #     query_data = query_data.filter(is_success=is_success)

    if is_valid is not None:     # 任务状态 已忽略0 任务执行中1、任务执行成功2、任务执行失败3、任务错误4
        query_data = query_data.filter(is_valid=is_valid)
    return query_data


# 查询所有任务信息
def show_all_tasks(request):
    try:
        request_data = common.print_header_data(request)                    # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_data = get_task_query_terms(request_data)                    # 构造查询参数

        # 过滤查询，若query_terms={}，相当于all
        query_data = query_data.order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data,
                                    fields=('module', 'version', 'cmd', 'num', 'config',
                                            'generate_time', 'release_time', 'is_success', 'is_valid', 'device_id', 'user')
                                    )
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['task_id'] = data['pk']  # 加入主键id
            fields['task_module'] = fields.pop('module')
            fields['policy_version'] = fields.pop('version')

            cmd = fields.pop('cmd')
            if cmd == 'add':
                fields['task_cmd'] = 1
            elif cmd == 'del':
                fields['task_cmd'] = 2
            else:
                fields['task_cmd'] = 3
            fields['task_num'] = fields.pop('num')
            generate_time = fields.pop('generate_time')
            fields['task_generate_time'] = generate_time.replace('T', ' ')  # 去除因序列化时间类型出现的'T'

            release_time = fields.pop('release_time')
            if release_time is not None:
                fields['task_release_time'] = release_time.replace('T', ' ')  # 去除因序列化时间类型出现的'T'
            else:
                fields['task_release_time'] = '0000-00-00 00:00:00'

            # config_list = json.loads(fields['config'])
            # keyword_config = []
            # for config in config_list:
            #     if 'rule_content' in config:
            #         keyword_config.append(config['rule_content'])
            # fields['config'] = json.dumps(keyword_config, ensure_ascii=False) if keyword_config else ''

            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询任务总数
def show_task_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_data = get_task_query_terms(request_data)    # 构造查询参数

        count = query_data.count()
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 将策略任务或命令状态设置为已忽略
def update_to_unvalid(request, is_policy, log_str):
    try:
        # task.cmd-> 0:add 1:reset 2:start 3:stop
        request_data = common.print_header_data(request)
        task_id = request_data.get('id')
        if task_id is not None:
            if is_policy:
                Task.objects.filter(id=task_id).update(is_valid=0)
            else:
                Command.objects.filter(id=task_id).update(is_valid=0)
            common.generate_system_log(request_data, u'' + log_str, u'' + log_str,
                                       u'将' + log_str + request_data.get('id') + u'状态设置为已忽略')
            return common.ui_message_response(200, log_str.encode('utf-8') + '状态设置成功', log_str.encode('utf-8') + '状态设置为已忽略', status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '请求url中没有携带参数id', '请求参数没有id')
    except Exception:
        common.generate_system_log(request_data, u'' + log_str, u'' + log_str,
                                       u'将' + log_str + request_data.get('id') + u'状态设置为已忽略出现错误')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 将策略任务或者命令重新下发
def send_again(request, is_policy, log_str):
    try:
        request_data = common.print_header_data(request)

        # 根据job_id，获取插件任务的相关信息，用来重新下发
        job_id = common.check_request_int_field(request_data, 'id')
        if isinstance(job_id, Response):
            return job_id
        if is_policy:
            task = Task.objects.get(id=job_id)

            # 更新任务的相关信息
            Task.objects.filter(id=job_id).update(generate_time=du.get_current_time(), is_valid=1)

            # 记录日志
            common.generate_system_log(request_data, u'' + log_str, log_str + u'重新下发',
                                       u'将' + log_str + request_data.get('id') + json.dumps(
                                           task.config) + u'重新下发')
        else:
            command = Command.objects.get(id=job_id)
            Command.objects.filter(id=job_id).update(generate_time=du.get_current_time(), is_valid=1)

            # 记录日志
            common.generate_system_log(request_data, u'' + log_str, log_str + u'重新下发',
                                       u'将' + log_str + request_data.get('id') + u'重新下发')



        return common.ui_message_response(200, log_str.encode('utf-8') + '重新下发成功', '重新下发成功', status.HTTP_200_OK)


    except Exception:
        common.generate_system_log(request_data, u'' + log_str, log_str + u'重新下发',
                                   u'将' + log_str + request_data.get('id') + u'重新下发模块程序出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 生成命令
def generate_command(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        cmd_type = request_data.get('cmd')                               # 命令类型
        id_list = request_data.get('id_list')                            # 选择的id列表
        cmd_module = request_data.get('cmd_module')                      # 模块启停命令操作的模块
        sub_module = request_data.get('submodule')                       # 模块启停命令操作的子模块

        param = request_data.get('param')                                # 附件的相对路径
        filename = request_data.get('filename')                          # 附件的文件名

        version_check_method = request_data.get('version_check_method')  # 版本一致性检查的方法
        path = request_data.get('path')                                  # 版本一致性检查ls上传路径
        result = request_data.get('result')                              # 版本一致性检查ls上传结果
        input_filename = request_data.get('input_filename')              # 版本一致性检查的输入文件绝对路径
        offset = request_data.get('offset')                              # 文件起始位置
        length = request_data.get('length')                              # 文件指定长度

        user = request_data.get('user')                                  # 用户名
        password = request_data.get('passwd')                            # 密码

        cmd_type = common.check_request_int_field(request_data, 'cmd')
        if isinstance(cmd_type, Response):
            return cmd_type

        # 查询符合条件的device_id列表，作为命令下发对应的检测器
        id_list = json.loads(id_list)
        # device_id_list = list(Detector.objects.filter(id__in=id_list).values_list('device_id', flat=True))
        device_id_list = id_list
        if not device_id_list:
            return common.ui_message_response(400, '根据条件筛选检测器为空', '没有选择检测器')

        modules_list = ['alarm', 'abnormal', 'sensitive', 'object_listen', 'net_audit', 'block']  # 模块表
        sub_modules_list = [
            'trojan', 'attack', 'malware', 'other', 'abnormal', 'finger_file', 'sensitive_file',
            'keyword_file', 'encryption_file', 'compress_file', 'picture_file', 'style_file',
            'ip_listen', 'domain_listen', 'url_listen', 'account_listen', 'net_log', 'app_behavior',
            'block'
        ]  # 模块启停子模块表

        cmd_data = {}  # 构造命令数据
        if cmd_type == 1 or cmd_type == 2 or cmd_type == 5:   # 关机、重启、时间同步命令（没有参数）
            pass
        elif cmd_type == 3 or cmd_type == 4:                  # 模块启停
            if cmd_module is not None:                        # 请求参数中有cmd_module
                sub_module = json.loads(sub_module)       # 参数是数字列表
                cmd_data['module'] = modules_list[int(cmd_module) - 1]
                cmd_data['submodule'] = json.dumps([sub_modules_list[i - 1] for i in sub_module])
                cmd_data['param'] = json.dumps({
                    'module': cmd_data['module'],
                    'submodule': json.loads(cmd_data['submodule'])
                })
            else:
                return common.ui_message_response(400, '模块启停数据中没有cmd_module', '请求数据中没有cmd_module')
        elif cmd_type == 6:                        # 系统固件升级
            if param is not None:
                file_name = common.MEDIA_ROOT + param
                if os.path.exists(file_name):
                    cmd_data['md5'] = su.calc_md5(file_name)          # md5
                else:
                    return common.ui_message_response(400, '服务器上没有该文件:' + file_name.encode('utf-8'),
                                                      '固件文件不存在')
                with connection.cursor() as cursor:  # 运行mysql函数,生成版本号
                    cursor.execute('select nextversion(%s,%s)', ('firmware', '0'))  # 参数是一个元组
                    version_num = common.get_task_serial(cursor.fetchone()[0])
                cmd_data['soft_version'] = version_num
                cmd_data['filename'] = filename      # 文件名
                cmd_data['save_path'] = param                       # 文件存储相对路径
                cmd_data['param'] = json.dumps({
                    'filename': filename,
                    'md5': cmd_data['md5'],
                    'soft_version': version_num
                })
            else:
                return common.ui_message_response(400, '系统固件升级数据中没有param', '请求数据中没有param')
        elif cmd_type == 7:                          # 版本一致性检查
            if version_check_method is not None:
                if version_check_method == '1':      # 检查方法：读取文件内容方法，检测器返回指定文件内容（base64）
                    file_name = common.MEDIA_ROOT + param
                    cmd_data['param'] = json.dumps({
                        'method': 'get_file',
                        'filename': input_filename,
                        'offset': offset,
                        'length': length
                    })
                    offset = 0 if offset is None else int(offset)
                    length = -1 if length is None or length == '0' else int(length)
                    cmd_data['version_check_result'] = json.dumps(
                        {'get_file': su.get_base64(fu.read_file(file_name, int(offset), int(length)))})
                    cmd_data['save_path'] = param
                    cmd_data['filename'] = filename
                elif version_check_method == '2':    # 检查方法：读取目录文件列表方法
                    cmd_data['param'] = json.dumps({
                        'method': 'ls',
                        'path': path
                    })
                    try:
                        result = json.loads(result)
                    except ValueError:
                        return common.ui_message_response(400, '版本一致性检查读取目录命令填写的结果不是json格式', 
                                                          '读取目录命令填写的结果不符合规范')
                    cmd_data['version_check_result'] = json.dumps({'ls': result})
                elif version_check_method == '3':    # 检查方法：判断文件MD5方法
                    file_name = common.MEDIA_ROOT + param
                    cmd_data['param'] = json.dumps({
                        'method': 'md5sum',
                        'filename': input_filename,
                        'offset': offset,
                        'length': length
                    })
                    offset = 0 if offset is None else int(offset)
                    length = -1 if length is None or length == '0' else int(length)
                    cmd_data['version_check_result'] = json.dumps(
                        {'md5sum': su.get_md5(fu.read_file(file_name, int(offset), int(length)))})
                    cmd_data['save_path'] = param
                    cmd_data['filename'] = filename
                else:
                    return common.ui_message_response(400, '版本一致性检查数据中的version_check_method不是1、2、3',
                                                      '请求数据中不合法')
            else:
                return common.ui_message_response(400, '版本一致性检查数据中没有version_check_method',
                                                  '请求数据缺少必要的参数')
        elif cmd_type == 8:                          # 内置策略更新
            if param is not None:  # 请求参数中有param
                file_name = common.MEDIA_ROOT + param
                if os.path.exists(file_name):
                    cmd_data['md5'] = su.calc_md5(file_name)    # md5
                    cmd_data['filename'] = filename  # 文件名
                    cmd_data['save_path'] = param                   # 文件存储相对路径
                    cmd_data['param'] = json.dumps({
                        'filename': filename,
                        'md5': cmd_data['md5'],
                    })
                else:
                    return common.ui_message_response(400, '服务器上没有该文件:' + file_name.encode('utf-8'),
                                                      '固件文件不存在')
            else:
                return common.ui_message_response(400, '内置策略更新数据中没有param', '请求数据中没有param')
        elif cmd_type == 9:                                 # 本地WEB管理用户密码重置命令
            if user is not None and password is not None:
                cmd_data['param'] = json.dumps({'user': user, 'passwd': password})
            else:
                return common.ui_message_response(400, '用户密码重置数据中没有user或passwd', '请求数据中缺少必要参数')
        else:
            return common.ui_message_response(400, '请求数据中的cmd不符合要求', '请求数据中的cmd不合法')

        cmd_data['cmd_type'] = cmd_type
        cmd_data['generate_time'] = du.get_current_date_string()  # 获取当前时间
        # cmd_data['version'] = version_num

        print '管理中心生成命令任务'
        command_list = []
        for device_id in device_id_list:
            version_num = common.cal_task_version([Command, DirectorCommand], device_id, 'command', '3')
            command = copy.deepcopy(cmd_data)
            command['version'] = version_num
            command['device_id'] = device_id
            command_list.append(command)

        print 'command_list:', pu.pretty_print_format(command_list)
        serializer_cmd = CommandSerializer(data=command_list, many=True)
        if serializer_cmd.is_valid():
            serializer_cmd.save()  # 存储数据库command
            common.generate_system_log(request_data, u'命令操作', u'下发命令',
                                       u'给检测器列表' + json.dumps(device_id_list) + u'生成' + common.COMMAND_TYPE[
                                           cmd_type - 1] + u'命令')
        else:
            common.generate_system_log(request_data, u'命令操作', u'下发命令',
                                       u'给检测器列表' + json.dumps(device_id_list) + u'生成' + common.COMMAND_TYPE[
                                           cmd_type - 1] + u'命令，数据缺失或字段不符合规定，序列化出错')
            return common.ui_message_response(400, json.dumps(serializer_cmd.errors),
                                              '数据缺失或字段不符合规定，序列化出错')

        return common.ui_message_response(200, '命令生成成功', '命令生成成功', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'命令操作', u'下发命令', u'生成' + common.COMMAND_TYPE[cmd_type - 1] + u'命令模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 构造命令页面查询条件，用于显示列表信息和总数
def get_command_query_terms(request_data):

    # 获取请求参数
    cmd_id = request_data.get('cmd_id')         # 命令ID
    device_id = request_data.get('device_id')   # 检测器编号
    cmd_type = request_data.get('cmd_type')     # 命令类型
    time_min = request_data.get('time_min')     # 命令生成起始时间
    time_max = request_data.get('time_max')     # 命令生成结束时间

    # is_success = request_data.get('is_success')  # 实际任务随心跳下发后的任务执行成功状态
    is_valid = request_data.get('is_valid')   # 任务完成状态

    query_terms = {}  # 构造查询参数

    if cmd_id is not None:
        query_terms['id__contains'] = int(cmd_id)    # 模糊搜索
    if cmd_type is not None:
        query_terms['cmd_type'] = int(cmd_type)

    if time_min is not None:  # 生成命令的时间段筛选
        query_terms['generate_time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        query_terms['generate_time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

    is_director = request_data.get('is_director')
    if is_director == '1':
        query_data = DirectorCommand.objects.filter(**query_terms)
    else:
        query_data = Command.objects.filter(**query_terms)

    # if is_success is not None:
    #     query_data = query_data.filter(is_success=is_success)

    if is_valid is not None:     # 任务状态 已忽略0 任务执行中1、任务执行成功2、任务执行失败3、任务错误4
        query_data = query_data.filter(is_valid=is_valid)
    return query_data


# 查询所有命令信息
def show_all_commands(request):
    try:
        request_data = common.print_header_data(request)                    # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_data = get_command_query_terms(request_data)                 # 获取查询参数

        # 过滤查询，若query_terms={}，相当于all
        query_data = query_data.order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data,
                                    fields=('cmd_type', 'generate_time', 'release_time', 'device_id', 'is_valid', 'is_success', 'version', 'version_check_result', 'version_check_post', 'command_result', 'save_path', 'filename', 'param'))

        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['cmd_id'] = data['pk']                    # 加入主键id
            generate_time = fields['generate_time']
            if generate_time is not None:
                fields['generate_time'] = generate_time.replace('T', ' ')  # 去除因序列化时间类型出现的'T'

            release_time = fields['release_time']
            if release_time is not None:
                fields['release_time'] = release_time.replace('T', ' ')  # 去除因序列化时间类型出现的'T'
            # fields['check_post'] = fields.pop('command_result')

            show_data.append(fields)

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询命令总数
def show_command_count(request):
    try:
        request_data = common.print_header_data(request)      # 获取请求数据
        query_data = get_command_query_terms(request_data)   # 构造查询参数

        count = query_data.count()
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 判断是否生成任务
def judge_policy_generation(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        policy_type = common.check_request_int_field(request_data, 'policy_type')  # 策略模块
        if isinstance(policy_type, Response):
            return policy_type
        operate_type = common.check_request_int_field(request_data, 'type')  # 操作类型 （0：增量，1：全量）
        if isinstance(operate_type, Response):
            return operate_type
        if operate_type == 0:  # 增量
            # 查询所有未生成任务的规则数量
            amount = rule_models[policy_type - 1].objects.filter(rule_status=1).count()
            # amount = rule_models[policy_type - 1].objects.filter(
            #     ~Q(device_id_list_run=F('device_id_list')) | Q(operate__contains='group'), rule_status=1).count()   #这里认为 对于之前的生效范围和设置生效范围的一样的话就不进行增量操作

            if amount == 0:
                return common.ui_message_response(200, '没有策略需要生成', amount, status.HTTP_200_OK)
            else:
                return common.ui_message_response(200, '有策略需要生成', amount, status.HTTP_200_OK)
        elif operate_type == 1:  # 全量
            # 查询没有标记删除的规则（作为一条全量下发任务的config）的数量
            reset_amount = rule_models[policy_type - 1].objects.filter(is_del=1).count()
            # # 查询所有add类型的规则和del类型未生成任务的规则（作为一条全量下发任务的config）的数量
            # reset_amount = rule_models[policy_type - 1].objects.exclude(operate='del', rule_status=0).count()
            if reset_amount == 0:
                return common.ui_message_response(200, '没有策略需要生成', reset_amount, status.HTTP_200_OK)
            else:
                return common.ui_message_response(200, '有策略需要生成', reset_amount, status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '请求参数type不是0、1', '请求参数type不合法')

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# ************************************** 处理前端检测器请求 **************************************

def send_echo_2_director(model, task_id_list, job_type=0, data={'code': 200, 'msg': '任务已下发至检测器'}):
    """
    发送ECHO消息指到指挥中心
    :param model:            策略还是插件任务Model
    :param task_id_list:     下发的任务主键ID列表
    :param job_type:         标识是任务类型，0：策略、1：插件、2：命令
    :param data
    :return:
    """
    # print '准备发送echo', pu.pretty_print_format(task_id_list)
    for task_id in task_id_list:
        task = model.objects.get(id=task_id)
        down_job_id = task.down_job_id
        # print 'job_id:', down_job_id
        all_release = True
        finish_task = 0
        not_finish_task = 0
        for task in model.objects.filter(down_job_id=down_job_id):
            if task.is_valid == 1:
                print '未完成的任务->task_version', task.version, 'job_id:', task.down_job_id
                all_release = False
                not_finish_task += 1
            else:
                if task.is_valid == 2:
                    finish_task += 1

        business_type = ''
        source_type = 'ECHO_DIRECTOR_POLICY'
        finish_rate = int(finish_task * 1.0 / (finish_task + not_finish_task) * 100)
        if not_finish_task > 0:
            if job_type == 0:
                business_type = 'ECHO_' + common.DIRECTOR_POLICY_TYPE[task.module - 1]
                data = {'code': 100, 'msg': '策略下发进度(' + str(finish_rate) + '%)'}
            elif job_type == 1:
                business_type = 'ECHO_DIRECTOR_PLUG_SYNC'
                source_type = 'ECHO_DIRECTOR_PLUG'
                data = {'code': 100, 'msg': '插件下发进度(' + str(finish_rate) + '%)'}
            else:
                source_type = 'ECHO_DIRECTOR_COMMAND'
                business_type = 'ECHO_DIRECTOR_COMMAND_SYNC'
                data = {'code': 100, 'msg': '命令下发进度(' + str(finish_rate) + '%)'}
        else:
            if job_type == 0:
                business_type = 'ECHO_' + common.DIRECTOR_POLICY_TYPE[task.module - 1]
                set_policy_job_finished(down_job_id, 2, data['msg'])
            elif job_type == 1:
                business_type = 'ECHO_DIRECTOR_PLUG_SYNC'
                source_type = 'ECHO_DIRECTOR_PLUG'
                set_plugin_job_finished(down_job_id, 2, data['msg'])
            else:
                source_type = 'ECHO_DIRECTOR_COMMAND'
                business_type = 'ECHO_DIRECTOR_COMMAND_SYNC'
                set_command_job_finished(down_job_id, 2, data['msg'])

        # echo消息
        echo_header = {
            'Dst-Node': task.down_node_id,
            'Src-Node': dc.SRC_NODE,
            'Src-Center': dc.SRC_CENTER_ID,
            'Msg-Type': 'echo',
            'Content-Type': 'application/json',
            'version': '1.0',
            # 'Cookie': 'unknown',
            'Data-Type': 'msg',
            'Task-Type': '0',
            'User-Agent': dc.CENTER_USER_AGENT,
            'Capture-Date': time.strftime('%a, %d %b %Y %H:%M:%S'),
            'Source_Type': source_type,
            'BusinessData-Type': business_type,
            'X-Forwarded-For': dc.detect_center_host,
            'Channel-Tpye': 'JCQ'
        }

        echo_data = {
            "job_id": down_job_id,
            "resp_final": data['code'],
            "r_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "resp_msg": data['msg']
        }

        if not_finish_task == 0:
            print u"#####指挥中心同步生成" + source_type + "任务全部下发, 发送" + business_type + u"消息"
        else:
            print u"#####指挥中心同步生成" + source_type + "任务进度(" + str(finish_rate) + "%), 发送" + business_type + u"消息"
        sender.send_director(dc.DIRECTOR_URL, dc.SRC_CENTER_ID, business_type, echo_header,
                             data=json.dumps(echo_data))


# 心跳处理，下发策略、命令、插件和插件策略
def process_heartbeat(request):
    try:
        report_time = du.get_current_time()  # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'heartbeat', 1))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'heartbeat', 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        # 测试业务系统队列
        # print "11111111111111111111111"
        # if not config.const.UPLOAD_BUSINESS:
        #     print "222222222222222222222222"
        #     sender.async_send_business_data('哈哈哈哈哈', '哈哈哈哈哈', '180506010001', [({'abc': 'abc'}, {'abc': 'abc'})])


        detector_info = Detector.objects.filter(device_id=detector_id)
        # judge_online.record_online_event(detector_id)
        detector_info.update(heartbeat_time=report_time)   # 更新最后一次心跳时间
        # detector_info.update(heartbeat_time=report_time, is_online=True)   # 更新最后一次心跳时间

        # module_type = detector_info.values(*common.module_fields)[0]   # 模块策略是否可以下发标志
        version_check_type = detector_info[0].version_check_type  # 版本一致性检查是否可以下发标志

        release_data = []  # 下发的策略、命令和插件列表

        # 可以下发的策略
        policy_data = Task.objects.filter(device_id=detector_id, is_valid=1)

        director_policy_data = DirectorTask.objects.filter(device_id=detector_id, is_valid=1)

        # 可以下发的命令（不包括版本一致性检查）
        # cmd_data = Command.objects.filter(device_id=detector_id, is_valid=1).exclude(cmd_type=7)
        cmd_data = Command.objects.filter(device_id=detector_id, is_valid=1)

        # director_cmd_data = DirectorCommand.objects.filter(device_id=detector_id, is_valid=1).exclude(cmd_type=7)
        director_cmd_data = DirectorCommand.objects.filter(device_id=detector_id, is_valid=1)

        # print "director_cmd_data:", pu.pretty_print_format(director_cmd_data)

        ######测试修改后的插件下发
        plug_data = PlugTask.objects.filter(is_valid=1, device_id=detector_id)

        director_plug_data = DirectorPluginTask.objects.filter(device_id=detector_id, is_valid=1)

        if not (policy_data.exists() or director_policy_data.exists() or cmd_data.exists() or director_cmd_data.exists() or plug_data.exists() or director_plug_data.exists()):
            return common.detector_message_response(200, '没有策略(命令、插件、插件策略)下发', [],
                                                    status.HTTP_200_OK)

        release_time = du.get_current_time()   # 下发策略的时间


        if policy_data.exists():
            new_module_list = []  # 控制每一个模块只下发一条策略，保证增量下发
            task_id_list = []  # 下发的策略id
            for task in policy_data:
                if task.module not in new_module_list:

                    # print '@@@@@@@@@@@@@@@@@', task.config.encode('utf-8')
                    policy = {'type': 'policy', 'module': common.module_names[task.module - 1],
                              'version': task.version, 'cmd': task.cmd, 'num': task.num,
                              'config': su.get_base64(task.config.encode('utf-8'))}
                    release_data.append(policy)
                    new_module_list.append(task.module)
                    task_id_list.append(task.id)
            if task_id_list:  # 更新task表,is_valid=2表示策略正在执行   ###########现在默认任务执行成功
                Task.objects.filter(id__in=task_id_list).update(is_valid=2, release_time=release_time)


        # 下发指挥中心的的策略
        if director_policy_data.exists():
            new_module_list = []  # 控制每一个模块只下发一条策略，保证增量下发
            task_id_list = []  # 下发的策略id
            for task in director_policy_data:
                if task.module not in new_module_list:
                    policy = {'type': 'policy', 'module': common.module_names[task.module - 1],
                              'version': task.version, 'cmd': task.cmd, 'num': task.num,
                              'config': su.get_base64(task.config.encode('utf-8'))}
                    release_data.append(policy)
                    new_module_list.append(task.module)
                    task_id_list.append(task.id)
            if task_id_list:  # 更新task表,is_valid=2表示策略正在执行   ###########现在默认任务执行成功
                DirectorTask.objects.filter(id__in=task_id_list).update(is_valid=2, release_time=release_time)
                send_echo_2_director(DirectorTask, task_id_list)



        if cmd_data.exists():   # 命令（一次下发一条）
            # c_data = cmd_data[0]
            # for c_data in cmd_data:
            c_data = cmd_data[0]
            cmd = {
                'type': 'command',
                'cmd': common.cmd_names[c_data.cmd_type - 1]
            }
            if c_data.cmd_type in [1, 2]:  # 关机、重启命令，没有参数
                pass
            elif c_data.cmd_type == 5:  # 时间同步命令
                cmd['param'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            else:   # 其他已填充param命令
                cmd['param'] = json.loads(c_data.param)
            release_data.append(cmd)
            Command.objects.filter(id=c_data.id).update(is_valid=2, release_time=release_time, command_result='已下发')

        # 指挥命令
        if director_cmd_data.exists():   # 命令（一次下发一条）
            # c_data = cmd_data[0]
            # for c_data in cmd_data:
            c_data = director_cmd_data[0]
            cmd = {
                'type': 'command',
                'cmd': common.cmd_names[c_data.cmd_type - 1]
            }
            if c_data.cmd_type in [1, 2]:  # 关机、重启命令，没有参数
                pass
            elif c_data.cmd_type == 5:  # 时间同步命令
                cmd['param'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            else:   # 其他已填充param命令
                cmd['param'] = json.loads(c_data.param)
            release_data.append(cmd)
            DirectorCommand.objects.filter(id=c_data.id).update(is_valid=2, release_time=release_time, command_result='已下发')
            if c_data.cmd_type != 7:
                send_echo_2_director(DirectorCommand, [c_data.id], job_type=2)

        # 测试修改后的插件下发
        # plug_data = PlugTask.objects.filter(is_success=0, device_id=detector_id).order_by('-id')
        if plug_data.exists():
            for plug_task in plug_data:
                for command in json.loads(plug_task.config):
                    release_data.append(command)
            plug_data.update(is_valid=2, release_time=du.get_current_time())  # 现在默认任务随心跳下发后就执行成功

        # 下发指挥中心插件
        if director_plug_data.exists():
            task_id_list = []  # 下发的策略id
            for plug_task in director_plug_data:
                for command in json.loads(plug_task.config):
                    release_data.append(command)
                    task_id_list.append(plug_task.id)
            if task_id_list:  # 更新task表,is_valid=2表示策略正在执行   ###########现在默认任务执行成功
                director_plug_data.update(is_valid=2, release_time=du.get_current_time())  # 现在默认任务随心跳下发后就执行成功
                send_echo_2_director(DirectorPluginTask, task_id_list, job_type=1)


        return common.detector_message_response(200, '下发成功', release_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', {'message': '服务器内部错误'},
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 同步时间
def sync_time(request):
    try:
        # common.print_header_data(request)              # 打印请求头和请求数据
        detector_id = common.check_detector_available(request, Detector)
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'sync_time', 1))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'sync_time', 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')
        
        return common.detector_message_response(200, '同步时间成功',
                                                {'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())},
                                                status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', {'message': '服务器内部错误'},
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 检测器下载升级文件
def download_update_firmware(request, sub_function_dir):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        detector_id = common.check_detector_available(request, Detector)
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'firmware_update', 1))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'firmware_update', 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')
        
        file_name = request_data.get('filename')    # 文件名
        version = request_data.get('version')       # 版本号
        command_info = Command.objects.filter(filename=file_name, soft_version=version).order_by('-id')
        director_command_info = DirectorCommand.objects.filter(filename=file_name, soft_version=version).order_by('-id')
        if command_info.exists() or director_command_info.exists():
            if command_info.exists():
                save_path = sub_function_dir + command_info[0].save_path
            else:
                save_path = sub_function_dir + director_command_info[0].save_path
            file_path = os.path.join(common.MEDIA_ROOT, save_path)
            return common.construct_download_file_header(file_path, save_path, file_name, cal_md5=True)
        else:
            return common.detector_message_response(400, '数据库查询不到该记录', '所需升级文件不存在')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 检测器上传版本一致性检查信息
def process_version_check(request):
    try:
        # report_time = du.get_current_time()           # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)
        if isinstance(detector_id, Response):
            return detector_id

        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'version_check', 1))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'version_check', 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')
        
        version_check_info = Command.objects.filter(device_id=detector_id, is_valid=2, cmd_type=7, command_result='已下发')
        director_version_check_info = DirectorCommand.objects.filter(device_id=detector_id, is_valid=2, cmd_type=7, command_result='已下发')
        if version_check_info.exists() or director_version_check_info.exists():
            if version_check_info.exists():
                command = version_check_info.order_by('-id')[0]   # 刚下发的版本一致性检测命令
                report_data = json.dumps(request_data)
                save_data = command.version_check_result
                result = '一致' if report_data == save_data else '不一致'

                Command.objects.filter(id=command.id).update(version_check_post=report_data, command_result=result)
            if director_version_check_info.exists():
                command = director_version_check_info.order_by('-id')[0]  # 刚下发的版本一致性检测命令
                report_data = json.dumps(request_data)
                save_data = command.version_check_result
                result = '一致' if report_data == save_data else '不一致'

                DirectorCommand.objects.filter(id=command.id).update(version_check_post=report_data, command_result=result)
                send_version_check_echo_2_director([command.id])
        else:
            return common.detector_message_response(400, '数据库没有版本一致性检查的命令',
                                                    '没有下发过版本一致性检查的命令')

        return common.detector_message_response(200, '数据接收成功', {'message': 'success'}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_version_check_echo_2_director(task_id_list):
    """
    发送ECHO消息指到指挥中心
    :param task_id_list:     下发的任务主键ID列表
    :return:
    """
    # print '准备发送echo', pu.pretty_print_format(task_id_list)
    for task_id in task_id_list:
        task = DirectorCommand.objects.get(id=task_id)
        down_job_id = task.down_job_id
        # print 'job_id:', down_job_id
        all_release = True
        finish_task = 0
        not_finish_task = 0
        msg = {}
        for task in DirectorCommand.objects.filter(down_job_id=down_job_id):

            print task.command_result, task.version, task.is_valid
            if task.is_valid == 2 and task.command_result.find('下发') > -1:
                print '未完成的任务->task_version', task.version, 'job_id:', task.down_job_id
                all_release = False
                not_finish_task += 1
            else:
                if task.is_valid == 2:
                    finish_task += 1
                    msg[task.device_id] = task.command_result
        source_type = 'ECHO_DIRECTOR_COMMAND'
        business_type = 'ECHO_DIRECTOR_COMMAND_SYNC'
        finish_rate = int(finish_task * 1.0 / (finish_task + not_finish_task) * 100)

        if not_finish_task > 0:
            data = {'code': 100, 'msg': "一致性命令完成进度(" + str(finish_rate) + "): " + json.dumps(msg, ensure_ascii=False).encode('utf-8')}
        else:
            data = {'code': 200, 'msg': "一致性命令已完成: " + json.dumps(msg, ensure_ascii=False).encode('utf-8')}
            set_command_job_finished(down_job_id, 2, data['msg'])

        # echo消息
        echo_header = {
            'Dst-Node': task.down_node_id,
            'Src-Node': dc.SRC_NODE,
            'Src-Center': dc.SRC_CENTER_ID,
            'Msg-Type': 'echo',
            'Content-Type': 'application/json',
            'version': '1.0',
            # 'Cookie': 'unknown',
            'Data-Type': 'msg',
            'Task-Type': '0',
            'User-Agent': dc.CENTER_USER_AGENT,
            'Capture-Date': time.strftime('%a, %d %b %Y %H:%M:%S'),
            'Source_Type': source_type,
            'BusinessData-Type': business_type,
            'X-Forwarded-For': dc.detect_center_host,
            'Channel-Tpye': 'JCQ'
        }

        echo_data = {
            "job_id": down_job_id,
            "resp_final": data['code'],
            "r_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "resp_msg": data['msg']
        }

        if not_finish_task == 0:
            print u"#####指挥中心同步生成" + source_type + "任务全部下发, 发送" + business_type + u"消息"
        else:
            print u"#####指挥中心同步生成" + source_type + "任务进度(" + str(finish_rate) + "%), 发送" + business_type + u"消息"
        sender.send_director(dc.DIRECTOR_URL, dc.SRC_CENTER_ID, business_type, echo_header,
                             data=json.dumps(echo_data))


# 检测器下载内置策略
def download_inner_policy(request, sub_function_dir):
    try:
        # report_time = du.get_current_time()           # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'inner_policy', 1))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'inner_policy', 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')
        
        file_name = request_data.get('filename')    # 文件名
        command_info = Command.objects.filter(filename=file_name).order_by('-id')
        director_command_info = DirectorCommand.objects.filter(filename=file_name).order_by('-id')
        if command_info.exists() or director_command_info.exists():
            if command_info.exists():
                save_path = sub_function_dir + command_info[0].save_path
            else:
                save_path = sub_function_dir + director_command_info[0].save_path
            file_path = os.path.join(common.MEDIA_ROOT, save_path)
            return common.construct_download_file_header(file_path, save_path, file_name, cal_md5=True)
        else:
            return common.detector_message_response(400, '数据库查询不到该记录', '内置策略不存在')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', {'message': '服务器内部错误'},
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
