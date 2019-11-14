# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


risk_choices = (
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
    (0, '子串匹配'),
    (1, '右匹配'),
    (2, '左匹配'),
    (3, '完全匹配'),
)


class DirectorTask(models.Model):
    module            = models.IntegerField(default=0)
    version           = models.CharField(max_length=64, blank=True)
    cmd               = models.CharField(max_length=8)
    num               = models.IntegerField(default=0)
    config            = models.TextField()
    generate_time     = models.DateTimeField(null=True, blank=True)
    release_time      = models.DateTimeField(null=True, blank=True)
    is_valid          = models.IntegerField(default=1)
    device_id         = models.CharField(max_length=12, blank=True)
    is_success        = models.CharField(max_length=32, default='false')
    success_time      = models.DateTimeField(null=True, blank=True)

    down_job_id = models.CharField(max_length=64, blank=True)   # 指挥中心生成的对应任务的任务ID
    down_node_id = models.CharField(max_length=64, blank=True)   # 指挥中心下发该任务的指挥节点ID，用于反馈echo时填入DST_NODE头字段

    class Meta:
        db_table = 'director_task'

    def __unicode__(self):
        return self.name


class DirectorTrojanRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    trojan_id               = models.IntegerField()
    store_pcap              = models.IntegerField(default=1)
    os                      = models.CharField(max_length=128, blank=True)
    trojan_name             = models.CharField(max_length=128)
    trojan_type             = models.IntegerField(choices=trojan_type_choices)
    desc                    = models.CharField(max_length=512, blank=True)
    rule                    = models.CharField(max_length=2048)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField()
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_trojan'

    def __unicode__(self):
        return self.name


class DirectorAttackRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    store_pcap              = models.IntegerField(default=1)
    rule                    = models.CharField(max_length=2048)
    attack_type             = models.IntegerField(choices=attack_type_choices)
    application             = models.CharField(max_length=128, blank=True)
    os                      = models.CharField(max_length=128, blank=True)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField()
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_attack'

    def __unicode__(self):
        return self.name


class DirectorMalwareRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    md5                     = models.CharField(max_length=128, blank=True)
    signature               = models.CharField(max_length=2048, blank=True)
    malware_type            = models.CharField(max_length=128)
    malware_name            = models.CharField(max_length=128)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_malware'

    def __unicode__(self):
        return self.name


class DirectorAbnormalRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    abn_type                = models.IntegerField()
    allow_file              = models.IntegerField(choices=allow_choices)
    risk_min                = models.IntegerField(choices=risk_choices)
    file_size_limit         = models.IntegerField()
    file_num_hour           = models.IntegerField()
    rate_limit              = models.IntegerField()
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_abnormal'

    def __unicode__(self):
        return self.name


class DirectorKeywordRule(models.Model):
    rule_type_cho = (
        (0, '关键词'),
        (1, '正则表达式'),
    )

    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    rule_type               = models.IntegerField(choices=rule_type_cho)
    min_match_count         = models.IntegerField(default=1)
    rule_content            = models.CharField(max_length=512)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_keyword_file'

    def __unicode__(self):
        return self.name


class DirectorEncryptionRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    filesize_minsize        = models.IntegerField()
    filesize_maxsize        = models.IntegerField()
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_encryption_file'

    def __unicode__(self):
        return self.name


class DirectorCompressRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    depth                   = models.IntegerField()
    backsize                = models.IntegerField()
    dropsize                = models.IntegerField()
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_compress_file'

    def __unicode__(self):
        return self.name


class DirectorPictureRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    filesize_minsize        = models.IntegerField()
    filesize_maxsize        = models.IntegerField()
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_picture_filter'

    def __unicode__(self):
        return self.name


class DirectorIPListenRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    sip                     = models.CharField(max_length=32)
    sport                   = models.CharField(max_length=32)
    dip                     = models.CharField(max_length=32)
    dport                   = models.CharField(max_length=32)
    protocol                = models.IntegerField(choices=protocol_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_ip_listen'

    def __unicode__(self):
        return self.name


class DirectorDNSListenRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    dns                     = models.CharField(max_length=64)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_dns_listen'

    def __unicode__(self):
        return self.name


class DirectorURLListenRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    url                     = models.CharField(max_length=128)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_url_listen'

    def __unicode__(self):
        return self.name


class DirectorAccountListenRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    account_type            = models.CharField(max_length=32)
    account                 = models.CharField(max_length=128)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    risk                    = models.IntegerField(choices=risk_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_account_listen'

    def __unicode__(self):
        return self.name


class DirectorNetLogRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    interval                = models.IntegerField()
    num                     = models.IntegerField()
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_net_log'

    def __unicode__(self):
        return self.name


class DirectorAppBehaviorRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    interval                = models.IntegerField()
    num                     = models.IntegerField()
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_app_behavior'

    def __unicode__(self):
        return self.name


class DirectorWebFilterRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    url                     = models.CharField(max_length=128)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_web_filter'

    def __unicode__(self):
        return self.name


class DirectorDNSFilterRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    dns                     = models.CharField(max_length=64)
    rule_type               = models.IntegerField(choices=rule_type_choices)
    match_type              = models.IntegerField(choices=match_type_choices)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_dns_filter'

    def __unicode__(self):
        return self.name


class DirectorIPWhiteListRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    ip                      = models.CharField(max_length=32)
    port                    = models.CharField(max_length=32)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_ip_whitelist'

    def __unicode__(self):
        return self.name


class DirectorBlockRule(models.Model):
    task_id                 = models.BigIntegerField()
    rule_id                 = models.BigIntegerField()
    sip                     = models.CharField(max_length=32)
    sport                   = models.CharField(max_length=32)
    dip                     = models.CharField(max_length=32)
    dport                   = models.CharField(max_length=32)
    protocol                = models.IntegerField(default=6)
    version                 = models.CharField(max_length=64, blank=True)
    operate                 = models.CharField(max_length=64, blank=True)
    rule_status             = models.IntegerField(default=1)
    creat_time              = models.DateTimeField()
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    is_del                  = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    map_rule_id_list = models.TextField(blank=True)

    class Meta:
        db_table = 'director_rule_block'

    def __unicode__(self):
        return self.name
        
        
class DirectorPlugin(models.Model):
    cmd = models.CharField(max_length=128, blank=True)
    version = models.CharField(max_length=64, blank=True)
    plug_type               = models.CharField(max_length=10, blank=True)
    plug_id                 = models.IntegerField()
    plug_version            = models.CharField(max_length=16, blank=True)
    plug_config_version     = models.CharField(max_length=16, blank=True)
    cpu         = models.IntegerField(default=0)
    mem         = models.IntegerField(default=0)
    disk        = models.IntegerField(default=0)
    plug_name               = models.TextField(blank=True)
    plug_config_name        = models.TextField(blank=True)
    plug_path               = models.TextField(blank=True)
    plug_config_path        = models.TextField(blank=True)
    generate_time           = models.DateTimeField(null=True, blank=True)
    receive_time            = models.DateTimeField(null=True, blank=True)
    device_id_list_run      = models.TextField(blank=True)
    device_id_list          = models.TextField(blank=True)
    remark                  = models.TextField(blank=True)
    plug_status             = models.IntegerField(default=0)
    is_del              = models.IntegerField(default=1)
    src_node                = models.CharField(max_length=64, blank=True)

    is_plug_data_release = models.SmallIntegerField(default=0)         # 标识插件数据是否收到, 0: 未收到 1: 已收到
    is_plug_file_release = models.SmallIntegerField(default=0)         # 标识插件文件是否收到, 0: 未收到 1: 已收到
    is_config_file_release = models.SmallIntegerField(default=0)       # 标识插件配置文件是否收到, 0: 未收到 1: 已收到

    # is_add_plug_data_release = models.IntegerField(default=0)                  # 下发添加插件命令数据是否已收到 0: 未收到 1: 已收到
    # is_add_plug_file_release = models.IntegerField(default=0)                  # 新增插件文件是否已收到 0: 未收到 1: 已收到
    # is_add_config_file_release = models.IntegerField(default=0)                # 新增插件配置文件是否已收到 0: 未收到 1: 已收到
    #
    # is_update_plug_data_release = models.IntegerField(default=0)           # 下发更新插件命令数据是否已收到 0: 未收到 1: 已收到
    # is_update_plug_file_release = models.IntegerField(default=0)           # 下发更新插件命令插件文件是否已收到 0: 未收到 1: 已收到
    # is_update_config_file_release = models.IntegerField(default=0)    # 下发更新插件命令插件配置文件是否已收到 0: 未收到 1: 已收到
    #
    # is_update_config_data_release = models.IntegerField(default=0)         # 下发更新插件配置命令数据是否已收到 0: 未收到 1: 已收到
    # is_update_config_file_release = models.IntegerField(default=0)         # 下发更新插件配置命令文件是否已收到 0: 未收到 1: 已收到

    plug_url = models.TextField(blank=True)
    plug_config_url = models.TextField(blank=True)

    down_job_id = models.CharField(max_length=64, blank=True)  # 指挥中心生成的对应任务的任务ID


    class Meta:
        db_table = 'director_plugin'

    def __unicode__(self):
        return self.plug_id


class DirectorPluginTask(models.Model):
    version = models.CharField(max_length=64, blank=True)
    cmd = models.CharField(max_length=128)
    num = models.IntegerField(default=0)
    config = models.TextField()
    generate_time           = models.DateTimeField(null=True, blank=True)
    release_time            = models.DateTimeField(null=True, blank=True)
    is_valid                = models.IntegerField(default=1)
    device_id               = models.CharField(max_length=12)
    is_success              = models.IntegerField(default=0)
    success_time            = models.DateTimeField(null=True, blank=True)

    down_job_id = models.CharField(max_length=64, blank=True)  # 指挥中心生成的对应任务的任务ID
    down_node_id = models.CharField(max_length=64, blank=True)  # 指挥中心下发该任务的指挥节点ID，用于反馈echo时填入DST_NODE头字段

    class Meta:
        db_table = 'director_plug_task'

    def __unicode__(self):
        return self.version


class DirectorCommand(models.Model):
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

    down_job_id = models.CharField(max_length=64, blank=True)  # 指挥中心生成的对应任务的任务ID
    down_node_id = models.CharField(max_length=64, blank=True)  # 指挥中心下发该任务的指挥节点ID，用于反馈echo时填入DST_NODE头字段

    class Meta:
        db_table = 'director_command'

    def __unicode__(self):
        return self.name


class ManagementCenterInfo(models.Model):
    center_id         = models.CharField(max_length=12)
    center_serial = models.IntegerField(default=0)
    center_ip = models.CharField(max_length=64, blank=True)

    soft_version      = models.CharField(max_length=32)
    device_ca         = models.TextField()
    organs            = models.CharField(max_length=64)
    address           = models.CharField(max_length=128)
    address_code      = models.CharField(max_length=6)
    contact           = models.TextField()
    mem_total         = models.IntegerField(default=0)
    interface         = models.TextField()
    cpu_info          = models.TextField()
    disk_info         = models.TextField()

    center_status = models.SmallIntegerField(default=6)    # 待注册

    register_time               = models.DateTimeField(null=True, blank=True)
    register_frequency          = models.IntegerField(default=0)
    register_status             = models.IntegerField(default=2)       # （0：注册成功；1：注册失败；2：注册未审核）
    register_fail_reason        = models.CharField(max_length=64, blank=True)

    auth_time = models.DateTimeField(null=True, blank=True)
    auth_frequency = models.IntegerField(default=0)
    auth_status = models.IntegerField(default=2)                       #  (0: 认证成功  1：认证失败 2: 未认证)
    auth_fail_reason = models.CharField(max_length=64, blank=True)

    cookie = models.CharField(max_length=64, blank=True)

    src_node = models.CharField(max_length=64, blank=True)
    src_ip = models.CharField(max_length=64, blank=True)
    ip_whitelist = models.TextField(blank=True)

    class Meta:
        db_table = 'management_center_info'

    def __unicode__(self):
        return self.center_id


director_job_issue_type = [
    (0, '增量下发'),
    (1, '全量检测器'),
    (2, '全量管理中心')
]


director_job_status = [
    (0, '无效'),
    (1, '执行中'),
    (2, '执行成功'),
    (3, '执行失败')
]


class DirectorPolicyJob(models.Model):
    job_id = models.CharField(max_length=64)
    src_node = models.CharField(max_length=64)
    issue_type = models.SmallIntegerField(choices=director_job_issue_type)
    issue_times = models.IntegerField(default=1)
    policy_type = models.SmallIntegerField()      # 从1开始
    receive_time = models.DateTimeField(auto_now_add=True)
    is_valid = models.SmallIntegerField(choices=director_job_status)
    success_time = models.DateTimeField(blank=True)
    job_result = models.TextField(blank=True, default='执行中')

    class Meta:
        db_table = 'director_policy_job'

    def __unicode__(self):
        return self.job_id


class DirectorPluginJob(models.Model):
    job_id = models.CharField(max_length=64)
    src_node = models.CharField(max_length=64)
    issue_type = models.SmallIntegerField(choices=director_job_issue_type)
    issue_times = models.IntegerField(default=1)
    receive_time = models.DateTimeField(auto_now_add=True)
    is_valid = models.SmallIntegerField(choices=director_job_status)
    success_time = models.DateTimeField(blank=True)
    job_result = models.TextField(blank=True, default='执行中')

    class Meta:
        db_table = 'director_plugin_job'

    def __unicode__(self):
        return self.job_id


class DirectorCommandJob(models.Model):
    job_id = models.CharField(max_length=64)
    src_node = models.CharField(max_length=64)
    cmd_type = models.SmallIntegerField()  # 从1开始
    issue_type = models.SmallIntegerField(choices=director_job_issue_type)
    issue_times = models.IntegerField(default=1)
    receive_time = models.DateTimeField(auto_now_add=True)
    is_valid = models.SmallIntegerField(choices=director_job_status)
    success_time = models.DateTimeField(blank=True)
    job_result = models.TextField(blank=True, default='执行中')

    class Meta:
        db_table = 'director_command_job'

    def __unicode__(self):
        return self.job_id