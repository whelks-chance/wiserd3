# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0012_auto_20151116_1534'),
    ]

    operations = [

        migrations.AddField(
            model_name='nomissearch',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 16, 15, 57, 26, 786328), auto_now=True),
            preserve_default=False,
        )

    ]
