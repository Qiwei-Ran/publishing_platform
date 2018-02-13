# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='\u90ae\u7bb1')),
                ('username', models.CharField(unique=True, max_length=30, verbose_name='\u7528\u6237\u540d')),
                ('first_name', models.CharField(max_length=30, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last_name')),
                ('mobile', models.CharField(max_length=30, verbose_name='\u624b\u673a', validators=[django.core.validators.RegexValidator(b'^[0-9+()-]+$', 'Enter a valid mobile number.', b'invalid')])),
                ('session_key', models.CharField(max_length=60, null=True, verbose_name='session_key', blank=True)),
                ('user_key', models.TextField(null=True, verbose_name='user_key', blank=True)),
                ('menu_status', models.BooleanField(default=False, verbose_name='\u7528\u6237\u83dc\u5355\u72b6\u6001')),
                ('user_active', models.BooleanField(default=0, verbose_name='\u8bbe\u7f6e\u5bc6\u7801\u72b6\u6001')),
                ('uuid', models.CharField(unique=True, max_length=64)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DepartmentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department_groups_name', models.CharField(max_length=64, null=True, verbose_name='\u7ec4\u540d', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u4ecb\u7ecd', blank=True)),
            ],
            options={
                'verbose_name': '\u90e8\u95e8\u7ec4',
                'verbose_name_plural': '\u90e8\u95e8\u7ec4',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DepartmentMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department_name', models.CharField(max_length=64, null=True, verbose_name='\u90e8\u95e8\u540d\u79f0', blank=True)),
                ('description', models.TextField(null=True, verbose_name='\u4ecb\u7ecd', blank=True)),
                ('desc_gid', models.IntegerField(blank=True, null=True, verbose_name='\u90e8\u95e8\u7ec4', choices=[(1001, '\u8fd0\u7ef4\u90e8'), (1002, '\u7f51\u7edc\u90e8'), (1003, '\u7814\u53d1\u90e8'), (1004, '\u6d4b\u8bd5\u90e8')])),
            ],
            options={
                'verbose_name': '\u90e8\u95e8',
                'verbose_name_plural': '\u90e8\u95e8',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customuser',
            name='department',
            field=models.ForeignKey(related_name='users', verbose_name='\u90e8\u95e8', blank=True, to='users.DepartmentMode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
