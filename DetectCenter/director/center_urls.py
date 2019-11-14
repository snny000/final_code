from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [

    url(r'^show/?$', views.CenterShow.as_view()),
    url(r'^register/?$', views.CenterRegister.as_view()),
    url(r'^auth/?$', views.CenterAuth.as_view()),
    url(r'^reset/?$', views.CenterReset.as_view()),
    url(r'^update_ip_whitelist/?$', views.CenterUpdateIpWhitelist.as_view()),
    url(r'^save_director_config/?$', views.CenterSaveDirectorConfig.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)