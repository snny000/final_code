# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


# 构造数据
def construct_data():

    lis = list('zyxwvutsrqponmlkjihgfedcba1234567890')

    data = []
    # num = random.randint(1, 10000)
    num = 5
    i = 0
    while i < num:
        app_behavior = {
            "sip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
            "sport": random.randint(1024, 65534),
            "smac": '-'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
            "dip": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
            "dport": random.randint(1024, 65534),
            "dmac": '-'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
            "protocol": random.choice(['TCP', 'UDP']),
            "app": random.choice(['http', 'email', 'ftp', 'netdisk', 'dns', 'ssl']),
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - random.randint(1, 15))),
        }
        domain = "www." + "".join(random.sample(lis, random.randint(4, 20))) + \
                 random.choice([".cn", ".com", ".net", ".org"])
        if app_behavior['app'] == 'http':
            private_param = {
                "domain": domain,
                "url": "/hello?parm1=p1&param2=p2",
                "method": random.choice(["POST", "GET"]),
                "ret_code": random.choice([200, 400, 500]),
                "user_agent": "Mozilla/5.0",
                "cookie": "SESSION=14028C8C0E5627F0AF3698CCE11D297B",
                "server": "Apache-Coyote/1.1",
                "refer": "http://" + domain + "/jsoa/login.jsp"
            }
        elif app_behavior['app'] == 'email':
            sender = "zhangsan@yahoo.com"
            receiver = "lisi@yahoo.com;hello@gmail.com"
            private_param = {
                "sender": sender,
                "receiver": receiver,
                "cc": "xiaoming@163.com;xiaohua@qq.com",
                "bcc": "liang@163.com;xiaoqiang@iie.cn",
                "subject": "测试邮件",
                "attachment": ["附件1.doc", "附件2.pdf"],
                "domain": "yahoo",
                "authinfo": {
                    "mail_from": sender,
                    "rcpt_to": receiver,
                    "ehlo": socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                }
            }
        elif app_behavior['app'] in ['ftp', 'netdisk']:
            private_param = {
                "filename": "传输文件.txt",
                "filesize": random.randint(1024, 8192)
            }
        elif app_behavior['app'] == 'dns':
            resp_result = []
            dns_num = random.randint(1, 3)
            j = 0
            while j < dns_num:
                resp_result.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))
                j += 1
            private_param = {
                "request": domain,
                "response": resp_result
            }
        else:
            private_param = {
                "finger": "3002c1103ea0f47250b431fd635679f4a4548c5d",
                "country": "CN",
                "organize": "IIE",
                "cname": "VeriSign Class 3 Code Signing 2009-2 CA",
                "sni": domain,
                "uorganize": "aname.com Corporation",
                "ucname": "aname"
            }

        data.append(dict(app_behavior, **private_param))
        i += 1
    return num, json.dumps(data)


def send_app_behavior(session, detector_id, limit_num):
    num, data = construct_data()
    if num <= limit_num:
        headers = {
            "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
            "Content-Type": "application/json",
            "cookie": cookie
        }
        r = session.post(ROOT_URL + "V1/net_audit/app_behavior", data=data, headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    else:
        file_name = str(int(time.time())) + '.gz'
        file_path = TEST_PATH + 'audit_app_behavior/' + detector_id + '/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_path += file_name
        gzip_f = gzip.GzipFile(filename='', mode='wb', compresslevel=9, fileobj=open(file_path, 'wb'))
        gzip_f.write(data)
        gzip_f.close()
        
        # file_desc = '{"filetype"="gz";"time"="' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '";"checksum"="' + calc_md5(file_path) + '";"filename"="' + file_name + '"}'
        file_desc = json.dumps({
            "filetype": "gz",
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "checksum": calc_md5(file_path),
            "filename": file_name
        })
        print file_desc
        
        boundary = '---------------------------7de1ae242c06ca'
        headers = {
            "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
            "Content-Type": "multipart/form-data;boundary=" + boundary,
            "cookie": cookie,
            "Content-Filedesc": file_desc
        }

        request_file = MultipartEncoder(
            fields={
                "file": (file_name, open(file_path, "rb"), "multipart/form-data")
            },
            boundary=boundary
        )
        r = session.post(ROOT_URL + "V1/net_audit/app_behavior", data=request_file, headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    set_num = 1
    device_id = DETECTOR_ID
    s = requests.Session()
    send_app_behavior(s, device_id, set_num)
