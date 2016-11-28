from rest_framework import serializers
from dataportal3.models import *


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search


class DcInfoSerializer(serializers.ModelSerializer):
    subjects = serializers.SlugRelatedField(many=True, read_only=True, slug_field='tag_text')
    creators = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    publishers = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    contributors = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    coverage_spatial = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    relation_same_collection = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    relation_different_collection = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')

    type = serializers.SlugRelatedField(read_only=True, slug_field='dc_type_title')
    format = serializers.SlugRelatedField(read_only=True, slug_field='dc_format_title')
    language = serializers.SlugRelatedField(read_only=True, slug_field='dc_language_title')
    user_id = serializers.SlugRelatedField(read_only=True, slug_field='user_name')

    class Meta:
        model = DcInfo


class DublincoreFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DublincoreFormat


class DublincoreLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DublincoreLanguage


class DublincoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DublincoreType


class ThematicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicGroup


class ThematicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicTag


class QTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QType


class QuestionSerializer(serializers.ModelSerializer):
    # thematic_tags_set = ThematicTagSerializer(read_only=True, many=True)
    # thematic_groups_set = ThematicGroupSerializer(read_only=True, many=True)

    thematic_tags_set = serializers.SlugRelatedField(slug_field="tag_text", read_only=True, many=True)
    thematic_groups_set = serializers.SlugRelatedField(slug_field="grouptitle", read_only=True, many=True)

    link_from_name = serializers.SerializerMethodField()
    def get_link_from_name(self, foo):
        # print type(foo)
        if foo.link_from_question:
            return foo.link_from_question.questionnumber
        else:
            return None

    sub_of_name = serializers.SerializerMethodField()
    def get_sub_of_name(self, foo):
        # print type(foo)
        if foo.subof_question:
            return foo.subof_question.questionnumber
        else:
            return None

    # link_from_name = serializers.SlugRelatedField(many=True, read_only=True, slug_field='questionnumber')
    # subof_name = serializers.SlugRelatedField(many=True, read_only=True, slug_field='questionnumber')

    type = serializers.SlugRelatedField(read_only=True, slug_field='q_type_text')
    survey = serializers.SlugRelatedField(read_only=True, slug_field='identifier')

    class Meta:
        model = Question


class ResponseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseType


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response


class RouteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteType


class SpatialLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpatialLevel


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey


class SurveyFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFrequency


class SurveyQuestionsLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestionsLink


class SpatialSurveyLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpatialSurveyLink


class SurveySpatialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveySpatialLink


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail


class get_upload_directorySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_upload_directory


class ShapeFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShapeFileUpload


class FeatureCollectionStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureCollectionStore


class FeatureStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureStore


class NomisSearchSerializer(serializers.ModelSerializer):
    search_type = serializers.SlugRelatedField(read_only=True, slug_field='name')
    datetime = serializers.DateTimeField('%d/%b/%y %H:%M:%S %z')

    class Meta:
        model = NomisSearch


class Aberystwyth_Locality_DissolvedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aberystwyth_Locality_Dissolved


class Bangor_Locality_DissolvedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bangor_Locality_Dissolved


class Heads_of_the_ValleysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heads_of_the_Valleys


class QualDcInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualDcInfo


class QualCalaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualCalais


class QualTranscriptDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualTranscriptData


class QualStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualStats


class SurveyVisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyVisibility


class SurveyVisibilityMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyVisibilityMetadata


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup


class UserGroupSurveyCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroupSurveyCollection
