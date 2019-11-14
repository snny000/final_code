# -*- coding:utf-8 -*-
from rest_framework import serializers
from models import *


class DetectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detector
        fields = ('id', 'device_id', 'device_type', 'contractor', 'soft_version', 'device_ca',
                  'organs', 'address', 'address_code', 'contact', 'memo',
                  'register_time', 'register_frequency', 'register_status',
                  'register_fail_reason', 'op_person', 'op_ip', 'op_time',

                  'interface', 'mem_total', 'cpu_info', 'disk_info', 'auth_time',
                  'auth_frequency', 'auth_status', 'auth_fail_reason',

                  'is_online', 'last_warning_time', 'device_status', 'alarm_total_num',

                  'alarm_status',
                  'trojan_status', 'trojan_version',
                  'attack_status', 'attack_version',
                  'malware_status', 'malware_version',
                  'other_status', 'other_version',

                  'abnormal_status', 'abnormal_version',

                  'sensitive_status',
                  'finger_file_status', 'finger_file_version',
                  'sensitive_file_status', 'sensitive_file_version',
                  'keyword_file_status', 'keyword_file_version',
                  'encryption_file_status', 'encryption_file_version',
                  'compress_file_status', 'compress_file_version',
                  'picture_file_status', 'picture_file_version',
                  'style_file_status', 'style_file_version',

                  'object_listen_status',
                  'ip_listen_status', 'ip_listen_version',
                  'domain_listen_status', 'domain_listen_version',
                  'url_listen_status', 'url_listen_version',
                  'account_listen_status', 'account_listen_version',

                  'net_audit_status',
                  'net_log_status', 'net_log_version',
                  'app_behavior_status', 'app_behavior_version',
                  'web_filter_version', 'dns_filter_version',

                  'ip_whitelist_version',

                  'block_status', 'block_version',

                  'version_check_type',

                  'is_effective', 'comment', 'heartbeat_time')


class BusinessStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessStatus
        fields = ('id', 'uptime', 'soft_version', 'time', 'report_time', 'device_id')


class ModuleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleStatus
        fields = ('id', 'device_id', 'name', 'status', 'submodule', 'report_time')


class NetworkCardStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkCardStatus
        fields = ('id', 'interface_seq', 'interface_flag', 'interface_stat',
                  'interface_flow', 'interface_error', 'interface_drop',
                  'duration_time', 'report_time', 'device_id')


class SuspectedStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspectedStatus
        fields = ('id', 'event_type', 'time', 'risk', 'msg', 'report_time', 'device_id')


class PluginStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PluginStatus
        fields = ('id', 'plug_id', 'status', 'plug_version',
                  'plug_policy_version', 'report_time', 'device_id')


class SystemRunningStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemRunningStatus
        fields = ('id', 'cpu', 'mem', 'disk', 'time', 'plug_stat', 'report_time', 'device_id', 'did')


class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminLogin
        fields = ('id', 'login_id', 'login_password', 'level', 'create_time', 'update_time')


class DeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = ('id', 'device_id', 'soft_version', 'contractor', 'device_ca', 'organs', 'address', 'address_code',
                  'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info')


class DetectorOnlineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectorOnlineEvent
        fields = ('id', 'device_id', 'event', 'time')


class DetectorAuditModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectorAuditMode
        fields = ('id', 'mode')
