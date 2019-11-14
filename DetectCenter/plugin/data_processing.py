# -*- coding:utf-8 -*-

# from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.core.serializers import serialize
from plugin_serializers import *
from DetectCenter import common, date_util as du, file_util as fu, print_util as pu, queryset_util as qu, config
from detector.models import Detector
import plugin_common as pc
from DetectCenter import common_center_2_director as ccd, sender
from django.db.models import Q, F
from director.models import DirectorPluginTask, DirectorPlugin
from plugin.models import PlugTask
from director.detect_center_reg_auth import check_global_director_connection

import traceback
import datetime
import json
import os
import logging
import time, copy
import shutil


# ************************************** 处理前端检测器请求 **************************************

# logger_record = logging.getLogger('project.record')


# 根据plug_id和plug_version获取插件
def get_plug(request, plug_id):
    try:
        report_time = du.get_current_time()           # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'plug', plug_id))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'get_plug', int(plug_id))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')
        
        # 获取请求参数
        plug_version = request_data.get('plug_version')  # 插件版本
        plug_info = PluginDetector.objects.filter(plug_id=plug_id, plug_version=plug_version).order_by('-id')
        director_plug_info = DirectorPlugin.objects.filter(plug_id=plug_id, plug_version=plug_version).order_by('-id')
        if plug_info.exists() or director_plug_info.exists():
            if plug_info.exists():
                plug_path = plug_info[0].plug_path
            else:
                plug_path = director_plug_info[0].plug_path
            file_path = os.path.join(common.MEDIA_ROOT, plug_path)
            file_name = os.path.split(plug_path)[1]
            return common.construct_download_file_header(file_path, plug_path, file_name)
        else:
            return common.detector_message_response(400, '数据库查询不到该记录', '插件不存在')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 根据plug_id和plug_config_version获取插件策略
def get_plug_policy(request, plug_id):
    try:
        report_time = du.get_current_time()           # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'plug_policy', plug_id))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'get_plug_config', int(plug_id))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')
        
        # 获取请求参数
        plug_config_version = request_data.get('plug_config_version')  # 插件策略版本
        plug_config_info = PluginDetector.objects.filter(
            plug_id=plug_id, plug_config_version=plug_config_version).order_by('-id')
        director_plug_config_info = DirectorPlugin.objects.filter(
            plug_id=plug_id, plug_config_version=plug_config_version).order_by('-id')
        if plug_config_info.exists() or director_plug_config_info.exists():
            if plug_config_info.exists():
                plug_policy_path = plug_config_info[0].plug_config_path
            else:
                plug_policy_path = director_plug_config_info[0].plug_config_path
            file_path = os.path.join(common.MEDIA_ROOT, plug_policy_path)
            file_name = os.path.split(plug_policy_path)[1]
            return common.construct_download_file_header(file_path, plug_policy_path, file_name, cal_md5=True)
        else:
            return common.detector_message_response(400, '数据库查询不到该记录', '插件策略不存在')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 处理插件检测结果上报
def process_plugin_alarm_file(request, file_relative_path):
    try:
        send_file = request.body
        report_time = du.get_current_date_string()        # 获取当前时间
        common.print_header_data(request)              # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'plug_alarm', len(request.FILES)))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'plug_alarm', len(request.FILES))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')

        data = request.META.get('HTTP_CONTENT_FILEDESC')  # 请求头中的数据字段

        if len(request.FILES) == 1:    # 上传一个文件
            file_absolute_path = os.path.join(common.MEDIA_ROOT, file_relative_path)  # 绝对路径（没有文件名）
            request_file = request.FILES.values()[0]
            # 文件重命名：检测器ID + '_' + 全局唯一编号 + 原文件后缀名
            save_file_name = common.rename_detector_upload_file(detector_id, request_file.name)
            is_success = fu.handle_upload_file(file_absolute_path, request_file, save_file_name)  # 上传文件
            if not is_success:  # 文件上传失败
                return common.detector_message_response(400, '服务器上存在相同的文件', '文件已经上传或者文件命名重复')

            data = common.check_detector_upload_header_filedesc_field(data)   # 校验Content-Filedesc字段
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
            data['save_path'] = file_relative_path + save_file_name

            serializer = PluginAlarmSerializer(data=data)  # 数据序列化
            if serializer.is_valid():
                serializer.save()  # 存储数据库
                if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
                    common_header = ccd.get_common_command_header_of_detector(msg_type='alert', source_type='JCQ_CJGJ', business_type='JCQ_CJGJ_FILE', request=request, device_id=detector_id, capture_date=data['time'])
                    ccd.upload_file_2_director_of_detector(common_header, data, json.dumps((data['filename'], common.MEDIA_ROOT + data['save_path'])), 'JCQ_CHGJ_FILE', from_type='JCQ_CHGJ_FILE', is_plugin=True, async_level=2)

                # 生成业务处置系统所需文件
                if config.const.UPLOAD_BUSINESS_DISPOSAL:
                    file_dir = os.path.join(config.const.DISPOSAL_DIR, 'plug')
                    t_str = str(int(time.time()))
                    file_name = 'plug_alarm_filedesc' + t_str + '_' + str(1)
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

                return common.detector_message_response(200, '数据和文件存储成功', {'message': 'success'},
                                                        status.HTTP_200_OK)
            else:
                return common.detector_message_response(400, json.dumps(serializer.errors),
                                                        '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# 插件状态上报
def process_plugin_status(request):
    try:
        report_time = du.get_current_date_string()           # 获取当前时间
        request_data = common.print_header_data(request)  # 获取请求数据

        detector_id = common.check_detector_available(request, Detector)  # 检查检测器是否合法，合法就返回检测器ID
        if isinstance(detector_id, Response):
            return detector_id
        data_list = common.detector_upload_json_preprocess(request_data)  # 返回List()格式的上传json数据
        if isinstance(data_list, Response):
            return data_list

        # 日志记录
        # logger_record.info('%s %s %s %d' % (request.META.get('REMOTE_ADDR'), detector_id, 'plug_status', len(data_list)))
        log_str = '%s %s %s %s %d' % (request.META.get('REMOTE_ADDR'), request.META.get('HTTP_X_REMOTE_ADDR', '0.0.0.0'), detector_id, 'plug_status', len(data_list))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'detector_access_log/')
        
        for data in data_list:
            command_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            data['device_id'] = detector_id       # 加入检测器id字段
            data['report_time'] = report_time     # 加入上报时间字段

            if config.const.UPLOAD_DIRECTOR and check_global_director_connection():
                common_header = ccd.get_common_command_header_of_detector(msg_type='status', source_type='JCQ_CJZT', business_type='JCQ_CJZT', device_id=detector_id, request=request, data_type='msg')
                ccd.upload_json_2_director_of_detector(common_header, data, command_data, 'JCQ_CJZT', is_plugin=True, async_level=2)

            # 生成业务处置系统所需文件(告警元信息)
            if config.const.UPLOAD_BUSINESS_DISPOSAL:
                handle_data_type = 'plug_status'     ###############type未确定
                file_dir = os.path.join(config.const.DISPOSAL_DIR, 'plug')
                file_name = 'plug_status_' + str(int(time.time())) + '_' + str(1)
                sender.send_business_disposal(file_dir, file_name, request.META.get('HTTP_USER_AGENT'),
                                              handle_data_type, copy.deepcopy(data))


        serializer = PluginStatusSerializer(data=data_list, many=True)
        if serializer.is_valid():
            serializer.save()        # 存储数据库
            return common.detector_message_response(200, '数据存储成功', {'message': 'success'},
                                                    status.HTTP_200_OK)
        else:
            return common.detector_message_response(400, json.dumps(serializer.errors),
                                                    '数据缺失或字段不符合规定，序列化出错')
    except Exception:
        traceback.print_exc()
        return common.detector_message_response(500, '服务器内部错误', '服务器内部错误',
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)


