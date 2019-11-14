from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views


urlpatterns = [
    url(r'^finger_file/inner_policy$', views.FingerSensitive.as_view()),
    url(r'^finger_file/inner_policy_file$', views.FingerSensitiveFile.as_view()),

    url(r'^sensitive_file/inner_policy$', views.MarkSensitive.as_view()),
    url(r'^sensitive_file/inner_policy_file$', views.MarkSensitiveFile.as_view()),

    url(r'^keyword_file/center_policy$', views.KeywordSensitive.as_view()),
    url(r'^keyword_file/center_policy_file$', views.KeywordSensitiveFile.as_view()),

    url(r'^encryption_file/inner_policy$', views.EncryptionSensitive.as_view()),
    url(r'^encryption_file/inner_policy_file$', views.EncryptionSensitiveFile.as_view()),

    url(r'^compress_file/center_policy$', views.CompressSensitive.as_view()),
    url(r'^compress_file/center_policy_file$', views.CompressSensitiveFile.as_view()),

    url(r'^picture_file/center_policy$', views.PictureSensitive.as_view()),
    url(r'^picture_file/center_policy_file$', views.PictureSensitiveFile.as_view()),

    url(r'^style_file/inner_policy$', views.StyleSensitive.as_view()),
    url(r'^style_file/inner_policy_file$', views.StyleSensitiveFile.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)