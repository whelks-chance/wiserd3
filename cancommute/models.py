from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models


class CanadaShape(models.Model):

    gid = models.IntegerField(primary_key=True)
    csdname = models.TextField(blank=True, null=True)
    csduid = models.TextField(max_length=7)
    prname = models.TextField(max_length=10, blank=True, null=True)
    ccsname = models.TextField(max_length=10, blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'canadashapevi500'

    def __unicode__(self):
        return u'{} : {}'.format(self.csdname, self.csduid)


class Route(models.Model):
    origin = models.ForeignKey(CanadaShape, to_field="gid", related_name="routeorigin", blank=True, null=True)
    destination = models.ForeignKey(CanadaShape, to_field="gid", related_name="routedestination", blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    males = models.IntegerField(blank=True, null=True)
    females = models.IntegerField(blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return u'{} : {} : {} total : {} males : {} females'.format(self.origin.csdname,
                                      self.destination.csdname,
                                      self.total,
                                      self.males,
                                      self.females)
