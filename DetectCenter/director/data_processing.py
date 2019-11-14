# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, F
from django.db import connection
from django.core.serializers import serialize
from DetectCenter import sender, common, security_util as su, date_util as du, file_util as fu, queryset_util as qu, config, print_util as pu, hardware_util as hu, director_config as dc, https_requests as requests
from plugin.data_processing import result_set as plug_result_set, get_plug_fields, add_plugin_operate
from detector.models import Detector
from director_serializers import *
from policy.models import *
from plugin.models import PluginDetector, PlugTask
from plugin.plugin_serializers import PlugTaskSerializer
import heartbeat

from detect_center_reg_auth import check_global_director_connection

import traceback
import json
import time
import os
import copy
import xlrd
from policy import write_policy_data


rule_models = [
    TrojanRule, AttackRule, MalwareRule, AbnormalRule,
    KeywordRule, EncryptionRule, CompressRule, PictureRule,
    IPListenRule, DNSListenRule, URLListenRule, AccountListenRule,
    NetLogRule, AppBehaviorRule, WebFilterRule, DNSFilterRule,
    IPWhiteListRule, BlockRule
]  # 模型列表


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


director_rule_models = [
    DirectorTrojanRule, DirectorAttackRule, DirectorMalwareRule, DirectorAbnormalRule,
    DirectorKeywordRule, DirectorEncryptionRule, DirectorCompressRule, DirectorPictureRule,
    DirectorIPListenRule, DirectorDNSListenRule, DirectorURLListenRule, DirectorAccountListenRule,
    DirectorNetLogRule, DirectorAppBehaviorRule, DirectorWebFilterRule, DirectorDNSFilterRule,
    DirectorIPWhiteListRule, DirectorBlockRule
]  # 模型列表

director_rule_serializers = [
    DirectorTrojanRuleSerializer, DirectorAttackRuleSerializer, DirectorMalwareRuleSerializer,
    DirectorAbnormalRuleSerializer, DirectorKeywordRuleSerializer, DirectorEncryptionRuleSerializer,
    DirectorCompressRuleSerializer, DirectorPictureRuleSerializer, DirectorIPListenRuleSerializer,
    DirectorDNSListenRuleSerializer, DirectorURLListenRuleSerializer, DirectorAccountListenRuleSerializer,
    DirectorNetLogRuleSerializer, DirectorAppBehaviorRuleSerializer, DirectorWebFilterRuleSerializer,
    DirectorDNSFilterRuleSerializer, DirectorIPWhiteListRuleSerializer, DirectorBlockRuleSerializer
]  # 序列化类列表

director_database_tables = [
    'director_rule_trojan', 'director_rule_attack', 'director_rule_malware', 'director_rule_abnormal',
    'director_rule_keyword_file', 'director_rule_encryption_file', 'director_rule_compress_file',
    'director_rule_picture_filter', 'director_rule_ip_listen', 'director_rule_dns_listen', 
    'director_rule_url_listen', 'director_rule_account_listen', 'director_rule_net_log', 
    'director_rule_app_behavior', 'director_rule_web_filter', 'director_rule_dns_filter',
    'director_rule_ip_whitelist', 'director_rule_block',
]  # 数据库表


# **************************************** 处理指挥中心数据 ****************************************


def save_policy_job(header, issue_type):
    job_id = header['HTTP_JOB_ID']
    policy_job = DirectorPolicyJob.objects.filter(job_id=job_id)
    if policy_job.exists():
        policy_job.update(receive_time=du.get_current_time(), is_valid=1, issue_times=F('issue_times')+1)
        DirectorTask.objects.filter(down_job_id=job_id).update(is_valid=0)   # 将之前生成的所有任务置为无效
    else:
        data = {
            'job_id': job_id,
            'src_node': header['HTTP_SRC_NODE'],
            'issue_type': issue_type,
            'policy_type': common.DIRECTOR_POLICY_TYPE.index(header['HTTP_BUSINESSDATA_TYPE']) + 1,
            'receive_time': du.get_current_date_string(),
            'is_valid': 1
        }
        serialize_data = DirectorPolicyJobSerializer(data=data)
        if serialize_data.is_valid():
            serialize_data.save()
        else:
            print '保存指挥中心下行策略JOB异常', serialize_data.errors


def set_policy_job_finished(job_id, finish_type, job_result):
    DirectorPolicyJob.objects.filter(job_id=job_id).update(is_valid=finish_type, success_time=du.get_current_time(), job_result=job_result)


def save_plugin_job(header, issue_type):
    job_id = header['HTTP_JOB_ID']
    plugin_job = DirectorPluginJob.objects.filter(job_id=job_id)
    if plugin_job.exists():
        plugin_job.update(receive_time=du.get_current_time(), is_valid=1, issue_times=F('issue_times')+1)
        DirectorPluginTask.objects.filter(down_job_id=job_id).update(is_valid=0)   # 将之前生成的所有任务置为无效
    else:
        data = {
            'job_id': job_id,
            'src_node': header['HTTP_SRC_NODE'],
            'issue_type': issue_type,
            'receive_time': du.get_current_date_string(),
            'is_valid': 1
        }
        serialize_data = DirectorPluginJobSerializer(data=data)
        if serialize_data.is_valid():
            serialize_data.save()
        else:
            print '保存指挥中心下行插件JOB异常', serialize_data.errors


def set_plugin_job_finished(job_id, finish_type, job_result):
    DirectorPluginJob.objects.filter(job_id=job_id).update(is_valid=finish_type, success_time=du.get_current_time(), job_result=job_result)


def save_command_job(header, issue_type, cmd_type):
    job_id = header['HTTP_JOB_ID']
    command_job = DirectorCommandJob.objects.filter(job_id=job_id)
    if command_job.exists():
        command_job.update(receive_time=du.get_current_time(), is_valid=1, issue_times=F('issue_times')+1)
        DirectorCommand.objects.filter(down_job_id=job_id).update(is_valid=0)   # 将之前生成的所有任务置为无效
    else:
        data = {
            'job_id': job_id,
            'src_node': header['HTTP_SRC_NODE'],
            'cmd_type': cmd_type,
            'issue_type': issue_type,
            'receive_time': du.get_current_date_string(),
            'is_valid': 1
        }
        serialize_data = DirectorCommandJobSerializer(data=data)
        if serialize_data.is_valid():
            serialize_data.save()
        else:
            print '保存指挥中心下行命令JOB异常', serialize_data.errors


def set_command_job_finished(job_id, finish_type, job_result):
    DirectorCommandJob.objects.filter(job_id=job_id).update(is_valid=finish_type, success_time=du.get_current_time(), job_result=job_result)


