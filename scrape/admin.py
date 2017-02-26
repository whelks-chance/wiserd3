from django.contrib import admin
from django.apps import apps
from grappelli_filters.admin import FiltersMixin
from grappelli_filters.filters import SearchFilter
from scrape import models

# Register your models here.


class TaxServicePropertyInformationAdmin(FiltersMixin, admin.ModelAdmin):

    list_filter = (
        ('address', SearchFilter),
        ('postcode', SearchFilter),
        ('description', SearchFilter),
        ('building_type__description', SearchFilter),

        ('lsoa_name', SearchFilter),
        ('lsoa_code', SearchFilter),

        ('billing_authority_code', SearchFilter),
        ('billing_authority_link__billing_authority_name', SearchFilter),
        ('billing_authority_link__billing_authority_code', SearchFilter),

        ('total_area_m2_unit', SearchFilter),
        ('total_area_m2_unit_num', SearchFilter),
        ('price_per_m2_unit', SearchFilter),
        ('price_per_m2_unit_num', SearchFilter),
        ('current_rateable_value', SearchFilter),
        ('current_rateable_value_num', SearchFilter),
    )

admin.site.register(models.TaxServicePropertyInformation, TaxServicePropertyInformationAdmin)


class BuildingTypeAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('description', SearchFilter),

    )
admin.site.register(models.BuildingType, BuildingTypeAdmin)


# Add all the regular models to admin
for model in apps.get_app_config('scrape').get_models():
    try:
        admin.site.register(model)
    except:
        pass