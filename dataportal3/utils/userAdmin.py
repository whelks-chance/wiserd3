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
    return user

def get_user_searches(request):
    user = auth.get_user(request)
    if type(user) is AnonymousUser:
        user = get_anon_user()
    user_profile = UserProfile.objects.get(user=user)
    searches = models.Search.objects.filter(user=user_profile)
    return searches