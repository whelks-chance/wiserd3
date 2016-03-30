# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0008_auto_20151107_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='speciality',
            new_name='specialty',
        ),
    ]
