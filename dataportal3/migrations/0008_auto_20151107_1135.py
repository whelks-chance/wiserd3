# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0007_userpreferences_topojson_high'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='init_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='institution',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='speciality',
            field=models.TextField(null=True, blank=True),
        ),
    ]
