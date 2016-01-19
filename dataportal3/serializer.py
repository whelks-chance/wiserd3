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
