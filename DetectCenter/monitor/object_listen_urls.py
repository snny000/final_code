from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^ip_listen/center_policy$', views.IPIntercept.as_view()),
    url(r'^ip_listen/center_policy_pcap$', views.IPInterceptFile.as_view()),

    url(r'^domain_listen/center_policy$', views.DNSIntercept.as_view()),
    url(r'^domain_listen/center_policy_pcap$', views.DNSInterceptFile.as_view()),

    url(r'^url_listen/center_policy$', views.URLIntercept.as_view()),
    url(r'^url_listen/center_policy_pcap$', views.URLInterceptFile.as_view()),

    url(r'^account_listen/center_policy$', views.AccountIntercept.as_view()),
    url(r'^account_listen/center_policy_pcap$', views.AccountInterceptFile.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)