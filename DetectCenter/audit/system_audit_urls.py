# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^$', views.AuditSystem.as_view()),         # 检测器上报
]

urlpatterns = format_suffix_patterns(urlpatterns)
