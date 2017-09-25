import json

from django.http import HttpResponse, Http404


# Create your views here.
from cancommute import models
from djgeojson.serializers import Serializer as GeoJSONSerializer


def cancommute_to_location(request):

    csduid = request.GET.get('csduid', None)

    if csduid:
        origin_models = models.Route.objects.filter(destination__csduid=csduid)
        # not_same_area_models = origin_models.exclude(origin__csduid=csduid)

        origin_is_destination_total = ''
        origin_is_destination = origin_models.filter(origin__csduid=csduid)
        if origin_is_destination.count():
            origin_is_destination_total = origin_is_destination[0].total

        # origin_models = models.Route.objects.all()

        s = GeoJSONSerializer().serialize(
            origin_models,
            use_natural_keys=True,
            with_modelname=False,
        )

        geo = json.loads(s)
        for e in geo['features']:
            e['properties']['REMOTE_VALUE'] = e['properties']['total']

        geo['properties'] = {'name': 'Commute route'}
        geo['properties']['remote_value_key'] = 'total'
        geo['properties']['number_of_routes'] = origin_models.count()
        geo['properties']['origin_is_destination'] = origin_is_destination_total

        s = json.dumps(geo)

        return HttpResponse(s, content_type="application/json")
    else:
        raise Http404