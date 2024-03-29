import json
import pprint

from django.apps import apps
from django.contrib import admin
from grappelli_filters.filters import SearchFilter
from grappelli_filters.admin import  FiltersMixin
from django import forms
from django.forms.widgets import Textarea

from django.contrib.gis import admin as gis_admin

# from old import models

# Register your models here.
from dataportal3.models import Question, UserGroupSurveyCollection, SurveyVisibilityMetadata, Response, Search, \
    ResponseTable, MetaDataToRemoteMapping, SchoolData, SpatialdataPostCodePoint, NomisSearch, SpatialSurveyLink, FeatureStore, DcInfo, \
    SpatialdataUKUA


class FlattenJsonWidget(Textarea):
    # def my_safe_repr(self, object, context, maxlevels, level):
    #     typ = pprint._type(object)
    #     if typ is unicode:
    #         object = str(object)
    #     return pprint._safe_repr(object, context, maxlevels, level)

    def render(self, name, value, attrs=None):
        if not value is None:
            print value, type(value)
            try:
                # # If there's no unicode awkwardness, print without u''
                # printer = pprint.PrettyPrinter()
                # printer.format = self.my_safe_repr
                # parsed_val = printer.pformat(value)

                parsed_val = json.dumps(value, indent=4)
            except:
                # use u'' for non ASCII data
                parsed_val = pprint.pformat(value)

            value = parsed_val
        return super(FlattenJsonWidget, self).render(name, value, attrs)


class JSONForm(forms.ModelForm):
    feature_attributes = forms.CharField(widget=FlattenJsonWidget)

    class Meta:
        model = ResponseTable
        fields = '__all__'

class JSONAdmin(admin.ModelAdmin):
    form = JSONForm


# admin.site.register(ResponseTable, JSONAdmin)

class DublinCoreAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(DcInfo, DublinCoreAdmin)


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
admin.site.register(FeatureStore, gis_admin.GeoModelAdmin)


class QuestionInline(admin.StackedInline):
    model = Question
    raw_id_fields = ("survey", "link_from_question", "subof_question", "response")

    # fk_name = "response"


class ResponseTableInline(admin.StackedInline):
    model = ResponseTable
    raw_id_fields = ("survey", "link_from_question", "response")


class ResponseAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('responseid', SearchFilter),
        ('responsetext', SearchFilter),
        ('route_notes', SearchFilter),
    )
    inlines = [
        QuestionInline, ResponseTableInline
    ]


admin.site.register(Response, ResponseAdmin)


class ResponseTableAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('response_id', SearchFilter),
        ('id', SearchFilter)
    )
    raw_id_fields = ("response_id", "survey", "link_from_question")

admin.site.register(ResponseTable, ResponseTableAdmin)


class PostcodePointAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('postcode', SearchFilter),
    )

admin.site.register(SpatialdataPostCodePoint, PostcodePointAdmin)


class SchoolAdmin(FiltersMixin, admin.ModelAdmin):
    # raw_id_fields = ("name", "postcode", "schoolType")
    list_filter = (
        ('name', SearchFilter),
        ('postcode', SearchFilter),
        ('schoolType', SearchFilter),
        ('LEANameEnglish', SearchFilter),
        ('schoolCode', SearchFilter),
    )
admin.site.register(SchoolData, SchoolAdmin)


class NomisSearchAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('uuid', SearchFilter),
        ('name', SearchFilter),
    )
admin.site.register(NomisSearch, NomisSearchAdmin)


class SpatialSurveyLinkAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('full_name', SearchFilter),
        ('data_name', SearchFilter),
        ('survey__identifier', SearchFilter)
    )
admin.site.register(SpatialSurveyLink, SpatialSurveyLinkAdmin)


class UKUAAdmin(FiltersMixin, admin.ModelAdmin):
    list_filter = (
        ('ctyua15cd', SearchFilter),
        ('ctyua15nm', SearchFilter),
        ('ctyua15nmw', SearchFilter)
    )
admin.site.register(SpatialdataUKUA, UKUAAdmin)


# TODO this is a mess
class SurveyVisibilityMetadataInline(admin.StackedInline):
    model = SurveyVisibilityMetadata


class UserGroupSurveyCollectionAdmin(admin.ModelAdmin):
    inlines = [
        SurveyVisibilityMetadataInline,
    ]
admin.site.register(UserGroupSurveyCollection, UserGroupSurveyCollectionAdmin)


class MetadataMappingAdmin(FiltersMixin, admin.ModelAdmin):
    raw_id_fields = ("wiserd_question", "remote_dataset")
    list_filter = (
        ('wiserd_question__qid', SearchFilter),
        ('remote_dataset__dataset_identifier', SearchFilter)
    )

admin.site.register(MetaDataToRemoteMapping, MetadataMappingAdmin)

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