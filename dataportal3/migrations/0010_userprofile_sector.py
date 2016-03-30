# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0009_auto_20151107_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='sector',
            field=models.TextField(null=True, blank=True),
        ),
    ]
