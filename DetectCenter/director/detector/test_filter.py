# -*- coding: utf-8 -*-

import os
import sys
import django

pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DetectCenter.settings")

django.setup()

from django.db import connection
import time
from detector.models import AdminLogin


def test_filter():
    users = AdminLogin.objects.filter(login_id__contains='admin')
    user_id = [user.id for user in users]
    # print user_id
    AdminLogin.objects.filter(id__in=user_id).update(login_password='000000')
    time.sleep(60)
    user_id = [user.id for user in users]
    # print user_id
    AdminLogin.objects.filter(id__in=user_id).update(login_password='000000')


if __name__ == '__main__':
    test_filter()
