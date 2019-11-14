# -*- coding: utf-8 -*-

import sys
# sys.path.append('..')


from DetectCenter import director_config as dc
from DetectCenter import https_requests as requests, date_util as du, queryset_util as qu, hardware_util as hu

from director.models import ManagementCenterInfo
from director.director_serializers import ManagementCenterInfoSerializer
from DetectCenter import print_util as pu, config
from django.core.serializers import serialize
from django.db.models import F
import json
import traceback


def check_global_director_connection():
    center_info = ManagementCenterInfo.objects.all()
    if center_info.exists() and center_info[0].center_status == 1:
        # print "管理中心已接入指挥中心"
        return True
    else:
        # print "管理中心未接入指挥中心"
        return False

# 获取管理中心的静态注册数据，实际生产中使用pyutil工具获取
def get_center_data():
    interface = hu.interface_info()

    cpu = hu.CPUinfo()

    disk = hu.disk_info()

    contact = [
        {"phone": "18210331668", "email": "wwenan@gmail.com", "name": "wwenan", "position": "程序员"},
        {"phone": "18210331668", "email": "wangxingxing@sina.com", "name": "wangxingxing", "position": "程序员"}
    ]

    register_data = {

        'center_id': dc.SRC_CENTER_ID,
        'soft_version': dc.SOFT_VERSION,
        'device_ca': dc.DEVICE_CA,
        'organs': dc.ORGANS,
        'address': dc.ADDRESS,
        'address_code': dc.ADDRESS_CODE,
        'contact': json.dumps(contact, encoding='utf-8', ensure_ascii=False),
        # 'contact': contact,
        'mem_total': hu.mem_total(),
        'interface': json.dumps(interface),
        # 'interface': interface,
        'cpu_info': json.dumps(cpu),
        # 'cpu_info': cpu,
        'disk_info': json.dumps(disk)
        # 'disk_info': disk
        # 'access_time': du.get_current_date_string()
    }
    return register_data


def send_register_request(url=dc.send_director_A + 'reg', src_center_id=dc.SRC_CENTER_ID, center_serial=dc.CENTER_SERIAL, src_node=dc.SRC_NODE, src_ip=dc.director_host, ip_whitelist=[dc.director_host, '172.17.0.1'], retract=0):
    try:
        pu.print_format_header('管理中心发起注册', retract=retract)
        
        headers = {
            'Src-Node': src_node,
            'Src-Center': src_center_id,
            'Content-Type': 'application/json',
            'Channel-Tpye': 'JCQ',
            'User-Agent': dc.CENTER_USER_AGENT,
            'X-Forwarded-For': dc.detect_center_host
        }

        register_data = get_center_data()

        register_data['center_id'] = src_center_id
        register_data['center_ip'] = dc.detect_center_host
        register_data['center_serial'] = center_serial
        register_data['src_node'] = src_node
        register_data['src_ip'] = src_ip
        register_data['ip_whitelist'] = json.dumps(ip_whitelist)
        # del copy_data['access_time']
        register_data['register_time'] = du.get_current_date_string()
        register_data['id'] = 1

        # pretty_print(register_data)
        management_center = ManagementCenterInfo.objects.filter(center_id=dc.SRC_CENTER_ID)
        if not management_center.exists():
            ManagementCenterInfo.objects.all().delete()
            ManagementCenterInfo.objects.create(**register_data)
            # serializer = ManagementCenterInfoSerializer(data=register_data)
            # if serializer.is_valid():
            #     serializer.save()
            # else:
            #     print 'save management center', serializer.errors
        else:
            del register_data['register_time']
            management_center.update(**register_data)

        management_center = ManagementCenterInfo.objects.filter(center_id=dc.SRC_CENTER_ID)
        data = serialize('json', management_center,
                         fields=('center_id', 'soft_version', 'device_ca', 'organs', 'address', 'address_code',
                                 'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info')
                         )  # 序列化
        list_data = json.loads(data)
        register_data = list_data[0]['fields']
        register_data['cpu_info'] = json.loads(register_data['cpu_info'])
        register_data['disk_info'] = json.loads(register_data['disk_info'])
        register_data['interface'] = json.loads(register_data['interface'])
        register_data['contact'] = json.loads(register_data['contact'])

        print "register_data:", pu.pretty_print_format(register_data)

        r = requests.post(url, data=json.dumps(register_data), headers=headers)
        # pu.print_with_retract(r.status_code, retract + 1)  # 响应码
        pu.print_with_retract(r.headers, retract + 1)  # 响应头
        pu.print_with_retract(r.text.encode('utf-8'), retract + 1)  # 响应消息正文

        result = json.loads(r.text.encode('utf-8'))

        center_info = ManagementCenterInfo.objects.filter(center_id=dc.SRC_CENTER_ID)
        if r.status_code == 200:              # （0：注册成功；1：注册失败；2：注册未审核）  #  (0: 认证成功  1：认证失败 2: 未认证)
            # if result["msg"] != u'该管理中心的已存在':
            center_info.update(center_status=2, register_frequency=F('register_frequency') + 1, register_status=2, register_fail_reason='未审核',
                                                                                   auth_frequency=0, auth_status=2, auth_fail_reason='未认证', cookie=None)
        elif result['msg'] == u'该管理中心的已存在':
            if center_info[0].register_status == 0 and center_info[0].auth_status == 0:  # 管理中心主动重置与指挥的连接状态
                center_info.update(register_time=du.get_current_time(), register_frequency=F('register_frequency') + 1)
                send_auth_login_request()
        config.const.DIRECTOR_VERSION = True
        config.const.UPLOAD_DIRECTOR = True

        pu.print_format_tail('管理中心发起注册', retract=retract)
        return result
    except:
        traceback.print_exc()


