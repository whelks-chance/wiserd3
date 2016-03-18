# Connecting to AllAuth Signals
from allauth.account import signals
from django.dispatch import receiver

__author__ = 'lostvisions'


@receiver(signals.user_signed_up)
def new_user_signup(sender, **kwargs):
    from models import UserProfile

    print "signed up a user!!!!"
    # time_now = datetime.datetime.now()
    # time_now = timezone.now()
    lv_user = UserProfile(user=kwargs['user'])
    # lv_user = UserProfile(user=kwargs['user'], sign_up_timestamp=time_now)
    lv_user.save()


@receiver(signals.user_logged_in)
def user_logged_in(sender, **kwargs):
    print 'logged in', kwargs['user']


@receiver(signals.email_confirmed)
def user_email_confirmed(sender, request, email_address, **kwargs):
    print 'gyisfdgsduifsd'
    print kwargs
    print 'email confirmed', sender, request, email_address