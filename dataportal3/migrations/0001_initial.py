# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields
import django.contrib.gis.db.models.fields
from django.conf import settings
import dataportal3.models
import django_hstore.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aberystwyth_Locality_Dissolved',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('id', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'Aberystwyth_Locality_Dissolved',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bangor_Locality_Dissolved',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('area_name', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'Bangor_Locality_Dissolved',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Heads_of_the_Valleys',
            fields=[
                ('gid', models.IntegerField(serialize=False, primary_key=True)),
                ('area_name', models.CharField(max_length=254, null=True, blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'Heads_of_the_Valleys',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DcInfo',
            fields=[
                ('identifier', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('creator', models.TextField(null=True, blank=True)),
                ('subject', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('publisher', models.CharField(max_length=255, null=True, blank=True)),
                ('contributor', models.CharField(max_length=255, null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('source', models.CharField(max_length=255, null=True, blank=True)),
                ('relation', models.CharField(max_length=255, null=True, blank=True)),
                ('coverage', models.TextField(null=True, blank=True)),
                ('rights', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dc_info',
            },
        ),
        migrations.CreateModel(
            name='DublincoreFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dcformatid', models.CharField(max_length=255)),
                ('dc_format_title', models.CharField(max_length=255, null=True, blank=True)),
                ('dc_format_description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dublincore_format',
            },
        ),
        migrations.CreateModel(
            name='DublincoreLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dclangid', models.CharField(max_length=255)),
                ('dc_language_title', models.CharField(max_length=255, null=True, blank=True)),
                ('dc_language_description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dublincore_language',
            },
        ),
        migrations.CreateModel(
            name='DublincoreType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dctypeid', models.CharField(max_length=50)),
                ('dc_type_title', models.CharField(max_length=255, null=True, blank=True)),
                ('dc_type_description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'dublincore_type',
            },
        ),
        migrations.CreateModel(
            name='FeatureCollectionStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('topojson_file', models.FileField(null=True, upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('feature_attributes', django_hstore.fields.DictionaryField(null=True, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
                ('feature_collection', models.ForeignKey(to='dataportal3.FeatureCollectionStore')),
            ],
        ),
        migrations.CreateModel(
            name='QType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('q_typeid', models.CharField(unique=True, max_length=20)),
                ('q_type_text', models.CharField(max_length=50, null=True, blank=True)),
                ('q_typedesc', models.CharField(max_length=50, null=True, db_column='q_typeDesc', blank=True)),
            ],
            options={
                'db_table': 'q_type',
            },
        ),
        migrations.CreateModel(
            name='QualCalais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(null=True, blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lon', models.FloatField(null=True, blank=True)),
                ('geo_point', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
                ('tagName', models.TextField(null=True, blank=True)),
                ('gazetteer', models.TextField(null=True, blank=True)),
                ('count', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QualDcInfo',
            fields=[
                ('identifier', models.TextField(serialize=False, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('creator', models.TextField(null=True, blank=True)),
                ('subject', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('publisher', models.TextField(null=True, blank=True)),
                ('contributor', models.TextField(null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('format', models.TextField(null=True, blank=True)),
                ('source', models.TextField(null=True, blank=True)),
                ('language', models.CharField(max_length=50, null=True, blank=True)),
                ('relation', models.TextField(null=True, blank=True)),
                ('coverage', django_hstore.fields.DictionaryField(null=True, blank=True)),
                ('rights', models.TextField(null=True, blank=True)),
                ('user_id', models.CharField(max_length=25, null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('words', django_hstore.fields.DictionaryField(null=True, blank=True)),
                ('calais', models.TextField(null=True, blank=True)),
                ('vern_geog', models.TextField(null=True, db_column='vern_Geog', blank=True)),
                ('the_geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
                ('tier', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'qual_dc_info',
            },
        ),
        migrations.CreateModel(
            name='QualStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('page_counts', django_hstore.fields.DictionaryField(null=True, blank=True)),
            ],
            options={
                'db_table': 'qual_transcript_stats',
            },
        ),
        migrations.CreateModel(
            name='QualTranscriptData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.TextField(unique=True, null=True, blank=True)),
                ('rawtext', models.TextField()),
                ('stats', models.TextField()),
                ('pages', models.IntegerField()),
                ('errors', models.TextField(null=True, blank=True)),
                ('calais', models.ForeignKey(to='dataportal3.QualCalais', null=True)),
                ('dc_info', models.ForeignKey(to='dataportal3.QualDcInfo', null=True)),
            ],
            options={
                'db_table': 'qual_transcript_data',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('qid', models.CharField(max_length=300, serialize=False, primary_key=True)),
                ('literal_question_text', models.TextField(null=True, blank=True)),
                ('questionnumber', models.CharField(max_length=300, null=True, blank=True)),
                ('thematic_groups', models.TextField(null=True, blank=True)),
                ('thematic_tags', models.TextField(null=True, blank=True)),
                ('link_from_id', models.CharField(max_length=50, null=True, blank=True)),
                ('subof_id', models.CharField(max_length=50, null=True, blank=True)),
                ('variableid', models.CharField(max_length=50, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('qtext_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('link_from_question', models.ForeignKey(related_name='link_from', blank=True, to='dataportal3.Question', null=True)),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('responseid', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('responsetext', models.TextField(null=True, blank=True)),
                ('routetype', models.CharField(max_length=255, null=True, blank=True)),
                ('table_ids', models.TextField(null=True, blank=True)),
                ('computed_var', models.TextField(null=True, blank=True)),
                ('checks', models.TextField(null=True, blank=True)),
                ('route_notes', models.TextField(null=True, blank=True)),
                ('user_id', models.CharField(max_length=255, null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'response',
            },
        ),
        migrations.CreateModel(
            name='ResponseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('responseid', models.CharField(max_length=255, null=True, blank=True)),
                ('response_name', models.CharField(max_length=255, null=True, blank=True)),
                ('response_description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'response_type',
            },
        ),
        migrations.CreateModel(
            name='RouteType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('routetypeid', models.CharField(max_length=50)),
                ('routetype_description', models.TextField(null=True, blank=True)),
                ('routetype', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'route_type',
            },
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.TextField(null=True, blank=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('type', models.TextField(null=True, blank=True)),
                ('image_png', models.TextField(null=True, blank=True)),
                ('uid', models.UUIDField(default=uuid.uuid4)),
                ('readable_name', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'user_search',
            },
        ),
        migrations.CreateModel(
            name='ShapeFileUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('shapefile', models.FileField(max_length=1024, upload_to=dataportal3.models.get_upload_directory)),
                ('description', models.TextField(null=True, blank=True)),
                ('country', models.TextField(null=True, blank=True)),
                ('uuid', models.TextField(null=True, blank=True)),
                ('submit_time', models.DateTimeField(auto_now=True)),
                ('progress', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpatialLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=300)),
                ('level', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'spatial_level',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surveyid', models.CharField(unique=True, max_length=255)),
                ('identifier', models.CharField(max_length=50, null=True, blank=True)),
                ('survey_title', models.TextField(null=True, blank=True)),
                ('datacollector', models.CharField(max_length=50, null=True, blank=True)),
                ('collectionstartdate', models.DateField(null=True, blank=True)),
                ('collectionenddate', models.DateField(null=True, blank=True)),
                ('moc_description', models.TextField(null=True, blank=True)),
                ('samp_procedure', models.TextField(null=True, blank=True)),
                ('collectionsituation', models.TextField(null=True, blank=True)),
                ('surveyfrequency', models.CharField(max_length=255, null=True, blank=True)),
                ('surveystartdate', models.DateField(null=True, blank=True)),
                ('surveyenddate', models.DateField(null=True, blank=True)),
                ('des_weighting', models.TextField(null=True, blank=True)),
                ('samplesize', models.CharField(max_length=100, null=True, blank=True)),
                ('responserate', models.CharField(max_length=20, null=True, blank=True)),
                ('descriptionofsamplingerror', models.TextField(null=True, blank=True)),
                ('dataproduct', models.CharField(max_length=255, null=True, blank=True)),
                ('dataproductid', models.CharField(max_length=25, null=True, blank=True)),
                ('location', models.TextField(null=True, blank=True)),
                ('link', models.TextField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('user_id', models.CharField(max_length=25, null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('long', models.TextField(null=True, blank=True)),
                ('short_title', models.TextField(null=True, blank=True)),
                ('spatialdata', models.NullBooleanField()),
            ],
            options={
                'db_table': 'survey',
            },
        ),
        migrations.CreateModel(
            name='SurveyFrequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('svyfreqid', models.CharField(unique=True, max_length=255)),
                ('svy_frequency_title', models.CharField(max_length=255, null=True, blank=True)),
                ('svy_frequency_description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'survey_frequency',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionsLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surveyid', models.CharField(max_length=50, null=True, blank=True)),
                ('qid', models.CharField(max_length=50, null=True, blank=True)),
                ('pkid', models.IntegerField(verbose_name='pk')),
            ],
            options={
                'db_table': 'survey_questions_link',
            },
        ),
        migrations.CreateModel(
            name='SurveySpatialLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surveyid', models.CharField(max_length=255)),
                ('spatial_id', models.CharField(max_length=300)),
                ('long_start', models.DateField(null=True, blank=True)),
                ('long_finish', models.DateField(null=True, blank=True)),
                ('user_id', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('admin_units', models.TextField(null=True, blank=True)),
                ('custom_shape', models.TextField(null=True, blank=True)),
                ('admin_areas', models.TextField(null=True, blank=True)),
                ('custom_shape_id', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'survey_spatial_link',
            },
        ),
        migrations.CreateModel(
            name='ThematicGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tgroupid', models.CharField(max_length=20)),
                ('grouptitle', models.CharField(max_length=75)),
                ('groupdescription', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'thematic_group',
            },
        ),
        migrations.CreateModel(
            name='ThematicTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagid', models.CharField(max_length=20)),
                ('tag_text', models.CharField(max_length=255)),
                ('tag_description', models.CharField(max_length=255, null=True, blank=True)),
                ('thematic_group', models.ForeignKey(blank=True, to='dataportal3.ThematicGroup', null=True)),
            ],
            options={
                'db_table': 'thematic_tag',
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.CharField(max_length=25)),
                ('user_name', models.CharField(max_length=50, null=True, blank=True)),
                ('user_email', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'user_detail',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default='regular', max_length=30)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'user_role',
            },
        ),
        migrations.AddField(
            model_name='survey',
            name='data_entry',
            field=models.ForeignKey(blank=True, to='dataportal3.UserDetail', null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='dublin_core',
            field=models.ForeignKey(blank=True, to='dataportal3.DcInfo', null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='frequency',
            field=models.ForeignKey(blank=True, to='dataportal3.SurveyFrequency', null=True),
        ),
        migrations.AddField(
            model_name='shapefileupload',
            name='user',
            field=models.ForeignKey(to='dataportal3.UserProfile'),
        ),
        migrations.AddField(
            model_name='search',
            name='user',
            field=models.ForeignKey(to='dataportal3.UserProfile'),
        ),
        migrations.AddField(
            model_name='response',
            name='response_type',
            field=models.ForeignKey(blank=True, to='dataportal3.ResponseType', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='response',
            field=models.ForeignKey(blank=True, to='dataportal3.Response', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='subof_question',
            field=models.ForeignKey(related_name='subof', blank=True, to='dataportal3.Question', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(to='dataportal3.Survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='thematic_groups_set',
            field=models.ManyToManyField(to='dataportal3.ThematicGroup'),
        ),
        migrations.AddField(
            model_name='question',
            name='thematic_tags_set',
            field=models.ManyToManyField(to='dataportal3.ThematicTag'),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(blank=True, to='dataportal3.QType', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='user_id',
            field=models.ForeignKey(blank=True, to='dataportal3.UserDetail', null=True),
        ),
        migrations.AddField(
            model_name='qualstats',
            name='transcript_data',
            field=models.ForeignKey(to='dataportal3.QualTranscriptData'),
        ),
        migrations.AddField(
            model_name='qualdcinfo',
            name='thematic_groups_set',
            field=models.ManyToManyField(to='dataportal3.ThematicGroup'),
        ),
        migrations.AddField(
            model_name='qualcalais',
            name='qual_dc',
            field=models.ForeignKey(to='dataportal3.QualDcInfo', null=True),
        ),
        migrations.AddField(
            model_name='featurecollectionstore',
            name='shapefile_upload',
            field=models.ForeignKey(blank=True, to='dataportal3.ShapeFileUpload', null=True),
        ),
        migrations.AddField(
            model_name='featurecollectionstore',
            name='survey',
            field=models.ForeignKey(blank=True, to='dataportal3.Survey', null=True),
        ),
        migrations.AddField(
            model_name='dcinfo',
            name='format',
            field=models.ForeignKey(blank=True, to='dataportal3.DublincoreFormat', null=True),
        ),
        migrations.AddField(
            model_name='dcinfo',
            name='language',
            field=models.ForeignKey(blank=True, to='dataportal3.DublincoreLanguage', null=True),
        ),
        migrations.AddField(
            model_name='dcinfo',
            name='type',
            field=models.ForeignKey(blank=True, to='dataportal3.DublincoreType', null=True),
        ),
        migrations.AddField(
            model_name='dcinfo',
            name='user_id',
            field=models.ForeignKey(blank=True, to='dataportal3.UserDetail', null=True),
        ),
    ]
