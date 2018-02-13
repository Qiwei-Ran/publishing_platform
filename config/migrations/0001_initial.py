# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=64)),
                ('ip', models.IPAddressField(verbose_name='IP\u5730\u5740')),
                ('host_name', models.CharField(max_length=255, verbose_name='\u4e3b\u673a\u540d')),
                ('belong_projects', models.CharField(max_length=255, verbose_name='\u6240\u5c5e\u9879\u76ee')),
                ('user', models.CharField(max_length=255, verbose_name='\u767b\u5f55\u7528\u6237')),
                ('ssh_key', models.TextField(verbose_name='\u767b\u5f55key')),
                ('status', models.IntegerField(default=0, verbose_name='\u72b6\u6001', choices=[(1, '\u5728\u7ebf'), (0, '\u79bb\u7ebf')])),
                ('memo', models.TextField(verbose_name='\u5907\u6ce8', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('is_del', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4fe1\u606f',
                'verbose_name_plural': '\u4e3b\u673a\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
    ]
