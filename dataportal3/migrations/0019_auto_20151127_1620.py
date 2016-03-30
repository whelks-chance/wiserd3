# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0018_auto_20151124_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='spatialsurveylink',
            name='data_prefix',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='data_suffix',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='data_type',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='users',
            field=models.ManyToManyField(to='dataportal3.UserProfile'),
        ),
    ]
