from datetime import datetime
import json
import os
import pprint
import uuid
from BeautifulSoup import BeautifulSoup
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
# from django.contrib.gis.gdal import CoordTransform
# from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import operator
from dataportal3 import models
from dataportal3.forms import ShapefileForm
from dataportal3.utils.ShapeFileImport import celery_import, ShapeFileImport
from dataportal3.utils.remote_data import RemoteData
from dataportal3.utils.spatial_search.spatial_search import find_intersects
from dataportal3.utils.userAdmin import get_anon_user, get_user_searches, get_request_user, get_user_preferences
import requests
from old.views import text_search, date_handler
from wiserd3 import settings

def index(request):
    return render(request, 'index.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request)
                  },
                  context_instance=RequestContext(request))


def user_settings(request):
    return render(request, 'settings.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                  },
                  context_instance=RequestContext(request))


def search_survey_question_gui(request):
    search_terms = request.GET.get('search_terms', '')
    ors = search_terms.split(',')
    return render(request, 'search.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'search_terms': search_terms,
                      'url': request.get_full_path()
                  }, context_instance=RequestContext(request))


def search_survey_question_api(request):
    search_terms = request.GET.get('search_terms', '')

    print request.user
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)

    search, created = models.Search.objects.using('new').get_or_create(user=user_profile,
                                                                       query=search_terms,
                                                                       readable_name=search_terms,
                                                                       type='text')
    search.save()

    api_data = text_search(search_terms)
    api_data['url'] = request.get_full_path()
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def blank(request):
    return render(request, 'blank.html', {}, context_instance=RequestContext(request))


def survey_detail(request, survey_id):

    print request.user
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)

    search, created = models.Search.objects.using('new').get_or_create(user=user_profile, query=survey_id, type='survey')
    search.save()

    return render(request, 'survey_detail.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'survey_id': survey_id
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

    b = []
    try:
        capabilities = requests.get('http://inspire.wales.gov.uk/maps/wms?request=getCapabilities&version=1.3.0')
        soup = BeautifulSoup(capabilities.text)
        x = soup.wms_capabilities.capability.findAll('layer', queryable=1)
        for y in x:
            b.append({
                'tile_name': [z.string for z in y.findAll('name')][0],
                'name': [z.string for z in y.findAll('title')][0]
            })
    except:
        pass
    surveys = request.GET.getlist('surveys', [])

    wiserd_layers_clean = []
    uploaded_layers_clean = []
    try:
        wiserd_layers = models.GeometryColumns.objects.using('survey').filter(f_table_schema='spatialdata')
        for w_layer in wiserd_layers:
            wiserd_layers_clean.append({
                'display_name': w_layer.f_table_name.replace('_', ' ').title(),
                'table_name': w_layer.f_table_name
            })

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

    return render(request, 'map.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'surveys': json.dumps(surveys),
                      'wms_layers': b,
                      'wiserd_layers': wiserd_layers_clean,
                      'upload_layers': uploaded_layers_clean,
                      'area_names': json.dumps(area_names)
                  },
                  context_instance=RequestContext(request))


def question(request, question_id):
    print request.user
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)

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
            user_prefs = get_user_preferences(request)
            if 'links_new_tab' in request.GET:
                user_prefs.links_new_tab = True
            else:
                user_prefs.links_new_tab = False
            user_prefs.save()
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


