import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from dataportal3.models import *
from dataportal3.serializer import *
from rest_framework import viewsets, filters
from rest_framework import permissions


class AnonGetAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            if request.method == 'GET':
                return True
            return False


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class UserPreferencesViewSet(viewsets.ModelViewSet):
    queryset = UserPreferences.objects.all()
    serializer_class = UserPreferencesSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer


class DcInfoViewSet(viewsets.ModelViewSet):
    queryset = DcInfo.objects.all()
    serializer_class = DcInfoSerializer


class DublincoreFormatViewSet(viewsets.ModelViewSet):
    queryset = DublincoreFormat.objects.all()
    serializer_class = DublincoreFormatSerializer


class DublincoreLanguageViewSet(viewsets.ModelViewSet):
    queryset = DublincoreLanguage.objects.all()
    serializer_class = DublincoreLanguageSerializer


class DublincoreTypeViewSet(viewsets.ModelViewSet):
    queryset = DublincoreType.objects.all()
    serializer_class = DublincoreTypeSerializer


class ThematicGroupViewSet(viewsets.ModelViewSet):
    queryset = ThematicGroup.objects.all()
    serializer_class = ThematicGroupSerializer


class ThematicTagViewSet(viewsets.ModelViewSet):
    queryset = ThematicTag.objects.all()
    serializer_class = ThematicTagSerializer


class QTypeViewSet(viewsets.ModelViewSet):
    queryset = QType.objects.all()
    serializer_class = QTypeSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('qid', 'survey__surveyid', 'survey__identifier',)


class ResponseTypeViewSet(viewsets.ModelViewSet):
    queryset = ResponseType.objects.all()
    serializer_class = ResponseTypeSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class RouteTypeViewSet(viewsets.ModelViewSet):
    queryset = RouteType.objects.all()
    serializer_class = RouteTypeSerializer


class SpatialLevelViewSet(viewsets.ModelViewSet):
    queryset = SpatialLevel.objects.all()
    serializer_class = SpatialLevelSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    filter_fields = ('identifier', 'survey_title', 'surveyid',)


class SurveyFrequencyViewSet(viewsets.ModelViewSet):
    queryset = SurveyFrequency.objects.all()
    serializer_class = SurveyFrequencySerializer


class SurveyQuestionsLinkViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestionsLink.objects.all()
    serializer_class = SurveyQuestionsLinkSerializer


class SpatialSurveyLinkViewSet(viewsets.ModelViewSet):
    queryset = SpatialSurveyLink.objects.all()
    serializer_class = SpatialSurveyLinkSerializer


class SurveySpatialLinkViewSet(viewsets.ModelViewSet):
    queryset = SurveySpatialLink.objects.all()
    serializer_class = SurveySpatialLinkSerializer


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class ShapeFileUploadViewSet(viewsets.ModelViewSet):
    queryset = ShapeFileUpload.objects.all()
    serializer_class = ShapeFileUploadSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class FeatureCollectionStoreViewSet(viewsets.ModelViewSet):
    queryset = FeatureCollectionStore.objects.all()
    serializer_class = FeatureCollectionStoreSerializer


class FeatureStoreViewSet(viewsets.ModelViewSet):
    queryset = FeatureStore.objects.all()
    serializer_class = FeatureStoreSerializer


class NomisSearchViewSet(viewsets.ModelViewSet):
    # def get_queryset(self):
    #
    #     queryset_parent = super(NomisSearchViewSet, self).get_queryset()
    #
    #     print 'queryset_parent', queryset_parent.query
    #
    #     print 'query_params', self.request.query_params
    #
    #     kargs = {}
    #
    #     for opt in self.request.query_params:
    #         if '__isnull' in opt:
    #
    #             # Stupid check because "False" is true
    #             res = None
    #             if self.request.query_params[opt] in ['False', 'false']:
    #                 res = False
    #             elif self.request.query_params[opt] in ['True', 'true']:
    #                 res = True
    #
    #             if res is not None:
    #                 kargs[opt] = res
    #             else:
    #                 kargs[opt] = self.request.query_params[opt]
    #
    #     print 'kargs', kargs
    #
    #     if len(kargs):
    #         query = queryset_parent.filter(**kargs)
    #         print query.query
    #         return query
    #
    #     query = queryset_parent
    #     print query.query
    #     return query

    model = NomisSearch
    queryset = model.objects.all()
    serializer_class = NomisSearchSerializer
    filter_fields = ('user', 'search_type', 'name', 'uuid')
    # filter_backends = (DjangoFilterBackend,)


# class Aberystwyth_Locality_DissolvedViewSet(viewsets.ModelViewSet):
#     queryset = Aberystwyth_Locality_Dissolved.objects.all()
#     serializer_class = Aberystwyth_Locality_DissolvedSerializer
#
#
# class Bangor_Locality_DissolvedViewSet(viewsets.ModelViewSet):
#     queryset = Bangor_Locality_Dissolved.objects.all()
#     serializer_class = Bangor_Locality_DissolvedSerializer
#
#
# class Heads_of_the_ValleysViewSet(viewsets.ModelViewSet):
#     queryset = Heads_of_the_Valleys.objects.all()
#     serializer_class = Heads_of_the_ValleysSerializer


class QualDcInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [AnonGetAllowed]
    queryset = QualDcInfo.objects.all()
    serializer_class = QualDcInfoSerializer


class QualCalaisViewSet(viewsets.ModelViewSet):
    queryset = QualCalais.objects.all()
    serializer_class = QualCalaisSerializer


class QualTranscriptDataViewSet(viewsets.ModelViewSet):
    queryset = QualTranscriptData.objects.all()
    serializer_class = QualTranscriptDataSerializer


class QualStatsViewSet(viewsets.ModelViewSet):
    queryset = QualStats.objects.all()
    serializer_class = QualStatsSerializer


class SurveyVisibilityViewSet(viewsets.ModelViewSet):
    queryset = SurveyVisibility.objects.all()
    serializer_class = SurveyVisibilitySerializer


class SurveyVisibilityMetadataViewSet(viewsets.ModelViewSet):
    queryset = SurveyVisibilityMetadata.objects.all()
    serializer_class = SurveyVisibilityMetadataSerializer


class UserGroupViewSet(viewsets.ModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class UserGroupSurveyCollectionViewSet(viewsets.ModelViewSet):
    queryset = UserGroupSurveyCollection.objects.all()
    serializer_class = UserGroupSurveyCollectionSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)