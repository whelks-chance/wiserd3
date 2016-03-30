# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0006_auto_20151103_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='topojson_high',
            field=models.BooleanField(default=False),
        ),
    ]
