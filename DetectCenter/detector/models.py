# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from DetectCenter import common


class Detector(models.Model):

    # 注册信息
    device_id                   = models.CharField(max_length=12)
    device_type                 = models.CharField(max_length=2)
    contractor                  = models.CharField(max_length=32, blank=True)
    soft_version                = models.CharField(max_length=32, blank=True)
    device_ca                   = models.TextField(blank=True)
    organs                      = models.CharField(max_length=64)
    address                     = models.CharField(max_length=128, blank=True)
    address_code                = models.CharField(max_length=6, blank=True)
    contact                     = models.TextField()
    memo                        = models.CharField(max_length=128, blank=True)
    register_time               = models.DateTimeField()
    register_frequency          = models.IntegerField(default=1)
    register_status             = models.IntegerField(default=2)
    register_fail_reason        = models.CharField(max_length=64, blank=True)
    op_person                   = models.CharField(max_length=64, blank=True)
    op_ip                       = models.CharField(max_length=64, blank=True)
    op_time                     = models.DateTimeField(null=True, blank=True)

    # 认证信息
    interface                   = models.CharField(max_length=1024, blank=True)
    mem_total                   = models.IntegerField(default=0)
    cpu_info                    = models.CharField(max_length=1024, blank=True)
    disk_info                   = models.CharField(max_length=1024, blank=True)
    auth_time                   = models.DateTimeField(null=True, blank=True)
    auth_frequency              = models.IntegerField(default=0)
    auth_status                 = models.IntegerField(default=2)
    auth_fail_reason            = models.CharField(max_length=64, blank=True)

    is_online                   = models.IntegerField(default=0)
    last_warning_time           = models.DateTimeField(null=True, blank=True)
    device_status               = models.IntegerField(default=common.DETECTOR_STATUS['register_no_check'])
    alarm_total_num             = models.IntegerField(default=0)

    # 业务状态中模块状态
    alarm_status                = models.CharField(max_length=4, blank=True)

    trojan_status               = models.CharField(max_length=4, blank=True)
    trojan_version              = models.CharField(max_length=32, blank=True)

    attack_status               = models.CharField(max_length=4, blank=True)
    attack_version              = models.CharField(max_length=32, blank=True)

    malware_status              = models.CharField(max_length=4, blank=True)
    malware_version             = models.CharField(max_length=32, blank=True)

    other_status                = models.CharField(max_length=4, blank=True)
    other_version               = models.CharField(max_length=32, blank=True)


    abnormal_status             = models.CharField(max_length=4, blank=True)
    abnormal_version            = models.CharField(max_length=32, blank=True)


    sensitive_status            = models.CharField(max_length=4, blank=True)

    finger_file_status          = models.CharField(max_length=4, blank=True)
    finger_file_version         = models.CharField(max_length=32, blank=True)

    sensitive_file_status       = models.CharField(max_length=4, blank=True)
    sensitive_file_version      = models.CharField(max_length=32, blank=True)

    keyword_file_status         = models.CharField(max_length=4, blank=True)
    keyword_file_version        = models.CharField(max_length=32, blank=True)

    encryption_file_status      = models.CharField(max_length=4, blank=True)
    encryption_file_version     = models.CharField(max_length=32, blank=True)

    compress_file_status        = models.CharField(max_length=4, blank=True)
    compress_file_version       = models.CharField(max_length=32, blank=True)

    picture_file_status         = models.CharField(max_length=4, blank=True)
    picture_file_version        = models.CharField(max_length=32, blank=True)

    style_file_status           = models.CharField(max_length=4, blank=True)
    style_file_version          = models.CharField(max_length=32, blank=True)


    object_listen_status        = models.CharField(max_length=4, blank=True)

    ip_listen_status            = models.CharField(max_length=4, blank=True)
    ip_listen_version           = models.CharField(max_length=32, blank=True)

    domain_listen_status        = models.CharField(max_length=4, blank=True)
    domain_listen_version       = models.CharField(max_length=32, blank=True)

    url_listen_status           = models.CharField(max_length=4, blank=True)
    url_listen_version          = models.CharField(max_length=32, blank=True)

    account_listen_status       = models.CharField(max_length=4, blank=True)
    account_listen_version      = models.CharField(max_length=32, blank=True)


    net_audit_status            = models.CharField(max_length=4, blank=True)

    net_log_status              = models.CharField(max_length=4, blank=True)
    net_log_version             = models.CharField(max_length=32, blank=True)

    app_behavior_status         = models.CharField(max_length=4, blank=True)
    app_behavior_version        = models.CharField(max_length=32, blank=True)
    web_filter_version          = models.CharField(max_length=32, blank=True)
    dns_filter_version          = models.CharField(max_length=32, blank=True)

    ip_whitelist_version        = models.CharField(max_length=32, blank=True)

    block_status                = models.CharField(max_length=4, blank=True)
    block_version               = models.CharField(max_length=32, blank=True)

    # 版本一致性是否下发标志
    version_check_type          = models.IntegerField(default=0)

    is_effective                = models.BooleanField(default=True)
    comment                     = models.CharField(max_length=128, blank=True)
    heartbeat_time              = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'detector_info'

    def __unicode__(self):
        return self.name


