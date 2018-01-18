# -*- coding: utf-8 -*-

#import base64
import zipfile
#from datetime import datetime
import json
import os
import pprint
import uuid

import StringIO
import re
from BeautifulSoup import BeautifulSoup
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
# from django.contrib.gis.gdal import CoordTransform
# from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import MultipleObjectsReturned
from django.core.serializers import serialize
from django.db import connections
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
import operator
from dataportal3 import models
from dataportal3.forms import ShapefileForm
from dataportal3.models import ResponseTable
from dataportal3.utils.ShapeFileImport import celery_import, ShapeFileImport
from dataportal3.utils.admin_email import EMAIL_TYPES, send_email
from dataportal3.utils.ckan.ckan_data import CKANdata
from dataportal3.utils.remote_data import RemoteData
from dataportal3.utils.spatial_search.spatial_search import find_intersects, geometry_columns
from dataportal3.utils.statswales.statswales_odata import StatsWalesOData
from dataportal3.utils.userAdmin import get_anon_user, get_user_searches, get_request_user, get_user_preferences, \
    survey_visible_to_user, set_session_preferred_language
import requests
from old.views import text_search, date_handler
from rubbish.formatting.question_ordering import QuestionSorter
from wiserd3 import settings
from wiserd3.settings import NAW_LAYER_UUIDS, NAW_CY_LAYER_UUIDS, REDIS_DATA_CACHE_HOST, REDIS_DATA_CACHE_PORT, \
    REDIS_DATA_CACHE_DB
# from verbalexpressions import VerEx
from djgeojson.serializers import Serializer as GeoJSONSerializer
import redis

redis_cache = redis.StrictRedis(host=REDIS_DATA_CACHE_HOST, port=REDIS_DATA_CACHE_PORT, db=REDIS_DATA_CACHE_DB)

def dashboard(request):
    tech_blog_posts = ''
    wiserd_blog_posts = ''
    try:
        tech_blog = requests.get('http://dataportal-development.blogspot.com/feeds/posts/default')
        soup = BeautifulSoup(tech_blog.text)
        x = soup.find('opensearch:totalresults')
        print x.text
        tech_blog_posts = x.text

        tech_blog = requests.get('http://blogs.cardiff.ac.uk/wiserd/')
        soup = BeautifulSoup(tech_blog.text)
        x = soup.find("aside", {"id": "categories-2"}).ul.findAll('li')[0].findAll()[0]
        wiserd_blog_posts = x.nextSibling.strip().replace('(', '').replace(')', '')
    except:
        pass
    return render(request, 'dashboard.html',
                  {
                      'tech_blog_posts': tech_blog_posts,
                      'wiserd_blog_posts': wiserd_blog_posts,
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  },context_instance=RequestContext(request))


# def user_settings(request):
#     return render(request, 'settings.html',
#                   {
#                       'languages': models.UserLanguage.objects.all(),
#                       'preferences': get_user_preferences(request),
#                       'searches': get_user_searches(request),
#                   },
#                   context_instance=RequestContext(request))


def search_survey_question_gui(request):
    search_terms = request.GET.get('search_terms', '')
    # ors = search_terms.split(',')
    return render(request, 'search.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'search_terms': search_terms,
                      'url': request.get_full_path()
                  }, context_instance=RequestContext(request))


def search_survey_question_api(request):
    search_terms = request.GET.get('search_terms', '')
    thematic_groups = []
    thematic_tags = []
    thematic_groups_questions = []
    thematic_tags_questions = []
    combine_text_and_tags_questions = models.Question.objects.none()

    api_data, questions_models = text_search(search_terms)

    if search_terms:
        # Don't save a blank search
        user_profile = get_request_user(request)
        search, created = models.Search.objects.using('new').get_or_create(user=user_profile,
                                                                           query=search_terms,
                                                                           readable_name=search_terms,
                                                                           type='text')
        search.save()

        # thematic_groups_objects = models.ThematicGroup.objects.filter(
        #     Q(grouptitle__icontains=search_terms) | Q(groupdescription__icontains=search_terms)
        # )
        # thematic_groups = list(thematic_groups_objects.values())
        #
        # thematic_groups_questions_objects = models.Question.objects.filter(
        #     thematic_groups_set__in=thematic_groups_objects
        # )
        # thematic_groups_questions = list(thematic_groups_questions_objects.values())

        thematic_tags_objects = models.ThematicTag.objects.filter(
            Q(tag_text__icontains=search_terms) | Q(tag_description__icontains=search_terms)
        )
        thematic_tags = list(thematic_tags_objects.values())

        thematic_tags_questions_objects = models.Question.objects.filter(
            thematic_tags_set__in=thematic_tags_objects
        ).distinct("qid")

        combine_text_and_tags = thematic_tags_questions_objects | questions_models
        print combine_text_and_tags.count(), 'forces eval'

        combine_text_and_tags_values = combine_text_and_tags.prefetch_related('type') \
            .prefetch_related('survey').distinct("qid") \
            .values("survey__identifier", "survey__collectionstartdate",
                    "survey__survey_title", "qid", "literal_question_text",
                    "questionnumber", "thematic_groups", "thematic_tags", "link_from",
                    "subof", "type__q_type_text", "variableid", "notes", "user_id",
                    "created", "updated", "qtext_index", 'metadatatoremotemapping__remote_dataset__dataset_identifier')
        combine_text_and_tags_questions = list(combine_text_and_tags_values)

        # question_mappings = models.MetaDataToRemoteMapping.objects.filter(wiserd_question__in=list(models.Question.objects.search(combine_text_and_tags)))

        # qid_sublist = list(combine_text_and_tags.values_list('qid', flat=True))

        # Don't need this as we have metadatatoremotemapping__remote_dataset__dataset_identifier above

        # question_mappings = models.MetaDataToRemoteMapping.objects.filter(wiserd_question__qid__in=list(combine_text_and_tags.values_list('qid', flat=True))).prefetch_related('wiserd_question').prefetch_related('remote_dataset')
        #
        # print question_mappings.query
        # print question_mappings
        #
        # api_data['question_mappings'] = list(question_mappings.values('wiserd_question__qid', "remote_dataset__dataset_identifier"))

    api_data['url'] = request.get_full_path()

    # api_data['thematic_groups'] = thematic_groups
    # api_data['thematic_groups_questions'] = thematic_groups_questions

    api_data['thematic_tags'] = thematic_tags
    # api_data['thematic_tags_questions'] = combine_text_and_tags_questions
    api_data['search_result_data'] = combine_text_and_tags_questions

    conn_queries = connections['new'].queries
    # for q in connections['new'].queries:
    #     print '\n\n', q
    print 'question conn num end', len(conn_queries)
    # print question_mappings.query

    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def search_survey_api(request):
    search_terms = request.GET.get('search_terms', '')
    show_all = request.GET.get('show_all', '')

    user_profile = get_request_user(request)

    if show_all:
        survey_models = models.Survey.objects.all().values()

    elif search_terms:
        search, created = models.Search.objects.using('new').get_or_create(user=user_profile,
                                                                           query=search_terms,
                                                                           readable_name=search_terms,
                                                                           type='text')
        search.save()

        survey_models = models.Survey.objects.filter(
            Q(survey_title__icontains=search_terms) | Q(short_title__icontains=search_terms)
        ).distinct("identifier").values()
    else:
        survey_models = models.Survey.objects.none()

    data = []
    for survey_model in survey_models:
        geogs_list = models.SpatialSurveyLink.objects.filter(
            survey__identifier=survey_model['identifier']
        ).values_list('boundary_name', flat=True)

        # print '***'
        # print geogs_list.query

        survey_model['area'] = list(set(geogs_list))
        data.append(survey_model)

    api_data = {
        'method': 'search_survey',
        'search_result_data': data,
        'results_count': len(data),
        'search_term': search_terms,
        'url': request.get_full_path()
    }

    # conn_queries = connections['new'].queries
    # print 'survey conn num end', len(conn_queries)
    # print 'survey queries', conn_queries

    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def blank(request):
    return render(request, 'blank.html', {}, context_instance=RequestContext(request))


# def survey_visible_to_user(survey_id, user_profile):
#     # Assume access is OK unless a visibility is set
#     # Switch access to False if any visibility levels are set
#     # Then keep assuming false until a single True is seen
#     # 9 No's and 1 Yes means Yes
#     allowed = True
#     access_data = []
#
#     # Find any specific visibility metadata for this survey
#     # It is possible that multiple visibilities may be set for a single survey
#     survey_visibilities = models.SurveyVisibilityMetadata.objects.filter(survey__identifier=survey_id)
#     if survey_visibilities.count():
#
#         # We have at least one visibility set, so assume False to begin with
#         # We'll enable access again if we need to
#         allowed = False
#
#         # Search through each visibility metadata entry to check access is allowed
#         for survey_vis in survey_visibilities:
#
#             # Each visibility has a primary contact to designate access to users
#             # This person may or may not be a defined member of the associated user group,
#             # but will require at least a shell user account within the dataportal
#             contact = survey_vis.primary_contact.user
#
#             if survey_vis.survey_visibility.visibility_id == 'SUR_VIS_ALL':
#                 # Allow access as visibility is Allow All
#                 allowed = True
#
#             elif survey_vis.survey_visibility.visibility_id == 'SUR_VIS_NONE':
#                 # Deny access - be careful using this, as race conditions may apply
#                 # TODO what happens if the survey is allowed by one group and denied by another?
#                 allowed = False
#
#             elif survey_vis.survey_visibility.visibility_id == 'SUR_VIS_GROUP':
#                 # Grab all user groups for this surveys
#                 user_group_members = survey_vis.user_group_survey_collection.user_group.user_group_members.all()
#
#                 survey_collection_name = survey_vis.user_group_survey_collection.name
#                 survey_collection_user_group_name = survey_vis.user_group_survey_collection.user_group.name
#                 print survey_collection_name, survey_collection_user_group_name, user_group_members
#
#                 if user_profile in user_group_members:
#                     allowed = True
#
#                     access_data.append({
#                         'contact': contact,
#                         'survey_collection_name': survey_collection_name,
#                         'survey_collection_user_group_name': survey_collection_user_group_name
#                     })
#
#     return allowed, access_data
#

def survey_detail(request, survey_id):
    user_profile = get_request_user(request)

    search, created = models.Search.objects.using('new').get_or_create(user=user_profile, query=survey_id, type='survey')
    search.save()

    # Check if we're allowed to show this data
    allowed, access_data = survey_visible_to_user(survey_id, user_profile)

    if allowed:
        return render(request, 'survey_detail.html',
                      {
                          'preferences': get_user_preferences(request),
                          'searches': get_user_searches(request),
                          'survey_id': survey_id,
                          'access_allow': {
                              'method': 'survey_detail',
                              'survey_id': survey_id,
                              'document_type': 'survey',
                              'access_data': access_data
                          }
                      }, context_instance=RequestContext(request))
    else:
        return render(request, 'access_fail.html',
                      {
                          'preferences': get_user_preferences(request),
                          'searches': get_user_searches(request),
                          'access_fail': {
                              'method': 'survey_detail',
                              'survey_id': survey_id,
                              'document_type': 'survey',
                              'access_data': access_data
                          }
                      }, context_instance=RequestContext(request))


def tables(request):
    search_id = request.GET.get('search_id', '')
    geom = ''
    search_name = ''
    image_png = ''
    if len(search_id):
        search = models.Search.objects.get(uid=search_id)
        if search.readable_name is not None and len(search.readable_name):
            search_name = search.readable_name
        else:
            search_name = 'Search - ' + str(search.id)

        if search.type == 'spatial':
            geom = search.query
            image_png = search.image_png

    return render(request, 'tables.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'search_id': search_id,
                      'geom': geom,
                      'image_png': image_png,
                      'search_name': search_name
                  },
                  context_instance=RequestContext(request))


