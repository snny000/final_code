# -*- coding: utf-8 -*-

UPLOAD_ES = False

es_host = '192.168.120.75'

# 通联关系和应用行为审计日志上传ES（ElasticSearch）服务器所用的url
CR_URL = 'http://' + es_host + '/net_log_bulk.php'
AB_URL = 'http://' + es_host + '/app_behavior_bulk.php'