# -*- coding: utf-8 -*-
from django.test import TestCase

# Create your tests here.

dict = {"id": 0, "name": "木马攻击任务组", "rule_type": 1, "create_person": "admin", "remarks": "test"}
operate_list = []
operate_map = {'add': 1, 'del': 2, 'change': 3, 'group': 4, '': 5}
operate_list.append(operate_map[u'change'])
print operate_list


t = (1, 2)
print t.index(2)
l = list(t)
l[t.index(2)] = 3
print tuple(l)


print 1 * 1.0 / 3

print int(1 * 1.0 / 3 * 100)


print 'aaa'.find('aa')

import json
print json.dumps({'qqwww': u'哈哈哈哈'}, encoding='utf-8')

print 'aaa' + json.dumps({'qqwww': u'哈哈哈哈'}, ensure_ascii=False).encode('utf-8')