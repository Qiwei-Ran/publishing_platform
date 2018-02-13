# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_ppstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ppproject',
            name='is_del',
            field=models.CharField(default=0, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppproject',
            name='state',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='create_time',
            field=models.DateTimeField(null=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='deploy_address',
            field=models.CharField(max_length=255, verbose_name='\u7ebf\u4e0a\u53d1\u5e03\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='deploy_success',
            field=models.IntegerField(default=0, max_length=10, verbose_name='\u90e8\u7f72\u6210\u529f\u4e0e\u5426'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='description',
            field=models.CharField(max_length=255, verbose_name='\u5907\u6ce8', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='is_del',
            field=models.CharField(default=0, max_length=255, null=True, verbose_name='\u662f\u5426\u5220\u9664'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='project_name',
            field=models.CharField(max_length=255, verbose_name='\u9879\u76ee\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='relation_person',
            field=models.CharField(max_length=255, verbose_name='\u5173\u8054\u4eba'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='svn_address',
            field=models.CharField(max_length=255, verbose_name='SVN\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='test_address',
            field=models.CharField(max_length=255, verbose_name='\u6d4b\u8bd5\u53d1\u5e03\u5730\u5740'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ppprojectdetail',
            name='update_time',
            field=models.DateTimeField(null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', blank=True),
            preserve_default=True,
        ),
    ]
