# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operarecord',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 19, 17, 39, 57, 94750), max_length=255, verbose_name='\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
