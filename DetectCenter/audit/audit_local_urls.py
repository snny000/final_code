# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    # 管理中心本地审计日志接口
    url(r'^show$', views.LocalAuditShow.as_view()),
    url(r'^count$', views.LocalAuditCount.as_view()),
    url(r'^send_audit$', views.SendLocalAudit.as_view()),
    url(r'^send_status$', views.SendRunningStatus.as_view()),
    url(r'^send_center_info$', views.SendCenterInfo.as_view()),
    url(r'^send_detector_info$', views.SendDetectorInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)