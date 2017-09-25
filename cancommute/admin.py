from django.contrib import admin

from django.apps import apps
from grappelli_filters.admin import FiltersMixin
from grappelli_filters.filters import SearchFilter

from cancommute import models


class CanadaShapeAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('csduid', SearchFilter),
        ('csdname', SearchFilter),
    )
admin.site.register(models.CanadaShape, CanadaShapeAdmin)


class CanadaRouteAdmin(FiltersMixin, admin.ModelAdmin):
    raw_id_fields = ("origin", "destination")

admin.site.register(models.Route, CanadaRouteAdmin)

for model in apps.get_app_config('cancommute').get_models():
    try:
        admin.site.register(model)
    except:
        pass
