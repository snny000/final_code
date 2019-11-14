# -*- coding:utf-8 -*-

from DetectCenter import common
from detector.models import Detector
import json


def generate_plug_on_device_status_dict(stat=''):
    """
    将插件在生效检测器上的特定格式开启状态数据转为字典
    #1:1#2:1#-> {'1': '1', '2': '1'}
    :param stat:    数据库存储数据：#1:1#2:1#
    :return:        dict
    """
    result = dict()
    if stat is None or stat == '' or len(stat) < 2:
        pass
    else:
        device_status_list = stat[1:-1].split('#')
        for ll in device_status_list:
            temp = ll.split(':')
            if temp and len(temp) == 2:
                result[int(temp[0])] = temp[1]
    return result


def generate_plug_on_device_status_str(dict={}):
    """
    将字典转换为插件在生效检测器上的特定格式开启状态数据
    {'1': '1', '2': '1'} -> #1:1#2:1#
    :param dict:    字典数据
    :return:        数据库存储数据
    """
    result = ''
    if dict is None or len(dict) == 0:
        pass
    else:
        temp = list()
        for k, v in dict.items():
            temp.append(str(k) + ':' + str(v))
        result = '#' + '#'.join(temp) + '#'
    return result


def check_ui_upload_cmd_validity(cmd, plug_id, plug_cmd, cmd_type_list):
    """
    检查UI下发插件相关操作和命令的数据合法性，主要包括cmd，plug_id
    :param cmd:             在cmd_type_list中插件操作或命令对应的索引
    :param plug_id:         上传的插件ID
    :param plug_cmd:        入库的插件信息字典
    :param cmd_type_list:   插件操作或命令对应的类型
    :return:                plug_cmd
    """
    if cmd is None:
        return common.ui_message_response(400, '没有cmd参数', '没有cmd参数')
    else:
        try:
            cmd = int(cmd)
            plug_cmd['cmd'] = cmd_type_list[cmd - 1]
        except Exception:
            return common.ui_message_response(400, '参数cmd不是数字', '参数cmd不符合要求')

    if plug_id is None:
        return common.ui_message_response(400, '没有plug_id参数', '没有plug_id参数')
    else:
        try:
            plug_cmd['plug_id'] = int(plug_id)
        except Exception:
            return common.ui_message_response(400, '参数plug_id不是数字', '参数plug_id不符合要求')


def construct_plug_cmd_detector_ids(device_id_list, plug_cmd):
    """
    构造插件操作或命令下发的的检测器ID
    :param device_id_list:  检测器主键id
    :param plug_cmd:        入库的插件信息字典
    :return:                plug_cmd
    """
    if device_id_list is None:
        return common.ui_message_response(400, '没有detector_id_list参数', '没有detector_id_list参数')

    if device_id_list == '[]':  # 表示全部生效
        plug_cmd['device_id_list'] = '#'
        device_ids = list(Detector.objects.filter(device_status=1).values_list('device_id', flat=True))
    else:
        device_id_list = json.loads(device_id_list)
        plug_cmd['device_id_list'] = '#' + '#'.join(map(str, device_id_list)) + '#'
        device_ids = list(Detector.objects.filter(id__in=device_id_list).values_list('device_id', flat=True))
    return device_ids
