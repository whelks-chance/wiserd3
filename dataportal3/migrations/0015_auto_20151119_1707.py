# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0014_auto_20151116_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomissearch',
            name='display_attributes',
            field=django_hstore.fields.DictionaryField(null=True, blank=True),
        ),
        migrations.AlterModelTable(
            name='aberystwyth_locality_dissolved',
            table='aberystwyth_locality_dissolved',
        ),
        migrations.AlterModelTable(
            name='bangor_locality_dissolved',
            table='bangor_locality_dissolved',
        ),
        migrations.AlterModelTable(
            name='heads_of_the_valleys',
            table='heads_of_the_valleys',
        ),
    ]
