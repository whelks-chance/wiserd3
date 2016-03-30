# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0017_auto_20151124_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='identifier',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='surveyid',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
        ),
    ]
