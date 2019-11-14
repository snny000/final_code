from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [

    url(r'^reg_rs/?$', views.AuditResult.as_view()),

    url(r'^rule_sync/?$', views.PolicyReception.as_view()),
    url(r'^plug_sync/?$', views.PlugReception.as_view()),
    # url(r'^plug_file/?$', views.PlugReceptionFile.as_view()),
    url(r'^cmd_sync/?$', views.CmdReceptionFile.as_view()),

    url(r'^download_plug', views.DownloadPlug.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)