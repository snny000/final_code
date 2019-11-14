# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_system_audit(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "cookie": cookie
    }

    request_data = {
        "id": str(random.randint(1, 99999999999999999999)),
        "user": "张三",
        "event_type": "manage",
        "opt_type": "系统配置",
        "time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "message": "用户登录"
    }

    r = session.post(ROOT_URL + "V1/system_audit/", data=json.dumps(request_data), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    send_system_audit(s, device_id)
