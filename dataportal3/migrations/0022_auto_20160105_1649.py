# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataportal3', '0021_usergroup_usergroupsurveycollection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroupsurveycollection',
            name='survey_visibility_metadata',
        ),
        migrations.AddField(
            model_name='surveyvisibilitymetadata',
            name='user_group_survey_collection',
            field=models.ForeignKey(to='dataportal3.UserGroupSurveyCollection', null=True),
        ),
    ]