@csrf_exempt
def get_geojson(request):

    print request.POST

    time1 = datetime.now()
    layer_type = request.POST.get('layer_type')

    if layer_type == 'wiserd_layer':
        wiserd_layer = request.POST.getlist('layer_names[]')[0]
        spatial_table_name = str(wiserd_layer).replace('_', '').strip()
        wiserd_layer_model = apps.get_model(
            app_label='dataportal3',
            model_name=wiserd_layer
        )
        shape_table_object = wiserd_layer_model.objects.using('survey_spatialdata').all()

        shape_list = shape_table_object.extra(
            select={
                'geometry': 'ST_AsGeoJSON(ST_Transform(ST_SetSRID("the_geom", 27700),4326))'
            }
        ).values('geometry')

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

    time2 = datetime.now()
    print time2 - time1

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

        print datetime.now() - time2

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

    print datetime.now() - time2
    geojson_feature = {
        "type": "FeatureCollection",
        "features": shape_feature_list,
        "properties": {
            'name': spatial_table_name
        }
    }
    end_result = json.dumps(geojson_feature)
    print datetime.now() - time1
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

    # form = ShapefileForm(request.POST, request.FILES )
    # print form
    # print ShapefileForm()
    # print form.is_valid()

    messages = []

    # shapefile_upload = models.ShapeFileUpload()
    # shapefile_upload.user = get_request_user(request)
    # shapefile_upload.uuid = str(uuid.uuid4())
    # shapefile_upload.shapefile = request.FILES['file']
    # shapefile_upload.name = request.POST.get('shapefile_name', '')
    # shapefile_upload.save()
    #
    # filepath_url = shapefile_upload.shapefile.url

    # try:
    # shp_import = ShapeFileImport(
    #     get_request_user(request),
    #     zip_file=request.FILES['file'],
    #     filename=request.POST.get('shapefile_name', '')
    # )
    # shp_import.extract_zip()
    # celery_key = shp_import.import_to_gis()

    user = get_request_user()
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

    # shapefile_upload.description = shapefile_info
    # shapefile_upload.save()
    # except Exception as ex:
    #     print ex

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
    return render(request, 'index.html',
                  {'logout_success': logout_success, 'msg': msg},
                  context_instance=RequestContext(request))


def profile(request):
    return render(request, 'profile.html',
                  {},
                  context_instance=RequestContext(request))


def remote_data(request):
    rd = RemoteData()
    to_return = {}
    print request.GET

    method = request.GET.get("method", None)

    if method == 'search':
        search_term = request.GET.get("search_term", None)
        print search_term, type(search_term)
        if search_term:
            datasets = rd.search_datasets(search_term)
            to_return['datasets'] = datasets

    if method == 'metadata':
        dataset_id = request.GET.get("dataset_id", None)

        to_return['metadata'] = rd.get_dataset_overview(dataset_id)

    return HttpResponse(json.dumps(to_return, indent=4), content_type="application/json")


def remote_data_topojson(request):
    print request.GET

    codelist = None
    codelist_json = request.GET.get('codelist_selected', None)
    if codelist_json:
        codelist = json.loads(codelist_json)
        print pprint.pformat(codelist)

    dataset_id = request.GET.get('dataset_id', '')
    nomis_variable = request.GET.get('nomis_variable', '')
    geog = request.GET.get('geography', '')
    print dataset_id, nomis_variable, geog

    rd = RemoteData()
    a = rd.get_topojson_with_data(dataset_id, geog, nomis_variable, codelist)
    a = json.dumps(a, indent=4)

    return HttpResponse(a, content_type="application/json")


def search_qual_api(request):
    search_terms = request.GET.get('search_terms', '')

    print request.user
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)

    search, created = models.Search.objects.using('new').get_or_create(user=user_profile,
                                                                       query=search_terms,
                                                                       readable_name=search_terms,
                                                                       type='text')
    search.save()

    api_data = qual_search(search_terms)
    api_data['url'] = request.get_full_path()
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def qual_search(search_terms):

    fields = ['identifier']
    qual_models = models.QualTranscriptData.objects.filter(
        dc_info__qualcalais__value__icontains=search_terms
    ).distinct().values('identifier', 'pages', 'dc_info__title', 'dc_info__tier', 'dc_info__description')

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

        spatials = find_intersects(geography_wkt)

        # print pprint.pformat(spatials)

        for boundary_type in spatials['boundary_surveys'].keys():
            survey_ids.extend(
                spatials['boundary_surveys'][boundary_type]['table_options'].keys()
            )

        print survey_ids

        if len(survey_ids) > 0:
            survey_model = models.Survey.objects.filter(identifier__in=survey_ids).values('short_title', 'collectionenddate', 'identifier')
            print len(survey_model)

            for s in survey_model:

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

    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def site_setup(request):
    data = {
        'found_files': [],
        'missing_files': []
    }

    for topojson_file in settings.TOPOJSON_OPTIONS:
        if os.path.isfile(topojson_file['topojson_file']):
            data['found_files'].append(topojson_file['geog_short_code'])
        else:
            data['missing_files'].append(topojson_file['geog_short_code'])

    return render(request, 'site_setup.html',
                  {
                      'preferences': get_user_preferences(request),
                      'searches': get_user_searches(request),
                      'url': request.get_full_path(),
                      'data': data
                  }, context_instance=RequestContext(request))
