import json

from django.http import HttpResponse, Http404


# Create your views here.
from cancommute import models
from djgeojson.serializers import Serializer as GeoJSONSerializer


def cancommute_to_location(request):

    csduid = request.GET.get('csduid', None)

    if csduid:
        destination_model = models.CanadaShape.objects.get(csduid=csduid)
        destination_location_name = destination_model.csdname

        route_models = models.Route.objects.filter(destination__csduid=csduid)

        origin_is_destination_total = ''
        origin_is_destination = route_models.filter(origin__csduid=csduid)
        if origin_is_destination.count():
            origin_is_destination_total = origin_is_destination[0].total

        s = GeoJSONSerializer().serialize(
            route_models,
            use_natural_keys=True,
            with_modelname=False,
        )

        geo = json.loads(s)
        for e in geo['features']:
            e['properties']['REMOTE_VALUE'] = e['properties']['total']

        geo['properties'] = {'name': 'Commute route'}
        geo['properties']['remote_value_key'] = 'total'
        geo['properties']['number_of_routes'] = route_models.count()
        geo['properties']['origin_is_destination'] = origin_is_destination_total
        geo['properties']['destination_location_name'] = {
            'eng': destination_location_name,
            'prname':destination_model.prname
        }

        s = json.dumps(geo)

        return HttpResponse(s, content_type="application/json")
    else:
        raise Http404