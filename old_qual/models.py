# from django.db import models
from django.contrib.gis.db import models
from django_hstore import hstore

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

# Create your models here.


class DcInfo(models.Model):
    # id = models.IntegerField(primary_key=True)

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
    coverage = models.TextField(blank=True, null=True)
    rights = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    words = models.TextField(blank=True, null=True)
    calais = models.TextField(blank=True, null=True)
    vern_geog = models.TextField(db_column='vern_Geog', blank=True, null=True)  # Field name made lowercase.

    # the_geom = models.TextField()  # This field type is a guess.

    thematic_group = models.TextField(blank=True, null=True)
    tier = models.TextField(blank=True, null=True)
    identifier2 = models.TextField(blank=True, null=True)

    the_geom = models.GeometryField(blank=True, null=True)
    objects = hstore.HStoreGeoManager()

    class Meta:
        managed = False
        db_table = 'dc_info'


class TranscriptData(models.Model):
    id = models.TextField(primary_key=True)
    rawtext = models.TextField()
    stats = models.TextField()
    pages = models.IntegerField()
    errors = models.TextField(blank=True, null=True)
    # pk = models.AutoField(primary_key=True)
    # text_index = models.TextField(blank=True, null=True)  # This field type is a guess.

    text_index = VectorField()

    objects = SearchManager(
        fields = ('rawtext'),
        config = 'pg_catalog.english', # this is default
        search_field = 'text_index', # this is default
        auto_update_search_field = True
    )

    class Meta:
        managed = False
        db_table = 'transcript_data'