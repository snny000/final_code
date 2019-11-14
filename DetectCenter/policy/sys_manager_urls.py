from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^sync_time$', views.TimeSync.as_view()),
    url(r'^version_check$', views.VersionCheck.as_view()),
    url(r'^update$', views.FirmwareUpdate.as_view()),
    url(r'^inner_policy_update$', views.InnerPolicy.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)