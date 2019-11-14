from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show$', views.CommandShow.as_view()),
    url(r'^count$', views.CommandCount.as_view()),
    url(r'^ignore_command', views.IgnoreCommandTask.as_view()),
    url(r'^send_again', views.CommandTaskSendAgain.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)