# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show$', views.AlarmShow.as_view()),
    url(r'^detail$', views.AlarmDetail.as_view()),
    url(r'^count$', views.AlarmCount.as_view()),
    url(r'^export$', views.AlarmDetailReportExport.as_view()),  # 告警列表页到处告警类型-告警数量详情信息

    url(r'^media/(.*)$', views.ProcessDownloadFile.as_view()),    # 告警文件下载接口，已改成使用通用的download接口

    # 新增
    url(r'^get_statistics_count$', views.GetStatisticsCount.as_view()),
    # 告警详情统计
    url(r'^newly_trend$', views.AlarmCountSeveralDays.as_view()),             # 查询给定最近天数的告警数
    url(r'^warning_type_histogram$', views.AlarmCountEveryType.as_view()),    # 可根据给定query_condition参数类型查询告警数据
    url(r'^show_alarm_between_days$', views.ShowAlarmBetweenDays.as_view()),          # 查询time_max和time_min之间的告警数
    url(r'^show_alarm_group$', views.ShowAlarmGroup.as_view()),

    # 告警统计导出
    url(r'^export_alarm_report$', views.ExportAlarmReport.as_view()),
    url(r'^export_time_alarm_report$', views.ExportTimeAlarmReport.as_view()),
    url(r'^export_last_days_report$', views.ExportLastDaysReport.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)