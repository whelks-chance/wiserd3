from __future__ import unicode_literals

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
import uuid
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from wiserd3.settings import MEDIA_ROOT
from django_hstore import hstore


class UserRole(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'user_role'

    def __unicode__(self):
        return str(self.id) + ':' + self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    role = models.CharField(max_length=30, default='regular')
    # sign_up_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'

    def __unicode__(self):
        return str(self.id) + ':' + self.user.username


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


class DcInfo(models.Model):
    identifier = models.CharField(primary_key=True, max_length=50)
    title = models.TextField(blank=True, null=True)
    creator = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    contributor = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    type = models.ForeignKey('DublincoreType', blank=True, null=True)
    format = models.ForeignKey('DublincoreFormat', blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    language = models.ForeignKey('DublincoreLanguage', blank=True, null=True)
    relation = models.CharField(max_length=255, blank=True, null=True)
    coverage = models.TextField(blank=True, null=True)
    rights = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey('UserDetail', blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'dc_info'

    def __unicode__(self):
        return str(self.identifier) + ':' + self.title


class DublincoreFormat(models.Model):
    dcformatid = models.CharField(unique=True, max_length=255)
    dc_format_title = models.CharField(max_length=255, blank=True, null=True)
    dc_format_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_format'

    def __unicode__(self):
        return str(self.dcformatid) + ':' + self.dc_format_title


class DublincoreLanguage(models.Model):
    dclangid = models.CharField(unique=True, max_length=255)
    dc_language_title = models.CharField(max_length=255, blank=True, null=True)
    dc_language_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_language'

    def __unicode__(self):
        return str(self.dclangid) + ':' + self.dc_language_title


class DublincoreType(models.Model):
    dctypeid = models.CharField(unique=True, max_length=50)
    dc_type_title = models.CharField(max_length=255, blank=True, null=True)
    dc_type_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_type'

    def __unicode__(self):
        return str(self.dctypeid) + ':' + self.dc_type_title


class ThematicGroup(models.Model):
    tgroupid = models.CharField(max_length=20)
    grouptitle = models.CharField(max_length=75)
    groupdescription = models.CharField(max_length=250)

    class Meta:
        db_table = 'thematic_group'

    def __unicode__(self):
        return str(self.tgroupid) + ':' + self.grouptitle


class ThematicTag(models.Model):
    tagid = models.CharField(max_length=20)
    thematic_group = models.ForeignKey('ThematicGroup', blank=True, null=True)
    tag_text = models.CharField(max_length=255)
    tag_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'thematic_tag'

    def __unicode__(self):
        return str(self.tagid) + ':' + self.tag_text


class QType(models.Model):
    q_typeid = models.CharField(unique=True, max_length=20)
    q_type_text = models.CharField(max_length=50, blank=True, null=True)
    q_typedesc = models.CharField(db_column='q_typeDesc', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'q_type'

    def __unicode__(self):
        return str(self.q_typeid) + ':' + self.q_type_text


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
        return str(self.qid) + ':' + self.literal_question_text


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
        return self.responseid + ':' + self.responsetext


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

    surveyid = models.CharField(unique=True, max_length=255)
    identifier = models.CharField(max_length=50, blank=True, null=True)
    survey_title = models.TextField(blank=True, null=True)
    datacollector = models.CharField(max_length=50, blank=True, null=True)
    collectionstartdate = models.DateField(blank=True, null=True)
    collectionenddate = models.DateField(blank=True, null=True)
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
    dataproduct = models.CharField(max_length=255, blank=True, null=True)
    dataproductid = models.CharField(max_length=25, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    long = models.TextField(blank=True, null=True)
    short_title = models.TextField(blank=True, null=True)
    spatialdata = models.NullBooleanField()

    class Meta:
        db_table = 'survey'

    def __unicode__(self):
        return str(self.surveyid) + ':' + self.survey_title


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
        return str(self.surveyid) + ':' + self.qid + ':' + self.pkid

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
    topojson_file = models.FileField(blank=True, null=True)

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


class Aberystwyth_Locality_Dissolved(models.Model):
    gid = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=254, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Aberystwyth_Locality_Dissolved'

    def __unicode__(self):
        return str(self.gid) + ':Aberystwyth_Locality_Dissolved'

class Bangor_Locality_Dissolved(models.Model):
    gid = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=254, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bangor_Locality_Dissolved'

    def __unicode__(self):
        return str(self.gid) + ':Bangor_Locality_Dissolved'


class Heads_of_the_Valleys(models.Model):
    gid = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=254, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Heads_of_the_Valleys'

    def __unicode__(self):
        return str(self.gid) + ':Heads_of_the_Valleys'


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