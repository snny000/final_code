# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import task_group_views as views

urlpatterns = [

    # 任务组相关
    url(r'^show$', views.TaskGroupProcess.as_view()),
    url(r'^count', views.GetTaskCount.as_view()),
    url(r'^policy_show$', views.GetTaskPolicy.as_view()),
    url(r'^policy_count$', views.GetTaskPolicyCount.as_view()),
    url(r'^add_update$', views.AddOrUpdateTaskgroup.as_view()),
    url(r'^delete$', views.DeleteTaskGroup.as_view()),
    url(r'^batch_update$', views.UpdateBatchTaskgroup.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
