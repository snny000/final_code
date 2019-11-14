from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^net_log$', views.CommunicationRelations.as_view()),
    url(r'^app_behavior$', views.ApplicationBehavior.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
