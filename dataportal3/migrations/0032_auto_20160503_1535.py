# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0031_auto_20160416_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spatialsurveylinkgroup',
            name='geom_table_name',
        ),
        migrations.RemoveField(
            model_name='spatialsurveylinkgroup',
            name='survey',
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='data_formatting',
            field=models.TextField(null=True, blank=True),
        ),
    ]