# 接收指挥中心某一监测模块的策略变化信息
def receive_policy(request):
    try:
        result = check_down_director_ip_valid(request)  # 校验是否接收指挥中心数据及指挥中心IP是否合法
        if isinstance(result, Response):
            return result

        report_time = du.get_current_date_string()  # 获取当前时间
        # report_time = time.strftime('%Y-%m-%d %H:%M:%S')
        request_header = request.META            # 获取请求头
        # request_data = common.print_header_data(request)
        try:
            request_data = json.loads(request.body)  # 获取请求数据
        except:
            return common.ui_message_response(400, '请求数据不是json格式', '请求数据不符合规定')
        print 'data:', pu.pretty_print_format(request_data)

        business_type = request_header.get('HTTP_BUSINESSDATA_TYPE')
        if business_type in common.DIRECTOR_POLICY_TYPE:
            policy_type = common.DIRECTOR_POLICY_TYPE.index(business_type)
        else:
            return common.ui_message_response(400, 'BusinessData-Type字段不符合规定', 'BusinessData-Type字段不符合规定')

        if not isinstance(request_data, dict):  # 判断请求数据类型是否合规
            return common.detector_message_response(400, '请求数据不是json格式', '请求数据不符合规定')
        else:
            data = request_data.copy()  # request_data是 immutable QueryDict 对象，需要转变

        # reset center
        if 'sync_center' in data and data['sync_center']:

            save_policy_job(request_header, 2)     # 保存JOB

            sync_policy = data['sync_center']

            sync_policy_id_list = [policy['rule_id'] for policy in sync_policy]
            center_director_policy_id_list = [policy.rule_id for policy in director_rule_models[policy_type].objects.filter(is_del=1, rule_status=0)]
            del_id_list = list(set(center_director_policy_id_list) - set(sync_policy_id_list))
            del_policy = director_rule_models[policy_type].objects.filter(rule_id__in=del_id_list)
            if del_policy.exists():
                del_policy.update(is_del=0)
                print "设置以下策略：", pu.pretty_print_format(del_id_list), "状态为已删除"

            add_sync = []
            for rule in sync_policy:

                convert_policy_common_field(rule, common.DIRECTOR_POLICY_TYPE.index(request_header['HTTP_BUSINESSDATA_TYPE']) + 1)

                if 'command_node_id' in rule:
                    rule['src_node'] = rule.pop('command_node_id')
                else:
                    rule['src_node'] = request_header['HTTP_SRC_NODE']

                if 'virtual_group_id' in rule:
                    del rule['virtual_group_id']
                if 'manage_id' in rule:
                    del rule['manage_id']

                rule['receive_time'] = report_time
                if 'create_time' in rule:
                    rule['creat_time'] = rule.pop('create_time')
                # rule['operate'] = 'add' if rule['is_del'] == 1 else 'del'
                query_data = director_rule_models[policy_type].objects.filter(rule_id=rule['rule_id'], is_del=1)
                if query_data.exists():
                    rule['is_del'] = 1
                    if query_data[0].device_id_list != rule.get('device_id_list_run'):
                        rule['rule_status'] = 1
                        if query_data[0].operate == 'add':
                            rule['operate'] = 'add'
                        else:
                            rule['operate'] = 'change#' + query_data[0].operate
                        rule['device_id_list'] = rule.pop('device_id_list_run')

                    query_data.update(**rule)
                else:
                    # 获取管理中心本地的时候有与指挥下发的相同的策略
                    rule['map_rule_id_list'] = common.check_center_director_rule_is_equal(rule, policy_type + 1,
                                                                                          rule_models[policy_type])

                    if 'is_del' in rule and rule['is_del'] == 0:
                        rule['operate'] = 'del'
                    else:
                        rule['operate'] = 'add'
                        rule['device_id_list'] = rule.pop('device_id_list_run')
                        rule['device_id_list_run'] = ''
                    rule['rule_status'] = 1
                    add_sync.append(rule)
            serializer_data = director_rule_serializers[policy_type](data=add_sync, many=True)
            if serializer_data.is_valid():
                serializer_data.save()
            elif common.is_serial_id_overflow_errer(serializer_data.errors):
                for rule in add_sync:
                    director_rule_models[policy_type].objects.create(**rule)
            else:
                return common.ui_message_response(400, json.dumps(serializer_data.errors), '数据缺失或字段不符合规定，序列化出错')

            # 生成增量任务
            result = generate_increment_policy(policy_type+1, director_down_header=request_header)
            if result[0] == 0:
                set_policy_job_finished(request_header['HTTP_JOB_ID'], 2, result[1])
                send_echo_2_no_task(request_header, {'code': 200, 'msg': result[1]})
            elif result[0] == 2:
                set_policy_job_finished(request_header['HTTP_JOB_ID'], 3, result[1])
                send_echo_2_no_task(request_header, {'code': 400, 'msg': result[1]})

        # reset detector
        elif 'sync_device' in data and data['sync_device']:
            save_policy_job(request_header, 1)  # 保存JOB

            # 指挥中心全量生成策略
            device_id_list = data.get('sync_device', [])
            device_id_list = [str(i) for i in device_id_list]
            director_result = generate_fulldose_policy(policy_type + 1, json.dumps(device_id_list), director_down_header=request_header)
            if director_result[0] == 0:
                set_policy_job_finished(request_header['HTTP_JOB_ID'], 2, director_result[1])
                send_echo_2_no_task(request_header, {'code': 200, 'msg': director_result[1]})
            elif director_result[0] == 2:
                set_policy_job_finished(request_header['HTTP_JOB_ID'], 3, director_result[1])
                send_echo_2_no_task(request_header, {'code': 400, 'msg': director_result[1]})
            else:
                pass
        # increment
        else:
            save_policy_job(request_header, 0)  # 保存JOB

            # add
            if 'add' in data and data['add']:
                add_policy = data['add']
                for rule in add_policy:
                    convert_policy_common_field(rule, common.DIRECTOR_POLICY_TYPE.index(request_header['HTTP_BUSINESSDATA_TYPE']) + 1)

                    # 获取管理中心本地的时候有与指挥下发的相同的策略
                    rule['map_rule_id_list'] = common.check_center_director_rule_is_equal(rule, policy_type + 1,
                                                                                          rule_models[policy_type])

                    rule['operate'] = 'add'
                    rule['receive_time'] = report_time
                    if 'create_time' in rule:
                        rule['creat_time'] = rule.pop('create_time')

                    if 'command_node_id' in rule:
                        rule['src_node'] = rule.pop('command_node_id')
                    else:
                        rule['src_node'] = request_header['HTTP_SRC_NODE']

                    if 'virtual_group_id' in rule:
                        del rule['virtual_group_id']
                    if 'manage_id' in rule:
                        del rule['manage_id']

                    rule['device_id_list'] = rule['device_id_list_run']
                    del rule['device_id_list_run']

                    rule['rule_status'] = 1

                rule_id_list = [policy['rule_id'] for policy in add_policy]
                rule_infos = director_rule_models[policy_type].objects.filter(rule_id__in=rule_id_list)
                insert_policy = []
                if rule_infos.exists():
                    update_id_list = rule_infos.values_list('rule_id', flat=True)
                    print 'update_id_list:', update_id_list
                    for rule in add_policy:
                        if rule['rule_id'] in update_id_list:
                            rule['device_id_list_run'] = ''
                            rule['is_del'] = 1
                            rule_info = director_rule_models[policy_type].objects.filter(rule_id=rule['rule_id'])
                            rule_info.update(**rule)

                        else:
                            insert_policy.append(rule)
                else:
                    insert_policy = add_policy

                # print 'add_policy:', add_policy
                if insert_policy:
                    serializer_data = director_rule_serializers[policy_type](data=insert_policy, many=True)
                    if serializer_data.is_valid():
                        serializer_data.save()
                    elif common.is_serial_id_overflow_errer(serializer_data.errors):
                        for new_rule in insert_policy:
                            director_rule_models[policy_type].objects.create(**new_rule)
                    else:
                        return common.ui_message_response(400, json.dumps(serializer_data.errors), '数据缺失或字段不符合规定，序列化出错')

            # del
            if 'del' in data and data['del']:
                del_policy = data['del']
                # print 'del_policy:', del_policy
                for rule_id in del_policy:
                    rule = director_rule_models[policy_type].objects.filter(rule_id=rule_id)
                    if rule.exists():
                        if rule[0].device_id_list_run is not None and rule[0].device_id_list_run != '':
                            rule.update(version='', operate='del', rule_status=1, device_id_list='', receive_time=report_time,
                                        is_del=0)
                        else:
                            rule.delete()

            # update
            if 'update' in data and data['update']:
                for rule_dict in data['update']:
                    rule = director_rule_models[policy_type].objects.filter(rule_id=rule_dict.get('rule_id'))
                    if rule.exists():
                        if rule[0].operate == 'add':
                            rule.update(version='', device_id_list=rule_dict.get('device_id_list_run'), rule_status=1, receive_time=report_time)
                        else:
                            rule.update(version='', device_id_list=rule_dict.get('device_id_list_run'), rule_status=1,
                                        receive_time=report_time, operate='change#' + rule[0].operate)

            # update task
            if 'update_task_id' in data and data['update_task_id']:
                for rule_task_dict in data['update_task_id']:
                    rule = director_rule_models[policy_type].objects.filter(rule_id=rule_task_dict.get('rule_id'))
                    if rule.exists():
                        if rule[0].operate == 'add':
                            rule.update(version='', task_id=rule_task_dict.get('task_id'), rule_status=1,
                                        receive_time=report_time)
                        else:
                            rule.update(version='', task_id=rule_task_dict.get('task_id'), rule_status=1,
                                        receive_time=report_time, operate='group#' + rule[0].operate)

            # 生成增量任务
            result = generate_increment_policy(policy_type+1, director_down_header=request_header)
            if result[0] == 0:
                set_policy_job_finished(request_header['HTTP_JOB_ID'], 2, result[1])
                send_echo_2_no_task(request_header, {'code': 200, 'msg': result[1]})
            elif result[0] == 2:
                set_policy_job_finished(request_header['HTTP_JOB_ID'], 3, result[1])
                send_echo_2_no_task(request_header, {'code': 400, 'msg': result[1]})

        
        return common.ui_message_response(200, '数据接收成功', '请求成功', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


def convert_policy_common_field(rule, policy_type):
    if 'label' in rule:
        rule['remark'] = rule.pop('label')
    if policy_type == 2:  # 漏洞利用规则，修改数字对应的攻击类型
        rule['attack_type'] = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw'].index(rule.pop('attack_type')) + 1
    elif policy_type in [6, 8]:  # 加密规则或图片规则，修改config的组织方式
        rule['filesize_minsize'] = rule['filesize']['minsize']
        rule['filesize_maxsize'] = rule['filesize']['maxsize']
        del rule['filesize']
    elif policy_type == 7:  # 压缩规则，修改config的组织方式
        rule['dropsize'] = rule['filesize']['dropsize']
        rule['backsize'] = rule['filesize']['backsize']
        del rule['filesize']


# 对于没有任务可以生成的指挥下行策略或插件同步直接返回echo消息
def send_echo_2_no_task(director_down_header={}, data={'code': 200, 'msg': '任务已下发至检测器'}):
    """
    对于没有任务可以生成的指挥下行策略或插件同步直接返回echo消息
    :param director_down_header:      包含下行数据 发送和接收指挥节点以及业务类型和JOB_ID的请求头
    :param data                             echo消息的响应码和相应数据
    :return:
    """
    # echo消息
    echo_header = {
        'Dst-Node': director_down_header['HTTP_SRC_NODE'],
        'Src-Node': director_down_header['HTTP_DST_NODE'],
        'Src-Center': dc.SRC_CENTER_ID,
        'Msg-Type': 'echo',
        'Content-Type': 'application/json',
        'version': '1.0',
        # 'Cookie': 'unknown',
        'Data-Type': 'msg',
        'Task-Type': '0',
        'User-Agent': dc.CENTER_USER_AGENT,
        'Capture-Date': time.strftime('%a, %d %b %Y %H:%M:%S'),
        'Source_Type': 'ECHO_' + director_down_header.get('HTTP_SOURCE_TYPE'),
        'BusinessData-Type': 'ECHO_' + director_down_header.get('HTTP_BUSINESSDATA_TYPE'),
        'X-Forwarded-For': dc.detect_center_host,
        'Channel-Tpye': 'JCQ'
    }

    echo_data = {
        "job_id": director_down_header['HTTP_JOB_ID'],
        "resp_final": data['code'],
        "r_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "resp_msg": data['msg']
    }

    print u"#####指挥中心同步异常或没有任务生成, 发送ECHO_" + director_down_header.get('HTTP_BUSINESSDATA_TYPE') + u"消息"
    sender.send_director(dc.DIRECTOR_URL, dc.SRC_CENTER_ID, 'ECHO_' + director_down_header.get('HTTP_BUSINESSDATA_TYPE'), echo_header, json.dumps(echo_data))


# 增量方式生成策略任务
def generate_increment_policy(policy_type, director_down_header={}):
    """
    全量方式生成策略任务
    :param policy_type:        标识策略类型，从1开始
    :param director_down_header  指挥中心下行的策略的携带的请求头
    :return:                   set 0: 没有任务需要生成 1: 有任务需要生成  2: 出现异常
    """
    try:
        pu.print_format_header("增量生成指挥中心策略任务", number=25)

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
        rule_data = director_rule_models[policy_type-1].objects.filter(rule_status=1)
        # rule_data = model.objects.filter(~Q(device_id_list_run=F('device_id_list')) | Q(operate__contains='group'), rule_status=1)   #这里认为 对于之前的生效范围和设置生效范围的一样的话就不进行增量操作
        if not rule_data.exists():
            # return common.ui_message_response(200, '没有未下发的规则', '没有未下发的规则', status.HTTP_200_OK)
            print '指挥中心没有未下发的规则'
            # if is_director:
            #     send_echo_2_no_task(director_down_header)
            return 0, '没有未下发的规则'

        rule_json = serialize('json', rule_data, fields=result_set)  # 序列化成json
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

        for rule in rule_data:  # 遍历所有规则

            if rule.device_id_list == rule.device_id_list_run == '':    # 新增同时没有设置生效范围
                continue

            # previous_device_list 表示该规则已经生成任务的检测器主键id列表
            previous_device_list = common.generate_device_ids_list_from_model_str(rule.device_id_list_run, id_device_dict.values())

            # now_device_list表示该规则变更之后的检测器主键id列表
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
                # rule_info = model.objects.filter(
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
                        'is_valid': 1
                    }
                    task_data['down_job_id'] = director_down_header['HTTP_JOB_ID']
                    task_data['down_node_id'] = director_down_header['HTTP_SRC_NODE']
                    task_list.append(task_data)
                except:
                    print '生成检测器{0}任务失败'.format(k)

        # 更新相应rule表的版本号、状态、操作时间，检测器运行列表更新为检测器变更列表
        # rule_data.update(version=version_num, rule_status=0, operate='', device_id_list_run=F('device_id_list'))
        rule_data.update(version='', rule_status=0, operate='', device_id_list_run=F('device_id_list'))

        if not task_list:
            print '指挥中心下发的策略没有任务需要生成'
            # return common.ui_message_response(200, '没有任务需要生成', '没有任务需要生成', status.HTTP_200_OK)
            # if is_director:
            #     send_echo_2_no_task(director_down_header)
            return 0, '下发的策略没有任务需要生成'

        else:
            serializer_task = DirectorTaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
            else:
                # return common.ui_message_response(400, json.dumps(serializer_task.errors),
                #                                   'task数据缺失或字段不符合规定，序列化出错')
                print '指挥中心下发的策略生成任务时数据缺失或字段不符合规定', serializer_task.errors

        common.generate_system_log({'uuid': '指挥中心'}, u'策略操作', u'指挥中心策略增量下发',
                                   u'指挥中心策略增量下发' + json.dumps(task_list,
                                                                                                     cls=qu.CJsonEncoder,
                                                                                                     encoding='utf-8',
                                                                                                     ensure_ascii=False))
        # return common.ui_message_response(200, 'task生成成功', '任务生成成功', status.HTTP_200_OK)
        print '指挥中心下发的策略生成任务成功'

        pu.print_format_tail("增量生成指挥中心策略任务", number=25)

        if config.const.UPLOAD_BUSINESS_DISPOSAL:
            write_policy_data.process_policy(common.module_names[policy_type-1])

        return 1, '下发的策略生成任务成功'
    except Exception:
        traceback.print_exc()
        common.generate_system_log({'uuid': '指挥中心'}, u'策略操作', u'指挥中心策略增量下发',
                                   u'指挥中心策略增量下发' + u'模块异常')
        # return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
        #                                   status.HTTP_500_INTERNAL_SERVER_ERROR)
        print '指挥中心策略增量下发' + '模块异常'
        return 2, '管理中心策略增量下发模块异常'


