# -*- coding: utf-8 -*-
from DetectCenter import common


def check_dict_data(data, flag='注册信息'):
    """
    校验字典类型数据
    :param data: 校验的数据
    :return:     校验后的数据
    """
    if not isinstance(data, dict):  # 判断请求数据类型是否合规
        return common.detector_message_response(400, '%s数据不是dict类型' % flag, '%s不是dict类型数据' % flag)
    else:
        return data.copy()  # request_data是 immutable QueryDict 对象，需要转变


def fill_business_data_by_field(field_str, data, detector_id, report_time):
    """
    填充检测器ID和上报时间到检测器上传的业务状态数据用户入库
    :param field_str:      业务状态数据字段-> interface, suspected, plug_status
    :param data:           检测器上传的数据
    :param detector_id:    检测器ID
    :param report_time:    上报时间
    :return:               检测器上传的数据填充后对应字段的数据
    """
    business_data = []
    if field_str in data:
        plugin_status = data[field_str]  # List
        for item in plugin_status:
            item['device_id'] = detector_id
            item['report_time'] = report_time
            business_data.append(item)
        return business_data
    else:
        return common.detector_message_response(400, '请求数据缺少{0}参数'.format(field_str),
                                                '请求数据缺少{0}参数'.format(field_str))
