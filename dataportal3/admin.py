from django.apps import apps
from django.contrib import admin

from dataportal3 import models
from django.contrib.gis import admin as gis_admin

# from old import models

# Register your models here.


# class ImageSanityAdmin(admin.ModelAdmin):
#     raw_id_fields = ("image",)

# admin.site.register(Tag, ImageSanityAdmin)

admin.site.register(models.FeatureStore, gis_admin.GeoModelAdmin)

for model in apps.get_app_config('dataportal3').get_models():
    try:
        admin.site.register(model)
    except:
        pass


for model in apps.get_app_config('old').get_models():
    try:
        admin.site.register(model)
    except:
        pass