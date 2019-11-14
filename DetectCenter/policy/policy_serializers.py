# -*- coding:utf-8 -*-
from rest_framework import serializers
from models import *


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ('id', 'group_id', 'name', 'rule_type', 'create_person', 'create_time', 'rule_id_list', 'remarks')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'module', 'version', 'cmd', 'num', 'config', 'generate_time',
                  'release_time', 'is_valid', 'device_id', 'is_success', 'success_time',
                  'user')


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('id', 'cmd_type', 'module', 'submodule', 'filename', 'md5', 'soft_version', 'save_path',
                  'param', 'version_check_result', 'version_check_post',
                  'generate_time', 'release_time', 'is_valid', 'device_id', 'command_result', 'is_success', 'success_time', 'version')


class TrojanRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrojanRule
        fields = ('id', 'rule_id', 'trojan_id', 'store_pcap', 'os', 'trojan_name', 'trojan_type',
                  'desc', 'rule', 'risk', 'version', 'operate', 'rule_status', 'creat_time',
                  'operate_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class AttackRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttackRule
        fields = ('id', 'rule_id', 'store_pcap', 'rule', 'attack_type', 'application', 'os',
                  'risk', 'version', 'operate', 'rule_status', 'creat_time', 'operate_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class MalwareRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MalwareRule
        fields = ('id', 'rule_id', 'md5', 'signature', 'malware_type', 'malware_name', 'risk',
                  'version', 'operate', 'rule_status', 'creat_time', 'operate_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class AbnormalRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbnormalRule
        fields = ('id', 'rule_id', 'abn_type', 'allow_file', 'risk_min', 'file_size_limit', 'file_num_hour',
                  'rate_limit',  'version', 'operate', 'rule_status', 'creat_time', 'operate_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class KeywordRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordRule
        fields = ('id', 'rule_id', 'rule_type', 'min_match_count', 'rule_content', 'risk', 'version',
                  'operate', 'rule_status', 'creat_time', 'operate_time', 'device_id_list_run',
                  'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class EncryptionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncryptionRule
        fields = ('id', 'rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list',
                  'remark', 'is_del', 'group_id', 'map_rule_id_list')


class CompressRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompressRule
        fields = ('id', 'rule_id', 'depth', 'backsize', 'dropsize', 'risk',  'version', 'operate',
                  'rule_status', 'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list',
                  'remark', 'is_del', 'group_id', 'map_rule_id_list')


class PictureRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureRule
        fields = ('id', 'rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list',
                  'remark', 'is_del', 'group_id', 'map_rule_id_list')


class IPListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPListenRule
        fields = ('id', 'rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'risk', 'version',
                  'operate', 'rule_status', 'creat_time', 'operate_time', 'device_id_list_run',
                  'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class DNSListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSListenRule
        fields = ('id', 'rule_id', 'dns', 'rule_type', 'match_type', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list',
                  'remark', 'is_del', 'group_id', 'map_rule_id_list')


class URLListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLListenRule
        fields = ('id', 'rule_id', 'url', 'rule_type', 'match_type', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list',
                  'remark', 'is_del', 'group_id', 'map_rule_id_list')


class AccountListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountListenRule
        fields = ('id', 'rule_id', 'account_type', 'account', 'rule_type', 'match_type', 'risk', 'version',
                  'operate', 'rule_status', 'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list',
                  'remark', 'is_del', 'group_id', 'map_rule_id_list')


class NetLogRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetLogRule
        fields = ('id', 'rule_id', 'interval', 'num', 'version', 'operate', 'rule_status', 'creat_time', 'operate_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class AppBehaviorRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppBehaviorRule
        fields = ('id', 'rule_id', 'interval', 'num', 'version', 'operate', 'rule_status', 'creat_time', 'operate_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class WebFilterRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebFilterRule
        fields = ('id', 'rule_id', 'url', 'rule_type', 'match_type', 'version', 'operate', 'rule_status',
                  'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class DNSFilterRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSFilterRule
        fields = ('id', 'rule_id', 'dns', 'rule_type',  'match_type', 'version', 'operate', 'rule_status',
                  'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class IPWhiteListRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPWhiteListRule
        fields = ('id', 'rule_id', 'ip', 'port', 'version', 'operate', 'rule_status', 'creat_time',
                  'operate_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'group_id', 'map_rule_id_list')


class BlockRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockRule
        fields = ('id', 'rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'version', 'operate',
                  'rule_status', 'creat_time', 'operate_time', 'device_id_list_run', 'device_id_list',
                  'remark', 'is_del', 'group_id', 'map_rule_id_list')
