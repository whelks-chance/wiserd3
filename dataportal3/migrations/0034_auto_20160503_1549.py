# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0033_auto_20160503_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spatialsurveylink',
            name='link_groups',
            field=models.ManyToManyField(to='dataportal3.SpatialSurveyLinkGroup', null=True, blank=True),
        ),
    ]
