# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_ppprojectdetail_deploy_success'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ppprojectdetail',
            old_name='deploy_success',
            new_name='deploy_success1',
        ),
    ]
