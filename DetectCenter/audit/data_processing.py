# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.response import Response
from django.core.serializers import serialize
from requests_toolbelt import MultipartEncoder
from DetectCenter import common, snowflake, settings, tasks, date_util as du, file_util as fu, security_util as su
from detector.models import Detector
from audit_serializers import *

from DetectCenter import common_center_2_director as ccd

import os
import traceback
import requests
import gzip
import datetime
import json
import logging
import copy
import time
import shutil
from DetectCenter import config, sender
from DetectCenter.es_config import *
from DetectCenter.business_config import *
from director.models import ManagementCenterInfo
from director.detect_center_reg_auth import check_global_director_connection

# ************************************** 处理前端检测器请求 **************************************

# logger_record = logging.getLogger('project.record')


# 构造行为审计业务数据传输请求头
def construct_header(business_type, user_agent, file_desc):
    request_header = {
        'Host': business_host,
        'Date': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),
        # 'Content-Type': 'multipart/form-data;boundary=' + boundary,
        'version': '1.0',
        # 'Cookie': 'unknown',
        'Source-Type': 'JCQ_XWSJ',
        'Data-Type': 'file',
        'User-Agent': user_agent,
        'Capture-Date': datetime.datetime.strptime(file_desc['time'], '%Y-%m-%d %H:%M:%S').strftime(
            '%a, %d %b %Y %H:%M:%S'),
        'BusinessData-Type': business_type,
        'Meta-Data': json.dumps({
            'id': '',
            'from_id': '',
            'from_type': ''
        }),
        'Content-Filedesc': json.dumps({
            'filetype': file_desc['filetype'],
            'filename': file_desc['filename'],
            'checksum': file_desc['checksum'],
            'url': ''
        })
    }
    return request_header


