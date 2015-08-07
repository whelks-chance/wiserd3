from __future__ import unicode_literals

# from djorm_pgfulltext.models import SearchManager
# from djorm_pgfulltext.fields import VectorField
import uuid
from django.contrib.gis.db import models
from django.contrib.auth.models import User

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
    qtext_index = models.TextField(blank=True, null=True)  # This field type is a guess.

    # qtext_index = VectorField()
    #
    # objects = SearchManager(
    #     fields = ('literal_question_text', 'notes'),
    #     config = 'pg_catalog.english', # this is default
    #     search_field = 'qtext_index', # this is default
    #     auto_update_search_field = True
    # )

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


class UserDetail(models.Model):
    user_id = models.CharField(max_length=25)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'user_detail'


class XSidLiw2007Aefa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liw2007_aefa_'


class XSidLiw2007Fire(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liw2007_fire_'


class XSidLiw2007Lsoa(models.Model):
    table_pk = models.IntegerField()
    area_id = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    area_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x_sid_liw2007_lsoa_'


class XSidLiw2007Parl(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liw2007_parl_'


class XSidLiw2007Pcode(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liw2007_pcode_'


class XSidLiw2007Police(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liw2007_police_'


class XSidLiw2007Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liw2007_ua_'


class XSidLiwhh2004Aefa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2004_aefa_'


class XSidLiwhh2004Fire(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2004_fire_'


class XSidLiwhh2004Lsoa(models.Model):
    table_pk = models.IntegerField()
    area_id = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    area_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2004_lsoa_'


class XSidLiwhh2004Parl(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2004_parl_'


class XSidLiwhh2004Pcode(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2004_pcode_'


class XSidLiwhh2004Police(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2004_police_'


class XSidLiwhh2004Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2004_ua_'


class XSidLiwhh2005Aefa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2005_aefa_'


class XSidLiwhh2005Fire(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2005_fire_'


class XSidLiwhh2005Lsoa(models.Model):
    table_pk = models.IntegerField()
    area_id = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    area_name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2005_lsoa_'


class XSidLiwhh2005Parl(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2005_parl_'


class XSidLiwhh2005Pcode(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2005_pcode_'


class XSidLiwhh2005Police(models.Model):
    table_pk = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2005_police_'


class XSidLiwhh2005Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2005_ua_'


class XSidLiwhh2006Aefa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2006_aefa_'


class XSidLiwhh2006Fire(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2006_fire_'


class XSidLiwhh2006Lsoa(models.Model):
    table_pk = models.IntegerField()
    area_id = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.
    area_name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2006_lsoa_'


class XSidLiwhh2006Parl(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2006_parl_'


class XSidLiwhh2006Pcode(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2006_pcode_'


class XSidLiwhh2006Police(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2006_police_'


class XSidLiwhh2006Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwhh2006_ua_'


class XSidLiwps2004Aefa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwps2004_aefa_'


class XSidLiwps2004Fire(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwps2004_fire_'


class XSidLiwps2004Lsoa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwps2004_lsoa_'


class XSidLiwps2004Parl(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwps2004_parl_'


class XSidLiwps2004Pcode(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwps2004_pcode_'


class XSidLiwps2004Police(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwps2004_police_'


class XSidLiwps2004Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_liwps2004_ua_'


class XSidWersmq2004Wales(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_wersmq2004_wales_'


class XSidWhs0306Aq1Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs0306aq1_ua_'


class XSidWhs0306Aq2Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs0306aq2_ua_'


class XSidWhs0306Aq3Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs0306aq3_ua_'


class XSidWhs0306Cq1Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs0306cq1_ua_'


class XSidWhs0306Cq2Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs0306cq2_ua_'


class XSidWhs0306Cq3Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs0306cq3_ua_'


class XSidWhs200703Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.CharField(max_length=500, blank=True, null=True)
    successful = models.CharField(max_length=500, blank=True, null=True)
    refused = models.CharField(max_length=500, blank=True, null=True)
    no_contact = models.CharField(max_length=500, blank=True, null=True)
    ineligible = models.CharField(max_length=500, blank=True, null=True)
    other = models.CharField(max_length=500, blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2007_03_ua_'


class XSidWhs20071315Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2007_1315_ua_'


class XSidWhs2007412Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2007_412_ua_'


class XSidWhs2007AqUa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2007aq_ua_'


class XSidWhs200803Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2008_03_ua_'


class XSidWhs20081315Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2008_1315_ua_'


class XSidWhs2008412Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2008_412_ua_'


class XSidWhs2008AqUa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2008aq_ua_'


class XSidWhs200903Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2009_03_ua_'


class XSidWhs20091315Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2009_1315_ua_'


class XSidWhs2009412Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2009_412_ua_'


class XSidWhs2009AqUa(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whs2009aq_ua_'


class XSidWhshh03061Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whshh03061_ua_'


class XSidWhshh03062Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whshh03062_ua_'


class XSidWhshh03063Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whshh03063_ua_'


class XSidWhshh2007Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whshh2007_ua_'


class XSidWhshh2008Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whshh2008_ua_'


class XSidWhshh2009Ua(models.Model):
    table_pk = models.IntegerField()
    area_name = models.CharField(max_length=500, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    successful = models.IntegerField(blank=True, null=True)
    refused = models.IntegerField(blank=True, null=True)
    no_contact = models.IntegerField(blank=True, null=True)
    ineligible = models.IntegerField(blank=True, null=True)
    other = models.FloatField(blank=True, null=True)
    response_rate = models.CharField(max_length=500, blank=True, null=True)
    adjusted_rr = models.CharField(max_length=500, blank=True, null=True)
    the_geom = models.GeometryField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'x_sid_whshh2009_ua_'