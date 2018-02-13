# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PpOperateRecord',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('user', models.CharField(max_length=255, blank=True)),
                ('operation', models.CharField(max_length=255, blank=True)),
                ('project', models.CharField(max_length=255, blank=True)),
                ('crate_time', models.DateTimeField(null=True, blank=True)),
                ('update_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'pp_operate_record',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PpProject',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('project_name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('state', models.IntegerField()),
                ('create_time', models.DateTimeField()),
                ('update_time', models.DateTimeField(null=True, blank=True)),
                ('is_del', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'pp_project',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PpProjectDetail',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('project_name', models.CharField(max_length=255)),
                ('svn_address', models.CharField(max_length=255)),
                ('relation_person', models.CharField(max_length=255)),
                ('test_address', models.CharField(max_length=255)),
                ('deploy_address', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'db_table': 'pp_project_detail',
            },
            bases=(models.Model,),
        ),
    ]
