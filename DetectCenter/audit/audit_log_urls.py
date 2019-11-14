# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    # 网络行为审计日志展示接口
    url(r'^show$', views.AuditLogShow.as_view()),
    url(r'^count$', views.AuditLogCount.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)