# -*- coding: utf-8 -*-

import threading
import time
import os

mutexes = {}   # 创建一个文件-锁的字典


def string2file(content, path="../log/", name="access.log"):
    filename = path + name
    if filename in mutexes:
        mu = mutexes[filename]
    else:
        mu = threading.Lock()
        mutexes[filename] = mu

    if mu.acquire(True):   # 获取锁状态
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception:
            print "路径已被创建"
        if os.path.exists(filename):
            fp = open(filename, 'a+')
        else:
            try:
                os.mknod(filename)
            except Exception:
                print "文件已被创建"
            fp = open(filename, 'a+')
        try:
            fp.write(content + '\n')
            fp.flush()
        except:
            print "write error"
        finally:
            fp.close()
            mu.release()  # 释放锁


def string2log_per_day(content, path="../log/", prefix="access", suffix="log"):
    date = time.strftime('%Y%m%d', time.localtime())
    name = prefix + date + suffix
    content = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '] ' + content
    string2file(content, path, name)
