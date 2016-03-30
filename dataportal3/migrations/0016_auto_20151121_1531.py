# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0015_auto_20151119_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurecollectionstore',
            name='topojson_file',
            field=models.FileField(max_length=512, null=True, upload_to=b'', blank=True),
        ),
    ]
