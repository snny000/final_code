# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import *


class AlarmAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmAll
        fields = ('id', 'alarm_id', 'sip', 'dip', 'risk', 'device_id',
                  'time', 'warning_module', 'warning_type', 'rule_id', 'group_id')


class AlarmAllFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmAllFile
        fields = ('id', 'time', 'alarm_id', 'num', 'filename', 'is_upload',
                  'checksum', 'filetype', 'trojan_id', 'report_time',
                  'device_id', 'save_path')


class AlarmTrojanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmTrojan
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'trojan_id',
                  'os', 'trojan_name', 'trojan_type', 'desc', 'report_time',
                  'device_id')


class AlarmAttackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmAttack
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'attack_type',
                  'application', 'os', 'report_time', 'device_id')


class AlarmMalwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmMalware
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'malware_type',
                  'malware_name', 'protocol', 'sender', 'recver', 'cc',
                  'bcc', 'subject', 'mail_from', 'rcpt_to', 'ehlo',
                  'report_time', 'device_id')


class AlarmOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmOther
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'desc',
                  'report_time', 'device_id')


class AlarmAbnormalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmAbnormal
        fields = ('id', 'alarm_id', 'sip', 'sport', 'smac', 'dip',
                  'dport', 'dmac', 'alert_type', 'alert_policy',
                  'alert_desc', 'time', 'risk', 'report_time',
                  'device_id')


class SensitiveEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveEmail
        fields = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'sender', 'receiver', 'cc',
                  'bcc', 'subject', 'domain', 'mail_from', 'rcpt_to',
                  'ehlo', 'protocol', 'report_time', 'device_id')


class SensitiveImSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveIm
        fields = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'sender', 'receiver',
                  'account', 'msg_content', 'report_time', 'device_id')


class SensitiveFileTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveFileTransfer
        fields = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'account', 'pwd',
                  'trans_dir', 'report_time', 'device_id')


class SensitiveHttpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveHttp
        fields = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'domain', 'url',
                  'method', 'ret_code', 'user_agent', 'cookie',
                  'server', 'refer', 'report_time', 'device_id')


class SensitiveNetdiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveNetdisk
        fields = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'protocol', 'account',
                  'domain', 'report_time', 'device_id')


class SensitiveOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveOther
        fields = ('id', 'alarm_id', 'alert_type', 'rule_id', 'risk',
                  'time', 'sm_inpath', 'sm_summary', 'sm_desc',
                  'dip', 'dport', 'dmac', 'sip', 'sport', 'smac',
                  'xm_dir', 'app_pro', 'app_opt', 'report_time',
                  'device_id')


class TargetInterceptIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetInterceptIP
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'report_time',
                  'device_id')


class TargetInterceptDNSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetInterceptDNS
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'dns',
                  'domain_ip', 'report_time', 'device_id')


class TargetInterceptURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetInterceptURL
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'url',
                  'method', 'ret_code', 'user_agent', 'cookie',
                  'server', 'refer', 'report_time', 'device_id')


class TargetInterceptAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetInterceptAccount
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac',
                  'dip', 'dport', 'dmac', 'time', 'risk', 'sender',
                  'receiver', 'cc', 'bcc', 'subject', 'mail_content',
                  'attachment', 'report_time', 'device_id')


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'alarm_id', 'rule_id', 'sip', 'sport', 'smac', 'dip',
                  'dport', 'dmac', 'time', 'report_time', 'device_id')
