# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


risk_choices = (
    (-1, '未知'),
    (0, '无风险'),
    (1, '一般级'),
    (2, '关注级'),
    (3, '严重级'),
    (4, '紧急级'),
)

trojan_type_choices = (
    (1, '特种木马'),
    (2, '普通木马'),
    (3, '远控'),
    (4, '其他')
)

prevalence_choices = (
    (1, '高'),
    (2, '中'),
    (3, '低'),
)

attack_type_choices = (
    (1, 'http'),
    (2, 'rpc'),
    (3, 'webcgi'),
    (4, 'overflow'),
    (5, 'systemflaw'),
)

allow_choices = (
    (1, '允许'),
    (0, '不允许'),
)

protocol_choices = (
    (6, 'TCP'),
    (17, 'UDP'),
    (0, '无限制'),
)

rule_type_choices = (
    (0, '无表达式'),
    (1, '正则表达式'),
)

match_type_choices = (
    (-1, '未选择'),
    (0, '子串匹配'),
    (1, '右匹配'),
    (2, '左匹配'),
    (3, '完全匹配'),
)


class TaskGroup(models.Model):
    """
    任务组的表
    """

    class Meta:
        db_table = 'task_group'

    id = models.AutoField(max_length=11, db_column='id', primary_key=True)
    group_id = models.BigIntegerField()
    name = models.CharField(max_length=64)
    rule_type = models.IntegerField()
    create_person = models.CharField(max_length=64, blank=True)
    create_time = models.DateTimeField()
    rule_id_list = models.TextField(blank=True)
    remarks = models.CharField(max_length=1024, blank=True)


class Task(models.Model):
    module            = models.IntegerField(default=0)
    version           = models.CharField(max_length=64, blank=True)
    cmd               = models.CharField(max_length=64)
    num               = models.IntegerField(default=0)
    config            = models.TextField()
    generate_time     = models.DateTimeField(null=True, blank=True)
    release_time      = models.DateTimeField(null=True, blank=True)
    is_valid          = models.IntegerField(default=1)
    device_id         = models.CharField(max_length=12, blank=True)
    is_success        = models.CharField(max_length=32, default='false')
    success_time      = models.DateTimeField(null=True, blank=True)
    user              = models.CharField(max_length=32, blank=True)

    class Meta:
        db_table = 'task'

    def __unicode__(self):
        return self.name


class Command(models.Model):
    cmd_type                = models.IntegerField()
    module                  = models.CharField(max_length=32, blank=True)
    submodule               = models.TextField(blank=True)
    filename                = models.CharField(max_length=128, blank=True)
    md5                     = models.CharField(max_length=128, blank=True)
    soft_version            = models.CharField(max_length=32, blank=True)
    save_path               = models.TextField(blank=True)
    param           = models.TextField(blank=True)
    version_check_result    = models.TextField(blank=True)
    version_check_post      = models.TextField(blank=True)
    generate_time           = models.DateTimeField(null=True, blank=True)
    release_time            = models.DateTimeField(null=True, blank=True)
    is_valid                = models.IntegerField(default=1)
    device_id               = models.CharField(max_length=12)
    success_time            = models.DateTimeField(null=True, blank=True)
    is_success              = models.CharField(max_length=32, default='false')
    version                 = models.CharField(max_length=64, blank=True)
    command_result          = models.CharField(max_length=16, default='未下发')

    class Meta:
        db_table = 'command'

    def __unicode__(self):
        return self.name


class TrojanRule(models.Model):
    rule_id                 = models.BigIntegerField()
    trojan_id               = models.IntegerField()
    store_pcap              = models.IntegerField(default=1)
    os                      = models.CharField(max_length=128, blank=True)
    trojan_name             = models.CharField(max_length=128)
    trojan_type             = models.IntegerField(choices=trojan_type_choices)
    desc                    = models.CharField(max_length=512, blank=True)
    rule                    = models.CharField(max_length=2048)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_trojan'

    def __unicode__(self):
        return self.name


class AttackRule(models.Model):
    rule_id                 = models.BigIntegerField()
    store_pcap              = models.IntegerField(default=1)
    rule                    = models.CharField(max_length=2048)
    attack_type             = models.IntegerField(choices=attack_type_choices)
    application             = models.CharField(max_length=128, blank=True)
    os                      = models.CharField(max_length=128, blank=True)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_attack'

    def __unicode__(self):
        return self.name


