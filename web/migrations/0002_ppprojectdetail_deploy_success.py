# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppprojectdetail',
            name='deploy_success',
            field=models.IntegerField(default=0, max_length=10),
            preserve_default=True,
        ),
    ]
