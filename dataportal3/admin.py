from django.apps import apps
from django.contrib import admin
from grappelli_filters import SearchFilter, FiltersMixin


from dataportal3 import models
from django.contrib.gis import admin as gis_admin

# from old import models

# Register your models here.
from dataportal3.models import Question, UserGroupSurveyCollection, SurveyVisibilityMetadata, Response, Search


class DublinCoreAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(models.DcInfo, DublinCoreAdmin)


class QuestionAdmin(FiltersMixin, admin.ModelAdmin):
    raw_id_fields = ("survey", "link_from_question", "subof_question", "response")
    list_filter = (
        ('literal_question_text', SearchFilter),
        ('qid', SearchFilter),
        ('questionnumber', SearchFilter),
        ('survey__surveyid', SearchFilter)
    )
admin.site.register(Question, QuestionAdmin)


class SearchAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('query', SearchFilter),
        ('type', SearchFilter),
        ('readable_name', SearchFilter),
        ('user__user__username', SearchFilter)
    )


admin.site.register(Search, SearchAdmin)
admin.site.register(models.FeatureStore, gis_admin.GeoModelAdmin)


class QuestionInline(admin.StackedInline):
    model = Question
    raw_id_fields = ("survey", "link_from_question", "subof_question", "response")

    # fk_name = "response"


class ResponseAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('responseid', SearchFilter),
        ('responsetext', SearchFilter),
        ('route_notes', SearchFilter),
    )
    inlines = [
        QuestionInline,
    ]


admin.site.register(Response, ResponseAdmin)


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