# -*- coding:utf-8 -*-

from rest_framework.response import Response
from rest_framework import status
from settings import BASE_DIR, REST_FRAMEWORK
import datetime
import time
import re
import os
import hashlib
import snowflake
import requests
import json
import base64
import traceback
import random
import config

from django.http import HttpResponse
from django.db import connection

from DetectCenter import date_util as du, file_util as fu, security_util as su, print_util as pu
from DetectCenter.director_config import *
# 检测器上传文件存放的根目录
MEDIA_ROOT = BASE_DIR + '/media/'
LOG_PATH = BASE_DIR + '/log/'


# 密码过期时间
EXPIRE_TIME = datetime.timedelta(days=30)


# 进程锁
# lock = multiprocessing.Lock()

# 获取authKey
# def get_auth_key2():
    # lock.acquire()
    # try:
        # r_auth = requests.post(AUTH_URL, data={'uid': test_uid, 'password': test_pwd})
        # if r_auth.status_code == status.HTTP_200_OK:
            # return r_auth.json()['data']['authKey'].encode('utf-8')
        # else:
            # return None
    # finally:
        # lock.release()


# 获取authKey
def get_auth_key(url=config.const.AUTH_URL):
    r_auth = requests.post(url, data={'uid': config.const.AUTH_UID, 'password': config.const.AUTH_PWD})
    if r_auth.status_code == status.HTTP_200_OK:
        return r_auth.json()['data']['authKey'].encode('utf-8')
    else:
        return None


# 响应头的通用字段
RESPONSE_HEADER = {
    "Server": "IIE CAS",
    # "Date": datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
}

# 地址编码
ADDRESS = {
    '100000': '北京',
    '200000': '上海',
    '510000': '广州'
}

# 厂商列表
contractor_dict = {
    '01': '中孚',
    '02': '蓝盾',
    '03': '天融信',
    '04': '鼎普',
    '05': '网安',
    '06': '信工所',
    '07': '未知'
}

# 检测器接入状态
DETECTOR_STATUS = {
    'normal':             1,          # 正常运行 ,
    'register_no_check':  2,          # 注册未审核
    'register_fail':      3,          # 注册失败
    'register_success':   4,          # 注册成功
    'auth_fail':          5,          # 认证失败
    'forbidden':          6,          # 禁用(该状态不通过device_status字段入库，通过is_effective入库)
}

# 告警模块
WARN_MODULE = {
    'alarm':              1,          # 攻击窃密
    'abnormal':           2,          # 异常行为
    'sensitive':          3,          # 违规泄密
    'object_listen':      4,          # 目标帧听
    # 'net_audit':          5           # 网络行为审计
    'block':              5,          # 阻断告警
}

# 告警类型
WARN_TYPE = {
    'trojan':                 1,      # 木马攻击窃密
    'attack':                 2,      # 漏洞利用窃密
    'malware':                3,      # 恶意程序窃密
    'other':                  4,      # 其他攻击窃密
    'abnormal':               5,      # 未知攻击窃密
    'sensitive_email':        6,      # 违规泄密——电子邮件协议
    'sensitive_im':           7,      # 违规泄密——即时通信协议
    'sensitive_filetransfer': 8,      # 违规泄密——文件传输协议
    'sensitive_http':         9,      # 违规泄密——网页发布协议
    'sensitive_netdisk':      10,     # 违规泄密——网盘协议
    'sensitive_other':        11,     # 违规泄密——其他协议
    'intercept_ip':           12,     # IP侦听
    'intercept_dns':          13,     # 域名帧听
    'intercept_url':          14,     # URL侦听
    'intercept_account':      15,     # 账号侦听
    'block':                  16      # 阻断告警
}


# 前端检测器业务数据类型

SOURCE_TYPE = {
    'alarm': 'JCQ_GJQM',   # 包含了未知攻击
    'sensitive': 'JCQ_CSSM',
    'object_listen': 'JCQ_MBSJ',
    'block': 'JCQ_TXZD'
}


