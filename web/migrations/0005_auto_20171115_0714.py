# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20171115_0636'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppprojectdetail',
            name='create_time',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ppprojectdetail',
            name='is_del',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ppprojectdetail',
            name='update_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
