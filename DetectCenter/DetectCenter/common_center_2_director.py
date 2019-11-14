# -*- coding: utf-8 -*-
import json
import time
from director_config import *
import sender
from DetectCenter import date_util as du

from requests_toolbelt import MultipartEncoder

jcq_upload_2_director_header_condition_task_id = '0'


def upload_json_2_director_of_detector(common_header, data, send_data, log_data_type, from_type='', is_plugin=False, task_id=jcq_upload_2_director_header_condition_task_id, async_level=0, url=DIRECTOR_URL, retract=0):
    """
    管理中心上传前端检测器的上传的插件、告警、审计、状态信息中的json信息到指挥节点
    :param common_header:    基础请求头信息
    :param data:             前端检测器上传json的处理后信息（包含检测器ID）
    :param send_data:        前端检测器上传json原始信息
    :param log_data_type:    用于记录log
    :param from_type:        消息的来源小类
    :param is_plugin:        是否为插件
    :param task_id:          固定为'D1342'(指挥下行的任务组ID回传)
    :param async_level:      是否使用异步发送，0（不使用）、1（高优先级）、2（普通优先级）、3（低优先级）
    :param url
    :param retract           打印控制台缩进数，以"tab"为单位
    :return:
    """
    custom_header = {
        'Meta-Data': json.dumps({
            'id': data.get('alarm_id', '0'),     # 检测器上传的json信息中的id值作为管理中心存储和上传的alarm_id
            'from_id': '',
            'from_type': from_type,
            'risk': data.get('risk', 0)          # 用于告警数据上传时指定风险级别
        }),
        'Condition': json.dumps({
            'plug_id' if is_plugin else 'rule_id': data.get('plug_id', 0) if is_plugin else data.get('rule_id', 0),
            'task_id': task_id,
            'device_id': data['device_id'],
        })
    }

    command_header = dict(common_header, **custom_header)

    if async_level == 0:
        sender.send_director(url, data['device_id'], log_data_type, command_header, send_data, retract)
    elif async_level == 1:
        sender.async_send_director_hi(url, data['device_id'], log_data_type, command_header, send_data, retract)
        # sender.send_director(url, data['device_id'], log_data_type, command_header, send_data, retract)
    elif async_level == 2:
        sender.async_send_director(url, data['device_id'], log_data_type, command_header, send_data, retract)
        # sender.send_director(url, data['device_id'], log_data_type, command_header, send_data, retract)
    else:
        sender.async_send_director_lo(url, data['device_id'], log_data_type, command_header, send_data, retract)
        # sender.send_director(url, data['device_id'], log_data_type, command_header, send_data, retract)


def upload_file_2_director_of_detector(common_header, data, send_file, log_data_type, from_type='', risk=0, is_plugin=False, task_id=jcq_upload_2_director_header_condition_task_id, async_level=0, url=DIRECTOR_URL, retract=0):
    """
    管理中心上传前端检测器的上传的插件、告警、审计、状态信息中的文件信息到指挥节点
    :param common_header:    基础请求头信息
    :param data:             前端检测器上传文件的Content-Filedesc信息（包含检测器ID）
    :param send_file:        要发送的文件名称和路径tuple：(filename, filepath)
    :param log_data_type:    用于记录log
    :param from_type:        消息的来源小类
    :param risk:             int：告警级别
    :param is_plugin:        是否为插件
    :param task_id:          固定为'D1342'(指挥下行的任务组ID回传)
    :param async_level:      是否使用异步发送，0（不使用）、1（高优先级）、2（普通优先级）、3（低优先级）
    :param url
    :param retract           打印控制台缩进数，以"tab"为单位
    :return:
    """
    custom_header = {
        'Meta-Data': json.dumps({
            'id': '',           # 检测器上传的文件信息本身没有id值，所以将该文件关联的json消息的id值作为管理中心存储和上传的alarm_id，此时的alarm_id赋给from_id字段
            'from_id': data.get('alarm_id', ''),
            'from_type': from_type,
            'risk': risk,
        }),
        'Content-Filedesc': json.dumps({
            'filetype': data['filetype'],
            'filename': data['filename'],
            'checksum': data['checksum'],
            'url': ''
        }),
        'Condition': json.dumps({
            'plug_id' if is_plugin else 'rule_id': data.get('plug_id', '') if is_plugin else data.get('rule_id', ''),
            'task_id': task_id,
            'device_id': data['device_id'],
        })
    }
    command_header = dict(common_header, **custom_header)

    if async_level == 0:
        sender.send_director(url, data['device_id'], log_data_type, command_header, send_file, retract)
    elif async_level == 1:
        sender.async_send_director_hi(url, data['device_id'], log_data_type, command_header, send_file, retract)
        # sender.send_director(url, data['device_id'], log_data_type, command_header, send_file, retract)
    elif async_level == 2:
        sender.async_send_director(url, data['device_id'], log_data_type, command_header, send_file, retract)
        # sender.send_director(url, data['device_id'], log_data_type, command_header, send_file, retract)
    else:
        sender.async_send_director_lo(url, data['device_id'], log_data_type, command_header, send_file, retract)
        # sender.send_director(url, data['device_id'], log_data_type, command_header, send_file, retract)


