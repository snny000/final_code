# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from django.core.serializers import serialize
from django.db import connection, transaction
from django.db.models import Count, Q
from django.http import HttpResponse
from monitor_serializers import *
from policy.models import TaskGroup
from policy.data_processing import rule_models
from director.data_processing import director_rule_models
from models import *
from DetectCenter import common, settings, tasks, date_util as du, file_util as fu, print_util as pu
from detector.models import Detector
from detector import judge_online
from DetectCenter import common_center_2_director as ccd
from collections import Counter
from requests_toolbelt import MultipartEncoder
import traceback
import datetime
import json
import os
import requests
import threading
import logging
import copy
import multiprocessing
import time
import xlsxwriter
import shutil
from DetectCenter import config, sender
from DetectCenter.business_config import *
from director.detect_center_reg_auth import check_global_director_connection
from director.models import DirectorTask

warning_serializers = [
    AlarmTrojanSerializer, AlarmAttackSerializer, AlarmMalwareSerializer, AlarmOtherSerializer,
    AlarmAbnormalSerializer, SensitiveEmailSerializer, SensitiveImSerializer, SensitiveFileTransferSerializer,
    SensitiveHttpSerializer, SensitiveNetdiskSerializer, SensitiveOtherSerializer, TargetInterceptIPSerializer,
    TargetInterceptDNSSerializer, TargetInterceptURLSerializer, TargetInterceptAccountSerializer, BlockSerializer
]   # 告警序列化类列表


warning_models = [
    AlarmTrojan, AlarmAttack, AlarmMalware, AlarmOther, AlarmAbnormal,
    SensitiveEmail, SensitiveIm, SensitiveFileTransfer, SensitiveHttp, SensitiveNetdisk, SensitiveOther,
    TargetInterceptIP, TargetInterceptDNS, TargetInterceptURL, TargetInterceptAccount, Block
]   # 告警model列表


# ************************************** 处理前端检测器请求 **************************************

# logger_alarm = logging.getLogger('project.alarm')
# logger_record = logging.getLogger('project.record')


# 判断上传的告警有无重复的ID（包括是否与数据库原有记录重复，是否本次上传中有重复）
def judge_same_alarm_id(data_list, detector_id):
    repeat_id_list = []  # 重复告警id列表

    alarm_id_list = [data['id'] for data in data_list]
    is_repeat_id = AlarmAll.objects.filter(device_id=detector_id, alarm_id__in=alarm_id_list)
    if is_repeat_id.exists():  # 数据库存在上传的ID
        for data in is_repeat_id:
            repeat_id_list.append(data.alarm_id)
        return common.detector_message_response(400, json.dumps(
            repeat_id_list, encoding='utf-8') + '中的告警id在数据库中已存在', '列表' + json.dumps(
            repeat_id_list, encoding='utf-8') + '中的告警id与以往记录重复')

    count_dict = Counter(alarm_id_list)
    if len(alarm_id_list) != len(count_dict):  # 上传的告警中有重复的ID
        for k, v in count_dict.iteritems():
            if v > 1:
                repeat_id_list.append(k)
        return common.detector_message_response(400, '上传的告警中存在重复的ID : ' + json.dumps(
            repeat_id_list, encoding='utf-8'), '上传的告警中存在重复的ID : ' + json.dumps(
            repeat_id_list, encoding='utf-8'))

    return False


BUSINESS_TYPE_MODEL_MAP = {
    'JCQ_GJQM_TROJAN': 0,             # 木马攻击窃密检测
    'JCQ_GJQM_ATTACK': 1,             # 漏洞利用检测
    'JCQ_GJQM_MALWARE': 2,            # 恶意程序检测
    'JCQ_GJQM_OTHER': -1,              # 其他攻击窃密检测
    'JCQ_GJQM_ABNORMAL': 3,           # 未知攻击窃密检测
    'JCQ_CSSM_MB': -1,                 # 密标文件检测
    'JCQ_CSSM_SENSITIVE': -1,          # 标密文件检测（暂时没有）
    'JCQ_CSSM_KEYWORD': 4,            # 关键词检测
    'JCQ_CSSM_FILTEREDENC': 5,        # 加密检测
    'JCQ_CSSM_FILTEREDCOM': 6,        # 压缩检测
    'JCQ_CSSM_FILTEREDPIC': 7,        # 图文筛选
    'JCQ_CSSM_LAYOUT': -1,             # 版式检测
    'JCQ_MBSJ_IP': 8,                 # IP审计
    'JCQ_MBSJ_DOMAIN': 9,             # 域名审计
    'JCQ_MBSJ_URL': 10,                # URL审计
    'JCQ_MBSJ_ACCOUNT': 11,            # 账号审计
    'JCQ_TXZD_BLOCK': 17,              # 通信阻断告警
    'JCQ_XWSJ_NETLOG_FILE': 12,        # 通联关系审计
    'JCQ_XWSJ_APPBEHAVIOR_FILE': 13    # 应用行为审计
}

