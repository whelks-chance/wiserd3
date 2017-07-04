from __future__ import unicode_literals
import string
from unicodedata import decimal

from django.utils import timezone
from django.utils.crypto import random
from django.utils.datetime_safe import time
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
import uuid
from django.contrib.gis.db import models
from django.contrib.auth.models import User
import math
from wiserd3.settings import MEDIA_ROOT
from django_hstore import hstore

from django.contrib.postgres.fields.jsonb import JSONField


def uniqid(prefix='', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0,10,1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid


class UserRole(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'user_role'

    def __unicode__(self):
        return str(self.id) + ':' + self.name


class UserLanguage(models.Model):
    user_language_title = models.CharField(max_length=255)
    user_language_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_language'

    def __unicode__(self):
        return str(self.id) + ':' + self.user_language_title


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    role = models.CharField(max_length=30, default='regular')
    # sign_up_timestamp = models.DateTimeField(auto_now=True)

    institution = models.TextField(blank=True, null=True)
    specialty = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    init_user = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_profile'

    def __unicode__(self):
        return str(self.id) + ':' + self.user.username


class UserPreferences(models.Model):
    user = models.ForeignKey(UserProfile)
    links_new_tab = models.BooleanField(default=False)
    topojson_high = models.BooleanField(default=False)
    preferred_language = models.ForeignKey('UserLanguage', blank=True, null=True)

    class Meta:
        db_table = 'user_preferences'

    def __unicode__(self):
        return str(self.id) + ':' + self.user.user.username


class UserTracking(models.Model):
    user = models.ForeignKey(UserProfile)
    datetime = models.DateTimeField(auto_now=True)
    ip = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.id) + ' : ' + self.user.user.username + ' : ' + self.url + ' : ' + str(self.datetime)


class Search(models.Model):
    user = models.ForeignKey(UserProfile)
    query = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now=True)
    type = models.TextField(blank=True, null=True)
    image_png = models.TextField(blank=True, null=True)
    uid = models.UUIDField(default=uuid.uuid4)
    readable_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_search'

    def __unicode__(self):
        return str(self.id) + ':' + self.user.user.username + ':' + self.query + ':' + str(self.datetime)


