from django.conf.urls import url, include, patterns
from rest_framework_jwt import views
from rest_framework_nested import routers
from api_views import *
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

__author__ = 'ubuntu'


router = routers.DefaultRouter()
router.register(r'UserRole', UserRoleViewSet, base_name='UserRole')
router.register(r'UserProfile', UserProfileViewSet, base_name='UserProfile')
router.register(r'UserPreferences', UserPreferencesViewSet, base_name='UserPreferences')
router.register(r'Search', SearchViewSet, base_name='Search')
router.register(r'DcInfo', DcInfoViewSet, base_name='DcInfo')
router.register(r'DublincoreFormat', DublincoreFormatViewSet, base_name='DublincoreFormat')
router.register(r'DublincoreLanguage', DublincoreLanguageViewSet, base_name='DublincoreLanguage')
router.register(r'DublincoreType', DublincoreTypeViewSet, base_name='DublincoreType')
router.register(r'ThematicGroup', ThematicGroupViewSet, base_name='ThematicGroup')
router.register(r'ThematicTag', ThematicTagViewSet, base_name='ThematicTag')
router.register(r'QType', QTypeViewSet, base_name='QType')
router.register(r'Question', QuestionViewSet, base_name='Question')
router.register(r'ResponseType', ResponseTypeViewSet, base_name='ResponseType')
router.register(r'Response', ResponseViewSet, base_name='Response')
router.register(r'RouteType', RouteTypeViewSet, base_name='RouteType')
router.register(r'SpatialLevel', SpatialLevelViewSet, base_name='SpatialLevel')
router.register(r'Survey', SurveyViewSet, base_name='Survey')
router.register(r'SurveyFrequency', SurveyFrequencyViewSet, base_name='SurveyFrequency')
router.register(r'SurveyQuestionsLink', SurveyQuestionsLinkViewSet, base_name='SurveyQuestionsLink')
router.register(r'SpatialSurveyLink', SpatialSurveyLinkViewSet, base_name='SpatialSurveyLink')
router.register(r'SurveySpatialLink', SurveySpatialLinkViewSet, base_name='SurveySpatialLink')
router.register(r'UserDetail', UserDetailViewSet, base_name='UserDetail')
router.register(r'ShapeFileUpload', ShapeFileUploadViewSet, base_name='ShapeFileUpload')
router.register(r'FeatureCollectionStore', FeatureCollectionStoreViewSet, base_name='FeatureCollectionStore')
router.register(r'FeatureStore', FeatureStoreViewSet, base_name='FeatureStore')
router.register(r'NomisSearch', NomisSearchViewSet, base_name='NomisSearch')
# router.register(r'Aberystwyth_Locality_Dissolved', Aberystwyth_Locality_DissolvedViewSet, base_name='Aberystwyth_Locality_Dissolved')
# router.register(r'Bangor_Locality_Dissolved', Bangor_Locality_DissolvedViewSet, base_name='Bangor_Locality_Dissolved')
# router.register(r'Heads_of_the_Valleys', Heads_of_the_ValleysViewSet, base_name='Heads_of_the_Valleys')
router.register(r'QualDcInfo', QualDcInfoViewSet, base_name='QualDcInfo')
router.register(r'QualCalais', QualCalaisViewSet, base_name='QualCalais')
router.register(r'QualTranscriptData', QualTranscriptDataViewSet, base_name='QualTranscriptData')
router.register(r'QualStats', QualStatsViewSet, base_name='QualStats')
router.register(r'SurveyVisibility', SurveyVisibilityViewSet, base_name='SurveyVisibility')
router.register(r'SurveyVisibilityMetadata', SurveyVisibilityMetadataViewSet, base_name='SurveyVisibilityMetadata')
router.register(r'UserGroup', UserGroupViewSet, base_name='UserGroup')
router.register(r'UserGroupSurveyCollection', UserGroupSurveyCollectionViewSet, base_name='UserGroupSurveyCollection')

urlpatterns = [
    url(r'^', include(router.urls, namespace='api')),
    url(r'^refresh-api-token-auth/', refresh_jwt_token),
    url(r'^obtain-api-token-auth/', obtain_jwt_token),
    url(r'^docs/', include('rest_framework_swagger.urls'))
]