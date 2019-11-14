def aaa(d):
    d["a"] = "a"


def bbb(a):
    a = 2

if __name__ == "__main__":
    d = dict()
    aaa(d)
    print d

    a = 3
    bbb(a)
    print a



print 'abd'.find('aba')


ss = 'abababa'
ss = ss.replace('a', 'b')
print ss


# int(None)


print [][0: 1]
print [1, 2][0: 1]

import os
print os.path.splitext('aaa.jpg')[1]

print 'True'

print os.path.split('/aaaa/bbb')[1]

print 3 in [1, 2]

print os.path.join('/alidata', 'aaa')

import shutil
shutil.copy('./urls.py', './aaa/urlss.py')