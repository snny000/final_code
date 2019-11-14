from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^reg_request$', views.Register.as_view()),
    url(r'^re_reg_request$', views.ReRegister.as_view()),
    url(r'^regstatus$', views.RegisterStatus.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)