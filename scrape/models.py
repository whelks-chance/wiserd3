from django.db import models
from django.contrib.gis.db import models

# Create your models here.


class BuildingType(models.Model):
    description = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return u'{}'.format(self.description)


class BillingAuthority(models.Model):
    billing_authority_name = models.CharField(max_length=100, blank=True, null=True)
    billing_authority_code = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return u'{}_::_{}'.format(self.billing_authority_name, self.billing_authority_code)


class TaxServicePropertyInformation(models.Model):

    address = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)

    description = models.CharField(max_length=250, blank=True, null=True)
    building_type = models.ForeignKey(BuildingType, blank=True, null=True)

    billing_authority_code = models.CharField(max_length=25, blank=True, null=True)
    billing_authority_link = models.ForeignKey(BillingAuthority, blank=True, null=True)

    total_area_m2_unit = models.CharField(max_length=50, blank=True, null=True)
    total_area_m2_unit_num = models.FloatField(blank=True, null=True)

    price_per_m2_unit = models.CharField(max_length=50, blank=True, null=True)
    price_per_m2_unit_num = models.FloatField(blank=True, null=True)

    current_rateable_value = models.CharField(max_length=50, blank=True, null=True)
    current_rateable_value_num = models.FloatField(blank=True, null=True)

    lsoa_name = models.CharField(max_length=254, blank=True, null=True)
    lsoa_code = models.CharField(max_length=254, blank=True, null=True)

    geom = models.GeometryField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'tax_service_property_information'

    def __unicode__(self):
        return u'{}_{}'.format(self.address, self.current_rateable_value)