def map_search(request):
    print request.GET

    # Default template
    template_name = 'navigation.html'
    # Third Party Templating
    tpt = request.GET.get('tpt', 'default')

    naw = request.GET.get('naw', False)
    if naw:
        tpt = 'naw'
        template_name = 'naw_navigation.html'

    use_template = request.GET.get('use_template', True)
    if use_template == 'False':
        template_name = 'empty.html'
        use_template = False

    if tpt in settings.THIRD_PARTY_INTERFACES:
        template_name = tpt + '_navigation.html'
        if tpt == 'm4w':
            template_name = 'm4w_navigation.html'

        if tpt == 'naw':
            naw = True
            template_name = 'naw_navigation.html'

        if tpt == 'wmh':
            template_name = 'wmh_navigation.html'

        if tpt == 'aqp':
            template_name = 'aqp_navigation.html'

    if tpt == 'wiserd_projects':
        template_name = 'wiserd_projects_navigation.html'

    if tpt == 'aqp':
        template_name = 'aqp_navigation.html'

    if tpt == 'wep':
        template_name = 'wep_navigation.html'

    if tpt == 'partner_projects':
        template_name = 'partner_projects_navigation.html'

    if tpt == 'about':
        template_name = 'about_navigation.html'

    try:
        get_template(template_name)
    except TemplateDoesNotExist:
        raise Http404

    layer_uuids = request.GET.getlist('layers', [])
    print 'layer_uuids', layer_uuids, type(layer_uuids)

    wms_layers = {}
    # for layer in settings.WMS_LAYERS:
    #     try:
    #         filename = os.path.join(settings.BASE_DIR, os.path.join('dataportal3', os.path.join('static', layer['filename'])))
    #         print filename
    #         capabilities = open(filename, 'r').read()
    #         soup = BeautifulSoup(capabilities)
    #         x = soup.wms_capabilities.capability.findAll('layer', queryable=1)
    #         b = []
    #         for y in x:
    #             b.append({
    #                 'tile_name': [z.string for z in y.findAll('name')][0],
    #                 'name': [z.string for z in y.findAll('title')][0]
    #             })
    #         wms_layers[layer['url_wms']] = b
    #
    #     except Exception as e9832478:
    #         print type(e9832478), e9832478

    surveys = request.GET.getlist('surveys', [])
    boundaries = request.GET.getlist('boundary', [])
    local_data_layers = []

    if len(surveys) == len(boundaries):
        for idx, survey_id in enumerate(surveys):
            print 'idx', idx
            print 'survey_id', survey_id
            print 'boundaries[idx]', boundaries[idx]

            link_table_data = models.SpatialSurveyLink.objects.filter(survey__identifier=survey_id, boundary_name=boundaries[idx]).values_list('data_name', flat=True)
            # datas = []
            print 'data available for ', survey_id, list(link_table_data)
            # for links in link_table:
            #     datas.append()
            local_data_layers.append({
                'name': models.Survey.objects.get(identifier=survey_id).survey_title.replace('_', ' '),
                'survey_id': survey_id,
                'boundary_name': boundaries[idx],
                'data': list(link_table_data)
            })

    uploaded_layers_clean = []
    try:
        # wiserd_layers = models.GeometryColumns.objects.using('survey').filter(f_table_schema='spatialdata')
        # for w_layer in wiserd_layers:
        #     wiserd_layers_clean.append({
        #         'display_name': w_layer.f_table_name.replace('_', ' ').title(),
        #         'table_name': w_layer.f_table_name
        #     })

        uploaded_layers = models.FeatureCollectionStore.objects.filter(
            shapefile_upload__progress=ShapeFileImport.progress_stage['import_success']
        )
        for uploaded_layer in uploaded_layers:
            uploaded_layers_clean.append({
                'display_name': uploaded_layer.name,
                'table_name': uploaded_layer.id
            })

    except Exception as ex:
        print ex
        pass

    area_names = request.GET.getlist('area_names', [])

    topojson_geographies = []
    for topojson in settings.TOPOJSON_OPTIONS:
        topojson_geographies.append({
            'name': topojson['name'],
            'geog_short_code': topojson['geog_short_code'],
        })

    remote_layer_ids = request.GET.getlist('remote_layer_ids', [])
    remote_layer_data, local_layer_data = get_remote_layer_render_data_for_uid(
        remote_layer_ids,
        get_request_user(request)
    )

    remote_data_layers = []
    remote_data_ids = request.GET.getlist('rd_ids', [])
    remote_data_sources = request.GET.getlist('rd_srcs', [])

    if len(remote_data_ids) == len(remote_data_sources):
        for count, data in enumerate(remote_data_ids):
            remote_data_layers.append(
                {
                    'id': remote_data_ids[count],
                    'src': remote_data_sources[count]
                }
            )


    # TODO remove hard coded uids especially if they're not unique
    naw_key_searches = [
        # {
        #     'uid': '40d5be16-c11f-43b2-9c29-45555dc07945',
        #     'description': 'A quick postcode'
        # }, {
        #     'uid': '147b3009-5ce0-42ce-940e-38d594bf53be',
        #     'description': 'Another layer'
        # }
    ]
    naw_key_searches.extend(settings.NAW_SEARCH_LAYER_UUIDS)

    m4w_key_searches = []
    m4w_key_searches.extend(settings.M4W_SEARCH_LAYER_UUIDS)

    use_welsh = False
    user_prefs = get_user_preferences(request)
    assert isinstance(user_prefs, models.UserPreferences)
    if user_prefs.preferred_language:
        if user_prefs.preferred_language.user_language_title == 'Welsh':
            use_welsh = True

    if get_language() == 'cy':
        use_welsh = True

    if naw:
        if use_welsh:
            layer_uuids.extend(NAW_CY_LAYER_UUIDS)
        else:
            layer_uuids.extend(NAW_LAYER_UUIDS)

    return render(request, 'map.html',
                  {
                      'tpt': tpt,
                      'naw': naw,
                      'template_name': template_name,
                      'use_template': use_template,
                      'naw_key_searches': naw_key_searches,
                      'm4w_key_searches': m4w_key_searches,
                      'local_data_layers': local_data_layers,
                      'remote_searches': remote_layer_data,
                      'local_searches': local_layer_data,
                      'layer_uuids': layer_uuids,
                      'topojson_geographies': topojson_geographies,
                      'preferences': get_user_preferences(request),
                      'use_welsh': use_welsh,
                      'searches': get_user_searches(request),
                      'surveys': json.dumps(surveys),
                      'wms_layers': wms_layers,
                      'wiserd_layers': settings.KNOWING_LOCALITIES_TABLES,
                      'brexit_layers': settings.BREXIT_LAYERS,
                      'ge_layers': settings.GE_LAYERS,
                      'upload_layers': uploaded_layers_clean,
                      'area_names': json.dumps(area_names),
                      'remote_data_layers': remote_data_layers
                  },
                  context_instance=RequestContext(request))


def get_remote_layer_render_data_for_uid(nomissearch_uids, request_user):
    remote_layer_data = []
    local_layer_data = []

    remote_searches = models.NomisSearch.objects.filter(uuid__in=nomissearch_uids, user=request_user)

    for remote_layer_model in remote_searches:
        codelist = []
        for code in remote_layer_model.search_attributes:
            codelist.append({
                'option': code,
                'variable': remote_layer_model.search_attributes[code]
            })

        print remote_layer_model.display_attributes

        point_icon = ''
        if 'point_icon' in remote_layer_model.display_attributes:
            point_icon = remote_layer_model.display_attributes['point_icon']

        layer_data = {
            'bin_num': remote_layer_model.display_attributes['bin_num'],
            'bin_type': remote_layer_model.display_attributes['bin_type'],
            'colorpicker': remote_layer_model.display_attributes['colorpicker'],
            'point_icon': point_icon,
            'codelist': codelist,
            'geography_id': remote_layer_model.geography_id,
            'uuid': remote_layer_model.uuid,
            'name': remote_layer_model.name,
            'dataset_id': remote_layer_model.dataset_id
        }

        if remote_layer_model.search_type is None:
            search_type = 'Nomis'
        else:
            search_type = remote_layer_model.search_type.name

        layer_data['source'] = search_type

        if search_type == 'Nomis':
            remote_layer_data.append(layer_data)

        if search_type == 'StatsWales':
            remote_layer_data.append(layer_data)

        if search_type == 'Survey':
            local_layer_data.append(layer_data)

    # print 'local_layer_data', local_layer_data
    # print 'remote_layer_data', remote_layer_data

    return remote_layer_data, local_layer_data


def question(request, question_id):
    # print request.user
    # user = auth.get_user(request)
    # if type(user) is AnonymousUser:
    #     user = get_anon_user()
    # user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)

    user_profile = get_request_user(request)
    search, created = models.Search.objects.using('new').get_or_create(user=user_profile, query=question_id, type='question')
    search.save()

    return render(request, 'question_detail.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'question_id': question_id
                  },
                  context_instance=RequestContext(request))


@csrf_exempt
def edit_metadata(request):
    print 'get', request.GET

    # assume failure
    edit_metadata_response = {
        'success': False
    }

    try:
        # probably only want to allow actions on things the user owns
        user = auth.get_user(request)
        if type(user) is AnonymousUser:
            user = get_anon_user()
        user_profile = models.UserProfile.objects.using('new').get(user=user)

        function = request.GET.get('function', None)

        # User will need the searches UID and a new name for it
        if function == 'edit_search_name':
            search_uid = request.GET.get('search_uid', None)
            if search_uid:
                search = models.Search.objects.using('new').get(user=user_profile, uid=search_uid)
                new_name = request.GET.get('new_name', None)
                if new_name:
                    search.readable_name = new_name
                    search.save()
                    edit_metadata_response['success'] = True

        if function == 'set_user_preferences':

            request_user = get_request_user(request)
            request_user.institution = request.GET.get('institution', '')
            request_user.specialty = request.GET.get('specialty', '')
            request_user.sector = request.GET.get('sector', '')
            request_user.comments = request.GET.get('comments', '')
            check_enable_naw = request.GET.get('check_enable_naw', '')
            if check_enable_naw:
                request_user.role = 'naw'
            else:
                # Forms don't send unchecked checkboxes
                request_user.role = 'regular'

            request_user.init_user = True
            request_user.save()

            user_prefs = get_user_preferences(request)
            if 'links_new_tab' in request.GET:
                user_prefs.links_new_tab = True
            else:
                user_prefs.links_new_tab = False

            if 'topojson_high' in request.GET:
                user_prefs.topojson_high = True
            else:
                user_prefs.topojson_high = False

            if 'user_language' in request.GET:
                try:
                    user_prefs.preferred_language = models.UserLanguage.objects.get(
                        id=request.GET.get('user_language')
                    )
                except:
                    # No appropriate language found, default English
                    user_prefs.preferred_language = models.UserLanguage.objects.get(user_language_title='English')

            else:
                # No language given, default English
                user_prefs.preferred_language = models.UserLanguage.objects.get(user_language_title='English')

            user_prefs.save()
            set_session_preferred_language(request)
            edit_metadata_response['success'] = True

    # Any failure in here results in sending the success as being False, as set above
    # Add whatever the error message is here. Used in debugging, ideally should not be shown to user
    except Exception as e:
        print e
        edit_metadata_response['error'] = str(e)

    return HttpResponse(json.dumps(edit_metadata_response, indent=4), content_type="application/json")


@csrf_exempt
def get_imported_feature(request):

    rd = RemoteData()
    a = rd.get_test_data('van', 'parl2011')
    a = json.dumps(a, indent=4)
    return HttpResponse(a, content_type="application/json")

    # with open('/home/ubuntu/shp/x_sid_liw2007_fire_/output-fixed.json', 'r') as output:
    # with open('/home/ubuntu/shp/x_sid_liw2007_lsoa_/output-fixed-0.1.json', 'r') as output:

    # with open('/home/ubuntu/shp/x_sid_liw2007_pcode_/output-fixed-ms.json', 'r') as output:
    #     a = output.read()

    # final = json.dumps(topojson, indent=4)

    wiserd_layer = request.POST.getlist('layer_names[]')[0]

    spatial_table_name = str(wiserd_layer).replace('_', '').strip()

    feature_collection = models.FeatureCollectionStore.objects.get(
        id=spatial_table_name
    )

    feature_collection_features = feature_collection.featurestore_set.all()

    if True:
        print 'easy one'
        end_result = serialize('geojson',
                               feature_collection_features,
                               geometry_field='geometry')
        end_result = json.loads(end_result)
        end_result['properties'] = {'name': feature_collection.name}

    else:
        print 'going the hard way'
        fs = []
        for feature in feature_collection_features:
            # g = GEOSGeometry(feature.geometry.geojson)
            shape_list_group = {
                'type': 'Feature',
                'geometry': {
                    'type': 'MultiPolygon',
                    'coordinates': json.loads(
                        # g.simplify(0.2 ).geojson
                        feature.geometry.geojson
                    )
                },
                'properties': {
                    'feature_attributes': feature.feature_attributes,
                    "name": feature.name
                }
            }
            fs.append(shape_list_group)

        geojson_feature = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "EPSG:4326"
                }
            },
            "features": fs,
            "properties": {
                'name': spatial_table_name
            }
        }
        end_result = geojson_feature

    final = json.dumps(end_result, indent=4)
    return HttpResponse(final, content_type="application/json")


