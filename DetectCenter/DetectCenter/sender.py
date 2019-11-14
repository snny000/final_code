# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from rest_framework import status
from django.http import HttpResponse
import json
import https_requests as requests
import string
import time
import datetime
import tasks
import log_util as lu
import file_util as fu
import traceback
import common, date_util as du, print_util as pu
import gzip
import logging
from requests_toolbelt import MultipartEncoder
import os
from director.models import ManagementCenterInfo
from director import detect_center_reg_auth
from audit.models import AuditLog
from DetectCenter import director_config, config
from director.models import DirectorPlugin
# from director.data_processing import generate_increment_plug_task, generate_fulldose_plug_task


def check_director_cookies(retract=0):
    # 携带cookie
    cookies = director_config.CENTER_COOKIE
    if director_config.CENTER_COOKIE is None or director_config.CENTER_COOKIE == '':
        pu.print_with_retract('CENTER_COOKIE变量为空，查询数据库')
        center_info = ManagementCenterInfo.objects.all()
        if not center_info.exists() or center_info[0].cookie is None or center_info[0].cookie == '':  # 还没有认证过，或者认证失败
            pu.print_with_retract('数据库不存在cookie，重新认证')
            result = detect_center_reg_auth.send_auth_login_request()
            if result['code'] != 200:  # 认证失败
                pu.print_with_retract(result['msg'])
                return
            # 认证成功
            cookies = ManagementCenterInfo.objects.all()[0].cookie
        else:  # 数据库存有cookie
            pu.print_with_retract('数据库存在cookie')
            cookies = center_info[0].cookie
        cookies = json.loads(cookies, encoding='utf-8')
    pu.print_with_retract('CENTER_COOKIE: ' + json.dumps(cookies))
    director_config.CENTER_COOKIE = cookies
    return cookies


# 发送至指挥中心
def send_director(url, device_id, data_type, header, data, retract=0):
    """
    发送数据到指挥中心
    :param url:
    :param device_id:    如果发送的是检测其数据，则为检测器ID，如果是管理中心数据则为管理中心ID，用户记录日志
    :param data_type:    用于标识发送的数据类型
    :param header:       请求头
    :param data:         请求数据，可能是文件，如果是文件data格式是tuple（filename，filepath）
    :param retract       打印控制台缩进数，以"tab"为单位
    :return:
    """
    try:

        pu.print_format_header('发送至指挥中心', retract=retract)


        cookies = check_director_cookies()    # 携带cookie

        print "header:", pu.pretty_print_format(header)
        print "data:", pu.pretty_print_format(json.loads(data))

        if header.get('Data-Type') == 'file':
            boundary = '---------------------------' + (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(6))))[0:10]
            header['Content-Type'] = 'multipart/form-data;boundary=' + boundary
            data = json.loads(data)
            print "###file config", data[0], data[1]
            data = MultipartEncoder(
                fields={
                    "file": (data[0], open(data[1], "rb"), "multipart/form-data")  # 文件流
                },
                boundary=boundary
            )  # 文件实体对象

        pu.print_with_retract('send %s type data to director' % data_type)
        resp = requests.post(url, headers=header, data=data, cookies=cookies)
        # pu.print_with_retract(resp.status_code, retract=retract+1)  # 响应码
        # pu.print_with_retract(resp.headers, retract=retract+1)  # 响应头
        pu.print_with_retract(resp.text.encode('utf-8'), retract=retract+1)  # 响应消息正文
        log_str = '%s %s %d %s' % (device_id, data_type, resp.status_code, resp.text.encode('utf-8'))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'director_log/', prefix='send_director.', suffix='log')

        if resp.status_code == 400:   # cookie失效或者不合法
            pu.print_with_retract('管理中心的Cookie失效, 重新认证')
            res = detect_center_reg_auth.send_auth_login_request()
            if res['code'] == 200:
                resp = requests.post(url, headers=header, data=data, cookies=check_director_cookies())
                # pu.print_with_retract(resp.status_code, retract=retract+1)  # 响应码
                # pu.print_with_retract(resp.headers, retract=retract+1)  # 响应头
                pu.print_with_retract(resp.text.encode('utf-8'), retract=retract+1)  # 响应消息正文

        pu.print_format_tail('发送至指挥中心', retract=retract)
    except Exception as e:
        # print e.args, "##", e.message
        traceback.print_exc()
        log_str = '%s %s %s' % (device_id, data_type, 'send_exception')
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'director_log/', prefix='send_director.', suffix='log')