BUSINESS_TYPE = [
    'BUSINESS_TYPE',               # 业务类型
    'JCQ_GJQM_TROJAN',             # 木马攻击窃密检测
    'JCQ_GJQM_ATTACK',             # 漏洞利用检测
    'JCQ_GJQM_MALWARE',            # 恶意程序检测
    'JCQ_GJQM_OTHER',              # 其他攻击窃密检测
    'JCQ_GJQM_ABNORMAL',           # 未知攻击窃密检测
    'JCQ_CSSM_MB',                 # 密标文件检测
    'JCQ_CSSM_SENSITIVE',          # 标密文件检测（暂时没有）
    'JCQ_CSSM_KEYWORD',            # 关键词检测
    'JCQ_CSSM_FILTEREDENC',        # 加密检测
    'JCQ_CSSM_FILTEREDCOM',        # 压缩检测
    'JCQ_CSSM_FILTEREDPIC',        # 图文筛选
    'JCQ_CSSM_LAYOUT',             # 版式检测
    'JCQ_MBSJ_IP',                 # IP审计
    'JCQ_MBSJ_DOMAIN',             # 域名审计
    'JCQ_MBSJ_URL',                # URL审计
    'JCQ_MBSJ_ACCOUNT',            # 账号审计
    'JCQ_TXZD_BLOCK',              # 通信阻断告警
    'JCQ_XWSJ_NETLOG_FILE',        # 通联关系审计
    'JCQ_XWSJ_APPBEHAVIOR_FILE'    # 应用行为审计
]

# 上传到指挥中心的策略类型
COMMAND_POLICY_TYPE = [
    'CENTER_POLICY_TROJAN',         # 木马攻击检测策略
    'CENTER_POLICY_ATTACK',         # 漏洞利用检测策略
    'CENTER_POLICY_MALWARE',        # 恶意文件检测策略
    'CENTER_POLICY_ABNORMAL',       # 未知攻击检测策略
    'CENTER_POLICY_KEYWORD',        # 关键词策略
    'CENTER_POLICY_ENCRYPTION',     # 加密文件筛选策略
    'CENTER_POLICY_COMPRESS',       # 压缩文件检测策略
    'CENTER_POLICY_PICTURE',        # 图片文件筛选策略
    'CENTER_POLICY_IPLISTEN',       # IP审计策略
    'CENTER_POLICY_DNSLISTEN',      # 域名审计策略
    'CENTER_POLICY_URLLISTEN',      # url审计策略
    'CENTER_POLICY_ACCOUNTLISTEN',  # 账号审计策略
    'CENTER_POLICY_NETLOG',         # 通联关系审计结果上传策略
    'CENTER_POLICY_APPBEHAVIOR',    # 应用行为审计结果上传策略
    'CENTER_POLICY_WEBFILTER',      # web访问审计白名单
    'CENTER_POLICY_DNSFILTER',      # dns访问审计白名单
    'CENTER_POLICY_IPWHITELIST',    # IP白名单策略
    'CENTER_POLICY_BLOCK'           # 通信阻断策略
]

# 指挥中心下发的策略类型
DIRECTOR_POLICY_TYPE = [
    'DIRECTOR_POLICY_TROJAN',         # 木马攻击检测策略
    'DIRECTOR_POLICY_ATTACK',         # 漏洞利用检测策略
    'DIRECTOR_POLICY_MALWARE',        # 恶意文件检测策略
    'DIRECTOR_POLICY_ABNORMAL',       # 未知攻击检测策略
    'DIRECTOR_POLICY_KEYWORD',        # 关键词策略
    'DIRECTOR_POLICY_ENCRYPTION',     # 加密文件筛选策略
    'DIRECTOR_POLICY_COMPRESS',       # 压缩文件检测策略
    'DIRECTOR_POLICY_PICTURE',        # 图片文件筛选策略
    'DIRECTOR_POLICY_IPLISTEN',       # IP审计策略
    'DIRECTOR_POLICY_DNSLISTEN',      # 域名审计策略
    'DIRECTOR_POLICY_URLLISTEN',      # url审计策略
    'DIRECTOR_POLICY_ACCOUNTLISTEN',  # 账号审计策略
    'DIRECTOR_POLICY_NETLOG',         # 通联关系审计结果上传策略
    'DIRECTOR_POLICY_APPBEHAVIOR',    # 应用行为审计结果上传策略
    'DIRECTOR_POLICY_WEBFILTER',      # web访问审计白名单
    'DIRECTOR_POLICY_DNSFILTER',      # dns访问审计白名单
    'DIRECTOR_POLICY_IPWHITELIST',    # IP白名单策略
    'DIRECTOR_POLICY_BLOCK'           # 通信阻断策略
]


module_status = ['alarm_status', 'abnormal_status', 'sensitive_status',
                 'object_listen_status', 'net_audit_status', 'block_status']  # 模块状态名

# 子模块名
module_names = [
    'trojan', 'attack', 'malware', 'abnormal', 'keyword_file', 'encryption_file', 'compress_file',
    'picture_file', 'ip_listen', 'domain_listen', 'url_listen', 'account_listen', 'net_log',
    'app_behavior', 'web_filter', 'dns_filter', 'ip_whitelist', 'block']  # 模块名

