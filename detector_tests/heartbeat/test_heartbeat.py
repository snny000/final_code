# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_heartbeat(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "Cookie": cookie
    }

    r = session.post(ROOT_URL + "V1/heartbeat", headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))

    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    send_heartbeat(s, device_id)
