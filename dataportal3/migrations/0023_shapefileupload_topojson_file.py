# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0022_auto_20160105_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='shapefileupload',
            name='topojson_file',
            field=models.FileField(max_length=512, null=True, upload_to=b'', blank=True),
        ),
    ]
