# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0003_auto_20151030_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('links_new_tab', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='dataportal3.UserProfile')),
            ],
            options={
                'db_table': 'user_preferences',
            },
        ),
    ]
