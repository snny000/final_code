# -*- coding: utf-8 -*-

import psutil
import time
import os
import json


handle_dir = '/alidata/DetectorManagement/businessDisposition/'
system_audit_flag = 1
file_dir = handle_dir + 'system_audit/'
if not os.path.exists(file_dir):
    os.makedirs(file_dir)
file_name = 'system_audit_' + str(int(time.time())) + '_' + str(system_audit_flag)
file_path = file_dir + file_name
f_handler = open(file_path, 'wb')
f_handler.write('---------------------------7d81741d1803de--------------\n')
f_handler.write('Type:audit(system)\n')
mem_usage = str(psutil.virtual_memory().percent) + '%'
# psutil.swap_memory().percent
# time.sleep(1)
cpu_usage = str(psutil.cpu_percent(interval=1.0)) + '%'
disk_usage = str(psutil.disk_usage('/').percent) + '%'

data = json.dumps({
    'mem_usage': mem_usage,
    'cpu_usage': cpu_usage,
    'disk_usage': disk_usage,
    'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
})
f_handler.write(data)
f_handler.close()
