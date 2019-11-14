# -*- coding: utf-8 -*-

import time
import requests

def send_audit_log():
    r = requests.post('http://192.168.120.234:8089/audit_local/send_audit')
    print time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' send_center_audit ' + str(r.status_code) + ' ' + r.text.encode('utf-8')


if __name__ == '__main__':
    send_audit_log()
