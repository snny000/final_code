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

prevalence_choices = (
    (1, '高'),
    (2, '中'),
    (3, '低'),
)

trojan_type_choices = (
    (1, '特种木马'),
    (2, '普通木马'),
    (3, '远控'),
    (4, '其他')
)

alert_type_choices = (
    (1, '电子密标文件告警'),
    (2, '标密文件告警'),
    (3, '关键词告警'),
    (4, '加密文件告警'),
    (5, '多层压缩文件告警'),
    (6, '图文文件告警'),
    (7, '含图文的文档告警'),
    (8, '版式文件告警')
)

xm_dir_choices = (
    (1, '发送'),
    (2, '接收'),
    (3, '未知'),
)


class AlarmAll(models.Model):
    alarm_id          = models.CharField(max_length=20)
    sip               = models.GenericIPAddressField()
    dip               = models.GenericIPAddressField()
    risk              = models.IntegerField(choices=risk_choices)
    device_id         = models.CharField(max_length=12)
    time              = models.DateTimeField()
    warning_module    = models.IntegerField()
    warning_type      = models.IntegerField()

    rule_id = models.BigIntegerField(blank=True, default=0)
    group_id = models.BigIntegerField(blank=True, default=0)

    class Meta:
        db_table = 'alarm_all'

    def __unicode__(self):
        return self.name


class AlarmTrojan(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id           = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)

    trojan_id         = models.IntegerField()
    os                = models.CharField(max_length=128, blank=True)
    trojan_name       = models.CharField(max_length=128)
    trojan_type       = models.IntegerField(choices=trojan_type_choices)
    desc              = models.CharField(max_length=512, blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'alarm_trojan'

    def __unicode__(self):
        return self.name


class AlarmTrojanFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    is_upload         = models.BooleanField(default=False)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32)

    trojan_id         = models.IntegerField()

    report_time       = models.DateTimeField()
    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'alarm_trojan_file'

    def __unicode__(self):
        return self.name


class AlarmAttack(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)

    attack_type       = models.CharField(max_length=128)
    application       = models.CharField(max_length=128, blank=True)
    os                = models.CharField(max_length=128, blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'alarm_attack'

    def __unicode__(self):
        return self.name


class AlarmAttackFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    is_upload         = models.BooleanField(default=False)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32)

    report_time       = models.DateTimeField()
    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'alarm_attack_file'

    def __unicode__(self):
        return self.name


class AlarmMalware(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)

    malware_type      = models.CharField(max_length=128)
    malware_name      = models.CharField(max_length=128)

    protocol          = models.CharField(max_length=32)
    sender            = models.CharField(max_length=128, blank=True)
    recver            = models.TextField(blank=True)
    cc                = models.TextField(blank=True)
    bcc               = models.TextField(blank=True)
    subject           = models.TextField(blank=True)
    mail_from         = models.TextField(blank=True)
    rcpt_to           = models.TextField(blank=True)
    ehlo              = models.TextField(blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'alarm_malware'

    def __unicode__(self):
        return self.name


class AlarmMalwareFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    is_upload         = models.BooleanField(default=False)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'alarm_malware_file'

    def __unicode__(self):
        return self.name


class AlarmOther(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)

    desc              = models.CharField(max_length=512)

    report_time       = models.DateTimeField()
    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'alarm_other'

    def __unicode__(self):
        return self.name


class AlarmOtherFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    is_upload         = models.BooleanField(default=False)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'alarm_other_file'

    def __unicode__(self):
        return self.name


class AlarmAbnormal(models.Model):

    abnormal_type_choices = (
        (1, '可疑心跳保活行为'),
        (2, '远程控制行为'),
        (3, '异常私有协议'),
        (4, '异常通用代理行为')
    )

    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    alert_type        = models.IntegerField(choices=abnormal_type_choices)
    alert_policy      = models.CharField(max_length=64)
    alert_desc        = models.CharField(max_length=512)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)

    report_time       = models.DateTimeField()
    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'alarm_abnormal'

    def __unicode__(self):
        return self.name


class AlarmAbnormalFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'alarm_abnormal_file'

    def __unicode__(self):
        return self.name