module_fields = [module + '_type' for module in module_names]  # Detector model中的模块类型，决定是否下发策略

cmd_names = ['shutdown', 'reboot', 'startm', 'stopm', 'sync_time', 'update', 'version_check',
             'inner_policy_update', 'passwd']  # 命令类型

#
# # 监测策略对应的模块
# POLICY_TYPE = {
#     'trojan':           1,    # 木马攻击监测策略
#     'attack':           2,    # 漏洞利用监测策略
#     'pefile':           3,    # 恶意程序监测策略
#     'abnormal':         4,    # 异常行为上报策略
#     'sensitive_file':   5,    # 内容监测策略
#     'compress_file':    6,    # 压缩文件监测策略
#     'picture_file':     7,    # 图片筛选回传策略
#     'ip_listen':        8,    # IP侦听监测策略
#     'domain_listen':    9,    # 域名侦听监测策略
#     'url_listen':       10,   # URL侦听监测策略
#     'account_listen':   11,   # 帐号侦听监测策略
#     'net_log':          12,   # 通联关系监测策略
#     'active_ip':        13,   # 活跃IP监测策略
#     'flow_stats':       14,   # 协议流量监测策略
#     'app_behavior':     15,   # 应用行为监测策略
#     'web_filter':       16,   # 应用行为web过滤策略
#     'dns_filter':       17    # 应用行为DNS过滤策略
# }
POLICY_TYPE = [u'木马规则', u'漏洞利用规则', u'恶意文件规则', u'未知攻击文件上传规则', u'关键词规则', u'加密文件筛选规则', u'压缩文件规则', u'图文文件筛选规则', u'IP审计规则', u'DNS审计规则', u'URL审计规则', u'账号审计规则', u'通联关系上传规则', u'应用行为上传规则', u'web过滤规则', u'DNS过滤规则', u'IP白名单过滤规则', u'阻断规则']
COMMAND_TYPE = [u'关机',u'重启', u'模块启动', u'模块停止', u'时间同步', u'系统固件升级', u'版本一致性检查', u'内置策略更新', u'本地WEB管理用户密码重置']

# 上传到指挥中心定义的日志记录规则类型
COMMAND_RULE_TYPE = [
    'rule_trojan',         # 木马攻击检测规则
    'rule_attack',         # 漏洞利用检测规则
    'rule_malware',        # 恶意文件检测规则
    'rule_abnormal',       # 未知攻击检测规则
    'rule_keyword',        # 关键词规则
    'rule_encryption',     # 加密文件筛选规则
    'rule_compress',       # 压缩文件检测规则
    'rule_picture',        # 图片文件筛选规则
    'rule_iplisten',       # IP审计规则
    'rule_domainlisten',   # 域名审计规则
    'rule_urllisten',      # url审计规则
    'rule_accountlisten',  # 账号审计规则
    'rule_netlog',         # 通联关系审计结果上传规则
    'rule_appbehavior',    # 应用行为审计结果上传规则
    'rule_webfilter',      # web访问审计白名单规则
    'rule_dnsfilter',      # dns访问审计白名单规则
    'rule_ipwhitelist',    # IP白名单规则
    'rule_block',          # 通信阻断规则
]


def cal_task_version(models, device_id, task_type_str, task_type='1'):
    """
    计算要生成任务的版本号
    :param models:              对应的任务表
    :param device_id:           要生成任务的检测器ID
    :param task_type_str:       生成任务的类型， 'policy', 'plugin', 'command'
    :param task_type:           生成任务序列号中标识任务类别，1: 'policy', 2: 'plugin', 3: 'command'
    :return:
    """
    with connection.cursor() as cursor:  # 运行mysql函数,生成版本号
        cursor.execute('select nextversion(%s,%s)', (task_type_str, task_type))  # 参数是一个元组
        version_num = get_task_serial(cursor.fetchone()[0])
    last_task_list = []
    for model in models:
        task_info = model.objects.filter(device_id=device_id).order_by('-id')
        if task_info.exists():
            last_task_list.append(task_info[0])
    if last_task_list:
        last_task = last_task_list[0]
        for task in last_task_list:
            if task.generate_time > last_task.generate_time:
                last_task = task
        last_version_num = last_task.version
        import math
        version_num = version_num + '.' + str(int(math.fabs(int(version_num.split('.')[-1]) - int(last_version_num.split('.')[-2]))))
    else:
        version_num = version_num + '.0'
    return version_num


