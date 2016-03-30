# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0023_shapefileupload_topojson_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpatialdataNawer',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=254, null=True, blank=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('altname', models.CharField(max_length=254, null=True, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'nawer',
                'managed': False,
            },
        ),
        # migrations.RemoveField(
        #     model_name='shapefileupload',
        #     name='topojson_file',
        # ),
        migrations.AddField(
            model_name='nomissearch',
            name='search_type',
            field=models.TextField(null=True, blank=True),
        ),
    ]