def send_auth_login_request(retract=0, url=dc.send_director_A + 'login'):
    try:
        pu.print_format_header('管理中心发起认证', retract=retract)

        center_info = ManagementCenterInfo.objects.all()
        result = None
        if center_info.exists():

            headers = {
                'Src-Node': center_info[0].src_node,
                'Src-Center': center_info[0].center_id,
                'Content-Type': 'application/json',
                'Channel-Tpye': 'JCQ',
                'User-Agent': center_info[0].center_id + '/' + center_info[0].soft_version + '(' + center_info[0].organs + ')',
                'X-Forwarded-For': center_info[0].center_ip
            }
            if center_info[0].register_status == 2:
                pu.print_with_retract(u"管理中心" + center_info[0].center_id + u"还未审核，请等待审核完毕")
                result = {'code': 400, 'msg': u"管理中心" + center_info[0].center_id + u"还未审核，请等待审核完毕"}
            elif center_info[0].register_status == 1:
                pu.print_with_retract(u"管理中心" + center_info[0].center_id + u"审核失败，请核对指挥中心的管理中心备案信息，重新注册")
                send_register_request(src_center_id=center_info[0].center_id, center_serial=center_info[0].center_serial, src_node=center_info[0].src_node, src_ip=center_info[0].src_ip, ip_whitelist=center_info[0].ip_whitelist)
                result = {'code': 400, 'msg': u"管理中心" + center_info[0].center_id + u"审核失败，请核对指挥中心的管理中心备案信息，重新注册"}

            else:
                data = serialize('json', center_info,
                                 fields=('center_id', 'soft_version', 'device_ca', 'organs', 'address', 'address_code',
                                         'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info')
                                 )  # 序列化
                list_data = json.loads(data)
                auth_data = list_data[0]['fields']
                # auth_data['access_time'] = du.get_current_date_string()

                auth_data['cpu_info'] = json.loads(auth_data['cpu_info'])
                auth_data['disk_info'] = json.loads(auth_data['disk_info'])
                auth_data['interface'] = json.loads(auth_data['interface'])
                auth_data['contact'] = json.loads(auth_data['contact'])

                print 'auth_data:', pu.pretty_print_format(auth_data)

                r = requests.post(url, data=json.dumps(auth_data), headers=headers)
                # pu.print_with_retract(r.status_code, retract + 1)  # 响应码
                pu.print_with_retract(r.headers, retract + 1)  # 响应头
                pu.print_with_retract(r.text.encode('utf-8'), retract + 1)  # 响应消息正文

                result = json.loads(r.text.encode('utf-8'))

                if result['code'] == 200 and result['msg'] != u'已经接入，无需再次接入':
                    # print '认证成功'
                    header_cookie = r.headers.get('Set-Cookie', None)
                    if header_cookie is not None:
                        cookie_list = header_cookie.split(';')
                        if cookie_list is not None:
                            for cookie in cookie_list:
                                if str(cookie).find('session') != -1:
                                    l = cookie.split(',')
                                    if l is not None:
                                        for ll in l:
                                            if str(ll).find('session') != -1:
                                                dc.CENTER_COOKIE = {
                                                    str(ll.split('=')[0].strip()): str(ll.split('=')[1])}
                    if header_cookie is not None:
                        center_info.update(center_status=1, auth_time=du.get_current_time(),
                                           auth_frequency=F('auth_frequency') + 1,
                                           auth_status=0, auth_fail_reason='认证成功', cookie=json.dumps(dc.CENTER_COOKIE))
                    else:
                        center_info.update(center_status=1, auth_time=du.get_current_time(),
                                           auth_frequency=F('auth_frequency') + 1,
                                           auth_status=0, auth_fail_reason='认证成功')
                    dc.CENTER_COOKIE = json.loads(center_info[0].cookie, encoding='utf-8')
                    from audit.data_processing import send_detector_info, send_audit
                    from rest_framework.request import Request
                    from director import heartbeat
                    heartbeat.heartbeat_2_director()  # 发送心跳
                    if center_info[0].auth_frequency == 1:
                        send_detector_info(Request, retract=retract+1)         # 发送管理中心所有的检测器信息
                    send_audit(Request, retract=retract+1)                 # 发送管理中心自身审计日志
                elif result['msg'] == u'已经接入，无需再次接入':
                    center_info.update(auth_time=du.get_current_time(), auth_frequency=F('auth_frequency') + 1,
                                       auth_status=0, auth_fail_reason='认证成功', center_status=1)
                else:
                    # print '认证失败'
                    center_info.update(center_status=5, auth_time=du.get_current_time(), auth_frequency=F('auth_frequency') + 1, auth_status=1, auth_fail_reason=result['msg'], cookie=None)

        pu.print_format_tail('管理中心发起认证', retract=retract)
        return result
    except:
        traceback.print_exc()

#
# if __name__ == '__main__':
#     print '1（注册），2（认证）'
#     choice = raw_input("Input your choice: ")
#     if choice == '1':
#         send_register_request()
#     elif choice == '2':
#         print send_auth_login_request()
#     else:
#         print '输入错误，请重新运行程序！'
