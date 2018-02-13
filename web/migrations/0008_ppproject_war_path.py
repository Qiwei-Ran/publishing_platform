# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20171130_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppproject',
            name='war_path',
            field=models.CharField(default='baidu', unique=False, max_length=255),
            preserve_default=False,
        ),
    ]
