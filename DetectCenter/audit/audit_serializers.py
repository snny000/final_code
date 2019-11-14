# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import *


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'log_type', 'request_id', 'time', 'filename', 'filetype', 'checksum',
                  'save_path', 'receive_time', 'start_process_time', 'end_process_time',
                  'process_status', 'device_id')


class AuditSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditSystem
        fields = ('id', 'log_id', 'user', 'time', 'event_type', 'opt_type',
                  'message', 'report_time', 'device_id')
                
class AuditManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditManagement
        fields = ('id', 'log_id', 'user', 'time', 'event_type', 'opt_type',
                  'message', 'device_id', 'is_send_command')
