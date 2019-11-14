# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_version_check(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "cookie": cookie
    }

    data = read_file('/bhome/wwenan/Detector/DetectorManagement/detector_tests/test_files/123456.txt', 0, 10)

    result = {
        "get_file": get_base64(data)
    }
    # result = {
        # 'ls': ["/home/DetectorManagement", "/home/elsearch", "/home/HS", "/home/software", "/home/test"]
    # }
    result = {
        'md5sum': get_md5(data)
    }
    r = session.post(ROOT_URL + "V1/sys_manager/version_check",
                     data=json.dumps(result), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.text.encode('utf-8')

if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    send_version_check(s, device_id)
