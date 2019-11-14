# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_inner_policy_update(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "cookie": cookie
    }
    payload = {
        'filename': '20171218095957_655329.txt',
    }

    r = session.get(ROOT_URL + "V1/sys_manager/inner_policy_update", params=payload, headers=headers,
                    verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.text.encode('utf-8')

if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    send_inner_policy_update(s, device_id)