# 全量生成策略
def generate_fulldose_policy(policy_type, device_id_list, director_down_header={}):
    """
    全量方式生成策略任务
    :param policy_type:        标识策略类型，从1开始
    :param device_id_list:     要全量策略的检测器列表, 管理中心本地策略为检测器主键ID列表，指挥中心策略为检测器ID列表
    :param director_down_header  指挥中心下行的策略的携带的请求头
    :return:                   set 0: 没有任务需要生成 1: 有任务需要生成  2: 出现异常
    """
    try:
        pu.print_format_header("指挥中心全量生成策略任务", number=25)

        result_set = get_rule_fields(policy_type)  # 获取查询的规则集合

        task_list = []  # 任务

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}  # id与device_id的对应关系
        device_id_dict = {item[1]: item[0] for item in device_id_all}
        if device_id_list == '[]':  # 表示空检测器
            print '指挥中心没有选择要下发的检测器'
            # if is_director:
            #     send_echo_2_no_task(director_down_header)
            return 0, '没有选择要下发的检测器'
        else:
            device_id_list = json.loads(device_id_list)

        for device_id in device_id_list:
            if not Detector.objects.filter(device_id=device_id).exists():
                return 2, '检测器%s不存在' % device_id

        generate_time = du.get_current_time()
        # rule_data = model.objects.filter(Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'))
        # director_rule_data = director_rule_models[policy_type-1].objects.filter(is_del=1)
        # rule_data = rule_models[policy_type-1].objects.filter(is_del=1)

        is_device_has_policy = False    # 标识对所有的检测器，是否有策略可以下发
        # 筛选类规则（未知攻击、加密、压缩、图片、通联关系、应用行为）只选择一条
        if policy_type in [4, 6, 7, 8, 13, 14]:
            for d_id in device_id_list:
                director_rule_data = director_rule_models[policy_type-1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
                rule_data = rule_models[policy_type-1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
                if not rule_data.exists() and not director_rule_data.exists():
                    print '对于检测器' + d_id + ',指挥中心和管理中心没有可全量下发的策略'
                    # if is_director:
                    #     send_echo_2_no_task(director_down_header)
                    continue
                else:
                    is_device_has_policy = is_device_has_policy | True

                director_rule_json = serialize('json', director_rule_data, fields=result_set)
                director_config_list = [json.loads(director_rule_json)[-1]['fields']]

                rule_json = serialize('json', rule_data, fields=result_set)  # 序列化成json
                config_list = [json.loads(rule_json)[-1]['fields']]
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
                    'is_valid': 1
                }
                task_data['down_job_id'] = director_down_header['HTTP_JOB_ID']
                task_data['down_node_id'] = director_down_header['HTTP_SRC_NODE']
                task_list.append(task_data)

        else:  # 告警类规则（可以多条规则）
            for d_id in device_id_list:
                director_rule_data = director_rule_models[policy_type-1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'))
                rule_data = rule_models[policy_type-1].objects.filter(
                    Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'))
                if not rule_data.exists() and not director_rule_data.exists():
                    print '对于检测器' + d_id + ',指挥中心和管理中心没有可全量下发的策略'
                    # if is_director:
                    #     send_echo_2_no_task(director_down_header)
                    continue
                else:
                    is_device_has_policy = is_device_has_policy | True

                director_rule_json = serialize('json', director_rule_data, fields=result_set)
                director_rule_all = json.loads(director_rule_json)
                director_config_list = [data['fields'] for data in director_rule_all]

                rule_json = serialize('json', rule_data, fields=result_set)  # 序列化成json
                rule_all = json.loads(rule_json)
                config_list = [data['fields'] for data in rule_all]  # config
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
                }
                task_data['down_job_id'] = director_down_header['HTTP_JOB_ID']
                task_data['down_node_id'] = director_down_header['HTTP_SRC_NODE']
                task_list.append(task_data)

        if not is_device_has_policy:
            return 0, '没有可全量下发的策略'

        if not task_list:
            print '指挥中心和管理中心下发的策略没有任务需要生成'
            # return common.ui_message_response(200, '没有任务需要生成', '没有任务需要生成', status.HTTP_200_OK)
            # if is_director:
            #     send_echo_2_no_task(director_down_header)
            return 0, '下发的策略没有任务需要生成'

        else:
            serializer_task = DirectorTaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
                common.generate_system_log({'uuid': '指挥中心'}, u'策略操作', u'指挥中心全量刷新检测器策略',
                                           u'指挥中心全量刷新检测器策略' + json.dumps(task_list, cls=qu.CJsonEncoder,
                                                                         encoding='utf-8', ensure_ascii=False))
            else:
                common.generate_system_log({'uuid': '指挥中心'}, u'策略操作', u'指挥中心全量刷新检测器策略', u'指挥中心全量刷新检测器策略，task数据缺失或字段不符合规定，序列化出错')
                print '指挥中心和管理中心下发的策略生成任务时数据缺失或字段不符合规定', serializer_task.errors

        # return common.ui_message_response(200, 'task生成成功', '任务生成成功', status.HTTP_200_OK)
        print '指挥中心和管理中心下发的策略生成任务成功'

        pu.print_format_tail("指挥中心全量生成策略任务", number=25)

        return 1, '下发的策略生成任务成功'
    except Exception:
        traceback.print_exc()
        common.generate_system_log({'uuid': '指挥中心'}, u'策略操作', u'指挥中心全量刷新检测器策略', u'指挥中心全量刷新检测器策略' + u'模块异常')
        # return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
        #                                   status.HTTP_500_INTERNAL_SERVER_ERROR)
        print '指挥中心全量刷新检测器策略' + '模块异常'
        return 2, '指挥中心全量刷新检测器策略模块异常'


# 接收指挥中心插件
def receive_plug(request):
    try:
        result = check_down_director_ip_valid(request)  # 校验是否接收指挥中心数据及指挥中心IP是否合法
        if isinstance(result, Response):
            return result

        report_time = du.get_current_date_string()  # 获取当前时间
        request_header = request.META            # 获取请求头

        generate_task = False

        try:
            request_data = json.loads(request.body)  # 获取请求数据
        except:
            return common.ui_message_response(400, '请求数据不是json格式', '请求数据不符合规定')
        print 'data:', pu.pretty_print_format(request_data)

        if not isinstance(request_data, dict):  # 判断请求数据类型是否合规
            return common.detector_message_response(400, '请求数据不是json格式', '请求数据不符合规定')
        else:
            data = request_data.copy()  # request_data是 immutable QueryDict 对象，需要转变


        #
        # reset center
        if 'sync_center' in data:
            save_plugin_job(request_header, 2)

            sync_plug = data['sync_center']
            is_down_plug_file_list = []

            sync_plug_id_list = [int(plugin['plug_id']) for plugin in sync_plug]
            center_director_plug_id_list = [plugin.plug_id for plugin in DirectorPlugin.objects.filter(is_del=1, plug_status=0)]
            del_id_list = list(set(center_director_plug_id_list) - set(sync_plug_id_list))
            del_plug = DirectorPlugin.objects.filter(plug_id__in=del_id_list)
            if del_plug.exists():
                del_plug.update(is_del=0)
                print "设置以下插件：", pu.pretty_print_format(del_id_list), "状态为已删除"

            add_sync = []
            for plug in sync_plug:
                plug['receive_time'] = report_time
                plug['plug_id'] = int(plug['plug_id'])

                if 'command_node_id' in plug:
                    plug['src_node'] = plug.pop('command_node_id')
                else:
                    plug['src_node'] = request_header['HTTP_SRC_NODE']

                if 'virtual_group_id' in plug:
                    del plug['virtual_group_id']
                if 'manage_id' in plug:
                    del plug['manage_id']

                plug['plug_type'] = 'detect'

                convert_director_2_center_field(plug)

                plug['down_job_id'] = request_header['HTTP_JOB_ID']
                plug['is_plug_data_release'] = 1  # 设置新增插件数据已收到

                plug['plug_url'] = construct_plug_file_download_url(plug['plug_path'], plug['plug_name'],
                                                                    plug['src_node'])
                plug['plug_config_url'] = construct_plug_file_download_url(plug['plug_config_path'],
                                                                           plug['plug_config_name'], plug['src_node'])

                # 防止下发的path覆盖了本地的path
                del plug['plug_path']
                del plug['plug_config_path']

                # plug['cmd'] = 'add' if plug['is_del'] == 1 else 'del'
                query_data = DirectorPlugin.objects.filter(plug_id=plug['plug_id'], is_del=1)
                if query_data.exists():
                    # print '##############'
                    download_set = judge_is_download_plug_file(plug, query_data)
                    is_down_plug_file_list.append(download_set)

                    plug['is_del'] = 1
                    # 下发插件和本地插件不相同
                    if not (download_set == (0, 0) and DirectorPlugin.objects.filter(plug_id=plug['plug_id'], plug_version=plug['plug_version'], plug_config_version=plug['plug_config_version'], cpu=plug['cpu'], mem=plug['mem'], disk=plug['disk']).exists()):
                        plug['plug_status'] = 1
                        if query_data[0].cmd == 'add':
                            plug['cmd'] = 'add'
                        else:
                            plug['cmd'] = 'update_plug#' + query_data[0].cmd

                    if query_data[0].device_id_list != plug['device_id_list_run']:
                        plug['device_id_list'] = plug.pop('device_id_list_run')
                        plug['plug_status'] = 1
                        if query_data[0].cmd == 'add':
                            plug['cmd'] = 'add'
                        else:
                            plug['cmd'] = 'change#' + query_data[0].cmd
                    query_data.update(**plug)
                else:
                    # print '@@@@@@@@@@@@@@'
                    if 'is_del' in plug and plug['is_del'] == 0:
                        # print '1111111111111111111'
                        is_down_plug_file_list.append((0, 0))

                        plug['cmd'] = 'del'
                    else:
                        # print '2222222222222222222'
                        is_down_plug_file_list.append((1, 1))

                        plug['cmd'] = 'add'
                        plug['device_id_list'] = plug.pop('device_id_list_run')
                        plug['device_id_list_run'] = ''
                    plug['plug_status'] = 1
                    add_sync.append(plug)
            print 'add_sync:', pu.pretty_print_format(add_sync)
            serializer_data = DirectorPluginSerializer(data=add_sync, many=True)
            if serializer_data.is_valid():
                serializer_data.save()
            elif common.is_serial_id_overflow_errer(serializer_data.errors):
                for plug in add_sync:
                    DirectorPlugin.objects.create(**plug)
            else:
                return common.ui_message_response(400, json.dumps(serializer_data.errors), '数据缺失或字段不符合规定，序列化出错')

            download_plug_file_from_director('plugin/', sync_plug, request_header, is_down_plug_file_list)

        # reset detector
        elif 'sync_device' in data:
            save_plugin_job(request_header, 1)

            # 生成指挥中心插件任务
            device_id_list = request_data.get('sync_device', [])
            device_id_list = [str(i) for i in device_id_list]
            director_result = generate_fulldose_plug_task(json.dumps(device_id_list), director_down_header=request_header)
            if director_result[0] == 0:
                set_plugin_job_finished(request_header['HTTP_JOB_ID'], 2, director_result[1])
                send_echo_2_no_task(request_header, {'code': 200, 'msg': director_result[1]})
            elif director_result[0] == 2:
                set_plugin_job_finished(request_header['HTTP_JOB_ID'], 3, director_result[1])
                send_echo_2_no_task(request_header, {'code': 400, 'msg': director_result[1]})
            else:
                pass

        # 增量下发插件
        else:
            save_plugin_job(request_header, 0)

            # add
            insert_plug = []
            if 'add' in data and data['add']:
                add_plug = data['add']
                for plug in add_plug:
                    plug['plug_id'] = int(plug['plug_id'])
                    plug['plug_type'] = 'detect'
                    plug['receive_time'] = report_time

                    if 'command_node_id' in plug:
                        plug['src_node'] = plug.pop('command_node_id')
                    else:
                        plug['src_node'] = request_header['HTTP_SRC_NODE']

                    plug['down_job_id'] = request_header['HTTP_JOB_ID']

                    if 'virtual_group_id' in plug:
                        del plug['virtual_group_id']
                    if 'manage_id' in plug:
                        del plug['manage_id']

                    plug['cmd'] = 'add'
                    plug['plug_status'] = 1
                    plug['device_id_list'] = plug.pop('device_id_list_run')

                    convert_director_2_center_field(plug)

                    plug['is_plug_data_release'] = 1  # 设置新增插件数据已收到
                    plug['is_plug_file_release'] = 0  # 设置新增插件数据已收到
                    plug['is_config_file_release'] = 0  # 设置新增插件数据已收到

                    plug['plug_url'] = construct_plug_file_download_url(plug['plug_path'], plug['plug_name'],
                                                                        plug['src_node'])
                    plug['plug_config_url'] = construct_plug_file_download_url(plug['plug_config_path'],
                                                                               plug['plug_config_name'],
                                                                               plug['src_node'])

                plug_id_list = [plug['plug_id'] for plug in add_plug]
                plug_info = DirectorPlugin.objects.filter(plug_id__in=plug_id_list)
                if plug_info.exists():
                    update_plug_id = [plug_id for plug_id in plug_info.values_list('plug_id', flat=True)]
                    for plug in add_plug:
                        if plug['plug_id'] in update_plug_id:  # 指挥中心下发新增的插件在管理中心已存在，
                            plug['device_id_list_run'] = ''
                            plug['is_del'] = 1
                            DirectorPlugin.objects.filter(plug_id=plug['plug_id']).update(**plug)
                        else:
                            insert_plug.append(plug)
                else:
                    insert_plug = add_plug

                # print add_plug
                if insert_plug:
                    serializer_data = DirectorPluginSerializer(data=insert_plug, many=True)
                    if serializer_data.is_valid():
                        serializer_data.save()
                    else:
                        return common.ui_message_response(400, json.dumps(serializer_data.errors),
                                                          '数据缺失或字段不符合规定，序列化出错')

                is_down_plug_file_list = []
                for plug in add_plug:
                    is_down_plug_file_list.append((1, 1))
                download_plug_file_from_director('plugin/', add_plug, request_header, is_down_plug_file_list)
                # sender.async_download_plug_file_from_director('plugin', add_plug, request_header, is_down_plug_file_list)

            # del
            del_plug = []
            if 'del' in data and data['del']:
                del_plug = data['del']
                # print del_plug
                for del_id in del_plug:
                    plug = DirectorPlugin.objects.filter(plug_id=del_id)
                    if plug.exists():
                        if plug[0].device_id_list_run is None or plug[0].device_id_list_run == '':
                            plug.delete()
                        else:
                            plug.update(version='', cmd='del', plug_status=1, device_id_list='', down_job_id=request_header['HTTP_JOB_ID'],
                                        receive_time=report_time, is_del=0)
                            generate_task = True

            # update
            if 'update' in data and data['update']:
                update_plug = data['update']
                is_down_plug_file_list = []
                final_update_plug = []
                for plug in update_plug:
                    plug['plug_id'] = int(plug['plug_id'])

                    convert_director_2_center_field(plug)
                    plug['down_job_id'] = request_header['HTTP_JOB_ID']

                    plug['receive_time'] = report_time
                    plug['is_plug_data_release'] = 1
                    plug['src_node'] = request_header['HTTP_SRC_NODE']
                    plug['version'] = ''
                    plug['plug_status'] = 1
                    plug['plug_url'] = construct_plug_file_download_url(plug['plug_path'], plug['plug_name'], plug['src_node'])
                    plug['plug_config_url'] = construct_plug_file_download_url(plug['plug_config_path'], plug['plug_config_name'], plug['src_node'])

                    # 防止下发的path覆盖了本地的path
                    del plug['plug_path']
                    del plug['plug_config_path']

                    plug_info = DirectorPlugin.objects.filter(plug_id=plug['plug_id'])
                    if plug_info.exists():

                        final_update_plug.append(plug)
                        is_down_plug_file_list.append(judge_is_download_plug_file(plug, plug_info))

                        if plug_info[0].cmd == 'add':
                            plug['cmd'] = 'add'
                        else:
                            plug['cmd'] = 'update_plug#' + plug_info[0].cmd
                        plug_info.update(**plug)
                # print update_plug
                download_plug_file_from_director('plugin/', final_update_plug, request_header, is_down_plug_file_list)
                # sender.async_download_plug_file_from_director('plugin', final_update_plug, request_header, is_down_plug_file_list)

            # update_config
            if 'update_config' in data and data['update_config']:
                update_plug_config = data['update_config']
                is_down_plug_file_list = []
                final_update_config_plug = []
                for plug in update_plug_config:

                    plug['plug_id'] = int(plug['plug_id'])
                    convert_director_2_center_field(plug)
                    plug['down_job_id'] = request_header['HTTP_JOB_ID']

                    plug['receive_time'] = report_time
                    plug['is_plug_data_release'] = 1
                    plug['is_plug_file_release'] = 1
                    plug['src_node'] = request_header['HTTP_SRC_NODE']
                    plug['version'] = ''
                    plug['plug_status'] = 1

                    plug['plug_config_url'] = construct_plug_file_download_url(plug['plug_config_path'], plug['plug_config_name'], plug['src_node'])

                    # 防止下发的path覆盖了本地的path
                    del plug['plug_config_path']

                    plug_info = DirectorPlugin.objects.filter(plug_id=plug['plug_id'])
                    if plug_info.exists():
                        final_update_config_plug.append(plug)
                        is_down_plug_file_list.append(judge_is_download_plug_file(plug, plug_info))

                        if plug_info[0].cmd == 'add':
                            plug['cmd'] = 'add'
                        else:
                            plug['cmd'] = 'update_config#' + plug_info[0].cmd
                        plug_info.update(**plug)
                # print update_plug_config
                download_plug_file_from_director('plugin/', final_update_config_plug, request_header, is_down_plug_file_list)
                # sender.async_download_plug_file_from_director('plugin', final_update_config_plug, request_header, is_down_plug_file_list)

            # update device
            if 'update_detector_list' in data and data['update_detector_list']:
                plug_id_device_list = data['update_detector_list']
                for plug_id_device in plug_id_device_list:
                    plug = DirectorPlugin.objects.filter(plug_id=plug_id_device['plug_id'])
                    if plug.exists():
                        generate_task = True
                        if plug[0].cmd == 'add':
                            plug.update(version='', plug_status=1, device_id_list=plug_id_device['device_id_list_run'], src_node=request_header['HTTP_SRC_NODE'], down_job_id=request_header['HTTP_JOB_ID'],
                                        receive_time=report_time)
                        else:
                            plug.update(version='', plug_status=1, device_id_list=plug_id_device['device_id_list_run'], src_node=request_header['HTTP_SRC_NODE'], down_job_id=request_header['HTTP_JOB_ID'],
                                        cmd='change#' + plug[0].cmd, receive_time=report_time)

            if generate_task:
                result = generate_increment_plug_task(request_header)
                if result[0] == 0:
                    set_plugin_job_finished(request_header['HTTP_JOB_ID'], 2, result[1])
                    send_echo_2_no_task(request_header, {'code': 200, 'msg': result[1]})
                elif result[0] == 2:
                    set_plugin_job_finished(request_header['HTTP_JOB_ID'], 3, result[1])
                    send_echo_2_no_task(request_header, {'code': 400, 'msg': result[1]})

        return common.ui_message_response(200, '数据接收成功', 'success', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 通过指挥下发的插件数据中的文件路径与本地插件路径判断文件是否需要下载
def judge_is_download_plug_file(plug, plug_info):
    download_list = [0, 0]
    if 'plug_url' in plug and plug['plug_url'] != plug_info[0].plug_url:
        download_list[0] = 1
    else:
        plug['is_plug_file_release'] = 1

    if 'plug_config_url' in plug and plug['plug_config_url'] != plug_info[0].plug_config_url:
        download_list[1] = 1
    else:
        plug['is_config_file_release'] = 1

    return tuple(download_list)


# 批量从指挥节点下载插件（配置）文件
def download_plug_file_from_director(sub_function_path, plug_list, director_down_header={}, is_down_plug_file_list=[]):
    """
    从指挥节点下载插件（配置）文件
    :param sub_function_path:       文件存储的功能子目录，如 'plugin'、'command'
    :param plug_list:               要获取文件的插件列表
    :param director_down_header:
    :param is_down_plug_file_list:  标识下载哪些插件文件列表 [(1, 1),...] -> (1, 1):标识插件和插件配置文件都下载
    :return:
    """
    index = 0
    for plug in plug_list:
        if is_down_plug_file_list[index][0]:    # 插件文件
            plug_path = sender.download_file_from_director(plug['plug_url'], sub_function_path, plug['plug_name'])
            if plug_path != '':
                DirectorPlugin.objects.filter(plug_id=plug['plug_id']).update(plug_path=plug_path,
                                                                              is_plug_file_release=1)
            else:
                DirectorPlugin.objects.filter(plug_id=plug['plug_id']).update(plug_path=plug_path)

        if is_down_plug_file_list[index][1]:    # 插件配置文件
            plug_config_path = sender.download_file_from_director(plug['plug_config_url'], sub_function_path, plug['plug_config_name'])
            if plug_config_path != '':
                DirectorPlugin.objects.filter(plug_id=plug['plug_id']).update(plug_config_path=plug_config_path, is_config_file_release=1)
            else:
                DirectorPlugin.objects.filter(plug_id=plug['plug_id']).update(plug_config_path=plug_config_path)
        index += 1

    result = generate_increment_plug_task(director_down_header)
    if result[0] == 0:
        set_plugin_job_finished(director_down_header['HTTP_JOB_ID'], 2, result[1])
        send_echo_2_no_task(director_down_header, {'code': 200, 'msg': result[1]})
    elif result[0] == 2:
        set_plugin_job_finished(director_down_header['HTTP_JOB_ID'], 3, result[1])
        send_echo_2_no_task(director_down_header, {'code': 400, 'msg': result[1]})


def construct_plug_file_download_url(path, name, node_id):
    return dc.send_director_A + 'download/' + path + '?rename=' + name + '&node_id=' + node_id


def convert_director_2_center_field(plug):
    if 'plug_config_cpu' in plug:
        plug['cpu'] = plug['plug_config_cpu']
        del plug['plug_config_cpu']
    if 'plug_config_mem' in plug:
        plug['mem'] = plug['plug_config_mem']
        del plug['plug_config_mem']
    if 'plug_config_disk' in plug:
        plug['disk'] = plug['plug_config_disk']
        del plug['plug_config_disk']


# 接收指挥中心插件附件
# def receive_plug_file(request):
#     try:
#         result = check_down_director_ip_valid(request)  # 校验是否接收指挥中心数据及指挥中心IP是否合法
#         # if isinstance(result, Response):
#         #     return result
#
#         request_header = request.META
#
#         request_file = request.FILES.values()[0]
#         filename = json.loads(request_header['HTTP_CONTENT_FILEDESC'])['filename'] + '.' + json.loads(request_header['HTTP_CONTENT_FILEDESC'])['filetype']
#         file_relative_path = 'director/plug/'
#         file_absolute_path = os.path.join(common.MEDIA_ROOT, file_relative_path)
#         save_file_name = common.rename_detector_upload_file(request_header['HTTP_SRC_NODE'], filename)
#         is_success = fu.handle_upload_file(file_absolute_path, request_file, save_file_name)  # 上传文件
#         if not is_success:  # 文件上传失败
#             return common.ui_message_response(400, '服务器上存在相同的文件', '文件命名重复')
#
#         file_relative = os.path.join(file_relative_path, save_file_name)
#         meta_data = json.loads(request_header['HTTP_META_DATA'])
#
#         plug_id = meta_data['plug_id']
#         from random import randint
#         time.sleep(randint(0, 10) / 10.0)
#         plug_info = DirectorPlugin.objects.filter(plug_id=plug_id)
#         if plug_info.exists():
#
#             if meta_data['plug_or_config'] == 'plug':
#                 plug_info.update(plug_path=file_relative, plug_name=filename, is_plug_file_release=1)
#             else:
#                 plug_info.update(plug_config_path=file_relative, plug_config_name=filename, is_config_file_release=1)
#
#             director_down_header = {
#                 'HTTP_BUSINESSDATA_TYPE': meta_data['from_type'],
#                 'HTTP_JOB_ID': plug_info[0].down_job_id,
#                 'HTTP_SRC_NODE': request_header['HTTP_SRC_NODE'],
#                 'HTTP_DST_NODE': request_header['HTTP_DST_NODE']
#             }
#
#             result = generate_increment_plug_task(director_down_header=director_down_header)
#             if result[0] == 0:
#                 set_plugin_job_finished(plug_info[0].down_job_id, 2)
#                 send_echo_2_no_task(director_down_header, {'code': 200, 'msg': result[1]})
#             elif result[0] == 2:
#                 set_plugin_job_finished(plug_info[0].down_job_id, 3)
#                 send_echo_2_no_task(director_down_header, {'code': 400, 'msg': result[1]})
#         else:        # 新增插件数据未到达
#             data = {}
#             if meta_data['plug_or_config'] == 'plug':
#                 data['plug_path'] = file_relative
#                 data['plug_name'] = filename
#                 data['is_plug_file_release'] = 1
#             else:
#                 data['plug_config_path'] = file_relative
#                 data['plug_config_name'] = filename
#                 data['is_config_file_release'] = 1
#             data['plug_id'] = plug_id
#             data['plug_status'] = 1
#             data['cmd'] = 'add'
#             serializer_data = DirectorPluginSerializer(data=data)
#             if serializer_data.is_valid():
#                 serializer_data.save()
#             else:
#                 return common.ui_message_response(400, json.dumps(serializer_data.errors), '数据缺失或字段不符合规定，序列化出错')
#
#     except Exception:
#         traceback.print_exc()
#         return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 生成某个模块的插件任务
def generate_increment_plug_task(director_down_header={}):
    """
    生成某个模块的插件任务
    :param director_down_header:    指挥下行数据的请求头
    :return:                   set 0: 没有任务需要生成 1: 有任务需要生成  2: 出现异常
    """
    try:
        pu.print_format_header("增量生成指挥中心插件任务", number=25)

        generate_time = du.get_current_date_string()

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}   # id与device_id的对应关系

        device_plugs_dict = {}  # key: 检测器ID, value: 要下发的插件操作List

        # 查询未生成任务的插件信息
        plug_data = DirectorPlugin.objects.filter(plug_status=1).order_by('-id')
        if not plug_data.exists():
            # return common.ui_message_response(200, '没有未下发的插件', '没有未下发的插件', status.HTTP_200_OK)
            print '指挥中心没有未下发的插件'
            # if is_director:
            #     send_echo_2_no_task(director_down_header)
            return 0, '没有未下发的插件'

        plug_json = serialize('json', plug_data, fields=plug_result_set + ('is_del', 'is_plug_data_release', 'is_plug_file_release', 'is_config_file_release'))  # 序列化成json
        plug_all = json.loads(plug_json)   # 所有插件的List信息

        invalid_plug_id_list = []

        index = 0
        for plug in plug_data:
            # first_cmd = plug.cmd.split("#")[0]
            # previous_device_list 表示该规则已经生成任务的检测器主键id列表
            previous_device_list = common.generate_device_ids_list_from_model_str(plug.device_id_list_run, id_device_dict.values())

            # now_device_list表示该规则变更之后的检测器主键id列表
            now_device_list = common.generate_device_ids_list_from_model_str(plug.device_id_list, id_device_dict.values())

            print 'previous_device_list:', previous_device_list
            print 'now_device_list:', now_device_list

            plug_dict = plug_all[index]['fields']
            print 'plug:', pu.pretty_print_format(plug_dict)

            index += 1
            if 'add' in plug.cmd:

                if not (plug.is_plug_data_release and plug.is_plug_file_release and plug.is_config_file_release):   # 判断指挥下行的新增插件的数据和相关文件是否入库
                    invalid_plug_id_list.append(plug.plug_id)
                    continue

                for detector_id in now_device_list:
                    plug_set = get_plug_fields('add')
                    add_command = {'type': 'plug', 'cmd': 'add'}
                    for field in plug_set:
                        add_command[field] = plug_dict.get(field)
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
                    # add_plugin_operate(detector_id, {'type': 'plug', 'cmd': 'start', 'plug_id': plug.plug_id}, device_plugs_dict)   # 添加一条开启插件命令
            if 'del' in plug.cmd:
                for detector_id in previous_device_list:
                    add_command = {'type': 'plug', 'cmd': 'del', 'plug_id': plug.plug_id}
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
            if 'update_plug' in plug.cmd:

                if not (plug.is_plug_data_release and plug.is_plug_file_release and plug.is_config_file_release):   # 判断指挥下行的更新插件的数据和相关文件是否入库
                    invalid_plug_id_list.append(plug.plug_id)
                    continue

                for detector_id in previous_device_list:
                    plug_set = get_plug_fields('update_plug')
                    add_command = {'type': 'plug', 'cmd': 'update'}
                    for field in plug_set:
                        add_command[field] = plug_dict.get(field)
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
            if 'update_config' in plug.cmd:

                if not (plug.is_plug_data_release and plug.is_config_file_release):   # 判断指挥下行的更新插件配置的数据和相关文件是否入库
                    invalid_plug_id_list.append(plug.plug_id)
                    continue

                for detector_id in previous_device_list:
                    plug_set = get_plug_fields('update_config')
                    add_command = {'type': 'plug', 'cmd': 'config_update'}
                    for field in plug_set:
                        add_command[field] = plug_dict.get(field)
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)

            if 'change' in plug.cmd:

                add_device_ids = set(now_device_list) - (set(previous_device_list) & set(now_device_list))
                for detector_id in add_device_ids:   # 插件对应的部分检测器增加
                    plug_set = get_plug_fields('add')
                    add_command = {'type': 'plug', 'cmd': 'add'}
                    for field in plug_set:
                        add_command[field] = plug_dict.get(field)
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
                    # add_plugin_operate(detector_id, {'type': 'plug', 'cmd': 'start', 'plug_id': plug.plug_id}, device_plugs_dict)  # 添加一条开启插件命令
                del_device_ids = set(previous_device_list) - (set(previous_device_list) & set(now_device_list))
                for detector_id in del_device_ids:   # 插件对应的部分检测器删除
                    add_command = {'type': 'plug', 'cmd': 'del', 'plug_id': plug.plug_id}
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)

        task_list = []
        for k, v in device_plugs_dict.items():
            version_num = common.cal_task_version([PlugTask, DirectorPluginTask], k, 'plugin', '2')
            print "task_list", k, v
            try:
                task_data = {
                    'version': version_num,
                    'cmd': 'add',
                    'num': len(v),
                    'config': json.dumps(v, encoding='utf-8', ensure_ascii=False),
                    'generate_time': generate_time,
                    'device_id': k,
                    'is_valid': 1
                }
                task_data['down_job_id'] = director_down_header['HTTP_JOB_ID']
                task_data['down_node_id'] = director_down_header['HTTP_SRC_NODE']

                task_list.append(task_data)
            except Exception:
                traceback.print_exc()
                print '生成检测器{0}任务失败'.format(k)


        if not task_list and len(invalid_plug_id_list) == 0:
            print '指挥中心下发的插件没有任务需要生成'
            return 0, '下发的插件没有任务需要生成'
        elif not task_list and len(invalid_plug_id_list) > 0:
            print '指挥中心下发的插件数据或附件不全，不能下发'
            return 1, '下发的插件数据或附件不全，不能下发'
        else:
            print '############', pu.pretty_print_format(task_list)
            serializer_task = DirectorPluginTaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
            else:
                print '指挥中心下发的插件生成任务时数据缺失或字段不符合规定', serializer_task.errors

        # 更新相应plug表的版本号、状态、操作时间，检测器运行列表更新为检测器变更列表
        all_plug_id_list = [plug.plug_id for plug in plug_data]
        plug_data.filter(plug_id__in=(set(all_plug_id_list) - set(invalid_plug_id_list))).update(version='', plug_status=0, cmd='', device_id_list_run=F('device_id_list'),
                                                                                                 is_plug_data_release=0, is_plug_file_release=0, is_config_file_release=0)

        common.generate_system_log({'uuid': '指挥中心'}, u'插件操作', u'指挥中心插件增量下发',
                                   u'指挥中心插件增量下发' + json.dumps(task_list, cls=qu.CJsonEncoder, encoding='utf-8', ensure_ascii=False))
        # return common.ui_message_response(200, '插件任务生成成功', '插件任务生成成功', status.HTTP_200_OK)
        print '指挥中心下发的插件生成任务成功'

        pu.print_format_tail("增量生成指挥中心插件任务", number=25)
        return 1, '下发的插件生成任务成功'
    except Exception:
        common.generate_system_log({'uuid': '指挥中心'}, u'插件操作', u'指挥中心插件增量下发', u'指挥中心插件增量下发' + u'模块异常')
        traceback.print_exc()
        # return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)
        print '指挥中心插件增量下发' + '模块异常'
        return 2, '管理中心插件增量下发模块异常'


