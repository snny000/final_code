# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show_all_plug$', views.ShowAllPlug.as_view()),
    url(r'^show_plug_count$', views.ShowPlugCount.as_view()),
    url(r'^add_update_plugin$', views.AddUpdatePlugin.as_view()),
    url(r'^fileupload$', views.FileUpload.as_view()),
    url(r'^delete_plug$', views.DeletePlug.as_view()),
    url(r'^change_plug$', views.ChangePlug.as_view()),
    url(r'^append_plug$', views.AppendPlug.as_view()),
    url(r'^plug_synchronization$', views.PlugSynchronization.as_view()),
    url(r'^fulldose_report/?$', views.FulldoseReport2DirectCenter.as_view()),     # 全量同步管理中心插件到指挥节点
    url(r'^is_changed$', views.JudgePlugGeneration.as_view()),
    url(r'^show$', views.TaskShow.as_view()),
    url(r'^count$', views.TaskCount.as_view()),
    url(r'^update_task_plug$', views.UpdateTaskPlug.as_view()),
    url(r'^send_again$', views.SendAgain.as_view()),
    url(r'^media/(.*)$', views.ProcessDownloadFile.as_view()),     # 插件文件下载接口，已改成使用通用的download接口
    url(r'^plug_start_stop$', views.StartStopPlug.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)