# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userauthweb',
            name='add_department',
            field=models.BooleanField(default=False, verbose_name='\u90e8\u95e8\u7ba1\u7406'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userauthweb',
            name='add_user',
            field=models.BooleanField(default=False, verbose_name='\u6dfb\u52a0\u7528\u6237'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userauthweb',
            name='delete_user',
            field=models.BooleanField(default=False, verbose_name='\u5220\u9664\u7528\u6237'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userauthweb',
            name='edit_pass',
            field=models.BooleanField(default=False, verbose_name='\u4fee\u6539\u5bc6\u7801'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userauthweb',
            name='edit_user',
            field=models.BooleanField(default=False, verbose_name='\u4fee\u6539\u7528\u6237'),
            preserve_default=True,
        ),
    ]