# **************************************** 处理界面请求 ****************************************


# 构造插件告警页面查询条件，用于显示列表信息和总数
def get_plug_alarm_query_terms(request_data):

    # 获取请求参数
    alarm_id = request_data.get('alarm_id')          # 插件告警ID
    plug_id = request_data.get('plug_id')            # 插件ID
    device_id = request_data.get('device_id')        # 检测器ID
    file_type = request_data.get('filetype')         # 文件类型
    time_min = request_data.get('time_min')          # 告警起始时间
    time_max = request_data.get('time_max')          # 告警结束时间

    # 构造查询参数
    query_terms = {}

    if alarm_id is not None:
        query_terms['alarm_id__contains'] = alarm_id   # 模糊查询
    if plug_id is not None:
        try:
            query_terms['plug_id__contains'] = int(plug_id)  # 模糊查询
        except Exception:
            pass
    if file_type is not None:
        query_terms['filetype'] = file_type
    if time_min is not None:                               # 生成任务的时间段筛选
        query_terms['time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        query_terms['time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

    if device_id is not None:
        query_terms['device_id__contains'] = device_id      # 模糊查询

    return query_terms


# 查询所有插件告警信息
def show_all_plug_alarm(request):
    try:
        request_data = common.print_header_data(request)                    # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_plug_alarm_query_terms(request_data)              # 获取查询条件

        # 过滤查询，若query_terms={}，相当于all
        query_data = PluginAlarm.objects.filter(**query_terms).order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data,
                                    fields=('alarm_id', 'plug_id', 'device_id', 'num',
                                            'filename', 'filetype', 'checksum', 'time',
                                            'save_path')
                                    )
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            if fields['time'] is not None:
                fields['time'] = fields['time'].replace('T', ' ')  # 去除因序列化时间类型出现的'T'
            if fields['plug_id'] is None:
                fields['plug_id'] = ''
            if fields['num'] is None:
                fields['num'] = ''
            fields['file_path'] = fields.pop('save_path')

            show_data.append(fields)

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询插件告警总数
def show_plug_alarm_count(request):
    try:
        request_data = common.print_header_data(request)          # 获取请求数据
        query_terms = get_plug_alarm_query_terms(request_data)    # 获取查询参数

        count = PluginAlarm.objects.filter(**query_terms).count()
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 插件状态
plug_status = ['plug_add_succ', 'plug_add_fail', 'plug_update_succ', 'plug_update_fail',
               'plug_config_succ', 'plug_config_fail', 'plug_start_succ', 'plug_start_fail',
               'plug_stop_succ', 'plug_stop_fail', 'plug_del_succ', 'plug_del_fail',
               'plug_run_fail', 'plug_res_overload']


# 构造插件状态页面查询条件，用于显示列表信息和总数
def get_plug_status_query_terms(request_data):

    # 获取请求参数
    plug_id = request_data.get('plug_id')            # 插件ID
    device_id = request_data.get('device_id')        # 检测器ID
    stat = request_data.get('status')              # 插件状态

    # 构造查询参数
    query_terms = {}

    if plug_id is not None:
        query_terms['plug_id__contains'] = plug_id  # 模糊查询

    if device_id is not None:
        query_terms['device_id__contains'] = device_id      # 模糊查询
    if stat is not None:
        query_terms['status'] = plug_status[int(stat) - 1]

    return query_terms


# 查询所有插件状态信息
def show_all_plug_status(request):
    try:
        request_data = common.print_header_data(request)                    # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_terms = get_plug_status_query_terms(request_data)             # 获取查询条件

        # 过滤查询，若query_terms={}，相当于all
        query_data = PluginStatus.objects.filter(**query_terms).order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data, fields=('device_id', 'plug_id', 'status', 'report_time'))
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            fields['status'] = plug_status.index(fields['status']) + 1
            fields['time'] = fields['report_time'].replace('T', ' ')  # 去除因序列化时间类型出现的'T'

            show_data.append(fields)

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询插件状态总数
def show_plug_status_count(request):
    try:
        request_data = common.print_header_data(request)           # 获取请求数据
        query_terms = get_plug_status_query_terms(request_data)    # 获取查询参数

        count = PluginStatus.objects.filter(**query_terms).count()
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)






