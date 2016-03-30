# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0029_userpreferences_preferred_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_language_title', models.CharField(max_length=255)),
                ('user_language_description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'user_language',
            },
        ),
        migrations.AlterField(
            model_name='userpreferences',
            name='preferred_language',
            field=models.ForeignKey(blank=True, to='dataportal3.UserLanguage', null=True),
        ),
    ]
