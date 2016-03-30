# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0027_auto_20160218_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='spatialsurveylink',
            name='category',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='category_cy',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='full_name',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='full_name_cy',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='notes_cy',
            field=models.TextField(null=True, blank=True),
        ),
    ]
