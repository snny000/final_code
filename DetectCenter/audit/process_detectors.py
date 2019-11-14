# -*- coding:utf-8 -*-

from rest_framework import status
from DetectCenter import common, statistics_log
from detector.models import Detector


def process_header(request):
    header = request.META
    # 处理user_agent
    user_agent = header.get('HTTP_USER_AGENT')  # 请求头中的User-Agent
    if user_agent is None:
        return common.detector_message_response(400, '请求头缺少User-Agent字段', '请求头缺少User-Agent字段')
    elif not common.is_valid_user_agent(user_agent):
        return common.detector_message_response(400, '请求头User_Agent字段不符合标准', '请求头User_Agent字段不符合标准')
    else:
        detector_id = user_agent[0:12]  # 从User-Agent中提取检测器ID并返回

    if detector_id not in request.session:  # 通过session验证检测器是否认证
        return common.detector_message_response(403, '检测器没有认证', '检测器没有认证', status.HTTP_403_FORBIDDEN)

    is_effective = Detector.objects.filter(device_id=detector_id)[0].is_effective
    if not is_effective:
        return common.detector_message_response(403, '检测器已禁用', '检测器已禁用', status.HTTP_403_FORBIDDEN)

    return detector_id


def process_net_log(request,):
    header, request_data = common.get_request_data(request)  # 获取请求数据
    response_data = process_header(request)                    # 获取检测器ID
    if not isinstance(response_data, basestring):
        return response_data                                  # 返回响应信息
    detector_id = response_data
    log_str = '%s %s %s %d' % (header.get('REMOTE_ADDR'), detector_id, 'net_log', len(request.FILES))
    statistics_log.string2log_per_day(content=log_str, path=common.LOG_PATH, prefix="statistics.", suffix=".log")

