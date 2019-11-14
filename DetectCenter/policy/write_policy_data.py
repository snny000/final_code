# -*- coding: utf-8 -*-

import os
import sys
import django

pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DetectCenter.settings")

django.setup()

from policy.models import TrojanRule, AttackRule, MalwareRule, AbnormalRule, KeywordRule, EncryptionRule, CompressRule, PictureRule, IPListenRule, DNSListenRule, URLListenRule, AccountListenRule, NetLogRule, AppBehaviorRule, WebFilterRule, DNSFilterRule, IPWhiteListRule, BlockRule
from director.models import *
from detector.models import Detector
from DetectCenter import config, settings
from django.db.models import Q
from django.core.serializers import serialize
import json
import ConfigParser
import time


module = {
    'trojan': TrojanRule,
    'attack': AttackRule,
    'malware': MalwareRule,
    'abnormal': AbnormalRule,
    'keyword_file': KeywordRule,
    'encryption_file': EncryptionRule,
    'compress_file': CompressRule,
    'picture_filter': PictureRule,
    'ip_listen': IPListenRule,
    'domain_listen': DNSListenRule,
    'url_listen': URLListenRule,
    'account_listen': AccountListenRule,
    'net_log': NetLogRule,
    'app_behavior': AppBehaviorRule,
    'web_filter': WebFilterRule,
    'dns_filter': DNSFilterRule,
    'ip_whitelist': IPWhiteListRule,
    'block': BlockRule
}

director_rule_models = {
    'trojan': DirectorTrojanRule,
    'attack': DirectorAttackRule,
    'malware': DirectorMalwareRule,
    'abnormal': DirectorAbnormalRule,
    'keyword_file': DirectorKeywordRule,
    'encryption_file': DirectorEncryptionRule,
    'compress_file': DirectorCompressRule,
    'picture_filter': DirectorPictureRule,
    'ip_listen': DirectorIPListenRule,
    'domain_listen': DirectorDNSListenRule,
    'url_listen': DirectorURLListenRule,
    'account_listen': DirectorAccountListenRule,
    'net_log': DirectorNetLogRule,
    'app_behavior': DirectorAppBehaviorRule,
    'web_filter': DirectorWebFilterRule,
    'dns_filter': DirectorDNSFilterRule,
    'ip_whitelist': DirectorIPWhiteListRule,
    'block': DirectorBlockRule
}

def get_rule_fields(module_name):

    result_set = ()     # 规则内容的集合

    if module_name == 'trojan':  # 木马攻击检测
        result_set = ('rule_id', 'trojan_id', 'store_pcap', 'os', 'trojan_name', 'trojan_type', 'desc',
                      'rule', 'risk')
    elif module_name == 'attack':  # 漏洞利用检测
        result_set = ('rule_id', 'store_pcap', 'rule', 'attack_type', 'application', 'os', 'risk')
    elif module_name == 'malware':  # 恶意程序检测
        result_set = ('rule_id', 'md5', 'signature', 'malware_type', 'malware_name', 'risk')
    elif module_name == 'abnormal':  # 未知攻击窃密检测文件上传
        result_set = ('rule_id', 'abn_type', 'allow_file', 'risk_min', 'file_size_limit', 'file_num_hour', 'rate_limit')
    elif module_name == 'keyword_file':  # 关键词检测
        result_set = ('rule_id', 'rule_type', 'min_match_count', 'rule_content', 'risk')
    elif module_name == 'encryption_file':  # 加密文件筛选
        result_set = ('rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk')
    elif module_name == 'compress_file':  # 压缩文件检测
        result_set = ('rule_id', 'depth', 'backsize', 'dropsize', 'risk')
    elif module_name == 'picture_filter':  # 图片筛选回传
        result_set = ('rule_id', 'filesize_minsize', 'filesize_maxsize', 'risk')
    elif module_name == 'ip_listen':  # IP侦听检测
        result_set = ('rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol', 'risk')
    elif module_name == 'domain_listen':  # 域名侦听检测
        result_set = ('rule_id', 'dns', 'rule_type', 'match_type', 'risk')
    elif module_name == 'url_listen':  # URL侦听检测
        result_set = ('rule_id', 'url', 'rule_type', 'match_type', 'risk')
    elif module_name == 'account_listen':  # 账号侦听检测
        result_set = ('rule_id', 'account_type', 'account', 'rule_type', 'match_type', 'risk')
    elif module_name == 'net_log':  # 通联关系上传
        result_set = ('rule_id', 'interval', 'num')
    elif module_name == 'app_behavior':  # 应用行为上传
        result_set = ('rule_id', 'interval', 'num')
    elif module_name == 'web_filter':  # web过滤
        result_set = ('rule_id', 'url', 'rule_type', 'match_type')
    elif module_name == 'dns_filter':  # dns过滤
        result_set = ('rule_id', 'dns', 'rule_type', 'match_type')
    elif module_name == 'ip_whitelist':  # IP白名单策略
        result_set = ('rule_id', 'ip', 'port')
    elif module_name == 'block':  # 阻断策略
        result_set = ('rule_id', 'sip', 'sport', 'dip', 'dport', 'protocol')
    else:
        pass

    return result_set

    
