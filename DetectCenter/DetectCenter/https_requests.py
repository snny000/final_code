# -*- coding: utf-8 -*-
import requests
from DetectCenter.director_config import *


session = requests.Session()

def post(url=None, data=None, headers=None, verify=True, cookies=None):

    # print 'headers:', headers

    r = ''
    if url.split(':')[0] == 'https':
        r = session.post(url, headers=headers, data=data, cookies=cookies,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    elif url.split(':')[0] == 'http':
        r = session.post(url, headers=headers, data=data, cookies=cookies, verify=False)
    # print r.status_code
    # print r.headers
    # print r.text.encode('utf-8')
    return r


def get(url=None, data=None, headers=None, verify=True, cookies=None):

    # print 'headers:', headers

    r = ''
    if url.split(':')[0] == 'https':
        r = session.get(url, headers=headers, params=data, cookies=cookies,
                         verify=CA_CRT_PATH, cert=(CLIENT_CRT_PATH, CLIENT_KEY_PATH))
    elif url.split(':')[0] == 'http':
        r = session.get(url, headers=headers, params=data, cookies=cookies, verify=False)
    # print r.status_code
    # print r.headers
    # print r.text.encode('utf-8')
    return r


if __name__ == '__main__':
    r = post("http://192.168.120.75:8089/msg/aaa", data={"a": 1})
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')

    r = post("https://192.168.120.75:443/msg/aaa", data={"a": 1})
    print r.status_code
    print r.headers
    print r.text.encode('utf-8')