def get_wiserd_layer_topojson(
        layer_type,
        wiserd_layer,
        app_label,
        layer_field,
        update_cache,
        remote_value_filter):
    # from topojson import topojson

    # spatial_table_name = str(wiserd_layer).replace('_', '').strip()

    layer_key = '{}-{}-{}-{}-{}'.format(layer_type, app_label, wiserd_layer, layer_field, remote_value_filter)

    redis_cached_data = None
    if not update_cache:
        try:
            redis_cached_data = redis_cache.get(layer_key)
        except:
            redis_cached_data = None

    if redis_cached_data:
        s = redis_cached_data

    else:
        if wiserd_layer == 'TaxServicePropertyInformation':
            wiserd_layer_model = apps.get_model(
                app_label='scrape',
                model_name=wiserd_layer
            )
            shape_table_object = wiserd_layer_model.objects.filter(
                Q(lsoa_name__contains='Cardiff 032A') |
                Q(lsoa_name__contains='Cardiff 032C') |
                Q(lsoa_name__contains='Cardiff 032D') |
                Q(lsoa_name__contains='Cardiff 032E') |
                Q(lsoa_name__contains='Cardiff 032F') |
                Q(lsoa_name__contains='Cardiff 032G') |

                Q(lsoa_name__contains='Cardiff 033A') |
                Q(lsoa_name__contains='Cardiff 033B') |
                Q(lsoa_name__contains='Cardiff 033C') |
                Q(lsoa_name__contains='Cardiff 033D') |

                Q(lsoa_name__contains='Cardiff 036A') |
                Q(lsoa_name__contains='Cardiff 036B') |
                Q(lsoa_name__contains='Cardiff 036C') |
                Q(lsoa_name__contains='Cardiff 036D') |

                Q(lsoa_name__contains='Cardiff 042A') |
                Q(lsoa_name__contains='Cardiff 042B') |
                Q(lsoa_name__contains='Cardiff 042C') |
                Q(lsoa_name__contains='Cardiff 042D') |

                Q(lsoa_name__contains='Cardiff 044A') |
                Q(lsoa_name__contains='Cardiff 044B') |
                Q(lsoa_name__contains='Cardiff 044C') |
                Q(lsoa_name__contains='Cardiff 044D') |

                Q(lsoa_name__contains='Cardiff 046A') |
                Q(lsoa_name__contains='Cardiff 046B') |
                Q(lsoa_name__contains='Cardiff 046C') |
                Q(lsoa_name__contains='Cardiff 046D') |

                # Q(lsoa_name__contains='Cardiff 048A') |
                # Q(lsoa_name__contains='Cardiff 048B') |
                Q(lsoa_name__contains='Cardiff 048C') |
                Q(lsoa_name__contains='Cardiff 048D') |
                Q(lsoa_name__contains='Cardiff 048E') |

                Q(lsoa_name__contains='Cardiff 049A') |
                Q(lsoa_name__contains='Cardiff 049B') |
                Q(lsoa_name__contains='Cardiff 049C') |
                Q(lsoa_name__contains='Cardiff 049D') |
                Q(lsoa_name__contains='Cardiff 049E') |
                Q(lsoa_name__contains='Cardiff 049F') |

                Q(lsoa_name__contains='Cardiff 005G')

            )
            print 'shape_table_object', shape_table_object.count()

        elif wiserd_layer == 'SchoolData':
            wiserd_layer_model = apps.get_model(
                app_label='dataportal3',
                model_name=wiserd_layer
            )
            shape_table_object = wiserd_layer_model.objects.filter(LEANameEnglish__contains='Cardiff')
            print 'shape_table_object', shape_table_object.count()

        elif wiserd_layer == 'SpatialdataLSOA':
            wiserd_layer_model = apps.get_model(
                app_label='dataportal3',
                model_name=wiserd_layer
            )
            shape_table_object = wiserd_layer_model.objects.filter(name__contains='Cardiff')
            print 'shape_table_object', shape_table_object.count()

        else:

            print("Looking for table {} in {}".format(wiserd_layer, app_label))

            wiserd_layer_model = apps.get_model(
                app_label=app_label,
                model_name=wiserd_layer
            )

            print remote_value_filter
            if remote_value_filter:
                variable_column = layer_field
                search_type = 'exact'
                filter = variable_column + '__' + search_type
                shape_table_object = wiserd_layer_model.objects.filter(**{filter: remote_value_filter})
                # print shape_table_object.query
            else:
                shape_table_object = wiserd_layer_model.objects.all()

        # shape_list = shape_table_object.extra(
        #     select={
        #         'geometry': 'ST_AsGeoJSON(ST_Transform(ST_SetSRID("geom", 27700),4326))'
        #     }
        # ).values('geometry')

        s = GeoJSONSerializer().serialize(
            shape_table_object,
            use_natural_keys=True,
            with_modelname=False,
            simplify=0.00005
        )

        try:
            redis_cache.set(layer_key, s)
        except:
            pass

    geo = json.loads(s)
    # geo = geojson_points_to_topojson(geo)

    #
    # geo = topojson(
    #     geo,
    #     quantization=1e4,
    #     # simplify=0.0005
    # )

    geo['properties'] = {'name': wiserd_layer}
    # if wiserd_layer == 'SchoolData':
    #     geo['properties']['remote_value_key'] = 'fsm_percent'
    #     # geo['properties']['remote_value_key'] = 'schTypeEnglish'

    # if wiserd_layer == 'TaxServicePropertyInformation':
    #     geo['properties']['remote_value_key'] = 'building_type'

    if layer_field:
        geo['properties']['remote_value_key'] = layer_field

    geos = json.dumps(geo)
    return geos


@csrf_exempt
def get_geojson(request):

    print request.POST

    # time1 = datetime.now()
    layer_type = request.POST.get('layer_type')
    app_label = request.POST.get('app_label', 'dataportal3')
    layer_field = request.POST.get('field', None)
    update_cache = request.POST.get('update_cache', None)

    if layer_type == 'wiserd_layer':
        wiserd_layer = request.POST.getlist('layer_names[]')[0]

        geos = get_wiserd_layer_topojson(
            layer_type,
            wiserd_layer,
            app_label,
            None,
            update_cache,
            None
        )

        return HttpResponse(geos, content_type="application/json")

    if layer_type == 'survey':
        surveys = request.POST.getlist('layer_names[]')
        print surveys, type(surveys)

        area_names = request.POST.getlist('area_names[]')

        print surveys

        q_obj_sids = [Q(surveyid__istartswith=sid) for sid in surveys]
        qs = reduce(operator.or_, q_obj_sids)
        spatial_link_query = models.SurveySpatialLink.objects.using('survey').filter(qs)
        print spatial_link_query.query

        spatial_links = spatial_link_query.values('spatial_id', 'admin_areas', 'surveyid')
        # shape_table_object = models.XSidLiwhh2005Ua.objects.using('survey_gis').all()
        if spatial_links.count() > 0:
            spatial_link = spatial_links[0]
            spatial_table_name = str(spatial_link['spatial_id']).replace('_', '').strip()
            spatial_table = apps.get_model(
                app_label='old',
                model_name=spatial_table_name
            )
            shape_table_object = spatial_table.objects.using('survey_gis').all()

            geojson_layers = shape_table_object.extra(
                select={
                    'geometry': 'ST_AsGeoJSON("the_geom")'
                }
            ).values('area_name', 'response_rate', 'geometry')

            if len(area_names):
                print 'area_names', area_names
                geojson_layers = geojson_layers.filter(area_name__in=area_names)

            print area_names

            # print type(geojson_layers)
            # shape_list = list(geojson_layers)
            shape_list = geojson_layers
            print geojson_layers.query


    # print shape_list
    # print type(shape_list[0])

    # time2 = datetime.now()
    # print time2 - time1

    shape_feature_list = [
        # {
        #     "type": "Feature",
        #     "geometry": {
        #         "type": "Point",
        #         "coordinates": [-3.5, 51.5]
        #     },
        #     "properties": {
        #         "name": "null island",
        #         "marker-symbol": "bus"
        #     }
        # }
    ]

    for shape in shape_list:

        shape_properties = {}
        for key in shape:
            if key is not 'geometry':
                shape_properties[key] = shape[key]
                # print shape[key], shape_properties[key]

        if 'response_rate' in shape_properties:
            print shape_properties['response_rate'], type(shape_properties['response_rate'])
            rgb_int = float(shape_properties['response_rate']) * 2.54
            rgb_tuple = (rgb_int, rgb_int, rgb_int)
            hex_code = '#%02x%02x%02x' % rgb_tuple
            shape_properties['color'] = hex_code
            shape_properties['opacity'] = 0.1

        # print datetime.now() - time2

        # print shape
        shape_list_group = {
            'type': 'Feature',
            'geometry': {
                'type': 'MultiPolygon',
                # 'coordinates': ast.literal_eval(shape['geometry'])['coordinates']
                'coordinates': json.loads(shape['geometry'])['coordinates']
                # 'coordinates': shape['geometry']

            },
            'properties': shape_properties
        }

        shape_feature_list.append(shape_list_group)

    # print datetime.now() - time2
    geojson_feature = {
        "type": "FeatureCollection",
        "features": shape_feature_list,
        "properties": {
            'name': spatial_table_name
        }
    }
    end_result = json.dumps(geojson_feature)
    # print datetime.now() - time1
    return HttpResponse(end_result, content_type="application/json")


def file_management(request):

    user_shapefiles = models.ShapeFileUpload.objects.filter(user=get_request_user(request))

    return render(request, 'file_management.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'user_shapefiles': user_shapefiles,
                      'shapefile_form': ShapefileForm()
                  },
                  context_instance=RequestContext(request))


# TODO dont be csrf exempt, check logged in
# @csrf_exempt
def upload_shapefile(request):
    print request.POST
    print request.FILES
    print len(request.FILES)

    messages = []
    user = get_request_user(request)
    print user
    zip_file = request.FILES['file']
    print zip_file
    filename = request.POST.get('shapefile_name', '')
    print filename

    shapefile_upload = models.ShapeFileUpload()
    shapefile_upload.user = user
    shapefile_upload.uuid = str(uuid.uuid4())
    shapefile_upload.shapefile = zip_file
    shapefile_upload.name = filename
    shapefile_upload.progress = ShapeFileImport.progress_stage['init']
    shapefile_upload.save()

    celery_key = celery_import.delay(
        user_id=user.id,
        zip_file=None,
        filename=filename,
        shapefile_upload_id=shapefile_upload.id
    )

    return render(request, 'file_management.html',
                  {
                      'preferences': get_user_preferences(request),
                      'messages': messages,
                      'shapefile_form': ShapefileForm(),
                      'searches': get_user_searches(request)
                  },
                  context_instance=RequestContext(request))

# @csrf_exempt
# def get_upload_progress(request):
#     cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], request.GET['X-Progress-ID'])
#     data = cache.get(cache_key)
#     return HttpResponse(json.dumps(data))


def shapefile_list(request):
    return render(request, 'file_management.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  },
                  context_instance=RequestContext(request))


@csrf_exempt
def new_spatial_search(request):

    geo_wkt = request.POST.getlist('geography', '')

    #  OSGB WGS84
    #     ct = CoordTransform(SpatialReference('27700'), SpatialReference('4326'))
    #     ct = CoordTransform(SpatialReference('EPSG:27700'), SpatialReference('EPSG:4326'))
    # geom = GEOSGeometry(geojson[0], srid=27700).transform(ct)

    geom = GEOSGeometry(geo_wkt[0], srid=27700)

    response_data = {
        'data': []
    }
    search_uid = ''
    survey_info = {}

    response_data['success'] = True
    response_data['uid'] = search_uid

    response_data['data'] = survey_info.values()

    search = models.Search()
    search.user = get_request_user(request)
    search.query = geo_wkt
    search.type = 'spatial'
    search.image_png = request.POST.get('image_png', None)
    search.save()

    search_uid = str(search.uid)
    response_data['uid'] = search_uid

    uid_only = request.POST.get('uid_only', False)
    # if uid_only:
    #     # we only record what was searched for, do not complete the search yet
    #     pass
    # else:

    spatial_intersects = models.FeatureStore.objects.filter(geometry__intersects=geom)
    response_data['data'] = list(spatial_intersects.values('name', 'feature_collection__name'))
    print response_data['data']

    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def logout(request):
    logout_success = False
    msg = 'Auth Error, please refresh the page'
    if request.user.is_authenticated():
        auth.logout(request)
        msg = 'You have successfully logged out'
        logout_success = True
    #do logout
    return render(request, 'dashboard.html',
                  {'logout_success': logout_success, 'msg': msg},
                  context_instance=RequestContext(request))


def get_nomis_searches(request):
    userr = get_request_user(request)
    return models.NomisSearch.objects.filter(user=userr).order_by('-datetime')


def profile(request):
    userr = get_request_user(request)
    return render(request, 'profile.html',
                  {
                      'languages': models.UserLanguage.objects.all(),
                      'nomis_layers': get_nomis_searches(request),
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'userr': userr,
                      'userr_dict': userr.__dict__,
                  },context_instance=RequestContext(request))

