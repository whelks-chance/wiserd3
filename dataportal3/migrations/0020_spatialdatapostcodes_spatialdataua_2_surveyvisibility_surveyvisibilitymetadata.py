# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0019_auto_20151127_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpatialdataPostCodeS',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('label', models.CharField(max_length=254, null=True, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'pcode_s',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SpatialdataUA_2',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=254, null=True, blank=True)),
                ('name', models.CharField(max_length=254, null=True, blank=True)),
                ('altname', models.CharField(max_length=254, null=True, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'ua_2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SurveyVisibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visibility_id', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyVisibilityMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primary_contact', models.ForeignKey(to='dataportal3.UserProfile')),
                ('survey', models.ForeignKey(to='dataportal3.Survey')),
                ('survey_visibility', models.ForeignKey(to='dataportal3.SurveyVisibility')),
            ],
        ),
    ]