def print_with_retract(print_data, retract=0):
    """
    带缩进（tab）打印
    :param print_data:     要打印的数据
    :param retract:    需要缩进的tab数量
    :return:
    """
    if retract != 0:
        tab = ""
        for i in range(retract):
            tab += "    "
        print tab, print_data
    else:
        print print_data


def check_center_director_rule_is_equal(rule, policy_type, compare_model):
    """
    检验管理中心和指挥中心下发的策略是否相同
    :param rule:              下发的策略
    :param policy_type:       策略种类，用于获取需要比较的字段, 从1开始
    :param compare_model:     查询的的model
    :return:                  重复的rule_id List(主键ID)
    """
    if policy_type == 1:  # 木马攻击检测
        result_set = ('trojan_id', 'store_pcap', 'os', 'trojan_name', 'trojan_type', 'desc', 'rule', 'risk')
    elif policy_type == 2:  # 漏洞利用检测
        result_set = ('store_pcap', 'rule', 'attack_type', 'application', 'os', 'risk')
    elif policy_type == 3:  # 恶意程序检测
        result_set = ('md5', 'signature', 'malware_type', 'malware_name', 'risk')
    elif policy_type == 4:  # 未知攻击窃密检测文件上传
        result_set = ('abn_type', 'allow_file', 'risk_min', 'file_size_limit', 'file_num_hour', 'rate_limit')
    elif policy_type == 5:  # 关键词检测
        result_set = ('rule_type', 'min_match_count', 'rule_content', 'risk')
    elif policy_type == 6:  # 加密文件筛选
        result_set = ('filesize_minsize', 'filesize_maxsize', 'risk')
    elif policy_type == 7:  # 压缩文件检测
        result_set = ('depth', 'backsize', 'dropsize', 'risk')
    elif policy_type == 8:  # 图片筛选回传
        result_set = ('filesize_minsize', 'filesize_maxsize', 'risk')
    elif policy_type == 9:  # IP侦听检测
        result_set = ('sip', 'sport', 'dip', 'dport', 'protocol', 'risk')
    elif policy_type == 10:  # 域名侦听检测
        result_set = ('dns', 'rule_type', 'match_type', 'risk')
    elif policy_type == 11:  # URL侦听检测
        result_set = ('url', 'rule_type', 'match_type', 'risk')
    elif policy_type == 12:  # 账号侦听检测
        result_set = ('account_type', 'account', 'rule_type', 'match_type', 'risk')
    elif policy_type == 13:  # 通联关系上传
        result_set = ('interval', 'num')
    elif policy_type == 14:  # 应用行为上传
        result_set = ('interval', 'num')
    elif policy_type == 15:  # web过滤
        result_set = ('url', 'rule_type', 'match_type')
    elif policy_type == 16:  # dns过滤
        result_set = ('dns', 'rule_type', 'match_type')
    elif policy_type == 17:  # IP白名单策略
        result_set = ('ip', 'port')
    elif policy_type == 18:  # 阻断策略
        result_set = ('sip', 'sport', 'dip', 'dport', 'protocol')
    else:
        result_set = ()

    query_terms = {field: rule.get(field) for field in result_set}
    rule_info = compare_model.objects.filter(**query_terms).filter(is_del=1)
    if rule_info.exists():
        map_id_list = '#' + '#'.join([str(r.rule_id) for r in rule_info]) + '#'
    else:
        map_id_list = ''
    if map_id_list != '':
        print '得到与 %s 类型策略 %s 相同的规则：%s' % (POLICY_TYPE[policy_type - 1], str(rule['rule_id']), map_id_list)
    return map_id_list


def is_serial_id_overflow_errer(errors):
    """
    判断策略、任务组等入库数据中的serialID是否溢出
    :param errors:  rest-framework序列化的异常信息
    :return:
    """
    if errors is None:
        return False
    # print errors
    errors_dict = {}
    if isinstance(errors, dict):
        errors_dict = errors.copy()
    if isinstance(errors, list):
        errors_dict = errors[0]
    tmp = {}
    for k, v in errors_dict.items():
        if len(v) == 1 and str(v[0]).find('9223372036854775807') != -1 and str(v[0]).find('equal') != -1:
            tmp[k] = v
    for k in tmp:
        if k in errors_dict:
            errors_dict.pop(k)
    if len(errors_dict) == 0:
        return True
    else:
        return False


def get_rule_serial(id, serial=CENTER_SERIAL):
    """
    rule serial 生成规则的唯一识别ID
    :param id:          原规则ID号
    :param serial:      管理中心ID号
    :return:
    """
    rule_serial = int(serial)*65536*65536 + id

    return rule_serial


