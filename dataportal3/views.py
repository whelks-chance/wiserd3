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
from dataportal3.utils.userAdmin import get_anon_user


def index(request):
    return render(request, 'index.html', {}, context_instance=RequestContext(request))


def blank(request):
    return render(request, 'blank.html', {}, context_instance=RequestContext(request))


def tables(request):
    return render(request, 'tables.html', {}, context_instance=RequestContext(request))


def map(request):
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()

    user_profile = UserProfile.objects.get(user=user)

    searches = models.Search.objects.filter(user=user_profile)

    return render(request, 'map.html', {'searches': searches}, context_instance=RequestContext(request))

