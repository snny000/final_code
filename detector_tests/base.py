# -*- coding: utf-8 -*-

from requests_toolbelt import MultipartEncoder
from itertools import imap
import requests
import json
import time
import random
import socket
import struct
import hashlib
import gzip
import os
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ROOT_URL = 'https://192.168.120.234/'   # 服务器URL
ROOT_URL = 'https://219.143.226.98/'
TEST_PATH = BASE_DIR + '/test_files/'   # 测试文件上传时的文件路径

# CA证书路径（根证书路径，客户端证书和私钥路径）
CA_CRT_PATH = BASE_DIR + '/certificates/private/ca.crt'
CLIENT_CRT_PATH = BASE_DIR + '/certificates/server/client.crt'
CLIENT_KEY_PATH = BASE_DIR + '/certificates/server/client.key'

print "CA_PATH:", CA_CRT_PATH

# 测试用检测器ID
DETECTOR_ID = '180306010001'

# 测试用cookie（认证之后会改变）
#cookie = 'SESSION=jxpu632355f5f141vx5f1tnw0vwqr0h'
#cookie = 'SESSION=9582zki1t8knfvb3iiucirjp1dp3e6v4'
cookie = 'SESSION=jioptdon4ute1towlir7q2e61er9uvty'

# 检测器版本号
device_version = '20180124_1234'

# 厂商英文名
vendor_name = 'IIE'


# 获取文件的md5值
def calc_md5(file_path):
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()


# 从文件的offset位置读取length长度字符，默认读取全部
def read_file(file_path, offset=0, length=-1):
    if length == 0:
        length = -1
    f = open(file_path, 'rb')
    f.seek(offset)
    data = f.read(length)
    f.close()
    return data


# 获取base64编码
def get_base64(string):
    return base64.b64encode(string)


# 获取MD5值
def get_md5(string):
    md5obj = hashlib.md5()
    md5obj.update(string)
    return md5obj.hexdigest()

