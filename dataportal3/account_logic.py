from allauth.account.adapter import DefaultAccountAdapter
from dataportal3.utils.userAdmin import get_request_user
from django.core.urlresolvers import reverse

__author__ = 'ubuntu'


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        request_user = get_request_user(request)
        # If the user hasn't been shown the welcome screen before, show it now.
        if not request_user.init_user:
            return reverse('welcome')
        else:
            print 'user role', request_user.role
            if request_user.role == 'naw':
                return reverse('naw_dashboard')
            else:
                return reverse('index')
