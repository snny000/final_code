# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    # 检测器日志展示接口
    url(r'^show$', views.SystemAuditShow.as_view()),
    url(r'^count$', views.SystemAuditCount.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)