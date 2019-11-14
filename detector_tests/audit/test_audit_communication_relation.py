# -*- coding:utf-8 -*-

import sys
sys.path.append('..')

from base import *


# 构造数据
def construct_data():
    data = ''
    # num = random.randint(1, 100000)
    num = 10
    i = 0
    while i < num:
        # net_log = {
            # 'sip': socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
            # 'sport': str(random.randint(1024, 65534)),
            # 'smac': '-'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
            # 'dip': socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
            # 'dport': str(random.randint(1024, 65534)),
            # 'dmac': '-'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
            # 'protocol': str(random.choice([6, 17])),
            # 'app': random.choice(['FTP', 'Telnet', 'SMTP', 'HTTP', 'RIP', 'NFS', 'DNS']),
            # 'tcp_flag': random.choice(['SYN', 'FIN', 'ACK', 'PSH', 'RST', 'URG']),
            # 'in_bytes': str(random.randint(100, 100000)),
            # 'out_bytes': str(random.randint(100, 100000)),
            # 'in_pkts': str(random.randint(10, 10000)),
            # 'out_pkts': str(random.randint(10, 10000)),
            # 'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 3600)),
            # 'end_time': time.strftime('%Y-%m-%d %H:%M:%S')
        # }
        net_log = [
            socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))), 
            str(random.randint(1024, 65534)), 
            '-'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
            socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))),
            str(random.randint(1024, 65534)),
            '-'.join(['%02x' % x for x in imap(lambda arg: random.randint(0, 255), range(6))]),
            str(random.choice([6, 17])),
            random.choice(['FTP', 'Telnet', 'SMTP', 'HTTP', 'RIP', 'NFS', 'DNS']),
            random.choice(['SYN', 'FIN', 'ACK', 'PSH', 'RST', 'URG']),
            str(random.randint(100, 100000)),
            str(random.randint(100, 100000)),
            str(random.randint(10, 10000)),
            str(random.randint(10, 10000)),
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 3600)),
            time.strftime('%Y-%m-%d %H:%M:%S')
        ]
        data += '#'.join(net_log)
        if i != num - 1:
            data += '\n'
        i += 1
    return num, data


def send_communication_relation(session, detector_id, limit_num):
    num, data = construct_data()
    if num <= limit_num:
        headers = {
            "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
            "Content-Type": "text/plain",
            "cookie": cookie
        }
        r = session.post(ROOT_URL + "V1/net_audit/net_log", data=data, headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    else:
        file_name = str(int(time.time())) + '.gz'
        file_path = TEST_PATH + 'audit_net_log/' + detector_id + '/'
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
            "Cookie": cookie,
            "Content-Filedesc": file_desc
        }

        request_file = MultipartEncoder(
            fields={
                "file": (file_name, open(file_path, "rb"), "multipart/form-data")
            },
            boundary=boundary
        )
        r = session.post(ROOT_URL + "V1/net_audit/net_log", data=request_file, headers=headers,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


if __name__ == '__main__':
    set_num = 1
    device_id = DETECTOR_ID
    s = requests.Session()
    send_communication_relation(s, device_id, set_num)
