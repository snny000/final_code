from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^show$', views.DeviceShow.as_view()),
    url(r'^count$', views.DeviceCount.as_view()),
    url(r'^detail$', views.DeviceDetail.as_view()),
    url(r'^save$', views.DeviceAddUpdate.as_view()),
    url(r'^fileupload$', views.FileUpload.as_view()),
    url(r'^import$', views.DeviceImport.as_view()),
    url(r'^template$', views.TemplateDownload.as_view()),

    url(r'^delete/?$', views.DetectorInfoDelete.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)