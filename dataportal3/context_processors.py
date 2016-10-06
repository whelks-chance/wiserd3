import os

from django.utils.translation import get_language

from dataportal3 import models
from dataportal3.utils.userAdmin import get_user_preferences
from wiserd3 import settings


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

