#-*- coding: utf-8 -*-
from rest_framework import serializers
from models import *


class PluginAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginAlarm
        fields = ('id', 'time', 'alarm_id', 'plug_id', 'num', 'filename',
                  'checksum', 'filetype', 'device_id', 'report_time', 'save_path'
                  )


class PluginStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginStatus
        fields = ('id', 'plug_id', 'status', 'device_id', 'report_time')


#################################################################################################################
class PluginDetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginDetector
        fields = ('id', 'cmd', 'plug_type', 'plug_id', 'plug_version', 'plug_config_version',
                  'cpu', 'mem', 'disk', 'device_id_list', 'generate_time', 'plug_path', 'plug_config_path',
                  'device_id_list_run', 'plug_status', 'is_del', 'plug_name', 'plug_config_name')

class PlugTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlugTask
        fields = ('id', 'version', 'cmd', 'num', 'config', 'generate_time', 'release_time', 'is_valid', 'device_id', 'is_success',
                  'success_time', 'user')