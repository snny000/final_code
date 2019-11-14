# -*- coding: utf-8 -*-
from django.test import TestCase

# Create your tests here.

a = ("a", "b")

for x in a:
    print x

b = list()
# b.append()
#
# len()

{"plug_type": "detect", "plug_id": 1111111111, "plug_version": "1111", "plug_config_version": "2222", "cpu": 1, "mem": 1, "disk": 1, "plug_path": "test/20171204_1245.txt", "plug_config_path": "test/20171204_1246.txt"}


c = {'a': 2}
print c['a']

print ('abd' in 'abdf')


def generate_plug_on_device_status_dict(stat=''):
    result = dict()
    if stat is None or stat == '' or len(stat) < 2:
        pass
    else:
        device_status_list = stat[1:-1].split('#')
        for ll in device_status_list:
            temp = ll.split(':')
            if temp and len(temp) == 2:
                result[temp[0]] = temp[1]
    return result


def generate_plug_on_device_status_str(dict={}):
    result = ''
    if dict is None or len(dict) == 0:
        pass
    else:
        temp = list()
        for k, v in dict.items():
            temp.append(str(k) + ':' + str(v))
        result = '#' + '#'.join(temp) + '#'
    return result

d= generate_plug_on_device_status_dict('#123:1#1234:1#')

print d

ss = generate_plug_on_device_status_str(d)

print ss

print '中国'

# 查找2个字典的交集和并集 指的是键

dict1 = {1: 2, 2: 3}
dict2 = {1: 2, 4: 3}

# 并集
union = dict(dict1, **dict2)
print union

# 交集
# for要用循环次数小的 可以提高性能
inter = [x for x in dict1 if x in dict2]
print inter

for k in dict1:
    if k in dict2:
        dict2.pop(k)

print dict2

print isinstance(1, int)

# from rest_framework.response import Response

# a = Response('', 200, headers={}, content_type='application/json;charset=utf-8')

# print isinstance(a, Response)

s = set([1, 1, 1, 2])
print [v for v in s]