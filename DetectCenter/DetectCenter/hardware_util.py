# -*- coding: utf-8 -*-

from collections import OrderedDict
import traceback

def CPUinfo():
    """
    Return the info in /proc/cpuinfo as a dirctionary in the follow format:
    [{'physical_id': , 'core': , 'clock': }, ...]

    """

    CPUinfo = OrderedDict()
    procinfo = OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                # end of one processor
                CPUinfo['proc%s' % nprocs] = procinfo
                nprocs = nprocs + 1
                # Reset
                procinfo = OrderedDict()
            else:
                if line.split(':')[0].strip() in ['physical id', 'core id', 'cpu cores', 'cpu MHz', 'model name', 'processor']:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()

    if not len(CPUinfo):
        return []

    # VPrint(CPUinfo)
    cpu_msg = []
    physical_id = int(CPUinfo['proc0']['physical id'])
    final_physical_id = 0
    count = 0
    frequency = 0.0
    for procinfo in CPUinfo.values():
        if int(procinfo['physical id']) == physical_id:
            frequency += float(str(procinfo['model name'])[str(procinfo['model name']).find('@') + 1: str(procinfo['model name']).find('GHz')].strip())
            count += 1
            if count == int(procinfo['cpu cores']):
                d = {'physical_id': final_physical_id, 'core': count, 'clock': round(frequency / count, 2)}
                cpu_msg.append(d)
        else:
            count = 1
            frequency = float(str(procinfo['model name'])[str(procinfo['model name']).find('@') + 1: str(procinfo['model name']).find('GHz')].strip())
            physical_id = int(procinfo['physical id'])
            final_physical_id += 1

    return cpu_msg


def mem_total():
    """
    获取内存总量 单位MB
    :return:
    """
    with open('/proc/meminfo') as f:
        for line in f:
            if line.find('MemTotal') != 1:
                return int(float(line.split(':')[1].strip()[0:line.split(':')[1].strip().find('kB')-1]) / 1024.0)


def disk_info():
    import psutil
    return [{'serial': 'ST1000NM0011', 'size': psutil.disk_usage('/').total / 1024 / 1024 / 1024}]



def interface_info():
    """
    获取系统的网卡信息，包括ip, mac, netmask, gateway, manage
    """
    import os
    import sys

    try:
        import netifaces
    except ImportError:
        try:
            command_to_execute = "pip install netifaces || easy_install netifaces"
            os.system(command_to_execute)
        except OSError:
            print "Can NOT install netifaces, Aborted!"
            sys.exit(1)
        import netifaces

    interface_info = []

    print "网关", netifaces.gateways()
    print "网卡名", netifaces.interfaces()

    GATEWAY = netifaces.gateways()['default'][netifaces.AF_INET][0]
    netmask = '255.255.255.0'
    for interface in netifaces.interfaces():
        # print interface
        # print netifaces.ifaddresses(interface)
        if interface == 'lo':
            pass
        else:
            mac_addr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            try:
                ip_addr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                netmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
                if ip_addr == GATEWAY:
                    manage = True
                else:
                    manage = False
                interface_info.append({'ip': ip_addr, 'mac': mac_addr, 'gateway': GATEWAY, 'netmask': netmask, 'manage': manage})
            except Exception as e:
                interface_info.append({'ip': '127.0.0.1', 'mac': mac_addr, 'gateway': GATEWAY, 'netmask': netmask, 'manage': False})
                # print "#############"
                # print traceback.print_exc()

    # VPrint(interface_info)
    return interface_info

import json
def VPrint(content):
    print json.dumps(content, encoding='utf-8', ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # print '#####' + u'哈哈'
    # print '#####' + '哈哈'
    # cpu_msg = CPUinfo()
    # VPrint(cpu_msg)
    # print mem_total()
    # VPrint(interface_info())
    import psutil
    print psutil.disk_usage('/')
    print psutil.disk_partitions()