class SensitiveEmail(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    alert_type        = models.IntegerField(choices=alert_type_choices)
    rule_id = models.BigIntegerField()
    risk              = models.IntegerField(choices=risk_choices)
    time              = models.DateTimeField()
    sm_inpath         = models.CharField(max_length=512, blank=True)
    sm_summary        = models.CharField(max_length=512, blank=True)
    sm_desc           = models.CharField(max_length=128, blank=True)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    xm_dir            = models.IntegerField(choices=xm_dir_choices)
    app_pro           = models.CharField(max_length=16)

    sender            = models.CharField(max_length=128)
    receiver          = models.TextField()
    cc                = models.TextField(blank=True)
    bcc               = models.TextField(blank=True)
    subject           = models.CharField(max_length=256)
    domain            = models.CharField(max_length=64, blank=True)
    mail_from         = models.TextField(blank=True)
    rcpt_to           = models.TextField(blank=True)
    ehlo              = models.TextField(blank=True)
    protocol          = models.CharField(max_length=32, blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'sensitive_email'

    def __unicode__(self):
        return self.name


class SensitiveIm(models.Model):
    id                 = models.IntegerField(primary_key=True)
    alarm_id           = models.CharField(max_length=20)
    alert_type         = models.IntegerField(choices=alert_type_choices)
    rule_id = models.BigIntegerField()
    risk               = models.IntegerField(choices=risk_choices)
    time               = models.DateTimeField()
    sm_inpath          = models.CharField(max_length=512, blank=True)
    sm_summary         = models.CharField(max_length=512, blank=True)
    sm_desc            = models.CharField(max_length=128, blank=True)
    dip                = models.GenericIPAddressField()
    dport              = models.IntegerField()
    dmac               = models.CharField(max_length=18)
    sip                = models.GenericIPAddressField()
    sport              = models.IntegerField()
    smac               = models.CharField(max_length=18)
    xm_dir             = models.IntegerField(choices=xm_dir_choices)
    app_pro            = models.CharField(max_length=16)

    protocol           = models.CharField(max_length=32)
    sender             = models.CharField(max_length=128, blank=True)
    receiver           = models.TextField(blank=True)
    account            = models.CharField(max_length=128, blank=True)
    msg_content        = models.TextField(blank=True)

    report_time        = models.DateTimeField()

    device_id          = models.CharField(max_length=12)

    class Meta:
        db_table       = 'sensitive_im'

    def __unicode__(self):
        return self.name


class SensitiveFileTransfer(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    alert_type        = models.IntegerField(choices=alert_type_choices)
    rule_id = models.BigIntegerField()
    risk              = models.IntegerField(choices=risk_choices)
    time              = models.DateTimeField()
    sm_inpath         = models.CharField(max_length=512, blank=True)
    sm_summary        = models.CharField(max_length=512, blank=True)
    sm_desc           = models.CharField(max_length=128, blank=True)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    xm_dir            = models.IntegerField(choices=xm_dir_choices)
    app_pro           = models.CharField(max_length=16)

    protocol          = models.CharField(max_length=32)
    account           = models.CharField(max_length=32, blank=True)
    pwd               = models.CharField(max_length=32, blank=True)
    trans_dir         = models.IntegerField(choices=xm_dir_choices)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'sensitive_filetransfer'

    def __unicode__(self):
        return self.name


class SensitiveHttp(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    alert_type        = models.IntegerField(choices=alert_type_choices)
    rule_id = models.BigIntegerField()
    risk              = models.IntegerField(choices=risk_choices)
    time              = models.DateTimeField()
    sm_inpath         = models.CharField(max_length=512, blank=True)
    sm_summary        = models.CharField(max_length=512, blank=True)
    sm_desc           = models.CharField(max_length=128, blank=True)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    xm_dir            = models.IntegerField(choices=xm_dir_choices)
    app_pro           = models.CharField(max_length=16)

    protocol          = models.CharField(max_length=32)
    domain            = models.CharField(max_length=128)
    url               = models.TextField()
    method            = models.CharField(max_length=8)
    ret_code          = models.IntegerField(blank=True)
    user_agent        = models.TextField(blank=True)
    cookie            = models.TextField(blank=True)
    server            = models.TextField(blank=True)
    refer             = models.TextField(blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'sensitive_http'

    def __unicode__(self):
        return self.name


class SensitiveNetdisk(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    alert_type        = models.IntegerField(choices=alert_type_choices)
    rule_id = models.BigIntegerField()
    risk              = models.IntegerField(choices=risk_choices)
    time              = models.DateTimeField()
    sm_inpath         = models.CharField(max_length=512, blank=True)
    sm_summary        = models.CharField(max_length=512, blank=True)
    sm_desc           = models.CharField(max_length=128, blank=True)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    xm_dir            = models.IntegerField(choices=xm_dir_choices)
    app_pro           = models.CharField(max_length=16)

    protocol          = models.CharField(max_length=32)
    account           = models.TextField(blank=True)
    domain            = models.TextField(blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'sensitive_netdisk'

    def __unicode__(self):
        return self.name


class SensitiveOther(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    alert_type        = models.IntegerField(choices=alert_type_choices)
    rule_id = models.BigIntegerField()
    risk              = models.IntegerField(choices=risk_choices)
    time              = models.DateTimeField()
    sm_inpath         = models.CharField(max_length=512, blank=True)
    sm_summary        = models.CharField(max_length=512, blank=True)
    sm_desc           = models.CharField(max_length=128, blank=True)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    xm_dir            = models.IntegerField(choices=xm_dir_choices)
    app_pro           = models.CharField(max_length=16)
    app_opt           = models.TextField()

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table = 'sensitive_other'

    def __unicode__(self):
        return self.name


class SensitiveAllFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    filename          = models.CharField(max_length=64)
    checksum          = models.CharField(max_length=128)
    is_upload         = models.BooleanField(default=False)
    filetype          = models.CharField(max_length=32, blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'sensitive_all_file'

    def __unicode__(self):
        return self.name


class TargetInterceptIP(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'intercept_ip'

    def __unicode__(self):
        return self.name


class TargetInterceptIPFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32, default='pcap')

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'intercept_ip_file'

    def __unicode__(self):
        return self.name


class TargetInterceptDNS(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)
    dns               = models.TextField()
    domain_ip         = models.TextField()

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'intercept_dns'

    def __unicode__(self):
        return self.name


class TargetInterceptDNSFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32, default='pcap')

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'intercept_dns_file'

    def __unicode__(self):
        return self.name


class TargetInterceptURL(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)
    url               = models.TextField()
    method            = models.CharField(max_length=8)
    ret_code          = models.IntegerField(blank=True)
    user_agent        = models.TextField(blank=True)
    cookie            = models.TextField(blank=True)
    server            = models.TextField(blank=True)
    refer             = models.TextField(blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'intercept_url'

    def __unicode__(self):
        return self.name


class TargetInterceptURLFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32, default='pcap')

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'intercept_url_file'

    def __unicode__(self):
        return self.name


class TargetInterceptAccount(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()
    risk              = models.IntegerField(choices=risk_choices)
    sender            = models.CharField(max_length=128)
    receiver          = models.TextField()
    cc                = models.TextField(blank=True)
    bcc               = models.TextField(blank=True)
    subject           = models.CharField(max_length=256, blank=True)
    mail_content      = models.TextField(blank=True)
    attachment        = models.TextField(blank=True)

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'intercept_account'

    def __unicode__(self):
        return self.name


class TargetInterceptAccountFile(models.Model):
    time              = models.DateTimeField()
    alarm_id          = models.CharField(max_length=20)
    num               = models.IntegerField()
    filename          = models.CharField(max_length=64)
    checksum          = models.CharField(max_length=128)
    filetype          = models.CharField(max_length=32, default='pcap')

    report_time       = models.DateTimeField()

    device_id         = models.CharField(max_length=12)
    save_path         = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table      = 'intercept_account_file'

    def __unicode__(self):
        return self.name


class Block(models.Model):
    id                = models.IntegerField(primary_key=True)
    alarm_id          = models.CharField(max_length=20)
    rule_id = models.BigIntegerField()
    sip               = models.GenericIPAddressField()
    sport             = models.IntegerField()
    smac              = models.CharField(max_length=18)
    dip               = models.GenericIPAddressField()
    dport             = models.IntegerField()
    dmac              = models.CharField(max_length=18)
    time              = models.DateTimeField()

    report_time       = models.DateTimeField()
    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'alarm_block'

    def __unicode__(self):
        return self.name
