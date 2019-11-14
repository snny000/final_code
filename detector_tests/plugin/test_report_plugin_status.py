# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_plugin_status(session, detector_id, plug_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "Cookie": cookie
    }

    # 插件状态
    plug_status = ['plug_add_succ', 'plug_add_fail', 'plug_update_succ', 'plug_update_fail',
                   'plug_config_succ', 'plug_config_fail', 'plug_start_succ', 'plug_start_fail',
                   'plug_stop_succ', 'plug_stop_fail', 'plug_del_succ', 'plug_del_fail']
    data = {
        'plug_id': plug_id,
        'status': random.choice(plug_status)
    }

    send_url = ROOT_URL + "V1/plug_manager/plug_stat"
    print send_url
    r = session.post(send_url, headers=headers, data=json.dumps(data),
                    verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))

    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    device_id = DETECTOR_ID
    p_id = 123
    s = requests.Session()
    send_plugin_status(s, device_id, p_id)