# 带生成任务的插件部署
plugin_operate_map = {'add': 0, 'del': 1, 'change': 2, 'update_plug': 3, 'update_config': 4, '': 5}
plug_status_map = {1: '未同步', 0: '已同步'}
is_del_map = {1: '未删除', 0: '已删除'}

add_update_plug_cmd_map = {0: 'add', 1: 'update_plug', 2: 'update_config'}

task_cmd_map = {0: 'add', 1: 'reset', 2: 'start', 3: 'stop'}

# task_is_success_map = {0: '任务执行中', 1: '任务执行成功', 2: '任务执行失败', 3: '任务错误', 4: '已忽略'}   # 不用了

task_is_valid_map = {0: '已忽略', 1: '任务执行中', 2: '任务执行成功', 3: '任务执行失败', 4: '任务错误'}   # 现在默认任务随心跳下发后就当成任务执行成功，后续可能根据检测器的反馈确定实际执行成功状态


result_set = ('id', 'cmd', 'plug_type', 'plug_id', 'plug_version', 'plug_config_version',
              'cpu', 'mem', 'disk', 'device_id_list', 'generate_time', 'plug_path', 'plug_config_path',
              'device_id_list_run', 'plug_on_device_status', 'plug_status', 'plug_name', 'plug_config_name', 'is_plug_data_release', 'is_plug_file_release', 'is_config_file_release')


