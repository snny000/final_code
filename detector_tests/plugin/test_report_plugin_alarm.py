# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_plugin_alarm(session, detector_id, alarm_id, plug_id, num):
    file_name = alarm_id + '_002_' + str(num) + '.pcap'
    file_path = TEST_PATH + 'plugin_alarm/' + detector_id + '/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path += file_name
    content = ''
    for i in range(random.randint(100, 10000)):
        val = random.randint(0x4E00, 0x9FBF)
        content += unichr(val).encode('utf-8')
    with open(file_path, 'wb') as f:
        f.write(content)

    # file_desc = '{"time"="' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '";"id"="' + \
    #             alarm_id + '";"plug_id"=' + str(plug_id) + ';"num"=' + str(num) + ';"checksum"="' + \
    #             calc_md5(file_path) + '";"filename"="' + file_name + '";"filetype"="pcap"}'
    # print file_desc
    file_desc = json.dumps({
        "filetype": "PCAP",
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "id": alarm_id,
        "num": num,
        "checksum": calc_md5(file_path),
        "filename": file_name,
        "plug_id": plug_id
    })

    boundary = '---------------------------7de1ae242c06ca'
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "multipart/form-data;boundary=" + boundary,
        "Cookie": cookie,
        "Content-Filedesc": file_desc
    }

    files = MultipartEncoder(
        fields={
            "file": (file_name, open(file_path, "rb"), "multipart/form-data")
        },
        boundary=boundary
    )

    send_url = ROOT_URL + "V1/plug_manager/plug_warn/plug_alarm_file"
    print send_url
    r = session.post(send_url, headers=headers, data=files,
                    verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))

    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    device_id = DETECTOR_ID
    a_id = sys.argv[1]
    p_id = sys.argv[2]
    n = 1
    s = requests.Session()
    send_plugin_alarm(s, device_id, a_id, p_id, n)
