# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0002_remove_qualtranscriptdata_calais'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dublincoreformat',
            name='dcformatid',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='dublincorelanguage',
            name='dclangid',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='dublincoretype',
            name='dctypeid',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