# 构造插件查询条件，用于显示列表信息和总数，根据指定结果集获取查询结果
def get_plug_query_terms(request_data):
    query_terms = {}

    plug_id = request_data.get('plug_id')  # 插件id
    if plug_id is not None:
        query_terms['plug_id__contains'] = plug_id

    plug_status = request_data.get('plug_status')  # 是否同步
    if plug_status is not None:
        query_terms['plug_status'] = plug_status

    time_min = request_data.get('time_min')  # 产生时间筛选
    if time_min is not None:
        query_terms['generate_time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    time_max = request_data.get('time_max')
    if time_max is not None:
        query_terms['generate_time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

    is_director = request_data.get('is_director')
    if is_director == '1':
        query_data = DirectorPlugin.objects.exclude(plug_status=0, is_del=0).filter(**query_terms)
    else:
        query_data = PluginDetector.objects.exclude(plug_status=0, is_del=0).filter(**query_terms)

    # 获取检测器查询条件
    device_id = request_data.get('device_id')  # 检测器id，如'1609010001'
    if device_id is not None:
        devices = Detector.objects.filter(device_id__contains=device_id)
        if devices.exists():
            filter_item = Q(device_id_list_run='#')
            for device in devices:
                print device.device_id
                filter_item = filter_item | Q(device_id_list_run__contains='#' + str(device.id) + "#")
            query_data = query_data.filter(filter_item)

    return query_data


def show_all_plug(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_data = get_plug_query_terms(request_data)  # 获取查询结果和指定显示结果集
        query_data = query_data.order_by('-id')[start_pos:end_pos]  # 排序

        serializer_data = serialize('json', query_data, fields=result_set)
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            operate_list = []
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            # operate = {'add': 1, 'del': 2,'change':3,'update_plug':4,'update_config':5, '': 6}
            if fields['cmd'].strip() in ['', 'add', 'del']:
                operate_list.append(plugin_operate_map[fields['cmd'].strip()])
            else:
                cmd_list = fields['cmd'].strip().split('#')
                for cmd in cmd_list:
                    if cmd == '':
                        continue
                    operate_list.append(plugin_operate_map[cmd])
            new_operate_list = []
            for v in operate_list:
                if v not in new_operate_list:
                    new_operate_list.append(v)
            fields['cmd'] = json.dumps(map(int, new_operate_list), separators=(',', ':'))

            fields['device_id_list_run'] = common.generate_device_ids_ui_str_from_model_str(fields['device_id_list_run'])   # 运行该规则的检测器
            fields['device_id_list'] = common.generate_device_ids_ui_str_from_model_str(fields['device_id_list'])    # 准备要下发的检测器

            if 'plug_on_device_status' in fields:
                fields['plug_on_device_status'] = json.dumps(pc.generate_plug_on_device_status_dict(fields.pop('plug_on_device_status')))

            fields['generate_time'] = fields.pop('generate_time').replace('T', ' ')

            show_data.append(fields)
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查询插件模块的总数
def show_plug_count(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        query_data = get_plug_query_terms(request_data)  # 获取查询结果

        count = query_data.count()  # 查询数量（与查询接口对应）
        show_data = {'count': count}
        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 添加、更新插件、更新插件策略
def add_update_plugin(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        plug_data = request_data.get('json')  # plug_data信息
        if plug_data is not None:  # 请求参数中有json（字符串，json解析后是dict）
            plug_data = json.loads(plug_data)
        else:
            return common.ui_message_response(400, '请求url中没有携带参数json', '请求参数没有json')

        # cmd_type_list = ['add', 'update_plug', 'update_config']

        cmd = common.check_request_int_field(request_data, 'cmd')
        if isinstance(cmd, Response):
            return cmd
        plug_data['cmd'] = add_update_plug_cmd_map[cmd]

        plug_data['plug_status'] = 1
        plug_data['is_del'] = 1

        # sid = transaction.savepoint()  # 事务保存点

        if cmd == 0:   # 添加插件
            # # 添加本级指挥节点
            # node_id_list = request_data.get('node_id_list', '')
            # if len(node_id_list) > 1:
            #     node_id_list = str(node_id_list[1:-1]).split('#')
            #     plug_data['node_id'] = node_id_list[0]
            # else:
            #     plug_data['node_id'] = 'A'

            if PluginDetector.objects.filter(plug_id=plug_data['plug_id']).exists():
                return common.ui_message_response(400, '插件ID %s 已存在' % plug_data['plug_id'], '插件ID %s 已存在' % plug_data['plug_id'])
            plug_data['generate_time'] = du.get_current_time()
            serializer = PluginDetectorSerializer(data=plug_data)  # 数据序列化
            if serializer.is_valid():
                serializer.save()  # 存储数据库
            else:
                return common.ui_message_response(400, json.dumps(serializer.errors),
                                                  '数据缺失或字段不符合规定，序列化出错')
        else:
            plug_id = common.check_request_int_field(request_data, 'id')
            if isinstance(plug_id, Response):
                return plug_id
            origin_cmd = PluginDetector.objects.get(id=plug_id).cmd
            if origin_cmd in ['add', 'del']:
                plug_data['cmd'] = origin_cmd
            else:
                plug_data['cmd'] = plug_data['cmd'] + '#' + origin_cmd

            print 'update_data:', plug_data
            PluginDetector.objects.filter(id=plug_id).update(**plug_data)
        cmd_type = [u'添加插件', u'更新插件', u'更新插件配置']
        common.generate_system_log(request_data, u'插件操作', cmd_type[cmd - 1], u'更新' + request_data.get('json') + u'插件')

        return common.ui_message_response(200, '插件生成（更新）成功或插件策略更新成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'插件操作失败', u'插件模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 删除多条插件
def delete_plug(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        id_list = common.check_request_list_or_dict_field(request_data, 'id')
        if isinstance(id_list, Response):
            return id_list

        delete_id_list = []  # 待删除的主键id列表
        update_id_list = []  # 待更新的主键id列表

        plug_list = PluginDetector.objects.filter(id__in=id_list)
        if not plug_list.exists():
            return common.ui_message_response(400, '根据条件没有查询到需要删除的规则记录', '没有选择的规则')
        for plug in plug_list:
            if plug.device_id_list_run == '':  # 当前插件没有在任何检测器上存在
                delete_id_list.append(plug.id)  # 直接删除
            else:
                update_id_list.append(plug.id)  # 更新
            PluginDetector.objects.filter(id__in=delete_id_list).delete()  # 删除
            PluginDetector.objects.filter(id__in=update_id_list).update(plug_status=1, device_id_list='', is_del=0,
                                                                        cmd='del')  # 更新
        common.generate_system_log(request_data, u'插件操作', u'删除插件',
                                   u'删除' + request_data.get('id') + u'插件')
        return common.ui_message_response(200, '删除成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'删除插件',
                                   u'删除' + request_data.get('id') + u'插件' + u'模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 接收插件id和检测器id，变更插件生效的检测器（此操作仅在选中规则生效的检测器范围一样才执行）
def change_plug(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        plug_id_list = common.check_request_list_or_dict_field(request_data, 'id')
        if isinstance(plug_id_list, Response):
            return plug_id_list

        device_id_list = request_data.get('detector_id_list')  # 检测器id列表
        plug_data = PluginDetector.objects.filter(id__in=plug_id_list)

        if device_id_list is not None:
            if device_id_list == '[]':  # 表示全部生效
                for info in plug_data:
                    if info.plug_status == 1 and info.cmd == 'add':
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list='#', cmd='add', plug_status=1)
                    else:
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list='#', cmd='change' + '#' + info.cmd, plug_status=1)

            elif device_id_list == '[0]':  # 表示清空生效范围
                for info in plug_data:
                    if info.plug_status == 1 and info.cmd == 'add':
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list='', cmd='add', plug_status=1)
                    else:
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list='', cmd='change' + '#' + info.cmd, plug_status=1)
            else:
                device_id_list = json.loads(device_id_list)
                update_detector_value = '#' + '#'.join(map(str, device_id_list)) + '#'
                for info in plug_data:
                    if info.plug_status == 1 and info.cmd == 'add':
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list=update_detector_value, cmd='add', plug_status=1)
                    else:
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list=update_detector_value, cmd='change' + '#' + info.cmd, plug_status=1)

            common.generate_system_log(request_data, u'插件操作', u'变更插件适用范围',
                                       u'变更插件中id列表为' + request_data.get('id') + u'的规则的生效检测器为' + request_data.get('detector_id_list'))
        else:  # 没有检测器id列表参数表示全部生效
            return common.ui_message_response(400, '参数detector_id_list不存在', '参数detector_id_list不存在')

        return common.ui_message_response(200, '变更成功', 'success', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'变更插件适用范围', u'变更插件生效检测器范围模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 接收插件id和检测器id，追加插件生效的检测器（此操作不限制选中的插件生效的检测器范围是否一样）
def append_plug(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        plug_id_list = common.check_request_list_or_dict_field(request_data, 'id')
        if isinstance(plug_id_list, Response):
            return plug_id_list
        device_id_list = request_data.get('detector_id_list')  # 检测器id列表参数

        if device_id_list is not None:
            plug_info = PluginDetector.objects.filter(id__in=plug_id_list)
            if device_id_list == '[]':  # 追加全部检测器
                for info in plug_info:
                    if info.plug_status == 1 and info.cmd == 'add':
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list='#', cmd='add', plug_status=1)
                    else:
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list='#', cmd='change' + '#' + info.cmd, plug_status=1)

            else:  # 追加部分检测器，求原先列表和现在列表的并集
                device_id_list = json.loads(device_id_list)
                for info in plug_info:

                    if info.device_id_list not in ['', '#']:  # 原先列表不是全部，也不为空
                        origin_detector_list = map(int, info.device_id_list[1: -1].split('#'))
                        update_detector_value = '#' + '#'.join(map(
                            str, sorted(set(device_id_list) | set(origin_detector_list)))) + '#'
                    elif info.device_id_list == '':  # 原来列表为空
                        update_detector_value = '#' + '#'.join(map(str, device_id_list)) + '#'
                    else:
                        continue

                    if info.plug_status == 1 and info.cmd == 'add':
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list=update_detector_value, cmd='add', plug_status=1)
                    else:
                        PluginDetector.objects.filter(id=info.id).update(
                            device_id_list=update_detector_value, cmd='change' + '#' + info.cmd, plug_status=1)

            common.generate_system_log(request_data, u'插件操作', u'追加插件生效范围',
                                       u'追加插件中id列表为' + request_data.get('id') + u'的插件的生效检测器追加' + request_data.get('detector_id_list'))
        else:  # 没有检测器id列表参数表示全部生效
            return common.ui_message_response(400, '参数detector_id_list不存在', '参数detector_id_list不存在')
        return common.ui_message_response(200, '追加成功', 'success', status.HTTP_200_OK)

    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'追加插件生效范围',
                                   u'追加插件生效检测器范围模块出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_plug_fields(cmd):
    plug_set = ()
    if cmd == 'add' or cmd == 'update_plug':
        plug_set = ('plug_type', 'plug_id', 'plug_version', 'plug_config_version', 'cpu', 'mem', 'disk')
    elif cmd == 'update_config':
        plug_set = ('plug_id', 'plug_config_version', 'cpu', 'mem', 'disk')
    else:
        pass
    return plug_set


def add_plugin_operate(detector_id, operate, detector_operate_dict):
    if detector_id not in detector_operate_dict:
        print "add:", detector_id, "###########", operate
        detector_operate_dict[detector_id] = [operate]
    else:
        print "append:", detector_id, "###########", operate
        detector_operate_dict[detector_id].append(operate)


# 生成某个模块的插件任务
def generate_increment_plug_task(request_data):
    """
    生成某个模块的插件任务
    :param request_data:
    :return:
    """
    try:
        pu.print_format_header('增量下发插件')

        generate_time = du.get_current_time()

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}   # id与device_id的对应关系
        device_id_dict = {item[1]: item[0] for item in device_id_all}   # device_id与id的对应关系
        print "device_id_dict:", pu.pretty_print_format(device_id_dict)

        device_plugs_dict = {}  # key: 检测器ID, value: 要下发的插件操作List

        # 查询未生成任务的插件信息
        plug_data = PluginDetector.objects.filter(plug_status=1).order_by('-id')
        if not plug_data.exists():
            return common.ui_message_response(200, '没有未下发的插件', '没有未下发的插件', status.HTTP_200_OK)

        plug_json = serialize('json', plug_data, fields=result_set)  # 序列化成json
        plug_all = json.loads(plug_json)   # 所有插件的List信息

        # 插件和新的开启状态信息字典
        plug_on_device_status_dict = {}   # key: 插件主键ID value: 插件最终下发的检测器的开启信息
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
            print 'plug:', plug_dict

            # 处理插件在检测器上开启状态
            add_device_status_dict = {}  # 新增的检测器状态
            del_device_status_dict = {}  # 要删除的检测器状态

            index += 1
            if 'add' in plug.cmd:
                for detector_id in now_device_list:
                    plug_set = get_plug_fields('add')
                    add_command = {'type': 'plug', 'cmd': 'add'}
                    for field in plug_set:
                        add_command[field] = plug_dict.get(field)
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
                    # add_plugin_operate(detector_id, {'type': 'plug', 'cmd': 'start', 'plug_id': plug.plug_id}, device_plugs_dict)   # 添加一条开启插件命令
                    add_device_status_dict[device_id_dict[detector_id]] = '1'
            if 'del' in plug.cmd:
                for detector_id in previous_device_list:
                    add_command = {'type': 'plug', 'cmd': 'del', 'plug_id': plug.plug_id}
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
                    del_device_status_dict[device_id_dict[detector_id]] = '0'
            if 'update_plug' in plug.cmd:
                for detector_id in previous_device_list:
                    plug_set = get_plug_fields('update_plug')
                    add_command = {'type': 'plug', 'cmd': 'update'}
                    for field in plug_set:
                        add_command[field] = plug_dict.get(field)
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
            if 'update_config' in plug.cmd:
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
                    add_device_status_dict[device_id_dict[detector_id]] = '1'
                del_device_ids = set(previous_device_list) - (set(previous_device_list) & set(now_device_list))
                for detector_id in del_device_ids:   # 插件对应的部分检测器删除
                    add_command = {'type': 'plug', 'cmd': 'del', 'plug_id': plug.plug_id}
                    add_plugin_operate(detector_id, add_command, device_plugs_dict)
                    del_device_status_dict[device_id_dict[detector_id]] = '0'

            # 处理 插件在检测器上的运行状态
            pre_device_status_dict = pc.generate_plug_on_device_status_dict(plug.plug_on_device_status)
            union = dict(pre_device_status_dict, **add_device_status_dict)
            for k in del_device_status_dict:
                if k in union:
                    union.pop(k)
            print "add_status:", add_device_status_dict, "del_status:", del_device_status_dict
            plug_on_device_status_dict[plug.id] = pc.generate_plug_on_device_status_str(union)

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
                    'user': request_data.get('uuid', '')
                }
                task_list.append(task_data)
            except Exception:
                traceback.print_exc()
                print '生成检测器{0}任务失败'.format(k)


        if not task_list:
            return common.ui_message_response(200, '没有任务需要生成', '没有任务需要生成', status.HTTP_200_OK)
        else:
            serializer_task = PlugTaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
            else:
                return common.ui_message_response(400, json.dumps(serializer_task.errors),
                                                  'task数据缺失或字段不符合规定，序列化出错')


        # 更新相应plug表的版本号、状态、操作时间，检测器运行列表更新为检测器变更列表
        for k, value in plug_on_device_status_dict.items():   # plug_on_device_status_dict与plug_data长度相同
            # PluginDetector.objects.filter(id=k).update(version=version_num, plug_status=0, cmd='', device_id_list_run=F('device_id_list'), plug_on_device_status=value)
            PluginDetector.objects.filter(id=k).update(version='', plug_status=0, cmd='', device_id_list_run=F('device_id_list'), plug_on_device_status=value)

        common.generate_system_log(request_data, u'插件操作', u'插件增量下发',
                                   u'插件增量下发' + json.dumps(task_list, cls=qu.CJsonEncoder, encoding='utf-8', ensure_ascii=False))
        return common.ui_message_response(200, '插件任务生成成功', '插件任务生成成功', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'插件增量下发', u'插件增量下发模块异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 全量生成插件任务
def generate_fulldose_plug_task(request_data):
    """
    全量生成插件任务
    :param request_data:
    :return:
    """
    try:

        pu.print_format_header('管理中心全量下发插件')

        device_id_list = request_data.get('detector_id_list')  # 全量下发需选择检测器

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}  # id与device_id的对应关系
        print '------------全量下发'

        if device_id_list is None:
            return common.ui_message_response(400, '请求url中没有携带参数detector_id_list', '请求参数没有detector_id_list')
        elif device_id_list == '[]':  # 表示全部检测器
            device_id_list = id_device_dict.values()
        else:
            device_id_list = json.loads(device_id_list)

        generate_time = du.get_current_time()

        device_plugs_dict = {}

        is_device_has_plug = False  # 标识对所有的检测器，是否有插件可以下发
        for device_id in device_id_list:
            # plug_data = PluginDetector.objects.filter(
            #     Q(device_id_list_run__contains='#' + str(device_id) + '#') | Q(device_id_list_run='#'))
            plug_data = PluginDetector.objects.filter(
                Q(device_id_list_run__contains='#' + str(device_id) + '#') | Q(device_id_list_run='#'), is_del=1)
            plug_data_director = DirectorPlugin.objects.filter(
                Q(device_id_list_run__contains='#' + str(device_id) + '#') | Q(device_id_list_run='#'), is_del=1)
            if (not plug_data.exists() and not plug_data_director.exists()):
                print '对于检测器' + device_id + ',指挥中心和管理中心没有可全量下发的插件'
                # if is_director:
                #     send_echo_2_no_task(director_down_header)
                continue
            else:
                is_device_has_plug = is_device_has_plug | True

            plug_json = serialize('json', plug_data, fields=result_set)  # 序列化成json
            plug_all = json.loads(plug_json)
            plug_data_list = [plug['fields'] for plug in plug_all]

            plug_json_director = serialize('json', plug_data_director, fields=result_set)  # 序列化成json
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
                    'user': request_data.get('uuid', ''),
                    'is_valid': 1
                    # 'is_success': 'false'
                }
                task_list.append(task_data)
            except:
                traceback.print_exc()
                print '生成检测器{0}任务失败'.format(k)

        if not is_device_has_plug:
            return common.ui_message_response(200, '没有可全量下发的插件', '没有可全量下发的插件', status.HTTP_200_OK)

        if not task_list:
            return common.ui_message_response(200, '没有任务需要生成', '没有任务需要生成', status.HTTP_200_OK)
        else:
            serializer_task = PlugTaskSerializer(data=task_list, many=True)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
                common.generate_system_log(request_data, u'插件操作', u'全量刷新检测器插件',
                                           u'全量刷新检测器插件' + json.dumps(task_list, cls=qu.CJsonEncoder, encoding='utf-8',
                                                                     ensure_ascii=False))
            else:
                common.generate_system_log(request_data, u'插件操作', u'全量刷新检测器插件',
                                           u'全量刷新检测器插件，task数据缺失或字段不符合规定，序列化出错')
                return common.ui_message_response(400, json.dumps(serializer_task.errors),
                                                  'task数据缺失或字段不符合规定，序列化出错')

        return common.ui_message_response(200, '插件任务生成成功', '插件任务生成成功', status.HTTP_200_OK)
    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'插件操作', u'插件模块异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def report_all_plugin_to_direct_center(request):
    try:
        request_data = common.print_header_data(request)

        # 所有正在运行的检测器
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}  # id与device_id的对应关系

        plug_data = PluginDetector.objects.filter(is_del=1)

        # result_set = get_result_set(policy_type)
        plug_json = serialize('json', plug_data)
        plug_all = json.loads(plug_json)

        command_data_list = []
        for plug in plug_all:
            # print rule['fields']
            fields = plug['fields']

            device_id_list_run = fields['device_id_list_run']
            if device_id_list_run != '#' and device_id_list_run != '':
                id_list = map(int, device_id_list_run[1:-1].split("#"))
                fields['device_id_list_run'] = '#' + '#'.join([id_device_dict[id] for id in id_list]) + '#'
            device_id_list = fields['device_id_list']
            if device_id_list != '#' and device_id_list != '':
                id_list = map(int, device_id_list[1:-1].split("#"))
                fields['device_id_list'] = '#' + '#'.join([id_device_dict[id] for id in id_list]) + '#'

            command_data_list.append(fields)

        command_data = {}
        if command_data_list:
            command_data['sync_director'] = command_data_list

        print "fulldose upload to director:", command_data

        # common_header = ccd.get_common_command_header('CENTER_POLICY', common.COMMAND_POLICY_TYPE[policy_type - 1],
        #                                              task_type='1')
        # ccd.jcq_upload_json_2_director(common_header, common.COMMAND_RULE_TYPE[policy_type - 1], command_data)

        return common.ui_message_response(200, '全量同步管理中心插件到指挥中心成功', '全量同步插件成功')
    except:
        traceback.print_exc()
        return common.ui_message_response(400, '全量同步管理中心插件到指挥中心失败', '服务器内部错误')


