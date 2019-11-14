# -*- coding: utf-8 -*-

from celery import app
import statistics_log
import common
import https_requests as requests
import traceback
import time
import file_util as fu, sender
from DetectCenter.business_config import *
# from director.data_processing import download_plug_file_from_director

@app.task
def task_send_director(url, detector_id, data_type, header, data, retract=0):
    sender.send_director(url, detector_id, data_type, header, data)

@app.task
def task_send_director_hi(url, detector_id, data_type, header, data, retract=0):
    # print "call task_send_director_hi"
    sender.send_director(url, detector_id, data_type, header, data)

@app.task
def task_send_director_lo(url, detector_id, data_type, header, data, retract=0):
    sender.send_director(url, detector_id, data_type, header, data)


# 处理业务系统异步
@app.task
def task_send_business_file(logger_str, flag, device_id, header, file_path, filename, url=BUSINESS_URL):
    sender.send_business_file(logger_str, flag, device_id, header, file_path, filename, url)

@app.task
def task_send_business_data(logger_str, flag, device_id, send_data, url=BUSINESS_URL):
    sender.send_business_data(logger_str, flag, device_id, send_data, url)


# 处理ES上传数据
@app.task
def task_send_es_net_log(request_id, url, file_path, detector_id):
    sender.send_es_net_log(request_id, url, file_path, detector_id)

@app.task
def task_send_es_app_behavior(request_id, url, file_path, detector_id):
    sender.send_app_behavior(request_id, url, file_path, detector_id)


# 处理业务处置系统异步
@app.task
def task_send_business_disposal(file_dir, file_name, user_agent, handle_data_type, handle_data):
    sender.send_business_disposal(file_dir, file_name, user_agent, handle_data_type, handle_data)


# @app.task
# def task_download_plug_file_from_director(sub_function_path, plug_list, director_down_header={}, is_down_plug_file_list=[]):
#     download_plug_file_from_director(sub_function_path, plug_list, director_down_header, is_down_plug_file_list)