# TODO way too casual
@csrf_exempt
def data_api(request):
    rd = RemoteData()
    to_return = {}
    print request.GET

    method = request.GET.get("method", None)
    if method is None:
        method = request.POST.get("method", None)

    if method == 'topojson_layer_by_name':
        topojson_name = request.GET.get("name", None)
        to_return = get_topojson_by_name(request, topojson_name)

    if method == 'search_layer_topojson':
        search_uuid = request.GET.get("search_uuid", None)
        to_return = get_topojson_for_uuid(request, search_uuid)

    # This takes a list of fields from a layer described by an uploaded shapefile
    # The layer will have been searched for and displayed, and can be edited for content here
    # The selected fields are to show in the layer when rendered in future
    if method == 'update_hidden_fields':
        search_uuid = request.POST.get("search_uuid", None)
        selected_fields = request.POST.getlist("selected_fields[]", [])
        all_fields = request.POST.getlist("all_fields[]", [])

        display_dict = {}
        for field in all_fields:
            if field in selected_fields:
                display_dict[field] = True
            else:
                display_dict[field] = False

        search_object = models.NomisSearch.objects.get(uuid=search_uuid)
        search_object.display_fields = display_dict
        search_object.save()

        to_return = [display_dict]

    if method == 'remote_search':

        search_term = request.GET.get("search_term", None)
        print type(search_term), search_term

        if search_term == u'health_hack':
            # TODO remove
            print 'shortcut'

            json_hack = {
                "services": [
                    {
                        "message": "Success",
                        "name": "StatsWales",
                        "success": True,
                        "time": 1.343425
                    },
                    {
                        "message": "Success",
                        "name": "NomisWeb",
                        "success": True,
                        "time": 2.178326
                    },
                    {
                        "message": "Success",
                        "name": "DataHub",
                        "success": True
                    }
                ],
                "datasets": [
                    {
                        "source": "StatsWales",
                        "id": "HLTH1599",
                        "name": "Inequality gap in life expectancy and healthy life expectancy at birth (Slope Index of Inequality) in years by Local Health Board and Local Authority"
                    },
                    {
                        "source": "StatsWales",
                        "id": "HLTH1598",
                        "name": "Life expectancy and Healthy life expectancy at birth by Local Health Board and Local Authority"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0019",
                        "name": "WIMD 2014 Indicator Data - LSOA"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0031",
                        "name": "WIMD Indicator Data - RU"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0005",
                        "name": "WIMD Indicator Data - MSOA"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0004",
                        "name": "WIMD Indicator Data - LSOA"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0003",
                        "name": "WIMD Indicator Data - LA"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0020",
                        "name": "WIMD Indicator Data - LSOA"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0032",
                        "name": "WIMD 2014 Indicator Data - RU"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0036",
                        "name": "WIMD 2014 Indicator Data - LA"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0035",
                        "name": "WIMD Indicator Data - LSOA"
                    },
                    {
                        "source": "StatsWales",
                        "id": "HLTH1210",
                        "name": "Live births by Local Health Board of residence and place of birth"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0033",
                        "name": "WIMD 2014 Indicator Data - RU"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0030",
                        "name": "WIMD 2014 Indicator Data - CF"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0034",
                        "name": "WIMD Indicator Data - RU"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD1401",
                        "name": "WIMD 2014 Domain Ranks"
                    },
                    {
                        "source": "StatsWales",
                        "id": "wimd0038",
                        "name": "WIMD Indicator Data - RU"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0029",
                        "name": "WIMD 2014 Indicator Data - CF"
                    },
                    {
                        "source": "StatsWales",
                        "id": "WIMD0028",
                        "name": "WIMD Indicator Data - CF"
                    },
                    {
                        "source": "StatsWales",
                        "id": "HLTH1201",
                        "name": "Live births by mother's age and Local Health Board"
                    },
                    {
                        "source": "StatsWales",
                        "id": "HLTH1203",
                        "name": "Live births by birth weight and Local Health Board"
                    },
                    {
                        "source": "StatsWales",
                        "id": "HLTH1202",
                        "name": "Live births by gestational age and Local Health Board"
                    },
                    {
                        "source": "StatsWales",
                        "id": "HLTH1207",
                        "name": "Breastfeeding status at birth, live births to Welsh residents"
                    },
                    {
                        "source": "StatsWales",
                        "id": "HLTH1208",
                        "name": "Live births to Welsh residents by place of birth and Local Health Board (place of birth, Local Health Board)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_29_1",
                        "name": "vat registrations/deregistrations by industry"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_531_1",
                        "name": "QS302EW - General health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_532_1",
                        "name": "QS303EW - Long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_606_1",
                        "name": "KS106EW - Adults not in employment and dependent children and persons with long-term health problems or disability for all households"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_617_1",
                        "name": "KS301EW - Health and provision of unpaid care"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_666_1",
                        "name": "DC2301EW - Ethnic group by provision of unpaid care by general health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_670_1",
                        "name": "DC3201EW - Long-term health problem or disability by general health by ethnic group by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_671_1",
                        "name": "DC3202WA - Long-term health problem or disability by general health by Welsh language skills by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_672_1",
                        "name": "DC3203EW - Long-term health problem or disability by general health by religion by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_673_1",
                        "name": "DC3301EW - Provision of unpaid care by general health by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_674_1",
                        "name": "DC3302EW - Long term health problem or disability by health by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_675_1",
                        "name": "DC3601EW - General health by NS-SeC by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_676_1",
                        "name": "DC3602EW - Long-term health problem or disability by NS-SeC by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_684_1",
                        "name": "DC6301EWla - Economic activity by provision of unpaid care by general health by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_685_1",
                        "name": "DC6302EW - Economic activity by hours worked by sex by long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_691_1",
                        "name": "DC3303EWr - Provision of unpaid care by general health by sex by age (regional)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_739_1",
                        "name": "DC3204EWr - General health by ethnic group by sex by age (regional)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_740_1",
                        "name": "DC3205EWr - Long-term health problem or disability by ethnic group by sex by age (regional)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_741_1",
                        "name": "DC6303EWr - NS-SeC by general health by sex by age (regional)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_742_1",
                        "name": "DC6304EWr - NS-SeC by long-term health problem or disability by sex by age (regional)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_758_1",
                        "name": "DC1301EW - Household composition by number of people in household with a long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_766_1",
                        "name": "DC2302EWr - Proficiency in English by general health by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_767_1",
                        "name": "DC2303EW - Proficiency in English by general health by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_780_1",
                        "name": "DC3304EWla - Long-term health problem or disability by general health by age - Communal establishment residents"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_781_1",
                        "name": "DC3401EWla - General health by communal establishment management and type by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_782_1",
                        "name": "DC3402EWla - Long-term health problem or disability by communal establishment management and type by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_816_1",
                        "name": "LC3202WA - General health by ability to speak Welsh by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_817_1",
                        "name": "LC3204WA - Long-term health problem or disability by ability to speak Welsh by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_822_1",
                        "name": "LC2301EW - Ethnic group by provision of unpaid care by general health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_823_1",
                        "name": "LC2303EW - Proficiency in English by general health by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_824_1",
                        "name": "LC3203EW - General health by religion by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_826_1",
                        "name": "LC3205EW - Long-term health problems by ethnic group by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_827_1",
                        "name": "LC3207EW - Long-term health problem or disability by religion by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_828_1",
                        "name": "LC3301EW - Provision of unpaid care by general health by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_829_1",
                        "name": "LC3302EW - Long-term health problem or disability by general health by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_831_1",
                        "name": "LC3601EW - General health by NS-SeC"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_832_1",
                        "name": "LC3602EW - Long-term health problem or disability by NS-SeC by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_833_1",
                        "name": "LC6301EW - Economic activity by provision of unpaid care by general health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_834_1",
                        "name": "LC6302EW - Economic activity by hours worked by long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_835_1",
                        "name": "LC3206EW - General health by ethnic group by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_859_1",
                        "name": "LC1301EW - Household composition by number of people in household with a long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_913_1",
                        "name": "ST302EWla - General Health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_939_1",
                        "name": "WD302EW - General health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_988_1",
                        "name": "CT0067 - General health by year of arrival in the UK by country of birth by age (national)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_989_1",
                        "name": "CT0068 - General health by year of arrival in the UK by passports held by age (national)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1042_1",
                        "name": "LC5301EW - Highest level of qualification by long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1092_1",
                        "name": "LC3101EWls - Long term health problem or disability by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1097_1",
                        "name": "LC3403EW - General health by long-term health problem or disability by occupancy rating (rooms)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1098_1",
                        "name": "LC3404EW - General health by long-term health problem or disability by occupancy rating (bedrooms)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1099_1",
                        "name": "LC3405EW - General health by long-term health problem or disability by car or van availability by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1115_1",
                        "name": "DC5301EW - Highest level of qualification by long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1160_1",
                        "name": "DC3403EW - General health by long-term health problem or disability by occupancy rating (rooms) by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1161_1",
                        "name": "DC3404EW - General health by long-term health problem or disability by occupancy rating (bedrooms) by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1162_1",
                        "name": "DC3405EW - General health by long-term health problem or disability by car or van availability by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1163_1",
                        "name": "DC3407EW - Long-term health problem or disability by car or van availability by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1164_1",
                        "name": "DC3408EW - Long-term health problem or disability by tenure by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1165_1",
                        "name": "DC3409EW - General health by tenure by sex by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1167_1",
                        "name": "DC3306EW -  Provision of unpaid care by number of people in household with a long-term health problem or disability by economic activity by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1284_1",
                        "name": "UKMIG005 - Migration by long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1309_1",
                        "name": "WP302EW - General Health (Workplace population)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1362_1",
                        "name": "OT302EW - General health (Out of term-time population)"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1400_1",
                        "name": "LC3406EW - General health by car or van availability by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1403_1",
                        "name": "LC3408EW - Long-term health problem or disability by tenure by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1404_1",
                        "name": "LC3409EW - General health by tenure by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1405_1",
                        "name": "LC3305EW - Long-term health problem or disability by provision of unpaid care by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1406_1",
                        "name": "LC3407EW - Long-term health problem or disability by car or van availability by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1407_1",
                        "name": "LC3307EW - Provision of unpaid care by general health by households with people who have a long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1408_1",
                        "name": "LC3306EW - Provision of unpaid care by households with people with a long-term health problem or disability by economic activity by sex"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1410_1",
                        "name": "LC3102EW - Long-term health problem or disability by number of children in family"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1505_1",
                        "name": "KS301UK - Health and provision of unpaid care"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1546_1",
                        "name": "QS302UK - General health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1547_1",
                        "name": "QS303UK - Long-term health problem or disability"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1608_1",
                        "name": "KS008 - Health and provision of unpaid care"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1645_1",
                        "name": "UV020 - General health"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1716_1",
                        "name": "CS016 - Sex and age by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1717_1",
                        "name": "CS017 - Tenure and age by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1718_1",
                        "name": "CS018 - Sex and amenities and central heating by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1719_1",
                        "name": "CS019 - General health and limiting long-term illness and occupancy rating by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1722_1",
                        "name": "CS022 - Sex and number of cars or vans in household by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1723_1",
                        "name": "CS023 - Age and general health by NS-Sec"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1725_1",
                        "name": "CS025 - Sex and age by general health and provision of unpaid care"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1726_1",
                        "name": "CS026 - Sex and economic activity by general health and provision of unpaid care"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1765_1",
                        "name": "CS065 - Sex and age by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1816_1",
                        "name": "ST016 - Sex and age by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1817_1",
                        "name": "ST017 - Tenure and age by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1818_1",
                        "name": "ST018 - Sex and amenities and central heating by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1819_1",
                        "name": "ST019 - General health and limiting long-term illness and occupancy rating by age"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1822_1",
                        "name": "ST022 - Sex and number of cars in household by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1823_1",
                        "name": "ST023 - Sex and age and general health by NS-SeC"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1825_1",
                        "name": "ST025 - Sex and age by general health and provision of unpaid care"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1826_1",
                        "name": "ST026 - Sex and economic activity by general health and provision of unpaid care"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1865_1",
                        "name": "ST065 - Sex and age by general health and limiting long-term illness"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1875_1",
                        "name": "ST107 - Sex and age and limiting long-term illness and general health by ethnic group"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1905_1",
                        "name": "ST137 - Sex and age and limiting long-term illness and general health by knowledge of Welsh"
                    },
                    {
                        "source": "Nomis",
                        "id": "NM_1920_1",
                        "name": "ST152 - Sex and age and limiting long-term illness and general health by religion"
                    },
                    {
                        "source": "CKAN_datahub",
                        "id": "059f7dd7-ca00-48e4-b291-46ef167cf2fc",
                        "name": "lsoa mapped data"
                    },
                    {
                        "source": "CKAN_datahub",
                        "id": "650200e9-cfad-4efa-9fbf-cf35483b1e36",
                        "name": "wimd2014"
                    }
                ]
            }
            return HttpResponse(json.dumps(json_hack), content_type="application/json")
        else:
            print 'health not ==', search_term

        remote_api = request.GET.get("remote_api", None)

        # print search_term
        if search_term:
            datasets = []
            services = []

            stats_wales_service = {
                'name': 'StatsWales'
            }
            try:
                swod = StatsWalesOData()
                swod_datasets, statswales_request = swod.keyword_search(search_term.lower())

                # formatted = []
                # for d in swod_datasets:
                #     if d['Tag_ENG'] == 'Title':
                #         formatted.append({
                #             'id': d['Dataset'],
                #             'name': d['Description_ENG'],
                #             'source': 'StatsWales'
                #         })
                # datasets += formatted

                datasets += swod_datasets

                stats_wales_service['message'] = 'Success'
                stats_wales_service['time'] = statswales_request.elapsed.total_seconds()
                stats_wales_service['success'] = True
            except Exception as e87234:
                stats_wales_service['message'] = 'The WISERD DataPortal failed to connect to the remote data service.'
                stats_wales_service['error'] = (str(e87234), str(type(e87234)))
                stats_wales_service['success'] = False
            services.append(stats_wales_service)

            nomis_service = {
                'name': 'NomisWeb'
            }
            try:
                nomis_datasets, nomis_request = rd.search_datasets(search_term)
                datasets += nomis_datasets
                nomis_service['message'] = 'Success'
                nomis_service['time'] = nomis_request.elapsed.total_seconds()
                nomis_service['success'] = True
            except Exception as e53264:
                nomis_service['message'] = 'The WISERD DataPortal failed to connect to the remote data service.'
                nomis_service['error'] = str(e53264)
                nomis_service['success'] = False
            services.append(nomis_service)

            datahub_service = {
                'name': 'DataHub'
            }
            try:
                ckan_data = CKANdata()
                ckan_datasets, ckan_request = ckan_data.keyword_search(search_term.lower())
                datasets += ckan_datasets
                datahub_service['message'] = 'Success'
                # datahub_service['time'] = ckan_request.elapsed.total_seconds()
                datahub_service['success'] = True
            except Exception as e87234:
                datahub_service['message'] = 'The WISERD DataPortal failed to connect to the remote data service.'
                datahub_service['error'] = str(e87234)
                datahub_service['success'] = False
            services.append(datahub_service)

            to_return['services'] = services
            to_return['datasets'] = datasets

    if method == 'remote_metadata':
        dataset_id = request.GET.get("dataset_id", None)
        source = request.GET.get("source", None)

        if source == 'Nomis':
            to_return['metadata'] = rd.get_dataset_overview(dataset_id)
        if source == 'StatsWales':
            swod = StatsWalesOData()
            to_return['metadata'] = swod.get_dataset_overview(dataset_id)
        if source == 'CKAN_datahub':
            ckan_data = CKANdata()
            to_return['metadata'] = ckan_data.get_dataset_overview(dataset_id)

    if method == 'remote_data_render_data':
        remote_layer_ids = request.GET.getlist('remote_layer_ids[]', [])
        remote_layer_data = get_remote_layer_render_data_for_uid(remote_layer_ids, get_request_user(request))
        to_return['nomis_layers'] = remote_layer_data

    if method == 'record_nomis_search':
        layer_id = request.GET.get("layer_id", None)
        layer_name = request.GET.get("layer_name", '')
        if layer_id:
            display_dict = {
                'bin_type': request.GET.get("bin_type", ''),
                'bin_num': request.GET.get("bin_num", ''),
                'colorpicker': request.GET.get("colorpicker", ''),
                'point_icon': request.GET.get("point_icon", '')

            }

            search_object = models.NomisSearch.objects.get(uuid=layer_id)
            search_object.display_attributes = display_dict
            search_object.name = layer_name
            search_object.save()

    if method == 'local_data_metadata':
        survey_id = request.GET.get("survey_id", None)
        boundary = request.GET.get("boundary_name", None)
        print survey_id, boundary

        link_table_data = models.SpatialSurveyLink.objects.filter(
            survey__identifier=survey_id,
            boundary_name=boundary
        )
        # print link_table_data.query

        data_names = link_table_data.exclude(
            data_type='unicode'
            # ).values_list('data_name', flat=True)
        ).values('data_name', 'full_name')

        unicode_data_names = link_table_data.filter(
            data_type='unicode'
            # ).values_list('data_name', flat=True)
        ).values('data_name', 'full_name')

        to_return['local_data_metadata'] = {
            'data_names': list(data_names),
            'unicode_data': list(unicode_data_names)
        }

    if method == 'data_urls':
        codelist = None
        codelist_json = request.GET.get('codelist_selected', None)
        if codelist_json:
            codelist = json.loads(codelist_json)
            print pprint.pformat(codelist)

        dataset_id = request.GET.get('dataset_id', '')
        nomis_variable = request.GET.get('nomis_variable', '')
        geog = request.GET.get('geography', '')
        print dataset_id, nomis_variable, geog

        region_id, topojson_file = rd.get_dataset_geodata(geog, high=False)
        dataset_url, dataset_file = rd.get_dataset_url(dataset_id, region_id, '', codelist)

        to_return['data_urls'] = {
            'dataset_url': dataset_url,
            'dataset_url_csv': dataset_url.replace('.json', '.csv')
        }

    return HttpResponse(json.dumps(to_return, indent=4), content_type="application/json")


