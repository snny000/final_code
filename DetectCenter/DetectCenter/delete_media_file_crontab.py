# -*- coding:utf-8 -*-
import os
import traceback
from datetime import datetime, timedelta
from DetectCenter import file_util as fu

remove_days = 60
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

exclude_file = ['rules.zip', 'detector_info.xlsx']

dir_path_list = [BASE_DIR + '/media/', BASE_DIR + '/log/']


def delete_media_file(days=remove_days, _dir_path_list=[BASE_DIR + '/media/']):
    for _dir in _dir_path_list:
        delete_media_file_detail(days=days, dir_path=_dir)


def delete_media_file_detail(days=remove_days, dir_path=BASE_DIR + '/media/'):
    try:

        # print '\n开始删除%s天前文件' % days, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_all = os.listdir(dir_path)
        for f in file_all:
            path = os.path.join(dir_path, f)
            if os.path.isfile(path):
                mtime = os.path.getmtime(path)
                if (datetime.now() - datetime.fromtimestamp(mtime)) > timedelta(days=days) and not os.path.split(path)[1] in exclude_file:
                    log_str = "%s %s" % ('刪除文件', path)
                    fu.string2log_append_per_day(log_str, path=BASE_DIR + '/log/remove_file_crontab/', prefix='delete', suffix='log')
                    os.remove(path)
            else:
                delete_media_file_detail(days=days, dir_path=path)
    except:
        traceback.print_exc()
