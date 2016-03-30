# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0011_userprofile_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='NomisSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('uuid', models.TextField(null=True, blank=True)),
                ('dataset_id', models.TextField(null=True, blank=True)),
                ('geography_id', models.TextField(null=True, blank=True)),
                ('search_attributes', django_hstore.fields.DictionaryField(null=True, blank=True)),
                ('user', models.ForeignKey(to='dataportal3.UserProfile')),
            ],
        ),
        migrations.AlterModelOptions(
            name='aberystwyth_locality_dissolved',
            options={},
        ),
        migrations.AlterModelOptions(
            name='bangor_locality_dissolved',
            options={},
        ),
        migrations.AlterModelOptions(
            name='heads_of_the_valleys',
            options={},
        ),
    ]