class MalwareRule(models.Model):
    rule_id                 = models.BigIntegerField()
    md5                     = models.CharField(max_length=128, blank=True)
    signature               = models.CharField(max_length=2048, blank=True)
    malware_type            = models.CharField(max_length=128)
    malware_name            = models.CharField(max_length=128)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_malware'

    def __unicode__(self):
        return self.name


class AbnormalRule(models.Model):
    rule_id                 = models.BigIntegerField()
    abn_type                = models.IntegerField()
    allow_file              = models.IntegerField(choices=allow_choices)
    risk_min                = models.IntegerField(choices=risk_choices)
    file_size_limit         = models.IntegerField()
    file_num_hour           = models.IntegerField()
    rate_limit              = models.IntegerField()
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_abnormal'

    def __unicode__(self):
        return self.name


class KeywordRule(models.Model):
    rule_type_cho = (
        (0, '关键词'),
        (1, '正则表达式'),
    )

    rule_id                 = models.BigIntegerField()
    rule_type               = models.IntegerField(choices=rule_type_cho)
    min_match_count         = models.IntegerField(default=1)
    rule_content            = models.CharField(max_length=512)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_keyword_file'

    def __unicode__(self):
        return self.name


class EncryptionRule(models.Model):
    rule_id                 = models.BigIntegerField()
    filesize_minsize        = models.IntegerField()
    filesize_maxsize        = models.IntegerField()
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_encryption_file'

    def __unicode__(self):
        return self.name


class CompressRule(models.Model):
    rule_id                 = models.BigIntegerField()
    depth                   = models.IntegerField()
    backsize                = models.IntegerField()
    dropsize                = models.IntegerField()
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_compress_file'

    def __unicode__(self):
        return self.name


class PictureRule(models.Model):
    rule_id                 = models.BigIntegerField()
    filesize_minsize        = models.IntegerField()
    filesize_maxsize        = models.IntegerField()
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_picture_file'

    def __unicode__(self):
        return self.name


class IPListenRule(models.Model):
    rule_id                 = models.BigIntegerField()
    sip                     = models.CharField(max_length=32)
    sport                   = models.CharField(max_length=32)
    dip                     = models.CharField(max_length=32)
    dport                   = models.CharField(max_length=32)
    protocol                = models.IntegerField(choices=protocol_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_ip_listen'

    def __unicode__(self):
        return self.name


class DNSListenRule(models.Model):
    rule_id                 = models.BigIntegerField()
    dns                     = models.CharField(max_length=64)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_dns_listen'

    def __unicode__(self):
        return self.name


class URLListenRule(models.Model):
    rule_id                 = models.BigIntegerField()
    url                     = models.CharField(max_length=128)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_url_listen'

    def __unicode__(self):
        return self.name


class AccountListenRule(models.Model):
    rule_id                 = models.BigIntegerField()
    account_type            = models.CharField(max_length=32)
    account                 = models.CharField(max_length=128)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_account_listen'

    def __unicode__(self):
        return self.name


class NetLogRule(models.Model):
    rule_id                 = models.BigIntegerField()
    interval                = models.IntegerField()
    num                     = models.IntegerField()
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_net_log'

    def __unicode__(self):
        return self.name


class AppBehaviorRule(models.Model):
    rule_id                 = models.BigIntegerField()
    interval                = models.IntegerField()
    num                     = models.IntegerField()
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_app_behavior'

    def __unicode__(self):
        return self.name


class WebFilterRule(models.Model):
    rule_id                 = models.BigIntegerField()
    url                     = models.CharField(max_length=128)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_web_filter'

    def __unicode__(self):
        return self.name


class DNSFilterRule(models.Model):
    rule_id                 = models.BigIntegerField()
    dns                     = models.CharField(max_length=64)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_dns_filter'

    def __unicode__(self):
        return self.name


class IPWhiteListRule(models.Model):
    rule_id                 = models.BigIntegerField()
    ip                      = models.CharField(max_length=32)
    port                    = models.CharField(max_length=32)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_ip_whitelist'

    def __unicode__(self):
        return self.name


class BlockRule(models.Model):
    rule_id                 = models.BigIntegerField()
    sip                     = models.CharField(max_length=32)
    sport                   = models.CharField(max_length=32)
    dip                     = models.CharField(max_length=32)
    dport                   = models.CharField(max_length=32)
    protocol                = models.IntegerField(default=6)
    version                 = models.CharField(max_length=32, blank=True)
    operate                 = models.CharField(max_length=64)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField(auto_now_add=True)
    operate_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)

    group_id = models.BigIntegerField(default=0, blank=True)
    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'rule_block'

    def __unicode__(self):
        return self.name