def codelist_to_attributes(codelist):
    code_dict = {}
    for code in codelist:
        try:
            code_dict[code['option']] = code['variable']
        except:
            raise Exception(code)
    return code_dict


def remote_data_topojson(request):
    # print request.GET

    codelist = None
    codelist_json = request.GET.get('codelist_selected', None)
    if codelist_json:
        codelist = json.loads(codelist_json)
        print pprint.pformat(codelist)

    dataset_id = request.GET.get('dataset_id', '')
    nomis_variable = request.GET.get('nomis_variable', '')
    geog = request.GET.get('geography', '')
    source = request.GET.get('source', '')
    print dataset_id, nomis_variable, geog

    user_prefs = get_user_preferences(request)

    nomis_search = models.NomisSearch()
    nomis_search.uuid = str(uuid.uuid4())
    nomis_search.user = get_request_user(request)
    nomis_search.dataset_id = dataset_id
    nomis_search.geography_id = geog
    nomis_search.search_attributes = codelist_to_attributes(codelist)
    nomis_search.search_type = models.SearchType.objects.get(name=source)
    nomis_search.save()

    if source == 'Nomis':
        rd = RemoteData()
        a = rd.get_topojson_with_data(dataset_id, geog, nomis_variable, codelist, high=user_prefs.topojson_high)

    if source == 'CKAN_datahub':
        ckan_data = CKANdata()

        filter_options = []
        for code in codelist:
            option = str(code['option']).replace(' ', '') + '_Code'
            variable = code['variable']
            filter_options.append([option, variable])

        all_data = ckan_data.get_data_dict(
            str(dataset_id).lower(),
            filter_options,
            {'SEARCH_UUID': nomis_search.uuid}
        )

        rd = RemoteData()
        region_id, topojson_file = rd.get_dataset_geodata(geog, user_prefs.topojson_high)
        a = rd.update_topojson(topojson_file, all_data, measure_is_percentage=False)

    if source == 'StatsWales':
        swod = StatsWalesOData()
        filter_option_data_types = swod.get_metadata_for_dataset(dataset_id)

        filter_options = []
        for code in codelist:
            option = str(code['option']).replace(' ', '') + '_Code'
            variable = code['variable']

            if filter_option_data_types[option] == 'Edm.Int64':
                variable = int(variable)

            filter_options.append([option, swod.equals_conditional, variable])

        all_data = swod.get_data_dict(
            str(dataset_id).lower(),
            filter_options,
            {'SEARCH_UUID': nomis_search.uuid}
        )

        rd = RemoteData()
        region_id, topojson_file = rd.get_dataset_geodata(geog, user_prefs.topojson_high)
        a = rd.update_topojson(topojson_file, all_data, measure_is_percentage=False)

    to_return = {
        'topojson': a,
        'search_uuid': nomis_search.uuid
    }
    to_return_json = json.dumps(to_return, indent=4)

    return HttpResponse(to_return_json, content_type="application/json")


def local_data_topojson(request):
    print request.GET
    survey_id = request.GET.get('survey_id', '')
    boundary_name = request.GET.get('boundary_name', '')
    # data_name = request.GET.get('data_name_todo', 'TotEle2015')
    data_name = request.GET.get('data_name', 'response_rate')
    # data_name = request.GET.get('data_name_todo', 'TrnOut2010')

    print 'survey_id', survey_id, type(survey_id)
    print 'boundary_name', boundary_name, type(boundary_name)
    print 'data_name', data_name, type(data_name)

    # From the human readable name, we want to access the shortcode
    geog = ''
    for geom in geometry_columns:
        if 'name' in geom:
            if boundary_name in geom['name']:
                if 'geog_short_code' in geom:
                    geog = geom['geog_short_code']
    print 'geog found', geog

    # if boundary_name == 'Unitary Authority':
    #     geog = 'ua'
    # if boundary_name == 'Parliamentary':
    #     geog = 'parl2011'
    # if boundary_name == 'Post Code':
    #     geog = 'pcode'

    all_data = {}

    survey_spatial_data = models.SpatialSurveyLink.objects.filter(
        survey__identifier=survey_id,
        boundary_name=boundary_name,
        data_name=data_name
    )
    # print type(survey_spatial_data)
    # print survey_spatial_data.count()
    # print survey_spatial_data.query

    survey_spatial_data_strings = models.SpatialSurveyLink.objects.filter(
        survey__identifier=survey_id,
        boundary_name=boundary_name,
        data_type='unicode'
    ).order_by('data_name')

    # TODO use get but check unique, at the moment we're just dropping data
    regional_data = survey_spatial_data[0].regional_data

    region_string_data = {}
    for region in regional_data:
        region_string_data[region] = []
        for data_strings in survey_spatial_data_strings:
            # For each region in this survey's SpatialSurveyLink,
            # build a string of the unicode data elements
            # name_of_data : value_of_data, "Title Cased"
            region_string_data[region].append({
                'title': str(data_strings.data_name).title(),
                'value': str(data_strings.regional_data[region]).title()
            })

        # Shorthand Name,Category,FullName,Notes,CategoryCY,FullNameCY,NotesCY
        spatial_survey_fields = [
            {
                'field': 'data_name',
                'name': 'Name'
            },
            {
                'field': 'category',
                'name': 'Category'
            },
            {
                'field': 'full_name',
                'name': 'Full Name'
            },
            {
                'field': 'notes',
                'name': 'Notes'
            },
            {
                'field': 'category_cy',
                'name': 'Category CY'
            },
            {
                'field': 'full_name_cy',
                'name': 'Full Name CY'
            },
            {
                'field': 'notes_cy',
                'name': 'Notes CY'
            }
        ]

        for spatial_survey_field in spatial_survey_fields:
            region_string_data[region].append({
                'title': spatial_survey_field['name'],
                'value': getattr(survey_spatial_data[0], spatial_survey_field['field'])
            })
            # print 'region_string_data', region_string_data

    for region in regional_data:
        regions = [{
            'name': '',
            'value': regional_data[region],
            "geography_id": '',
            "geography_code": '',
            "data_status": "A",
            "geography": region,
            "string_data": region_string_data[region],
            "data_title": data_name,
        }]

        all_data[region] = regions

    nomis_search = models.NomisSearch()
    nomis_search.uuid = str(uuid.uuid4())
    nomis_search.user = get_request_user(request)
    nomis_search.dataset_id = survey_id
    nomis_search.geography_id = geog
    nomis_search.search_attributes = codelist_to_attributes([
        {
            'option': 'data_name',
            'variable': data_name
        }
    ])
    nomis_search.search_type = models.SearchType.objects.get(name='Survey')
    nomis_search.save()

    rd = RemoteData()
    region_id, topojson_file = rd.get_dataset_geodata(geog, False)
    a = rd.update_topojson(topojson_file, all_data, False)

    to_return = {
        'topojson': a,
        'search_uuid': nomis_search.uuid
    }
    to_return_json = json.dumps(to_return, indent=4)

    return HttpResponse(to_return_json, content_type="application/json")


def search_qual_api(request):
    search_terms = request.GET.get('search_terms', '')

    # print request.user
    # user = auth.get_user(request)
    # if type(user) is AnonymousUser:
    #     user = get_anon_user()
    user_profile = get_request_user(request)
    # user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=userr)

    try:
        search, created = models.Search.objects.using('new').get_or_create(user=user_profile,
                                                                           query=search_terms,
                                                                           readable_name=search_terms,
                                                                           type='text')

    # FIXME Shouldn't happen, but apparently does. Ensure unique at database level? Drop duplicates?
    except MultipleObjectsReturned as mor:
        search = models.Search.objects.using('new').filter(user=user_profile,
                                                           query=search_terms,
                                                           readable_name=search_terms,
                                                           type='text')[0]

    search.save()

    api_data = qual_search(search_terms)
    api_data['url'] = request.get_full_path()

    # conn_queries = connections['new'].queries
    # print 'qual conn num end', len(conn_queries)
    # print 'survey queries', conn_queries

    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def qual_search(search_terms):

    fields = ['identifier']
    if search_terms:
        qual_models = models.QualTranscriptData.objects.filter(
            dc_info__qualcalais__value__icontains=search_terms
        ).distinct('identifier').prefetch_related('dc_info').values('identifier', 'pages', 'dc_info__title', 'dc_info__date', 'dc_info__tier', 'dc_info__description')
    else:
        qual_models = models.QualTranscriptData.objects.none()

    data = []
    for qual_model in qual_models:
        data.append(qual_model)

    api_data = {
        'fields': fields,
        'method': 'search_survey_question',
        'search_result_data': data,
        'results_count': len(data),
        'search_term': search_terms
    }
    return api_data


def qual_transcript(request, qual_id):
    print request.user
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)

    search, created = models.Search.objects.using('new').get_or_create(user=user_profile, query=qual_id, type='qual')
    search.save()

    transcript_title = models.QualTranscriptData.objects.get(identifier=qual_id)

    return render(request, 'qual_detail.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'qual_title': transcript_title.dc_info.title,
                      'qual_id': qual_id
                  },
                  context_instance=RequestContext(request))


@csrf_exempt
def qual_dc_data(request, qual_id):
    qual_dc_models = models.QualDcInfo.objects.all().filter(identifier=qual_id).values("identifier", "title", "creator", "subject", "description", "publisher", "contributor", "date", "type", "format", "source", "language", "relation", "coverage", "rights", "user_id", "created")

    quals = []
    for dc_model in qual_dc_models:
        quals.append({
            'data': dc_model,
            'qual_id': qual_id
        })
    api_data = {
        'url': request.get_full_path(),
        'method': 'qual_dc_data',
        'search_result_data': quals,
        'results_count': len(quals),
    }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


@csrf_exempt
def qual_metadata(request, qual_id):
    qual_trans_models = models.QualTranscriptData.objects.all().filter(identifier=qual_id)
    quals = []
    for qual_model in qual_trans_models:

        # print model_to_dict(qual_model)

        qual_details = {
            'data': model_to_dict(qual_model),
            'qual_id': qual_id
        }

        qual_calais = qual_model.dc_info.qualcalais_set.values('value', 'lat', 'lon', 'tagName', 'gazetteer','count')
        # print type(qual_calais), qual_calais
        qual_details['calais'] = list(qual_calais)

        quals.append(qual_details)

    api_data = {
        'url': request.get_full_path(),
        'method': 'qual_metadata',
        'search_result_data': quals,
        'results_count': len(quals),
    }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


