# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20171115_0635'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ppprojectdetail',
            old_name='deploy_success1',
            new_name='deploy_success',
        ),
    ]
