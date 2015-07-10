__author__ = 'ubuntu'
from django.contrib.auth.models import User


def get_anon_user():
    try:
        user = User.objects.get(username='Anon Y Mouse')
    except:
        user = User.objects.create_user(username='Anon Y Mouse')
    return user