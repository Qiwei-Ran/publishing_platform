# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OperaRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=255, verbose_name='\u7528\u6237')),
                ('request_method', models.CharField(max_length=255, verbose_name='\u8bf7\u6c42\u65b9\u6cd5')),
                ('request_url', models.CharField(max_length=255, verbose_name='\u8bf7\u6c42URL')),
                ('request_date', models.CharField(max_length=255, verbose_name='\u8bf7\u6c42\u6570\u636e')),
                ('create_time', models.TimeField(default=datetime.datetime(2018, 1, 19, 17, 38, 1, 768545), max_length=255, verbose_name='\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u64cd\u4f5c\u8bb0\u5f55',
                'verbose_name_plural': '\u64cd\u4f5c\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
    ]
