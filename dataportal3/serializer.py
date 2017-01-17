from rest_framework import serializers
from dataportal3.models import *


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'


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
        fields = '__all__'


class DublincoreFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DublincoreFormat
        fields = '__all__'


class DublincoreLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DublincoreLanguage
        fields = '__all__'


class DublincoreTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DublincoreType
        fields = '__all__'


class ThematicGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicGroup
        fields = '__all__'


class ThematicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicTag
        fields = '__all__'


class QTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QType
        fields = '__all__'


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
        fields = '__all__'


class ResponseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseType
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'


class RouteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteType
        fields = '__all__'


class SpatialLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpatialLevel
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class SurveyFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFrequency
        fields = '__all__'


class SurveyQuestionsLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestionsLink
        fields = '__all__'


class SpatialSurveyLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpatialSurveyLink
        fields = '__all__'


class SurveySpatialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveySpatialLink
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'


class get_upload_directorySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_upload_directory
        fields = '__all__'


class ShapeFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShapeFileUpload
        fields = '__all__'


class FeatureCollectionStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureCollectionStore
        fields = '__all__'


class FeatureStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureStore
        fields = '__all__'


class NomisSearchSerializer(serializers.ModelSerializer):
    search_type = serializers.SlugRelatedField(read_only=True, slug_field='name')
    datetime = serializers.DateTimeField('%d/%b/%y %H:%M:%S %z')

    class Meta:
        model = NomisSearch
        fields = '__all__'


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
        fields = '__all__'


class QualCalaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualCalais
        fields = '__all__'


class QualTranscriptDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualTranscriptData
        fields = '__all__'


class QualStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualStats
        fields = '__all__'


class SurveyVisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyVisibility
        fields = '__all__'


class SurveyVisibilityMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyVisibilityMetadata
        fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'


class UserGroupSurveyCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroupSurveyCollection
        fields = '__all__'
