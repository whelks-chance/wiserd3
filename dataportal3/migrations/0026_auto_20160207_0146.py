# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0025_auto_20160202_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomissearch',
            name='display_fields',
            field=django_hstore.fields.DictionaryField(null=True, blank=True),
        ),
    ]