@csrf_exempt
def spatial_search(request):
    # print request.POST

    test_available = False
    search_uid = ''

    response_data = {
        'data': []
    }

    geography_wkt = request.POST.get('geography', '')

    # A test set of data for if we don't want to wait for the DB
    if test_available and (len(request.POST.get('test', '')) or len(geography_wkt) == 0):
        response_data = {'data': [{'area': u'Wales', 'survey_short_title': u'WERS', 'date': '2005 / 04 / 30', 'survey_id': u'sid_wersmq2004', 'survey_id_full': u'sid_wersmq2004                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_412', 'survey_id_full': u'sid_whs2008_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': '', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_03', 'survey_id_full': u'sid_whs2007_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Gwent, Monmouthshire, South East Wales, NP152, South Wales, W01001581', 'survey_short_title': u'LiW Property', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwps2004', 'survey_id_full': u'sid_liwps2004                                                                                                                                                                                                                                                  ', 'areas': [u'NP152', u'Gwent', u'South East Wales', u'Monmouthshire', u'South Wales', u'W01001581']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_03', 'survey_id_full': u'sid_whs2009_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007aq', 'survey_id_full': u'sid_whs2007aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2005 / 09 / 30', 'survey_id': u'sid_whs0306aq', 'survey_id_full': u'sid_whs0306aq                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_03', 'survey_id_full': u'sid_whs2008_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008aq', 'survey_id_full': u'sid_whs2008aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_1315', 'survey_id_full': u'sid_whs2007_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2007 / 07 / 31', 'survey_id': u'sid_liw2007', 'survey_id_full': u'sid_liw2007                                                                                                                                                                                                                                                    ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire 005E', u'Monmouth', u'Gwent', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_1315', 'survey_id_full': u'sid_whs2008_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_412', 'survey_id_full': u'sid_whs2009_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009aq', 'survey_id_full': u'sid_whs2009aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_412', 'survey_id_full': u'sid_whs2007_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2006 / 10 / 13', 'survey_id': u'sid_liwhh2006', 'survey_id_full': u'sid_liwhh2006                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'South Wales', u'Monmouthshire 005E', u'South East Wales', u'NP151']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_1315', 'survey_id_full': u'sid_whs2009_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Monmouthshire, Monmouth, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwhh2004', 'survey_id_full': u'sid_liwhh2004                                                                                                                                                                                                                                                  ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire', u'South East Wales', u'Monmouthshire 005E', u'Monmouth']}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2005 / 08 / 14', 'survey_id': u'sid_liwhh2005', 'survey_id_full': u'sid_liwhh2005                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'Monmouth', u'NP151', u'South Wales', u'Monmouthshire 005E']}], 'success': True}
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")

    # We need a geography to do a spatial search!
    # This may come from the search database, via the front end, in a request (a bit roundabout!)
    elif len(geography_wkt) == 0:
        response_data['success'] = False
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")

    geojson = request.POST.get('geojson', '')


    # If we have a search ID, return the data for that ID
    search_id = request.POST.get('search_id', '')
    if len(search_id):
        pass
    else:
        # If we're missing a search ID, create a new search record for this request

        print request.user
        user = auth.get_user(request)
        if type(user) is AnonymousUser:
            user = get_anon_user()
        user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)
        search = models.Search()
        search.user = user_profile
        search.query = request.POST.get('geography', None)
        search.type = 'spatial'
        search.image_png = request.POST.get('image_png', None)

        # If we have a center point for this geography, try and find a city/town/etc name for it
        center_lat_lng = request.POST.getlist('centre_lat_lng[]', None)
        if center_lat_lng:
            print center_lat_lng
            lat = center_lat_lng[0]
            lng = center_lat_lng[1]
            nominatim_url = 'http://nominatim.openstreetmap.org/reverse?format=json&lat={0}&lon={1}&zoom=18&addressdetails=1'.format(lat, lng)
            print nominatim_url
            s = requests.Session()
            s.headers.update({'referer': 'data.wiserd.ac.uk'})
            nominatim_request = s.get(nominatim_url)

            # print nominatim_url
            # nominatim_request = requests.request('get', nominatim_url)

            nominatim_json = json.loads(nominatim_request.text)
            print pprint.pformat(nominatim_json)

            if 'state' in nominatim_json['address']:
                search.readable_name = nominatim_json['address']['state']
            if 'county' in nominatim_json['address']:
                search.readable_name = nominatim_json['address']['county']
            if 'city' in nominatim_json['address']:
                search.readable_name = nominatim_json['address']['city']

            geo_area = request.POST.get('geo_area_km2', None)
            if geo_area:
                geo_area = float(geo_area)
                print geo_area

                if geo_area < 20:
                    if 'town' in nominatim_json['address']:
                        search.readable_name = nominatim_json['address']['town']
                    if 'village' in nominatim_json['address']:
                        search.readable_name = nominatim_json['address']['village']

                if geo_area < 10:
                    if 'suburb' in nominatim_json['address']:
                        search.readable_name = nominatim_json['address']['suburb']

        search.save()
        search_uid = str(search.uid)

    response_data['success'] = True
    response_data['uid'] = search_uid

    uid_only = request.POST.get('uid_only', False)
    if uid_only:
        # we only record what was searched for, do not complete the search yet
        pass
    else:
        survey_ids = []
        survey_info = {}

        # find which regions intersect with the geography, in WellKnownText format
        spatials = find_intersects(geography_wkt)

        # print pprint.pformat(spatials)
        with open('spatial_intersects.txt', 'wb') as file_output:
            file_output.write(json.dumps(spatials, indent=4))

        for boundary_type in spatials['boundary_surveys'].keys():
            survey_ids.extend(
                spatials['boundary_surveys'][boundary_type]['table_options'].keys()
            )

        # print survey_ids

        if len(survey_ids) > 0:
            survey_model = models.Survey.objects.filter(identifier__in=survey_ids).values('short_title', 'collectionenddate', 'identifier')
            print 'number of surveys', len(survey_model)

            for s in survey_model:
                # c = connections['new'].queries
                # print len(c)

                try:
                    # print s['collectionenddate']
                    date = s['collectionenddate'].strftime('%Y / %m / %d')
                    # print date
                except:
                    date = ''

                survey_data = {}
                survey_data['survey_short_title'] = s['short_title']
                survey_data['identifier'] = s['identifier']
                survey_data['date'] = date
                # survey_data['area'] = ''
                survey_data['area'] = spatials['survey_boundaries'][s['identifier']]
                # survey_data['intersects'] = spatials['boundary_surveys']

                if len(survey_data['identifier']):
                    if survey_info.has_key(survey_data['identifier']):
                        survey_info[survey_data['identifier']]['areas'].append(survey_data['area'])

                        area_list = list(set(survey_info[survey_data['identifier']]['areas']))
                        # cleaned_list = [area for area in area_list if not has_numbers(area)]
                        cleaned_list = area_list

                        survey_info[survey_data['identifier']]['area'] = ', '.join(cleaned_list)
                    else:
                        survey_info[survey_data['identifier']] = survey_data

        response_data['survey_ids'] = survey_ids
        response_data['data'] = survey_info.values()
        response_data['intersects'] = spatials['intersects']

    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def site_setup(request):
    data = {
        'found_files': [],
        'missing_files': [],
        'found_files_2': [],
        'missing_files_2': []
    }

    for topojson_file in settings.TOPOJSON_OPTIONS:
        if os.path.isfile(topojson_file['topojson_file']):
            data['found_files'].append(topojson_file['geog_short_code'])
        else:
            data['missing_files'].append(topojson_file['geog_short_code'])

    for topojson_file in geometry_columns:
        if 'topojson_file' in topojson_file:
            if os.path.isfile(topojson_file['topojson_file']):
                data['found_files_2'].append(topojson_file['table_name'])
            else:
                data['missing_files_2'].append(topojson_file['table_name'])

    return render(request, 'site_setup.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'url': request.get_full_path(),
                      'data': data
                  }, context_instance=RequestContext(request))


@login_required
def welcome(request):
    userr = get_request_user(request)
    default_email = userr.user.email

    regex_match_and_valid = False
    matched = False
    verified = False
    email_address = None

    try:
        # Get the address object for this email address string
        email_address = EmailAddress.objects.get_for_user(userr.user, default_email)

        matches = re.search(
            '(.+)\@(assembly\.wales|cynulliad\.cymru|wales\.gov\.uk|cymru\.gov\.uk)',
            email_address.email
        )

        # Test if the email is valid gmail
        if matches:
            matched = True
        if email_address.verified:
            verified = True
        if matched and verified:
            regex_match_and_valid = True

        print 'matched:', matched, 'verified:', verified, 'regex_match_and_valid:', regex_match_and_valid
    except Exception as ex423:
        print 'regex email check error: ', ex423

    data = {
        'userr': userr,
        'default_email': default_email,
        'email': email_address.email,
        'regex_match_and_valid': regex_match_and_valid,
        'verified': verified,
        'matched': matched,
        'preferences': get_user_preferences(request),
        'languages': models.UserLanguage.objects.all()
    }
    # print data
    return render(request, 'welcome.html', data, context_instance=RequestContext(request))


def save_profile_extras(request):
    print 'post', request.POST
    request_user = get_request_user(request)
    request_user.institution = request.POST.get('institution', '')
    request_user.specialty = request.POST.get('specialty', '')
    request_user.sector = request.POST.get('sector', '')
    request_user.comments = request.POST.get('comments', '')
    check_enable_naw = request.POST.get('check_enable_naw', '')
    if check_enable_naw:
        request_user.role = 'naw'
    else:
        # Forms don't send unchecked checkboxes
        request_user.role = 'regular'

    request_user.init_user = True
    request_user.save()

    user_language_id = request.POST.get('user_language', '')
    if user_language_id:
        user_preferences = get_user_preferences(request)
        user_preferences.preferred_language = models.UserLanguage.objects.get(id=user_language_id)
        user_preferences.save()

        set_session_preferred_language(request)

    if request_user.role == 'naw':
        return redirect('naw_dashboard')
    else:
        return redirect('index')


def permission_denied_handler(request):
    from django.http import HttpResponse
    return HttpResponse('you have no permissions!')


def events(request):
    return render(request, 'events.html',
                  {
                      'welcome': 'hi',
                  }, context_instance=RequestContext(request))


def search_data(request, search_uuid):
    error = None
    dataset_url = ''
    dataset_data_header_items_clean = []

    try:

        found_search = models.NomisSearch.objects.get(uuid=search_uuid)
        assert isinstance(found_search, models.NomisSearch)

        dataset_id = found_search.dataset_id
        geog = found_search.geography_id

        codelist = []
        for code in found_search.search_attributes:
            codelist.append({
                'option': code,
                'variable': found_search.search_attributes[code]
            })

        if found_search.search_type == models.SearchType.objects.get(name='Nomis'):

            rd = RemoteData()
            region_id, topojson_file = rd.get_dataset_geodata(geog, high=False)
            dataset_url, dataset_file = rd.get_dataset_url(dataset_id, region_id, '', codelist)

            dataset_url = dataset_url.replace('.json', '.csv')

            dataset_data = requests.get(dataset_url).text
            dataset_data_list = dataset_data.split('\n')

            dataset_data_header = dataset_data_list[0]
            dataset_data_header_items = dataset_data_header.split(',')

            for header_item in dataset_data_header_items:
                # dataset_data_header_items_clean.append(header_item.rstrip('"').lstrip('"'))
                dataset_data_header_items_clean.append({
                    'data': header_item.rstrip('"').lstrip('"')
                })

                # dataset_data_list_full = []
                # for data_row_index, data_row in enumerate(dataset_data_list[1:]):
                #     print data_row
                #     print data_row_index
                #     data_row_items = data_row.split(',')
                #
                #     if len(data_row_items) == len(dataset_data_header_items_clean):
                #         dataset_data_dict = {}
                #         for header_index, header_item in enumerate(dataset_data_header_items_clean):
                #             print header_index, len(data_row_items), header_item, data_row_items[header_index]
                #             # print header_index > len(data_row_items)
                #             dataset_data_dict[header_item] = data_row_items[header_index].rstrip('"').lstrip('"')
                #         dataset_data_list_full.append(dataset_data_dict)

    except Exception as e8943279:
        print e8943279
        error = str(e8943279)

    return render(request, 'search_data.html',
                  {
                      'error': error,
                      'dataset_id': dataset_id,
                      'dataset_url': dataset_url,
                      'search_options': found_search.search_attributes,
                      'display_options': found_search.display_attributes,
                      'dataset_data_header': dataset_data_header_items_clean,
                      # 'dataset_data': dataset_data_list[1:],
                      # 'dataset_data_list_full': dataset_data_list_full,
                      'provider': found_search.search_type.name,
                      'search_uuid': search_uuid
                  }, context_instance=RequestContext(request))


