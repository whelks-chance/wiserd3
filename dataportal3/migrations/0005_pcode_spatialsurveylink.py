# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0004_userpreferences'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pcode',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'pcode',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialSurveyLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom_table_name', models.TextField(null=True, blank=True)),
                ('regional_data', django_hstore.fields.DictionaryField(null=True, blank=True)),
                ('data_name', models.TextField(null=True, blank=True)),
                ('data_description', models.TextField(null=True, blank=True)),
                ('survey', models.ForeignKey(blank=True, to='dataportal3.Survey', null=True)),
            ],
            options={
                'db_table': 'spatial_survey_link',
            },
        ),
    ]
