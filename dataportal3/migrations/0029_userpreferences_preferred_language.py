# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0028_auto_20160314_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='preferred_language',
            field=models.ForeignKey(blank=True, to='dataportal3.DublincoreLanguage', null=True),
        ),
    ]
