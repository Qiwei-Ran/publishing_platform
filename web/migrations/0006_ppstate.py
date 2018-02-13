# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20171115_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='PpState',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.IntegerField(max_length=255)),
            ],
            options={
                'db_table': 'pp_state',
            },
            bases=(models.Model,),
        ),
    ]