def get_task_serial(id, serial=CENTER_SERIAL):
    """
    task serial 生成任务的唯一识别ID
    :param id:          原任务版本号
    :param serial:      管理中心ID号
    :return:
    """
    task_serial = str(serial) + '.' + str(id)
    return task_serial


# 将后台数据库存储的运行的检测器id 格式 转变成 list格式
def generate_device_ids_list_from_model_str(devices_model_str, all_device_ids_list):
    """
    将后台数据库存储的运行的检测器主键ID 格式 转变成 list格式
    后台存储格式：        ''->空 '#'->全部检测器 '#180306010001#180306010002#'->180306010001/180306010002检测器
    :param devices_model_str:
    :param all_device_ids_list:  全部检测器ID的List
    :return:
    """
    if devices_model_str == '#':
        device_list = all_device_ids_list
    elif devices_model_str == '':
        device_list = []
    else:
        # device_list = map(int, devices_model_str[1:-1].split('#'))
        device_list = map(str, devices_model_str[1:-1].split('#'))
    return device_list


# 将后台数据库存储的运行的检测器id 格式 转变成 界面的list str格式
def generate_device_ids_ui_str_from_model_str(devices_model_str):
    """
    将后台数据库存储的运行的检测器主键ID 格式 转变成 界面的list str格式
    后台存储格式：        ''->空 '#'->全部检测器 '#180306010001#180306010002#'->180306010001/180306010002检测器
    界面的List str格式：  '[0]'->空 '[]'->全部检测器 '[180306010001, 180306010002]'->180306010001/180306010002检测器
    :param devices_model_str:
    :return:
    """
    if devices_model_str not in ['', '#']:  # 运行该规则的检测器
        devices_ui_str = json.dumps(
            map(int, devices_model_str[1:-1].split('#')), separators=(',', ':'))
    elif devices_model_str == '':  # 表示空
        devices_ui_str = '[0]'
    else:  # 表示全部
        devices_ui_str = '[]'
    return devices_ui_str


# 接收界面上传文件，返回文件在服务器上的存储路径
def process_upload_file(request, sub_function_dir, time_sub_dir_grading=3):
    try:
        request_data = print_header_data(request)  # 获取请求数据
        sub_time_dir = fu.get_sub_dir(time_sub_dir_grading)
        file_path = MEDIA_ROOT + sub_function_dir + sub_time_dir  # 页面上传文件存放的目录
        if isinstance(request_data, dict):
            request_file = request.FILES.values()
            file_list = []
            for f in request_file:
                file_dict = {}
                extension = os.path.splitext(f.name)[1]  # 文件扩展名
                save_name = rename_ui_upload_file() + extension

                is_success = fu.handle_upload_file(file_path, f, save_name)  # 上传文件
                if not is_success:  # 文件上传失败
                    return ui_message_response(400, '服务器上存在相同的文件:' + f.name.encode('utf-8'),
                                                      f.name.encode('utf-8') + '文件已经上传或者文件命名重复')
                else:
                    file_dict['file_path'] = sub_function_dir + sub_time_dir + save_name
                    file_list.append(file_dict)

            return ui_message_response(200, '文件上传成功', file_list, status.HTTP_200_OK)
        else:
            return ui_message_response(400, '上传的数据不是dict', '上传的数据不是dict')
    except Exception:
        traceback.print_exc()
        return ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 处理界面下载服务器下载
def process_download_file(request, sub_function_name, save_path):
    try:
        print_header_data(request)  # 获取请求数据
        file_path = MEDIA_ROOT + sub_function_name + save_path
        if save_path is None or save_path.strip() == '':
            return ui_message_response(400, '未提交文件路径或提交文件路径为空', '未提交文件路径或提交文件路径为空')
        path_list = save_path.split('/')
        path_list.reverse()
        filename = path_list[0]

        # print filename

        return construct_download_file_header(file_path, sub_function_name + save_path, filename)
    except Exception:
        traceback.print_exc()
        return ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


# 通用处理界面下载服务器下载，上传文件存储的相对路径
def process_download_file1(request):
    try:
        request_data = print_header_data(request)  # 获取请求数据
        save_path = request_data.get('path')
        file_path = MEDIA_ROOT + save_path
        if file_path is None or file_path.strip() == '':
            return ui_message_response(400, '未提交文件路径或提交文件路径为空', '未提交文件路径或提交文件路径为空')
        path_list = save_path.split('/')
        path_list.reverse()
        filename = path_list[0]

        # print filename

        return construct_download_file_header(file_path, save_path, filename)
    except Exception:
        traceback.print_exc()
        return ui_message_response(500, '服务器内部错误', '服务器内部错误',
                                          status.HTTP_500_INTERNAL_SERVER_ERROR)


