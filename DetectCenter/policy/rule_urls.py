# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show$', views.RuleShow.as_view()),
    url(r'^count$', views.RuleCount.as_view()),
    url(r'^count_all$', views.RuleCountAll.as_view()),
    url(r'^insert$', views.RuleInsert.as_view()),
    url(r'^import$', views.RuleBatchInsert.as_view()),
    url(r'^del$', views.RuleDelete.as_view()),
    url(r'^sync$', views.PolicyGenerate.as_view()),
    url(r'^fulldose_report', views.FulldoseReport2DirectCenter.as_view()),
    url(r'^is_changed$', views.JudgePolicyGeneration.as_view()),
    url(r'^range$', views.RuleDetectorChange.as_view()),
    url(r'^range_append$', views.RuleDetectorAppend.as_view()),
    url(r'^rewrite_label$', views.LabelModify.as_view()),
    url(r'^fileupload$', views.FileUpload.as_view()),
    url(r'^template$', views.RuleTemplateDownload.as_view()),

    # 任务组操作
    url(r'^update_group$', views.UpdateGroup.as_view()),
    url(r'^copy_rule_group$', views.CopyRuleGroup.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