# 接收通联关系压缩包，存入服务器，调用send_net_log函数上传数据
def process_communication_relation_upload(request, file_relative_path):
    try:
        # request_data = common.print_header_data(request)  # 获取请求数据
        # send_file = request.body
        request_id = snowflake.next_id(1, 0)  # 确定请求的全局唯一ID
        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'net_log', len(request.FILES)))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'net_log', len(request.FILES))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        file_desc = request.META.get('HTTP_CONTENT_FILEDESC')  # 请求头中的数据字段
        file_desc = common.check_detector_upload_header_filedesc_field(file_desc)  # 校验Content-Filedesc字段
        if isinstance(file_desc, Response):
            return file_desc

        print 'file_desc:', pu.pretty_print_format(file_desc)

        if len(request.FILES) == 1:  # 上传一个gzip压缩文件
            file_absolute_path = os.path.join(common.MEDIA_ROOT, file_relative_path)  # 绝对路径（没有文件名）
            request_file = request.FILES.values()[0]
            gzip_f = gzip.GzipFile(mode='rb', fileobj=request_file)
            try:
                gzip_f.readline()  # 尝试gzip读取文件，若无法读取则不是gzip格式文件
                request_file.seek(0)  # 将文件流重置偏移为文件开头
                gzip_f.close()  # 关闭文件流
            except IOError:
                gzip_f.close()  # 关闭文件流
                request_file.close()
                return common.detector_message_response(400, '不是一个gzip压缩文件',
                                                        request_file.name + ' not a gzipped file')

            file_name = request_file.name  # 原始文件名
            save_file_name = common.rename_detector_upload_file(detector_id, file_name)  # 存储文件名
            is_success = fu.handle_upload_file(file_absolute_path, request_file, save_file_name)  # 上传文件
            if is_success:  # 没有重名文件，上传成功
                request_file.close()  # 关闭文件流
                file_path = os.path.join(file_absolute_path, save_file_name)

                # 生成业务处置系统所需文件（原始文件）
                if config.const.UPLOAD_BUSINESS_DISPOSAL:
                    try:
                        # common.generate_business_file('net_log', file_path, detector_id + '_' + str(int(time.time())) + '_' + str(1) + '.gz')
                        if not os.path.exists(config.const.DISPOSAL_DIR + 'net_log/'):
                            os.makedirs(config.const.DISPOSAL_DIR + 'net_log/')
                        shutil.copy(file_path, config.const.DISPOSAL_DIR + 'net_log/' + detector_id + '_' + file_desc['checksum'])
                        # pass
                    except:
                        traceback.print_exc()

                save_data = {
                    'log_type': 1,
                    'request_id': request_id,
                    'time': datetime.datetime.strptime(file_desc['time'], '%Y-%m-%d %H:%M:%S'),
                    'filename': file_desc['filename'],
                    'checksum': file_desc['checksum'],
                    'filetype': file_desc['filetype'],
                    'save_path': file_relative_path + save_file_name,
                    'receive_time': du.get_current_time(),
                    'device_id': detector_id
                }
                serializer = AuditLogSerializer(data=save_data)
                if serializer.is_valid():
                    serializer.save()  # 存储数据库

                    if config.const.UPLOAD_ES:
                        sender.async_send_es_net_log(request_id, CR_URL, file_path, detector_id)

                    if config.const.UPLOAD_BUSINESS:
                        user_agent = request.META.get('HTTP_USER_AGENT')
                        business_request_header = construct_header('JCQ_XWSJ_NETLOG_FILE', user_agent, file_desc)
                        sender.async_send_business_file('project.audit', 'net_log', detector_id, business_request_header,
                                                        common.MEDIA_ROOT + save_data['save_path'], file_desc['filename'])

                    if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
                        common_header = ccd.get_common_command_header_of_detector('alert', 'JCQ_XWSJ',
                                                                                  'JCQ_XWSJ_NETLOG_FILE', request,
                                                                                  detector_id,
                                                                                  capture_date=datetime.datetime.strptime(
                                                                                      file_desc['time'],
                                                                                      '%Y-%m-%d %H:%M:%S'))
                        ccd.upload_file_2_director_of_detector(common_header, save_data,
                                                               json.dumps((file_desc['filename'], file_path)),
                                                               'JCQ_XWSJ_NETLOG_FILE', 'JCQ_XWSJ_NETLOG_FILE',
                                                               async_level=3)

                    return common.detector_message_response(200, '文件存储成功', {'message': 'success'},
                                                            status.HTTP_200_OK)
                else:
                    return common.detector_message_response(400, json.dumps(serializer.errors),
                                                            '数据处理失败')

            else:
                return common.detector_message_response(400, '文件上传失败: 文件重名', '文件上传失败')
        # elif len(request.FILES) == 0:  # 上传数据（文本字符串）
        # data = request_data.strip().replace('\n', '~=~')
        # requests.post(CR_URL, data={'data': data})
        # return common.detector_message_response(200, '数据存储成功', {'message': 'success'},
        # status.HTTP_200_OK)
        else:
            return common.detector_message_response(400, '上传的不是一个文件', '上传数据格式有误')

    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


from DetectCenter import print_util as pu