def check_request_list_or_dict_field(request_data, print_name):
    """
    校验请求中的List或者dict类型参数
    :param request_data:     请求参数数据
    :param print_name:       请求中对应的字段名
    :return:                 参数数据或者错误信息
    """
    param = request_data.get(print_name)
    if param is not None:  # 请求参数中有print_name（字符串，json解析后是list或者dict）
        try:
            param = json.loads(param)
            if not isinstance(param, (list, dict)):
                return ui_message_response(400, '请求参数{0}的不是list或者dict类型'.format(print_name), '请求参数{0}的不是list或者dict类型'.format(print_name))
            else:
                return param
        except:
            traceback.print_exc()
            return ui_message_response(400, '请求参数{0}的Json解析失败'.format(print_name), '请求参数{0}的Json解析失败'.format(print_name))
    else:
        return ui_message_response(400, '请求url中没有携带参数{0}'.format(print_name), '请求参数没有{0}'.format(print_name))


def check_request_int_field(request_data, print_name):
    """
    校验请求中的int类型参数
    :param request_data:   请求参数数据
    :param print_name:     请求中对应的字段名
    :return:               参数数据或者错误信息
    """
    field = request_data.get(print_name)
    if field is not None:  # 请求参数中有type
        try:
            return int(field)
        except Exception:
            return ui_message_response(400, '请求参数{0}的值不是数字'.format(print_name), '请求参数{0}格式不正确'.format(print_name))
    else:
        return ui_message_response(400, '请求url中没有携带参数{0}'.format(print_name), '请求参数没有{0}'.format(print_name))


def check_detector_upload_header_filedesc_field(data):
    """
    对前端检测器的上传的文件校验Content-Filedesc字段
    :param data:   Content-Filedesc字段数据
    :return:
    """
    if data is None:
        return detector_message_response(400, '请求头中没有Content-Filedesc字段', '请求头中没有Content-Filedesc字段')
    else:
        try:
            data = json.loads(data)
        except ValueError:
            return detector_message_response(400, '文件描述请求头Content-Filedesc不是json类型',
                                                    '文件描述请求头不符合json格式')
        return data


def check_time_field(data):
    """
    格式化上传数据中的time字段
    :param data:
    :return:
    """
    if 'time' in data:  # 将数据中字符串表示的时间转变为时间类型
        try:
            data['time'] = datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
        except Exception:
            return detector_message_response(400, '请求数据中的time字段值不符合yyyy-MM-dd HH:mm:ss的格式',
                                                    '请求数据中的time字段值不符合yyyy-MM-dd HH:mm:ss的格式')
    else:
        return detector_message_response(400, '请求数据中没有time字段', '请求数据中没有time字段')


def construct_download_file_header(abs_path, save_path, file_name, cal_md5=False, static_relative_path="/media/"):
    """
    构造从管理中心下载文件的响应头
    :param abs_path:   文件在服务器的绝对路径
    :param save_path:  文件相对与项目static_relative_path存储的相对路径
    :param file_name:  文件名
    :param cal_md5:    是否计算文件的MD5校验值
    :return:           请求响应，主要包括响应头
    """
    response = HttpResponse()
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Length'] = os.path.getsize(abs_path)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name.encode('utf-8'))
    response['X-Accel-Redirect'] = '{0}'.format((static_relative_path + save_path).encode('utf-8'))  # 支持断点续传
    if cal_md5:
        response['x-md5'] = su.calc_md5(abs_path)
    return response


def check_detector_available(request, detector_model):
    """
    检查检测器的合法性，包括是否认证和是否存在和是否被禁用
    :param request:      网络请求
    :param detector_model:  设备model
    :return:             如果检测器所有信息都合法就返回检测器ID，否则返回校验信息给前端检测器
    """
    detector_id = get_detector_id(request)  # 获取检测器ID
    if not isinstance(detector_id, basestring):  # basestring是str和unicode的超类
        return detector_id  # 返回响应信息

    if detector_id not in request.session:  # 通过session验证检测器是否认证
        return detector_message_response(403, '检测器没有认证', '检测器没有认证', status.HTTP_403_FORBIDDEN)

    detector_info = detector_model.objects.filter(device_id=detector_id)
    if not detector_info.exists():
        return detector_message_response(403, '检测器不存在', '检测器不存在', status.HTTP_403_FORBIDDEN)

    is_effective = detector_info[0].is_effective
    if not is_effective:
        return detector_message_response(403, '该检测器已禁用', '服务器禁用了该检测器',
                                                status.HTTP_403_FORBIDDEN)
    return detector_id


