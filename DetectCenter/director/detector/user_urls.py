from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^passwd$', views.PasswordUpdate.as_view()),
    url(r'^insert$', views.UserAdd.as_view()),
    url(r'^del$', views.UserDel.as_view()),
    url(r'^chmod$', views.AuthorityUpdate.as_view()),
    url(r'^show$', views.UserShow.as_view()),
    url(r'^count$', views.UserCount.as_view()),
    url(r'^detail$', views.UserDetail.as_view()),
    url(r'^logout$', views.Logout.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