class DcCreator(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class DcPublisher(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class DcContributor(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '{}'.format(self.name)


class DcGeography(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    higher_geographies = models.ForeignKey('DcGeography', blank=True, null=True)
    ons_gss_code = models.CharField(max_length=9, blank=True, null=True)

    def __unicode__(self):
        return '{} : {}'.format(self.name, self.ons_gss_code)


class DcInfo(models.Model):
    identifier = models.CharField(primary_key=True, max_length=255)
    title = models.TextField(null=True)

    # creator_old = models.TextField(blank=True, null=True)
    # subject_old = models.TextField(blank=True, null=True)
    # publisher_old = models.CharField(max_length=255, blank=True, null=True)
    # contributor_old = models.CharField(max_length=255, blank=True, null=True)
    # relation_old = models.CharField(max_length=255, blank=True, null=True)
    # coverage_old = models.TextField(blank=True, null=True)
    # date = models.DateField(blank=True, null=True)

    subjects = models.ManyToManyField('ThematicTag')
    creators = models.ManyToManyField('DcCreator')
    publishers = models.ManyToManyField('DcPublisher')
    contributors = models.ManyToManyField('DcContributor', blank=True)

    description = models.TextField(null=True)
    type = models.ForeignKey('DublincoreType', null=True)
    format = models.ForeignKey('DublincoreFormat', null=True)

    source_url = models.TextField(blank=True, null=True)
    source_doi = models.TextField(blank=True, null=True)
    language = models.ForeignKey('DublincoreLanguage', null=True)

    relation_same_collection = models.ManyToManyField(
        'DcInfo', related_name='dc_relation_same_collection', blank=True)
    relation_different_collection = models.ManyToManyField(
        'DcInfo', related_name='dc_relation_different_collection', blank=True)

    coverage_spatial = models.ManyToManyField('DcGeography', blank=True)

    coverage_temporal_start = models.DateTimeField(null=True)
    coverage_temporal_end = models.DateTimeField(null=True)

    rights = models.TextField(null=True)
    user_id = models.ForeignKey('UserDetail', null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'dc_info'

    def __unicode__(self):
        return '{} : {}'.format(self.identifier, self.title)


class DublincoreFormat(models.Model):
    dcformatid = models.CharField(unique=True, max_length=255)
    dc_format_title = models.CharField(max_length=255, blank=True, null=True)
    dc_format_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_format'

    def __unicode__(self):
        return '{} : {}'.format(self.dcformatid, self.dc_format_title)


class DublincoreLanguage(models.Model):
    dclangid = models.CharField(unique=True, max_length=255)
    dc_language_title = models.CharField(max_length=255, blank=True, null=True)
    dc_language_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_language'

    def __unicode__(self):
        return '{} : {}'.format(self.dclangid, self.dc_language_title)


class DublincoreType(models.Model):
    dctypeid = models.CharField(unique=True, max_length=50)
    dc_type_title = models.CharField(max_length=255, blank=True, null=True)
    dc_type_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_type'

    def __unicode__(self):
        return '{} : {}'.format(self.dctypeid, self.dc_type_title)


class ThematicGroup(models.Model):
    tgroupid = models.CharField(max_length=20)
    grouptitle = models.CharField(max_length=75)
    groupdescription = models.CharField(max_length=250)

    class Meta:
        db_table = 'thematic_group'

    def __unicode__(self):
        return '{} : {}'.format(self.tgroupid, self.grouptitle)


class ThematicTag(models.Model):
    tagid = models.CharField(max_length=20)
    thematic_group = models.ForeignKey('ThematicGroup', blank=True, null=True)
    tag_text = models.CharField(max_length=255)
    tag_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'thematic_tag'

    def __unicode__(self):
        return '{} : {}'.format(self.tagid, self.tag_text)


class QType(models.Model):
    q_typeid = models.CharField(unique=True, max_length=20)
    q_type_text = models.CharField(max_length=50, blank=True, null=True)
    q_typedesc = models.CharField(db_column='q_typeDesc', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'q_type'

    def __unicode__(self):
        return '{} : {}'.format(self.q_typeid, self.q_type_text)


class Question(models.Model):
    survey = models.ForeignKey('Survey')
    thematic_groups_set = models.ManyToManyField('ThematicGroup')
    thematic_tags_set = models.ManyToManyField('ThematicTag')

    link_from_question = models.ForeignKey('Question', blank=True, null=True, related_name='link_from')
    subof_question = models.ForeignKey('Question', blank=True, null=True, related_name='subof')

    response = models.ForeignKey('Response', blank=True, null=True)

    qid = models.CharField(primary_key=True, max_length=300)
    literal_question_text = models.TextField(blank=True, null=True)
    questionnumber = models.CharField(max_length=300, blank=True, null=True)
    thematic_groups = models.TextField(blank=True, null=True)
    thematic_tags = models.TextField(blank=True, null=True)

    link_from_id = models.CharField(max_length=50, blank=True, null=True)
    subof_id = models.CharField(max_length=50, blank=True, null=True)

    # type = models.CharField(max_length=50, blank=True, null=True)
    type = models.ForeignKey('QType', blank=True, null=True)

    variableid = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey('UserDetail', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    # qtext_index = models.TextField(blank=True, null=True)  # This field type is a guess.

    qtext_index = VectorField()

    objects = SearchManager(
        fields = ('literal_question_text', 'notes'),
        config = 'pg_catalog.english', # this is default
        search_field = 'qtext_index', # this is default
        auto_update_search_field = True
    )

    class Meta:
        db_table = 'question'

    def __unicode__(self):
        return '{} : {}'.format(self.qid, self.literal_question_text)

    @staticmethod
    def autocomplete_search_fields():
        return ("qid__iexact", "literal_question_text__icontains", "questionnumber__icontains")


class ResponseType(models.Model):
    # "responseid", "response_name", "response_description"
    responseid = models.CharField(max_length=255, blank=True, null=True)
    response_name = models.CharField(max_length=255, blank=True, null=True)
    response_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'response_type'

    def __unicode__(self):
        return str(self.responseid) + ':' + self.response_name


class Response(models.Model):
    # "responseid", "responsetext", "response_type", "routetype", "table_ids",
    # "computed_var", "checks", "route_notes", "user_id", "created", "updated"
    responseid = models.CharField(primary_key=True, max_length=100)
    responsetext = models.TextField(blank=True, null=True)
    # response_type = models.CharField(max_length=255)

    response_type = models.ForeignKey('ResponseType', blank=True, null=True)
    routetype = models.CharField(max_length=255, blank=True, null=True)
    table_ids = models.TextField(blank=True, null=True)
    computed_var = models.TextField(blank=True, null=True)
    checks = models.TextField(blank=True, null=True)
    route_notes = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'response'

    def __unicode__(self):
        return '{} : {}'.format(self.responseid, self.responsetext)


class RouteType(models.Model):
    routetypeid = models.CharField(max_length=50)
    routetype_description = models.TextField(blank=True, null=True)
    routetype = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'route_type'

    def __unicode__(self):
        return str(self.routetypeid) + ':' + self.routetype


class SpatialLevel(models.Model):
    code = models.CharField(max_length=300)
    level = models.CharField(max_length=50)

    class Meta:
        db_table = 'spatial_level'

    def __unicode__(self):
        return str(self.code) + ':' + self.level


# class SpatialRefSys(models.Model):
#     srid = models.IntegerField(primary_key=True)
#     auth_name = models.CharField(max_length=256, blank=True, null=True)
#     auth_srid = models.IntegerField(blank=True, null=True)
#     srtext = models.CharField(max_length=2048, blank=True, null=True)
#     proj4text = models.CharField(max_length=2048, blank=True, null=True)
#
#     class Meta:
#         db_table = 'spatial_ref_sys'


class Survey(models.Model):
    dublin_core = models.ForeignKey('DcInfo', blank=True, null=True)
    frequency = models.ForeignKey('SurveyFrequency', blank=True, null=True)
    data_entry = models.ForeignKey('UserDetail', blank=True, null=True)

    keywords = models.TextField(blank=True, null=True)

    surveyid = models.CharField(unique=True, max_length=255, default=uniqid) # blank=True, null=True
    identifier = models.CharField(unique=True, max_length=255, blank=True, null=True)
    survey_title = models.TextField(blank=True, null=True)
    datacollector = models.CharField(max_length=50, blank=True, null=True)
    moc_description = models.TextField(blank=True, null=True)
    samp_procedure = models.TextField(blank=True, null=True)
    collectionsituation = models.TextField(blank=True, null=True)
    surveyfrequency = models.CharField(max_length=255, blank=True, null=True)
    surveystartdate = models.DateField(blank=True, null=True)
    surveyenddate = models.DateField(blank=True, null=True)
    des_weighting = models.TextField(blank=True, null=True)
    samplesize = models.CharField(max_length=100, blank=True, null=True)
    responserate = models.CharField(max_length=20, blank=True, null=True)
    descriptionofsamplingerror = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    long = models.TextField(blank=True, null=True)
    spatialdata = models.NullBooleanField()

    # hide
    collectionstartdate = models.DateField(blank=True, null=True)
    collectionenddate = models.DateField(blank=True, null=True)
    dataproduct = models.CharField(max_length=255, blank=True, null=True)
    dataproductid = models.CharField(max_length=25, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    short_title = models.TextField(blank=True, null=True)

    qtext_index = VectorField()

    objects = SearchManager(
        fields=('survey_title',
                'keywords',
                # 'dublin_core__description',
                'datacollector'),
        config='pg_catalog.english',  # this is default
        search_field='qtext_index',
        auto_update_search_field=True
    )

    class Meta:
        db_table = 'survey'

    def __unicode__(self):
        return '{} : {}'.format(self.surveyid, self.survey_title)


class SurveyFrequency(models.Model):
    svyfreqid = models.CharField(unique=True, max_length=255)
    svy_frequency_title = models.CharField(max_length=255, blank=True, null=True)
    svy_frequency_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'survey_frequency'

    def __unicode__(self):
        return str(self.svyfreqid) + ':' + self.svy_frequency_title


class SurveyQuestionsLink(models.Model):
    surveyid = models.CharField(max_length=50, blank=True, null=True)
    qid = models.CharField(max_length=50, blank=True, null=True)
    pkid = models.IntegerField(verbose_name='pk')

    class Meta:
        db_table = 'survey_questions_link'

    def __unicode__(self):
        return str(self.surveyid) + ':' + self.qid + ':' + str(self.pkid)


class SpatialSurveyLinkGroup(models.Model):
    group_name = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'spatial_survey_link_group'

    def __unicode__(self):
        return self.group_name


# TODO tidy these two up
class SpatialSurveyLink(models.Model):
    survey = models.ForeignKey('Survey', null=True, blank=True)
    geom_table_name = models.TextField(null=True, blank=True)
    boundary_name = models.TextField(null=True, blank=True)
    regional_data = hstore.DictionaryField(null=True, blank=True)
    data_name = models.TextField(null=True, blank=True)
    data_global_average = models.TextField(null=True, blank=True)
    data_prefix = models.TextField(null=True, blank=True)
    data_suffix = models.TextField(null=True, blank=True)
    data_type = models.TextField(null=True, blank=True)
    data_formatting = models.TextField(null=True, blank=True)
    data_description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField('UserProfile')

    category = models.TextField(blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    category_cy = models.TextField(blank=True, null=True)
    full_name_cy = models.TextField(blank=True, null=True)
    notes_cy = models.TextField(blank=True, null=True)

    link_groups = models.ManyToManyField('SpatialSurveyLinkGroup', null=True, blank=True)

    class Meta:
        db_table = 'spatial_survey_link'

    def __unicode__(self):
        return str(self.survey.identifier) + ':' + self.geom_table_name + ':' + self.data_name


# TODO tidy these two up
class SurveySpatialLink(models.Model):
    surveyid = models.CharField(max_length=255)
    spatial_id = models.CharField(max_length=300)
    long_start = models.DateField(blank=True, null=True)
    long_finish = models.DateField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    admin_units = models.TextField(blank=True, null=True)
    custom_shape = models.TextField(blank=True, null=True)
    admin_areas = models.TextField(blank=True, null=True)
    custom_shape_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'survey_spatial_link'

    def __unicode__(self):
        return str(self.surveyid) + ':' + self.spatial_id

# class GeometryColumns(models.Model):
#     f_table_catalog = models.CharField(max_length=256, blank=True, null=True)
#     f_table_schema = models.CharField(max_length=256, blank=True, null=True)
#     # f_table_name = models.CharField(max_length=256, blank=True, null=True)
#     f_table_name = models.CharField(primary_key=True, max_length=256)
#     f_geometry_column = models.CharField(max_length=256, blank=True, null=True)
#     coord_dimension = models.IntegerField()
#     srid = models.IntegerField()
#     type = models.CharField(max_length=30, blank=True, null=True)
#
#     class Meta:
#         db_table = 'geometry_columns'


class UserDetail(models.Model):
    user_id = models.CharField(max_length=25)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'user_detail'

    def __unicode__(self):
        return str(self.user_id) + ':' + self.user_name


def get_upload_directory(self, filename):
        return MEDIA_ROOT + str(self.uuid) + '/' + filename


class ShapeFileUpload(models.Model):
    user = models.ForeignKey(UserProfile)
    name = models.TextField(blank=True, null=True)
    shapefile = models.FileField(upload_to=get_upload_directory, max_length=1024)
    description = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    submit_time = models.DateTimeField(auto_now=True)
    progress = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.user.user.username) + ':' + str(self.name) + ':' + str(self.uuid)


class FeatureCollectionStore(models.Model):
    name = models.TextField(blank=True, null=True)
    shapefile_upload = models.ForeignKey(ShapeFileUpload, blank=True, null=True)
    survey = models.ForeignKey(Survey, blank=True, null=True)
    topojson_file = models.FileField(blank=True, null=True, max_length=512)

    def __unicode__(self):
        return str(self.name)


class FeatureStore(models.Model):
    name = models.TextField(blank=True, null=True)
    feature_collection = models.ForeignKey(FeatureCollectionStore)
    feature_attributes = hstore.DictionaryField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)

    objects = hstore.HStoreGeoManager()

    def __unicode__(self):
        return str(self.feature_collection.name) + ':' + str(self.name)


class SearchType(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.name) + ':' + self.description


class NomisSearch(models.Model):
    name = models.TextField(blank=True, null=True)
    uuid = models.TextField(blank=True, null=True)
    user = models.ForeignKey(UserProfile)
    dataset_id = models.TextField(blank=True, null=True)
    geography_id = models.TextField(blank=True, null=True)
    search_attributes = hstore.DictionaryField(blank=True, null=True)
    display_attributes = hstore.DictionaryField(blank=True, null=True)
    display_fields = hstore.DictionaryField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    search_type = models.ForeignKey(SearchType, blank=True, null=True)

    def __unicode__(self):
        # print self.name, self.geography_id, self.uuid
        return u'{}:{}:{}:{}'.format(
            self.name,
            self.uuid,
            self.geography_id,
            (self.search_type.name if self.search_type is not None else '-?-error-?-')
        )


class Aberystwyth_Locality_Dissolved(models.Model):
    gid = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        # db_table = 'Aberystwyth_Locality_Dissolved'
        db_table = 'aberystwyth_locality_dissolved'

    def __unicode__(self):
        return str(self.gid) + ':aberystwyth_locality_dissolved'

class Bangor_Locality_Dissolved(models.Model):
    gid = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bangor_locality_dissolved'

    def __unicode__(self):
        return str(self.gid) + ':bangor_locality_dissolved'


class Heads_of_the_Valleys(models.Model):
    gid = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'heads_of_the_valleys'

    def __unicode__(self):
        return str(self.gid) + ':heads_of_the_valleys'


class QualDcInfo(models.Model):
    identifier = models.TextField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    creator = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publisher = models.TextField(blank=True, null=True)
    contributor = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    format = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    relation = models.TextField(blank=True, null=True)

    ## coverage = models.TextField(blank=True, null=True)
    coverage = hstore.DictionaryField(blank=True, null=True)

    rights = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    ## words = models.TextField(blank=True, null=True)
    words = hstore.DictionaryField(blank=True, null=True)

    calais = models.TextField(blank=True, null=True)
    vern_geog = models.TextField(db_column='vern_Geog', blank=True, null=True)  # Field name made lowercase.

    ## the_geom = models.TextField()  # This field type is a guess.
    the_geom = models.GeometryField(blank=True, null=True)

    # thematic_group = models.TextField(blank=True, null=True)
    thematic_groups_set = models.ManyToManyField('ThematicGroup')

    tier = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'qual_dc_info'

    def __unicode__(self):
        return str(self.identifier) + ':' + self.title

class QualCalais(models.Model):
    value = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    geo_point = models.GeometryField(blank=True, null=True)
    tagName = models.TextField(blank=True, null=True)
    gazetteer = models.TextField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    qual_dc = models.ForeignKey('QualDcInfo', null=True)

    def __unicode__(self):
        return str(self.tagName) + ':' + self.value


class QualTranscriptData(models.Model):
    identifier = models.TextField(unique=True, blank=True, null=True)
    # calais = models.ForeignKey('QualCalais', null=True)
    dc_info = models.ForeignKey("QualDcInfo", null=True)
    rawtext = models.TextField()
    stats = models.TextField()
    pages = models.IntegerField()
    errors = models.TextField(blank=True, null=True)

    # Stop trying to add this back in
    # text_index = VectorField(db_index=False)
    #
    # objects = SearchManager(
    #     fields = ('rawtext'),
    #     config = 'pg_catalog.english',  # this is default
    #     search_field = 'text_index',  # this is default
    #     auto_update_search_field = True
    # )

    class Meta:
        db_table = 'qual_transcript_data'

    def __unicode__(self):
        return str(self.identifier) + ':' + str(self.pages) + ' pages'


class QualStats(models.Model):
    name = models.TextField(blank=True, null=True)
    page_counts = hstore.DictionaryField(blank=True, null=True)
    transcript_data = models.ForeignKey('QualTranscriptData')

    class Meta:
        db_table = 'qual_transcript_stats'

    def __unicode__(self):
        return str(self.id) + ':' + self.name


# Options like :
# allow full access to everyone
# allow metadata access (appears in searches) to everyone
# allow full access to users in groups X, Y and Z
# allow full access to users in groups X, Y and metadata access to users in group Z (complex)
# allow no access to anyone
class SurveyVisibility(models.Model):
    visibility_id = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.id) + ':' + self.visibility_id


class SurveyVisibilityMetadata(models.Model):
    survey = models.ForeignKey('Survey')
    survey_visibility = models.ForeignKey('SurveyVisibility')
    primary_contact = models.ForeignKey('UserProfile')
    user_group_survey_collection = models.ForeignKey('UserGroupSurveyCollection', null=True)

    def __unicode__(self):
        return str(self.id) + ':' + self.survey.identifier + ':' + self.survey_visibility.visibility_id


class UserGroup(models.Model):
    name = models.TextField(blank=True, null=True)
    user_group_members = models.ManyToManyField('UserProfile')

    def __unicode__(self):
        return str(self.id) + ':' + self.name


class UserGroupSurveyCollection(models.Model):
    name = models.TextField(blank=True, null=True)
    user_group = models.ForeignKey('UserGroup')
    # survey_visibility_metadata = models.ManyToManyField('SurveyVisibilityMetadata')

    def __unicode__(self):
        return str(self.id) + ':' + self.name + ':' + self.user_group.name

#
# spatial tables below
#
#
#

class SpatialdataAEFA(models.Model):
    gid = models.IntegerField(primary_key=True)
    # name = models.CharField(max_length=254, blank=True, null=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_aefa'


class SpatialdataPolice(models.Model):
    gid = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_police'


class SpatialdataPostCode(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_pcode'


class SpatialdataPostCodePoint(models.Model):
    gid = models.IntegerField(primary_key=True)
    postcode = models.CharField(max_length=254, blank=True, null=True)
    easting = models.IntegerField(blank=True, null=True)
    northing = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.postcode)

    class Meta:
        managed = False
        db_table = 'pcode_point'


class PostcodePointLSOAlinks(models.Model):
    postcode = models.CharField(max_length=254, blank=True, null=True)
    lsoa_name = models.CharField(max_length=254, blank=True, null=True)
    lsoa_code = models.CharField(max_length=254, blank=True, null=True)

    def __unicode__(self):
        return '{} :: {} :: {}'.format(str(self.postcode), str(self.lsoa_name), self.lsoa_code)

    class Meta:
        # managed = False
        db_table = 'postcode_point_lsoa_links'


class SchoolData(models.Model):
    # id = models.IntegerField(primary_key=True)
    lat = models.DecimalField(decimal_places=20, max_digits=30, blank=True, null=True)
    lea = models.IntegerField(blank=True, null=True)
    lng = models.DecimalField(decimal_places=20, max_digits=30, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    schoolCode = models.IntegerField(blank=True, null=True)
    schoolType = models.IntegerField(blank=True, null=True)
    statusNameEng = models.CharField(max_length=24, blank=True, null=True)
    statusNameWelsh = models.CharField(max_length=24, blank=True, null=True)

    LEANameEnglish = models.CharField(max_length=254, blank=True, null=True)
    LEANameWelsh = models.CharField(max_length=254, blank=True, null=True)
    schTypeEnglish = models.CharField(max_length=254, blank=True, null=True)
    schTypeWelsh = models.CharField(max_length=254, blank=True, null=True)
    schLanguageEnglish = models.CharField(max_length=254, blank=True, null=True)
    schLanguageWelsh = models.CharField(max_length=254, blank=True, null=True)
    genderMix = models.CharField(max_length=254, blank=True, null=True)
    commentsEng = models.TextField(blank=True, null=True)
    commentsCym = models.TextField(blank=True, null=True)
    schoolGroupingCodePrim = models.IntegerField(blank=True, null=True)
    addressLine1 = models.CharField(max_length=254, blank=True, null=True)
    addressLine2 = models.CharField(max_length=254, blank=True, null=True)
    addressLine3 = models.CharField(max_length=254, blank=True, null=True)
    addressLine4 = models.CharField(max_length=254, blank=True, null=True)
    postcode = models.CharField(max_length=254, blank=True, null=True)
    telephoneNo = models.CharField(max_length=254, blank=True, null=True)

    fsm_percent = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)

    school_dict = hstore.DictionaryField(blank=True, null=True)
    school_json = JSONField(blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.schoolCode) + ':' + str(self.name) + ':' + str(self.postcode)

    class Meta:
        managed = True
        db_table = 'schools'


class SpatialdataPostCodeS(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'pcode_s'


class SpatialdataParl(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_parl'


class SpatialdataMSOA(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_msoa'


class SpatialdataLSOA(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    # zonecode = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_lsoa'


class SpatialdataFire(models.Model):
    gid = models.IntegerField(primary_key=True)
    # name = models.CharField(max_length=254, blank=True, null=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_fire'


class SpatialdataUA(models.Model):
    gid = models.IntegerField(primary_key=True)
    # name = models.CharField(max_length=254, blank=True, null=True)
    label = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.label)

    class Meta:
        managed = False
        db_table = 'spatialdata_ua'


class SpatialdataUA_2(models.Model):
    gid = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    altname = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'ua_2'


class SpatialdataNawer(models.Model):
    gid = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    altname = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'nawer'


# This is for the reverted NAW regions, as SpatialdataNawer/nawer was incorrect for a while
class SpatialdataNAWregions(models.Model):
    gid = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    namewelsh = models.CharField(max_length=254, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_assemblyregions2'


class SpatialdataConstituency(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    code = models.CharField(max_length=9, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_constituency'


class SpatialdataNAWConstituency(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    code = models.CharField(max_length=9, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'spatialdata_assemblyconstituency2'



class SpatialdataUKUA(models.Model):
    gid = models.IntegerField(primary_key=True)
    ctyua15cd = models.CharField(max_length=80, blank=True, null=True)
    ctyua15nm = models.CharField(max_length=80, blank=True, null=True)
    ctyua15nmw = models.CharField(max_length=80, blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} :: {}'.format(self.ctyua15cd, self.ctyua15nm)

    class Meta:
        managed = False
        db_table = 'uk_ua'


class SpatialdataUKLAD(models.Model):
    gid = models.IntegerField(primary_key=True)
    lad13cd = models.CharField(max_length=9, blank=True, null=True)
    lad13cdo = models.CharField(max_length=4, blank=True, null=True)
    lad13nm = models.CharField(max_length=28, blank=True, null=True)
    lad13nmw = models.IntegerField(blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} :: {}'.format(self.lad13cd, self.lad13nm)

    class Meta:
        managed = False
        db_table = 'uk_lad'


class SpatialdataUKLADSCO(models.Model):
    gid = models.IntegerField(primary_key=True)
    lad13cd = models.CharField(max_length=9, blank=True, null=True)
    lad13cdo = models.CharField(max_length=4, blank=True, null=True)
    lad13nm = models.CharField(max_length=21, blank=True, null=True)
    lad13nmw = models.IntegerField(blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} :: {}'.format(self.lad13cd, self.lad13nm)

    class Meta:
        managed = False
        db_table = 'uk_lad_sco'


class SpatialdataParlConstNI(models.Model):
    gid = models.IntegerField(primary_key=True)
    fid = models.CharField(max_length=9, blank=True, null=True)
    pc_id = models.CharField(max_length=9, blank=True, null=True)
    pc_name = models.CharField(max_length=26, blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} :: {}'.format(self.pc_id, self.pc_name)

    class Meta:
        managed = False
        db_table = 'parl_const_ni'


class GE15(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    area_code = models.CharField(max_length=3, blank=True, null=True)
    descriptio = models.CharField(max_length=50, blank=True, null=True)
    file_name = models.CharField(max_length=50, blank=True, null=True)

    number = models.FloatField(blank=True, null=True)
    number0 = models.FloatField(blank=True, null=True)
    polygon_id = models.FloatField(blank=True, null=True)
    unit_id = models.FloatField(blank=True, null=True)

    code = models.CharField(max_length=9, blank=True, null=True)

    hocl_ge201 = models.CharField(max_length=254, blank=True, null=True, db_column="hocl-ge201")
    hocl_ge2_1 = models.CharField(max_length=254, blank=True, null=True, db_column="hocl-ge2_1")
    hocl_ge2_8 = models.CharField(max_length=254, blank=True, null=True, db_column="hocl-ge2_8")

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} :: {} :: {} :: {}'.format(self.hocl_ge2_1, self.code, self.hocl_ge2_1, self.hocl_ge2_8)

    class Meta:
        managed = False
        db_table = 'ge15'


class GE17(models.Model):
    gid = models.IntegerField(primary_key=True)
    constituen = models.CharField(max_length=60, blank=True, null=True)
    ons_id = models.CharField(max_length=3, blank=True, null=True)
    # descriptio = models.CharField(max_length=50, blank=True, null=True)
    # file_name = models.CharField(max_length=50, blank=True, null=True)
    #
    # number = models.FloatField(blank=True, null=True)
    # number0 = models.FloatField(blank=True, null=True)
    # polygon_id = models.FloatField(blank=True, null=True)
    # unit_id = models.FloatField(blank=True, null=True)
    #
    # code = models.CharField(max_length=9, blank=True, null=True)
    #
    first_part = models.CharField(max_length=254, blank=True, null=True, db_column="first_part")
    # hocl_ge2_1 = models.CharField(max_length=254, blank=True, null=True, db_column="hocl-ge2_1")
    # hocl_ge2_8 = models.CharField(max_length=254, blank=True, null=True, db_column="hocl-ge2_8")

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} :: {} :: {}'.format(self.constituen, self.ons_id, self.first_part)

    class Meta:
        managed = False
        db_table = 'uk_ge_17'


class GE17Cart(models.Model):
    gid = models.IntegerField(primary_key=True)
    constituen = models.CharField(max_length=60, blank=True, null=True)
    ons_id = models.CharField(max_length=3, blank=True, null=True)
    # descriptio = models.CharField(max_length=50, blank=True, null=True)
    # file_name = models.CharField(max_length=50, blank=True, null=True)
    #
    # number = models.FloatField(blank=True, null=True)
    # number0 = models.FloatField(blank=True, null=True)
    # polygon_id = models.FloatField(blank=True, null=True)
    # unit_id = models.FloatField(blank=True, null=True)
    #
    # code = models.CharField(max_length=9, blank=True, null=True)
    #
    first_part = models.CharField(max_length=254, blank=True, null=True, db_column="first_part")
    # hocl_ge2_1 = models.CharField(max_length=254, blank=True, null=True, db_column="hocl-ge2_1")
    # hocl_ge2_8 = models.CharField(max_length=254, blank=True, null=True, db_column="hocl-ge2_8")

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} :: {} :: {}'.format(self.constituen, self.ons_id, self.first_part)

    class Meta:
        managed = False
        db_table = 'uk_ge_17_cart'


class WelshRail(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=48, blank=True, null=True)
    type = models.CharField(max_length=16, blank=True, null=True)
    osm_id = models.BigIntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'welshrail'


class UKRailStation(models.Model):
    gid = models.IntegerField(primary_key=True)
    identifier = models.CharField(max_length=13, blank=True, null=True)
    code = models.CharField(max_length=16, blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'ukrailstation'


class PowerStation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    output = models.CharField(max_length=10, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'power_station'

    def __unicode__(self):
        return u'{} :: {}'.format(self.name, self.type)


class WelshLanguageABS(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=9, blank=True, null=True)
    data_lsoa = models.CharField(max_length=254, blank=True, null=True)
    data_welsh = models.IntegerField(max_length=10, blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'welsh_language_abs'


class Brexit(models.Model):
    region = models.CharField(max_length=25, blank=True, null=True)
    leave_total = models.IntegerField(max_length=10, blank=True, null=True)
    leave_percent = models.FloatField(max_length=10, blank=True, null=True)
    remain_total = models.IntegerField(max_length=10, blank=True, null=True)
    remain_percent = models.FloatField(max_length=10, blank=True, null=True)
    outcome = models.CharField(max_length=10, blank=True, null=True)
    outcome_int = models.IntegerField(max_length=10, blank=True, null=True)
    turnout_percent = models.FloatField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.name) + ':' + str(self.region) + ':' + str(self.outcome)


class MineTest(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    postcode = models.CharField(max_length=7, blank=True, null=True)
    coordinate = models.CharField(max_length=254, blank=True, null=True)
    x = models.FloatField(max_length=10, blank=True, null=True)
    y = models.FloatField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=254, blank=True, null=True)
    image = models.CharField(max_length=254, blank=True, null=True)
    image_righ = models.CharField(max_length=254, blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'minetest'

    def __unicode__(self):
        return "{} : {} : {}".format(self.name, self.x, self.y)


class WMHpoints(models.Model):
    community_town = models.CharField(max_length=250, blank=True, null=True)
    coords = models.TextField(blank=True, null=True)
    y = models.CharField(max_length=25, blank=True, null=True)
    x = models.CharField(max_length=25, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    postcode = models.CharField(max_length=25, blank=True, null=True)
    council_borough = models.TextField(blank=True, null=True)
    memory_of = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=25, blank=True, null=True)
    colliery = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    built = models.CharField(max_length=25, blank=True, null=True)
    artist_architect = models.TextField(blank=True, null=True)
    people = models.TextField(blank=True, null=True)
    img_1 = models.TextField(blank=True, null=True)
    img_2 = models.TextField(blank=True, null=True)
    img_3 = models.TextField(blank=True, null=True)
    img_4 = models.TextField(blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return "{} : {} : {}".format(self.name, self.community_town, self.colliery)


class ResponseTable(models.Model):
    feature_attributes = JSONField(blank=True, null=True)
    survey = models.ForeignKey('Survey', blank=True, null=True)
    link_from_question = models.ForeignKey('Question', blank=True, null=True)
    response = models.ForeignKey('Response', blank=True, null=True, unique=True)

    def __unicode__(self):
        return str(self.response) + ':' + str(len(self.feature_attributes))


class RemoteDataProvider(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.name) + ':' + str(self.description)


class RemoteDataset(models.Model):
    remote_data_provider = models.ForeignKey('RemoteDataProvider', blank=True, null=True)

    name = models.CharField(max_length=255)
    dataset_identifier = models.CharField(max_length=255, blank=True, null=True)

    description = models.CharField(max_length=255)
    api_url = models.TextField(blank=True, null=True)
    description_url = models.TextField(blank=True, null=True)
    dataset_attributes = hstore.DictionaryField(blank=True, null=True)

    def __unicode__(self):
        return str(self.name) + ':' + str(self.dataset_identifier) + ':' + str(self.remote_data_provider.name)


class MetaDataToRemoteMapping(models.Model):
    wiserd_question = models.ForeignKey('Question', blank=True, null=True)
    remote_dataset = models.ForeignKey('RemoteDataset', blank=True, null=True)

    def __unicode__(self):
        return '{}:{}:{}:{}'.format(
            self.wiserd_question.survey.identifier,
            self.wiserd_question.qid,
            self.remote_dataset.dataset_identifier,
            self.remote_dataset.name
        )

import dataportal3.signals.handlers