def async_send_director(url, detector_id, data_type, header, data, retract=0):
    tasks.task_send_director.apply_async((url, detector_id, data_type, header, data), serializer='msgpack')  ####异步发送


def async_send_director_hi(url, detector_id, data_type, header, data, retract=0):
    tasks.task_send_director_hi.apply_async((url, detector_id, data_type, header, data), serializer='msgpack')  ####异步发送


def async_send_director_lo(url, detector_id, data_type, header, data, retract=0):
    tasks.task_send_director_lo.apply_async((url, detector_id, data_type, header, data), serializer='msgpack')  ####异步发送


# 发送文件至业务系统
def send_business_file(logger_str, flag, device_id, header, file_path, filename, url=config.const.BUSINESS_URL):

    pu.print_format_header('\n发送文件到业务系统')
    try:
        # logger = logging.getLogger(logger_str)
        if config.const.OBTAIN_AUTH_KEY:
            print '获取业务系统授权Key'
            header['Authorization'] = common.get_auth_key()
            print 'Authorization_Key:', header['Authorization']
        header['Connection'] = 'keep-alive'  # 长连接
        boundary = '---------------------------' + (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(6))))[0:10]
        header['Content-Type'] = 'multipart/form-data;boundary=' + boundary
        files = MultipartEncoder(
            fields={
                "file": (filename, open(file_path, "rb"), "multipart/form-data")  # 文件流
            },
            boundary=boundary
        )  # 文件实体对象

        print 'header:', pu.pretty_print_format(header)
        print '发送%s数据到业务系统' % flag
        r = requests.post(url, headers=header, data=files)
        # r = requests.post(url, headers=header, files={'file': (filename, open(file_path, "rb"))})
        # pu.print_with_retract(r.status_code, retract + 1)  # 响应码
        pu.print_with_retract(r.headers,  1)  # 响应头
        pu.print_with_retract(r.text.encode('utf-8'), 1)  # 响应消息正文

        log_str = '%s %s %d %s' % (device_id, flag, r.status_code, r.text.encode('utf-8'))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_business/', prefix='send_business.', suffix='log')
    except Exception:
        traceback.print_exc()
        log_str = '%s %s %s' % (device_id, flag, 'send_exception')
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_business/', prefix='send_business.', suffix='log')

    pu.print_format_tail('发送文件到业务系统\n')


# 发送数据至业务系统
def send_business_data(logger_str, flag, device_id, send_data, url=config.const.BUSINESS_URL):

    pu.print_format_header('\n发送json数据到业务系统')

    try:
        # logger = logging.getLogger(logger_str)
        for d in send_data:
            send_header = d[0]
            if config.const.OBTAIN_AUTH_KEY:
                print '获取业务系统授权Key'
                send_header['Authorization'] = common.get_auth_key()
                print 'Authorization_Key:', send_header['Authorization']
            # send_header['Authorization'] = '96f9047831be4bb8a2bbd1417f58e94b'
            # send_header['Connection'] = 'keep-alive'

            print 'header:', pu.pretty_print_format(send_header), '\ndata:', d[1]
            print '发送%s数据到业务系统' % flag
            r = requests.post(url, headers=send_header, data=json.dumps(d[1]))
            # pu.print_with_retract(r.status_code, retract + 1)  # 响应码
            pu.print_with_retract(r.headers, 1)  # 响应头
            pu.print_with_retract(r.text.encode('utf-8'), 1)  # 响应消息正文

            log_str = '%s %s %d %s' % (device_id, flag, r.status_code, r.text.encode('utf-8'))
            fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_business/', prefix='send_business.', suffix='log')
    except Exception:
        traceback.print_exc()
        log_str = '%s %s %s' % (device_id, flag, 'send_exception')
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_business/', prefix='send_business.', suffix='log')

    pu.print_format_tail('发送json数据到业务系统\n')


def async_send_business_file(logger_str, flag, device_id, header, file_path, filename, url=config.const.BUSINESS_URL):
    tasks.task_send_business_file.apply_async((logger_str, flag, device_id, header, file_path, filename, url), serializer='msgpack')  ####异步发送


def async_send_business_data(logger_str, flag, device_id, send_data, url=config.const.BUSINESS_URL):
    tasks.task_send_business_data.apply_async((logger_str, flag, device_id, send_data, url), serializer='msgpack')  ####异步发送


