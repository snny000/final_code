"""DetectCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# from detector import views as detector_views
import common

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^msg/', include('detector.aaa_urls')),

    url(r'^V1/register/', include('detector.register_urls')),
    url(r'^V1/auth/', include('detector.auth_urls')),
    url(r'^V1/business_status', include('detector.business_status_urls')),
    url(r'^V1/system_status', include('detector.system_status_urls')),

    url(r'^V1/alarm/', include('monitor.alarm_urls')),
    url(r'^V1/abnormal/', include('monitor.abnormal_urls')),
    url(r'^V1/sensitive/', include('monitor.sensitive_urls')),
    url(r'^V1/object_listen/', include('monitor.object_listen_urls')),
    url(r'^V1/block/', include('monitor.block_urls')),

    url(r'^V1/system_audit/', include('audit.system_audit_urls')),
    url(r'^V1/net_audit/', include('audit.net_audit_urls')),

    url(r'^V1/heartbeat', include('policy.heartbeat_urls')),
    url(r'^V1/sys_manager/', include('policy.sys_manager_urls')),

    url(r'^V1/plug_manager/', include('plugin.plug_manager_urls')),

    url(r'^detector/', include('detector.detector_urls')),
    url(r'^detector_info/', include('detector.detector_info_urls')),
    url(r'^alarm/', include('monitor.show_alarm_urls')),

    url(r'^rule/', include('policy.rule_urls')),
    url(r'^cmd/', include('policy.cmd_urls')),
    url(r'^rule_task/', include('policy.policy_task_urls')),
    url(r'^cmd_task/', include('policy.cmd_task_urls')),
    # url(r'^file/', include('policy.upload_urls')),
    url(r'^task_group/', include('policy.task_group_urls')),

    url(r'^audit_log/', include('audit.audit_log_urls')),
    url(r'^audit_system/', include('audit.audit_system_urls')),
    url(r'^audit_local/', include('audit.audit_local_urls')),

    url(r'^plug_alarm/', include('plugin.plug_alarm_urls')),
    url(r'^plug_status/', include('plugin.plug_status_urls')),
    url(r'^plugin/', include('plugin.plugin_urls')),

    url(r'^director/', include('director.director_urls')),
    url(r'V1/jcc/', include('director.director_urls')),

    url(r'^login/', include('login.login_urls')),
    url(r'^center/', include('director.center_urls')),


    url(r'^download/?$', common.process_download_file1),

]
