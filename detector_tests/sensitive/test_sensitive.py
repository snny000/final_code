# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_sensitive_data(session, detector_id, alarm_id, alert_type):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        "Cookie": cookie
    }

    app_pro_cho = random.choice(['Email', 'Im', 'Filetransfer', 'Http', 'Netdisk', "Other"])
    if app_pro_cho == 'Email':
        app_opt = {
            "sender": "Zhangsan@163.com", "receiver": "lisi@gmail.com;wangliang@yahoo.com",
            "cc": "wangwu@qq.com;zhaoliu@163.com", "bcc": "zhangliu@iie.cn",
            "subject": "参加会议", "domain": "163",
            "authinfo": {'mail_from': "Zhangsan@163.com",
                         "rcpt_to": "lisi@gmail.com;wangliang@yahoo.com",
                         "ehlo": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                         },
            "protocol": "smtp"
        }
    elif app_pro_cho == 'Im':
        app_opt = {
            "protocol": "Qq", "sender": "Zhangsan@163.com", "receiver": "lisi@gmail.com;wangwu@gmail.com",
            "account": "123456", "msg_content": "您好"
        }
    elif app_pro_cho == 'Filetransfer':
        app_opt = {
            "protocol": "ftp", "account": "ftp123", "pwd": "123456ftp", "trans_dir": random.randint(1, 3)
        }
    elif app_pro_cho == 'Http':
        app_opt = {
            "protocol": "http", "domain": "www.test.com", "url": "www.test.com:8090/index.html",
            "method": "POST", "ret_code": 401, "user_agent": "Mozilla/5.0",
            "cookie": "SESSION=14028C8C0E5627F0AF3698CCE11D297B;",
            "server": "Apache-Coyote/1.1", "refer": "http://www.mydomain.com/jsoa/login.jsp"
        }
    elif app_pro_cho == 'Netdisk':
        app_opt = {
            "protocol": "Baidu", "account": "Zhangsan", "domain": "百度网盘"
        }
    else:
        app_opt = {"protocol": "unknown"}

    alert_msg = {
        "id": alarm_id,
        "alert_type": alert_type,
        "rule_id": 0,
        "risk": random.randint(0, 4),
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "sm_inpath": "1.rar\\2.rar\\test\\2.doc",
        "sm_summary": "领悟会议精神,应用到工作中…",
        "sm_desc": "检测器",
        "sip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "sport": random.randint(1024, 65534),
        "smac": ':'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
        "dip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
        "dport": random.randint(1024, 65534),
        "dmac": ':'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
        "xm_dir": random.randint(1, 3),
        "app_pro": app_pro_cho,
        "app_opt": app_opt
    }

    if alert_type == 1:     # 密标文件检测
        send_url = ROOT_URL + "V1/sensitive/finger_file/inner_policy"
    elif alert_type == 2:   # 标密文件检测
        send_url = ROOT_URL + "V1/sensitive/sensitive_file/inner_policy"
    elif alert_type == 3:   # 关键词检测
        alert_msg['rule_id'] = random.randint(1, 1000)
        send_url = ROOT_URL + "V1/sensitive/keyword_file/center_policy"
    elif alert_type == 4:   # 加密文件检测
        send_url = ROOT_URL + "V1/sensitive/encryption_file/inner_policy"
    elif alert_type == 5:   # 多层压缩文件检测
        alert_msg['rule_id'] = random.randint(1, 1000)
        send_url = ROOT_URL + "V1/sensitive/compress_file/center_policy"
    elif alert_type in [6, 7]:  # 图文文件筛选
        alert_msg['rule_id'] = random.randint(1, 1000)
        send_url = ROOT_URL + "V1/sensitive/picture_file/center_policy"
    elif alert_type == 8:    # 版式文件检测
        send_url = ROOT_URL + "V1/sensitive/style_file/inner_policy"
    else:
        assert 1 <= alert_type <= 8, "alert_type不在[1, 8]内"
        return

    print send_url
    r = session.post(send_url, data=json.dumps(alert_msg), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))

    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


def send_sensitive_file(session, detector_id, alarm_id, alert_type):
    file_name = str(int(time.time())) + '_002_' + str(random.randint(1, 100)) + '.pcap'
    if alert_type == 1:
        file_path = TEST_PATH + 'sensitive_finger/' + detector_id + '/'
        send_url = ROOT_URL + "V1/sensitive/finger_file/inner_policy_file"
    elif alert_type == 2:
        file_path = TEST_PATH + 'sensitive_file/' + detector_id + '/'
        send_url = ROOT_URL + "V1/sensitive/sensitive_file/inner_policy_file"
    elif alert_type == 3:
        file_path = TEST_PATH + 'sensitive_keyword/' + detector_id + '/'
        send_url = ROOT_URL + "V1/sensitive/keyword_file/center_policy_file"
    elif alert_type == 4:
        file_path = TEST_PATH + 'sensitive_encryption/' + detector_id + '/'
        send_url = ROOT_URL + "V1/sensitive/encryption_file/inner_policy_file"
    elif alert_type == 5:
        file_path = TEST_PATH + 'sensitive_compress/' + detector_id + '/'
        send_url = ROOT_URL + "V1/sensitive/compress_file/center_policy_file"
    elif alert_type in [6, 7]:
        file_path = TEST_PATH + 'sensitive_picture/' + detector_id + '/'
        send_url = ROOT_URL + "V1/sensitive/picture_file/center_policy_file"
    elif alert_type == 8:
        file_path = TEST_PATH + 'sensitive_style/' + detector_id + '/'
        send_url = ROOT_URL + "V1/sensitive/style_file/inner_policy_file"
    else:
        assert 1 <= alert_type <= 8, "alert_type不在[1, 8]内"
        return

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
                # alarm_id + '";"checksum"="' + calc_md5(file_path) + '";"filename"="' + file_name + \
                # '";"is_upload"="false"}'
    file_desc = json.dumps({
        "filetype": "PCAP",
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "id": alarm_id,
        "checksum": calc_md5(file_path),
        "filename": file_name,
        "is_upload": False
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

    print send_url
    r = session.post(send_url, data=files, headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))

    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    import sys
    device_id = DETECTOR_ID
    s = requests.Session()
    # for i in range(1, 100):
    # a_id = '2017052500000' + str(i)
    a_id = sys.argv[1]
    # a_type = random.randint(1, 8)
    #a_type = 1
    a_type = int(sys.argv[2])
    send_sensitive_data(s, device_id, a_id, a_type)
    send_sensitive_file(s, device_id, a_id, a_type)
    # time.sleep(3)
