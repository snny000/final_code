# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-12 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DirectorAbnormalRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('abn_type', models.IntegerField()),
                ('allow_file', models.IntegerField(choices=[(1, '\u5141\u8bb8'), (0, '\u4e0d\u5141\u8bb8')])),
                ('risk_min', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('file_size_limit', models.IntegerField()),
                ('file_num_hour', models.IntegerField()),
                ('rate_limit', models.IntegerField()),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_abnormal',
            },
        ),
        migrations.CreateModel(
            name='DirectorAccountListenRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('account_type', models.CharField(max_length=32)),
                ('account', models.CharField(max_length=128)),
                ('rule_type', models.IntegerField(choices=[(0, '\u65e0\u8868\u8fbe\u5f0f'), (1, '\u6b63\u5219\u8868\u8fbe\u5f0f')])),
                ('match_type', models.IntegerField(choices=[(0, '\u5b50\u4e32\u5339\u914d'), (1, '\u53f3\u5339\u914d'), (2, '\u5de6\u5339\u914d'), (3, '\u5b8c\u5168\u5339\u914d')])),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_account_listen',
            },
        ),
        migrations.CreateModel(
            name='DirectorAppBehaviorRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('interval', models.IntegerField()),
                ('num', models.IntegerField()),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_app_behavior',
            },
        ),
        migrations.CreateModel(
            name='DirectorAttackRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('store_pcap', models.IntegerField(default=1)),
                ('rule', models.CharField(max_length=2048)),
                ('attack_type', models.IntegerField(choices=[(1, 'http'), (2, 'rpc'), (3, 'webcgi'), (4, 'overflow'), (5, 'systemflaw')])),
                ('application', models.CharField(blank=True, max_length=128)),
                ('os', models.CharField(blank=True, max_length=128)),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField()),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_attack',
            },
        ),
        migrations.CreateModel(
            name='DirectorBlockRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('sip', models.CharField(max_length=32)),
                ('sport', models.CharField(max_length=32)),
                ('dip', models.CharField(max_length=32)),
                ('dport', models.CharField(max_length=32)),
                ('protocol', models.IntegerField(default=6)),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_block',
            },
        ),
        migrations.CreateModel(
            name='DirectorCompressRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('depth', models.IntegerField()),
                ('backsize', models.IntegerField()),
                ('dropsize', models.IntegerField()),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_compress_file',
            },
        ),
        migrations.CreateModel(
            name='DirectorDNSFilterRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('dns', models.CharField(max_length=64)),
                ('rule_type', models.IntegerField(choices=[(0, '\u65e0\u8868\u8fbe\u5f0f'), (1, '\u6b63\u5219\u8868\u8fbe\u5f0f')])),
                ('match_type', models.IntegerField(choices=[(0, '\u5b50\u4e32\u5339\u914d'), (1, '\u53f3\u5339\u914d'), (2, '\u5de6\u5339\u914d'), (3, '\u5b8c\u5168\u5339\u914d')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_dns_filter',
            },
        ),
        migrations.CreateModel(
            name='DirectorDNSListenRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('dns', models.CharField(max_length=64)),
                ('rule_type', models.IntegerField(choices=[(0, '\u65e0\u8868\u8fbe\u5f0f'), (1, '\u6b63\u5219\u8868\u8fbe\u5f0f')])),
                ('match_type', models.IntegerField(choices=[(0, '\u5b50\u4e32\u5339\u914d'), (1, '\u53f3\u5339\u914d'), (2, '\u5de6\u5339\u914d'), (3, '\u5b8c\u5168\u5339\u914d')])),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_dns_listen',
            },
        ),
        migrations.CreateModel(
            name='DirectorEncryptionRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('filesize_minsize', models.IntegerField()),
                ('filesize_maxsize', models.IntegerField()),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_encryption_file',
            },
        ),
        migrations.CreateModel(
            name='DirectorIPListenRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('sip', models.CharField(max_length=32)),
                ('sport', models.CharField(max_length=32)),
                ('dip', models.CharField(max_length=32)),
                ('dport', models.CharField(max_length=32)),
                ('protocol', models.IntegerField(choices=[(6, 'TCP'), (17, 'UDP'), (0, '\u65e0\u9650\u5236')])),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_ip_listen',
            },
        ),
        migrations.CreateModel(
            name='DirectorIPWhiteListRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('ip', models.CharField(max_length=32)),
                ('port', models.CharField(max_length=32)),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_ip_whitelist',
            },
        ),
        migrations.CreateModel(
            name='DirectorKeywordRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('rule_type', models.IntegerField(choices=[(0, '\u5173\u952e\u8bcd'), (1, '\u6b63\u5219\u8868\u8fbe\u5f0f')])),
                ('min_match_count', models.IntegerField(default=1)),
                ('rule_content', models.CharField(max_length=512)),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_keyword_file',
            },
        ),
        migrations.CreateModel(
            name='DirectorMalwareRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('md5', models.CharField(blank=True, max_length=128)),
                ('signature', models.CharField(blank=True, max_length=2048)),
                ('malware_type', models.CharField(max_length=128)),
                ('malware_name', models.CharField(max_length=128)),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_malware',
            },
        ),
        migrations.CreateModel(
            name='DirectorNetLogRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('interval', models.IntegerField()),
                ('num', models.IntegerField()),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_net_log',
            },
        ),
        migrations.CreateModel(
            name='DirectorPictureRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('filesize_minsize', models.IntegerField()),
                ('filesize_maxsize', models.IntegerField()),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_picture_file',
            },
        ),
        migrations.CreateModel(
            name='DirectorPlugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plug_type', models.CharField(blank=True, max_length=10)),
                ('plug_id', models.IntegerField()),
                ('plug_version', models.CharField(blank=True, max_length=16)),
                ('plug_config_version', models.CharField(blank=True, max_length=16)),
                ('plug_config_cpu', models.IntegerField(default=0)),
                ('plug_config_mem', models.IntegerField(default=0)),
                ('plug_config_disk', models.IntegerField(default=0)),
                ('plug_name', models.TextField(blank=True)),
                ('plug_config_name', models.TextField(blank=True)),
                ('plug_path', models.TextField(blank=True)),
                ('plug_config_path', models.TextField(blank=True)),
                ('generate_time', models.DateTimeField(blank=True, null=True)),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('device_id_list', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('plug_status', models.IntegerField(default=0)),
                ('is_release', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_plugin',
            },
        ),
        migrations.CreateModel(
            name='DirectorPluginTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plug_cmd_type', models.CharField(max_length=16)),
                ('plug_cmd_detail', models.TextField()),
                ('generate_time', models.DateTimeField(blank=True, null=True)),
                ('release_time', models.DateTimeField(blank=True, null=True)),
                ('is_valid', models.IntegerField(default=1)),
                ('device_id', models.CharField(max_length=12)),
                ('is_success', models.IntegerField(default=0)),
                ('success_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'director_plug_task',
            },
        ),
        migrations.CreateModel(
            name='DirectorTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.IntegerField(default=0)),
                ('version', models.CharField(blank=True, max_length=32)),
                ('cmd', models.CharField(max_length=8)),
                ('num', models.IntegerField(default=0)),
                ('config', models.TextField()),
                ('generate_time', models.DateTimeField(blank=True, null=True)),
                ('release_time', models.DateTimeField(blank=True, null=True)),
                ('is_valid', models.IntegerField(default=1)),
                ('device_id', models.CharField(blank=True, max_length=12)),
                ('is_success', models.CharField(default='false', max_length=32)),
                ('success_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'director_task',
            },
        ),
        migrations.CreateModel(
            name='DirectorTrojanRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('trojan_id', models.IntegerField()),
                ('store_pcap', models.IntegerField(default=1)),
                ('os', models.CharField(blank=True, max_length=128)),
                ('trojan_name', models.CharField(max_length=128)),
                ('trojan_type', models.IntegerField(choices=[(1, '\u7279\u79cd\u6728\u9a6c'), (2, '\u666e\u901a\u6728\u9a6c'), (3, '\u8fdc\u63a7'), (4, '\u5176\u4ed6')])),
                ('desc', models.CharField(blank=True, max_length=512)),
                ('rule', models.CharField(max_length=2048)),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField()),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_trojan',
            },
        ),
        migrations.CreateModel(
            name='DirectorURLListenRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('url', models.CharField(max_length=128)),
                ('rule_type', models.IntegerField(choices=[(0, '\u65e0\u8868\u8fbe\u5f0f'), (1, '\u6b63\u5219\u8868\u8fbe\u5f0f')])),
                ('match_type', models.IntegerField(choices=[(0, '\u5b50\u4e32\u5339\u914d'), (1, '\u53f3\u5339\u914d'), (2, '\u5de6\u5339\u914d'), (3, '\u5b8c\u5168\u5339\u914d')])),
                ('risk', models.IntegerField(choices=[(0, '\u65e0\u98ce\u9669'), (1, '\u4e00\u822c\u7ea7'), (2, '\u5173\u6ce8\u7ea7'), (3, '\u4e25\u91cd\u7ea7'), (4, '\u7d27\u6025\u7ea7')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_url_listen',
            },
        ),
        migrations.CreateModel(
            name='DirectorWebFilterRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.BigIntegerField()),
                ('rule_id', models.BigIntegerField()),
                ('url', models.CharField(max_length=128)),
                ('rule_type', models.IntegerField(choices=[(0, '\u65e0\u8868\u8fbe\u5f0f'), (1, '\u6b63\u5219\u8868\u8fbe\u5f0f')])),
                ('match_type', models.IntegerField(choices=[(0, '\u5b50\u4e32\u5339\u914d'), (1, '\u53f3\u5339\u914d'), (2, '\u5de6\u5339\u914d'), (3, '\u5b8c\u5168\u5339\u914d')])),
                ('version', models.CharField(blank=True, max_length=32)),
                ('operate', models.CharField(max_length=8)),
                ('rule_status', models.IntegerField(default=1)),
                ('creat_time', models.DateTimeField()),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('device_id_list_run', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('is_del', models.IntegerField(default=1)),
                ('src_node', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'db_table': 'director_rule_web_filter',
            },
        ),
    ]