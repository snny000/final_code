# -*- coding: utf-8 -*-

# Create your tests here.
import sys
sys.path.append('..')

# from DetectCenter import https_requests as requests
# from DetectCenter.director_config import *
#
#
# r = requests.post('http://192.168.120.234:8089/V1/jcc/reg_rs', data={'code': 1, 'detail': '审核通过', 'audit_time': '2017-12-29 12:12:12'})
# print r.text.encode('utf-8')
#
#
# h_data = {
#     "mem": 52,
#     "disk": 160,
#     "time": "2017-9-6 19:08:35",
#     "cpu": 15
# }
# h_header = {
#     'Src-Node': SRC_NODE,
#     'Src-Center': SRC_CENTER_ID,
#     'Content-Type': 'application/json',
#     'Channel-Tpye': 'JCQ',
# }
#
# h = requests.post('http://192.168.120.216:9001/V1/jcc/heartbeat', data=h_data, headers=h_header, cookies={'sessionid': 'q6hwhklyhowqkrqn4ppdu6tupjid2r0k'})
# print h.text.encode('utf-8')


print u'%s 啊啊啊' % u'不不不'

import json
print json.dumps([])

print set([1, 2]) - set([2, 3])

import os
path = 'aaa/dd.py'
print os.path.splitext(path)
print os.path.dirname(path)
tmp = path.split('/')
print tmp[len(tmp)-1]

print ['123', '123']


print json.loads(json.dumps([15256252]))

import math
print math.fabs(-1)

print 1 if [] else 2

from datetime import datetime
print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print "全量生成%s插件任务" % ("指挥中心" if 0 else "管理中心")

d = {1: 2}
print d.pop(1)
print d


def is_serial_id_overflow_errer(errors):
    """
    判断策略、任务组等入库数据中的serialID是否溢出
    :param errors:  rest-framework序列化的异常信息
    :return:
    """
    if errors is None:
        return False

    print errors
    errors_dict = {}
    if isinstance(errors, dict):
        errors_dict = errors.copy()
    if isinstance(errors, list):
        errors_dict = errors[0]
    tmp = {}
    for k, v in errors_dict.items():
        if len(v) == 1 and str(v[0]).find('9223372036854775807') != -1 and str(v[0]).find('equal') != -1:
            tmp[k] = v
    for k in tmp:
        if k in errors_dict:
            errors_dict.pop(k)
    print tmp, errors_dict
    if len(errors_dict) == 0:
        return True
    else:
        return False

print is_serial_id_overflow_errer({"group_id": ["Ensure this value is less than or equal to 9223372036854775807.", "fsjkldflsdkfjlds"], "rule_id": ["Ensure this value is less than or equal to 9223372036854775807."]})


from random import randint
print randint(1, 100)


from random import randint
import time
s = randint(0, 10) / 10.0
print s
time.sleep(s)
print 'aaaaaaaa'


print json.dumps({'a': None})

s = (1, 2, 3)
print 1 in s

def aaa(d):
    w = (1, 2)
    c_d = d.copy()
    for key in c_d:
        if key not in w:
            d.pop(key)
    return d

d = {1: 2, 3: 4}
d = aaa(d)
print d


print len({1: 2, 2: 3})


print str(None)

a = [{1: 2}]
b = [{2: 3}]
a.extend(b)
print a

print(False | False)

print (1, 2)[0]

a = (1, 1)
print a == (1, 1)
