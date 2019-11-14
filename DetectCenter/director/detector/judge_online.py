# -*- coding: utf-8 -*-

import os
import sys
import django
from DetectCenter import config
from director.detect_center_reg_auth import check_global_director_connection

# pathname = os.path.dirname(os.path.abspath(__file__))
# # sys.path.insert(0, pathname)
# sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DetectCenter.settings")
#
# django.setup()

from django.db import connection
import datetime

from detector.models import Detector, SystemRunningStatus
from detector.detector_serializers import DetectorOnlineEventSerializer
from datetime import timedelta
from DetectCenter import date_util as du, director_config, common_center_2_director as ccd
import traceback
import json
from django.core.serializers import serialize

over_time_minute = 5


def is_online(time_delta=180):
    cursor = connection.cursor()
    sql = 'UPDATE detector_info SET is_online=IF(NOW()-heartbeat_time>%d,0,1) WHERE heartbeat_time is not null;' % time_delta
    cursor.execute(sql)
    cursor.close()
    # print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '更新在线状态\n'


def record_event():
    try:
        print du.get_current_date_string(), '##开始检查在线状态'
        device_info = Detector.objects.all()
        if device_info.exists():
            for device in device_info:
                old_online_status = device.is_online
                if (du.get_current_time() - (device.heartbeat_time if device.heartbeat_time is not None else (du.get_current_time() - timedelta(minutes=over_time_minute+1)))) > timedelta(minutes=over_time_minute) \
                        and (du.get_current_time() - (device.last_warning_time if device.last_warning_time is not None else (du.get_current_time() - timedelta(minutes=over_time_minute+1)))) > timedelta(minutes=over_time_minute):
                    print '####设置%s状态为离线' % device.device_id
                    Detector.objects.filter(id=device.id).update(is_online=False)
                    if old_online_status:
                        online_event = {
                            'device_id': device.device_id,
                            'event': '离线',
                            'time': du.get_current_date_string()
                        }
                        serialize = DetectorOnlineEventSerializer(data=online_event)
                        if serialize.is_valid():
                            serialize.save()
                            print '####device_id:', device.device_id, '保存离线事件'
                        else:
                            print '####device_id:', device.device_id, '保存离线事件', serialize.errors
                        center_report_detector_running_status(device_id=device.device_id, device_is_online=0)
                else:
                    print '设置%s状态为在线' % device.device_id
                    Detector.objects.filter(id=device.id).update(is_online=True)
                    if not old_online_status:
                        online_event = {
                            'device_id': device.device_id,
                            'event': '上线',
                            'time': du.get_current_date_string()
                        }
                        serialize = DetectorOnlineEventSerializer(data=online_event)
                        if serialize.is_valid():
                            serialize.save()
                            print '####device_id:', device.device_id, '保存上线事件'
                        else:
                            print '####device_id:', device.device_id, '保存上线事件', serialize.errors
                        center_report_detector_running_status(device_id=device.device_id, device_is_online=1)

        print '##检查在线状态完毕'
    except Exception as e:
        print e.message, e.args


def record_online_event(device_id):
    device_info = Detector.objects.filter(device_id=device_id)
    if device_info.exists():
        if not device_info[0].is_online:
            print '记录重新上线事件'
            online_event = {
                'device_id': device_info[0].device_id,
                'event': '上线',
                'time': du.get_current_date_string()
            }
            serialize_data = DetectorOnlineEventSerializer(data=online_event)
            if serialize_data.is_valid():
                serialize_data.save()
            else:
                print 'device_id:', device_info[0].device_id, '保存上线事件', serialize_data.errors
            center_report_detector_running_status(device_id=device_info[0].device_id, device_is_online=1)


# 通过检测器运行状态上传接口定时上报检测器在线状态
def center_report_detector_running_status(device_id=None, device_is_online=1):
    try:
        if not (config.const.UPLOAD_DIRECTOR and check_global_director_connection()):
            return

        if device_id is None:
            return
        else:
            device_info = Detector.objects.filter(device_id=device_id)
        if device_info.exists():
            for device in device_info:
                run_status_info = SystemRunningStatus.objects.filter(device_id=device.device_id).order_by('-id')[0: 1]
                if run_status_info.exists():
                    serialize_data = serialize('json', run_status_info, fields=('cpu', 'mem', 'disk', 'time', 'plug_stat', 'did'))
                    data_list = json.loads(serialize_data)
                    run_data = data_list[0]['fields']
                    run_data['cpu'] = json.loads(run_data['cpu'])
                    run_data['plug_stat'] = json.loads(run_data['plug_stat'])
                    run_data['time'] = run_data['time'].replace('T', ' ')
                else:
                    run_data = {'cpu': [], 'mem': 0, 'disk': 0, 'time': du.get_current_date_string(), 'plug_stat': [], 'did': 1}
                run_data['is_online'] = device_is_online

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


if __name__ == '__main__':
    pathname = os.path.dirname(os.path.abspath(__file__))
    # sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DetectCenter.settings")

    django.setup()

    is_online()
    record_event()