def get_common_command_header_of_detector(msg_type, source_type, business_type, request, device_id, capture_date=du.get_current_time(), channel_type='JCQ', data_type='file', task_type='0'):
    """
    构造上传检测器来源数据至指挥节点的业务数据基本请求头
    :param msg_type:      声明业务数据的数据类别，即数据大类，需要作为触发器的判断依据，包括 'alert'、'status'、'echo'、'sync'、'cmd'、'rule'，其中上行消息暂时认为只有 'alert'、'status'、'echo'
    :param source_type:   声明业务数据的数据源，即数据中类，需要作为触发器的判断依据，包括JCQ_CSSM：检测器传输涉密日志
                                                                         JCQ_GJQM：检测器攻击窃密日志
                                                                         JCQ_MBSJ：检测器目标审计日志
                                                                         JCQ_TXZD：检测器通信阻断日志
                                                                         JCQ_XWSJ：检测器行为审计日志
    :param business_type: 声明业务数据的具体内容类型，即数据小类，另新定义了五种同步数据使用的业务数据类型，但是与上行数据无关，需要作为触发器的判断依据
    :param request:
    :param device_id:     检测器ID
    :param capture_date:  前端检测该条告警信息的捕获的时间
    :param channel_type:  保留字段，用与区分不同的数据来源，如JCQ表示来自检测器
    :param data_type:     包括'msg'、'file'，可以是json（标记为msg），也可以是文件（标记为file），用于处理数据时的判断数据类型依据
    :param task_type:     告警数据的任务编号，需要作为触发器的判断依据
    :return:
    """
    return {
        'Channel-Type': channel_type,
        'Msg-Type': msg_type,
        'Source-Type': source_type,
        'BusinessData-Type': business_type,
        'Data-Type': data_type,
        'Task-Type': task_type,
        'Src-Node': SRC_NODE,         # 源地区，用于指名产生告警的地区，管理中心的上级指挥节点
        'Src-Center': SRC_CENTER_ID,     # 用于指名产生告警的控制节点或设备，一般指检测器管理中心编号
        'User-Agent': request.META.get('HTTP_USER_AGENT'),
        'Capture-Date': capture_date.strftime('%a, %d %b %Y %H:%M:%S'),
        'Content-Type': request.META.get('HTTP_CONTENT_TYPE'),
        'version': '1.0',
        # 'Cookie': 'unknown',
        'X-Forwarded-For': detect_center_host,
        'Src-Device': device_id
    }


def get_common_command_header_of_center(source_type, business_type, msg_type='status', channel_type='JCQ', data_type='msg', task_type='0'):
    """
    构造上传管理中心来源数据至指挥节点的业务数据基本请求头
    :param msg_type:      声明业务数据的数据类别，即数据大类，需要作为触发器的判断依据，包括 'alert'、'status'、'echo'、'sync'、'cmd'、'rule'，其中上行消息暂时认为只有 'alert'、'status'、'echo'
    :param source_type:   声明业务数据的数据源，即数据中类，需要作为触发器的判断依据，包括JCQ_CSSM：检测器传输涉密日志
                                                                         JCQ_GJQM：检测器攻击窃密日志
                                                                         JCQ_MBSJ：检测器目标审计日志
                                                                         JCQ_TXZD：检测器通信阻断日志
                                                                         JCQ_XWSJ：检测器行为审计日志
    :param business_type: 声明业务数据的具体内容类型，即数据小类，另新定义了五种同步数据使用的业务数据类型，但是与上行数据无关，需要作为触发器的判断依据
    :param channel_type:  保留字段，用与区分不同的数据来源，如JCQ表示来自检测器
    :param data_type:     包括'msg'、'file'，可以是json（标记为msg），也可以是文件（标记为file），用于处理数据时的判断数据类型依据
    :param task_type:     告警数据的任务编号，需要作为触发器的判断依据
    :return:
    """
    return {
        'Channel-Type': channel_type,
        'Msg-Type': msg_type,
        'Source-Type': source_type,
        'BusinessData-Type': business_type,
        'Data-Type': data_type,
        'Task-Type': task_type,
        'Src-Node': SRC_NODE,         # 源地区，用于指名产生告警的地区，管理中心的上级指挥节点
        'Src-Center': SRC_CENTER_ID,     # 用于指名产生告警的控制节点或设备，一般指检测器管理中心编号
        'User-Agent': CENTER_USER_AGENT,
        'Capture-Date': time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()),
        'Content-Type': 'application/json',
        'version': '1.0',
        # 'Cookie': 'unknown',
        'X-Forwarded-For': detect_center_host
    }


def upload_json_2_director_of_center(common_header, log_data_type, command_data, rule_id='0', task_id='0', async_level=0, url=DIRECTOR_URL, retract=0):
    """
    管理中心上传管理中心的json信息到指挥节点
    :param common_header:    基础请求头信息
    :param log_data_type:    用于记录log
    :param command_data:
    :param rule_id:          规则ID
    :param task_id:          任务组ID
    :param async_level       是否使用异步发送，0（不使用）、1（高优先级）、2（普通优先级）、3（低优先级）
    :param url
    :param retract           打印控制台缩进数，以"tab"为单位
    :return:
    """
    custom_header = {
        'Meta-Data': json.dumps({
            'id': '',
            'from_id': '',
            'from_type': ''
        }),
        'Condition': json.dumps({
            'rule_id':  rule_id,
            'task_id':  task_id,
            'device_id': SRC_CENTER_ID,
        })
    }

    command_header = dict(common_header, **custom_header)

    if async_level == 0:
        sender.send_director(url, SRC_CENTER_ID, log_data_type, command_header, command_data, retract)
    elif async_level == 1:
        sender.async_send_director_hi(url, SRC_CENTER_ID, log_data_type, command_header, command_data, retract)
        # sender.send_director(url, SRC_CENTER, log_data_type, command_header, command_data, retract)
    elif async_level == 2:
        sender.async_send_director(url, SRC_CENTER_ID, log_data_type, command_header, command_data, retract)
        # sender.send_director(url, SRC_CENTER, log_data_type, command_header, command_data, retract)
    else:
        sender.async_send_director_lo(url, SRC_CENTER_ID, log_data_type, command_header, command_data, retract)
        # sender.send_director(url, SRC_CENTER, log_data_type, command_header, command_data, retract)
