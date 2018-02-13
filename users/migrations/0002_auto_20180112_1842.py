# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='\u540d\u5b57'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_key',
            field=models.TextField(null=True, verbose_name='\u7528\u6237\u767b\u5f55key', blank=True),
            preserve_default=True,
        ),
    ]
