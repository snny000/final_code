# -*- coding: utf-8 -*-

UPLOAD_BUSINESS = False

# 传输URL设置
business_host = '192.168.120.130'

# 业务数据和文件（告警和审计）上传服务器所用URL
BUSINESS_URL = 'http://' + business_host + '/groo/service'
# 发送授权申请URL
AUTH_URL = 'http://' + business_host + '/groo/service/authorization'