# 发送至ES
# 读取gzip文件，取出通联关系数据，发送至url（一次不超过5000条）
# 文件不是gzip压缩格式，则返回False，否则返回True
def send_es_net_log(request_id, url, file_path, detector_id):

    pu.print_format_header('\n发送通联关系审计数据到ES服务器')

    # logger_net_log = logging.getLogger('project.net_log')
    print '文件路径: ', file_path.encode('utf-8')
    query_data = AuditLog.objects.filter(request_id=request_id)  # 查询数据
    query_data.update(start_process_time=du.get_current_time())   # 修改开始处理时间
    net_data = ''
    data_count = 0
    gzip_f = gzip.GzipFile(mode='rb', fileobj=open(file_path, 'rb'))
    try:
        for line in gzip_f:   # 对于大文件速度比较快，Python虚拟机在内部对buffer进行管理，内存占用量小
            net_data += line
            data_count += 1
            # logger_net_log.info(detector_id + '---process line: ' + str(data_count))
            if data_count == 5000:
                print '开始发送数据'
                r = requests.post(url, data={'data': net_data.strip().replace('\n', '~=~')})
                # pu.print_with_retract(r.status_code, retract + 1)  # 响应码
                pu.print_with_retract(r.headers, 1)  # 响应头
                pu.print_with_retract(r.text.encode('utf-8'), 1)  # 响应消息正文

                log_str = '%s %s %d %s' % (detector_id, "net_log", r.status_code, r.text.encode('utf-8'))
                fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_es/', prefix='send_es.', suffix='log')
                if r.status_code == 200:
                    resp_result = json.loads(r.text.encode('utf-8'))
                    if resp_result['code'] == 1:   # ES数据执行失败
                        gzip_f.close()
                        # 修改结束处理时间和处理状态
                        query_data.update(end_process_time=du.get_current_time(), process_status=1)
                        return False
                else:
                    gzip_f.close()
                    # 修改结束处理时间和处理状态
                    query_data.update(end_process_time=du.get_current_time(), process_status=1)
                    return False
                data_count = 0
                net_data = ''
        if data_count != 0:    # 处理剩余的不足5000条的数据
            print '开始发送数据'
            r = requests.post(url, data={'data': net_data.strip().replace('\n', '~=~')})
            # pu.print_with_retract(r.status_code, retract + 1)  # 响应码
            pu.print_with_retract(r.headers, 1)  # 响应头
            pu.print_with_retract(r.text.encode('utf-8'), 1)  # 响应消息正文

            log_str = '%s %s %d %s' % (detector_id, "net_log", r.status_code, r.text.encode('utf-8'))
            fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_es/', prefix='send_es.', suffix='log')
            if r.status_code == 200:
                resp_result = json.loads(r.text.encode('utf-8'))
                if resp_result['code'] == 1:  # ES数据执行失败
                    gzip_f.close()
                    # 修改结束处理时间和处理状态
                    query_data.update(end_process_time=du.get_current_time(), process_status=1)
                    return False
            else:
                gzip_f.close()
                # 修改结束处理时间和处理状态
                query_data.update(end_process_time=du.get_current_time(), process_status=1)
                return False
        gzip_f.close()
        # logger_net_log.error('normally end thread!')
        # 修改结束处理时间和处理状态
        query_data.update(end_process_time=du.get_current_time(), process_status=0)

        pu.print_format_tail('发送通联关系审计数据到ES服务器\n')
        return True
    except IOError:
        gzip_f.close()
        log_str = '%s %s %s' % (detector_id, 'net_log', 'send_exception')
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_es/', prefix='send_es.', suffix='log')
        # 修改结束处理时间和处理状态
        query_data.update(end_process_time=du.get_current_time(), process_status=1)
        return False


def async_send_es_net_log(request_id, url, file_path, detector_id):
    tasks.task_send_es_net_log.apply_async((request_id, url, file_path, detector_id), serializer='msgpack')  ####异步发送


