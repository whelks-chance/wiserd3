# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0013_auto_20151116_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aberystwyth_locality_dissolved',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='bangor_locality_dissolved',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='heads_of_the_valleys',
            options={'managed': False},
        ),
        migrations.AlterField(
            model_name='nomissearch',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
