# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-23 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0007_auto_20170908_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementCenterInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('center_id', models.CharField(max_length=12)),
                ('soft_version', models.CharField(max_length=32)),
                ('organs', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=128)),
                ('address_code', models.CharField(max_length=6)),
                ('contact', models.TextField()),
                ('mem_total', models.IntegerField(default=0)),
                ('interface', models.TextField()),
                ('cpu_info', models.TextField()),
                ('disk_info', models.TextField()),
                ('access_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'management_center_info',
            },
        ),
        migrations.AddField(
            model_name='auditmanagement',
            name='is_send_command',
            field=models.IntegerField(default=0),
        ),
    ]