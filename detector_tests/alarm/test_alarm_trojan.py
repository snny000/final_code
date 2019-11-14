# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_alarm_trojan(session, detector_id, alarm_id, rule_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "cookie": cookie
    }

    attack_os = ['Windows', 'Ubuntu', 'OS X', 'MS-DOS', 'Unix', 'CentOS', 'Debian', 'RedHat', 'Fedora']
    trojan_os = random.choice(attack_os)

    # 木马告警
    trojan_data = [
    {
        "id": '2017111400009',
        "rule_id": rule_id,
        "sip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "sport": random.randint(1024, 65534),
        "smac": ':'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
        "dip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "dport": random.randint(1024, 65534),
        "dmac": ':'.join(['%02x' % x for x in imap(lambda arg:random.randint(0, 255), range(6))]),
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "risk": random.randint(0, 4),

        "trojan_id": random.randint(10000, 99999),
        "os": trojan_os,
        "trojan_name": "特洛伊木马",
        "trojan_type": random.randint(1, 4),
        "desc": "NoSecure 1.2 木马变种4连接操作"
    },
    {
        "id": '2017111400010',
        "rule_id": rule_id,
        "sip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "sport": random.randint(1024, 65534),
        "smac": ':'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
        "dip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "dport": random.randint(1024, 65534),
        "dmac": ':'.join(['%02x' % x for x in imap(lambda arg:random.randint(0, 255), range(6))]),
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "risk": random.randint(0, 4),

        "trojan_id": random.randint(10000, 99999),
        "os": trojan_os,
        "trojan_name": "特洛伊木马",
        "trojan_type": random.randint(1, 4),
        "desc": "NoSecure 1.2 木马变种4连接操作"
    },
    ]

    if rule_id == 0:
        r = session.post(ROOT_URL + "V1/alarm/trojan/inner_policy",
                         data=json.dumps(trojan_data), headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH)
                         )
    else:
        r = session.post(ROOT_URL + "V1/alarm/trojan/center_policy",
                         data=json.dumps(trojan_data), headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH)
                         )
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


def send_alarm_trojan_file(session, detector_id, alarm_id, rule_id, num):
    file_name = str(int(time.time())) + '_002_' + str(num) + '.pcap'
    file_path = TEST_PATH + 'alarm_trojan/' + detector_id + '/'
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
                # file_name + '";"is_upload"="false";"trojan_id"=50030}'
    file_desc = json.dumps({
        "filetype": "PCAP",
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "id": alarm_id,
        "num": num,
        "checksum": calc_md5(file_path),
        "filename": file_name,
        "is_upload": False,
        "trojan_id": 50030
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

    if rule_id == 0:
        r = session.post(ROOT_URL + "V1/alarm/trojan/inner_policy_pcap",
                         data=files, headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH)
                         )
    else:
        r = session.post(ROOT_URL + "V1/alarm/trojan/center_policy_pcap",
                         data=files, headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH)
                         )
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    import sys
    device_id = DETECTOR_ID
    alert_id = '2017111400002'
    # alert_id = sys.argv[1]
    file_num = 1
    # file_num = sys.argv[2]
    ruleID = 0
    s = requests.Session()
    send_alarm_trojan(s, device_id, alert_id, ruleID)
    send_alarm_trojan_file(s, device_id, '2017111400009', ruleID, file_num)
    send_alarm_trojan_file(s, device_id, '2017111400010', ruleID, file_num)
