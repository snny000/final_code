# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def download_plugin(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "Cookie": cookie,
        # "Range": "bytes=0-200"
    }

    r = session.get(ROOT_URL + "V1/plug_manager/plug_load/1", headers=headers,
                    params={'plug_version': '1'},
                    verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))

    print r.headers
    print r.status_code
    print r.text.encode('utf-8')


if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    download_plugin(s, device_id)
