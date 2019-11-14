# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DetectCenter.settings')

import pymysql

pymysql.install_as_MySQLdb()
django.setup()

app = Celery('DetectCenter')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task(bind=True)
# def debug_task(self):
#     print 'Request: {0!r}'.format(self.request)