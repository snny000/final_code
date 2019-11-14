# -*- coding:utf-8 -*-

"""
Django settings for DetectCenter project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import config
import time
from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f+o*f-n=j!ye68ssm#kzk!ckz45)h-o#!htj%_8%k49@_nma!w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_crontab',
    'rest_framework',
    'detector',
    'monitor',
    'audit',
    'policy',
    'plugin',
    'director',
    'login',
]

AUTH_USER_MODEL = 'login.User'
# AUTH_GROUP_MODEL = 'login.Group'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
       # 'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'PAGE_SIZE': 10,
}


SESSION_ENGINE = 'django.contrib.sessions.backends.db'    # engine (default)
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'     # engine (cache)
SESSION_COOKIE_NAME = 'SESSION'           # the key of session's cookie stored in the browser (default is sessionid)
SESSION_COOKIE_SECURE = False              # whether https transfer cookie (default is False)
SESSION_COOKIE_HTTPONLY = True             # whether cookie only supports http transmission (default is True)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7      # cookie's expiration date (default is two week, that is 1209600)


# CACHES = {
    # 'default': {
        # 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # 'LOCATION': '127.0.0.1:11211',
    # }
# }

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'DetectCenter.middleware.SimpleMiddleware',
	'DetectCenter.middleware.RequestsLog',
]

ROOT_URLCONF = 'DetectCenter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DetectCenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.const.DATABASE,
        'USER': config.const.USER,
        'PASSWORD': config.const.PASSWORD,
        'HOST': config.const.HOST,
        'PORT': config.const.PORT,
        'CONN_MAX_AGE': config.const.CONN_MAX_AGE,
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'detect_center',
        # 'USER': 'root',
        # 'PASSWORD': '123456',
        # 'HOST': '192.168.120.171',
        # 'PORT': '3306',
        # 'CONN_MAX_AGE': 30,
        # 'ATOMIC_REQUESTS': True
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# STATIC_URL = '/media/'
#
# STATIC_ROOT = os.path.join(BASE_DIR, 'media')
#
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'media'),
# )

####定时任务相关####
CRONJOBS = [
	('*/1 * * * *', 'director.heartbeat.task_heartbeat', '>> ' + BASE_DIR + '/log/celery_log/heartbeat.log'),  # 发送心跳到指挥节点
	('*/10 * * * *', 'audit.data_processing.send_audit', '>> ' + BASE_DIR + '/log/uwsgi.log'),              # 发送审计日志到指挥节点
	('*/1 * * * *', 'detector.judge_online.record_event', '>> ' + BASE_DIR + '/log/online.log'),           # 检查检测器的在线情况
	('* * */5 * *', 'DetectCenter.delete_media_file_crontab.delete_media_file', '>> ' + BASE_DIR + '/log/remove_file_crontab/crontab.log'),           # 检查检测器的在线情况
	# ('*/1 * * * *', 'DetectCenter.delete_media_file_crontab.delete_media_file', '>> ' + BASE_DIR + '/log/remove_file_crontab/crontab.log'),           # 检查检测器的在线情况
	# ('*/1 * * * *', 'detector.data_processing.center_report_detector_running_status', '>> ' + BASE_DIR + '/log/online.log'),  # 通过检测器运行状态上传接口上报检测器在线状态，现在通过检测器在线状态时间定时器上传
	# ('*/1 * * * *', 'DetectCenter.crontab.hello', '>> ' + BASE_DIR + '/log/hello.log')                   # 测试定时器
    ('* */10 * * *', 'policy.write_policy_data.process_policy', '>> ' + BASE_DIR + '/log/write_policy.log'),           # 检查检测器的在线情况
]

# celery configuration
####异步任务相关####
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
CELERY_TASK_SERIALIZER = "msgpack"
CELERY_RESULT_SERIALIZER = "msgpack"

BROKER_TRANSPORT = 'redis'

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

# BROKER_POOL_LIMIT = 50000
# BROKER_CONNECTION_TIMEOUT = 1000


CELERYD_MAX_TASKS_PER_CHILD = 50000       # 每个worker执行了多少任务就会死掉
CELERYD_PREFETCH_MULTIPLIER = 50         # worker 每次预取任务的数量，一般不取太多
# CELERY_CREATE_MISSING_QUEUES = True     # 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_TASK_RESULT_EXPIRES = 1200       # celery任务执行结果的超时时间
CELERY_ACKS_LATE = False                # true的时候任务执行时会确认消息是否执行过，与函数是否幂等有关
CELERY_DISABLE_RATE_LIMITS = True       # 关闭速率限制，负责执行速率限制的系统会带来一些开销，这将禁用一个线程，并且当队列不活动时，它不会花费太多的CPU周期。
CELERYD_FORCE_EXECV = True              # 有些情况下可以防止死锁
CELERY_DEFAULT_QUEUE = "task_default"        # 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面
# By default we will ignore result
# If you want to see results and try out tasks interactively, change it to False
# Or change this setting on tasks level
# CELERY_IGNORE_RESULT = True             # 忽视任务执行结果

CELERY_QUEUES = (  ####定义多个队列
    Queue('task_default', Exchange('task_default', delivery_mode=1), routing_key='task_default'),
    Queue('task_director', Exchange('task_director', delivery_mode=1), routing_key='task_director'),
    Queue('task_director_hi', Exchange('task_director_hi', delivery_mode=1), routing_key='task_director_hi'),
    Queue('task_director_lo', Exchange('task_director_lo', delivery_mode=1), routing_key='task_director_lo'),
    Queue('task_business', Exchange('task_business', delivery_mode=1), routing_key='task_business'),
    Queue('task_es', Exchange('task_es', delivery_mode=1), routing_key='task_es'),
    Queue('task_business_disposal', Exchange('task_business_disposal', delivery_mode=1), routing_key='task_business_disposal')
)

# 路由（哪个任务放入哪个队列）
CELERY_ROUTES = {
    'DetectCenter.tasks.task_send_director': {'queue': 'task_director', 'routing_key': 'task_director', 'delivery_mode': 'transient'},
    'DetectCenter.tasks.task_send_director_hi': {'queue': 'task_director_hi', 'routing_key': 'task_director_hi', 'delivery_mode': 'transient'},
    'DetectCenter.tasks.task_send_director_lo': {'queue': 'task_director_lo', 'routing_key': 'task_director_lo', 'delivery_mode': 'transient'},

    'DetectCenter.tasks.task_download_plug_file_from_director': {'queue': 'task_director', 'routing_key': 'task_director', 'delivery_mode': 'transient'},

    'DetectCenter.tasks.task_send_business_file': {'queue': 'task_business', 'routing_key': 'task_business', 'delivery_mode': 'transient'},
    'DetectCenter.tasks.task_send_business_data': {'queue': 'task_business', 'routing_key': 'task_business', 'delivery_mode': 'transient'},

    'DetectCenter.tasks.task_send_es_net_log': {'queue': 'task_es', 'routing_key': 'task_es', 'delivery_mode': 'transient'},
    'DetectCenter.tasks.task_send_es_app_behavior': {'queue': 'task_es', 'routing_key': 'task_es', 'delivery_mode': 'transient'},

    'DetectCenter.tasks.task_send_business_disposal': {'queue': 'task_business_disposal', 'routing_key': 'task_business_disposal', 'delivery_mode': 'transient'}
}

####################
DATA_UPLOAD_MAX_MEMORY_SIZE = 1073741824
FILE_UPLOAD_MAX_MEMORY_SIZE = 1073741824



# A sample logging configuration
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#
#     'formatters': {
#         'verbose': {
#             'format': '[%(asctime)s] [%(threadName)s: %(thread)d] [%(name)s: %(lineno)d] [%(levelname)s] - %(message)s'
#         },
#         'simple': {
#             'format': '[%(asctime)s] %(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         },
#     },
#
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG',
#             'formatter': 'simple',
#         },
#
#         'net_log': {
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'verbose',
#             'filename': '%s/log/net_log/net.%s.log' % (BASE_DIR, time.strftime('%Y%m%d')),
#         },
#
#         'app_behavior_log': {
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'verbose',
#             'filename': '%s/log/app_behavior_log/app_behavior.%s.log' % (BASE_DIR, time.strftime('%Y%m%d')),
#         },
#
#         'alarm_log': {
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'verbose',
#             'filename': '%s/log/alarm_log/alarm.%s.log' % (BASE_DIR, time.strftime('%Y%m%d')),
#         },
#
#         'status_log': {
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'verbose',
#             'filename': '%s/log/status_log/status.%s.log' % (BASE_DIR, time.strftime('%Y%m%d')),
#         },
#
#         'record_log': {
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'verbose',
#             'filename': '%s/log/detector_access_log/access.%s.log' % (BASE_DIR, time.strftime('%Y%m%d')),
#         },
#
#         'audit_log': {
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'verbose',
#             'filename': '%s/log/audit_log/behavior_audit.%s.log' % (BASE_DIR, time.strftime('%Y%m%d')),
#         },
#
#         'online_log': {
#             'class': 'cloghandler.ConcurrentRotatingFileHandler',
#             'level': 'INFO',
#             'formatter': 'simple',
#             'filename': '%s/log/online_log/online.%s.log' % (BASE_DIR, time.strftime('%Y%m%d')),
#         }
#     },
#
#     'loggers': {
#         'project.net_log': {
#             'level': 'INFO',
#             'handlers': ['net_log'],
#             'propagate': True
#         },
#         'project.app_behavior': {
#             'level': 'INFO',
#             'handlers': ['app_behavior_log'],
#             'propagate': True
#         },
#         'project.alarm': {
#             'level': 'INFO',
#             'handlers': ['alarm_log'],
#             'propagate': True
#         },
#         'project.status': {
#             'level': 'INFO',
#             'handlers': ['status_log'],
#             'propagate': True
#         },
#         'project.record': {
#             'level': 'INFO',
#             'handlers': ['record_log'],
#             'propagate': True
#         },
#         'project.audit': {
#             'level': 'INFO',
#             'handlers': ['audit_log'],
#             'propagate': True
#         },
#         'project.online': {
#             'level': 'INFO',
#             'handlers': ['online_log'],
#             'propagate': True
#         },
#     },
# }