# 接收应用行为压缩数据流
def process_app_behavior_upload(request, file_relative_path):
    try:
        # request_data = common.print_header_data(request)  # 获取请求数据
        # send_file = request.body
        request_id = snowflake.next_id(1, 1)  # 确定请求的全局唯一ID
        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'app_behavior', len(request.FILES)))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'app_behavior', len(request.FILES))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        file_desc = request.META.get('HTTP_CONTENT_FILEDESC')  # 请求头中的数据字段
        file_desc = common.check_detector_upload_header_filedesc_field(file_desc)
        if isinstance(file_desc, Response):
            return file_desc
        print 'file_desc:', pu.pretty_print_format(file_desc)

        if len(request.FILES) == 1:  # 上传一个gzip压缩包
            file_absolute_path = os.path.join(common.MEDIA_ROOT, file_relative_path)  # 绝对路径（没有文件名）
            request_file = request.FILES.values()[0]
            gzip_f = gzip.GzipFile(mode='rb', fileobj=request_file)
            try:
                gzip_f.readline()  # 尝试gzip读取文件，若无法读取则不是gzip格式文件
                request_file.seek(0)  # 将文件流重置偏移为文件开头
                gzip_f.close()  # 关闭文件流
            except IOError:
                gzip_f.close()  # 关闭文件流
                request_file.close()
                return common.detector_message_response(400, '不是一个gzip压缩文件',
                                                        request_file.name + ' not a gzipped file')

            file_name = request_file.name  # 原始文件名
            save_file_name = common.rename_detector_upload_file(detector_id, file_name)  # 存储文件名
            is_success = fu.handle_upload_file(file_absolute_path, request_file, save_file_name)  # 上传文件
            if is_success:
                request_file.close()  # 关闭文件流
                file_path = os.path.join(file_absolute_path, save_file_name)

                # 生成业务处置系统所需文件（原始文件）
                if config.const.UPLOAD_BUSINESS_DISPOSAL:
                    try:
                        # common.generate_business_file('app_behavior', file_path, detector_id + '_' + str(int(time.time())) + '_' + str(1) + '.gz')
                        if not os.path.exists(config.const.DISPOSAL_DIR + 'app_behavior/'):
                            os.makedirs(config.const.DISPOSAL_DIR + 'app_behavior/')
                        shutil.copy(file_path, config.const.DISPOSAL_DIR + 'app_behavior/' + detector_id + '_' + file_desc['checksum'])
                        # pass
                    except:
                        traceback.print_exc()

                save_data = {
                    'log_type': 2,
                    'request_id': request_id,
                    'time': datetime.datetime.strptime(file_desc['time'], '%Y-%m-%d %H:%M:%S'),
                    'filename': file_desc['filename'],
                    'checksum': file_desc['checksum'],
                    'filetype': file_desc['filetype'],
                    'save_path': file_relative_path + save_file_name,
                    'receive_time': du.get_current_time(),
                    'device_id': detector_id
                }
                serializer = AuditLogSerializer(data=save_data)
                if serializer.is_valid():
                    serializer.save()  # 存储数据库

                    if config.const.UPLOAD_ES:
                        sender.async_send_app_behavior(request_id, AB_URL, file_path, detector_id)

                    if config.const.UPLOAD_BUSINESS:
                        user_agent = request.META.get('HTTP_USER_AGENT')
                        business_request_header = construct_header('JCQ_XWSJ_APPBEHAVIOR_FILE', user_agent, file_desc)
                        sender.async_send_business_file('project.audit', 'app_behavior', detector_id,
                                                        business_request_header,
                                                        common.MEDIA_ROOT + save_data['save_path'],
                                                        file_desc['filename'])

                    if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
                        common_header = ccd.get_common_command_header_of_detector('alert', 'JCQ_XWSJ',
                                                                                  'JCQ_XWSJ_APPBEHAVIOR_FILE',
                                                                                  request, detector_id,
                                                                                  capture_date=datetime.datetime.strptime(
                                                                                      file_desc['time'],
                                                                                      '%Y-%m-%d %H:%M:%S'))
                        ccd.upload_file_2_director_of_detector(common_header, save_data,
                                                               json.dumps((file_desc['filename'], file_path)),
                                                               'JCQ_XWSJ_APPBEHAVIOR_FILE', 'JCQ_XWSJ_APPBEHAVIOR_FILE',
                                                               async_level=3)

                    return common.detector_message_response(200, '文件存储成功', {'message': 'success'},
                                                            status.HTTP_200_OK)
                else:
                    return common.detector_message_response(400, json.dumps(serializer.errors),
                                                            '数据处理失败')
            else:
                return common.detector_message_response(400, '文件上传失败: 文件重名', '文件上传失败')
        # elif len(request.FILES) == 0:  # 上传数据
        # requests.post(AB_URL, data={'data': request_data})
        # return common.detector_message_response(200, '数据存储成功', {'message': 'success'},
        # status.HTTP_200_OK)
        else:
            return common.detector_message_response(400, '上传的不是一个文件', '上传数据格式有误')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 接收系统审计信息
