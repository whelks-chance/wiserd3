# Connecting to AllAuth Signals
from pprint import pformat

from allauth.account import signals
from django.contrib.auth import user_logged_out
from django.dispatch import receiver
from django.utils.translation import LANGUAGE_SESSION_KEY

from dataportal3.models import UserProfile, UserPreferences, UserLanguage
from dataportal3.utils.userAdmin import set_session_preferred_language


@receiver(signals.user_signed_up)
def new_user_signup(sender, **kwargs):

    print "signed up a user!!!!"
    # time_now = datetime.datetime.now()
    # time_now = timezone.now()
    lv_user = UserProfile(user=kwargs['user'])
    # lv_user = UserProfile(user=kwargs['user'], sign_up_timestamp=time_now)
    lv_user.save()

    user_language_title = 'English'
    request = kwargs['request']
    if LANGUAGE_SESSION_KEY in request.session:
        if request.session[LANGUAGE_SESSION_KEY] == 'cy':
            user_language_title = 'Welsh'

    language = UserLanguage.objects.get(user_language_title=user_language_title)
    lv_user_preferences = UserPreferences()
    lv_user_preferences.preferred_language = language
    lv_user_preferences.user = lv_user
    lv_user_preferences.save()

@receiver(signals.user_logged_in)
def user_logged_in(sender, user, request, **kwargs):
    print user
    # print pformat(request.__dict__)

    print set_session_preferred_language(request)
    print 'logged in', user


@receiver(user_logged_out)
def user_logged_out(sender, user, request, **kwargs):
    print user

    print set_session_preferred_language(request, reset=True)
    print 'logged out', user


@receiver(signals.email_confirmed)
def user_email_confirmed(sender, request, email_address, **kwargs):
    print 'email confirmed', sender, request, email_address