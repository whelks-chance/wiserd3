import os
import pprint

from datetime import datetime
from django.utils.translation import get_language

from dataportal3 import models
from dataportal3.utils.userAdmin import get_user_preferences, get_request_user
from wiserd3 import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def usage_tracker(request):
    userr = get_request_user(request)

    # print 'User loaded a page : ', userr.user.username, datetime.now(), get_client_ip(request), request.get_full_path()
    if 'admin_tools' not in request.get_full_path():
        ut = models.UserTracking()
        ut.user = userr
        ut.ip = get_client_ip(request)
        ut.url = request.get_full_path()
        ut.save()

    return {}


def is_dev_processor(request):

    use_welsh = False
    user_prefs = get_user_preferences(request)
    assert isinstance(user_prefs, models.UserPreferences)
    if user_prefs.preferred_language:
        if user_prefs.preferred_language.user_language_title == 'Welsh':
            use_welsh = True

    if get_language() == 'cy':
        use_welsh = True

    if use_welsh:
        media_lang = settings.MEDIA_CY
    else:
        media_lang = settings.MEDIA_DEFAULT

    data = {
        'is_dev': settings.IS_DEV,
        'use_welsh': use_welsh,
        'media_lang': media_lang
    }

    return data