# 插件同步synchronization
def plug_synchronization(request):
    try:

        request_data = common.print_header_data(request)  # 获取请求数据

        # 获取请求参数，判断参数的合法性
        operate_type = common.check_request_int_field(request_data, 'type')
        if isinstance(operate_type, Response):
            return operate_type
        if operate_type == 0:    # 增量
            return generate_increment_plug_task(request_data)
        else:                    # 全量
            return generate_fulldose_plug_task(request_data)
    except:
        common.generate_system_log(request_data, u'插件操作', u'插件操作', u'插件模块异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 开启或者关闭某个检测器上的插件
def start_stop_plugin(request):
    try:

        request_data = common.print_header_data(request)
        generate_time = du.get_current_time()

        id = request_data.get('id')
        detector_id = common.check_request_int_field(request_data, 'detector_id')  # 检测器主键ID
        if isinstance(detector_id, Response):
            return Response
        operate = common.check_request_int_field(request_data, 'operate')
        if isinstance(operate, Response):
            return operate
        plug_data = PluginDetector.objects.filter(id=id)
        if not plug_data.exists():
            return common.ui_message_response(400, '给定插件不存在', '给定插件不存在')
        if detector_id is None:
            return common.ui_message_response(400, '请设置detector_id主键ID参数', '请设置detector_id主键ID参数')
        detector_info = Detector.objects.filter(id=detector_id)
        new_status = ''
        plug_id = ''
        for plug in plug_data:
            new_status = plug.plug_on_device_status
            plug_id = plug.plug_id
            print 'begin operate:', new_status
            plug_on_device_status_dict = pc.generate_plug_on_device_status_dict(plug.plug_on_device_status)
            if detector_id in plug_on_device_status_dict:
                plug_on_device_status_dict[detector_id] = str(operate)
                new_status = pc.generate_plug_on_device_status_str(plug_on_device_status_dict)
            else:
                return common.ui_message_response(400, '给定插件plug_id的生效检测器不包括给定检测器detector_id',
                                                  '给定插件plug_id的生效检测器不包括给定检测器detector_id')
        print 'after opearate:', new_status

        operate_str = 'start' if operate else 'stop'
        add_command = {'type': 'plug', 'cmd': operate_str, 'plug_id': plug_id}

        version_num = common.cal_task_version([PlugTask, DirectorPluginTask], detector_info[0].device_id if detector_info.exists() else detector_id, 'plugin', '2')

        task_data = {
            'version': version_num,
            'cmd': operate_str,
            'num': 1,
            'config': json.dumps([add_command], encoding='utf-8', ensure_ascii=False),
            'generate_time': generate_time,
            'device_id': detector_info[0].device_id if detector_info.exists() else detector_id,
            'user': request_data.get('uuid', '')
        }
        if not task_data:
            return common.ui_message_response(200, '没有任务需要生成', '没有任务需要生成', status.HTTP_200_OK)
        else:
            serializer_task = PlugTaskSerializer(data=task_data)  # 序列化task数据
            if serializer_task.is_valid():
                serializer_task.save()  # 存储数据库task表
            else:
                return common.ui_message_response(400, json.dumps(serializer_task.errors),
                                                  'task数据缺失或字段不符合规定，序列化出错')

        plug_data.update(plug_on_device_status=new_status)  # 更新对应插件在检测器上的开启状态

        # # 将detector_info表中对应检测器的plug_type标记为1，表示该插件有策略下发
        # update_fields = {'plug_type': 1}
        # Detector.objects.filter(id=detector_id).update(**update_fields)

        common.generate_system_log(request_data, u'插件操作', u'插件' + operate_str,
                                   u'插件' + operate_str + json.dumps(task_data, cls=qu.CJsonEncoder, encoding='utf-8',
                                                                    ensure_ascii=False))
        return common.ui_message_response(200, operate_str + '插件成功', operate_str + '插件成功', status.HTTP_200_OK)

    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'插件操作', u'插件模块异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 构造插件任务页面查询条件，用于显示列表信息和总数
def get_task_query_terms(request_data):
    # 获取请求参数
    task_cmd = request_data.get('cmd')  # 任务变更命令
    task_id = request_data.get('id')  # 任务ID
    task_version = request_data.get('version')  # 任务版本号
    device_id = request_data.get('device_id')   # 检测器ID
    # is_success = request_data.get('is_success')  # 实际任务随心跳下发后的任务执行成功状态
    is_valid = request_data.get('is_valid')   # 任务完成状态
    time_min = request_data.get('time_min')  # 任务生成起始时间
    time_max = request_data.get('time_max')  # 任务生成结束时间
    user = request_data.get('user')  # 操作用户
    query_terms = {}  # 构造查询参数


    if task_cmd is not None:  # 界面与数据库数据转换
        query_terms['cmd'] = task_cmd_map[int(task_cmd)]

    if task_id is not None:
        query_terms['id__contains'] = task_id  # 模糊查询

    if task_version is not None:
        query_terms['version__contains'] = task_version  # 模糊查询

    if device_id is not None:
        query_terms['device_id__contains'] = device_id

    if time_min is not None:  # 生成任务的时间段筛选
        query_terms['generate_time__gte'] = datetime.datetime.strptime(time_min, '%Y-%m-%d')
    if time_max is not None:
        query_terms['generate_time__lt'] = datetime.datetime.strptime(time_max, '%Y-%m-%d') + datetime.timedelta(1)

    if user is not None:
        query_terms['user'] = user

    is_director = request_data.get('is_director')
    if is_director == '1':
        query_data = DirectorPluginTask.objects.filter(**query_terms)
    else:
        query_data = PlugTask.objects.filter(**query_terms)

    # if is_success is not None:
    #     query_data = query_data.filter(is_success=is_success)

    if is_valid is not None:     # 任务状态 已忽略0 任务执行中1、任务执行成功2、任务执行失败3、任务错误4
        query_data = query_data.filter(is_valid=is_valid)

    return query_data


# 查询所有任务信息
def show_all_tasks(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据
        start_pos, end_pos, page_size = common.get_page_data(request_data)  # 获取页码数据
        query_data = get_task_query_terms(request_data)  # 构造查询参数

        # 过滤查询，若query_terms={}，相当于all
        query_data = query_data.order_by('-id')[start_pos:end_pos]
        serializer_data = serialize('json', query_data, fields=('id', 'version', 'cmd', 'num', 'config', 'generate_time', 'release_time', 'is_valid', 'device_id', 'is_success', 'is_valid', 'user'))
        list_data = json.loads(serializer_data)
        show_data = []
        for data in list_data:
            fields = data['fields']
            fields['id'] = data['pk']  # 加入主键id
            cmd = fields.pop('cmd')
            new_dict = {value: key for key, value in task_cmd_map.iteritems()}
            fields['cmd'] = new_dict[cmd]

            generate_time = fields.pop('generate_time')
            if generate_time is not None:
                fields['generate_time'] = generate_time.replace('T', ' ')  # 去除因序列化时间类型出现的'T'
            else:
                fields['generate_time'] = '0000-00-00 00:00:00'

            release_time = fields.pop('release_time')
            if release_time is not None:
                fields['release_time'] = release_time.replace('T', ' ')  # 去除因序列化时间类型出现的'T'
            else:
                fields['release_time'] = '0000-00-00 00:00:00'

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
        query_data = get_task_query_terms(request_data)  # 构造查询参数

        count = query_data.count()
        show_data = {'count': count}

        return common.ui_message_response(200, '查询成功', show_data, status.HTTP_200_OK)
    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 将插件任务状态设置为已忽略
def update_task_plug(request):
    try:
        # task.cmd-> 0:add 1:reset 2:start 3:stop
        request_data = common.print_header_data(request)
        task_id = request_data.get('id')
        if task_id is not None:
            plug_task = PlugTask.objects.filter(id=task_id).update(is_valid=0)
            for task in plug_task:
                if task.cmd in ['start', 'stop']:     # 对于开启或者关闭插件任务 需要改变原来插件上的对应检测器的开启状态
                    plug_id = json.loads(task.config)[0]['plug_id']
                    print 'plug_id:', plug_id, 'config:', json.loads(task.config)
                    pre_status_dict = pc.generate_plug_on_device_status_dict(PluginDetector.objects.filter(plug_id=plug_id)[0].plug_on_device_status)
                    print 'pre_status_dict:', pre_status_dict
                    if task.device_id in pre_status_dict:
                        pre_status_dict[task.device_id] = '1' if pre_status_dict[task.device_id] == '0' else '0'
                    print 'new_status_dict:', pre_status_dict
                    PluginDetector.objects.filter(plug_id=plug_id).update(plug_on_device_status=pc.generate_plug_on_device_status_str(pre_status_dict))

            common.generate_system_log(request_data, u'插件操作', u'插件任务',
                                       u'将插件任务' + request_data.get('id') + u'状态设置为已忽略')
            return common.ui_message_response(200, '插件任务状态设置成功', '状态设置为已忽略', status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '请求url中没有携带参数id', '请求参数没有id')
    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'插件任务',
                                   u'将插件任务' + request_data.get('id') + u'状态设置为已忽略出现错误')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 将插件任务重新下发
def send_again(request):
    try:
        request_data = common.print_header_data(request)

        # 根据job_id，获取插件任务的相关信息，用来重新下发
        job_id = common.check_request_int_field(request_data, 'id')
        if isinstance(job_id, Response):
            return job_id

        task = PlugTask.objects.get(id=job_id)

        # 更新任务的相关信息
        PlugTask.objects.filter(id=job_id).update(generate_time=du.get_current_time(), is_valid=1)

        # 记录日志
        common.generate_system_log(request_data, u'插件操作', u'插件任务重新下发',
                                   u'将插件任务' + request_data.get('id') + json.dumps(
                                       task.config) + u'插件任务重新下发')

        return common.ui_message_response(200, '插件任务重新下发成功', task.config, status.HTTP_200_OK)


    except Exception:
        common.generate_system_log(request_data, u'插件操作', u'插件任务重新下发',
                                   u'将插件任务' + request_data.get('id') + u'插件任务重新下发模块程序出现异常')
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 判断是否有插件任务需要生成
def judge_plug_generation(request):
    try:
        request_data = common.print_header_data(request)  # 获取请求数据

        operate_type = common.check_request_int_field(request_data, 'type')  # 操作类型（0：增量，1：全量）
        if isinstance(operate_type, Response):
            return operate_type
        if operate_type == 0:  # 增量
            # 查询所有未生成任务的规则数量
            amount = PluginDetector.objects.filter(plug_status=1).count()

            if amount == 0:
                return common.ui_message_response(200, '没有插件任务需要生成', amount, status.HTTP_200_OK)
            else:
                return common.ui_message_response(200, '有插件任务生成', amount, status.HTTP_200_OK)
        elif operate_type == 1:  # 全量
            # 查询没有标记删除的规则（作为一条全量下发任务的config）的数量
            reset_amount = PluginDetector.objects.filter(is_del=1).count()
            # # 查询所有add类型的规则和del类型未生成任务的规则（作为一条全量下发任务的config）的数量
            # reset_amount = rule_models[policy_type - 1].objects.exclude(operate='del', plug_status=0).count()
            if reset_amount == 0:
                return common.ui_message_response(200, '没有插件任务需要生成', reset_amount, status.HTTP_200_OK)
            else:
                return common.ui_message_response(200, '有插件任务生成', reset_amount, status.HTTP_200_OK)
        else:
            return common.ui_message_response(400, '请求参数type不是0、1', '请求参数type不合法')

    except Exception:
        traceback.print_exc()
        return common.ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)
