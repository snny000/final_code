# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from base import *


def send_register_request(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json"
    }

    interface = [
        {"ip": "192.168.120.136", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:88", "manage": True},
        {"ip": "192.168.120.146", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:89", "manage": False},
        {"ip": "192.168.120.156", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:90", "manage": False},
    ]
    cpu = [
        {"physical_id": 0, "core": 4, "clock": 2.3},
        {"physical_id": 1, "core": 4, "clock": 2.5}
    ]
    disk = [
        {"serial": "6Y200M006500A", "size": 4096},
        {"serial": "6Y200M006500B", "size": 2048},
        {"serial": "6Y200M006500C", "size": 2048},
        {"serial": "6Y200M006500D", "size": 4096},
        {"serial": "6Y200M006500E", "size": 2048},
        {"serial": "6Y200M006500F", "size": 4096}
    ]
    register_data = {
        "device_type": "01",
        "soft_version": device_version,
        "organs": "iie",
        "address": "北京市海淀区闵庄路甲89号",
        "address_code": "100000",
        "contact": [
            {"name": "Quennel", "phone": "13200007921", "email": "quennel@gmail.com", "position":"程序员"},
            {"name": "Peter", "phone": "13598273981", "email": "peter@sina.com", "position": "项目经理"},
            {"name": "Neil", "phone": "13981032671", "email": "neil@yahoo.com", "position": "测试员"},
        ],
        "interface": interface,
        "cpu_info": cpu,
        "disk_info": disk,
        "mem_total": 2048,
        "memo": "首次注册",
        "device_ca": 'iie',
    }
    r = session.post(ROOT_URL + "V1/register/reg_request",
                     data=json.dumps(register_data), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


def send_re_register_request(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json"
    }

    interface = [
        {"ip": "192.168.121.136", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:88", "manage": True},
        {"ip": "192.168.121.146", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:89", "manage": False},
        {"ip": "192.168.121.156", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:90", "manage": False},
    ]
    cpu = [
        {"physical_id": 0, "core": 4, "clock": 2.8},
        {"physical_id": 1, "core": 4, "clock": 2.5}
    ]
    disk = [
        {"serial": "7Y200M006500A", "size": 2048},
        {"serial": "7Y200M006500B", "size": 2048},
        {"serial": "7Y200M006500C", "size": 2048},
        {"serial": "7Y200M006500D", "size": 4096},
        {"serial": "7Y200M006500E", "size": 4096},
        {"serial": "7Y200M006500F", "size": 4096}
    ]
    register_data = {
        "device_type": "01",
        "soft_version": device_version,
        "organs": "iie",
        "address": "北京市海淀区复兴路128号区政府互联网接入机房F-12",
        "address_code": "100036",
        "contact": [
            {'name': '赵一鸣', 'phone': '13589234719', 'email': 'zhaoyiming@163.com', 'position': '项目经理'},
            {'name': '钱二磊', 'phone': '13689341988', 'email': 'qianerlei@gmail.com', 'position': '产品经理'},
            {'name': '孙富贵', 'phone': '13884232675', 'email': 'sunfugui@gmail.com', 'position': '程序员'},
        ],
        "interface": interface,
        "cpu_info": cpu,
        "disk_info": disk,
        "mem_total": 4096,
        "memo": "设备变更",
        "device_ca": 'iie',
    }
    r = session.post(ROOT_URL + "V1/register/re_reg_request",
                     data=json.dumps(register_data), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')


def send_register_status_request(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json"
    }
    r = session.get(ROOT_URL + "V1/register/regstatus", headers=headers,
                    verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')
    if r.status_code == 200:
        return json.loads(r.text.encode('utf-8')).get('type')
    else:
        return -1


def send_auth_login_request(session, detector_id):
    headers = {
        "User-Agent": "{0}/{1}({2})".format(detector_id, device_version, vendor_name),
        "Content-Type": "application/json",
        # "Cookie": cookie
    }

    interface = [
        {"ip": "192.168.120.136", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:88",
         "manage": True},
        {"ip": "192.168.120.146", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:89",
         "manage": False},
        {"ip": "192.168.120.156", "netmask": "192.168.0.0/24", "gateway": "192.168.1.254", "mac": "00:0d:48:09:4e:90",
         "manage": False},
    ]
    cpu = [
        {"physical_id": 0, "core": 4, "clock": 2.3},
        {"physical_id": 1, "core": 4, "clock": 2.5}
    ]
    disk = [
        {"serial": "6Y200M006500A", "size": 4096},
        {"serial": "6Y200M006500B", "size": 2048},
        {"serial": "6Y200M006500C", "size": 2048},
        {"serial": "6Y200M006500D", "size": 4096},
        {"serial": "6Y200M006500E", "size": 2048},
        {"serial": "6Y200M006500F", "size": 4096}
    ]
    auth_data = {
        "device_type": "01",
        "interface": interface,
        "mem_total": 2048,
        "cpu_info": cpu,
        "disk_info": disk,
        "soft_version": device_version,
    }

    r = session.post(ROOT_URL + "V1/auth/login",
                     data=json.dumps(auth_data), headers=headers,
                     verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')

    if r.status_code == 200 and json.loads(r.text.encode('utf-8'))['type'] == 0:
        cookie_list = r.headers.get('Set-Cookie').split(';')
        if cookie_list is not None:
            for cookie in cookie_list:
                if str(cookie).find('SESSION') != -1:
                    l = cookie.split(',')
                    if l is not None:
                        for ll in l:
                            if str(ll).find('SESSION') != -1:
                                session = str(ll).strip()


if __name__ == '__main__':
    device_id = DETECTOR_ID
    s = requests.Session()
    print '1（注册认证），2（只是认证），3（重新注册认证）'
    choice = raw_input("Input your choice: ")
    if choice == '1':
        send_register_request(s, device_id)
        while True:
            flag = send_register_status_request(s, device_id)
            if flag == 0:   # 注册成功
                send_auth_login_request(s, device_id)
                break
            elif flag == 2: # 注册审核中
                time.sleep(30)
            else:           # 注册失败或服务器处理请求失败
                break
    elif choice == '2':
        send_auth_login_request(s, device_id)
    elif choice == '3':
        send_re_register_request(s, device_id)
        while True:
            flag = send_register_status_request(s, device_id)
            if flag == 0:   # 注册成功
                send_auth_login_request(s, device_id)
                break
            elif flag == 2: # 注册审核中
                time.sleep(30)
            else:           # 注册失败或服务器处理请求失败
                break
    else:
        print '输入错误，请重新运行程序！'
