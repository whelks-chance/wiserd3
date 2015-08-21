from django.contrib import auth
from dataportal3 import models
from dataportal3.models import UserProfile

__author__ = 'ubuntu'
from django.contrib.auth.models import User, AnonymousUser


def get_anon_user():
    try:
        user = User.objects.get(username='Anon Y Mouse')
    except:
        user = User.objects.create_user(username='Anon Y Mouse')

    #     check for UserProfile
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return user


def get_user_searches(request):
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    user_profile = UserProfile.objects.get(user=user)
    searches = models.Search.objects.filter(user=user_profile).order_by('-datetime')

    # I bet there's a single line way to do this...
    search_by_type = {}
    spatial_searches = []
    survey_searches = []
    question_searches = []
    text_searches = []
    for search in searches:
        if search.type == 'spatial':
            spatial_searches.append(search)
        if search.type == 'survey':
            survey_searches.append(search)
        if search.type == 'question':
            question_searches.append(search)
        if search.type == 'text':
            text_searches.append(search)
    search_by_type = {
        'spatial': spatial_searches,
        'survey': survey_searches,
        'question': question_searches,
        'text': text_searches
    }
    return search_by_type