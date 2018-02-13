# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_remove_ppproject_war_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppproject',
            name='war_path',
            field=models.CharField(default=b'di', max_length=255),
            preserve_default=True,
        ),
    ]
