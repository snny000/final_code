
# Create your tests here.
import sys
sys.path.append('..')
from datetime import datetime, timedelta

aa = None
print (datetime.now() - (aa if aa is not None else (datetime.now() - timedelta(minutes=4))))

starttime = datetime.now()
#long running
endtime = datetime.now() - timedelta(minutes=4)
print endtime
print (endtime - starttime)




print int('2305843022098596108')
print int('9322486700791824108')


# print {'META': {'a': 1}}.META.get('a')


l1 = [{
    'ip': '123',
    'mac': '123'
}]

l2 = [{
    'mac': '123',
    'ip': '123'
}]

import json

l3 = [{
    'ip': '1',
    'mac': '2'
}, {
    'ip': '3',
    'mac': '4'
}]
l4 = [{
    'ip': '3',
    'mac': '4'
}, {
    'ip': '1',
    'mac': '2'
}]

l5 = [{
    'ip': '1',
    'mac': '2'
}, {
    'mac': '4',
    'ip': '3'
}]
# print set(l3).difference(set(l4))
# print set([1, 2]) - set([2, 1])

for i in [11, 21, 31]:
    print i

print(set([1, 2]).__len__())


def is_list_ele_equal(list1, list2):
    import copy
    l1 = copy.deepcopy(list1)
    l2 = copy.deepcopy(list2)
    for i in range(l1.__len__()):
        l1[i] = json.dumps(l1[i])
    for i in range(l2.__len__()):
        l2[i] = json.dumps(l2[i])
    print set(l1)
    print set(l2)
    if set(l1).difference(set(l2)).__len__() == 0:
        return True
    else:
        return False


print is_list_ele_equal(l3, l4)
print is_list_ele_equal(l3, l5)
print l3 == l4


print {'ip': '3', 'mac': '4'} == {'mac': '4', 'ip': '3'}
print json.dumps({'ip': '3', 'mac': '4'}) == json.dumps({'mac': '4', 'ip': '3'})