def get_topojson_for_uuid_view(request, search_uuid):
    response_data = get_topojson_for_uuid(request, search_uuid)
    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def geojson_points_to_topojson(geojson_object):
    geometries = []
    for f in geojson_object['features']:
        blob = {
            "type": "Point",
        }
        if 'properties' in f:
            blob["properties"] = f['properties']

        if 'geometry' in f and f['geometry']:
            if 'coordinates' in f['geometry'] and f['geometry']['coordinates']:
                blob["coordinates"] = f['geometry']['coordinates']
            # else:
            #     blob["coordinates"] = []
        # else:
        #     blob["coordinates"] = []
                geometries.append(blob)

        # geometries.append(
        #     {
        #         "type": "Point",
        #         "properties": f['properties'],
        #         "coordinates": f['geometry']['coordinates']
        #     },
        # )
    topojson_conversion = {
        "objects": {
            "name": {
                "type": "GeometryCollection",
                "geometries": geometries
            }
        },
        "arcs": [],
        "type": "Topology"
    }
    return topojson_conversion


def get_topojson_by_name(request, topojson_name):
    print topojson_name
    print request.GET
    from topojson import topojson

    response_data = {}

    nomis_search = models.NomisSearch()
    nomis_search.uuid = str(uuid.uuid4())
    nomis_search.user = get_request_user(request)
    nomis_search.dataset_id = None
    nomis_search.geography_id = topojson_name
    nomis_search.search_attributes = codelist_to_attributes({})
    nomis_search.search_type = models.SearchType.objects.get(name='User')
    nomis_search.save()

    codes = request.GET.getlist('codes[]')

    layer_data = {
        'bin_num': 6,
        'bin_type': 'q',
        'colorpicker': 'Spectral',
        'codelist': {},
        'geography_id': topojson_name,
        'uuid': nomis_search.uuid,
        'name': topojson_name,
        'dataset_id': '-1',
        'display_fields': ''
    }

    if topojson_name == 'assembly_region':
        filter_var_code = 'code__istartswith'
        filter_var_name = 'name__istartswith'
        filter_var_altname = 'altname__istartswith'

        if len(codes) == 0:
            region_subset = models.SpatialdataNawer.objects.using('new').all()
        else:
            ors = []
            for code in codes:
                ors.append(Q(**{filter_var_code: code}))
                ors.append(Q(**{filter_var_name: code.lower().strip()}))
                ors.append(Q(**{filter_var_altname: code}))

            region_subset = models.SpatialdataNawer.objects.using('new').all().filter(
                reduce(operator.or_, ors)
            )
        s = serialize('geojson', region_subset, properties=('geom', 'code','name', 'altname', 'REMOTE_VALUE'))
        topojson_conv = topojson(json.loads(s))
        response_data['topojson'] = topojson_conv

    elif topojson_name == 'unitary_authority':
        # filter_var_code = 'code__istartswith'
        filter_var_name = 'label__istartswith'
        # filter_var_altname = 'altname__istartswith'

        if len(codes) == 0:
            ua_subset = models.SpatialdataUA.objects.using('new').all()
        else:
            ors = []
            for code in codes:
                # ors.append(Q(**{filter_var_code: code}))
                ors.append(Q(**{filter_var_name: code}))
                # ors.append(Q(**{filter_var_altname: code}))

                ua_subset = models.SpatialdataUA.objects.using('new').all().filter(
                    reduce(operator.or_, ors)
                )

        s = GeoJSONSerializer().serialize(
            ua_subset,
            use_natural_keys=True,
            with_modelname=False,
            simplify=0.0005
        )

        # s = serialize('geojson', lsoa_subset, fields=('geom', 'code', 'name', 'REMOTE_VALUE'))
        topojson_conv = topojson(
            json.loads(s),
            quantization=1e4,
            # simplify=0.0005
        )
        response_data['topojson'] = topojson_conv
        # s = serialize('geojson', ua_subset, properties=('geom', 'label', 'REMOTE_VALUE'))
        # topojson_conv = topojson(json.loads(s))
        # response_data['topojson'] = topojson_conv

    elif topojson_name == 'assembly_constituency':
        filter_var = 'code__istartswith'
        if len(codes) == 0:
            constituency_subset = models.SpatialdataConstituency.objects.using('new').all()
        else:
            ors = []
            for code in codes:
                ors.append(Q(**{filter_var: code}))

            constituency_subset = models.SpatialdataConstituency.objects.using('new').all().filter(
                reduce(operator.or_, ors)
            )
        s = serialize('geojson', constituency_subset, properties=('geom', 'code', 'REMOTE_VALUE'))
        # geos = GEOSGeometry(s)
        # new_geos = geos.simplify(tolerance=0.1, preserve_topology=True)
        # topojson_conv = topojson(json.loads(s), quantization=1e6, simplify=0.0005)
        topojson_conv = topojson(json.loads(s))
        response_data['topojson'] = topojson_conv

    elif topojson_name == 'pcode_district':
        filter_var = 'label__istartswith'
        code = 'CF1'
        postcode_subset = models.SpatialdataPostCode.objects.using('new').all().filter(**{filter_var: code})

        # TODO check if this needs better serialisation as below
        s = serialize('geojson', postcode_subset, properties=('geom', 'label', 'REMOTE_VALUE'))
        topojson_conv = topojson(json.loads(s), quantization=1e6, simplify=0.0005)
        response_data['topojson'] = topojson_conv

    elif topojson_name == 'lsoa':
        filter_var = 'code__istartswith'
        if len(codes) == 0:
            lsoa_subset = models.SpatialdataLSOA.objects.using('new').all()
        else:
            ors = []
            for code in codes:
                ors.append(Q(**{filter_var: code}))

            lsoa_subset = models.SpatialdataLSOA.objects.using('new').all().filter(
                reduce(operator.or_, ors)
            )

        print len(list(lsoa_subset))
        # print list(lsoa_subset)

        s = GeoJSONSerializer().serialize(
            lsoa_subset,
            use_natural_keys=True,
            with_modelname=False,
            simplify=0.0005
        )

        # s = serialize('geojson', lsoa_subset, fields=('geom', 'code', 'name', 'REMOTE_VALUE'))
        topojson_conv = topojson(
            json.loads(s),
            quantization=1e4,
            # simplify=0.0005
        )
        response_data['topojson'] = topojson_conv

    elif topojson_name == 'pcode_point':
        filter_var = 'postcode__istartswith'

        if len(codes) == 0:
            code = 'CF101'
            # code2 = 'LL101'
            # code3 = 'SY101'
            postcode_subset = models.SpatialdataPostCodePoint.objects.using('new').all().filter(**{filter_var: code})
            # postcode_subset = models.SpatialdataPostCodePoint.objects.using('new').all().filter(
            #     Q(**{filter_var: code}) | Q(**{filter_var: code2}) | Q(**{filter_var: code3})
            # )
        else:
            ors = []
            for code in codes:
                if len(code) > 4:
                    if code[4] == ' ':
                        code = code.replace(' ', '')

                ors.append(Q(**{filter_var: code}))
            postcode_subset = models.SpatialdataPostCodePoint.objects.using('new').all().filter(
                reduce(operator.or_, ors)
            )
        # print postcode_subset.query

        # print list(postcode_subset)
        print len(list(postcode_subset))
        s = serialize('geojson', postcode_subset, properties=['geom', 'postcode', 'REMOTE_VALUE'])
        # format it like it's topojson, which for some reason the other topojson lib can't do for points
        response_data['topojson'] = geojson_points_to_topojson(json.loads(s))

    else:
        rd = RemoteData()
        region_id, topojson_file = rd.get_dataset_geodata(topojson_name, False)
        with open(topojson_file, 'r') as fd:
            response_data['topojson'] = json.loads(fd.read())

    layer_data['data_names'] = list([])

    response_data['all_data'] = {}


    response_data['search_uuid'] = nomis_search.uuid
    response_data['layer_data'] = layer_data
    # response_data['type'] = 'Topojson'

    return response_data


def get_topojson_for_uuid(request, search_uuid):
    request_user = get_request_user(request)
    user_prefs = get_user_preferences(request)

    response_data = {}
    #FIXME add a check for user here
    found_search_model = models.NomisSearch.objects.get(uuid=search_uuid)
    assert isinstance(found_search_model, models.NomisSearch)
    dataset_id = found_search_model.dataset_id
    geog = found_search_model.geography_id

    boundary_name = ''
    for geom in geometry_columns:
        if 'geog_short_code' in geom:
            if geog in geom['geog_short_code']:
                if 'name' in geom:
                    boundary_name = geom['name']

    codelist = []
    for code in found_search_model.search_attributes:
        codelist.append({
            'option': code,
            'variable': found_search_model.search_attributes[code]
        })
    # print found_search_model.display_attributes

    layer_data = {
        'bin_num': found_search_model.display_attributes['bin_num'],
        'bin_type': found_search_model.display_attributes['bin_type'],
        'colorpicker': found_search_model.display_attributes['colorpicker'],
        'codelist': codelist,
        'geography_id': found_search_model.geography_id,
        'uuid': found_search_model.uuid,
        'name': found_search_model.name,
        'dataset_id': found_search_model.dataset_id,
        'display_fields': found_search_model.display_fields
    }

    if 'point_icon' in found_search_model.display_attributes:
        layer_data['point_icon'] = found_search_model.display_attributes['point_icon']
    else:
        layer_data['point_icon'] = ''

    # local_search_layers = []
    # remote_search_layers = []

    if found_search_model.search_type is None:
        search_type = 'Nomis'
    else:
        search_type = found_search_model.search_type.name

    print 'search_type', search_type

    if search_type == 'LocalResearch':
        layer_data['remote_value_key'] = found_search_model.display_attributes['remote_value_key']
        layer_data['filter'] = found_search_model.display_attributes.get('filter')

        print layer_data['filter']

        geo = json.loads(
            get_wiserd_layer_topojson(
                'wiserd_layer',
                found_search_model.dataset_id,
                'dataportal3',
                layer_data['remote_value_key'],
                request.GET.get("update_cache", False),
                layer_data['filter']
            )
        )

        # print pprint.pformat(geo)

        for f in geo['features']:
            if 'properties' in f:
                f["properties"]['STRING_DATA'] = [
                        {
                            'title': 'test_img',
                            'value': 'https://thumb7.shutterstock.com/display_pic_with_logo/1467269/284551751/stock-photo-heaps-of-coal-284551751.jpg'
                        }
                    ]

        topojson_conv = geojson_points_to_topojson(geo)
        # from topojson import topojson

        # topojson_conv = topojson(
        #     json.loads(geo),
        #     quantization=1e4,
        #     # simplify=0.0005
        # )

        # TODO - this point data needs to be TopoJSON, not GeoJson
        response_data['topojson'] = topojson_conv

    if search_type == 'Nomis':
        # remote_search_layers.append(layer_data)

        rd = RemoteData()
        a = rd.get_topojson_with_data(dataset_id, geog, '', codelist, high=user_prefs.topojson_high, search_uuid=search_uuid)
        response_data['topojson'] = a

    if search_type == 'StatsWales':
        # remote_search_layers.append(layer_data)

        swod = StatsWalesOData()
        all_data = swod.get_data_dict(
            dataset_id,
            [
                # 'Area_Code': area_code,
                ('Year_Code', swod.equals_conditional, 2015),
                ('AgeGroup_Code', swod.equals_conditional , 'AllAges')
            ],
            {'search_uuid': search_uuid}
        )

        rd = RemoteData()
        region_id, topojson_file = rd.get_dataset_geodata(geog, user_prefs.topojson_high)

        a = rd.update_topojson(topojson_file, all_data, measure_is_percentage=False)

        response_data['topojson'] = a

    # TODO we want to inject new variables into properties here
    # Why do we have the nomis/ survey distinction for getting "all_data"?
    if search_type == 'Survey':
        # local_search_layers.append(layer_data)

        # survey_spatial_data_correction = models.SpatialSurveyLink.objects.filter(
        #     survey__identifier='wisid_AssemblyRegions_56a653f209d3a'
        # )
        # print 'survey_spatial_data_correction count', survey_spatial_data_correction.count()

        # for cor in survey_spatial_data_correction:
        #     # print cor.__dict__
        #     cor.boundary_name = 'National Assembly Region'
        #     cor.data_name = 'HECTARE'
        #     cor.save()

        data_name = ''
        all_data = {}

        for code in codelist:
            if code['option'] == 'data_name':
                data_name = code['variable']

        # print '======', dataset_id, boundary_name, data_name

        # FIXME this is stupid, either import the right name, or roll back the spatial_search dict
        if boundary_name == 'Parliamentary Constituencies 2011':
            boundary_name = 'Parliamentary'

        survey_spatial_data = models.SpatialSurveyLink.objects.get(
            survey__identifier=dataset_id,
            boundary_name=boundary_name,
            data_name=data_name
        )
        assert isinstance(survey_spatial_data, models.SpatialSurveyLink)

        survey_spatial_data_strings = models.SpatialSurveyLink.objects.filter(
            survey__identifier=dataset_id,
            boundary_name=boundary_name
            # data_type='unicode'
        ).order_by('data_name')

        regional_data = survey_spatial_data.regional_data

        display_fields = found_search_model.display_fields

        welsh_language_model = models.UserLanguage.objects.get(user_language_title='Welsh')
        use_welsh = False
        if user_prefs.preferred_language == welsh_language_model:
            use_welsh = True

            if survey_spatial_data.full_name_cy:
                layer_data['name'] = survey_spatial_data.full_name_cy

        # This is smarter than doing it in the loop, as grouping for an attr won't change within a layer
        attr_groupings = {}
        for attr in survey_spatial_data_strings:
            assert isinstance(attr, models.SpatialSurveyLink)
            attr_group = attr.link_groups.all().values_list('group_name', flat=True)
            attr_groupings[attr.data_name] = attr_group

        region_string_data = {}
        for region in regional_data:

            region_string_data[region] = []
            for data_strings in survey_spatial_data_strings:
                assert isinstance(data_strings, models.SpatialSurveyLink)
                # For each region in this survey's SpatialSurveyLink,
                # build a string of the unicode data elements
                # name_of_data : value_of_data, "Title Cased"

                # If display fields are given, only add the properties if they're set to "true"
                if display_fields:
                    if data_strings.data_name in display_fields:
                        # print data_strings.data_name, display_fields[data_strings.data_name]

                        if display_fields[data_strings.data_name] == 'true':
                            data_title = ''

                            if use_welsh:
                                if data_strings.full_name_cy:
                                    data_title += data_strings.full_name_cy
                                else:
                                    if data_strings.full_name:
                                        data_title += data_strings.full_name
                                    else:
                                        data_title += data_strings.data_name
                            else:
                                if data_strings.full_name:
                                    data_title += data_strings.full_name
                                else:
                                    data_title += data_strings.data_name

                            region_string_data[region].append({
                                'title': data_title,
                                'grouping': list(attr_groupings[data_strings.data_name]),
                                'value': data_strings.regional_data[region]
                            })
                else:
                    pass
                    # data_title = ''
                    #
                    # if data_strings.category:
                    #     data_title += '{} : '.format(data_strings.category)
                    #
                    # if data_strings.full_name:
                    #     data_title += data_strings.full_name
                    # else:
                    #     data_title += data_strings.data_name
                    #
                    # region_string_data[region].append({
                    #     'title': data_title,
                    #     'value': data_strings.regional_data[region]
                    # })

            # Shorthand Name,Category,FullName,Notes,CategoryCY,FullNameCY,NotesCY
            spatial_survey_fields = [
                {
                    'field': 'category', 'name': 'Category'
                },
                {
                    'field': 'notes', 'name': 'Notes'
                }
            ]

            spatial_survey_fields_cy =[
                {
                    'field': 'category_cy', 'name': 'Categorïau'
                },
                {
                    'field': 'full_name_cy', 'name': 'Enw'
                },
                {
                    'field': 'notes_cy', 'name': 'Nodiadau'
                }
            ]

            if use_welsh:
                spatial_survey_fields_lang = spatial_survey_fields_cy
            else:
                spatial_survey_fields_lang = spatial_survey_fields

            for spatial_survey_field in spatial_survey_fields_lang:
                region_string_data[region].append({
                    'title': spatial_survey_field['name'],
                    'value': getattr(survey_spatial_data, spatial_survey_field['field'])
                })

            if survey_spatial_data.full_name:
                data_name = survey_spatial_data.full_name

                # print 'region_string_data', region_string_data

        for region in regional_data:

            region_value = regional_data[region]
            if survey_spatial_data.data_type == 'float' and survey_spatial_data.data_formatting:
                region_value = survey_spatial_data.data_formatting.format(float(region_value))

            region_dict = {
                'name': '',
                'value': region_value,
                'data_global_average': survey_spatial_data.data_global_average,
                'data_prefix': survey_spatial_data.data_prefix,
                'data_suffix': survey_spatial_data.data_suffix,
                "geography_id": '',
                "geography_code": '',
                "data_status": "A",
                "geography": region,
                "string_data": region_string_data[region],
                "data_title": data_name,
                "search_uuid": found_search_model.uuid
            }

            if survey_spatial_data.full_name_cy:
                region_dict['data_title_alt1'] = survey_spatial_data.full_name_cy

            # FIXME - no idea why dict into array into dict
            regions = [region_dict]
            all_data[region] = regions

        rd = RemoteData()
        region_id, topojson_file = rd.get_dataset_geodata(geog, False)
        a = rd.update_topojson(topojson_file, all_data, False)
        response_data['topojson'] = a

        data_names = models.SpatialSurveyLink.objects.filter(
            survey__identifier=dataset_id,
            boundary_name=boundary_name,
        ).values_list('data_name', flat=True)

        # print 'data_name', data_names
        layer_data['data_names'] = list(data_names)

        response_data['all_data'] = all_data

    response_data['search_uuid'] = search_uuid

    # TODO remove this
    # response_data['connections'] = list(connections['new'].queries)
    response_data['layer_data'] = layer_data
    response_data['type'] = search_type

    return response_data


