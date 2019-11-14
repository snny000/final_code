# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from django.core.serializers import serialize
from django.db.models import F, Q, Count
from django.db import connection, transaction
from django.http import HttpResponse
from detector_serializers import *
from models import *
from DetectCenter import common, date_util as du, director_config, file_util as fu, config
from policy.policy_serializers import TaskSerializer
from policy.models import *
from monitor.models import AlarmAll
from director.models import DirectorTask
from director.data_processing import director_rule_models
from director.detect_center_reg_auth import check_global_director_connection

from policy.data_processing import rule_models, get_rule_fields
import detector_common as dc
from DetectCenter.business_config import *
import traceback
import json
import datetime
import xlsxwriter
import os
import xlrd
import copy
from DetectCenter import common_center_2_director as ccd
import logging
import requests
import time
from DetectCenter import sender


# ************************************** 测试请求 **************************************


# 测试方法
def aaa(request):
    try:
        print '测试方法'

        # 测试int型字段搜索包含contains关键词
        # from policy.models import TaskGroup
        # print TaskGroup.objects.filter(group_id__contains=1).count()

        # 测试 数据库表中查询记录中的空字段在非序列化和序列化后值  都为None
        # rules = TrojanRule.objects.filter()
        # if rules.exists():
        #     for rule in rules:
        #         print "no serializer:", rule.group_id
        #         # print rule
        #
        # rule_all = serialize('json', rules, fields=('rule_id', 'trojan_id', 'trojan_name', 'trojan_type', 'os', 'desc', 'rule', 'risk', 'store_pcap', 'group_id'))
        # rule_all = json.loads(rule_all)
        # for rule in rule_all:
        #     print 'serializer:', rule['fields'].get('group_id')
        #     print rule['fields']

        # query_terms = {'alarm_status': 'on', 'device_status': 1}
        # detector = Detector.objects.filter(**query_terms)
        # for d in detector:
        #     print d.device_id

        return common.ui_message_response(200, '请求成功', '请求成功', status.HTTP_200_OK)

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


#
# 测试方法   将device_status 为 3 4的还原
def resetAuditState(request):
    try:
        print '测试方法   将device_status 为 3 4的还原'

        Detector.objects.filter(device_status__in=(3, 4)).update(register_status=2, auth_status=1, device_status=2)

        return common.ui_message_response(200, '请求成功', '请求成功', status.HTTP_200_OK)

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# ************************************** 处理前端检测器请求 **************************************


# logger_status = logging.getLogger('project.status')


def check_register_detector(request):
    detector_id = common.get_detector_id(request)  # 获取检测器ID
    if isinstance(detector_id, Response):
        return detector_id  # 返回响应信息

    detector_info = Detector.objects.filter(device_id=detector_id)  # 查询是否注册
    if detector_info.exists():
        return common.detector_message_response(200, '检测器已经提交过注册请求', {'message': '检测器已经提交过注册请求'},
                                                status.HTTP_200_OK)
    return detector_id


