# -*- coding: utf-8 -*-


from DetectCenter import config
import psutil
import time
import os
import json


def send_status_2_disposal():
	# 计算状态值
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

	# 写入文件
	file_dir = os.path.join(config.const.DISPOSAL_DIR, 'system_status')
	if not os.path.exists(file_dir):
		os.makedirs(file_dir)
	file_name = 'system_status_' + str(int(time.time())) + '_' + str(1)
	file_path = os.path.join(file_dir, file_name)
	f_handler = open(file_path, 'wb')
	f_handler.write(config.const.DISPOSAL_BOUNDARY + '\n')
	f_handler.write('Type:status(system)\n')
	f_handler.write(data)
	f_handler.close()


if __name__ == '__main__':
	send_status_2_disposal()