def help_support(request):
    return render(request, 'help_support.html',
                  {
                      'welcome': 'hi',
                  }, context_instance=RequestContext(request))


def get_data_for_search_uuid(search_uuid):
    dataset_data_list_full = []
    try:

        found_search = models.NomisSearch.objects.get(uuid=search_uuid)
        dataset_id = found_search.dataset_id
        geog = found_search.geography_id

        codelist = []
        for code in found_search.search_attributes:
            codelist.append({
                'option': code,
                'variable': found_search.search_attributes[code]
            })

        if found_search.search_type == 'StatsWales':
            swod = StatsWalesOData()
            swod_const_options = [
                # 'Area_Code': area_code,
                ('Year_Code', swod.equals_conditional, 2015),
                ('AgeGroup_Code', swod.equals_conditional, 'AllAges')
            ]

            all_data = swod.get_data_dict(
                dataset_id,
                swod_const_options,
                {'search_uuid': search_uuid}
            )

            rd = RemoteData()
            region_id, topojson_file = rd.get_dataset_geodata(geog, high=False)

            a = rd.update_topojson(topojson_file, all_data, measure_is_percentage=False)
            dataset_url = swod.get_data_url(
                dataset_id,
                swod_const_options
            )

            # region_id = ''
            # topojson_file = ''
            # dataset_url = ''
            dataset_file = 'swod_{}_{}.dat'.format(dataset_id, search_uuid)

        if found_search.search_type == 'Nomis':

            rd = RemoteData()
            region_id, topojson_file = rd.get_dataset_geodata(geog, high=False)
            dataset_url, dataset_file = rd.get_dataset_url(dataset_id, region_id, '', codelist)

            dataset_url = dataset_url.replace('.json', '.csv')

            dataset_data = requests.get(dataset_url).text
            dataset_data_list = dataset_data.split('\n')

            dataset_data_header = dataset_data_list[0]
            dataset_data_header_items = dataset_data_header.split(',')
            # print dataset_data_header_items

            dataset_data_header_items_clean = []
            for header_item in dataset_data_header_items:
                dataset_data_header_items_clean.append(header_item.rstrip('"').lstrip('"'))
            # print dataset_data_header_items_clean

            for data_row_index, data_row in enumerate(dataset_data_list[1:]):
                # print data_row
                # print data_row_index
                data_row_items = data_row.split(',')

                if len(data_row_items) == len(dataset_data_header_items_clean):
                    dataset_data_dict = {}
                    for header_index, header_item in enumerate(dataset_data_header_items_clean):
                        # print header_index, len(data_row_items), header_item, data_row_items[header_index]
                        dataset_data_dict[header_item] = data_row_items[header_index].rstrip('"').lstrip('"')
                        # dataset_data_dict.append(data_row_items[header_index].rstrip('"').lstrip('"'))
                    dataset_data_list_full.append(dataset_data_dict)
    except Exception as e8943279:
        error = str(e8943279)
    return dataset_data_list_full


def csv_view_data(request, provider, search_uuid):
    dataset_data_list_full = get_data_for_search_uuid(search_uuid)
    return HttpResponse(json.dumps(dataset_data_list_full, indent=4), content_type="application/json")


def naw_dashboard(request):
    return render(request, 'naw_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  },context_instance=RequestContext(request))


def m4w_dashboard(request):
    return render(request, 'm4w_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  },context_instance=RequestContext(request))


def aqp_dashboard(request):
    return render(request, 'aqp_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  }, context_instance=RequestContext(request))

def wep_dashboard(request):
    return render(request, 'wep_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  }, context_instance=RequestContext(request))


def wmh_dashboard(request):
    return render(request, 'wmh_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  },context_instance=RequestContext(request))


def wiserd_projects_dashboard(request):
    return render(request, 'wiserd_projects_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  }, context_instance=RequestContext(request))

def partner_projects_dashboard(request):
    return render(request, 'partner_projects_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  }, context_instance=RequestContext(request))

def about_dashboard(request):
    return render(request, 'about_dashboard.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  }, context_instance=RequestContext(request))

def admin_api(request):
    userr = get_request_user(request)
    method = request.GET.get("method", None)

    if method and 'request_access' in method and userr.user.is_authenticated():
        document_type = request.GET.get("document_type", None)
        survey_id = request.GET.get("survey_id", None)

        request_access_email_success = send_email(userr, EMAIL_TYPES.REQUEST_ACCESS, {
            'survey_id': survey_id,
            'document_type': document_type
        })

        return render(request, 'access_request_confirm.html',
                      {
                          'userr': userr,
                          'preferences': get_user_preferences(request),
                          'searches': get_user_searches(request),
                          'access_request': {
                              'request_access_email_success': request_access_email_success,
                              'method': 'request_access',
                              'survey_id': survey_id,
                              'document_type': document_type
                          }

                      },context_instance=RequestContext(request))
    else:
        return render(request, 'dashboard.html',
                      {
                          'preferences': get_user_preferences(request),
                          'searches': get_user_searches(request)
                      },context_instance=RequestContext(request))


def send_email_confirmation_view(request):
    send_email_confirmation(request, get_request_user(request).user, signup=False)
    return welcome(request)


def dataportal(request):
    return redirect('index')


def http_404_error(request):

    return render(request, '404_template.html', {}, context_instance=RequestContext(request))


def licence_attribution(request):
    return render(request, 'licence_attribution.html', {}, context_instance=RequestContext(request))


def local_data(request):
    return render(request, 'local_data.html', {}, context_instance=RequestContext(request))


@csrf_exempt
def download_dataset_zip(request):
    dataset_id = request.GET.get('dataset_id')

    zip_subdir = 'wiserd_docs'
    zip_filename = "{}.zip".format(zip_subdir)

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w", zipfile.ZIP_DEFLATED)

    print os.path.abspath('./')

    filenames = ['./dataportal3/static/dataportal/docs/licence_attribution_en.html']

    for fpath in filenames:

        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    if dataset_id:
        print dataset_id

        zf.writestr('data.json', json.dumps(get_data_for_search_uuid(dataset_id), indent=4))
        zf.writestr('topojson_data.json', json.dumps(get_topojson_for_uuid(request, dataset_id), indent=4))

        try:
            screenshot_file = do_screenshot(dataset_id)
            zf.write(screenshot_file)
        except Exception as e:
            print e

    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    # and correct content-disposition
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

    # else:
    #     return render(request, '404.html', {'error': 'dataset_not_found'}, context_instance=RequestContext(request))


def do_screenshot(search_uuid):
    import time
    from pyvirtualdisplay import Display
    from selenium import webdriver
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait

    display = Display(visible=0, size=(1024, 768))
    display.start()

    delay = 5
    filename = 'map_{}.png'.format(search_uuid)

    browser = webdriver.Firefox()
    browser.get('http://localhost:8000/map?layers={}&use_template=False'.format(search_uuid))

    try:
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.ID, 'findme_{}'.format(search_uuid)))
        )
        time.sleep(delay)
        browser.save_screenshot(filename)

    except Exception as e32564:
        print type(e32564), e32564
        raise
    finally:
        browser.quit()
        display.stop()

    return filename


def gen_screenshot(request, search_uuid):

    filename = do_screenshot(search_uuid)

    try:
        with open(filename, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        return render(request, '404.html', {'error': 'dataset_not_found'}, context_instance=RequestContext(request))


def user_guide(request):
    return render(request, 'user_guide.html', {}, context_instance=RequestContext(request))


def browse_surveys(request):
    return render(request, 'browse_surveys.html', {}, context_instance=RequestContext(request))


def data_and_history(request):
    return render(request, 'data_and_history.html', {}, context_instance=RequestContext(request))


def response_table(request, question_id):
    # rts = ResponseTable.objects.all()

    question = models.Question.objects.get(qid=question_id)
    response = question.response
    rts = ResponseTable.objects.filter(response=response)

    search_result_data = []
    columns = []

    for rt in rts:
        attr = rt.feature_attributes

        for itr in attr:
            columns = itr.keys()
            search_result_data.append(itr)

    api_data = {
        'columns': columns,
        'search_result_data': search_result_data
    }

    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def question_links(request):
    qs = QuestionSorter()
    qs.do_order_questions()



    api_data = {
        'text_output': qs.output_logs(),

        'total questions considered': qs.counter,

        'total questions in table': len(models.Question.objects.all()),

        'total ordered': qs.total_ordered,

        'total unlinked': qs.unlinked,

        'failed to order': qs.counter - qs.total_ordered,
    }

    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def map_test(request):
    return render(request, 'map_test.html', {}, context_instance=RequestContext(request))


def wiserd_education(request):
    return render(request, 'wiserd_education.html', {}, context_instance=RequestContext(request))


def civil_society(request):
    return render(request, 'civil_society.html', {}, context_instance=RequestContext(request))


def snippet_test(request):
    return render(request, 'snippet_test.html', {}, context_instance=RequestContext(request))


def d3_test(request, survey_id):
    return render(request, 'd3_test.html', {'survey_id': survey_id}, context_instance=RequestContext(request))


def terms_conditions(request):
    return render(request, 'terms_conditions.html', {}, context_instance=RequestContext(request))
