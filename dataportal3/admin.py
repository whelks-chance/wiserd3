from django.apps import apps
from django.contrib import admin

from dataportal3 import models
from django.contrib.gis import admin as gis_admin

# from old import models

# Register your models here.
from dataportal3.models import Question, UserGroupSurveyCollection, SurveyVisibilityMetadata


class SanityAdmin(admin.ModelAdmin):
    raw_id_fields = ("survey", "link_from_question", "subof_question", "response")

admin.site.register(Question, SanityAdmin)
admin.site.register(models.FeatureStore, gis_admin.GeoModelAdmin)


# TODO this is a mess
class SurveyVisibilityMetadataInline(admin.StackedInline):
    model = SurveyVisibilityMetadata


class UserGroupSurveyCollectionAdmin(admin.ModelAdmin):
    inlines = [
        SurveyVisibilityMetadataInline,
    ]
admin.site.register(UserGroupSurveyCollection, UserGroupSurveyCollectionAdmin)

# class SurveyVisibilityMetadataAdmin(admin.ModelAdmin):
    # list_filter = ('survey',)
    # raw_id_fields = ('survey',)
# admin.site.register(SurveyVisibilityMetadata, SurveyVisibilityMetadataAdmin)

# Add all the regular models to admin
for model in apps.get_app_config('dataportal3').get_models():
    try:
        admin.site.register(model)
    except:
        pass

# Add all the old models - this can be removed eventually
for model in apps.get_app_config('old').get_models():
    try:
        admin.site.register(model)
    except:
        pass