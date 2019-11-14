# -*- coding:utf-8 -*-
import ConfigParser
import const
import traceback
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
const.CONF_PATH = BASE_DIR + "/DetectCenter/management.conf"  # 注意当前路径是工程目录

# 读取配置文件
cf = ConfigParser.ConfigParser()
cf.read(const.CONF_PATH)
# print 'cf.sections:', cf.sections()

try:
    # 数据库连接配置
    const.HOST = cf.get('db', 'host')
    const.PORT = cf.get('db', 'port')
    const.USER = cf.get('db', 'user')
    const.PASSWORD = cf.get('db', 'password')
    const.DATABASE = cf.get('db', 'database')
    const.CONN_MAX_AGE = cf.getint('db', 'conn_max_age')

    # ES连接配置
    const.UPLOAD_ES = True if cf.get('url', 'upload_es') == 'True' else False
    const.ES_HOST = cf.get('url', 'es_host')
    const.CR_URL = cf.get('url', 'net_log_url')
    const.AB_URL = cf.get('url', 'app_behavior_url')

    # 回传业务系统连接配置
    const.UPLOAD_BUSINESS = True if cf.get('url', 'upload_business') == 'True' else False
    const.AUTH_UID = cf.get('url', 'auth_uid')
    const.AUTH_PWD = cf.get('url', 'auth_pwd')
    const.AUTH_URL = cf.get('url', 'auth_url')
    const.BUSINESS_HOST = cf.get('url', 'business_host')
    const.BUSINESS_URL = cf.get('url', 'business_url')

    # 上传指挥中心连接配置
    const.DIRECTOR_VERSION = True if cf.get('url', 'director_version') == 'True' else False
    const.UPLOAD_DIRECTOR = True if cf.get('url', 'upload_director') == 'True' else False
    # const.DIRECTOR_HOST = cf.get('url', 'director_host')
    # const.DIRECTOR_URL = cf.get('url', 'director_url')
    # const.DIRECTOR_NODE = cf.get('url', 'director_node')
    # const.CENTER_ID = cf.get('url', 'center_id')

    # 业务处置系统相关配置
    const.UPLOAD_BUSINESS_DISPOSAL = True if cf.get('url', 'upload_business_disposal') == 'True' else False
    const.DISPOSAL_BOUNDARY = cf.get('url', 'disposal_boundary')
    const.DISPOSAL_DIR = cf.get('url', 'disposal_dir')

    # print const.UPLOAD_ES == 'False'
    # print const.UPLOAD_ES

except:
    traceback.print_exc()
finally:
    # 数据库连接配置
    const.HOST = '172.17.4.208'
    const.PORT = '3306'
    const.USER = 'root'
    const.PASSWORD = '123456'
    const.DATABASE = 'detect_center'
    const.CONN_MAX_AGE = 30