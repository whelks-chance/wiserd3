from django.shortcuts import render
from django.template import RequestContext


def index(request):
    return render(request, 'index.html', {}, context_instance=RequestContext(request))


def blank(request):
    return render(request, 'blank.html', {}, context_instance=RequestContext(request))


def tables(request):
    return render(request, 'tables.html', {}, context_instance=RequestContext(request))


def map(request):
    return render(request, 'map.html', {}, context_instance=RequestContext(request))