# 全量生成插件任务
def generate_fulldose_plug_task(device_id_list, director_down_header={}):
    """
    全量生成插件任务
    :param device_id_list           全量下发的的检测器列表,本地插件传入主键ID List, 指挥插件传入检测器ID List
    :param director_down_header:    指挥下行数据的请求头
    :return:                   set 0: 没有任务需要生成 1: 有任务需要生成  2: 出现异常
    """
    try:

        pu.print_format_header("指挥中心全量生成插件任务", number=25)

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}  # id与device_id的对应关系

        if device_id_list == '[]':  # 表示空检测器
            print '指挥中心没有选择要下发的检测器'
            # if is_director:
            #     send_echo_2_no_task(director_down_header)
            return 0, '没有选择要下发的检测器'
        else:
            device_id_list = json.loads(device_id_list)

        generate_time = du.get_current_time()

        device_plugs_dict = {}

        is_device_has_plug = False    # 标识对所有的检测器，是否有插件可以下发
        for device_id in device_id_list:
            plug_data = PluginDetector.objects.filter(
                Q(device_id_list_run__contains='#' + str(device_id) + '#') | Q(device_id_list_run='#'), is_del=1)
            plug_data_director = DirectorPlugin.objects.filter(
                Q(device_id_list_run__contains='#' + str(device_id) + '#') | Q(device_id_list_run='#'), is_del=1)
            if not plug_data.exists() and not plug_data_director.exists():
                print '对于检测器' + device_id + ',指挥中心和管理中心没有可全量下发的插件'
                # if is_director:
                #     send_echo_2_no_task(director_down_header)
                continue
            else:
                is_device_has_plug = is_device_has_plug | True

            plug_json = serialize('json', plug_data, fields=plug_result_set)  # 序列化成json
            plug_all = json.loads(plug_json)
            plug_data_list = [plug['fields'] for plug in plug_all]

            plug_json_director = serialize('json', plug_data_director, fields=plug_result_set)  # 序列化成json
            plug_all_director = json.loads(plug_json_director)
            plug_data_director_list = [plug['fields'] for plug in plug_all_director]

            plug_data_list.extend(plug_data_director_list)
            print 'plug:', pu.pretty_print_format(plug_data_list)
            for plug_dict in plug_data_list:
                plug_set = get_plug_fields('add')
                add_command = {'type': 'plug', 'cmd': 'add'}
                for field in plug_set:
                    add_command[field] = plug_dict.get(field)
                add_plugin_operate(device_id, add_command, device_plugs_dict)


        task_list = []

        for k, v in device_plugs_dict.items():
            version_num = common.cal_task_version([PlugTask, DirectorPluginTask], k, 'plugin', '2')
            try:
                task_data = {
                    'version': version_num,
                    'cmd': 'reset',
                    'num': len(v),
                    'config': json.dumps(v, encoding='utf-8', ensure_ascii=False),
                    'generate_time': generate_time,
                    'device_id': k,
                    'is_valid': 1
                }

                task_data['down_job_id'] = director_down_header['HTTP_JOB_ID']
                task_data['down_node_id'] = director_down_header['HTTP_SRC_NODE']
                task_list.append(task_data)
            except:
                traceback.print_exc()
                print '生成检测器{0}任务失败'.format(k)

        if not is_device_has_plug:
            return 0, '没有可全量下发的插件'

        if not task_list:
            print '指挥中心和管理中心下发的插件没有任务需要生成'
            # if is_director:
            #     send_echo_2_no_task(director_down_header)
            return 0, '下发的插件没有任务需要生成'
        else:
            serializer_task = DirectorPluginTaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
                common.generate_system_log({'uuid': '指挥中心'}, u'插件操作', u'指挥中心全量刷新检测器插件', u'指挥中心全量刷新检测器插件' + json.dumps(task_list, cls=qu.CJsonEncoder, encoding='utf-8', ensure_ascii=False))
            else:
                common.generate_system_log({'uuid': '指挥中心'}, u'插件操作', u'指挥中心全量刷新检测器插件', u'指挥中心和管理中心下发的插件生成任务时数据缺失或字段不符合规定，序列化出错')
                print '指挥中心和管理中心下发的插件生成任务时数据缺失或字段不符合规定', serializer_task.errors

        print '指挥中心和管理中心下发的插件生成任务成功'

        pu.print_format_tail("指挥中心全量生成插件任务", number=25)
        return 1, '下发的插件生成任务成功'
    except Exception:
        common.generate_system_log({'uuid': '指挥中心'}, u'插件操作', u'指挥中心全量刷新检测器插件', u'指挥中心全量刷新检测器插件' + u'模块异常')
        traceback.print_exc()
        print '指挥中心插件增量下发' + '模块异常'
        return 2, '指挥中心全量下发插件模块异常'