def send_app_behavior(request_id, url, file_path, detector_id):

    pu.print_format_header('\n发送应用行为审计数据到ES服务器')

    # logger_app_behavior = logging.getLogger('project.app_behavior')
    print '文件路径: ', file_path.encode('utf-8')
    query_data = AuditLog.objects.filter(request_id=request_id)  # 查询数据
    query_data.update(start_process_time=du.get_current_time())  # 修改开始处理时间
    gzip_f = gzip.GzipFile(mode='rb', fileobj=open(file_path, 'rb'))
    try:
        try:
            data = gzip_f.read().decode('utf-8-sig').encode('utf-8')  # 将含有BOM的utf-8转为不含BOM的utf-8
        except UnicodeDecodeError:
            data = gzip_f.read()
        print '开始发送数据'
        r = requests.post(url, data={'data': data})  # 发送数据到ES服务器
        # pu.print_with_retract(r.status_code, retract + 1)  # 响应码
        pu.print_with_retract(r.headers, 1)  # 响应头
        pu.print_with_retract(r.text.encode('utf-8'), 1)  # 响应消息正文

        log_str = '%s %s %d %s' % (detector_id, 'app_behavior', r.status_code, r.text.encode('utf-8'))
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_es/', prefix='send_es.', suffix='log')
        if r.status_code == 200:
            resp_result = json.loads(r.text.encode('utf-8'))
            if resp_result['code'] == 1:  # ES数据执行失败
                gzip_f.close()
                # 修改结束处理时间和处理状态
                query_data.update(end_process_time=du.get_current_time(), process_status=1)
                return False
            else:
                gzip_f.close()
                # 修改结束处理时间和处理状态
                query_data.update(end_process_time=du.get_current_time(), process_status=0)
                return True
        else:
            gzip_f.close()
            # 修改结束处理时间和处理状态
            query_data.update(end_process_time=du.get_current_time(), process_status=1)

            pu.print_format_header('发送应用行为审计数据到ES服务器\n')
            return False
    except IOError:
        gzip_f.close()
        log_str = '%s %s %s' % (detector_id, 'app_behavior', 'send_exception')
        fu.string2log_append_per_day(content=log_str, path=common.LOG_PATH + 'send_es/', prefix='send_es.', suffix='log')
        # 修改结束处理时间和处理状态
        query_data.update(end_process_time=du.get_current_time(), process_status=1)
        return False


def async_send_app_behavior(request_id, url, file_path, detector_id):
    tasks.task_send_es_app_behavior.apply_async((request_id, url, file_path, detector_id), serializer='msgpack')  ####异步发送


# 从指挥指挥中心下载文件
def download_file_from_director(url, sub_function_path, file_name):
    """
    从指挥指挥中心下载文件,返回文件存储路径
    :param url:                 下载文件请求url
    :param sub_function_path:   功能子目录，如'plugin'、'command'
    :param file_name:           原始文件名，用于获取文件后缀
    :return:
    """
    try:
        result_path = ''
        pu.print_format_header('从指挥中心下载文件')

        cookies = check_director_cookies()
        header = {
            'X-Forwarded-For': director_config.detect_center_host,
        }
        r = requests.get(url, headers=header, cookies=cookies)
        # r = post(session, send_url_A, headers=f_header, data=files)
        print r.status_code  # 响应码
        print r.headers  # 响应头
        content_len = len(r.content)
        print content_len
        if r.status_code == 200:
            rename_file_name = common.rename_file() + os.path.splitext(file_name)[1]
            relative_path = sub_function_path + fu.get_sub_dir(2)
            file_path = common.MEDIA_ROOT + relative_path
            if fu.handle_download_file(file_path, r, rename_file_name):
                result_path = relative_path + rename_file_name
        pu.print_format_tail('从指挥中心下载文件')
        return result_path
    except Exception:
        traceback.print_exc()
        return ''


def send_business_disposal(file_dir, file_name, user_agent, handle_data_type, handle_data):

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path = os.path.join(file_dir, file_name)
    with open(file_path, 'wb') as f_handler:
        f_handler.write(config.const.DISPOSAL_BOUNDARY + '\n')
        f_handler.write('User-Agent:' + user_agent + '\n')
        f_handler.write('Type:' + handle_data_type + '\n')
        f_handler.write(json.dumps(handle_data))


def async_send_business_disposal(file_dir, file_name, user_agent, handle_data_type, handle_data):
    tasks.task_send_business_disposal.apply_async((file_dir, file_name, user_agent, handle_data_type, handle_data), serializer='msgpack')

# def async_download_plug_file_from_director(sub_function_path, plug_list, director_down_header={}, is_down_plug_file_list=[]):
#     tasks.task_download_plug_file_from_director.apply_async((sub_function_path, plug_list, director_down_header, is_down_plug_file_list), serializer='msgpack')  ####异步发送