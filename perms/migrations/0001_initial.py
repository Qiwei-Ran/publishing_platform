# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings



class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=32, blank=True, unique=True)),
                ('group_name', models.CharField(unique=True, max_length=100, verbose_name='\u89d2\u8272\u540d\u79f0')),
                ('enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
                ('explanation', models.TextField(verbose_name='\u89d2\u8272\u63cf\u8ff0')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('group_user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237', blank=True)),
            ],
            options={
                'verbose_name': '\u89d2\u8272\u7ba1\u7406',
                'verbose_name_plural': '\u89d2\u8272\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuthSudo',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=32, blank=True, unique=True)),
                ('group_name', models.CharField(help_text='sudo\u7ec4', max_length=64, verbose_name='\u7ec4\u540d')),
                ('shell', models.TextField(verbose_name='\u547d\u4ee4')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'sudo\u6388\u6743',
                'db_table': 'AuthSudo',
                'managed': True,
                'verbose_name_plural': 'sudo\u6388\u6743',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAuthWeb',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=32, blank=True, unique=True)),
                ('select_project', models.BooleanField(default=False, verbose_name='\u67e5\u770b\u9879\u76ee')),
                ('add_project', models.BooleanField(default=False, verbose_name='\u65b0\u589e\u9879\u76ee')),
                ('del_project', models.BooleanField(default=False, verbose_name='\u5220\u9664\u9879\u76ee')),
                ('update_project', models.BooleanField(default=False, verbose_name='\u4fee\u6539\u9879\u76ee')),
                ('test_deploy', models.BooleanField(default=False, verbose_name='\u6d4b\u8bd5\u53d1\u5e03')),
                ('test_complete', models.BooleanField(default=False, verbose_name='\u6d4b\u8bd5\u5b8c\u6210')),
                ('online_deploy', models.BooleanField(default=False, verbose_name='\u7ebf\u4e0a\u53d1\u5e03')),
                ('log_look', models.BooleanField(default=False, verbose_name='\u65e5\u5fd7\u8bb0\u5f55')),
                ('group_name', models.ForeignKey(verbose_name='\u6240\u5c5e\u89d2\u8272', to='perms.AuthGroup', help_text='\u6dfb\u52a0\u89d2\u8272\u7ec4\u6743\u9650')),
            ],
            options={
                'verbose_name': '\u6743\u9650\u7ba1\u7406',
                'verbose_name_plural': '\u6743\u9650\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
    ]
