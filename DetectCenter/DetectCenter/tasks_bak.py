# -*- coding: utf-8 -*-

from celery import app
import statistics_log
import common
import requests
import traceback

@app.task
def send_data(url, detector_id, data_type, header, data):
    try:
        resp = requests.post(url, headers=header, data=data, timeout=60, verify=common.CA_CRT_PATH, cert=(common.CLIENT_CRT_PATH, common.CLIENT_KEY_PATH))
        log_str = '%s %s %d' % (detector_id, data_type, resp.status_code)
        statistics_log.string2log_per_day(content=log_str, path=common.LOG_PATH, prefix='send_command.', suffix='.log')
    except:
        traceback.print_exc()
        log_str = '%s %s %s' % (detector_id, data_type, 'send_exception')
        statistics_log.string2log_per_day(content=log_str, path=common.LOG_PATH, prefix='send_command.', suffix='.log')
