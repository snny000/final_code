from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show$', views.TaskShow.as_view()),
    url(r'^count$', views.TaskCount.as_view()),
    url(r'^ignore_task', views.IgnorePolicyTask.as_view()),
    url(r'^send_again', views.PolicyTaskSendAgain.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)