class BusinessStatus(models.Model):
    uptime                      = models.IntegerField()
    soft_version                = models.CharField(max_length=32)
    time                        = models.DateTimeField()

    report_time                 = models.DateTimeField()
    device_id                   = models.CharField(max_length=12)

    class Meta:
        db_table = 'status_business'

    def __unicode__(self):
        return self.name


class ModuleStatus(models.Model):
    device_id = models.CharField(max_length=12)
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=4)
    submodule = models.TextField()

    report_time = models.DateTimeField()

    class Meta:
        db_table = 'status_module'

    def __unicode__(self):
        return self.device_id + ' ' + self.name


class NetworkCardStatus(models.Model):

    NIC_status = (
        (1,  '网卡启用'),
        (2,  '网卡停用'),
        (3,  '网线掉落'),
        (4,  '网卡故障'),
        (99, '未知'),
    )

    interface_seq               = models.IntegerField()
    interface_flag              = models.CharField(max_length=64)
    interface_stat              = models.IntegerField(choices=NIC_status)
    interface_flow              = models.IntegerField()
    interface_error             = models.IntegerField()
    interface_drop              = models.IntegerField()
    duration_time               = models.IntegerField()

    report_time                 = models.DateTimeField()
    device_id                   = models.CharField(max_length=12)

    class Meta:
        db_table = 'status_network_card'

    def __unicode__(self):
        return self.name


class SuspectedStatus(models.Model):
    abnormal_type = (
        (1, '系统异常'),
        (2, '软件异常'),
        (3, '插件异常'),
        (4, '规则异常'),
    )

    risk_choices = (
        (0, '无风险'),
        (1, '一般级'),
        (2, '关注级'),
        (3, '严重级'),
        (4, '紧急级'),
    )

    event_type   = models.IntegerField(choices=abnormal_type)
    time         = models.DateTimeField()
    risk         = models.IntegerField(choices=risk_choices)
    msg          = models.CharField(max_length=128, blank=True)

    report_time  = models.DateTimeField()
    device_id    = models.CharField(max_length=12)

    class Meta:
        db_table = 'status_suspected'

    def __unicode__(self):
        return self.name


class PluginStatus(models.Model):
    plug_id                 = models.CharField(max_length=32)
    status                  = models.CharField(max_length=4)
    plug_version            = models.CharField(max_length=32)
    plug_policy_version     = models.CharField(max_length=32)

    report_time             = models.DateTimeField()
    device_id               = models.CharField(max_length=12)

    class Meta:
        db_table = 'status_plugin'

    def __unicode__(self):
        return self.name


class SystemRunningStatus(models.Model):
    cpu          = models.TextField()
    mem          = models.IntegerField()
    disk         = models.IntegerField()
    time         = models.DateTimeField()
    plug_stat    = models.TextField()

    report_time  = models.DateTimeField()
    device_id    = models.CharField(max_length=12)

    did = models.IntegerField(default=1, blank=True)

    class Meta:
        db_table = 'status_system_running'

    def __unicode__(self):
        return self.name


class AdminLogin(models.Model):
    login_id         = models.CharField(max_length=32)
    login_password   = models.CharField(max_length=32)
    level            = models.IntegerField(default=2)
    create_time      = models.DateTimeField(null=True, blank=True)
    update_time      = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'admin_login'

    def __unicode__(self):
        return self.name


class DeviceInfo(models.Model):
    device_id         = models.CharField(max_length=12)
    soft_version      = models.CharField(max_length=32, blank=True)
    device_ca         = models.TextField(blank=True)
    contractor        = models.CharField(max_length=128, blank=True)
    organs            = models.CharField(max_length=64)
    address           = models.CharField(max_length=128)
    address_code      = models.CharField(max_length=6)
    contact           = models.TextField()
    mem_total         = models.IntegerField(default=0)
    interface         = models.CharField(max_length=1024)
    cpu_info          = models.CharField(max_length=1024)
    disk_info         = models.CharField(max_length=1024)

    class Meta:
        db_table = 'device_msg'

    def __unicode__(self):
        return self.name



class DetectorOnlineEvent(models.Model):
    device_id = models.CharField(max_length=12)
    event = models.CharField(max_length=4)
    time = models.DateTimeField()

    class Meta:
        db_table = 'detector_online_event'

    def __unicode__(self):
        return self.name


class DetectorAuditMode(models.Model):
    mode = models.SmallIntegerField(default=1)

    class Meta:
        db_table = 'detector_audit_mode'

    def __unicode__(self):
        return self.mode