from django.contrib import auth
from dataportal3 import models
from dataportal3.models import UserProfile, UserPreferences
from django.contrib.auth.models import User, AnonymousUser

__author__ = 'ubuntu'


def get_anon_user():
    try:
        user = User.objects.get(username='Anon Y Mouse')
    except:
        user = User.objects.create_user(username='Anon Y Mouse')

    #     check for UserProfile
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return user


def get_request_user(request=None):
    try:
        # user = models.User.objects.get(username=request.user)
        dataportal_user = UserProfile.objects.get(user__username=request.user)
        return dataportal_user
    except Exception as e1:
        print e1
        # hack using the exception to use anonymous user if not logged in
        return UserProfile.objects.get(user=get_anon_user())


def get_user_preferences(request):
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        # TODO remove this hack.
        # TODO It defaults to Anon user if an unrecognised user is logged in.
        # TODO Should figure out how this impossible thing happened
        user = get_anon_user()
        user_profile = UserProfile.objects.get(user=user)

    user_prefs, created = UserPreferences.objects.get_or_create(user=user_profile)
    return user_prefs


def get_user_searches(request):
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        # TODO remove this hack.
        # TODO It defaults to Anon user if an unrecognised user is logged in.
        # TODO Should figure out how this impossible thing happened
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