# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0005_pcode_spatialsurveylink'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpatialdataAEFA',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_aefa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataFire',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_fire',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataLSOA',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_lsoa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataMSOA',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_msoa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataParl',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_parl',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataPolice',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_police',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataPostCode',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_pcode',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataUA',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'spatialdata_ua',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='boundary_name',
            field=models.TextField(null=True, blank=True),
        ),
    ]
