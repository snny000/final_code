from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^plug_load/(\d+)$', views.PluginDownload.as_view()),
    url(r'^plug_policy/(\d+)$', views.PluginPolicyDownload.as_view()),
    url(r'^plug_warn/plug_alarm$', views.PluginAlarmFileReport.as_view()),
    url(r'^plug_warn/plug_alarm_file$', views.PluginAlarmFileReport.as_view()),
    url(r'^plug_stat$', views.PluginStatusReport.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
