# -*- coding: utf-8 -*-

import sys
# sys.path.append('..')

import django
import os

print "111111111111111111"
pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DetectCenter.settings")
#
django.setup()

# path = os.getcwd()
# print sys.path
# sys.path.append(path)       ###添加工程目录到python解析器的检索列表中，用于导入settings
# print sys.path
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DetectCenter.settings')
# django.setup()

print "22222222222222222"

import detect_center_reg_auth as dcra
from director import heartbeat

if __name__ == '__main__':
    print '1（注册认证），2（认证）3（发送心跳）'
    choice = raw_input("Input your choice: ")
    if choice == '1':
        dcra.send_register_request()
    elif choice == '2':
        print dcra.send_auth_login_request()
    elif choice == '3':
        heartbeat.heartbeat_2_director()
    else:
        print '输入错误，请重新运行程序！'