def detector_upload_json_preprocess(request_data):
    """
    针对前端检测器上传的json数据进行简单的合法性检查
    :param request_data:  上传的请求数据
    :return:              List()格式数据
    """
    data_list = []
    if not isinstance(request_data, (dict, list)):  # 判断请求数据类型是否合规
        return detector_message_response(400, '请求数据不是dict，也不是list',
                                                '插件状态数据不是可序列化数据')
    elif isinstance(request_data, dict):  # dict类型数据
        data_list.append(request_data.copy())  # request_data是 immutable QueryDict 对象，需要转变
    else:  # list类型数据
        data_list = request_data
    return data_list


def detector_message_response(code, log_message, message, status_code=status.HTTP_400_BAD_REQUEST,
                              headers=RESPONSE_HEADER):
    """
    自定义前端检测器消息响应.

    :param code:               响应消息编码（自定义）
    :param log_message:        日志信息（开发者查看）
    :param message:            响应信息（前端监测器查看）
    :param status_code:        HTTP响应状态码
    :param headers:            响应头
    :return:                   a REST framework's Response object
    """
    # resp_data = {
    #     'type': code,
    #     'message': message
    # }

    # print '##################', message

    if status_code != status.HTTP_200_OK:
        resp_data = {'message': message}
        print '[ Error ] %d: %s(%d)' % (code, log_message, status_code)
    else:
        resp_data = message
        print '[ Success ] %d: %s(%d)' % (code, log_message, status_code)

    return Response(resp_data, status_code, headers=headers)


def ui_message_response(code, log_message, message, status_code=status.HTTP_400_BAD_REQUEST,
                        headers=RESPONSE_HEADER, retract=0):
    """
    自定义UI响应消息.

    :param code:               响应消息编码（自定义）
    :param log_message:        日志信息（开发者查看）
    :param message:            响应信息（请求用户查看）
    :param status_code:        响应状态码
    :param headers:            响应头
    :param retract:            打印控制台缩进数，以"tab"为单位
    :return:                   a REST framework's Response object
    """
    resp_data = {
        'code': code,
        'msg': message
    }
    if status_code != status.HTTP_200_OK:
        print_with_retract('[ Error ] %d: %s(%d)' % (code, log_message, status_code))
    else:
        print_with_retract('[ Success ] %d: %s(%d)' % (code, log_message, status_code))
    return Response(resp_data, status_code, headers=headers, content_type='application/json;charset=utf-8')


def is_valid_user_agent(user_agent):
    """
    检验User_Agent是否符合要求.
    User_Agent的标准：device_id/soft_version(vendor_name).其中，
    device_id：     12位数字的字符串；
    soft_version：  不超过32位的字符串，其前8位是表示日期的数字，第9位是下划线；
    vendor_name：   不超过32位的字符串
    """
    if isinstance(user_agent, basestring):
        m = re.match(r'\d{12}[/]\d{8}[_].{0,23}[(].{0,32}[)]', user_agent)
        if str(m) != 'None':
            try:
                time.strptime(user_agent[13:21], '%Y%m%d')
                return True
            except Exception:
                return False
        else:
            return False
    else:
        return False


def get_detector_id(request):
    """
    判断并获取请求头中的检测器ID
    """
    user_agent = request.META.get('HTTP_USER_AGENT')   # 请求头中的User-Agent
    if user_agent is None:
        return detector_message_response(400, '请求头中没有User-Agent字段', '请求头中没有User-Agent字段')
    elif not is_valid_user_agent(user_agent):
        return detector_message_response(400, '请求头中的User_Agent字段不符合要求',
                                         '请求头中的User_Agent字段不符合要求')
    else:
        detector_id = user_agent[0:12]
        if detector_id[4:6] not in contractor_dict or detector_id[6:8] != '01':
            return detector_message_response(400, '请求头中的User_Agent字段不符合要求', '请求头中的User_Agent字段不符合要求')
        return detector_id   # 从User-Agent中提取检测器ID并返回


# 重命名：检测器id + '_' + 全局唯一ID + '_' + 文件名
def rename_detector_upload_file(detector_id, file_name):
    # save_file_name = detector_id + '_' + str(snowflake.next_id(2, 0)) + '_' + file_name
    save_file_name = detector_id + '_' + str(snowflake.next_id(2, 0)) + os.path.splitext(file_name)[1]
    return save_file_name