cf = ConfigParser.ConfigParser()
cf.read(settings.BASE_DIR + "/policy/policy_flag.txt")

    

def process_policy(module_name):
    if not config.const.UPLOAD_BUSINESS_DISPOSAL:
        # print '##############################'
        return
    policy_flag = cf.getint('policy_flag', module_name)
    
    file_dir = config.const.DISPOSAL_DIR + 'policy/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_name = module_name + '_' + str(int(time.time())) + '_' + str(policy_flag)
    policy_flag += 1
    cf.set('policy_flag', module_name, policy_flag)
    with open(settings.BASE_DIR + "/policy/policy_flag.txt", 'wb') as f_flag:
        cf.write(f_flag)

    file_path = file_dir + file_name

    with open(file_path, 'wb') as f_handler:
    
        device_id_all = list(Detector.objects.filter(device_status=1).values_list('id', 'device_id'))
        id_device_dict = {item[0]: item[1] for item in device_id_all}   # id与device_id的对应关系

        data_type = ''
        if module_name in ['trojan', 'attack', 'malware', 'abnormal']:
            data_type = 'alarm(' + module_name + ')'
        elif module_name in ['keyword_file', 'encryption_file', 'compress_file', 'picture_filter']:
            data_type = 'sensitive(' + module_name + ')'
        elif module_name in ['ip_listen', 'domain_listen', 'url_listen', 'account_listen']:
            data_type = 'object_listen(' + module_name + ')'
        elif module_name in ['net_log', 'app_behavior', 'web_filter', 'dns_filter']:
            data_type = 'net_audit(' + module_name + ')'
        elif module_name == 'ip_whitelist':
            data_type = 'ip_whitelist(' + module_name + ')'
        elif module_name == 'block':
            data_type = 'block(' + module_name + ')'


        for d_id in id_device_dict.values():
            # print "d_id:", d_id
            rules = []
            director_rules = []
            query_data = module[module_name].objects.filter(Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
            if query_data.exists():
                result_set = get_rule_fields(module_name)   # 获取查询的规则集合
                rule_json = serialize('json', query_data, fields=result_set)  # 序列化成json
                rules = [data['fields'] for data in json.loads(rule_json)]
                if module_name == 'attack':       # 漏洞利用规则，修改数字对应的攻击类型
                    for data in rules:
                        data['attack_type'] = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw'][data['attack_type'] - 1]
                elif module_name in ['encryption_file', 'picture_filter']:    # 加密规则或图片规则，修改config的组织方式
                    for data in rules:
                        data['encryption_file'] = {"minsize": data.pop('filesize_minsize'), "maxsize": data.pop('filesize_maxsize')}
                elif module_name == 'compress_file':       # 压缩规则，修改config的组织方式
                    for data in rules:
                        data['filesize'] = {"backsize": data.pop('backsize'), "dropsize": data.pop('dropsize')}
            director_query_data = director_rule_models[module_name].objects.filter(
                Q(device_id_list_run__contains='#' + str(d_id) + '#') | Q(device_id_list_run='#'), is_del=1)
            if director_query_data.exists():
                result_set = get_rule_fields(module_name)  # 获取查询的规则集合
                director_rule_json = serialize('json', director_query_data, fields=result_set)  # 序列化成json
                director_rules = [data['fields'] for data in json.loads(director_rule_json)]
                if module_name == 'attack':  # 漏洞利用规则，修改数字对应的攻击类型
                    for data in director_rules:
                        data['attack_type'] = ['http', 'rpc', 'webcgi', 'overflow', 'systemflaw'][data['attack_type'] - 1]
                elif module_name in ['encryption_file', 'picture_filter']:  # 加密规则或图片规则，修改config的组织方式
                    for data in director_rules:
                        data['encryption_file'] = {"minsize": data.pop('filesize_minsize'),
                                                   "maxsize": data.pop('filesize_maxsize')}
                elif module_name == 'compress_file':  # 压缩规则，修改config的组织方式
                    for data in director_rules:
                        data['filesize'] = {"backsize": data.pop('backsize'), "dropsize": data.pop('dropsize')}
            # print ""
            # print ""
            # print rules, director_rules
            # print ""
            # print ""
            rules.extend(director_rules)
            if rules:
                # print data_type, rules
                f_handler.write(config.const.DISPOSAL_BOUNDARY + '\n')
                f_handler.write('User-Agent:' + d_id + '\n')
                f_handler.write('Type:' + data_type + '\n')
                f_handler.write(json.dumps(rules))


def process_all_policy():
    for name in module.keys():
        process_policy(name)


if __name__ == '__main__':
    for name in module.keys():
        process_policy(name)
