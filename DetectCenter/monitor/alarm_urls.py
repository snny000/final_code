from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^trojan/inner_policy$', views.TrojanAlarm.as_view()),
    url(r'^trojan/inner_policy_pcap$', views.TrojanAlarmFile.as_view()),

    url(r'^trojan/center_policy$', views.TrojanAlarm.as_view()),
    url(r'^trojan/center_policy_pcap$', views.TrojanAlarmFile.as_view()),

    url(r'^attack/inner_policy$', views.ExploitAlarm.as_view()),
    url(r'^attack/inner_policy_pcap$', views.ExploitAlarmFile.as_view()),

    url(r'^attack/center_policy$', views.ExploitAlarm.as_view()),
    url(r'^attack/center_policy_pcap$', views.ExploitAlarmFile.as_view()),

    url(r'^malware/inner_policy$', views.MalwareAlarm.as_view()),
    url(r'^malware/inner_policy_file$', views.MalwareAlarmFile.as_view()),

    url(r'^malware/center_policy$', views.MalwareAlarm.as_view()),
    url(r'^malware/center_policy_file$', views.MalwareAlarmFile.as_view()),

    url(r'^other/inner_policy$', views.OtherAlarm.as_view()),
    url(r'^other/inner_policy_pcap$', views.OtherAlarmFile.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)