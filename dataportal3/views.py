import ast
import json
import yaml
import pprint
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.core.serializers import serialize

from django.db import connections
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from dataportal3 import models
from dataportal3.utils.userAdmin import get_anon_user, get_user_searches


def index(request):
    return render(request, 'index.html',
                  {'searches': get_user_searches(request)},
                  context_instance=RequestContext(request))


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
    return render(request, 'map.html',
                  {
                      'searches': get_user_searches(request)
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


def get_geojson(request):
    shape_table_object = models.XSidLiwhh2005Ua.objects.using('survey_gis').all()
    geojson_layers = shape_table_object.extra(
        select={
            'geometry': 'ST_AsGeoJSON("the_geom")'
        }
    ).values('area_name', 'response_rate', 'geometry')

    print type(geojson_layers)

    shape_list = list(geojson_layers)
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
            print key
            if key is not 'geometry':
                shape_properties[key] = shape[key]
                print shape[key], shape_properties[key]

        rgb_int = float(shape_properties['response_rate']) * 2.54
        rgb_tuple = (rgb_int, rgb_int, rgb_int)
        hex_code = '#%02x%02x%02x' % rgb_tuple
        shape_properties['color'] = hex_code
        shape_properties['opacity'] = 0.1

        shape_list_group = {
            'type': 'Feature',
            'geometry': {
                'type': 'MultiPolygon',
                'coordinates': ast.literal_eval(shape['geometry'])['coordinates']
            },
            'properties': shape_properties
        }

        shape_feature_list.append(shape_list_group)

    geojsonFeature = {
        "type": "FeatureCollection",
        "features": shape_feature_list,
        "properties": {
            'name': 'XSidLiwhh2005Ua',
            'b': 2
        }
    }

    # geojsonFeature = {
    #     "type": "FeatureCollection",
    #     "features": [
    #         {
    #             "type": "Feature",
    #             "geometry": {
    #                 "type": "Point",
    #                 "coordinates": [0, 0]
    #             },
    #             "properties": {
    #                 "name": "null island"
    #             }
    #         }
    #     ]
    # }

    return HttpResponse(json.dumps(geojsonFeature), content_type="application/json")