# 处理网络攻击窃密、未知攻击窃密和目标审计上报数据，序列化后存入数据库
# （先取出重要字段存入alarm_all数据表，再提取出自动生成的id与原有数据一同插入特定的告警表）
def process_post_data_alarm(request, serializer_instance, warning_module, warning_type,
                            source_type, business_type, from_type=''):

    # sid = transaction.savepoint()  # 事务保存点
    try:
        report_time = du.get_current_time()           # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        data_list = common.detector_upload_json_preprocess(request_data)  # 返回List()格式的上传json数据
        if isinstance(data_list, Response):
            return data_list
        is_same = judge_same_alarm_id(data_list, detector_id)
        # if isinstance(is_same, Response):  # 返回告警ID重复的响应信息
        #     return is_same

        alarm_type = {v: k for k, v in common.WARN_TYPE.iteritems()}[warning_type]
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, alarm_type, len(data_list)))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, alarm_type, len(data_list))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        show_data_list = []          # 需要插入alarm_all
        alarm_data_list = []         # 告警数据组装之后的列表
        business_data_list = []      # 发送到业务数据服务器上的列表[(请求头, 数据),...]
        command_send_data = []       # 发送到指挥中心的数据[(请求头, 数据),...]
        handle_data = copy.deepcopy(data_list)   # 生成业务处置系统所需文件的告警数据

        number = 0                   # 告警数量
        for data in data_list:       # 循环遍历
            data = process_null_field(data)  # 兼容Null字段

            business_request_data = copy.deepcopy(data)    # 业务数据传输请求数据
            business_request_data['task_id'] = 0

            show_data_dict = {}
            # 将id改为alarm_id
            show_data_dict['alarm_id'] = data['id']
            data['alarm_id'] = data['id']

            result = common.check_time_field(data)
            if isinstance(request, Response):
                return result

            if 'proto_info' in data:   # 传输恶意程序的应用协议信息
                proto_info = data.pop('proto_info')
                data = dict(data, **proto_info)     # 合并字典

            if 'attachment' in data:   # 账号审计
                data['attachment'] = json.dumps(data['attachment'])

            data['device_id'] = detector_id       # 加入检测器id字段
            data['report_time'] = report_time     # 加入上报时间字段

            # for k, v in data.iteritems():
            #     if v is None:
            #         data[k] = ''

            show_data_dict['sip'] = data.get('sip', '127.0.0.1')
            show_data_dict['dip'] = data.get('dip', '127.0.0.1')
            show_data_dict['risk'] = data.get('risk', -1)
            show_data_dict['device_id'] = detector_id
            show_data_dict['time'] = data['time']
            show_data_dict['warning_module'] = warning_module
            show_data_dict['warning_type'] = warning_type
            show_data_dict['rule_id'] = data.get('rule_id', 0)
            show_data_dict['group_id'] = 0

            # 填充任务组ID
            if show_data_dict['rule_id'] != 0:
                policy_type = BUSINESS_TYPE_MODEL_MAP[business_type]
                if policy_type != -1:
                    for rule_model in [rule_models[policy_type], director_rule_models[policy_type]]:
                        rules = rule_model.objects.filter(rule_id=show_data_dict['rule_id'])
                        if rules.exists():
                            if hasattr(rules[0], 'group_id') and rules[0].group_id is not None:
                                show_data_dict['group_id'] = rules[0].group_id
                                business_request_data['task_id'] = rules[0].group_id
                            elif hasattr(rules[0], 'task_id') and rules[0].task_id is not None:
                                show_data_dict['group_id'] = rules[0].task_id
                                business_request_data['task_id'] = rules[0].task_id
                            break

            show_data_list.append(show_data_dict)
            alarm_data_list.append(data)
            number += 1

            if config.const.UPLOAD_BUSINESS:
                # 构建传输到业务数据服务器上的请求头和请求数据
                business_request_header = {
                    'Host': business_host,
                    'Date': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),
                    'Content-Type': 'application/json',
                    'Version': '1.0',
                    # 'Cookie': 'unknown',
                    'Source-Type': source_type,
                    'Data-Type': 'msg',
                    'User-Agent': request.META.get('HTTP_USER_AGENT'),
                    'Capture-Date': data['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                    'BusinessData-Type': business_type,
                    'Meta-Data': json.dumps({
                        'id': data['alarm_id'],
                        'from_id': '',
                        'from_type': from_type
                    }),
                }  # 业务数据传输请求头
                business_data_list.append((business_request_header, business_request_data))

            if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
                common_header = ccd.get_common_command_header_of_detector('alert', source_type, business_type, request, detector_id, data['time'], data_type='msg', task_type=str(business_request_data['task_id']))
                command_data = json.dumps(business_request_data, ensure_ascii=False).encode('utf-8')
                ccd.upload_json_2_director_of_detector(common_header, data, command_data, alarm_type, from_type, task_id=str(business_request_data['task_id']), async_level=1)

            send_alarm_file_to_director(show_data_dict['warning_type'], show_data_dict, source_type, business_type, request)  # 发送先到的告警文件

        serializer_all = AlarmAllSerializer(data=show_data_list, many=True)
        if serializer_all.is_valid():
            serializer_all.save()  # 存储数据库alarm_all
        elif common.is_serial_id_overflow_errer(serializer_all.errors):
            for data in show_data_list:
                AlarmAll.objects.create(**data)
        else:
            return common.detector_message_response(400, json.dumps(serializer_all.errors),
                                                    '数据缺失或字段不符合规定，序列化出错')

        # Bug
        # id_list = list(AlarmAll.objects.all().order_by('-id')[0: number].values_list('id', flat=True))  # 获取刚插入的主键id
        # id_list.reverse()
        # for i in range(number):
        #     alarm_data_list[i]['id'] = id_list[i]    # 每一条告警的主键id就是刚插入AlarmAll中数据的id

        for alarm_data in alarm_data_list:
            alarm_info = AlarmAll.objects.filter(alarm_id=alarm_data['alarm_id'])
            if alarm_info.exists():
                alarm_data['id'] = alarm_info[0].id

        serializer = serializer_instance(data=alarm_data_list, many=True)
        if serializer.is_valid() or common.is_serial_id_overflow_errer(serializer.errors):
            # transaction.savepoint_commit(sid)  # 提交

            # 将告警数据传输到业务数据处理服务器上
            if config.const.UPLOAD_BUSINESS:
                sender.async_send_business_data('project.alarm', business_type, detector_id, business_data_list)

            # 生成业务处置系统所需文件(告警元信息)
            if config.const.UPLOAD_BUSINESS_DISPOSAL:
                file_dir = ''
                file_name = ''
                handle_data_type = ''
                if warning_type == common.WARN_TYPE['trojan']:
                    # business_type = 'alarm'
                    handle_data_type = 'trojan_alarm'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'alarm')
                    file_name = 'alarm_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['attack']:
                    # business_type = 'alarm'
                    handle_data_type = 'attack_alarm'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'alarm')
                    file_name = 'alarm_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['malware']:
                    # business_type = 'alarm'
                    handle_data_type = 'malware_alarm'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'alarm')
                    file_name = 'alarm_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['other']:
                    # business_type = 'alarm'
                    handle_data_type = 'other_alarm'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'alarm')
                    file_name = 'alarm_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['abnormal']:
                    # business_type = 'alarm'
                    handle_data_type = 'abnormal_alarm'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'abnormal')
                    file_name = 'abnormal_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['intercept_ip']:
                    # business_type = 'object_listen'
                    handle_data_type = 'ip_listen'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'object_listen')
                    file_name = 'object_listen_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['intercept_dns']:
                    # business_type = 'object_listen'
                    handle_data_type = 'domain_listen'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'object_listen')
                    file_name = 'object_listen_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['intercept_url']:
                    # business_type = 'object_listen'
                    handle_data_type = 'url_listen'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'object_listen')
                    file_name = 'object_listen_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['intercept_account']:
                    # business_type = 'object_listen'
                    handle_data_type = 'account_listen'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'object_listen')
                    file_name = 'object_listen_alarm_' + str(int(time.time())) + '_' + str(1)
                elif warning_type == common.WARN_TYPE['block']:
                    # business_type = 'block'
                    handle_data_type = 'block'
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'block')
                    file_name = 'block_' + str(int(time.time())) + '_' + str(1)
                sender.send_business_disposal(file_dir, file_name, request.META.get('HTTP_USER_AGENT'), handle_data_type, handle_data)

            if serializer_all.is_valid():
                serializer.save()  # 存储数据库
            else:
                for data in alarm_data_list:
                    data = filter_unnecessary_field(warning_type, data)
                    warning_models[warning_type - 1].objects.create(**data)

            # judge_online.record_online_event(detector_id)  # 记录重新上线状态
            Detector.objects.filter(device_id=detector_id).update(last_warning_time=report_time)  # 修改最后告警时间，设置状态为在线
            # Detector.objects.filter(device_id=detector_id).update(last_warning_time=report_time, is_online=True)  # 修改最后告警时间，设置状态为在线

            return common.detector_message_response(200, '数据存储成功', {}, status.HTTP_200_OK)

        else:
            # transaction.savepoint_rollback(sid)   # 回滚
            alarm_ids = [item['id'] for item in alarm_data_list]
            AlarmAll.objects.filter(id__in=alarm_ids).delete()
            return common.detector_message_response(400, json.dumps(serializer.errors),
                                                    '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        # transaction.savepoint_rollback(sid)  # 回滚
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 处理违规泄密请求数据，序列化后存入数据库
def process_post_data_sensitive(request, source_type, business_type, from_type=''):
    try:
        report_time = du.get_current_time()           # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        data_list = common.detector_upload_json_preprocess(request_data)  # 返回List()格式的上传json数据
        if isinstance(data_list, Response):
            return data_list

        is_same = judge_same_alarm_id(data_list, detector_id)
        # if isinstance(is_same, Response):  # 返回告警ID重复的响应信息
        #     return is_same

        # 记录日志
        alarm_type = ''
        if len(data_list) > 0:
            alarm_type = ['unknown', 'finger', 'sensitive', 'keyword', 'encryption', 'compress', 'picture', 'picture_file', 'style'][data_list[0].get('alert_type', 0)]
            # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, alarm_type, len(data_list)))
            log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, alarm_type, len(data_list))
            fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        send_data_list = []  # 发送到业务数据服务器上的列表[(请求头, 数据),...]
        handle_data = []     # 生成业务处置系统所需文件的告警数据
        command_send_data = []  # 上传到指挥中心数据

        for data in data_list:  # 循环遍历
            data = process_null_field(data)      # 兼容Null字段

            business_request_data = copy.deepcopy(data)  # 业务数据传输请求数据
            business_request_data['task_id'] = 0
            handle_data.append(business_request_data)

            # 数据重新处理
            show_data = {}
            # 将id改为alarm_id
            show_data['alarm_id'] = data['id']
            data['alarm_id'] = data['id']

            if 'app_pro' in data:                  # 数据字典中有app_pro字段
                app_pro = data['app_pro'].lower()  # 将协议类型化为小写字母，以便确定序列化类
            else:
                return common.detector_message_response(400, '请求数据中没有app_pro字段', '请求数据中没有app_pro字段')

            result = common.check_time_field(data)
            if isinstance(request, Response):
                return result

            # 违规泄密检测支持的协议与序列化类的对应关系
            protocol_dict = {
                'email': SensitiveEmailSerializer,
                'im': SensitiveImSerializer,
                'filetransfer': SensitiveFileTransferSerializer,
                'http': SensitiveHttpSerializer,
                'netdisk': SensitiveNetdiskSerializer,
                'other': SensitiveOtherSerializer
            }

            if 'app_opt' in data:   # 请求数据字典中有app_opt字段
                if app_pro in protocol_dict and app_pro != 'other':  # 根据协议类型选择不同的序列化类
                    protocol_opt = data.pop('app_opt')  # 取出app_opt字段
                    if not isinstance(protocol_opt, dict):
                        return common.detector_message_response(400, '请求数据中的app_opt字段值不是dict格式',
                                                                '请求数据中的app_opt字段值不是json格式')
                    if 'authinfo' in protocol_opt and protocol_opt['authinfo'] != '':
                        authinfo = protocol_opt.pop('authinfo')
                        protocol_opt['mail_from'] = authinfo.get('mail_from', '')
                        protocol_opt['rcpt_to'] = authinfo.get('rcpt_to', '')
                        protocol_opt['ehlo'] = authinfo.get('ehlo', '')
                    data = dict(data, **protocol_opt)  # 合并字典
                else:
                    app_pro = 'other'
                    if isinstance(data['app_opt'], dict):
                        data['app_opt'] = json.dumps(data['app_opt'])
                    else:
                        return common.detector_message_response(400, '请求数据中的app_opt字段值不是dict格式',
                                                                '请求数据中的app_opt字段值不是json格式')
            else:
                return common.detector_message_response(400, '请求数据中没有app_opt字段', '请求数据中没有app_opt字段')

            data['device_id'] = detector_id      # 加入检测器id字段
            data['report_time'] = report_time    # 加入上报时间字段

            show_data['sip'] = data.get('sip', '127.0.0.1')
            show_data['dip'] = data.get('dip', '127.0.0.1')
            show_data['risk'] = data.get('risk', -1)
            show_data['device_id'] = detector_id
            show_data['time'] = data['time']
            show_data['rule_id'] = data.get('rule_id', 0)
            show_data['group_id'] = 0

            if show_data['rule_id'] != 0:
                policy_type = BUSINESS_TYPE_MODEL_MAP[business_type]
                if policy_type != -1:
                    for rule_model in [rule_models[policy_type], director_rule_models[policy_type]]:
                        rules = rule_model.objects.filter(rule_id=show_data['rule_id'])
                        if rules.exists():
                            if hasattr(rules[0], 'group_id') and rules[0].group_id is not None:
                                show_data['group_id'] = rules[0].group_id
                                business_request_data['task_id'] = rules[0].group_id
                            elif hasattr(rules[0], 'task_id') and rules[0].task_id is not None:
                                show_data['group_id'] = rules[0].task_id
                                business_request_data['task_id'] = rules[0].task_id
                            break

            warn_type = {
                'email': common.WARN_TYPE['sensitive_email'],
                'im': common.WARN_TYPE['sensitive_im'],
                'filetransfer': common.WARN_TYPE['sensitive_filetransfer'],
                'http': common.WARN_TYPE['sensitive_http'],
                'netdisk': common.WARN_TYPE['sensitive_netdisk'],
                'other': common.WARN_TYPE['sensitive_other']
            }    # 协议类型和告警标号对应表
            show_data['warning_module'] = common.WARN_MODULE['sensitive']
            show_data['warning_type'] = warn_type[app_pro]

            # sid = transaction.savepoint()    # 事务保存点

            serializer_all = AlarmAllSerializer(data=show_data)
            if serializer_all.is_valid():
                # print "alarm_all: valid", data['id']
                serializer_all.save()  # 存储数据库alarm_all
            elif common.is_serial_id_overflow_errer(serializer_all.errors):
                # print "alarm_all: overflow", data['id']
                AlarmAll.objects.create(**show_data)
            else:
                # print "alarm_all: serializer.errors", json.dumps(serializer_all.errors), data['id']
                return common.detector_message_response(400, json.dumps(serializer_all.errors),
                                                        '数据缺失或字段不符合规定，序列化出错')

            # data['id'] = AlarmAll.objects.last().id   # 获取刚插入AlarmAll中的id
            alarm_info = AlarmAll.objects.filter(alarm_id=data['alarm_id'])
            if alarm_info.exists():
                data['id'] = alarm_info[0].id
            # for k, v in data.iteritems():
            #     if v is None:
            #         data[k] = ''

            # print "data_detail: ", data
            serializer = protocol_dict[app_pro](data=data)  # 数据序列化
            if serializer.is_valid() or common.is_serial_id_overflow_errer(serializer.errors):
                if serializer.is_valid():
                    # print "alarm_detail: valid app_pro: " + app_pro, data['alarm_id']
                    serializer.save()  # 存储数据库
                else:
                    # print "alarm_detail: overflow app_pro: " + app_pro, data['alarm_id']
                    data = filter_unnecessary_field(show_data['warning_type'], data)
                    warning_models[show_data['warning_type']-1].objects.create(**data)

                # if business_type != 'JCQ_CSSM_SENSITIVE':
                # 构建传输到业务数据服务器上的请求头和请求数据
                if config.const.UPLOAD_BUSINESS:
                    business_request_header = {
                        'Host': business_host,
                        'Date': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),
                        'Content-Type': 'application/json',
                        'version': '1.0',
                        # 'Cookie': 'unknown',
                        'Source-Type': source_type,
                        'Data-Type': 'msg',
                        'User-Agent': request.META.get('HTTP_USER_AGENT'),
                        'Capture-Date': data['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                        'BusinessData-Type': business_type,
                        'Meta-Data': json.dumps({
                            'id': data['alarm_id'],
                            'from_id': '',
                            'from_type': from_type
                        }),
                    }  # 业务数据传输请求头
                    sender.async_send_business_data('project.alarm', business_type, detector_id, [(business_request_header, business_request_data)])

                if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
                    common_header = ccd.get_common_command_header_of_detector('alert', source_type, business_type, request, detector_id,
                                                                              data['time'], data_type='msg', task_type=str(business_request_data['task_id']))
                    command_data = json.dumps(business_request_data, ensure_ascii=False).encode('utf-8')
                    ccd.upload_json_2_director_of_detector(common_header, data, command_data, alarm_type, from_type, task_id=str(business_request_data['task_id']), async_level=1)

                send_alarm_file_to_director(show_data['warning_type'], show_data, source_type, business_type, request)  # 发送先到的告警文件

            else:
                # print "alarm_detail: serializer.errors", json.dumps(serializer_all.errors), "app_pro: " + app_pro, data['alarm_id']
                # transaction.savepoint_rollback(sid)  # 回滚事务
                AlarmAll.objects.filter(id=data['id']).delete()
                return common.detector_message_response(400, json.dumps(serializer.errors),
                                                        '数据缺失或字段不符合规定，序列化出错')

        # judge_online.record_online_event(detector_id)    # 记录重新上线状态
        Detector.objects.filter(device_id=detector_id).update(last_warning_time=report_time)  # 修改最后告警时间，设置状态为在线
        # Detector.objects.filter(device_id=detector_id).update(last_warning_time=report_time, is_online=True)  # 修改最后告警时间，设置状态为在线

        # 生成业务处置系统所需文件(告警元信息)
        if config.const.UPLOAD_BUSINESS_DISPOSAL:
            file_dir = os.path.join(config.const.DISPOSAL_DIR, 'sensitive')
            file_name = 'sensitive_alarm_' + str(int(time.time())) + '_' + str(1)
            handle_data_type = handle_data[0]['alert_type']
            handle_data_type = ['finger_file', 'sensitive_file', 'keyword_file', 'encryption_file', 'compress_file', 'picture_file', 'picture_file', 'style_file'][handle_data_type - 1]
            sender.send_business_disposal(file_dir, file_name, request.META.get('HTTP_USER_AGENT'), handle_data_type, handle_data)

        return common.detector_message_response(200, '数据存储成功' + data['alarm_id'], {}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


file_log_str = ['file_trojan', 'file_attack', 'file_malware', 'file_other', 'file_abnormal', 'file_mb', 'file_sensitive',
                'file_keyword', 'file_encryption', 'file_compress', 'file_picture', 'file_style', 'file_intercept_ip',
                'file_intercept_dns', 'file_intercept_url', 'file_intercept_account']


# 在收到告警数据后发送先到的告警文件到指挥中心
def send_alarm_file_to_director(warn_type, alarm_data, source_type, business_type, request):
    """
    在收到告警数据后发送先到的告警文件
    :param warn_type:         告警小类，对应16类
    :param alarm_data:        告警总览表的数据
    :param source_type:       策略大类
    :param business_type:     策略小类
    :param request:           请求
    :return:
    """
    if warn_type == 16:  # 通信阻断
        return
    print '############发送先到的告警文件到指挥中心'
    # alarm_file_info = warning_file_models[warn_type-1].objects.filter(alarm_id=alarm_data['alarm_id'])
    alarm_file_info = AlarmAllFile.objects.filter(alarm_id=alarm_data['alarm_id'])
    if alarm_file_info.exists() and config.const.UPLOAD_DIRECTOR and check_global_director_connection():
        alarm_type = file_log_str[common.BUSINESS_TYPE.index(business_type) - 1]
        alarm_file_data = json.loads(serialize('json', alarm_file_info))[0]['fields']
        if 'report_time' in alarm_file_data and alarm_file_data['report_time'] is not None:
            alarm_file_data['report_time'] = alarm_file_data['report_time'].replace('T', ' ')
        if 'time' in alarm_file_data and alarm_file_data['time'] is not None:
            alarm_file_data['time'] = alarm_file_data['time'].replace('T', ' ')

        print 'alarm_file_data:', pu.pretty_print_format(alarm_file_data)
        print 'alarm_show_data:', alarm_data
        print 'source_type:', source_type, ' business_type:', business_type
        common_header = ccd.get_common_command_header_of_detector('alert', source_type, business_type + '_FILE', request, alarm_data['device_id'], alarm_data['time'], task_type=str(alarm_data['group_id']))
        ccd.upload_file_2_director_of_detector(common_header, alarm_file_data, json.dumps((alarm_file_data['filename'], common.MEDIA_ROOT + alarm_file_data['save_path'])), alarm_type, from_type=business_type, risk=alarm_data['risk'], task_id=str(alarm_data['group_id']), async_level=1)      # 上传文件到指挥节点


# 兼容Null字段
def process_null_field(data):
    for field in data:
        if data[field] is None:
            print '###Null字段', field
            if field == 'rule_id':
                data[field] = 0
            elif field == 'ret_code':
                data[field] = -1
            else:                                  # 字符字段
                data[field] = 'null'
        elif data[field] == '' and field in ('sip', 'dip'):  #########临时处理  sip dip
            print '@@@空串字段sip, dip', field
            data[field] = '0.0.0.0'
        elif isinstance(data[field], dict):
            for key in data[field]:
                if data[field][key] is None:
                    print '###Null字段', key
                    if key == 'rule_id':
                        data[field][key] = 0
                    elif key == 'ret_code':      # MBSJ: alarm_intercept_url  CSSM: sensitive_http
                        data[field][key] = -1
                    else:                          # 字符字段
                        data[field][key] = 'null'
                elif data[field][key] == '' and key in ('sip', 'dip'):
                    print '@@@空串字段sip, dip', key
                    data[field][key] = '0.0.0.0'

    # print '去除Null字段后告警数据：', pu.pretty_print_format(data)
    return data


# 多余多余字段
def filter_unnecessary_field(warning_type, data):
    result_set = ()
    if warning_type == 1:      # 木马攻击窃密
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'trojan_id',
                  'os', 'trojan_name', 'trojan_type', 'desc', 'report_time',
                  'device_id')
    elif warning_type == 2:    # 漏洞利用窃密
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'attack_type',
                  'application', 'os', 'report_time', 'device_id')
    elif warning_type == 3:    # 恶意程序窃密
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'malware_type',
                  'malware_name', 'protocol', 'sender', 'recver', 'cc',
                  'bcc', 'subject', 'mail_from', 'rcpt_to', 'ehlo',
                  'report_time', 'device_id')
    elif warning_type == 4:    # 其他攻击窃密
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'desc',
                  'report_time', 'device_id')
    elif warning_type == 5:    # 未知攻击窃密
        result_set = ('id', 'alarm_id', 'sip', 'sport', 'smac', 'dip',
                  'dport', 'dmac', 'alert_type', 'alert_policy',
                  'alert_desc', 'time', 'risk', 'report_time',
                  'device_id')
    elif warning_type == 6:    # 违规泄密——电子邮件协议
        result_set = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'sender', 'receiver', 'cc',
                  'bcc', 'subject', 'domain', 'mail_from', 'rcpt_to',
                  'ehlo', 'protocol', 'report_time', 'device_id')
    elif warning_type == 7:    # 违规泄密——即时通信协议
        result_set = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'sender', 'receiver',
                  'account', 'msg_content', 'report_time', 'device_id')
    elif warning_type == 8:    # 违规泄密——文件传输协议
        result_set = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'account', 'pwd',
                  'trans_dir', 'report_time', 'device_id')
    elif warning_type == 9:    # 违规泄密——网页发布协议
        result_set = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'domain', 'url',
                  'method', 'ret_code', 'user_agent', 'cookie',
                  'server', 'refer', 'report_time', 'device_id')
    elif warning_type == 10:    # 违规泄密——网盘协议
        result_set = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'account',
                  'domain', 'report_time', 'device_id')
    elif warning_type == 11:    # 违规泄密——其他协议
        result_set = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'app_opt', 'report_time',
                  'device_id')
    elif warning_type == 12:    # IP侦听
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'report_time',
                  'device_id')
    elif warning_type == 13:    # 域名帧听
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'dns',
                  'domain_ip', 'report_time', 'device_id')
    elif warning_type == 14:    # URL侦听
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'url',
                  'method', 'ret_code', 'user_agent', 'cookie',
                  'server', 'refer', 'report_time', 'device_id')
    elif warning_type == 15:    # 账号侦听
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'sender',
                  'receiver', 'cc', 'bcc', 'subject', 'mail_content',
                  'attachment', 'report_time', 'device_id')
    elif warning_type == 16:    # 阻断告警
        result_set = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip',
                  'dport', 'dmac', 'time', 'report_time', 'device_id')
    else:
        pass
    copy_data = data.copy()

    for key in copy_data:
        if key not in result_set:
            data.pop(key)
    return data


