from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from views import Aaa

urlpatterns = [
    url(r'^aaa$', Aaa.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
