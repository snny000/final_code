from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^show$', views.PluginAlarmShow.as_view()),
    url(r'^count$', views.PluginAlarmCount.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
