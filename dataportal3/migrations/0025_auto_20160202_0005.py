# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0024_auto_20160201_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='nomissearch',
            name='search_type',
            field=models.ForeignKey(blank=True, to='dataportal3.SearchType', null=True),
        ),
    ]
