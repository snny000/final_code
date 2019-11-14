from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^sync$', views.PluginAddUpdate.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
