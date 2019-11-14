# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_business_status(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "Cookie": cookie
    }

    # 网卡连通性信息
    interface_info1 = {
        "interface_seq": 1,
        "interface_flag": "eth0",
        "interface_stat": random.choice([1, 2, 3, 4, 99]),
        "interface_flow": random.randint(1000, 100000),
        "interface_error": random.randint(10, 1000),
        "interface_drop": random.randint(10, 1000),
        "duration_time": random.randint(100, 1000)
    }
    interface_info2 = {
        "interface_seq": 2,
        "interface_flag": "eth1",
        "interface_stat": random.choice([1, 2, 3, 4, 99]),
        "interface_flow": random.randint(1000, 100000),
        "interface_error": random.randint(10, 1000),
        "interface_drop": random.randint(10, 1000),
        "duration_time": random.randint(100, 1000)
    }
    interface = [interface_info1, interface_info2]

    # 异常状态
    suspected = []
    num = random.randint(1, 4)
    i = 0
    sus_type = []
    while i < num:
        event_type = random.randint(1, 4)
        if event_type not in sus_type:
            sus_type.append(event_type)
            if event_type == 1:
                msg = random.choice(["CPU使用率大于90%", "内存使用率大于90%", "硬盘使用率大于95%"])
            elif event_type == 2:
                msg = random.choice(["本地web服务崩溃", "检测服务出现崩溃、重启等现象"])
            elif event_type == 3:
                msg = "检测器不能解析JC中心下发的规则"
            else:
                msg = "插件异常"

            suspected_status = {
                "event_type": event_type,
                "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(100, 1000))),
                "risk": random.randint(0, 4),
                "msg": msg
            }
            suspected.append(suspected_status)
            i += 1

    # 模块状态
    module_info = [
        {
            "name": "alarm",
            "status": 'on',
            'submodule': [
                {'name': 'trojan', 'status': 'on', 'version': {'trojan': '20170205004'}},
                {'name': 'attack', 'status': 'on', 'version': {'attack': '20170205003'}}
            ]
        },
        {
            "name": "abnormal",
            "status": 'off',
            'submodule': [
                {'name': 'abnormal', 'status': 'off', 'version': {'abnormal': '20170205006'}}
            ]
        }
    ]

    # 插件状态
    plugin_info = [
        {
            'plug_id': '122',
            'status': 'on',
            'plug_version': '20170206_001',
            'plug_policy_version': '20170206_007'
        },
        {
            'plug_id': '288',
            'status': 'off',
            'plug_version': '20170206_003',
            'plug_policy_version': '20170208_001'
        }
    ]

    request_data = {
        "uptime": 14000,
        "soft_version": device_version,
        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(100, 1000))),
        "interface": interface,
        'suspected': suspected,
        'module_status': module_info,
        'plug_status': plugin_info
    }

    send_url = ROOT_URL + "V1/business_status"
    r = session.post(send_url, data=json.dumps(request_data), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    send_business_status(s, device_id)
