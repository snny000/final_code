# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:35:14 2017

@author: Mirror
"""
# import requests
import DetectCenter.https_requests as requests
from requests_toolbelt import MultipartEncoder

import time
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout, HTTPError, TooManyRedirects

import datetime
import json
import os
import DetectCenter.file_util as fu


# session = requests.Session()
#
# def post(session=None, url=None, data=None, headers=None, verify=True):
#
#     r = ''
#     if url.split(':')[0] == 'https':
#         r = session.post(url, headers=headers, data=data,
#                          verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
#     elif url.split(':')[0] == 'http':
#         r = session.post(url, headers=headers, data=data, verify=False)
#     # print r.status_code
#     # print r.headers
#     # print r.text.encode('utf-8')
#     return r

def getSizeIntoString(sizeInBytes):
    byte_str = ''
    tmp = int(sizeInBytes)
    for (cutoff, label) in [(1024*1024*1024, "GB"), (1024*1024, "MB"), (1024, "KB")]:
        if tmp >= cutoff:
            byte_str += "%d %s, " % (tmp / cutoff, label)
            tmp = tmp % cutoff
    if tmp == 1:
        byte_str += "1 byte"
    elif tmp == 0:
        pass
    else:
        byte_str += str(tmp) + ' bytes'
    return byte_str

def getTimeIntoString(timeInMS):
    byte_str = ''
    tmp = int(timeInMS)
    for (cutoff, label) in [(60*60*1000, "Hour"), (60*1000, "Min"), (1000, "Sec")]:
        if tmp >= cutoff:
            byte_str += "%d %s, " % (tmp / cutoff, label)
            tmp = tmp % cutoff
    if tmp == 0:
        pass
    else:
        byte_str += str(tmp) + ' MSec'
    return byte_str


if __name__ == "__main__":

    # send_url_A = 'http://192.168.120.75:9009/msg/aaa'
    # send_url_A = 'http://192.168.120.75/msg/aaa'
    send_url_A = 'https://192.168.120.234:443/msg/aaa'

    code200 = 0L
    code500 = 0L
    codeErr = 0L

    #session = requests.Session()

    start = int(time.time() * 1000)
    # for i in xrange(10000):
    while 1:
        date = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        try:
            start2 = int(time.time() * 1000)

            # requests.post(send_url_A)
            r = requests.post(send_url_A, data={'a': 1})
            print r.status_code  # 响应码
            print r.headers  # 响应头
            print r.text.encode('utf-8')  # 响应消息正文
            end2 = int(time.time() * 1000)
            print 'url:%s    runtime: %d' % (send_url_A, (end2 - start2))
            code200 += 1
        except ConnectTimeout, e:
            codeErr += 1
            str_log = "Date: %s  链接超时异常: %s   消息类型： 消息 \n" % (date, str(e).encode('utf-8'))
            print str_log
            fu.string2file(str_log, "./log/", "ConnectError.log")
            print ""
        except ConnectionError, e:
            codeErr += 1
            str_log = "Date: %s  无法链接异常: %s   消息类型： 消息 \n" % (date, str(e).encode('utf-8'))
            print str_log
            fu.string2file(str_log, "./log/", "ConnectError.log")
        except ReadTimeout, e:
            codeErr += 1
            str_log = "Date: %s  本地超时异常: %s   消息类型： 消息 \n" % (date, str(e).encode('utf-8'))
            print str_log
            fu.string2file(str_log, "./log/", "ConnectError.log")
        except HTTPError, e:
            codeErr += 1
            str_log = "Date: %s  HTTP异常: %s   消息类型： 消息 \n" % (date, str(e).encode('utf-8'))
            print str_log
            fu.string2file(str_log, "./log/", "ConnectError.log")
        except TooManyRedirects, e:
            codeErr += 1
            str_log = "Date: %s  重定向过多异常: %s   消息类型： 消息 \n" % (date, str(e).encode('utf-8'))
            print str_log
            fu.string2file(str_log, "./log/", "ConnectError.log")
        except Exception, e:
            codeErr += 1
            str_log = "Date: %s  未知链接异常: %s   消息类型： 消息 \n" % (date, str(e).encode('utf-8'))
            print str_log
            fu.string2file(str_log, "./log/", "ConnectError.log")

        end = int(time.time() * 1000)

        str_log = "进程：%d \n时间：%s \n链接成功：%d \n流转异常：%d \n链接失败：%d \n已运行: %s\n\n" \
                  % (os.getpid(), date, code200, code500, codeErr, getTimeIntoString(end - start))

        fu.string2file(str_log, "./log/", "Stress.log")

