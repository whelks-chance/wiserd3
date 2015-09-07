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


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    role = models.CharField(max_length=30, default='regular')

    class Meta:
        db_table = 'user_profile'


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


class DublincoreFormat(models.Model):
    dcformatid = models.CharField(max_length=255)
    dc_format_title = models.CharField(max_length=255, blank=True, null=True)
    dc_format_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_format'


class DublincoreLanguage(models.Model):
    dclangid = models.CharField(max_length=255)
    dc_language_title = models.CharField(max_length=255, blank=True, null=True)
    dc_language_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_language'


class DublincoreType(models.Model):
    dctypeid = models.CharField(max_length=50)
    dc_type_title = models.CharField(max_length=255, blank=True, null=True)
    dc_type_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dublincore_type'


class ThematicGroup(models.Model):
    tgroupid = models.CharField(max_length=20)
    grouptitle = models.CharField(max_length=75)
    groupdescription = models.CharField(max_length=250)

    class Meta:
        db_table = 'thematic_group'


class ThematicTag(models.Model):
    tagid = models.CharField(max_length=20)
    thematic_group = models.ForeignKey('ThematicGroup', blank=True, null=True)
    tag_text = models.CharField(max_length=255)
    tag_description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'thematic_tag'


class QType(models.Model):
    q_typeid = models.CharField(unique=True, max_length=20)
    q_type_text = models.CharField(max_length=50, blank=True, null=True)
    q_typedesc = models.CharField(db_column='q_typeDesc', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'q_type'


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


class ResponseType(models.Model):
    # "responseid", "response_name", "response_description"
    responseid = models.CharField(max_length=255, blank=True, null=True)
    response_name = models.CharField(max_length=255, blank=True, null=True)
    response_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'response_type'


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


class RouteType(models.Model):
    routetypeid = models.CharField(max_length=50)
    routetype_description = models.TextField(blank=True, null=True)
    routetype = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'route_type'


class SpatialLevel(models.Model):
    code = models.CharField(max_length=300)
    level = models.CharField(max_length=50)

    class Meta:
        db_table = 'spatial_level'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        db_table = 'spatial_ref_sys'


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


class SurveyFrequency(models.Model):
    svyfreqid = models.CharField(unique=True, max_length=255)
    svy_frequency_title = models.CharField(max_length=255, blank=True, null=True)
    svy_frequency_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'survey_frequency'


class SurveyQuestionsLink(models.Model):
    surveyid = models.CharField(max_length=50, blank=True, null=True)
    qid = models.CharField(max_length=50, blank=True, null=True)
    pkid = models.IntegerField(verbose_name='pk')

    class Meta:
        db_table = 'survey_questions_link'


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


class GeometryColumns(models.Model):
    f_table_catalog = models.CharField(max_length=256, blank=True, null=True)
    f_table_schema = models.CharField(max_length=256, blank=True, null=True)
    # f_table_name = models.CharField(max_length=256, blank=True, null=True)
    f_table_name = models.CharField(primary_key=True, max_length=256)
    f_geometry_column = models.CharField(max_length=256, blank=True, null=True)
    coord_dimension = models.IntegerField()
    srid = models.IntegerField()
    type = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'geometry_columns'


class UserDetail(models.Model):
    user_id = models.CharField(max_length=25)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'user_detail'


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


