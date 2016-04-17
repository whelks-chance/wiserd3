# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0030_auto_20160329_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpatialSurveyLinkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.TextField(null=True, blank=True)),
                ('geom_table_name', models.TextField(null=True, blank=True)),
                ('survey', models.ForeignKey(blank=True, to='dataportal3.Survey', null=True)),
            ],
            options={
                'db_table': 'spatial_survey_link_group',
            },
        ),
        migrations.AddField(
            model_name='spatialsurveylink',
            name='link_groups',
            field=models.ManyToManyField(to='dataportal3.SpatialSurveyLinkGroup'),
        ),
    ]
