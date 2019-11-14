# -*- coding:utf-8 -*-
from rest_framework import serializers
from models import *


class DirectorTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorTask
        fields = ('id', 'module', 'version', 'cmd', 'num', 'config', 'generate_time',
                  'release_time', 'is_valid', 'device_id', 'is_success', 'success_time', 'down_job_id', 'down_node_id')


class DirectorTrojanRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorTrojanRule
        fields = ('id', 'task_id', 'rule_id', 'trojan_id', 'store_pcap', 'os', 'trojan_name', 'trojan_type',
                  'desc', 'rule', 'risk', 'version', 'operate', 'rule_status', 'creat_time',
                  'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorAttackRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorAttackRule
        fields = ('id', 'task_id', 'rule_id', 'store_pcap', 'rule', 'attack_type', 'application', 'os',
                  'risk', 'version', 'operate', 'rule_status', 'creat_time', 'receive_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorMalwareRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorMalwareRule
        fields = ('id', 'task_id', 'rule_id', 'md5', 'signature', 'malware_type', 'malware_name', 'risk',
                  'version', 'operate', 'rule_status', 'creat_time', 'receive_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorAbnormalRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorAbnormalRule
        fields = ('id', 'task_id', 'rule_id', 'abn_type', 'allow_file', 'risk_min', 'file_size_limit', 'file_num_hour',
                  'rate_limit',  'version', 'operate', 'rule_status', 'creat_time', 'receive_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorKeywordRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorKeywordRule
        fields = ('id', 'task_id', 'rule_id', 'rule_type', 'min_match_count', 'rule_content', 'risk', 'version',
                  'operate', 'rule_status', 'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorEncryptionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorEncryptionRule
        fields = ('id', 'task_id', 'rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorCompressRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorCompressRule
        fields = ('id', 'task_id', 'rule_id', 'depth', 'backsize', 'dropsize', 'risk',  'version', 'operate',
                  'rule_status', 'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorPictureRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorPictureRule
        fields = ('id', 'task_id', 'rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorIPListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorIPListenRule
        fields = ('id', 'task_id', 'rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'risk', 'version', 'operate', 
                  'rule_status', 'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorDNSListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorDNSListenRule
        fields = ('id', 'task_id', 'rule_id', 'dns', 'rule_type', 'match_type', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'device_id_list', 'receive_time', 'device_id_list_run', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorURLListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorURLListenRule
        fields = ('id', 'task_id', 'rule_id', 'url', 'rule_type', 'match_type', 'risk', 'version', 'operate',
                  'rule_status', 'creat_time', 'device_id_list', 'receive_time', 'device_id_list_run', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorAccountListenRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorAccountListenRule
        fields = ('id', 'task_id', 'rule_id', 'account_type', 'account', 'rule_type', 'match_type', 'risk', 'version',
                  'operate', 'rule_status', 'device_id_list', 'creat_time', 'receive_time', 'device_id_list_run', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorNetLogRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorNetLogRule
        fields = ('id', 'task_id', 'rule_id', 'interval', 'num', 'version', 'operate', 'rule_status', 'creat_time', 'receive_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorAppBehaviorRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorAppBehaviorRule
        fields = ('id', 'task_id', 'rule_id', 'interval', 'num', 'version', 'operate', 'rule_status', 'creat_time', 'receive_time',
                  'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorWebFilterRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorWebFilterRule
        fields = ('id', 'task_id', 'rule_id', 'url', 'rule_type', 'match_type', 'version', 'operate', 'rule_status',
                  'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorDNSFilterRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorDNSFilterRule
        fields = ('id', 'task_id', 'rule_id', 'dns', 'rule_type',  'match_type', 'version', 'operate', 'rule_status',
                  'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorIPWhiteListRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorIPWhiteListRule
        fields = ('id', 'task_id', 'rule_id', 'ip', 'port', 'version', 'operate', 'rule_status', 'creat_time',
                  'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')


class DirectorBlockRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorBlockRule
        fields = ('id', 'task_id', 'rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'version', 'operate',
                  'rule_status', 'creat_time', 'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'is_del', 'src_node', 'map_rule_id_list')

                  
class DirectorPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorPlugin
        fields = ('id', 'cmd', 'version', 'plug_type', 'plug_id', 'plug_version', 'plug_config_version', 'cpu', 'mem',
                  'disk', 'plug_name', 'plug_config_name', 'plug_path', 'plug_config_path', 'generate_time',
                  'receive_time', 'device_id_list_run', 'device_id_list', 'remark', 'plug_status', 'is_del', 'src_node',
                  'is_plug_data_release', 'is_plug_file_release', 'is_config_file_release',
                  # 'is_add_plug_data_release', 'is_add_plug_file_release', 'is_add_config_file_release',
                  # 'is_update_plug_data_release', 'is_update_plug_file_release', 'is_update_config_file_release',
                  # 'is_update_config_data_release', 'is_update_config_file_release',
                  'down_job_id', 'plug_url', 'plug_config_url')
                  
                  
class DirectorPluginTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorPluginTask
        fields = ('id', 'version', 'cmd', 'num', 'generate_time', 'release_time', 'is_valid', 'device_id', 'config',
                  'is_success', 'success_time', 'down_job_id', 'down_node_id')


class DirectorCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorCommand
        fields = ('id', 'cmd_type', 'module', 'submodule', 'filename', 'md5', 'soft_version', 'save_path',
                  'param', 'version_check_result', 'version_check_post',
                  'generate_time', 'release_time', 'is_valid', 'device_id', 'command_result', 'is_success', 'success_time', 'version', 'down_job_id', 'down_node_id')


class ManagementCenterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementCenterInfo
        fields = ('id', 'center_id', 'center_ip', 'soft_version', 'device_ca', 'organs', 'address', 'address_code',
                  'contact', 'mem_total', 'interface', 'cpu_info', 'disk_info',
                  'center_status', 'register_time', 'register_frequency', 'register_status', 'register_fail_reason',
                  'auth_time', 'auth_frequency', 'auth_status', 'auth_fail_reason', 'cookie',
                  'center_serial', 'src_node', 'src_ip', 'ip_whitelist')


class DirectorPolicyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorPolicyJob
        fields = ('id', 'job_id', 'src_node', 'issue_type', 'issue_times', 'policy_type', 'receive_time', 'is_valid', 'success_time', 'job_result')


class DirectorPluginJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorPluginJob
        fields = ('id', 'job_id', 'src_node', 'issue_type', 'issue_times', 'receive_time', 'is_valid', 'success_time', 'job_result')


class DirectorCommandJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorCommandJob
        fields = ('id', 'job_id', 'src_node', 'cmd_type', 'issue_type', 'issue_times', 'receive_time', 'is_valid', 'success_time', 'job_result')
