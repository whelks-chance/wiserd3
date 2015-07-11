import json
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser

from django.db import connections
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from dataportal3 import models
from dataportal3.models import UserProfile
from dataportal3.utils.userAdmin import get_anon_user, get_user_searches


def index(request):
    return render(request, 'index.html',
                  {'searches': get_user_searches(request)},
                  context_instance=RequestContext(request))


def blank(request):
    return render(request, 'blank.html', {}, context_instance=RequestContext(request))


def tables(request):
    search_id = request.GET.get('search_id', '')
    geom = ''
    if len(search_id):
        search = models.Search.objects.get(uid=search_id)
        if search.type == 'spatial':
            geom = search.query

    return render(request, 'tables.html',
                  {
                      'searches': get_user_searches(request),
                      'geom': geom
                  },
                  context_instance=RequestContext(request))


def map_search(request):
    return render(request, 'map.html',
                  {'searches': get_user_searches(request)},
                  context_instance=RequestContext(request))

