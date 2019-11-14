# -*- coding: utf-8 -*-
import base64
import hashlib


# 获取base64编码
def get_base64(string):
    return base64.b64encode(string)


# 获取MD5值
def get_md5(string):
    md5obj = hashlib.md5()
    md5obj.update(string)
    return md5obj.hexdigest()


# 获取文件的md5值(每次读取一部分进行计算，避免一次性读取大文件)
def calc_md5(file_path, chunk_size=512):
    md5obj = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            md5obj.update(data)
    return md5obj.hexdigest()
