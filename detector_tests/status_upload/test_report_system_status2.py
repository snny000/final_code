# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_system_status(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "Cookie": cookie
    }

    cpu_info = [
        {
            "physical_id": 1,
            "cpu_usage": random.randint(1, 100)
        },
        {
            "physical_id": 2,
            "cpu_usage": random.randint(1, 100)
        }
    ]
    plug_info = [
        {
            'plug_id': 'davc',
            'status': 'on',
            'cpu_range': 5,
            'cpu_usage': 3,
            'mem_range': 100,
            'mem_usage': 20,
            'disk_usage': 100,
        },
        {
            'plug_id': 'p_2',
            'status': 'on',
            'cpu_range': 8,
            'cpu_usage': 2,
            'mem_range': 200,
            'mem_usage': 120,
            'disk_usage': 300,
        }
    ]
    request_data = {
        "cpu": cpu_info,
        "mem": random.randint(1, 100),
        'disk': random.randint(100, 500),
        'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(100, 1000))),
        'plug_stat': plug_info
    }

    send_url = ROOT_URL + "V1/system_status"
    r = session.post(send_url, data=json.dumps(request_data), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    device_id = '170301020001'
    s = requests.Session()
    send_system_status(s, device_id)
