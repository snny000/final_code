# -*- coding: utf-8 -*-
import time
import traceback
from DetectCenter.director_config import *
import json
from DetectCenter import sender, config
from DetectCenter import hardware_util as hu, print_util as pu
from detect_center_reg_auth import check_global_director_connection

def task_heartbeat():
    if config.const.DIRECTOR_VERSION and check_global_director_connection():
        heartbeat_2_director()


def heartbeat_2_director():
    print '发送心跳到指挥中心'
    import psutil
    try:
        time.sleep(1)

        cpu_usage_list = []
        cpu_info = hu.CPUinfo()
        cpu_usage = psutil.cpu_percent(interval=2, percpu=True)
        print cpu_usage
        count = 1
        cpu_cores = len(cpu_usage) / len(cpu_info)
        import math
        fre = 0.0
        for per in cpu_usage:
            if count % cpu_cores == 0:
                print 'fre:', fre
                cpu_usage_list.append({'physical_id': count / cpu_cores - 1, 'cpu_usage': round(fre / cpu_cores, 1)})
                fre = 0.0
            else:
                fre += per
            count += 1

        mem_usage = int(psutil.virtual_memory().percent)
        disk_usage = int(psutil.disk_usage('/').free / 1024 / 1024 / 1024)  # 单位GB

        headers = {
            'Src-Node': SRC_NODE,
            'Src-Center': SRC_CENTER_ID,
            'Content-Type': 'application/json',
            'Channel-Tpye': 'JCQ',
            'User-Agent': CENTER_USER_AGENT,
            'X-Forwarded-For': detect_center_host
        }

        command_data = json.dumps({
            'mem': mem_usage,
            'cpu': cpu_usage_list,
            'disk': disk_usage,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }, ensure_ascii=False).encode('utf-8')

        # pu.pretty_print(command_data)

        sender.send_director(send_director_A + 'heartbeat', SRC_CENTER_ID, "CENTER_HEARTBEAT", headers, command_data)

    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    pass