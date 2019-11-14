from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show$', views.SystemAuditShow.as_view()),
    url(r'^count$', views.SystemAuditCount.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)