# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_firmware_update(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "cookie": cookie
    }
    payload = {
        'filename': '20180130220756_344348.exe',
        'version': '536870924.20180130.0.1'
    }

    r = session.get(ROOT_URL + "V1/sys_manager/update", params=payload, headers=headers,
                    verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.headers
    print r.status_code
    print r.text.encode('utf-8')

if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    send_firmware_update(s, device_id)