# 注册处理
def register(request):
    try:
        register_time = du.get_current_time()  # 获取注册时间
        # request_data = common.print_header_data(request)  # 获取请求数据
        request_data = json.loads(request.body)
        print 'register_data:', request_data

        detector_id = check_register_detector(request)
        if isinstance(detector_id, Response):
            return detector_id

        data = dc.check_dict_data(request_data)
        if isinstance(data, Response):
            return data


        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'register', 0 if not data else 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')


        # 加入检测器ID、注册时间字段，修改contact,interface,cpu_info,disk_info为字符串存入数据库
        data['device_id'] = detector_id
        data['register_time'] = register_time
        data['register_status'] = 2  # (0: 注册成功 1: 注册失败 2: 注册未审核)
        data['auth_status'] = 2  # (0: 认证成功 1: 认证失败 2: 未认证)
        data['device_status'] = common.DETECTOR_STATUS['register_no_check']
        if 'contact' in data and isinstance(data.get('contact'), (dict, list)):
            data['contact'] = json.dumps(data.get('contact'), encoding='utf-8', ensure_ascii=False)
        if 'interface' in data and isinstance(data.get('interface'), (dict, list)):
            data['interface'] = json.dumps(data.get('interface'))
        if 'cpu_info' in data and isinstance(data.get('cpu_info'), (dict, list)):
            data['cpu_info'] = json.dumps(data.get('cpu_info'))
        if 'disk_info' in data and isinstance(data.get('disk_info'), (dict, list)):
            data['disk_info'] = json.dumps(data.get('disk_info'))
        if '01' != data.get('device_type'):
            return common.detector_message_response(400, 'device_type不是01', 'device_type不正确')
        data['contractor'] = detector_id[4:6]

        serializer = DetectorSerializer(data=data)  # 数据序列化
        if serializer.is_valid():
            serializer.save()  # 存储数据库

            # 生成业务处置系统所需文件(告警元信息)
            if config.const.UPLOAD_BUSINESS_DISPOSAL:
                handle_data_type = 'detector_register'
                file_dir = os.path.join(config.const.DISPOSAL_DIR, 'detector_register')
                file_name = 'detector_register_' + str(int(time.time())) + '_' + str(1)
                dis_data = copy.deepcopy(data)
                dis_data['register_time'] = du.get_current_date_string()
                sender.send_business_disposal(file_dir, file_name, request.META.get('HTTP_USER_AGENT'),
                                              handle_data_type, dis_data)


            process_auto_audit(data, detector_id)
            return common.detector_message_response(200, '注册请求提交成功',
                                                    {'message': '注册请求发送成功，等待人工审核'}, status.HTTP_200_OK)
        return common.detector_message_response(400, json.dumps(serializer.errors),
                                                '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


#处理检测器注册自动审核逻辑
def process_auto_audit(data, device_id):
    print '处理自动审核'
    mode = 1
    mode_info = DetectorAuditMode.objects.all()
    if not mode_info.exists():
        DetectorAuditMode.objects.create(**{'id': 1, 'mode': mode})
    else:
        mode = mode_info[0].mode

    if mode == 0:
        device_msg = DeviceInfo.objects.filter(device_id=device_id)
        if device_msg.exists():
            check_message = ''  # 注册失败原因（注册成功，此处为空）
            if not is_list_ele_equal(json.loads(device_msg[0].cpu_info), json.loads(data['cpu_info'])):
                check_message += 'CPU信息不一致,'
            if not is_list_ele_equal(json.loads(device_msg[0].disk_info), json.loads(data['disk_info'])):
                check_message += '硬盘信息不一致,'
            if not is_list_ele_equal(json.loads(device_msg[0].interface), json.loads(data['interface'])):
                check_message += '网卡信息不一致,'
            if device_msg[0].mem_total != data['mem_total']:
                check_message += '内存不一致,'
            if 'device_ca' not in data or device_msg[0].device_ca != data['device_ca']:
                check_message += '检测器CA数字证书序列号不一致,'

            if check_message == '':
                check_type = 0  # 审核状态（0：注册成功；1：注册失败；2：注册未审核）
            else:
                check_type = 1
                check_message = check_message[0:-1]
            check_person = '自动审核'  # 审核人（此参数可能会由其他路径传入）

            # 审核状态（前者表示审核通过，后者表示审核未通过）
            check_status = [common.DETECTOR_STATUS['register_success'], common.DETECTOR_STATUS['register_fail'],
                            common.DETECTOR_STATUS['register_no_check']]
            Detector.objects.filter(device_id=device_id).update(register_status=int(check_type),
                                                                        register_fail_reason=check_message, auth_status=2,
                                                                        auth_fail_reason='#未认证#', auth_frequency=0,
                                                                        op_person=check_person, op_ip='127.0.0.1',
                                                                        op_time=du.get_current_time(),
                                                                        device_status=check_status[int(check_type)])


# 判断两个list中的元素是否相等
def is_list_ele_equal(list1, list2):
    import copy
    if not isinstance(list1, list) or not isinstance(list2, list):
        return False
    l1 = copy.deepcopy(list1)
    l2 = copy.deepcopy(list2)
    for i in range(l1.__len__()):
        l1[i] = json.dumps(l1[i])
    for i in range(l2.__len__()):
        l2[i] = json.dumps(l2[i])
    # print set(l1)
    # print set(l2)
    diff = set(l1).difference(set(l2))
    from DetectCenter import print_util as pu
    if diff.__len__() == 0:
        return True
    else:
        print "@@@@", pu.pretty_print_format(list(diff))
        return False


# 校验注册的检测器
def check_re_register_detector(request):
    detector_id = common.get_detector_id(request)  # 获取检测器ID
    if isinstance(detector_id, Response):
        return detector_id  # 返回响应信息

    detector_info = Detector.objects.filter(device_id=detector_id)  # 查询是否注册
    if not detector_info.exists():
        return common.detector_message_response(200, '检测器没有提交过注册请求', {'message': '检测器从未注册过'},
                                                status.HTTP_200_OK)

    if detector_id in request.session:  # 若存在则删除session
        del request.session[detector_id]

    if detector_info.exists() and not detector_info[0].is_effective:
        return common.detector_message_response(403, '该检测器已禁用', '服务器禁用了该检测器',
                                                status.HTTP_403_FORBIDDEN)
    return detector_info


# 重新注册处理
def re_register(request):
    try:
        re_register_time = du.get_current_time()  # 获取当前时间
        # request_data = common.print_header_data(request)  # 获取请求数据
        request_data = json.loads(request.body)
        print 'reregister_data:', request_data

        detector_info = check_re_register_detector(request)
        if isinstance(detector_info, Response):
            return detector_info

        data = dc.check_dict_data(request_data)
        if isinstance(data, Response):
            return data

        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_info[0].device_id if detector_info.exists() else 'unknown', 're_register', 0 if not data else 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        data_dict = {
            'device_type': data.get('device_type'),
            'soft_version': data.get('soft_version'),
            'interface': json.dumps(data.get('interface')),
            'mem_total': data.get('mem_total'),
            'cpu_info': json.dumps(data.get('cpu_info')),
            'disk_info': json.dumps(data.get('disk_info')),
            'organs': data.get('organs'),
            'device_ca': data.get('device_ca'),
            'address': data.get('address'),
            'address_code': data.get('address_code'),
            'contact': json.dumps(data.get('contact', '[]'), encoding='utf-8', ensure_ascii=False),
            'memo': data.get('memo'),
            'register_time': re_register_time,
            'register_frequency': F('register_frequency') + 1,
            'register_status': common.DETECTOR_STATUS['register_no_check'],
            'auth_frequency': 0,
            'auth_status': 2,  # (0: 认证成功 1: 认证失败 2: 未认证)
            'register_fail_reason': '',
            'op_person': '',
            'op_ip': '',
            'op_time': None,
            'device_status': common.DETECTOR_STATUS['register_no_check'],
        }

        detector_info.update(**data_dict)  # 修改数据库

        process_auto_audit(data_dict, detector_info[0].device_id)

        return common.detector_message_response(200, '重新注册请求提交成功',
                                                {'message': '重新注册请求发送成功，等待人工审核'}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 注册状态查询处理
def get_register_status(request):
    try:
        common.print_header_data(request)  # 获取请求数据
        detector_id = common.get_detector_id(request)  # 获取检测器ID
        if not isinstance(detector_id, basestring):
            return detector_id  # 返回响应信息

        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 're_register', 0)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        detector_info = Detector.objects.filter(device_id=detector_id)  # 查询是否注册
        if detector_info.exists():
            if not detector_info[0].is_effective:
                return common.detector_message_response(403, '该检测器已禁用', '服务器禁用了该检测器',
                                                        status.HTTP_403_FORBIDDEN)

            reg_status = detector_info[0].register_status  # 注册状态

            if reg_status == 0:  # 注册成功，修改设备状态为注册成功
                reg_fail_reason = '成功'
            elif reg_status == 1:  # 注册失败，修改设备状态为注册失败
                reg_fail_reason = detector_info[0].register_fail_reason.encode('utf-8')  # 注册失败原因
            else:
                reg_fail_reason = '审核中'

            return common.detector_message_response(reg_status, reg_fail_reason,
                                                    {'type': reg_status, 'message': reg_fail_reason},
                                                    status.HTTP_200_OK)
        else:  # 没有提交注册请求
            return common.detector_message_response(200, '检测器没有提交过注册请求', {'type': 1, 'message': '检测器从未注册过'},
                                                    status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_reset_task(is_first_auth, rule_model, detector_id, d_id=0):

    i = rule_models.index(rule_model) + 1

    result_set = get_rule_fields(i)
    if is_first_auth:
        director_rule_data = director_rule_models[i-1].objects.filter(is_del=1)
        rule_data = rule_model.objects.filter(is_del=1)
    else:
        director_rule_data = director_rule_models[i-1].objects.filter(
            Q(device_id_list_run__contains='#' + str(detector_id) + '#') |
            Q(device_id_list_run='#'), is_del=1)
        rule_data = rule_model.objects.filter(
            Q(device_id_list_run__contains='#' + str(detector_id) + '#') |
            Q(device_id_list_run='#'), is_del=1)
    if not rule_data.exists() and not director_rule_data.exists():  # 该模块没有策略
        rule_data = None
        director_rule_data = None
        task_data = {}
    else:
        director_rule_json = serialize('json', director_rule_data, fields=result_set)
        director_rule_all = json.loads(director_rule_json)
        director_config_list = [data['fields'] for data in director_rule_all] if director_rule_all else []

        rule_json = serialize('json', rule_data, fields=result_set)  # 序列化成json
        rule_all = json.loads(rule_json)
        config_list = [data['fields'] for data in rule_all] if rule_all else []  # config
        config_list.extend(director_config_list)

        if i in [4, 6, 7, 8, 13, 14]:
            config_list = [config_list[-1]]

        if i == 2:  # 漏洞利用规则，修改数字为对应的攻击类型
            for config in config_list:
                config['attack_type'] = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw'
                                         ][config['attack_type'] - 1]
        elif i in [6, 8]:  # 加密规则或图片规则，修改config的组织方式
            for config in config_list:
                config['filesize'] = {"minsize": config.pop('filesize_minsize'),
                                      "maxsize": config.pop('filesize_maxsize')}
        elif i == 7:  # 压缩规则，修改config的组织方式
            for config in config_list:
                config['filesize'] = {"backsize": config.pop('backsize'),
                                      "dropsize": config.pop('dropsize')}

        version_num = common.cal_task_version([Task, DirectorTask], detector_id, 'policy', '1')
        task_data = {
            'module': i,
            'version': version_num,
            'cmd': 'reset',
            'num': len(config_list),
            'config': json.dumps(config_list, encoding='utf-8', ensure_ascii=False),
            'generate_time': du.get_current_time(),
            'device_id': detector_id,
            'user': '检测器认证' if not is_first_auth else '检测器首次认证'
        }
    return rule_data, director_rule_data, task_data


# 认证处理
def auth_login(request):
    try:
        auth_time = du.get_current_time()  # 获取当前时间
        # request_data = common.print_header_data(request)  # 获取请求数据
        request_data = json.loads(request.body)
        print 'auth_data:', request_data

        detector_id = common.get_detector_id(request)  # 获取检测器ID
        if not isinstance(detector_id, basestring):
            # return detector_id
            return common.detector_message_response(1, '检测器ID不合法', {'type': 1, 'message': '检测器ID不合法'}, status.HTTP_200_OK)

        print 'Detector_id', detector_id

        data = dc.check_dict_data(request_data, '认证信息')
        if isinstance(data, Response):
            # return data
            return common.detector_message_response(1, '认证信息数据不是dict类型', {'type': 1, 'message': '认证信息与注册信息不符'}, status.HTTP_200_OK)

        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'auth_login', 0 if not data else 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        detector_info = Detector.objects.filter(device_id=detector_id)  # 查询是否注册
        if detector_info.exists():
            if not detector_info[0].is_effective:
                # return common.detector_message_response(403, '该检测器已禁用', '服务器禁用了该检测器', status.HTTP_403_FORBIDDEN)
                return common.detector_message_response(1, '该检测器已禁用', {'type': 1, 'message': '检测器已禁用'},
                                                        status.HTTP_200_OK)
            # 不是注册未审核，也不是注册失败，即注册成功
            if detector_info[0].device_status not in \
                    [common.DETECTOR_STATUS['register_no_check'], common.DETECTOR_STATUS['register_fail']]:
                # 比较注册提交的数据与认证提交的数据是否一致
                if not is_list_ele_equal(json.loads(detector_info[0].interface), data['interface']) or \
                        not is_list_ele_equal(json.loads(detector_info[0].cpu_info), data['cpu_info']) or \
                        not is_list_ele_equal(json.loads(detector_info[0].disk_info), data['disk_info']) or \
                        detector_info[0].mem_total != data['mem_total']:

                    auth_status = 1
                    auth_result = '认证信息与注册信息不符'
                    data_dict = {
                        'soft_version': data.get('soft_version', 'unknown'),
                        'auth_time': auth_time,
                        'auth_frequency': F('auth_frequency') + 1,
                        'auth_status': auth_status,
                        'auth_fail_reason': auth_result,
                        'device_status': common.DETECTOR_STATUS['auth_fail']  # 修改设备状态为认证失败
                    }
                    detector_info.update(**data_dict)  # 更新数据
                    return common.detector_message_response(auth_status, auth_result,
                                                            {'type': auth_status, 'message': auth_result},
                                                            status.HTTP_200_OK)
                else:

                    if detector_id in request.session:  # 通过session验证检测器是否认证
                        # return common.detector_message_response(403, '检测器已认证', '检测器已认证', status.HTTP_403_FORBIDDEN)
                        return common.detector_message_response(0, '检测器已认证', {'type': 0, 'message': '认证成功'},
                                                                status.HTTP_200_OK)
                    else:
                        # 设置Session
                        session_value = detector_id + '_' + auth_time.strftime('%Y-%m-%d %H:%M:%S')
                        request.session[detector_id] = session_value
                        # common.RESPONSE_HEADER['Set-Cookie'] = request.session[detector_id]  # 设置Cookie

                    auth_status = 0
                    auth_result = '认证成功'
                    data_dict = {
                        # 'interface': json.dumps(data['interface']),
                        # 'mem_total': data['mem_total'],
                        # 'cpu_info': json.dumps(data['cpu_info']),
                        # 'disk_info': json.dumps(data['disk_info']),
                        'auth_time': auth_time,
                        'auth_frequency': F('auth_frequency') + 1,
                        'auth_status': auth_status,
                        'auth_fail_reason': auth_result,
                        'is_online': 1,
                        'device_status': common.DETECTOR_STATUS['normal'],  # 修改设备状态为正常运行(认证成功)
                        'heartbeat_time': du.get_current_time()
                    }
                    from judge_online import record_online_event
                    record_online_event(device_id=detector_id)
                    detector_info.update(**data_dict)  # 更新数据

                    if detector_info[0].auth_frequency == 1 and config.const.UPLOAD_DIRECTOR and check_global_director_connection():  # 第一次认证
                        data = serialize('json', detector_info,
                                         fields=('device_id', 'soft_version', 'device_ca', 'organs', 'address', 'address_code',
                                                    'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info', 'register_time', 'auth_time'))  # 序列化
                        list_data = json.loads(data)
                        fields = list_data[0]['fields']

                        fields['cpu_info'] = json.loads(fields['cpu_info'])
                        fields['disk_info'] = json.loads(fields['disk_info'])
                        fields['interface'] = json.loads(fields['interface'])
                        fields['contact'] = json.loads(fields['contact'])

                        fields['register_time'] = fields['register_time'].replace('T', ' ')
                        fields['access_time'] = fields.pop('auth_time').replace('T', ' ')
                        command_data = json.dumps(fields, ensure_ascii=False).encode('utf-8')
                        common_header = ccd.get_common_command_header_of_center('JCQ_STATUS', 'JCQ_STATUS_INFO')
                        ccd.upload_json_2_director_of_center(common_header, 'JCQ_STATUS_INFO', command_data,
                                                             async_level=3)

                    # 全量下发策略（检测器重新认证时（断电重连）下发该检测器重新认证前的规则组成新的策略）
                    task_list = []  # 任务

                    print 'auth_frequency:', detector_info[0].auth_frequency

                    # 将以前的策略任务作废
                    Task.objects.filter(device_id=detector_id, is_valid=1).update(is_valid=0)
                    # DirectorTask.objects.filter(device_id=detector_id, is_valid=1).update(is_valid=0)
                    # 重新生成全量的策略
                    update_type = {}
                    for rule_model in rule_models:
                        rule_data, director_rule_data, task_data = get_reset_task(False, rule_model, detector_id,
                                                                                  detector_info[0].id)
                        if task_data:
                            task_list.append(task_data)
                            rule_data.update(rule_status=0, operate_time=auth_time)
                            director_rule_data.update(rule_status=0)

                    if task_list:
                        serializer_task = TaskSerializer(data=task_list, many=True)  # 序列化task数据
                        if serializer_task.is_valid():
                            serializer_task.save()  # 存储数据库task表
                        # else:
                        #     return common.ui_message_response(400, json.dumps(serializer_task.errors),
                        #                                       'task数据缺失或字段不符合规定，序列化出错')

                    print 'task_list------', task_list
                    return common.detector_message_response(auth_status, auth_result,
                                                            {'type': auth_status, 'message': auth_result},
                                                            status.HTTP_200_OK, headers={"Server": "IIE CAS",
                                                                                         'Set-Cookie': request.session[
                                                                                             detector_id]})
            else:
                # return common.detector_message_response(1, '注册未审核或注册失败，需先进行人工审核', {'type': 1, 'message': '注册未审核或注册失败，需先进行人工审核'}, status.HTTP_200_OK)
                return common.detector_message_response(1, '注册未审核或注册失败，需先进行人工审核', {'type': 1, 'message': '检测器审核中'}, status.HTTP_200_OK)
        else:
            return common.detector_message_response(1, '检测器没有提交过注册请求',
                                                    {'type': 1, 'message': '检测器未注册'},
                                                    status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 业务状态处理
def process_business_status(request):
    try:
        report_time = du.get_current_time()  # 获取当前时间

        detector_id = common.check_detector_available(request, Detector)
        if isinstance(detector_id, Response):
            return detector_id

        request_data = common.print_header_data(request)  # 获取请求数据

        data = dc.check_dict_data(request_data, '业务状态')
        if isinstance(data, Response):
            return data

        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'detector_business_status', 0 if not data else 1)
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        handle_data = copy.deepcopy(data)   # 生成业务处置系统所需文件的告警数据
        # 生成业务处置系统所需文件
        if config.const.UPLOAD_BUSINESS_DISPOSAL:
            handle_data_type = 'business_status'
            file_dir = os.path.join(config.const.DISPOSAL_DIR, 'status')
            file_name = 'business_status_' + str(int(time.time())) + '_' + str(1)
            sender.send_business_disposal(file_dir, file_name, request.META.get('HTTP_USER_AGENT'), handle_data_type, handle_data)

        data['module_status'].append({
            "status": "on",
            "submodule": [
                {
                    "status": "on",
                    "version": {
                        "ip_whitelist": ""
                    },
                    "name": "ip_whitelist"
                }
            ],
            "name": "ip_whitelist",
        })

        if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
            command_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            common_header = ccd.get_common_command_header_of_detector('status', 'STATUS_JCQ', 'JCQ_STATUS_BUSINESS',
                                                                      request, detector_id,
                                                                      datetime.datetime.strptime(data['time'],
                                                                                                 '%Y-%m-%d %H:%M:%S'),
                                                                      data_type='msg')
            ccd.upload_json_2_director_of_detector(common_header, {'device_id': detector_id}, command_data,
                                                   'JCQ_STATUS_BUSINESS', async_level=2)

        # 业务状态数据
        business_data = {
            'uptime': data.get('uptime', 0),
            'soft_version': data.get('soft_version', 'unknown'),
            'time': data.get('time', '0000-00-00 00:00:00'),
            'report_time': report_time,
            'device_id': detector_id
        }
        # 网卡连通性数据
        network_card_data = dc.fill_business_data_by_field('interface', data, detector_id, report_time)
        if isinstance(network_card_data, Response):
            return network_card_data

        # 系统工作异常状态数据
        suspected_data = dc.fill_business_data_by_field('suspected', data, detector_id, report_time)
        if isinstance(suspected_data, Response):
            return suspected_data

        # 模块状态数据
        update_module_data = {'soft_version': data.get('soft_version', 'unknown')}
        update_module_version = {}  # 模块版本号（key是模块名，value是该模块版本号）
        if 'module_status' in data:
            module_data = data['module_status']
            # module_list = []
            # sub_module_list = []
            for item in module_data:
                if item['name'] == 'ip_whitelist':  # ip白名单
                    update_module_data['ip_whitelist_version'] = item['submodule'][0]['version']['ip_whitelist']
                    update_module_version['ip_whitelist'] = item['submodule'][0]['version']['ip_whitelist']
                else:
                    update_module_data[item['name'] + '_status'] = item['status']  # 模块状态字段
                    sub_module = item['submodule']
                    for sub_item in sub_module:
                        update_module_data[sub_item['name'] + '_status'] = sub_item['status']  # 子模块状态字段
                        for k, v in sub_item['version'].iteritems():
                            update_module_data[k + '_version'] = v  # 子模块版本号字段
                            update_module_version[k] = v
                        # update_module_data[sub_item['name'] + '_warninfo'] = json.dumps(sub_item['warninfo'])
        else:
            return common.detector_message_response(400, '请求数据缺少module_status参数',
                                                    '请求数据缺少module_status参数')

        # 模块状态数据
        module_data = dc.fill_business_data_by_field('module_status', data, detector_id, report_time)
        if isinstance(module_data, Response):
            return module_data
        for module in module_data:
            module['submodule'] = json.dumps(module['submodule'])

        # 插件状态数据
        plugin_data = dc.fill_business_data_by_field('plug_status', data, detector_id, report_time)
        if isinstance(plugin_data, Response):
            return plugin_data

        # 序列化（业务状态、网卡连通性、系统工作异常状态、插件状态）
        serializer_business = BusinessStatusSerializer(data=business_data)
        serializer_module = ModuleStatusSerializer(data=module_data, many=True)
        serializer_interface = NetworkCardStatusSerializer(data=network_card_data, many=True)
        serializer_suspected = SuspectedStatusSerializer(data=suspected_data, many=True)
        serializer_plugin = PluginStatusSerializer(data=plugin_data, many=True)

        serializer_list = [serializer_business, serializer_module, serializer_interface, serializer_suspected,
                           serializer_plugin]
        if not serializer_business.is_valid():
            serializer_flag = 0
        elif not serializer_module.is_valid():
            serializer_flag = 1
        elif not serializer_interface.is_valid():
            serializer_flag = 2
        elif not serializer_suspected.is_valid():
            serializer_flag = 3
        elif not serializer_plugin.is_valid():
            serializer_flag = 4
        else:
            serializer_flag = 5

        if serializer_flag == 5:  # 全部序列化成功
            serializer_business.save()
            serializer_module.save()
            serializer_interface.save()
            serializer_suspected.save()
            serializer_plugin.save()
            # 更新detector_info表中的模块状态、版本号
            Detector.objects.filter(device_id=detector_id).update(**update_module_data)

            # # 修改task表中的is_success,is_valid;修改detector_info表中的各模块type
            # for k, v in update_module_version.iteritems():
            #     module_number = common.module_names.index(k)
            #     task = Task.objects.filter(module=module_number + 1, device_id=detector_id)
            #     running_task = task.filter(is_valid=2)  # 某一模块正在运行的任务只有一条
            #     # 表示策略执行成功
            #     # if running_task.exists() and running_task.count() == 1 and v == running_task[0].version:
            #     if running_task.exists() and running_task.count() == 1:
            #         running_task.update(is_valid=0, is_success=True, success_time=du.get_current_time())
            #         have_task = task.filter(is_valid=1)  # 还有未执行的任务
            #         if have_task.exists():
            #             type_field = {common.module_fields[module_number]: 1}
            #             Detector.objects.filter(device_id=detector_id).update(**type_field)
            # Task.objects.filter(is_valid=2, device_id=detector_id).update(
            #     is_valid=0, is_success=True, success_time=du.get_current_time())
            # have_task = Task.objects.filter(is_valid=1, device_id=detector_id)
            # module_number_list = []
            # type_field = {}
            # if have_task.exists():
            #     for task in have_task:
            #         if task.module not in module_number_list:
            #             module_number_list.append(task.module)
            #             type_field[common.module_fields[task.module - 1]] = 1
            # Detector.objects.filter(device_id=detector_id).update(**type_field)

            return common.detector_message_response(200, '业务状态上传成功', {'message': 'success'},
                                                    status.HTTP_200_OK)
        else:
            return common.detector_message_response(400, json.dumps(serializer_list[serializer_flag].errors),
                                                    '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 系统运行状态处理
def process_system_status(request):
    try:
        report_time = du.get_current_time()  # 获取当前时间

        detector_id = common.check_detector_available(request, Detector)
        if isinstance(detector_id, Response):
            return detector_id
        request_data = common.print_header_data(request)  # 获取请求数据

        status_data = []
        if isinstance(request_data, dict):  # 判断请求数据类型是否合规
            status_data.append(request_data.copy())
        elif isinstance(request_data, list):
            status_data = request_data
        else:
            return common.detector_message_response(400, '运行状态数据不是正确的JSON类型', '运行状态数据不是正确的JSON类型')

        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'detector_system_status', len(status_data))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
            device_info = Detector.objects.filter(device_id=detector_id)
            is_online = device_info[0].is_online if device_info.exists() else 0
            for data in status_data:
                data['is_online'] = is_online
            command_data = json.dumps(status_data, ensure_ascii=False).encode('utf-8')
            common_header = ccd.get_common_command_header_of_detector('status', 'STATUS_JCQ', 'JCQ_STATUS_SYSTEM', request,
                                                                      detector_id,
                                                                      datetime.datetime.strptime(status_data[0]['time'],
                                                                                                 '%Y-%m-%d %H:%M:%S'),
                                                                      data_type='msg')
            ccd.upload_json_2_director_of_detector(common_header, {'device_id': detector_id}, command_data,
                                                   'JCQ_STATUS_SYSTEM', async_level=1)

        handle_data = copy.deepcopy(status_data)  # 生成业务处置系统所需文件的告警数据

        # 生成业务处置系统所需文件
        # common.generate_business_meta('detector_status', request.META.get('HTTP_USER_AGENT'), 'status(system)', handle_data)
        if config.const.UPLOAD_BUSINESS_DISPOSAL:
            handle_data_type = 'detector_status'
            file_dir = os.path.join(config.const.DISPOSAL_DIR, 'status')
            file_name = 'detector_status_' + str(int(time.time())) + '_' + str(1)
            sender.send_business_disposal(file_dir, file_name, request.META.get('HTTP_USER_AGENT'), handle_data_type,
                                          handle_data)

        for data in status_data:
            data['cpu'] = json.dumps(data.setdefault('cpu', []))
            result = common.check_time_field(data)
            if isinstance(request, Response):
                return result

            data['plug_stat'] = json.dumps(data.setdefault('plug_stat', []))

            data['device_id'] = detector_id
            data['report_time'] = report_time

        serializer = SystemRunningStatusSerializer(data=status_data, many=True)  # 序列化
        if serializer.is_valid():
            serializer.save()  # 存储数据库
            return common.detector_message_response(200, '数据存储成功', {'message': 'success'}, status.HTTP_200_OK)

        return common.detector_message_response(400, json.dumps(serializer.errors),
                                                '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 通过检测器运行状态上传接口定时上报检测器在线状态
def center_report_detector_running_status(device_id=None):
    try:
        if not (config.const.UPLOAD_DIRECTOR and check_global_director_connection()):
            return
        if device_id is None:
            device_info = Detector.objects.filter()
        else:
            device_info = Detector.objects.filter(device_id=device_id)
        if device_info.exists():
            for device in device_info:
                run_status_info = SystemRunningStatus.objects.filter(device_id=device.device_id).order_by('-id')[0: 1]
                if run_status_info.exists():
                    serialize_data = serialize('json', run_status_info,
                                               fields=('cpu', 'mem', 'disk', 'time', 'plug_stat', 'did'))
                    data_list = json.loads(serialize_data)
                    run_data = data_list[0]['fields']
                    run_data['cpu'] = json.loads(run_data['cpu'])
                    run_data['plug_stat'] = json.loads(run_data['plug_stat'])
                    run_data['time'] = run_data['time'].replace('T', ' ')
                else:
                    run_data = {'device_id': device.device_id, 'cpu': [], 'mem': 0, 'disk': 0,
                                'time': du.get_current_date_string(), 'plug_stat': []}
                run_data['is_online'] = device.is_online

                command_data = json.dumps(run_data, ensure_ascii=False).encode('utf-8')
                common_header = {
                    'Channel-Type': 'JCQ',
                    'Msg-Type': 'status',
                    'Source-Type': 'STATUS_JCQ',
                    'BusinessData-Type': 'JCQ_STATUS_SYSTEM',
                    'Data-Type': 'msg',
                    'Task-Type': '',
                    'Src-Node': director_config.SRC_NODE,  # 源地区，用于指名产生告警的地区，管理中心的上级指挥节点
                    'Src-Center': director_config.SRC_CENTER_ID,  # 用于指名产生告警的控制节点或设备，一般指检测器管理中心编号
                    'User-Agent': device.device_id + '/' + device.soft_version + '(iie)',
                    'Capture-Date': datetime.datetime.strptime(run_data['time'],
                                                               '%Y-%m-%d %H:%M:%S').strftime('%a, %d %b %Y %H:%M:%S'),
                    'Content-Type': 'application/json',
                    'version': '1.0',
                    # 'Cookie': 'unknown',
                    'X-Forwarded-For': director_config.detect_center_host,
                    'Src-Device': device.device_id
                }
                ccd.upload_json_2_director_of_detector(common_header, {'device_id': device.device_id}, command_data,
                                                       'JCQ_STATUS_SYSTEM', async_level=1)
    except:
        traceback.print_exc()


# **************************************** 处理界面请求 ****************************************


# 构造检测器页面查询条件，用于显示列表信息和总数
def get_detector_query_terms(request_data):
    # 获取请求参数
    device_id = request_data.get('device_id')  # 检测器ID
    contractor = request_data.get('contractor')  # 厂商
    address_code = request_data.get('address_code')  # 检测器行政区域编码类型
    organs = request_data.get('organs')  # 检测器部署的客户单位
    device_status = request_data.get('device_status')  # 设备状态，见common中的DETECTOR_STATUS
    start_module = request_data.get('start_module')  # 正在运行的模块类型
    stop_module = request_data.get('stop_module')  # 已经停止的模块类型
    is_effective = request_data.get('device_is_effective')  # 检测器是否禁用
    register_time = request_data.get('time')  # 检测器注册时间
    is_online = request_data.get('is_online')  # 设备是否在线
    # 变更规则生效的检测器范围的参数
    device_id_list = request_data.get('id')  # 检测器对应的主键id列表

    # 插件生效的检测器范围的参数
    device_id_list_2 = request_data.get('device_ids')  # 检测器对应的id列表

    # 构造查询参数
    query_terms = {}

    if device_id is not None:
        query_terms['device_id__contains'] = device_id  # 检测器ID模糊查询
    if contractor is not None:
        query_terms['contractor'] = contractor
    if address_code is not None:
        query_terms['address_code'] = address_code
    if organs is not None:
        query_terms['organs__contains'] = organs  # 模糊查询
    if device_status is not None:
        if device_status == str(common.DETECTOR_STATUS['forbidden']):
            query_terms['is_effective'] = 0
        else:
            query_terms['device_status'] = device_status
    if start_module is not None:
        start_module = int(start_module)
        query_terms[common.module_status[start_module - 1]] = 'on'
    if stop_module is not None:
        stop_module = int(stop_module)
        query_terms[common.module_status[stop_module - 1]] = 'off'
    if device_id_list is not None:
        query_terms['id__in'] = json.loads(device_id_list)
    if device_id_list_2 is not None:
        query_terms['device_id__in'] = json.loads(device_id_list_2)
    if is_effective is not None:
        query_terms['is_effective'] = is_effective
    if register_time is not None:
        query_terms['register_time__gte'] = datetime.datetime.strptime(register_time, '%Y-%m-%d')
        query_terms['register_time__lt'] = datetime.datetime.strptime(register_time, '%Y-%m-%d') + datetime.timedelta(1)
    if is_online is not None:
        query_terms['is_online'] = is_online
    print query_terms
    return query_terms


# 查询所有检测器信息
def show_all_detectors(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_detector_query_terms(request_data)  # 获取查询条件

        query_data = Detector.objects.filter(**query_terms)[start_pos:end_pos]  # 过滤查询，若query_terms={}，相当于all
        serializer_data = serialize('json', query_data,
                                    fields=(
                                    'device_id', 'soft_version', 'device_ca', 'contractor', 'address_code', 'organs',
                                    'register_time',
                                    'device_status', 'last_warning_time', 'is_effective', 'is_online',
                                    'register_fail_reason', 'auth_fail_reason', 'auth_frequency')
                                    )  # 序列化
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            if fields['last_warning_time'] is not None:
                fields['last_warning_time'] = fields['last_warning_time'].replace('T', ' ')
            else:
                fields['last_warning_time'] = '0000-00-00 00:00:00'
            if fields['register_time'] is not None:
                fields['register_time'] = fields['register_time'].replace('T', ' ')
            is_effective = fields.pop('is_effective')
            fields['device_is_effective'] = 1 if is_effective else 0
            fields['contractor'] = fields['contractor']
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询检测器数量
def show_detectors_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_terms = get_detector_query_terms(request_data)  # 获取查询条件

        count = Detector.objects.filter(**query_terms).count()  # 过滤查询（数据条数），若query_terms={}，相当于all
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询某个检测器的详细情况
def show_detector_detail(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        query_id = common.check_request_int_field(request_data, 'id')  # 获取请求参数id
        if isinstance(query_id, Response):
            return query_id

        detector = Detector.objects.filter(id=query_id)  # 提取出某个检测器的基本信息
        if not detector.exists():
            return common.ui_message_response(400, '数据库中不存在此id', '请求参数id不正确')

        serializer_data = serialize('json', detector)
        list_data = json.loads(serializer_data)
        show_data = list_data[0]['fields']
        show_data['id'] = list_data[0]['pk']  # 加入主键id

        if 'register_fail_reason' in show_data:  # 修改显示字段
            show_data['register_message'] = show_data.pop('register_fail_reason')
        if 'auth_fail_reason' in show_data:
            show_data['message'] = show_data.pop('auth_fail_reason')

        # 去除因序列化时间类型出现的'T'
        if show_data['register_time'] is not None:
            show_data['register_time'] = show_data['register_time'].replace('T', ' ')
        if show_data['op_time'] is not None:
            show_data['op_time'] = show_data['op_time'].replace('T', ' ')
        if show_data['auth_time'] is not None:
            show_data['auth_time'] = show_data['auth_time'].replace('T', ' ')
        if show_data['last_warning_time'] is not None:
            show_data['last_warning_time'] = show_data['last_warning_time'].replace('T', ' ')
        else:
            show_data['last_warning_time'] = '0000-00-00 00:00:00'

        # 将json字符串转为list
        show_data['contact'] = json.loads(show_data['contact']) if show_data['contact'] != '' else []
        show_data['disk_info'] = json.loads(show_data['disk_info']) if show_data['disk_info'] != '' else []
        show_data['cpu_info'] = json.loads(show_data['cpu_info']) if show_data['cpu_info'] != '' else []
        show_data['interface'] = json.loads(show_data['interface']) if show_data['interface'] != '' else []

        # 提取出检测器的设备状态信息
        device_status = NetworkCardStatus.objects.filter(device_id=show_data['device_id'])
        if not device_status.exists():
            show_data['networkcard'] = []
        else:
            device_status = device_status.filter(report_time=device_status.last().report_time)  # 查询最后一次状态
            serializer_data = serialize('json', device_status,
                                        fields=('interface_seq', 'interface_flag', 'interface_stat',
                                                'interface_flow', 'interface_error', 'interface_drop',
                                                'duration_time')
                                        )
            list_data = json.loads(serializer_data)
            show_data['networkcard'] = [data['fields'] for data in list_data]

        # 提取出检测器的异常状态信息
        abnormal_status = SuspectedStatus.objects.filter(device_id=show_data['device_id'])
        if not abnormal_status.exists():
            show_data['suspected_status'] = []
        else:
            abnormal_status = abnormal_status.filter(report_time=abnormal_status.last().report_time)  # 查询最后一次状态
            abnormal_list = []
            for data in abnormal_status:
                abnormal_list.append({
                    'event_type': data.get_event_type_display(),
                    'time': data.time.strftime('%Y-%m-%d %H:%M:%S'),
                    'risk': data.risk,
                    'msg': data.msg
                })
            show_data['suspected_status'] = abnormal_list

        # 提取出检测器的插件状态信息
        plug_status = PluginStatus.objects.filter(device_id=show_data['device_id'])
        if not plug_status.exists():
            show_data['plug_status'] = []
        else:
            plug_status = plug_status.filter(report_time=plug_status.last().report_time)  # 查询最后一次状态
            serializer_data = serialize('json', plug_status,
                                        fields=('plug_id', 'status', 'plug_version', 'plug_policy_version'))
            list_data = json.loads(serializer_data)
            show_data['plug_status'] = [data['fields'] for data in list_data]

        # 提取出检测器的运行资源状态信息
        resource_status = SystemRunningStatus.objects.filter(device_id=show_data['device_id'])
        if not resource_status.exists():
            show_data['run_resource'] = {}
        else:
            resource_status = resource_status.filter(report_time=resource_status.last().report_time)  # 查询最后一次状态
            serializer_data = serialize('json', resource_status,
                                        fields=('cpu', 'mem', 'disk', 'time', 'plug_stat'))
            list_data = json.loads(serializer_data)
            resource_data = list_data[0]['fields']
            resource_data['cpu'] = json.loads(resource_data['cpu'])
            resource_data['plug_stat'] = json.loads(resource_data['plug_stat'])
            if resource_data['time'] is not None:
                resource_data['time'] = resource_data['time'].replace('T', ' ')
            show_data['run_resource'] = resource_data

        # 统计告警总数和各大类告警总数
        alarms_dict = {}
        alarm_data = AlarmAll.objects.filter(device_id=detector[0].device_id)
        alarms_dict['all'] = alarm_data.count()
        alarms_dict['alarm'] = alarm_data.filter(warning_module=1).count()
        alarms_dict['abnormal'] = alarm_data.filter(warning_module=2).count()
        alarms_dict['sensitive'] = alarm_data.filter(warning_module=3).count()
        alarms_dict['object_listen'] = alarm_data.filter(warning_module=4).count()
        alarms_dict['block'] = alarm_data.filter(warning_module=5).count()
        alarms_dict['other'] = alarm_data.filter(Q(warning_module__lt=1) or Q(warning_module__gt=5)).count()
        show_data['alarm_count'] = alarms_dict

        # 统计下发策略
        rule_count = {}
        from policy.data_processing import rule_models
        total = 0
        for i in range(len(common.module_names)):
            count = rule_models[i].objects.filter(
                Q(device_id_list_run='#') | Q(device_id_list_run__contains='#' + str(detector[0].id) + '#')).count()
            total += count
            rule_count[common.module_names[i]] = count
        rule_count['all'] = total
        show_data['rule_count'] = rule_count

        # 统计下发插件
        from plugin.models import PluginDetector, PluginAlarm, PlugTask
        plug_count = PluginDetector.objects.filter(
            Q(device_id_list_run='#') | Q(device_id_list_run__contains='#' + str(detector[0].id) + '#')).count()
        plug_task = PlugTask.objects.filter(device_id=detector[0].device_id).order_by('-id')
        if plug_task.exists():
            time = plug_task[0].generate_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            time = '0000-00-00 00:00:00'
        plug_alarm = PluginAlarm.objects.filter(device_id=detector[0].device_id).count()
        show_data['plug'] = {'plug_count': plug_count, 'time': time, 'plug_alarm': plug_alarm}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 审核检测器
def check_detector(request):
    try:
        op_time = du.get_current_time()  # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        query_id = common.check_request_int_field(request_data, 'id')  # 获取请求参数id
        if isinstance(query_id, Response):
            return query_id

        check_type = request.data.get('type', '2')  # 审核状态（0：注册成功；1：注册失败；2：注册未审核）
        check_person = request.data.get('op_person', '')  # 审核人（此参数可能会由其他路径传入）
        check_message = request.data.get('register_message', '')  # 注册失败原因（注册成功，此处为空）

        detector = Detector.objects.filter(id=query_id)  # 提取出某个检测器的基本信息
        if not detector.exists():
            return common.ui_message_response(400, '数据库中不存在此id', '请求参数id不正确')

        # 审核状态（前者表示审核通过，后者表示审核未通过）
        check_status = [common.DETECTOR_STATUS['register_success'], common.DETECTOR_STATUS['register_fail'],
                        common.DETECTOR_STATUS['register_no_check']]
        detector.update(register_status=int(check_type), register_fail_reason=check_message, auth_status=2,
                        auth_fail_reason='#未认证#', auth_frequency=0,
                        op_person=check_person, op_ip=request.META.get('REMOTE_ADDR', ''), op_time=op_time,
                        device_status=check_status[int(check_type)])

        return common.ui_message_response(200, '注册审核数据更新成功', '注册已审核', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 修改检测器有效性（是否有效）
def update_detector_effective_status(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        query_id = request_data.get('id')  # 标志id
        is_effective = request_data.get('type')  # 是否有效（0表示无效，1表示有效）
        comment = request_data.get('comment')  # 备注禁用原因
        if query_id is not None and is_effective is not None:
            query_id = int(query_id)
            is_effective = True if is_effective == '1' else False
        else:
            return common.ui_message_response(400, '请求参数不完整', '参数不符合规定')
        Detector.objects.filter(id=query_id).update(is_effective=is_effective, comment=comment)  # 修改检测器是否有效

        return common.ui_message_response(200, '有效状态修改成功', '状态修改成功', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 生成excel sheet
def generate_sheet(workbook, sheet_name, data):
    worksheet = workbook.add_worksheet(sheet_name)
    bold_format = workbook.add_format({'bold': True})

    for col in xrange(len(data[0])):
        worksheet.set_column(0, col, 20)

    for row in xrange(len(data)):
        if row == 0:
            for col in xrange(len(data[0])):
                worksheet.write(row, col, data[row][col], bold_format)
        else:
            for col in xrange(len(data[0])):
                worksheet.write(row, col, data[row][col])


# 导出检测器统计报表
def export_detectors_report(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        # query_terms = get_detector_query_terms(request_data)     # 获取查询条件
        # query_data = Detector.objects.filter(**query_terms)      # 过滤查询，若query_terms={}，相当于all

        valid_detectors = Detector.objects.filter(is_effective=1)  # 有效的检测器
        invalid_detectors = Detector.objects.filter(is_effective=0)  # 无效的检测器

        valid_list = [
            [u'检测器编号', u'厂商', u'部署位置', u'部署单位', u'最近告警时间'],
        ]
        invalid_list = [
            [u'检测器编号', u'厂商', u'部署位置', u'部署单位', u'最近告警时间'],
        ]
        for detector in valid_detectors:
            if detector.last_warning_time is not None:
                warning_time = detector.last_warning_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                warning_time = ''
            valid_list.append([
                detector.device_id, detector.contractor, detector.address,
                detector.organs, warning_time
            ])
        for detector in invalid_detectors:
            if detector.last_warning_time is not None:
                warning_time = detector.last_warning_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                warning_time = ''
            invalid_list.append([
                detector.device_id, detector.contractor, detector.address,
                detector.organs, warning_time
            ])

        file_path = os.path.join(common.MEDIA_ROOT, 'statistics_report/')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = u'检测器统计报表.xlsx'
        relative_path = 'statistics_report/' + file_name
        file_path = os.path.join(file_path, file_name)
        workbook = xlsxwriter.Workbook(file_path)
        generate_sheet(workbook, u'有效检测器', valid_list)
        generate_sheet(workbook, u'无效检测器', invalid_list)
        workbook.close()

        return common.construct_download_file_header(file_path, relative_path, file_name)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 构造设备管理页面查询条件，用于显示列表信息和总数
def get_device_query_terms(request_data):
    # 获取请求参数
    device_id = request_data.get('device_id')  # 检测器ID
    device_ca = request_data.get('device_ca')  # CA序列号
    address = request_data.get('address')  # 部署位置
    organs = request_data.get('organs')  # 部署单位

    # 构造查询参数
    query_terms = {}

    if device_id is not None:
        query_terms['device_id__contains'] = device_id  # 检测器ID模糊查询
    if device_ca is not None:
        query_terms['device_ca__contains'] = device_ca  # CA序列号模糊查询
    if address is not None:
        query_terms['address__contains'] = address  # 部署位置模糊查询
    if organs is not None:
        query_terms['organs__contains'] = organs  # 部署单位模糊查询

    return query_terms


# 查询所有设备信息
def show_all_devices(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_device_query_terms(request_data)  # 获取查询条件

        # 过滤查询，若query_terms={}，相当于all
        query_data = DeviceInfo.objects.filter(**query_terms)[start_pos:end_pos]
        serializer_data = serialize('json', query_data,
                                    fields=('device_id', 'soft_version', 'contractor', 'device_ca', 'organs', 'address',
                                            'address_code')
                                    )  # 序列化
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            show_data.append(fields)

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询设备数量
def show_devices_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_terms = get_device_query_terms(request_data)  # 获取查询条件

        count = DeviceInfo.objects.filter(**query_terms).count()  # 过滤查询（数据条数），若query_terms={}，相当于all
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询设备详情
def show_device_detail(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        query = {}
        if request_data.get('id') is not None:
            query_id = common.check_request_int_field(request_data, 'id')  # 获取请求参数id
            if isinstance(query_id, Response):
                return query_id
            query['id'] = query_id

        detector_id = request_data.get('detector_id')
        if detector_id is not None:
            query['device_id'] = detector_id

        device = DeviceInfo.objects.filter(**query)  # 提取出某个设备的基本信息
        if not device.exists():
            return common.ui_message_response(400, '数据库中不存在此id或者detector_id', '请求参数id或detector_id不正确')

        serializer_data = serialize('json', device)
        list_data = json.loads(serializer_data)
        show_data = list_data[0]['fields']
        show_data['id'] = list_data[0]['pk']  # 加入主键id

        # 将json字符串转为list
        show_data['contact'] = json.loads(show_data['contact']) if show_data['contact'] != '' else []
        show_data['disk_info'] = json.loads(show_data['disk_info']) if show_data['disk_info'] != '' else []
        show_data['cpu_info'] = json.loads(show_data['cpu_info']) if show_data['cpu_info'] != '' else []
        show_data['interface'] = json.loads(show_data['interface']) if show_data['interface'] != '' else []

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 增加或修改设备信息
def add_update_device(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数
        data = common.check_request_list_or_dict_field(request_data, 'json')
        if isinstance(data, Response):
            return data

        interface = data['interface']
        for k, v in interface.iteritems():
            if k == 'manage':
                interface[k] = True if v == '1' else False

        operate_data = {
            'device_id': data['device_id'],
            'device_ca': data['device_ca'],
            'soft_version': data['soft_version'],
            'contractor': data['contractor'],
            'organs': data['organs'],
            'address': data['address'],
            'address_code': data['address_code'],
            'contact': json.dumps(data.get('contact', '[]')),
            'mem_total': data['mem_total'],
            'interface': json.dumps(interface),
            'cpu_info': json.dumps(data.get('cpu_info', '[]')),
            'disk_info': json.dumps(data.get('disk_info', '[]'))
        }

        if data['id'] == 0:  # 增加
            serializer = DeviceInfoSerializer(data=operate_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return common.ui_message_response(400, json.dumps(serializer.errors),
                                                  '数据缺失或字段不符合规定，序列化出错')
        else:  # 修改，data['id']表示主键id
            DeviceInfo.objects.filter(id=data['id']).update(**operate_data)

        return common.ui_message_response(200, '增加或修改成功', 'success', status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 导入设备信息文件
def import_device_file(request, sub_function_dir):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        file_path = request_data.get('param')  # 规则文件相对路径
        if file_path is None:
            return common.ui_message_response(400, '请求url中没有携带参数file_path', '请求参数没有file_path')
        file_path = common.MEDIA_ROOT + sub_function_dir + file_path
        if not os.path.exists(file_path):
            return common.ui_message_response(400, '服务器上没有该文件:' + file_path.encode('utf-8'),
                                              '备案文件不存在')

        device_header = [
            'device_id', 'soft_version', 'device_ca', 'organs', 'contractor', 'address', 'address_code',
            'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info'
        ]  # 设备需要录入的信息
        try:
            book = xlrd.open_workbook(file_path)
        except:
            return common.ui_message_response(400, '文件格式不是xls或xlsx格式', '文件格式不是xls或xlsx格式')
        sheet = book.sheet_by_index(0)
        first_row = sheet.row_values(0)
        if set(first_row) != set(device_header):
            return common.ui_message_response(400, '文件第一行内容不正确', '文件第一行内容不正确')
        rows_num = sheet.nrows
        cols_num = sheet.ncols
        device_list = []
        for i in xrange(1, rows_num):
            device_info = {}
            for j in range(cols_num):
                device_info[first_row[j]] = sheet.cell_value(i, j)
            print '************', device_info
            if device_info:
                device_list.append(device_info)
            else:
                return common.ui_message_response(400, '文件第%d行存在数据类型错误' % (i + 1,), '文件第%d行存在数据类型错误' % (i + 1,))

        exist_device = []
        for device in device_list:
            if DeviceInfo.objects.filter(device_id=device['device_id']).exists():
                exist_device.append(device)

        device_list = [item for item in device_list if item not in exist_device]

        if not device_list and not exist_device:
            return common.ui_message_response(400, '文件内容不符合规范, 未识别到检测器信息', '文件内容不符合规范, 未识别到检测器信息')

        serializer = DeviceInfoSerializer(data=device_list, many=True)

        for device in device_list:
            result = check_is_valid_json('contact', device)
            if isinstance(result, Response):
                return result

            result = check_is_valid_json('interface', device)
            if isinstance(result, Response):
                return result

            result = check_is_valid_json('cpu_info', device)
            if isinstance(result, Response):
                return result

            result = check_is_valid_json('disk_info', device)
            if isinstance(result, Response):
                return result

        if serializer.is_valid():
            serializer.save()  # 存储数据库
            if not exist_device:
                return common.ui_message_response(200, '成功导入{0}个检测器'.format(len(device_list)),
                                                  '成功导入{0}个检测器'.format(len(device_list)), status.HTTP_200_OK)
            else:
                return common.ui_message_response(200, '成功导入{0}个检测器'.format(
                    len(device_list)) + ' device_id重复{0}个检测器，分别为：{1}'.format(len(exist_device),
                                                                             [device['device_id'] for device in
                                                                              exist_device]),
                                                  '成功导入{0}个检测器'.format(
                                                      len(device_list)) + ' device_id重复{0}个检测器，分别为：{1}'.format(
                                                      len(exist_device),
                                                      [device['device_id'] for device in exist_device]),
                                                  status.HTTP_200_OK)
        return common.ui_message_response(400, json.dumps(serializer.errors), '数据缺失或字段不符合规定，序列化出错')

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def check_is_valid_json(field, data):
    try:
        json.loads(data[field])
    except:
        traceback.print_exc()
        return common.ui_message_response(400,  '导入的检测器%s中%s字段不是标准的json格式' % (data['device_id'], field), '导入的检测器%s中%s字段不是标准的json格式' % (data['device_id'], field))


# 下载导入文件模板
def download_template(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        file_name = 'detector_info.xlsx'
        relative_path = 'template/' + file_name
        file_path = common.MEDIA_ROOT + relative_path
        if not os.path.exists(file_path):
            return common.ui_message_response(400, '服务器上没有该文件:' + file_path.encode('utf-8'),
                                              '文件不存在')

        return common.construct_download_file_header(file_path, relative_path, file_name)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 统计检测器的接入状态运行情况
def statistics_detector_status(request):
    try:
        detector_status_map = {1: '认证成功', 2: '注册待审核', 3: '审核失败', 4: '审核成功', 5: '认证失败', 6: '禁用'}
        request_data = common.print_header_data(request)
        status_count = Detector.objects.all().values('device_status').annotate(
            amount=Count('device_status')).order_by('-amount')
        print status_count

        show_data = {v: 0 for k, v in detector_status_map.items()}

        name_count_status = {item['device_status']: item['amount'] for item in status_count}
        print 'show_data:', show_data, "name_count_status:", name_count_status
        for k in detector_status_map:
            if k in name_count_status:
                show_data[detector_status_map[k]] = name_count_status.pop(k)

        device_info = Detector.objects.all()
        if device_info.exists():
            for device in device_info:
                if not device.is_effective:
                    show_data[detector_status_map[device.device_status]] -= 1
                    show_data['禁用'] += 1

        show_data = [{'status': k, 'amount': v} for k, v in show_data.items()]

        return common.ui_message_response(200, '统计成功' + json.dumps(show_data), show_data, status.HTTP_200_OK)

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


# 构造设备在线状态事件页面查询条件，用于显示列表信息和总数
def get_device_online_event_query_terms(request_data):
    # 获取请求参数
    device_id = request_data.get('device_id')  # 检测器ID
    event = request_data.get('event')  # 事件
    time_min = request_data.get('time_min')
    time_max = request_data.get('time_max')

    # 构造查询参数
    query_terms = {}

    if device_id is not None:
        query_terms['device_id__contains'] = device_id  # 检测器ID模糊查询
    if event is not None:
        query_terms['event'] = event
    if time_min is not None:  # 生成任务的时间段筛选
        query_terms['time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        query_terms['time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

    return query_terms


# 查询所有事件
def show_all_devices_online_event(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_device_online_event_query_terms(request_data)  # 获取查询条件

        # 过滤查询，若query_terms={}，相当于all
        query_data = DetectorOnlineEvent.objects.filter(**query_terms).order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data,
                                    fields=('id', 'device_id', 'event', 'time'))  # 序列化
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            if fields['time'] is not None:
                fields['time'] = fields['time'].replace('T', ' ')
            show_data.append(fields)

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询事件数量
def show_devices_online_event_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_terms = get_device_online_event_query_terms(request_data)  # 获取查询条件

        count = DetectorOnlineEvent.objects.filter(**query_terms).count()  # 过滤查询（数据条数），若query_terms={}，相当于all
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 删除检测器信息
def detector_delete(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        delete_id_list = json.loads(request_data.get('id', []))

        tmp = []
        device_info = Detector.objects.filter(id__in=delete_id_list)
        if device_info.exists():
            for device in device_info:
                # if device.device_status == 2:
                tmp.append(device.device_id)
                device.delete()

        common.generate_system_log(request_data, u'检测器操作', u'删除检测器', u'成功删除:%s' % json.dumps(tmp))
        return common.ui_message_response(200, '成功删除:%s' % json.dumps(tmp), '成功删除:%s' % json.dumps(tmp),
                                          status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        common.generate_system_log(request_data, u'检测器操作', u'删除检测器', u'删除检测器:%s' % json.dumps(tmp) + u'异常')
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 删除检测器信息
def detector_info_delete(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        delete_id_list = json.loads(request_data.get('id', []))

        tmp = []
        device_info = DeviceInfo.objects.filter(id__in=delete_id_list)
        if device_info.exists():
            for device in device_info:
                tmp.append(device.device_id)
                device.delete()
        common.generate_system_log(request_data, u'检测器操作', u'删除检测器备案', u'成功删除:%s' % json.dumps(tmp))
        return common.ui_message_response(200, '成功删除:%s' % json.dumps(tmp), '成功删除:%s' % json.dumps(tmp),
                                          status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        common.generate_system_log(request_data, u'检测器操作', u'删除检测器备案', u'删除检测器备案:%s' % json.dumps(tmp) + u'异常')
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询检测器审核模式
def detector_audit_mode_show(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        mode_info = DetectorAuditMode.objects.all()
        if not mode_info.exists():
            DetectorAuditMode.objects.create(**{'id': 1, 'mode': 1})
            return common.ui_message_response(200, '查询成功', 1, status_code=status.HTTP_200_OK)
        else:
            return common.ui_message_response(200, '查询成功', mode_info[0].mode, status_code=status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 修改检测器审核模式
def detector_audit_mode_alert(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        mode = request_data.get('mode')

        DetectorAuditMode.objects.update(mode=mode)
        return common.ui_message_response(200, '修改成功', '修改成功', status_code=status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)
