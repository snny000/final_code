# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class PluginAlarm(models.Model):
    time                    = models.DateTimeField(null=True, blank=True)
    alarm_id                = models.CharField(max_length=20, blank=True)
    plug_id                 = models.BigIntegerField(null=True, blank=True)
    num                     = models.IntegerField(null=True, blank=True)
    filename                = models.CharField(max_length=64)
    checksum                = models.CharField(max_length=128)
    filetype                = models.CharField(max_length=32, blank=True)

    device_id               = models.CharField(max_length=12)
    report_time             = models.DateTimeField()
    save_path               = models.TextField()

    class Meta:
        db_table = 'plugin_alarm'

    def __unicode__(self):
        return self.name


class PluginStatus(models.Model):
    plug_id                 = models.BigIntegerField()
    status                  = models.CharField(max_length=20)

    device_id               = models.CharField(max_length=12)
    report_time             = models.DateTimeField()

    class Meta:
        db_table = 'plugin_status'

    def __unicode__(self):
        return self.name


########################################################################################
class PluginDetector(models.Model):
    cmd = models.CharField(max_length=128)
    plug_type = models.CharField(max_length=10, blank=True)
    plug_id = models.BigIntegerField()
    plug_version = models.CharField(max_length=16, blank=True)
    plug_config_version = models.CharField(max_length=16, blank=True)
    cpu = models.IntegerField(default=0)
    mem = models.IntegerField(default=0)
    disk = models.IntegerField(default=0)
    plug_status = models.IntegerField()
    version = models.CharField(max_length=64, blank=True)
    device_id_list = models.TextField(blank=True)
    device_id_list_run = models.TextField(blank=True)
    plug_on_device_status = models.TextField(blank=True)
    generate_time = models.DateTimeField()
    plug_path = models.TextField(blank=True)
    plug_config_path = models.TextField(blank=True)
    is_del = models.IntegerField()
    plug_name = models.CharField(max_length=64, blank=True)
    plug_config_name = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = 'plugin_detector'

    def __unicode__(self):
        return self.name


class PlugTask(models.Model):
    version           = models.CharField(max_length=64, blank=True)
    cmd               = models.CharField(max_length=32)
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
        db_table = 'plug_task'

    def __unicode__(self):
        return self.name