def process_system_audit(request):
    try:
        report_time = du.get_current_time()  # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        data_list = common.detector_upload_json_preprocess(request_data)  # 返回List()格式的上传json数据
        if isinstance(data_list, Response):
            return data_list
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'detector_audit', len(data_list)))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'detector_audit', len(data_list))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        business_data_list = []  # 发送到业务数据服务器上的列表[(请求头, 数据),...]
        handle_data = copy.deepcopy(data_list)  # 生成业务处置系统所需文件的告警数据
        command_send_data = []  # 发送到指挥中心的数据[(请求头, 数据),...]

        for data in data_list:
            business_request_data = copy.deepcopy(data)  # 业务数据传输请求数据

            result = common.check_time_field(data)
            if isinstance(request, Response):
                return result

            if 'id' in data:
                data['log_id'] = data.pop('id')
            else:
                return common.detector_message_response(400, '请求数据中没有id字段', '请求数据中没有id字段')
            data['device_id'] = detector_id  # 加入检测器id字段
            data['report_time'] = report_time  # 加入上报时间字段

            if config.const.UPLOAD_BUSINESS:
                # 构建传输到业务数据服务器上的请求头和请求数据
                business_request_header = {
                    'Host': business_host,
                    'Date': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S'),
                    'Content-Type': 'application/json',
                    'Version': '1.0',
                    # 'Cookie': 'unknown',
                    'Source-Type': 'JCQ_XTSJ',
                    'Data-Type': 'msg',
                    'User-Agent': request.META.get('HTTP_USER_AGENT'),
                    'Capture-Date': data['time'].strftime('%a, %d %b %Y %H:%M:%S'),
                    'BusinessData-Type': 'JCQ_XTSJ',
                    'Meta-Data': json.dumps({
                        'id': detector_id
                    }),
                }  # 业务数据传输请求头
                ##### update by wwenan 2019.06.18 17:47####
                #business_data_list.append((business_request_header, business_request_data))
                ###########################################
		
            if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
                common_header = ccd.get_common_command_header_of_detector('status', 'AUDIT', 'JCQ_AUDIT',
                                                                          request, detector_id,
                                                                          capture_date=data['time'], data_type='msg')
                command_data = json.dumps(business_request_data, ensure_ascii=False).encode('utf-8')
                ccd.upload_json_2_director_of_detector(common_header, data, command_data, 'JCQ_AUDIT', async_level=3)

        serializer = AuditSystemSerializer(data=data_list, many=True)  # 序列化
        if serializer.is_valid():
            serializer.save()  # 存储数据库

            ##### update by wwenan 2019.06.18 17:47#####
            #if config.const.UPLOAD_BUSINESS:
                #sender.async_send_business_data('project.audit', 'JCQ_XTSJ', detector_id, business_data_list)
            ############################################

            # 生成业务处置系统所需文件
            if config.const.UPLOAD_BUSINESS_DISPOSAL:
                handle_data_type = 'detector_audit'
                file_dir = os.path.join(config.const.DISPOSAL_DIR, 'audit')
                file_name = 'detector_audit_' + str(int(time.time())) + '_' + str(1)
                sender.send_business_disposal(file_dir, file_name, request.META.get('HTTP_USER_AGENT'), handle_data_type, handle_data)

            return common.detector_message_response(200, '数据存储成功', {'message': 'Success'}, status.HTTP_200_OK)
        else:
            return common.detector_message_response(400, json.dumps(serializer.errors),
                                                    '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# **************************************** 处理界面请求 ****************************************


# 构造审计文件日志页面查询条件，用于显示列表信息和总数
def get_audit_log_query_terms(request_data):
    # 获取请求参数
    device_id = request_data.get('device_id')  # 检测器ID
    file_name = request_data.get('file_name')  # 文件名
    log_type = request_data.get('log_type')  # 日志类型（1表示通联关系，2表示应用行为）
    time_min = request_data.get('time_min')  # 时间起始值
    time_max = request_data.get('time_max')  # 时间结束值

    # 构造查询参数
    query_terms = {}

    if device_id is not None:
        query_terms['device_id__contains'] = device_id  # 模糊查询
    if file_name is not None:
        query_terms['filename__contains'] = file_name  # 模糊查询
    if log_type is not None:
        query_terms['log_type'] = int(log_type)
    if time_min is not None:  # 产生时间筛选
        query_terms['time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        query_terms['time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

    return query_terms


# 查询审计日志信息
def show_audit_log(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_audit_log_query_terms(request_data)  # 构造查询参数

        query_data = AuditLog.objects.filter(**query_terms).order_by('-id')[
                     start_pos:end_pos]  # 过滤查询，若query_terms={}，相当于all
        serializer_data = serialize('json', query_data,
                                    fields=('device_id', 'log_type', 'filename', 'time',
                                            'receive_time', 'save_path'))
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['time'] = fields['time'].replace('T', ' ')  # 去除时间显示时多出的字符'T'
            fields['receive_time'] = fields['receive_time'].replace('T', ' ')  # 去除时间显示时多出的字符'T'
            fields['file_name'] = fields.pop('filename')
            fields['file_path'] = common.MEDIA_ROOT + fields.pop('save_path')
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询审计日志信息数量
def show_audit_log_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_terms = get_audit_query_terms(request_data)  # 构造查询参数

        count = AuditLog.objects.filter(**query_terms).count()  # 数据条数
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 构造系统审计页面查询条件，用于显示列表信息和总数
def get_audit_query_terms(request_data):
    # 获取请求参数
    device_id = request_data.get('device_id')  # 检测器ID
    log_id = request_data.get('log_id')  # 日志ID
    user = request_data.get('user')  # 操作用户名
    opt_type = request_data.get('opt_type')  # 审计日志操作类型
    msg = request_data.get('message')  # 日志详情
    log_time = request_data.get('time')  # 时间

    # 构造查询参数
    query_terms = {}

    if device_id is not None:
        query_terms['device_id__contains'] = device_id  # 模糊查询
    if log_id is not None:
        query_terms['log_id__contains'] = log_id  # 模糊查询
    if user is not None:
        query_terms['user__contains'] = user  # 模糊查询
    if opt_type is not None:
        query_terms['opt_type__contains'] = opt_type  # 模糊查询
    if msg is not None:
        query_terms['message__contains'] = msg  # 模糊查询
    if log_time is not None:  # 产生时间筛选
        query_terms['time__gte'] = datetime.datetime.strptime(log_time, '%Y-%m-%d')
        query_terms['time__lt'] = datetime.datetime.strptime(log_time, '%Y-%m-%d') + datetime.timedelta(1)

    return query_terms


# 查询所有系统审计信息
def show_system_audit(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_audit_query_terms(request_data)  # 构造查询参数

        query_data = AuditSystem.objects.filter(**query_terms).order_by('-id')[
                     start_pos:end_pos]  # 过滤查询，若query_terms={}，相当于all
        serializer_data = serialize('json', query_data,
                                    fields=('device_id', 'log_id', 'user', 'opt_type', 'event_type',
                                            'message', 'time')
                                    )
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['time'] = fields['time'].replace('T', ' ')  # 去除时间显示时多出的字符'T'
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询系统审计信息数量
def show_system_audit_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_terms = get_audit_query_terms(request_data)  # 构造查询参数

        count = AuditSystem.objects.filter(**query_terms).count()  # 数据条数
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 构造本地审计页面查询条件，用于显示列表信息和总数
def get_local_audit_query_terms(request_data):
    # 获取请求参数
    log_id = request_data.get('log_id')  # 日志ID
    user = request_data.get('user')  # 操作用户名
    opt_type = request_data.get('opt_type')  # 审计日志操作类型
    msg = request_data.get('message')  # 日志详情
    log_time = request_data.get('time')  # 时间

    # 构造查询参数
    query_terms = {}

    if log_id is not None:
        query_terms['log_id__contains'] = log_id  # 模糊查询
    if user is not None:
        query_terms['user__contains'] = user  # 模糊查询
    if opt_type is not None:
        query_terms['opt_type__contains'] = opt_type  # 模糊查询
    if msg is not None:
        query_terms['message__contains'] = msg  # 模糊查询
    if log_time is not None:  # 产生时间筛选
        query_terms['time__gte'] = datetime.datetime.strptime(log_time, '%Y-%m-%d')
        query_terms['time__lt'] = datetime.datetime.strptime(log_time, '%Y-%m-%d') + datetime.timedelta(1)

    return query_terms


# 查询所有本地审计信息
def show_local_audit(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_local_audit_query_terms(request_data)  # 构造查询参数

        query_data = AuditManagement.objects.filter(**query_terms).order_by('-id')[
                     start_pos:end_pos]  # 过滤查询，若query_terms={}，相当于all
        serializer_data = serialize('json', query_data,
                                    fields=('log_id', 'user', 'opt_type', 'event_type',
                                            'message', 'time')
                                    )
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['time'] = fields['time'].replace('T', ' ')  # 去除时间显示时多出的字符'T'
            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询本地审计信息数量
def show_local_audit_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_terms = get_local_audit_query_terms(request_data)  # 构造查询参数

        count = AuditManagement.objects.filter(**query_terms).count()  # 数据条数
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def handwork_make_reqeust(request):
    request.META.set("")


# 发送管理系统自身审计日志
def send_audit(request, retract=0):
    try:
        if config.const.UPLOAD_DIRECTOR and check_global_director_connection():

            query_data = AuditManagement.objects.filter(is_send_command=0)
            if not query_data.exists():
                return common.ui_message_response(400, '不存在可发送的审计信息', '不存在可发送的审计信息')
            serializer_data = serialize('json', query_data,
                                        fields=('log_id', 'user', 'opt_type', 'event_type',
                                                'message', 'time')
                                        )
            list_data = json.loads(serializer_data)

            command_data = []
            for data in list_data:
                fields = data['fields']
                fields['id'] = fields.pop('log_id')
                fields['time'] = fields['time'].replace('T', ' ')  # 去除时间显示时多出的字符'T'
                command_data.append(fields)

            common_header = ccd.get_common_command_header_of_center('AUDIT', 'CENTER_AUDIT')
            command_data = json.dumps(command_data, ensure_ascii=False).encode('utf-8')
            ccd.upload_json_2_director_of_center(common_header, 'CENTER_AUDIT', command_data, async_level=3)

            # 修改为已发送
            update_id_list = [d['pk'] for d in list_data]
            AuditManagement.objects.filter(id__in=update_id_list).update(is_send_command=1)
            return common.ui_message_response(200, '发送管理中心审计日志成功', {}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


from DetectCenter.director_config import CENTER_USER_AGENT
# 写管理系统自身审计日志到业务处置（临时@@@@@@）
def write_center_audit_to_business_disposal():
    try:
        # 生成业务处置系统所需文件
        if config.const.UPLOAD_BUSINESS_DISPOSAL:
            # query_data = AuditManagement.objects.filter(is_send_command=0)
            query_data = AuditManagement.objects.filter()
            if not query_data.exists():
                print '没有审计信息'
            serializer_data = serialize('json', query_data,
                                        fields=('log_id', 'user', 'opt_type', 'event_type',
                                                'message', 'time')
                                        )
            list_data = json.loads(serializer_data)

            command_data = []
            for data in list_data:
                fields = data['fields']
                fields['id'] = fields.pop('log_id')
                fields['time'] = fields['time'].replace('T', ' ')  # 去除时间显示时多出的字符'T'
                command_data.append(fields)
            command_data = json.dumps(command_data, ensure_ascii=False).encode('utf-8')
            handle_data_type = 'center_audit'
            file_dir = os.path.join(config.const.DISPOSAL_DIR, 'audit')
            file_name = 'center_audit_' + str(int(time.time())) + '_' + str(1)
            sender.send_business_disposal(file_dir, file_name, CENTER_USER_AGENT, handle_data_type, command_data)
    except Exception:
        traceback.print_exc()



# 发送管理系统运行状态, 随心跳上传 不单独 上传
def send_running_status(request, retract=0):
    import psutil
    try:
        time.sleep(1)
        cpu_usage = int(psutil.cpu_percent(interval=1))
        psutil.cpu_stats()
        mem_usage = int(psutil.virtual_memory().percent)
        disk_usage = int(psutil.disk_usage('/').free / 1024 / 1024 / 1024)  # 单位GB

        command_data = json.dumps({
            'mem': mem_usage,
            'cpu': cpu_usage,
            'disk': disk_usage,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }, ensure_ascii=False).encode('utf-8')

        print command_data
        if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
            common_header = ccd.get_common_command_header_of_center('CENTER_STATUS', 'CENTER_STATUS_SYSTEM')
            ccd.upload_json_2_director_of_center(common_header, 'CENTER_STATUS', command_data, rule_id='0',
                                                 async_level=1)

            return common.ui_message_response(200, '发送管理中心状态成功', {}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 发送管理中心部署信息到指挥中心（已被注册接口取代）
def send_management_info(request):
    try:
        center_info = ManagementCenterInfo.objects.all()
        if not center_info.exists():
            return common.ui_message_response(400, '管理系统信息不存在', '管理系统信息不存在')

        data = serialize('json', center_info,
                         fields=('center_id', 'soft_version', 'device_ca', 'organs', 'address', 'address_code',
                                 'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info', 'access_time')
                         )  # 序列化
        list_data = json.loads(data)
        fields = list_data[0]['fields']

        fields['cpu_info'] = json.loads(fields['cpu_info'])
        fields['disk_info'] = json.loads(fields['disk_info'])
        fields['interface'] = json.loads(fields['interface'])
        fields['contact'] = json.loads(fields['contact'])

        print "management_center_info:", pu.pretty_print_format(fields)

        if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
            command_data = json.dumps(fields, ensure_ascii=False).encode('utf-8')
            common_header = ccd.get_common_command_header_of_center('CENTER_STATUS', 'CENTER_STATUS_INFO')
            ccd.upload_json_2_director_of_center(common_header, 'CENTER_STATUS_INFO', command_data, rule_id='0',
                                                 async_level=0)

            return common.ui_message_response(200, '发送管理中心信息成功', {}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 发送检测器部署信息到指挥中心
def send_detector_info(request, retract=0):
    try:
        if config.const.DIRECTOR_VERSION and check_global_director_connection():
            detector_info = Detector.objects.filter(device_status=1, is_effective=1)
            if not detector_info.exists():
                return common.ui_message_response(400, '不存在可上报至指挥中心的检测器', '不存在可上报至指挥中心的检测器')

            data = serialize('json', detector_info,
                             fields=('device_id', 'soft_version', 'organs', 'address', 'address_code', 'contact',
                                     'mem_total', 'interface', 'cpu_info', 'disk_info', 'register_time', 'auth_time')
                             )  # 序列化
            list_data = json.loads(data)
            command_data = []
            for info in list_data:
                fields = info['fields']
                if fields['register_time'] is not None:
                    fields['register_time'] = fields['register_time'].replace('T', ' ')
                else:
                    fields['register_time'] = '0000-00-00 00:00:00'
                if fields['auth_time'] is not None:
                    fields['access_time'] = fields.pop('auth_time').replace('T', ' ')
                else:
                    fields['access_time'] = '0000-00-00 00:00:00'

                fields['cpu_info'] = json.loads(fields['cpu_info'])
                fields['disk_info'] = json.loads(fields['disk_info'])
                fields['interface'] = json.loads(fields['interface'])
                fields['contact'] = json.loads(fields['contact'])

                command_data.append(fields)

            # print "detector_data:", pu.pretty_print_format(command_data)

            command_data = json.dumps(command_data, ensure_ascii=False).encode('utf-8')
            common_header = ccd.get_common_command_header_of_center('JCQ_STATUS', 'JCQ_STATUS_INFO')
            ccd.upload_json_2_director_of_center(common_header, 'JCQ_STATUS_INFO', command_data, rule_id='0',
                                                 async_level=0)

            return common.ui_message_response(200, '发送检测器信息成功', {}, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)