# 接收指挥中心命令
def receive_cmd(request):
    try:
        remote_ip = check_down_director_ip_valid(request)  # 校验是否接收指挥中心数据及指挥中心IP是否合法
        if isinstance(remote_ip, Response):
            return remote_ip

        report_time = du.get_current_date_string()  # 获取当前时间
        request_header = request.META            # 获取请求头

        generate_task = True

        request_data = json.loads(request.body)  # 获取请求数据

        print 'data:', pu.pretty_print_format(request_data)

        # 获取请求参数
        cmd_type = request_data.get('cmd_type')  # 命令类型
        device_id_list = request_data.get('device_id_list')  # 选择的id列表
        cmd_module = request_data.get('module')  # 模块启停命令操作的模块
        sub_module = request_data.get('submodule')  # 模块启停命令操作的子模块
        save_path = request_data.get('save_path')  # 版本一致性检查，固件升级，内置策略更新指挥本地文件的相对路径
        filename = request_data.get('filename')  # 版本一致性检查，固件升级，内置策略更新指挥本地的文件名
        param = request_data.get('param')

        cmd_str_int_map = {
            'shutdown': 1,
            'reboot': 2,
            'startm': 3,
            'stopm': 4,
            'sync_time': 5,
            'update': 6,
            'version_check': 7,
            'inner_policy_update': 8,
            'passwd': 9
        }

        cmd_data = {}  # 构造命令数据
        cmd_type = cmd_str_int_map[cmd_type]

        save_command_job(request_header, 0, cmd_type)

        if not device_id_list:
            # return common.ui_message_response(400, '根据条件筛选检测器为空', '没有选择检测器')
            set_command_job_finished(request_header['HTTP_JOB_ID'], 2, '没有选择要下发的检测器')
            send_echo_2_no_task(request_header, {'code': 200, 'msg': '没有选择要下发的检测器'})
            generate_task = False

        modules_list = ['alarm', 'abnormal', 'sensitive', 'object_listen', 'net_audit', 'block']  # 模块表
        sub_modules_list = [
            'trojan', 'attack', 'malware', 'other', 'abnormal', 'finger_file', 'sensitive_file',
            'keyword_file', 'encryption_file', 'compress_file', 'picture_file', 'style_file',
            'ip_listen', 'domain_listen', 'url_listen', 'account_listen', 'net_log', 'app_behavior',
            'block'
        ]  # 模块启停子模块表

        if cmd_type == 1 or cmd_type == 2 or cmd_type == 5:  # 关机、重启、时间同步命令（没有参数）
            pass

        elif cmd_type == 3 or cmd_type == 4:  # 模块启停
            cmd_data['module'] = cmd_module
            cmd_data['submodule'] = json.dumps(sub_module)
            cmd_data['param'] = json.dumps({
                'module': cmd_data['module'],
                'submodule': sub_module
            })

        elif cmd_type == 6:  # 系统固件升级
            # 下载文件
            file_url = construct_plug_file_download_url(save_path, filename, request_header['HTTP_SRC_NODE'])
            new_save_path = sender.download_file_from_director(file_url, 'command/', filename)
            if new_save_path == '':
                set_command_job_finished(request_header['HTTP_JOB_ID'], 3, '固件文件下载失败')
                send_echo_2_no_task(request_header, {'code': 400, 'msg': '固件文件下载失败'})
                generate_task = False
            else:
                file_path = common.MEDIA_ROOT + new_save_path
                cmd_data['md5'] = su.calc_md5(file_path)  # md5

                with connection.cursor() as cursor:  # 运行mysql函数,生成版本号
                    cursor.execute('select nextversion(%s,%s)', ('firmware', '0'))  # 参数是一个元组
                    version_num = common.get_task_serial(cursor.fetchone()[0])
                cmd_data['soft_version'] = version_num
                cmd_data['filename'] = filename  # 文件名
                cmd_data['save_path'] = new_save_path  # 文件存储相对路径
                cmd_data['param'] = json.dumps({
                    'filename': filename,
                    'md5': cmd_data['md5'],
                    'soft_version': version_num
                })

        elif cmd_type == 7:  # 版本一致性检查
            cmd_data['param'] = json.dumps(param)
            version_check_method = param['method']
            if version_check_method == 'ls':  # 检查方法：读取目录文件列表方法

                cmd_data['version_check_result'] = request_data.get('version_check_result')
            else:
                file_url = construct_plug_file_download_url(save_path, filename, request_header['HTTP_SRC_NODE'])
                new_save_path = sender.download_file_from_director(file_url, 'command/', filename)
                if new_save_path == '':
                    set_command_job_finished(request_header['HTTP_JOB_ID'], 3, version_check_method + '文件下载失败')
                    send_echo_2_no_task(request_header, {'code': 400, 'msg': version_check_method + '文件下载失败'})
                    generate_task = False
                else:
                    offset = param['offset']
                    length = param['length']
                    file_path = common.MEDIA_ROOT + new_save_path

                    if version_check_method == 'get_file':  # 检查方法：读取文件内容方法，检测器返回指定文件内容（base64）
                        offset = 0 if offset is None else int(offset)
                        length = -1 if length is None or length == '0' else int(length)
                        cmd_data['version_check_result'] = json.dumps(
                            {'get_file': su.get_base64(fu.read_file(file_path, int(offset), int(length)))})
                        cmd_data['save_path'] = new_save_path
                        cmd_data['filename'] = filename
                    elif version_check_method == 'md5sum':  # 检查方法：判断文件MD5方法
                        offset = 0 if offset is None else int(offset)
                        length = -1 if length is None or length == '0' else int(length)
                        cmd_data['version_check_result'] = json.dumps(
                            {'md5sum': su.get_md5(fu.read_file(file_path, int(offset), int(length)))})
                        cmd_data['save_path'] = new_save_path
                        cmd_data['filename'] = filename

        elif cmd_type == 8:  # 内置策略更新
            # 下载文件
            file_url = construct_plug_file_download_url(save_path, filename, request_header['HTTP_SRC_NODE'])
            new_save_path = sender.download_file_from_director(file_url, 'command/', filename)
            if new_save_path == '':
                set_command_job_finished(request_header['HTTP_JOB_ID'], 3, '内置策略更新文件下载失败')
                send_echo_2_no_task(request_header, {'code': 400, 'msg': '内置策略更新文件下载失败'})
                generate_task = False
            else:
                file_path = common.MEDIA_ROOT + new_save_path
                cmd_data['md5'] = su.calc_md5(file_path)  # md5
                cmd_data['filename'] = filename  # 文件名
                cmd_data['save_path'] = new_save_path  # 文件存储相对路径
                cmd_data['param'] = json.dumps({
                    'filename': filename,
                    'md5': cmd_data['md5'],
                })

        elif cmd_type == 9:  # 本地WEB管理用户密码重置命令
            cmd_data['param'] = json.dumps(param)

        else:
            # return common.ui_message_response(400, '请求数据中的cmd不符合要求', '请求数据中的cmd不合法')
            set_command_job_finished(request_header['HTTP_JOB_ID'], 3, '请求数据中的cmd不符合要求，无任务需要生成')
            send_echo_2_no_task(request_header, {'code': 400, 'msg': '请求数据中的cmd不符合要求，无任务需要生成'})
            generate_task = False

        print 'cmd_data:', pu.pretty_print_format(cmd_data)

        if generate_task:
            print '指挥中心生成命令任务'
            cmd_data['cmd_type'] = cmd_type
            cmd_data['generate_time'] = report_time
            cmd_data['down_node_id'] = request_header.get('HTTP_SRC_NODE')
            cmd_data['down_job_id'] = request_header.get('HTTP_JOB_ID')
            command_list = []
            for device_id in device_id_list:
                version_num = common.cal_task_version([Command, DirectorCommand], device_id, 'command', '3')
                command = copy.deepcopy(cmd_data)
                command['version'] = version_num
                command['device_id'] = device_id
                command_list.append(command)

            print 'command_list:', pu.pretty_print_format(command_list)
            serializer_cmd = DirectorCommandSerializer(data=command_list, many=True)
            if serializer_cmd.is_valid():
                common.generate_system_log({'uuid': '指挥中心'}, u'命令操作', u'下发命令',
                                           u'指挥中心给检测器列表' + json.dumps(device_id_list) + u'生成' + common.COMMAND_TYPE[
                                               cmd_type - 1] + u'命令')
                serializer_cmd.save()  # 存储数据库command
            else:
                common.generate_system_log({'uuid': '指挥中心'}, u'命令操作', u'下发命令',
                                           u'指挥中心给检测器列表' + json.dumps(device_id_list) + u'生成' + common.COMMAND_TYPE[
                                               cmd_type - 1] + u'命令数据缺失或字段不符合规定，序列化出错')
                return common.ui_message_response(400, json.dumps(serializer_cmd.errors), '数据缺失或字段不符合规定，序列化出错')
                print '数据缺失或字段不符合规定，序列化出错', serializer_cmd.errors

        else:
            print '没有命令任务需要生成'

        return common.ui_message_response(200, '数据接收成功', '数据接收成功', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log({'uuid': '指挥中心'}, u'命令操作', u'下发命令',
                                   u'指挥中心生成' + common.COMMAND_TYPE[cmd_type - 1] + u'命令模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 检查接收的指挥中心数据的IP是否合法
def check_down_director_ip_valid(request):
    try:
        # 检查管理中心是否接收指挥中心数据

        # print "####", config.const.UPLOAD_DIRECTOR, check_global_director_connection()
        if not (config.const.UPLOAD_DIRECTOR and check_global_director_connection()):
            return common.ui_message_response(403, '管理中心不接收指挥中心数据', '管理中心不接收指挥中心数据', status.HTTP_403_FORBIDDEN)

        request_meta = request.META
        # print 'header :', request_meta
        if 'REMOTE_ADDR' in request_meta:
            remote_ip = request_meta['REMOTE_ADDR']
            center_info = ManagementCenterInfo.objects.all()
            if not center_info.exists():
                return common.ui_message_response(403, '该管理中心还未向任何指挥中心注册，不接受下行消息', '该管理中心还未向任何指挥中心注册，不接受下行消息', status.HTTP_403_FORBIDDEN)
            ip_whitelist = json.loads(center_info[0].ip_whitelist)
            # print 'ip_whitelist:', ip_whitelist
            if remote_ip in ip_whitelist:
                return remote_ip
            else:
                return common.ui_message_response(403, remote_ip + '->该指挥节点IP不是管理中心的上级指挥节点, 非法指挥节点', remote_ip + '->该指挥节点IP不是管理中心的上级指挥节点, 非法指挥节点', status.HTTP_403_FORBIDDEN)
        return common.ui_message_response(400, '请求头字段不包含REMOTE_ADDR', '请求头字段不包含REMOTE_ADDR')
    except:
        traceback.print_exc()


# 异步获取指挥中心的本管理中心的审核结果
def obtain_register_status(request):
    try:
        # remote_ip = check_down_director_ip_valid(request)
        # if isinstance(remote_ip, Response):
        #     return remote_ip
        # request_data = common.print_header_data(request)
        # print "director_audit_result:", request.body
        request_data = json.loads(request.body, encoding='utf-8')
        pu.pretty_print(request_data)

        if 'code' in request_data:
            code = request_data.get('code')
            if code == 1:    # 审核成功
                ManagementCenterInfo.objects.all().update(center_status=4, register_status=0, register_fail_reason=request_data.get('detail'), auth_status=2)
                # print '管理中心审核通过，发起认证'
                # print detect_center_reg_auth.send_auth_login_request()
                config.const.DIRECTOR_VERSION = True
                config.const.UPLOAD_DIRECTOR = True
            else:            # 审核失败
                print '管理中心审核不通过，请核对注册信息和备案信息是否一致'
                ManagementCenterInfo.objects.all().update(center_status=3, register_status=1, register_fail_reason=request_data.get('detail'), auth_status=2)
            return common.ui_message_response(200, '处理审核结果成功', '处理审核结果成功', status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '审核结果有误', '审核结果有误')
    except:
        traceback.print_exc()


# **************************************** 处理管理中心界面数据 ****************************************


def center_show(request):
    try:
        request_data = common.print_header_data(request)
        center_info = ManagementCenterInfo.objects.all()
        if center_info.exists():
            serialize_data = serialize('json', center_info, fields=('center_id', 'center_serial', 'center_ip', 'ip_whitelist', 'src_node', 'src_ip', 'center_status', 'register_time', 'auth_time'))
            center_data = []
            for data in json.loads(serialize_data):
                field = data['fields']
                field['id'] = data['pk']
                if 'register_time' in field and field['register_time'] is not None:
                    field['register_time'] = field['register_time'].replace('T', ' ')
                else:
                    field['register_time'] = ''
                if 'auth_time' in field and field['auth_time'] is not None:
                    field['auth_time'] = field['auth_time'].replace('T', ' ')
                else:
                    field['auth_time'] = ''
                if 'ip_whitelist' in field and field['ip_whitelist'] != '':
                    field['ip_whitelist'] = json.loads(field['ip_whitelist'])
                center_data.append(field)
            return common.ui_message_response(200, u'查询成功:' + json.dumps(center_data), center_data, status.HTTP_200_OK)
        else:
            return common.ui_message_response(200, u'查询成功: []', [], status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


def center_save_director_config(request):
    try:
        request_data = common.print_header_data(request)

        dc.SRC_CENTER_ID = request_data['center_id']
        dc.detect_center_host = request_data['center_ip']
        dc.CENTER_SERIAL = request_data['center_serial']
        dc.SRC_NODE = request_data['src_node']
        dc.director_host = request_data['src_ip']
        dc.ip_whitelist = [request_data['src_ip'], '172.17.0.1']

        register_data = get_center_data()

        register_data['center_id'] = dc.SRC_CENTER_ID
        register_data['center_ip'] = dc.detect_center_host
        register_data['center_serial'] = dc.CENTER_SERIAL
        register_data['src_node'] = dc.SRC_NODE
        register_data['src_ip'] = dc.director_host
        register_data['ip_whitelist'] = json.dumps(dc.ip_whitelist)
        # del copy_data['access_time']
        register_data['id'] = 1
        register_data['center_status'] = 6

        # pretty_print(register_data)
        management_center = ManagementCenterInfo.objects.filter(center_id=dc.SRC_CENTER_ID)
        if not management_center.exists():
            ManagementCenterInfo.objects.all().delete()
            ManagementCenterInfo.objects.create(**register_data)
        else:
            management_center.update(**register_data)

        return common.ui_message_response(200, '配置指挥节点数据成功', '配置指挥节点数据成功', status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取管理中心的静态注册数据，实际生产中使用pyutil工具获取
def get_center_data():
    interface = hu.interface_info()

    cpu = hu.CPUinfo()

    disk = hu.disk_info()

    contact = [
        {"phone": "18210331668", "email": "wwenan@gmail.com", "name": "wwenan", "position": "程序员"},
        {"phone": "18210331668", "email": "wangxingxing@sina.com", "name": "wangxingxing", "position": "程序员"}
    ]

    register_data = {

        'soft_version': dc.SOFT_VERSION,
        'device_ca': dc.DEVICE_CA,
        'organs': dc.ORGANS,
        'address': dc.ADDRESS,
        'address_code': dc.ADDRESS_CODE,
        'contact': json.dumps(contact, encoding='utf-8', ensure_ascii=False),
        # 'contact': contact,
        'mem_total': hu.mem_total(),
        'interface': json.dumps(interface),
        # 'interface': interface,
        'cpu_info': json.dumps(cpu),
        # 'cpu_info': cpu,
        'disk_info': json.dumps(disk)
        # 'disk_info': disk
        # 'access_time': du.get_current_date_string()
    }
    return register_data


# 管理中心注册
def center_register(request):
    try:
        request_data = common.print_header_data(request)
        pu.print_format_header('管理中心发起注册')

        management_center = ManagementCenterInfo.objects.filter(center_id=request_data['center_id'])
        data = serialize('json', management_center,
                         fields=('center_id', 'soft_version', 'device_ca', 'organs', 'address', 'address_code',
                                 'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info')
                         )  # 序列化
        list_data = json.loads(data)
        register_data = list_data[0]['fields']
        register_data['cpu_info'] = json.loads(register_data['cpu_info'])
        register_data['disk_info'] = json.loads(register_data['disk_info'])
        register_data['interface'] = json.loads(register_data['interface'])
        register_data['contact'] = json.loads(register_data['contact'])

        print "register_data:", pu.pretty_print_format(register_data)

        headers = {
            'Src-Node': management_center[0].src_node,
            'Src-Center': management_center[0].center_id,
            'Content-Type': 'application/json',
            'Channel-Tpye': 'JCQ',
            'User-Agent': management_center[0].center_id + '/' + management_center[0].soft_version + '(' + management_center[0].organs + ')',
            'X-Forwarded-For': management_center[0].center_ip
        }

        r = requests.post(dc.send_director_A + 'reg', data=json.dumps(register_data), headers=headers)
        # pu.print_with_retract(r.status_code, 1)  # 响应码
        # pu.print_with_retract(r.headers, 1)  # 响应头
        pu.print_with_retract(r.text.encode('utf-8'), 1)  # 响应消息正文

        result = json.loads(r.text.encode('utf-8'))
        center_info = ManagementCenterInfo.objects.filter(center_id=dc.SRC_CENTER_ID)
        if r.status_code == 200:  # （0：注册成功；1：注册失败；2：注册未审核）  #  (0: 认证成功  1：认证失败 2: 未认证)
            # if result["msg"] != u'该管理中心的已存在':
            center_info.update(register_time=du.get_current_time(), register_frequency=F('register_frequency') + 1, register_status=2, register_fail_reason='未审核',
                                                                                auth_frequency=0, auth_status=2, auth_fail_reason='未认证', center_status=2, cookie=None)
        elif result['msg'] == u'该管理中心的已存在':
            if center_info[0].register_status == 0 and center_info[0].auth_status == 0:            # 管理中心主动重置与指挥的连接状态
                center_info.update(register_time=du.get_current_time(), register_frequency=F('register_frequency') + 1, center_status=4)
                # detect_center_reg_auth.send_auth_login_request()

        config.const.DIRECTOR_VERSION = True
        config.const.UPLOAD_DIRECTOR = True

        pu.print_format_tail('管理中心发起注册')
        return common.ui_message_response(result['code'], '指挥中心：' + result['msg'], '指挥中心：' + result['msg'], code_2_status_map(result['code']))

    except:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


def code_2_status_map(code):
    if code == 200:
        return status.HTTP_200_OK
    elif code == 400:
        return status.HTTP_400_BAD_REQUEST
    else:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


# 管理中心认证
def center_auth(request):
    try:
        request_data = common.print_header_data(request)
        pu.print_format_header('管理中心发起认证')

        center_info = ManagementCenterInfo.objects.filter(center_id=request_data['center_id'])
        if center_info.exists():

            headers = {
                'Src-Node': center_info[0].src_node,
                'Src-Center': center_info[0].center_id,
                'Content-Type': 'application/json',
                'Channel-Tpye': 'JCQ',
                'User-Agent': center_info[0].center_id + '/' + center_info[0].soft_version + '(' + center_info[0].organs + ')',
                'X-Forwarded-For': center_info[0].center_ip
            }
            data = serialize('json', center_info,
                             fields=('center_id', 'soft_version', 'device_ca', 'organs', 'address', 'address_code',
                                     'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info')
                             )  # 序列化
            list_data = json.loads(data)
            auth_data = list_data[0]['fields']
            # auth_data['access_time'] = du.get_current_date_string()

            auth_data['cpu_info'] = json.loads(auth_data['cpu_info'])
            auth_data['disk_info'] = json.loads(auth_data['disk_info'])
            auth_data['interface'] = json.loads(auth_data['interface'])
            auth_data['contact'] = json.loads(auth_data['contact'])

            print 'auth_data:', pu.pretty_print_format(auth_data)

            r = requests.post(dc.send_director_A + 'login', data=json.dumps(auth_data), headers=headers)
            # pu.print_with_retract(r.status_code, 1)  # 响应码
            # pu.print_with_retract(r.headers, 1)  # 响应头
            pu.print_with_retract(r.text.encode('utf-8'), 1)  # 响应消息正文

            result = json.loads(r.text.encode('utf-8'))

            if result['code'] == 200 and result['msg'] != u'已经接入，无需再次接入':
                # print '认证成功'
                header_cookie = r.headers.get('Set-Cookie', None)
                if header_cookie is not None:
                    cookie_list = header_cookie.split(';')
                    if cookie_list is not None:
                        for cookie in cookie_list:
                            if str(cookie).find('session') != -1:
                                l = cookie.split(',')
                                if l is not None:
                                    for ll in l:
                                        if str(ll).find('session') != -1:
                                            dc.CENTER_COOKIE = {str(ll.split('=')[0].strip()): str(ll.split('=')[1])}
                if header_cookie is not None:
                    center_info.update(center_status=1, auth_time=du.get_current_time(), auth_frequency=F('auth_frequency') + 1,
                                       auth_status=0, auth_fail_reason='认证成功', cookie=json.dumps(dc.CENTER_COOKIE))
                else:
                    center_info.update(center_status=1, auth_time=du.get_current_time(),
                                       auth_frequency=F('auth_frequency') + 1,
                                       auth_status=0, auth_fail_reason='认证成功')
                dc.CENTER_COOKIE = json.loads(center_info[0].cookie, encoding='utf-8')
                from audit.data_processing import send_detector_info, send_audit
                from rest_framework.request import Request
                heartbeat.heartbeat_2_director()        # 发送心跳
                if center_info[0].auth_frequency == 1:
                    send_detector_info(Request, retract=1)  # 发送管理中心所有的检测器信息
                send_audit(Request, retract=1)  # 发送管理中心自身审计日志
            elif result['msg'] == u'已经接入，无需再次接入':
                center_info.update(auth_time=du.get_current_time(), auth_frequency=F('auth_frequency') + 1,
                                   auth_status=0, auth_fail_reason='认证成功', center_status=1)
            else:
                # print '认证失败'
                center_info.update(center_status=5, auth_time=du.get_current_time(), auth_frequency=F('auth_frequency') + 1,
                                   auth_status=1, auth_fail_reason=result['msg'], cookie=None)
        else:
            return common.ui_message_response(400, '管理中心%s不存在' % request_data['center_id'], '管理中心%s不存在' % request_data['center_id'])
        pu.print_format_tail('管理中心发起认证')
        return common.ui_message_response(result['code'], '指挥中心：' + result['msg'], '指挥中心：' + result['msg'], code_2_status_map(result['code']))
    except:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 重置管理中心
def center_reset(request):
    try:
        request_data = common.print_header_data(request)
        ManagementCenterInfo.objects.filter(center_id=request_data['center_id']).update(center_status=0, src_node='', src_ip='', ip_whitelist=json.dumps([]))
        config.const.DIRECTOR_VERSION = False   # 控制是否包含指挥版本，控制包括心跳、上下行数据等所有数据是否发送，该字段为False时，UPLOAD_DIRECTOR也为False
        config.const.UPLOAD_DIRECTOR = False    # 控制是否处理指挥中心的上下行数据（不包括心跳），若该字段为True，DIRECTOR_VERSION也必须为True
        return common.ui_message_response(200, '重置成功', '重置成功', status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 修改管理中心接收指挥的白名单
def center_update_ip_whitelist(request):
    try:
        request_data = common.print_header_data(request)
        ip_whitelist = request_data['ip']
        dc.ip_whitelist = json.loads(ip_whitelist)
        print '修改后的IP白名单：', pu.pretty_print_format(dc.ip_whitelist)
        ManagementCenterInfo.objects.filter(center_id=request_data['center_id']).update(ip_whitelist=ip_whitelist)
        return common.ui_message_response(200, '修改IP白名单成功', '修改IP白名单成功', status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 下载指挥中心下发的插件（配置）文件（在统一时失败的插件）
def download_plug(request):
    try:
        request_data = common.print_header_data(request)

        plug_id = request_data.get('id')
        file_type = request_data.get('file_type')

        plug_info = DirectorPlugin.objects.filter(id=plug_id)
        plug_json = serialize('json', plug_info, fields=('id', 'plug_id', 'plug_name', 'plug_config_name', 'plug_url', 'plug_config_url', 'src_node', 'down_job_id'))
        plug_list = [plug['fields'] for plug in json.loads(plug_json)]
        download_list = [(1, 0)] if file_type == '0' else [(0, 1)]
        down_director_header = {
            'HTTP_JOB_ID': plug_list[0]['down_job_id'],
            'HTTP_SRC_NODE': plug_list[0]['src_node']
        }

        download_plug_file_from_director('plugin', plug_list, down_director_header, download_list)

        new_plug_info = DirectorPlugin.objects.filter(id=plug_id)
        if new_plug_info[0].plug_status == 0:
            return common.ui_message_response(200, '插件下载成功', {'path': new_plug_info[0].plug_path if file_type == '0' else new_plug_info[0].plug_config_path, 'name': new_plug_info[0].plug_name if file_type == '0' else new_plug_info[0].plug_config_name}, status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '插件下载失败', '插件下载失败')
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)