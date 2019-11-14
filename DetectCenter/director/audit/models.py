# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class AuditLog(models.Model):
    log_type                = models.IntegerField()
    request_id              = models.BigIntegerField()
    time                    = models.DateTimeField()
    filename                = models.TextField()
    filetype                = models.CharField(max_length=32, default='gz')
    checksum                = models.CharField(max_length=128)
    save_path               = models.TextField()
    receive_time            = models.DateTimeField()
    start_process_time      = models.DateTimeField(null=True, blank=True)
    end_process_time        = models.DateTimeField(null=True, blank=True)
    process_status          = models.IntegerField(default=2)
    device_id               = models.CharField(max_length=12)

    class Meta:
        db_table      = 'audit_log'

    def __unicode__(self):
        return self.device_id + 'audit_log'


class AuditSystem(models.Model):
    log_id            = models.CharField(max_length=20)
    user              = models.CharField(max_length=64)
    time              = models.DateTimeField()
    event_type        = models.CharField(max_length=64)
    opt_type          = models.CharField(max_length=64)
    message           = models.TextField(blank=True)

    report_time       = models.DateTimeField()
    device_id         = models.CharField(max_length=12)

    class Meta:
        db_table      = 'audit_system'

    def __unicode__(self):
        return self.device_id + 'audit_system'
        
        
class AuditManagement(models.Model):
    log_id            = models.CharField(max_length=20)
    user              = models.CharField(max_length=64, blank=True)
    time              = models.DateTimeField()
    event_type        = models.CharField(max_length=64)
    opt_type          = models.CharField(max_length=64)
    message           = models.TextField(blank=True)

    device_id         = models.CharField(max_length=12, blank=True)
    
    is_send_command   = models.IntegerField(default=0)

    class Meta:
        db_table      = 'audit_management'

    def __unicode__(self):
        return self.device_id + 'audit_management'