# 原始报文上传（一次处理一个文件）处理接口：根据serializer_instance实例对请求数据进行序列化，
# 存入相应的数据库，上传的文件存储到服务器
def process_post_file(request, file_relative_path,
                      source_type, business_type, from_type=''):
    try:
        send_file = request.body
        report_time = du.get_current_time()           # 获取当前时间
        common.print_header_data(request)                 # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        # 含有is_upload的告警
        # serial_class = [AlarmTrojanFileSerializer, AlarmAttackFileSerializer, AlarmMalwareFileSerializer,
        #                 AlarmOtherFileSerializer, AlarmAbnormalFileSerializer, SensitiveAllFileSerializer,
        #                 TargetInterceptIPFileSerializer, TargetInterceptDNSFileSerializer, TargetInterceptDNSFileSerializer, TargetInterceptAccountFileSerializer]
        # model_class = [AlarmTrojanFile, AlarmAttackFile, AlarmMalwareFile, AlarmOtherFile, AlarmAbnormalFile, SensitiveAllFile,
        #                TargetInterceptIPFile, TargetInterceptDNSFile, TargetInterceptURLFile, TargetInterceptAccount]

        data = request.META.get('HTTP_CONTENT_FILEDESC')    # 数据字段
        data = common.check_detector_upload_header_filedesc_field(data)  # 校验Content-Filedesc字段
        if isinstance(data, Response):
            return data

        if 'id' in data:  # 将id改为alarm_id
            data['alarm_id'] = data.pop('id')
        else:
            return common.detector_message_response(400, '请求数据中没有id字段', '请求数据中没有id字段')

        result = common.check_time_field(data)
        if isinstance(request, Response):
            return result

        data['device_id'] = detector_id  # 加入检测器id字段
        data['report_time'] = report_time  # 加入上报时间字段

        is_upload = data.get('is_upload')
        # if is_upload == 'false':
        #     # print 'a1'
        #     data['is_upload'] = False
        #     is_upload = False
        # elif is_upload == 'true':
        #     # print 'a2'
        #     data['is_upload'] = True
        #     is_upload = True
        # print len(request.FILES)
        # print is_upload
        # print is_upload is False
        filename = data['filename']   # 文件名

        # 存储文件
        if len(request.FILES) == 1 and (is_upload is None or is_upload is False):   # 第一次上传一个文件
            file_absolute_path = os.path.join(common.MEDIA_ROOT, file_relative_path)  # 绝对路径（没有文件名）
            request_file = request.FILES.values()[0]
            # 文件重命名：检测器ID + '_' + 全局唯一编号 + '_' + 原文件名
            # save_file_name = common.rename_file(detector_id, request_file.name)
            save_file_name = common.rename_detector_upload_file(detector_id, filename)
            is_success = fu.handle_upload_file(file_absolute_path, request_file, save_file_name)  # 上传文件
            if not is_success:  # 文件上传失败
                return common.detector_message_response(400, '服务器上存在相同的文件', '文件已经上传或者文件命名重复')
            data['save_path'] = os.path.join(file_relative_path, save_file_name)   # 文件存储的相对路径
        elif len(request.FILES) == 0 and is_upload is True:     # 文件已经上传
            # file_info = model_class[serial_class.index(serializer_instance)].objects.filter(
            #     device_id=detector_id, checksum=data['checksum'])
            file_info = AlarmAllFile.objects.filter(device_id=detector_id, checksum=data['checksum'])
            if not file_info.exists():
                return common.detector_message_response(400, '数据库没有同名的文件记录', '该文件以前没有上传过')
            data['save_path'] = file_info.last().save_path   # 文件存储的相对路径
        else:
            return common.detector_message_response(400, '传输的数据和文件不符合规定', '传输的数据和文件不符合规定')

        # 日志记录
        alarm_type = file_log_str[common.BUSINESS_TYPE.index(from_type) - 1]
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, alarm_type, len(request.FILES)))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, alarm_type, len(request.FILES))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        # 存储数据
        if len(filename) > 64:
            data['filename'] = filename[:64]
            
        
        # 生成业务处置系统所需文件
        if config.const.UPLOAD_BUSINESS_DISPOSAL:
            # 告警数据文件描述
            if 'GJQM' in business_type:
                if 'ABNORMAL' in business_type:
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'abnormal')
                    file_name = 'abnormal_filedesc_' + str(int(time.time())) + '_' + str(1)
                else:
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'alarm')
                    file_name = 'alarm_filedesc_' + str(int(time.time())) + '_' + str(1)
            elif 'CSSM' in business_type:
                file_dir = os.path.join(config.const.DISPOSAL_DIR, 'sensitive')
                file_name = 'sensitive_filedesc_' + str(int(time.time())) + '_' + str(1)
            elif 'MBSJ' in business_type:
                file_dir = os.path.join(config.const.DISPOSAL_DIR, 'object_listen')
                file_name = 'object_listen_filedesc_' + str(int(time.time())) + '_' + str(1)
            
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_path = os.path.join(file_dir, file_name)
            f_handler = open(file_path, 'wb')
            f_handler.write(config.const.DISPOSAL_BOUNDARY + '\n')
            f_handler.write('User-Agent:' + request.META.get('HTTP_USER_AGENT') + '\n')
            f_handler.write('Content-Filedesc:' + request.META.get('HTTP_CONTENT_FILEDESC') + '\n')
            f_handler.close()
            # 告警数据文件
            try:
                # if not os.path.exists(common.MEDIA_ROOT + data['save_path']):
                shutil.copyfile(os.path.join(common.MEDIA_ROOT, data['save_path']), os.path.join(file_dir, detector_id + '_' + data['checksum']))
            except:
                traceback.print_exc()
        
        alarm = AlarmAll.objects.filter(alarm_id=data['alarm_id'])
        risk = -1
        if alarm.exists():
            risk = alarm[0].risk
        # serializer = serializer_instance(data=data)  # 数据序列化
        serializer = AlarmAllFileSerializer(data=data)  # 数据序列化
        if serializer.is_valid():
            serializer.save()  # 存储数据库

            # 将告警文件传输到业务数据处理服务器上
            if config.const.UPLOAD_BUSINESS:
                business_request_header = {
                    'Host': business_host,
                    'Date': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),
                    'Content-Type': request.META.get('HTTP_CONTENT_TYPE'),
                    'version': '1.0',
                    # 'Cookie': 'unknown',
                    'Source-Type': source_type,
                    'Data-Type': 'file',
                    'User-Agent': request.META.get('HTTP_USER_AGENT'),
                    'Capture-Date': data['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                    'BusinessData-Type': business_type,
                    'Meta-Data': json.dumps({
                        'id': '0',
                        'from_id': data['alarm_id'],
                        'from_type': from_type
                    }),
                    'Content-Filedesc': json.dumps({
                        'filetype': data['filetype'],
                        'filename': filename,
                        'checksum': data['checksum'],
                        'url': ''
                    }),
                }  # 业务数据传输请求头
                sender.async_send_business_file('project.alarm', business_type, detector_id, business_request_header, common.MEDIA_ROOT + data['save_path'], data['filename'])

            if alarm.exists() and config.const.UPLOAD_DIRECTOR and check_global_director_connection():  # 告警数据到了才发送文件
                print '#########数据先到了'

                common_header = ccd.get_common_command_header_of_detector('alert', source_type, business_type, request, detector_id, data['time'], task_type=str(alarm[0].group_id) if alarm.exists() else '0')
                ccd.upload_file_2_director_of_detector(common_header, data, json.dumps((data['filename'], common.MEDIA_ROOT + data['save_path'])), alarm_type, from_type, risk=risk, task_id=str(alarm[0].group_id) if alarm.exists() else '0', async_level=1)      # 上传文件到指挥节点

            return common.detector_message_response(200, '数据和文件存储成功', {}, status.HTTP_200_OK)
        else:
            return common.detector_message_response(400, json.dumps(serializer.errors),
                                                    '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)

# **************************************** 处理界面请求 ****************************************


# 构造告警页面查询条件，用于显示列表信息和总数
def get_alarm_query_terms(request_data):
    # 获取请求参数
    alarm_id = request_data.get('alarm_id')              # 告警ID
    device_id = request_data.get('device_id')            # 检测器ID
    contractor = request_data.get('contractor')          # 厂商
    organs = request_data.get('organs')                  # 检测器部署的客户单位
    risk = request_data.get('risk')                      # 告警级别
    warning_type = request_data.get('warning_type')      # 告警类型
    warning_module = request_data.get('warning_module')  # 告警模块
    time_min = request_data.get('time_min')              # 告警发生起始时间
    time_max = request_data.get('time_max')              # 告警发生结束时间

    rule_id = request_data.get('rule_id')
    group_id = request_data.get('group_id')
    group_name = request_data.get('group_name')

    detector_query_terms = {}
    if device_id is not None:
        detector_query_terms['device_id__contains'] = device_id
    if contractor is not None:
        detector_query_terms['contractor'] = contractor
    if organs is not None:
        detector_query_terms['organs__contains'] = organs

    alarm_query_terms = {}
    if alarm_id is not None:
        alarm_query_terms['alarm_id__contains'] = alarm_id
    if risk is not None:
        alarm_query_terms['risk'] = risk
    if warning_type is not None:
        alarm_query_terms['warning_type'] = warning_type
    if warning_module is not None:
        alarm_query_terms['warning_module'] = warning_module
    if time_min is not None:   # 生成任务的时间段筛选
        alarm_query_terms['time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        alarm_query_terms['time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)
    # if detector_query_terms:
    #     alarm_query_terms['device_id__in'] = list(Detector.objects.filter(**detector_query_terms).values_list('device_id', flat=True))
    # 即使没有设置detector_query_terms，也只查库里包含的检测器的告警
    alarm_query_terms['device_id__in'] = list(Detector.objects.filter(**detector_query_terms).values_list('device_id', flat=True))

    if rule_id is not None:
        alarm_query_terms['rule_id__contains'] = rule_id
    if group_id is not None:
        alarm_query_terms['group_id__contains'] = group_id
    if group_name is not None:
        groups = TaskGroup.objects.filter(name__contains=group_name)
        alarm_query_terms['group_id__in'] = groups.values_list('group_id')

    return alarm_query_terms


# 查询所有告警信息
def show_all_alarm(request):
    try:
        request_data = common.print_header_data(request)                    # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_alarm_query_terms(request_data)                   # 构造查询条件
        print query_terms

        detector_list = list(Detector.objects.all().values_list('device_id', 'contractor', 'organs'))
        detector_dict = {item[0]: (item[1], item[2]) for item in detector_list}
        print detector_dict

        query_data = AlarmAll.objects.filter(**query_terms).order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data,
                                    fields=('alarm_id', 'device_id', 'warning_module',
                                            'warning_type', 'sip', 'dip', 'risk', 'time', 'rule_id', 'group_id')
                                    )
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            fields['contractor'] = detector_dict[fields['device_id']][0] if fields['device_id'] in detector_dict else '未知'
            fields['organs'] = detector_dict[fields['device_id']][1] if fields['device_id'] in detector_dict else '未知'
            fields['time'] = fields['time'].replace('T', ' ')
            task_group = TaskGroup.objects.filter(group_id=fields['group_id'])
            if task_group.exists():
                fields['group_name'] = task_group[0].name
            else:
                fields['group_name'] = ''
            fields['rule_id'] = str(fields['rule_id'])
            fields['group_id'] = str(fields['group_id'])
            show_type = fields['warning_type']
            if show_type != 16:   # 阻断告警没有对应文件
                # query_data = warning_file_models[show_type - 1].objects.filter(alarm_id=fields['alarm_id'])
                query_data = AlarmAllFile.objects.filter(alarm_id=fields['alarm_id'])
                if query_data.exists():
                    # fields['file_path'] = common.MEDIA_ROOT + query_data[0].save_path
                    fields['file_path'] = query_data[0].save_path
                    fields['file_name'] = query_data[0].filename
                else:
                    fields['file_path'] = ''
                    fields['file_name'] = ''
            else:
                fields['file_path'] = ''
                fields['file_name'] = ''
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询告警总数
def show_alarm_count(request):
    try:
        request_data = common.print_header_data(request)    # 获取请求数据
        query_terms = get_alarm_query_terms(request_data)   # 构造查询条件

        count = AlarmAll.objects.filter(**query_terms).count()
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询告警详情
def show_alarm_detail(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        query_id = request_data.get('id')                   # 数据库自增id
        warning_type = request_data.get('warning_type')     # 告警类型

        # 参数判断
        if query_id is None:
            return common.ui_message_response(400, '请求url中没有携带参数id', '请求url中没有携带参数id')
        else:
            query_id = int(query_id)
        if warning_type is None:
            return common.ui_message_response(400, '请求url中没有携带参数warning_type', '请求url中没有携带参数warning_type')
        else:
            warning_models_num = int(warning_type) - 1

        alarm_detail = warning_models[warning_models_num].objects.filter(id=query_id)  # 提取出某条告警的基本信息
        # alarm_detail = warning_models[warning_models_num].objects.filter(alarm_id=query_id)  # 提取出某条告警的基本信息
        if not alarm_detail.exists():
            return common.ui_message_response(400, '数据库中不存在此id或者id与warning_type不匹配', '请求参数不正确')

        serializer_data = serialize('json', alarm_detail)
        list_data = json.loads(serializer_data)
        show_data = list_data[0]['fields']
        show_data['id'] = list_data[0]['pk']  # 加入主键id
        if 'xm_dir' in show_data:
            show_data['xm_dir'] = [u'发送', u'接收', u'未知'][show_data['xm_dir'] - 1]    # 修改传输方向为对应中文

        if 'time' in show_data:
            show_data['time'] = show_data['time'].replace('T', ' ')   # 去除因序列化时间类型出现的'T'
        show_data['report_time'] = show_data['report_time'].replace('T', ' ')
        if 'rule_id' in show_data:
            show_data['rule_id'] = str(show_data['rule_id'])
        # show_data['group_id'] = str(show_data['group_id'])

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 导出告警类型-告警数量统计报表   告警列表页
def export_alarm_detail_report(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        headings = [
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'木马编号', u'操作系统', u'木马名称', u'木马类型', u'告警描述'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'攻击类型', u'应用程序', u'操作系统'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'恶意程序种类', u'恶意程序名称', u'传输协议', u'发送者', u'接收者', u'邮件抄送者', u'邮件密送者', u'邮件主题', u'MAIL FROM', u'RCPT TO',
             u'EHLO'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'告警描述'],
            [u'检测器编号', u'告警编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'攻击类型', u'判断依据', u'判断描述'],
            [u'检测器编号', u'告警编号', u'告警类型', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'文件内嵌路径', u'涉密摘要', u'涉密描述', u'数据传输方向', u'协议类型', u'发件人', u'收件人', u'抄送', u'密送', u'邮件主题', u'邮件提供商',
             u'MAIL FROM', u'RCPT TO', u'EHLO', u'应用协议'],
            [u'检测器编号', u'告警编号', u'告警类型', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'文件内嵌路径', u'涉密摘要', u'涉密描述', u'数据传输方向', u'协议类型', u'应用协议', u'发件人', u'收件人', u'Im账户', u'聊天内容'],
            [u'检测器编号', u'告警编号', u'告警类型', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'文件内嵌路径', u'涉密摘要', u'涉密描述', u'数据传输方向', u'协议类型', u'应用协议', u'账户', u'密码', u'文件传输方向'],
            [u'检测器编号', u'告警编号', u'告警类型', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'文件内嵌路径', u'涉密摘要', u'涉密描述', u'数据传输方向', u'协议类型', u'应用协议', u'域名', u'URL', u'请求方法', u'响应码', u'USER-AGENT',
             u'Cookie', u'服务端Server', u'引用页'],
            [u'检测器编号', u'告警编号', u'告警类型', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'文件内嵌路径', u'涉密摘要', u'涉密描述', u'数据传输方向', u'协议类型', u'应用协议', u'账户', u'网盘类型'],
            [u'检测器编号', u'告警编号', u'告警类型', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别',
             u'文件内嵌路径', u'涉密摘要', u'涉密描述', u'数据传输方向', u'协议类型', u'协议要素'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别', u'域名',
             u'IP列表'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别', u'URL',
             u'请求方法', u'响应码', u'USER-AGENT', u'Cookie', u'服务端Server', u'引用页'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间', u'告警级别', u'发件人',
             u'收件人', u'抄送', u'密送', u'邮件主题', u'邮件内容', u'附件列表'],
            [u'检测器编号', u'告警编号', u'规则编号', u'源IP', u'源端口', u'源MAC', u'目的IP', u'目的端口', u'目的MAC', u'告警时间']
        ]

        show_fields = [
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk',
             'trojan_id', 'os', 'trojan_name', 'trojan_type', 'desc'),
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk',
             'attack_type', 'application', 'os'),
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk',
             'malware_type', 'malware_name', 'protocol', 'sender', 'recver', 'cc', 'bcc', 'subject', 'mail_from',
             'rcpt_to', 'ehlo'),
            (
            'device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk', 'desc'),
            ('device_id', 'alarm_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk', 'alert_type',
             'alert_policy', 'alert_desc'),
            ('device_id', 'alarm_id', 'alert_type', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time',
             'risk', 'sm_inpath', 'sm_summary', 'sm_desc', 'xm_dir', 'app_pro', 'sender', 'receiver', 'cc', 'bcc',
             'subject', 'domain', 'mail_from', 'rcpt_to', 'ehlo', 'protocol'),
            ('device_id', 'alarm_id', 'alert_type', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time',
             'risk', 'sm_inpath', 'sm_summary', 'sm_desc', 'xm_dir', 'app_pro', 'protocol', 'sender', 'receiver',
             'account', 'msg_content'),
            ('device_id', 'alarm_id', 'alert_type', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time',
             'risk', 'sm_inpath', 'sm_summary', 'sm_desc', 'xm_dir', 'app_pro', 'protocol', 'account', 'pwd',
             'trans_dir'),
            ('device_id', 'alarm_id', 'alert_type', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time',
             'risk', 'sm_inpath', 'sm_summary', 'sm_desc', 'xm_dir', 'app_pro', 'protocol', 'domain', 'url', 'method',
             'ret_code', 'user_agent', 'cookie', 'server', 'refer'),
            ('device_id', 'alarm_id', 'alert_type', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time',
             'risk', 'sm_inpath', 'sm_summary', 'sm_desc', 'xm_dir', 'app_pro', 'protocol', 'account', 'domain'),
            ('device_id', 'alarm_id', 'alert_type', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time',
             'risk', 'sm_inpath', 'sm_summary', 'sm_desc', 'xm_dir', 'app_pro', 'app_opt'),
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk'),
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk', 'dns',
             'domain_ip'),
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk', 'url',
             'method', 'ret_code', 'user_agent', 'cookie', 'server', 'refer'),
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time', 'risk',
             'sender', 'receiver', 'cc', 'bcc', 'subject', 'mail_content', 'attachment'),
            ('device_id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip', 'dport', 'dmac', 'time')
        ]

        device_id = request_data.get('device_id')  # 检测器ID
        alarm_id = request_data.get('alarm_id')  # 告警ID
        risk = request_data.get('risk')  # 告警级别
        warning_type = request_data.get('warning_type')  # 告警类型
        time_min = request_data.get('time_min')  # 告警发生起始时间
        time_max = request_data.get('time_max')  # 告警发生结束时间

        query_terms = {}
        if device_id is not None:
            query_terms['device_id__contains'] = device_id
        if alarm_id is not None:
            query_terms['alarm_id__contains'] = alarm_id
        if risk is not None:
            query_terms['risk'] = risk
        if time_min is not None:  # 生成任务的时间段筛选
            query_terms['time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
        if time_max is not None:
            query_terms['time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

        if not warning_type:
            return common.ui_message_response(400, '没有选择告警类型', [])
        alarm_type = int(warning_type) - 1  # 告警类型

        query_data = warning_models[alarm_type].objects.filter(**query_terms)
        serializer_data = serialize('json', query_data, fields=show_fields[alarm_type])
        list_data = json.loads(serializer_data)

        file_path = os.path.join(common.MEDIA_ROOT, 'alarm_report/')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_list = [u'木马告警.xlsx', u'漏洞告警.xlsx', u'恶意程序告警.xlsx', u'其他窃密告警.xlsx', u'未知攻击告警.xlsx', u'Email涉密.xlsx',
                     u'即时通信涉密.xlsx', u'FTP涉密.xlsx', u'HTTP涉密.xlsx', u'网盘涉密.xlsx', u'其他涉密.xlsx', u'IP审计.xlsx',
                     u'域名审计.xlsx', u'URL审计.xlsx', u'账号审计.xlsx', u'通信阻断.xlsx']
        file_name = file_list[alarm_type]
        relative_path = 'alarm_report/' + file_name
        file_path = os.path.join(file_path, file_name)
        workbook = xlsxwriter.Workbook(file_path)

        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write_row('A1', headings[alarm_type], bold)

        row = 2
        for data in list_data:
            fields = data['fields']
            fields['time'] = fields['time'].replace('T', ' ')
            worksheet.write_row('A' + str(row), [fields[k] for k in show_fields[alarm_type]])
            row += 1

        # 关闭并输出excel文件
        workbook.close()

        response = HttpResponse()
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name.encode('utf-8'))
        response['X-Accel-Redirect'] = '/media/{0}'.format(relative_path.encode('utf-8'))  # 支持断点续传
        return response
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)



