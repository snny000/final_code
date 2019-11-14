# -*- coding:utf-8 -*-
from DetectCenter import common, tasks

import time
import json
from DetectCenter import sender, common
from DetectCenter.director_config import *

soft_version = '/20171012_123456789(IIE)'
audit_upload_2_director_header_condition_rule_id = 'D100235'


def get_common_command_header(source_type, business_type, msg_type='status', channel_type='JCQ', data_type='msg', task_type='0'):
    """
    构造上传至指挥节点的业务数据基本请求头
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
        'Src-Center': SRC_CENTER,     # 用于指名产生告警的控制节点或设备，一般指检测器管理中心编号
        'User-Agent': SRC_CENTER + soft_version,
        'Capture-Date': time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()),
        'Content-Type': 'application/json',
        'version': '1.0',
        'Cookie': 'unknown',
    }


def jcq_upload_json_2_director(common_header, log_data_type, command_data, rule_id=audit_upload_2_director_header_condition_rule_id, async_level=0, url=DIRECTOR_URL):
    """
    管理中心上传json信息到指挥节点
    :param common_header:    基础请求头信息
    :param log_data_type:    用于记录log
    :param command_data:
    :param rule_id:
    :param async_level       是否使用异步发送，0（不使用）、1（高优先级）、2（普通优先级）、3（低优先级）
    :param url
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
            'task_id':  common.jcq_upload_2_director_header_condition_task_id,
            'device_id': SRC_CENTER,
            'data_source': 'traffic'
        })
    }

    command_header = dict(common_header, **custom_header)

    if async_level == 0:
        sender.send_director(url, SRC_CENTER, log_data_type, command_header, command_data)
        # tasks.send_director_task.apply_async(
        #     (DIRECTOR_URL, SRC_CENTER, log_data_type, command_header, command_data),
        #     serializer='msgpack')
    elif async_level == 1:
        sender.async_send_director_hi(url, SRC_CENTER, log_data_type, command_header, command_data)
    elif async_level == 2:
        sender.async_send_director(url, SRC_CENTER, log_data_type, command_header, command_data)
    else:
        sender.async_send_director_lo(url, SRC_CENTER, log_data_type, command_header, command_data)
