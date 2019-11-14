from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^check$', views.Login.as_view()),
    url(r'^expire$', views.IsPasswordExpire.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