def get_statistics_alarm_query_terms(request_data):
    # 获取请求参数
    alarm_id = request_data.get('alarm_id')  # 告警ID

    rule_id = request_data.get('rule_id')  # 策略id
    group_id = request_data.get('group_id')  # 任务组id
    business_type = request_data.get('warning_module')  # 告警类型（告警大类）
    alarm_type = request_data.get('warning_type')  # 告警类型（告警小类）
    risk = request_data.get('risk')  # 告警级别
    days = request_data.get('days')  # 最近天数
    time_min = request_data.get('time_min')  # 告警发生起始时间
    time_max = request_data.get('time_max')  # 告警发生结束时间
    device_id = request_data.get('device_id')  # 检测器ID
    # content_length = request_data.get('content_length')  # 消息长度

    alarm_query_terms = {}
    if device_id is not None:
        alarm_query_terms['device_id__contains'] = device_id

    if days is not None:
        try:
            days = int(days)
        except Exception:
            return common.ui_message_response(500, 'days 不是数字', 'days 不是数字',
                                              status.HTTP_500_INTERNAL_SERVER_ERROR)
        str_now = time.strftime('%Y-%m-%d', time.localtime())
        now_date = datetime.datetime.strptime(str_now, '%Y-%m-%d')
        alarm_query_terms['time__range'] = (now_date - datetime.timedelta(days=days), now_date + datetime.timedelta(days=1))
    # if content_length is not None:
    #     alarm_query_terms['content_length__contains'] = content_length
    if alarm_id is not None:
        alarm_query_terms['alarm_id__contains'] = alarm_id
    if risk is not None:
        alarm_query_terms['risk'] = risk

    if rule_id is not None:
        alarm_query_terms['rule_id__contains'] = rule_id

    if group_id is not None:
        alarm_query_terms['group_id__contains'] = group_id

    if business_type is not None:
        alarm_query_terms['warning_module'] = business_type
    if alarm_type is not None:
        alarm_query_terms['warning_type'] = alarm_type
    if time_min is not None:  # 生成任务的时间段筛选
        alarm_query_terms['time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        alarm_query_terms['time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

    return alarm_query_terms


#自定义排序方法
def cmp(x, y):
    if x.get('date') > y.get('date'):
        return 1
    elif x.get('date') < y.get('date'):
        return -1
    else:
        return 0

# 查询最近days（默认为30）天的告警数量
def show_alarm_last_days(request):
    try:
        common.print_header_data(request)  # 获取请求数据
        request_data = common.print_header_data(request)  # 获取请求数据
        alarm_query_terms = get_statistics_alarm_query_terms(request_data)
        print alarm_query_terms
        days = request_data.get('days')
        if days is not None:
            days = int(days)
        else:
            days = 30
        days_list = du.get_last_days(days)    # 获取最近时间段内的每一天时间list
        now_day_list = []  #存在于表中的日期

        start_date = days_list[0]
        # end_date = days_list[-1]
        end_date = (datetime.datetime.strptime(days_list[-1], '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        s = '%Y-%m-%d'
        # sql = '''SELECT alarm_all.id,DATE_FORMAT(alarm_all.time, %s) days,count(id) count FROM alarm_all WHERE alarm_all.time BETWEEN %s AND %s GROUP BY days'''
        # raw_query = AlarmAll.objects.filter(**alarm_query_terms).raw(sql, [s, start_date, end_date])

        raw_query = AlarmAll.objects.filter(**alarm_query_terms).extra(select={'time': 'date( time )'}).values('time') \
                                                .annotate(available=Count('time'))
        show_data = []
        for data in raw_query:
            show_data_dict = {}
            # now_day_list.append(data.days)
            # show_data_dict['date'] = data.days
            # show_data_dict['amount'] = data.count
            now_day_list.append(data['time'].strftime("%Y-%m-%d"))
            show_data_dict['date'] = data['time'].strftime("%Y-%m-%d")
            show_data_dict['amount'] = data['available']
            show_data.append(show_data_dict)

        list_null_date = list(set(days_list).difference(set(now_day_list)))   #获取表中没有告警的日期，将count置为0（由于count聚合时某一天时间，表中不存在则不会返回）

        for datas in list_null_date:  #将没有告警的日期加入要返回的数据中，并且按照时间顺序排序
            show_data_dict = {}
            show_data_dict['date'] = datas
            show_data_dict['amount'] = 0
            show_data.append(show_data_dict)
        show_data.sort(cmp)         #调用自定义排序方法
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 根据时间条件，查询所在时间段内的告警数量
def show_alarm_days(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        time_min = request_data.get('time_min')  # 起始时间条件
        time_max = request_data.get('time_max')  # 结束时间条件
        if time_max is None or time_min is None:
            return common.ui_message_response(400, '请求中没有time_max或者time_min参数', '请求中没有time_max或者time_min参数')
        alarm_query_terms = get_statistics_alarm_query_terms(request_data)
        num = (datetime.datetime.strptime(time_max, '%Y-%m-%d') - datetime.datetime.strptime(time_min,
                                                                                             '%Y-%m-%d')).days + 1
        days_list = []
        for day in range(num - 1, -1, -1):
            date = datetime.datetime.strptime(time_max, '%Y-%m-%d') - datetime.timedelta(days=day)
            days_list.append(date.strftime("%Y-%m-%d"))


        now_day_list = []  # 存在于表中的日期

        start_date = days_list[0]
        # end_date = days_list[-1]
        end_date = (datetime.datetime.strptime(days_list[-1], '%Y-%m-%d') + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        s = '%Y-%m-%d'
        # sql = '''SELECT alarm_all.id,DATE_FORMAT(alarm_all.time,%s) days,count(id) count FROM alarm_all WHERE alarm_all.time BETWEEN %s AND %s GROUP BY days'''
        # raw_query = AlarmAll.objects.filter(**alarm_query_terms).raw(sql, [s, start_date, end_date])
        raw_query = AlarmAll.objects.filter(**alarm_query_terms).extra(select={'time': 'date( time )'}).values('time') \
                                        .annotate(available=Count('time'))
        show_data = []
        for data in raw_query:
            show_data_dict = {}
            # now_day_list.append(data.days)
            # show_data_dict['date'] = data.days
            # show_data_dict['amount'] = data.count
            now_day_list.append(data['time'].strftime("%Y-%m-%d"))
            show_data_dict['date'] = data['time'].strftime("%Y-%m-%d")
            show_data_dict['amount'] = data['available']
            show_data.append(show_data_dict)

        list_null_date = list(
            set(days_list).difference(set(now_day_list)))  # 获取表中没有告警的日期，将count置为0（由于count聚合时某一天时间，表中不存在则不会返回）

        for datas in list_null_date:  # 将没有告警的日期加入要返回的数据中，并且按照时间顺序排序
            show_data_dict = {}
            show_data_dict['date'] = datas
            show_data_dict['amount'] = 0
            show_data.append(show_data_dict)
        show_data.sort(cmp)  # 调用自定义排序方法

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询各种条件下的的告警数量（以表的字段作为分类，进行告警统计） 该条件下必须设置query_condition参数
def show_alarm_all_types(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        alarm_query_terms = get_statistics_alarm_query_terms(request_data)
        query_condition = request_data.get('query_condition')
        if query_condition is None:
            return common.ui_message_response(400, '请求参数中没有query_condition参数', '请求参数中没有query_condition参数')
        num = request_data.get('num')
        show_data = AlarmAll.objects.filter(**alarm_query_terms).values(query_condition).annotate(
            amount=Count(query_condition)).order_by('-amount')[:num]

        if query_condition == 'rule_id':
            for data in show_data:
                data['rule_id'] = str(data['rule_id'])

        if query_condition == 'group_id':
            show_data = show_data.exclude(group_id=0)

            for data in show_data:
                data['group_id'] = str(data['group_id'])
                qs = TaskGroup.objects.filter(group_id=data['group_id'])
                if qs.exists():
                    data['name'] = qs.values()[0]['name'] + '\n' + data['group_id']
                else:
                    data['name'] = '其他' + '\n' + data['group_id']
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询任务组的告警数量  实际show_alarm_all_types已经包含
def show_alarm_task(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        num = request_data.get('num')
        alarm_query_terms = get_statistics_alarm_query_terms(request_data)
        group_id_list = list(TaskGroup.objects.exclude(group_id=0).values_list('group_id', flat=True))
        show_data = AlarmAll.objects.filter(**alarm_query_terms).filter(group_id__in=group_id_list).values('group_id').annotate(
            amount=Count('group_id')).order_by('-amount')[:num]
        for data in show_data:
            data['name'] = TaskGroup.objects.filter(group_id=data['group_id'])[0].name
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询各个organ的告警数，取出最多的num（默认为10）个（目前不需要,可以废弃）
# def show_alarm_several_users(request, num=10):
#     try:
#         common.print_header_data(request)  # 获取请求数据
#
#         cursor = connection.cursor()
#         sql = 'select organs, count(*) as amount from alarm_all, detector_info_new ' \
#               'where alarm_all.device_id = detector_info_new.device_id group by organs order by amount desc ' \
#               'limit ' + str(num)
#         cursor.execute(sql)
#         raw = cursor.fetchall()  # tuple
#         show_data = []
#         data_dict = {}
#         length = len(raw)
#         for i in range(length):
#             data_dict['organs'] = raw[i][0]
#             data_dict['amount'] = raw[i][1]
#             show_data.append(data_dict)
#             data_dict = {}  # 每次都需要重新申请内存, 否则show_data的数据都是最后一条的复制
#         cursor.close()
#         # connection.close()
#         return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
#     except Exception:
#         traceback.print_exc()
#         return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
#                                           status.HTTP_500_INTERNAL_SERVER_ERROR)


# 导出除了以时间为分类聚合的其他统计结果
def export_alarm_report(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_condition = request_data.get('query_condition')
        show_data = show_alarm_all_types(request).data.get('msg')
        if query_condition is None:
            return common.ui_message_response(400, '请求url中没有携带参数query_condition', '请求参数没有query_condition')
        else:
            if query_condition == 'device_id':
                headings = [u'检测器id', u'告警数量']
                alarm_data = []
                alarm_data.append([data[query_condition] for data in show_data])
                alarm_data.append([data['amount'] for data in show_data])

            elif query_condition == 'group_id':
                headings = [u'任务组id', u'告警数量']
                alarm_data = []
                alarm_data.append([data['name'] for data in show_data])
                alarm_data.append([data['amount'] for data in show_data])

            elif query_condition == 'warning_type':
                headings = [u'告警类型（小类）', u'告警数量']
                alarm_data = [
                    [u'木马攻击', u'漏洞利用', u'恶意程序', u'其他攻击', u'未知攻击',
                     u'Email涉密', u'Im涉密', u'FTP涉密', u'HTTP涉密', u'Netdisk涉密', u'其他涉密',
                     u'IP审计', u'域名审计', u'URL审计', u'账号审计', u'通信阻断'],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
                for data in show_data:
                    alarm_data[1][data['warning_type'] - 1] = data['amount']

            elif query_condition == 'warning_module':
                # 告警大类1.传输涉密，2.攻击窃密，3.未知攻击，4.目标审计，5.通信阻断，6.插件告警
                headings = [u'告警类型（大类）', u'告警数量']
                alarm_data = [
                    [u'攻击窃密', u'异常行为', u'违规泄密', u'目标帧听', u'通信阻断'],
                    [0, 0, 0, 0, 0]
                ]
                for data in show_data:
                    alarm_data[1][data['warning_module'] - 1] = data['amount']

            elif query_condition == 'risk':
                # 告警级别：0.无风险，1.一般级，2.关注级，3.严重级，4.紧急级
                headings = [u'告警级别', u'告警数量']
                alarm_data = [
                    [u'无风险', u'一般级', u'关注级', u'严重级', u'紧急级'],
                    [0, 0, 0, 0, 0]
                ]
                for data in show_data:
                    alarm_data[1][data['risk']] = data['amount']

        file_path = os.path.join(common.MEDIA_ROOT, 'statistics_report/')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = headings[0] + u'-告警统计报表.xlsx'
        relative_path = 'statistics_report/' + file_name
        file_path = os.path.join(file_path, file_name)
        workbook = xlsxwriter.Workbook(file_path)

        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})

        worksheet.write_row('A1', headings, bold)
        worksheet.set_column(0, 0, 15)
        worksheet.write_column('A2', alarm_data[0])
        worksheet.write_column('B2', alarm_data[1])

        chart = workbook.add_chart({'type': 'column'})
        # 配置series,这个和前面wordsheet是有关系的
        chart.add_series({
            'name': '=Sheet1!$B$1',
            'categories': '=Sheet1!$A$2:$A$' + str(len(show_data) + 1),
            'values': '=Sheet1!$B$2:$B$' + str(len(show_data) + 1)
        })

        # 添加标题和x,y轴标签，设置无图例
        chart.set_title({'name': headings[0] + u'-告警数量统计图'})
        chart.set_x_axis({'name': headings[0]})
        chart.set_y_axis({'name': u'告警数量', 'major_gridlines': {'visible': False}})
        chart.set_legend({'position': 'none'})

        # 设置图标风格
        chart.set_style(12)
        # 插入数据，调整x,y长度
        worksheet.insert_chart('E5', chart, {'x_scale': 1, 'y_scale': 2})

        # 关闭并输出excel文件
        workbook.close()

        # 下载文件
        return common.construct_download_file_header(file_path, relative_path, file_name)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 导出时间-告警数量统计报表(某段时间内告警态势)
def export_time_alarm_report(request):
    try:
        common.print_header_data(request)  # 获取请求数据
        show_data = show_alarm_days(request).data.get('msg')
        if isinstance(show_data, Response):
            return show_data
        headings = [u'时间', u'告警数量']
        alarm_data = []
        alarm_data.append([data['date'] for data in show_data])
        alarm_data.append([data['amount'] for data in show_data])
        file_path = os.path.join(common.MEDIA_ROOT, 'statistics_report/')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = u'时间-告警统计报表.xlsx'
        relative_path = 'statistics_report/' + file_name
        file_path = os.path.join(file_path, file_name)
        workbook = xlsxwriter.Workbook(file_path)

        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})

        worksheet.write_row('A1', headings, bold)
        worksheet.set_column(0, 0, 15)
        worksheet.write_column('A2', alarm_data[0])
        worksheet.write_column('B2', alarm_data[1])
        chart = workbook.add_chart({'type': 'column'})
        # 配置series,这个和前面wordsheet是有关系的
        chart.add_series({
            'name': '=Sheet1!$B$1',
            'categories': '=Sheet1!$A$2:$A$' + str(len(show_data) + 1),
            'values': '=Sheet1!$B$2:$B$' + str(len(show_data) + 1)
        })

        # 添加标题和x,y轴标签，设置无图例
        chart.set_title({'name': u'时间-告警数量统计图'})
        chart.set_x_axis({'name': u'时间'})
        chart.set_y_axis({'name': u'告警数量', 'major_gridlines': {'visible': False}})
        chart.set_legend({'position': 'none'})

        # 设置图标风格
        chart.set_style(12)
        # 插入数据，调整x,y长度
        worksheet.insert_chart('E5', chart, {'x_scale': 1, 'y_scale': 2})

        # 关闭并输出excel文件
        workbook.close()

        return common.construct_download_file_header(file_path, relative_path, file_name)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 导出时间-告警数量统计报表(最近一段时间时间内告警态势)
def export_last_days_report(request):
    try:
        common.print_header_data(request)  # 获取请求数据
        show_data = show_alarm_last_days(request).data.get('msg')
        headings = [u'时间', u'告警数量']
        alarm_data = []
        alarm_data.append([data['date'] for data in show_data])
        alarm_data.append([data['amount'] for data in show_data])
        file_path = os.path.join(common.MEDIA_ROOT, 'statistics_report/')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = u'时间-告警统计报表.xlsx'
        relative_path = 'statistics_report/' + file_name
        file_path = os.path.join(file_path, file_name)
        workbook = xlsxwriter.Workbook(file_path)

        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})

        worksheet.write_row('A1', headings, bold)
        worksheet.set_column(0, 0, 15)
        worksheet.write_column('A2', alarm_data[0])
        worksheet.write_column('B2', alarm_data[1])

        chart = workbook.add_chart({'type': 'column'})
        # 配置series,这个和前面wordsheet是有关系的
        chart.add_series({
            'name': '=Sheet1!$B$1',
            'categories': '=Sheet1!$A$2:$A$' + str(len(show_data) + 1),
            'values': '=Sheet1!$B$2:$B$' + str(len(show_data) + 1)
        })

        # 添加标题和x,y轴标签，设置无图例
        chart.set_title({'name': u'时间-告警数量统计图'})
        chart.set_x_axis({'name': u'时间'})
        chart.set_y_axis({'name': u'告警数量', 'major_gridlines': {'visible': False}})
        chart.set_legend({'position': 'none'})

        # 设置图标风格
        chart.set_style(12)
        # 插入数据，调整x,y长度
        worksheet.insert_chart('E5', chart, {'x_scale': 1, 'y_scale': 2})

        # 关闭并输出excel文件
        workbook.close()

        return common.construct_download_file_header(file_path, relative_path, file_name)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_statistics_count(request):
    """
    根据检测器id统计各种策略告警数量
    :param request:
    :return:
    """
    try:
        result = {}
        result_as = {}
        result_bs = {}
        request_data = common.print_header_data(request)  # 获取请求数据
        # 获取请求参数
        device_id = request_data.get('device_id')
        # device_id = 170307020002
        # 构造查询函数
        if device_id is not None:
            for i in range(len(common.WARN_MODULE)):
                result_bs[i] = AlarmAll.objects.filter(device_id=device_id, warning_module=i).count()
            result['warning_module'] = result_bs
            for j in range(len(common.WARN_TYPE)):
                result_as[j] = AlarmAll.objects.filter(device_id=device_id, warning_type=j).count()
            result['warning_type'] = result_as
            return common.ui_message_response(200, '统计各种策略告警数量成功', result, status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '请求中没有参数device_id', '请求中没有参数device_id')

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)



