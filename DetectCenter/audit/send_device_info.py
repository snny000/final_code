# -*- coding: utf-8 -*-

import time
import requests

def send_center_info():
    r = requests.post('http://192.168.120.234:8089/audit_local/send_center_info')
    print time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' send_center_info ' + str(r.status_code) + ' ' + r.text.encode('utf-8')


def send_detector_info():
    r = requests.post('http://192.168.120.234:8089/audit_local/send_detector_info')
    print time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()) + ' send_detector_info ' + str(r.status_code) + ' ' + r.text.encode('utf-8')

    
if __name__ == '__main__':
    send_center_info()
    # send_detector_info()
