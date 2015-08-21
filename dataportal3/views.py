from datetime import datetime
import json
from BeautifulSoup import BeautifulSoup
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import operator
from dataportal3 import models
from dataportal3.utils.userAdmin import get_anon_user, get_user_searches
import requests
from old.views import text_search, date_handler
from django.core.cache import cache


def index(request):
    return render(request, 'index.html',
                  {'searches': get_user_searches(request)},
                  context_instance=RequestContext(request))


def search_survey_question_gui(request):
    search_terms = request.GET.get('search_terms', '')
    ors = search_terms.split(',')
    return render(request, 'search.html', {
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
                      'searches': get_user_searches(request),
                      'survey_id': survey_id}
                  ,
                  context_instance=RequestContext(request))


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
                      'searches': get_user_searches(request),
                      'search_id': search_id,
                      'geom': geom,
                      'image_png': image_png,
                      'search_name': search_name
                  },
                  context_instance=RequestContext(request))


def map_search(request):
    print request.GET

    capabilities = requests.get('http://inspire.wales.gov.uk/maps/wms?request=getCapabilities&version=1.3.0')
    soup = BeautifulSoup(capabilities.text)
    x = soup.wms_capabilities.capability.findAll('layer', queryable=1)
    b = []
    for y in x:
        b.append({
            'tile_name': [z.string for z in y.findAll('name')][0],
            'name': [z.string for z in y.findAll('title')][0]
        })
    surveys = request.GET.getlist('surveys', [])

    wiserd_layers = models.GeometryColumns.objects.using('survey').filter(f_table_schema='spatialdata')
    wiserd_layers_clean = []
    for w_layer in wiserd_layers:
        wiserd_layers_clean.append({
            'display_name': w_layer.f_table_name.replace('_', ' ').title(),
            'table_name': w_layer.f_table_name
        })

    return render(request, 'map.html',
                  {
                      'searches': get_user_searches(request),
                      'surveys': json.dumps(surveys),
                      'wms_layers': b,
                      'wiserd_layers': wiserd_layers_clean
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
                      'searches': get_user_searches(request),
                      'question_id': question_id
                  },
                  context_instance=RequestContext(request))

@csrf_exempt
def edit_metadata(request):
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

    # Any failure in here results in sending the success as being False, as set above
    # Add whatever the error message is here. Used in debugging, ideally should not be shown to user
    except Exception as e:
        print e
        edit_metadata_response['error'] = str(e)

    return HttpResponse(json.dumps(edit_metadata_response, indent=4), content_type="application/json")


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

        geojson_layers = shape_table_object.extra(
            select={
                'geometry': 'ST_AsGeoJSON(ST_Transform(ST_SetSRID("the_geom", 27700),4326))'
            }
        ).values('geometry')

    if layer_type == 'survey':
        surveys = request.POST.getlist('layer_names')[0]

        print surveys

        q_obj_sids = [Q(surveyid__istartswith=sid) for sid in surveys]
        qs = reduce(operator.or_, q_obj_sids)
        spatial_link = models.SurveySpatialLink.objects.using('survey').filter(qs).values('spatial_id', 'admin_areas', 'surveyid')[0]

        # shape_table_object = models.XSidLiwhh2005Ua.objects.using('survey_gis').all()

        spatial_table_name = str(spatial_link['spatial_id']).replace('_', '').strip()
        spatial_table = apps.get_model(
            app_label='dataportal3',
            model_name=spatial_table_name
        )
        shape_table_object = spatial_table.objects.using('survey_gis').all()

        geojson_layers = shape_table_object.extra(
            select={
                'geometry': 'ST_AsGeoJSON("the_geom")'
            }
        ).values('area_name', 'response_rate', 'geometry')

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
    return render(request, 'file_management.html',
                  {'searches': get_user_searches(request)},
                  context_instance=RequestContext(request))

# TODO dont be csrf exempt, check logged in
@csrf_exempt
def upload_shapefile(request):
    print request.POST
    print request.GET
    print request.FILES

    id = request.POST['id']

    path = '/tmp/portal/shapefiles/%s' % id

    f = request.FILES['shapefile_upload']

    destination = open(path, 'wb+')

    for chunk in f.chunks():

        destination.write(chunk)

    destination.close()

    # return status to client


@csrf_exempt
def get_upload_progress(request):
    cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], request.GET['X-Progress-ID'])
    data = cache.get(cache_key)
    return HttpResponse(json.dumps(data))
