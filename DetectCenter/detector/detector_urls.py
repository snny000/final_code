from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show/?$', views.DetectorShow.as_view()),
    url(r'^detail/?$', views.DetectorDetail.as_view()),
    url(r'^count/?$', views.DetectorCount.as_view()),
    url(r'^permit/?$', views.DetectorCheck.as_view()),
    url(r'^alert/?$', views.DetectorEffectivenessUpdate.as_view()),
    url(r'^export/?$', views.DetectorReportExport.as_view()),
    url(r'^statistic_status/?$', views.StatisticDetectorStatus.as_view()),

    url(r'^online_event_show/?$', views.OnlineEventShow.as_view()),
    url(r'^online_event_count/?$', views.OnlineEventCount.as_view()),

    url(r'^delete/?$', views.DetectorDelete.as_view()),

    url(r'^audit_mode_show/?$', views.AuditModeShow.as_view()),
    url(r'^audit_mode_alert/?$', views.AuditModeAlert.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)