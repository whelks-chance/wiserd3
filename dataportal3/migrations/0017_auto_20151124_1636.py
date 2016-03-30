# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0016_auto_20151121_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dcinfo',
            name='identifier',
            field=models.CharField(max_length=255, serialize=False, primary_key=True),
        ),
    ]
