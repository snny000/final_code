from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^inner_policy$', views.AbnormalAlarm.as_view()),
    url(r'^inner_policy_file$', views.AbnormalAlarmFile.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)