# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_alarm_other(session, detector_id, alarm_id, rule_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "cookie": cookie
    }

    # 其他告警
    trojan_data = {
        "id": alarm_id,
        "rule_id": rule_id,
        "sip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "sport": random.randint(1024, 65534),
        "smac": ':'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
        "dip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "dport": random.randint(1024, 65534),
        "dmac": ':'.join(['%02x' % x for x in imap(lambda arg:random.randint(0, 255), range(6))]),
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "risk": random.randint(0, 4),

        "desc": "邮件异常登录"
    }

    r = session.post(ROOT_URL + "V1/alarm/other/inner_policy",
                     data=json.dumps(trojan_data), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH)
                     )
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


def send_alarm_other_file(session, detector_id, alarm_id, rule_id, num):
    file_name = str(int(time.time())) + '_002_' + str(num) + '.pcap'
    file_path = TEST_PATH + 'alarm_other/' + detector_id + '/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path += file_name
    content = ''
    for i in range(random.randint(100, 10000)):
        val = random.randint(0x4E00, 0x9FBF)
        content += unichr(val).encode('utf-8')
    with open(file_path, 'wb') as f:
        f.write(content)

    # file_desc = '{"filetype"="PCAP";"time"="' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '";"id"="' + \
                # alarm_id + '";"num"=' + str(num) + ';"checksum"="' + calc_md5(file_path) + '";"filename"="' + \
                # file_name + '";"is_upload"="false"}'
    file_desc = json.dumps({
        "filetype": "PCAP",
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "id": alarm_id,
        "num": num,
        "checksum": calc_md5(file_path),
        "filename": file_name,
        "is_upload": False
    })
    print file_desc

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

    r = session.post(ROOT_URL + "V1/alarm/other/inner_policy_pcap",
                     data=files, headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH)
                     )
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    import sys
    device_id = DETECTOR_ID
    # alert_id = '20170525000004'
    alert_id = sys.argv[1]
    file_num = 1
    ruleID = 0
    s = requests.Session()
    send_alarm_other(s, device_id, alert_id, ruleID)
    send_alarm_other_file(s, device_id, alert_id, ruleID, file_num)
