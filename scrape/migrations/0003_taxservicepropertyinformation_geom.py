# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-24 15:06
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0002_auto_20170223_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxservicepropertyinformation',
            name='geom',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
