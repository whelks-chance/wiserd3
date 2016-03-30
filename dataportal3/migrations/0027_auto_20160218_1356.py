# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0026_auto_20160207_0146'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpatialdataConstituency',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=60, null=True, blank=True)),
                ('code', models.CharField(max_length=9, null=True, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_constituency',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='shapefileupload',
            name='topojson_file',
        ),
    ]
