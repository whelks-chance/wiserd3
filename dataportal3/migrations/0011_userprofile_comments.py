# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0010_userprofile_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
    ]
