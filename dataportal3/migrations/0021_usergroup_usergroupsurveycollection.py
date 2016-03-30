# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0020_spatialdatapostcodes_spatialdataua_2_surveyvisibility_surveyvisibilitymetadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('user_group_members', models.ManyToManyField(to='dataportal3.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroupSurveyCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('survey_visibility_metadata', models.ManyToManyField(to='dataportal3.SurveyVisibilityMetadata')),
                ('user_group', models.ForeignKey(to='dataportal3.UserGroup')),
            ],
        ),
    ]