# 重命名管理中心上传的文件 %Y%m%d%H%M%S_ + (100000, 999999)
def rename_ui_upload_file():
    return time.strftime('%Y%m%d%H%M%S_', time.localtime()) + str(random.randint(100000, 999999))


# 重命名的文件 %Y%m%d%H%M%S_ + (100000, 999999)
def rename_file():
    return time.strftime('%Y%m%d%H%M%S_', time.localtime()) + str(random.randint(100000, 999999))

from DetectCenter.settings import DEBUG
# 打印请求头（middleware.py已打印请求头）和请求数据，返回请求数据，如果是非DEBUG模式则不打印数据
def print_header_data(request):
    request_meta = request.META
    # if 'HTTP_USER_AGENT' in request_meta and request_meta['HTTP_USER_AGENT'].split('/')[0] in ['170502010002', '170502010003']: # 蓝盾Cookie太长，暂时性策略
        # if 'HTTP_COOKIE' in request_meta:
            # request_meta.pop('HTTP_COOKIE')
        # print 'header :', request_meta
    # else:
        # print 'header :', request_meta
    # print 'header :', request_meta

    request_data = ''
    if request.method == 'GET':
        if DEBUG:
            print 'get->request_data: ', pu.pretty_print_format(request.GET)
        request_data = request.GET
    elif request.method == 'POST':
        try:
            if request_meta['CONTENT_TYPE'].find('multipart/form-data;') >= 0:
                if DEBUG:
                    print 'post->request_data: ', request.data
            else:
                if DEBUG:
                    print 'post->request_data: ', pu.pretty_print_format(request.data)
        except:
            # traceback.print_exc()
            if DEBUG:
                print 'post->request_data: ', request.data
        request_data = request.data

    return request_data


# 获取界面显示每页起始条目和每页条数
def get_page_data(request_data):
    page_num = int(request_data.get('pn', 1))                                 # 页码，默认为第一页
    page_size = int(request_data.get('p_size', REST_FRAMEWORK['PAGE_SIZE']))  # 每页条数，默认为预设值

    start_pos = (page_num - 1) * page_size                                    # 每页起始条码
    end_pos = page_num * page_size                                            # 每页结束条码

    return start_pos, end_pos, page_size

    
def generate_system_log(request_data, event_type, opt_type, message):
    from audit.audit_serializers import AuditManagementSerializer
    audit_log = {
        'log_id': str(snowflake.next_id(3, 3)),
        'user': request_data.get('uuid', ''),
        'time': du.get_current_time(),
        'event_type': event_type,
        'opt_type': opt_type,
        'message': message,
        'is_send_command': 0
    }
    serializer = AuditManagementSerializer(data=audit_log)  # 序列化
    if serializer.is_valid():
        serializer.save()  # 存储数据库

        # 写入文件
        file_dir = os.path.join(config.const.DISPOSAL_DIR, 'audit')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_name = 'center_audit_' + str(int(time.time())) + '_' + str(1)
        file_path = os.path.join(file_dir, file_name)
        f_handler = open(file_path, 'wb')
        f_handler.write(config.const.DISPOSAL_BOUNDARY + '\n')
        f_handler.write('User-Agent:' + CENTER_USER_AGENT + '\n')
        f_handler.write('Type:center_audit\n')
        audit_log['time'] = audit_log['time'].strftime('%Y-%m-%d %H:%M:%S')
        f_handler.write(json.dumps(audit_log))
        f_handler.close()
    else:
        print '数据库操作失败'


from login.models import User
#权限管理
def _auth(args):#args 是传入的，需要验证的权限
  def __auth(func):
    def _login(request):
      try:
        request_data = print_header_data(request)  # 获取请求数据
        user = User.objects.get(username=request_data.get('uuid', ''))
        #如果定义了就将用户的权限跟预定义的进行匹配
        #if user.auth_group in args or user.auth_group == 'admin':
        user.get_group_permissions()
        if user.has_perm(args):
            return func(request)#权限验证通过，继续执行视图
        else: #否则执行禁止视图
            # return HttpResponseRedirect('/command/quanxian')
            # response = HttpResponse()
            # response['Content-Type'] = 'text/javascript'
            #
            #
            # response.write('alert(123)')
            return 0
      except User.DoesNotExist:
        return ui_message_response(500, '验证权限失败', '验证权限失败',
                                                      status.HTTP_500_INTERNAL_SERVER_ERROR)
    return _login
  return __auth