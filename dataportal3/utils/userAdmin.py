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


def survey_visible_to_user(survey_id, user_profile):
    # Assume access is OK unless a visibility is set
    # Switch access to False if any visibility levels are set
    # Then keep assuming false until a single True is seen
    # 9 No's and 1 Yes means Yes
    allowed = True
    access_data = []

    # Find any specific visibility metadata for this survey
    # It is possible that multiple visibilities may be set for a single survey
    survey_visibilities = models.SurveyVisibilityMetadata.objects.filter(survey__identifier=survey_id)
    if survey_visibilities.count():

        # We have at least one visibility set, so assume False to begin with
        # We'll enable access again if we need to
        allowed = False

        # Search through each visibility metadata entry to check access is allowed
        for survey_vis in survey_visibilities:

            # Each visibility has a primary contact to designate access to users
            # This person may or may not be a defined member of the associated user group,
            # but will require at least a shell user account within the dataportal
            contact = survey_vis.primary_contact.user

            if survey_vis.survey_visibility.visibility_id == 'SUR_VIS_ALL':
                # Allow access as visibility is Allow All
                allowed = True

            elif survey_vis.survey_visibility.visibility_id == 'SUR_VIS_NONE':
                # Deny access - be careful using this, as race conditions may apply
                # TODO what happens if the survey is allowed by one group and denied by another?
                allowed = False

            elif survey_vis.survey_visibility.visibility_id == 'SUR_VIS_GROUP':
                # Grab all user groups for this surveys
                user_group_members = survey_vis.user_group_survey_collection.user_group.user_group_members.all()

                survey_collection_name = survey_vis.user_group_survey_collection.name
                survey_collection_user_group_name = survey_vis.user_group_survey_collection.user_group.name
                print survey_collection_name, survey_collection_user_group_name, user_group_members

                if user_profile in user_group_members:
                    allowed = True

                    access_data.append({
                        'contact': contact.username,
                        'survey_collection_name': survey_collection_name,
                        'survey_collection_user_group_name': survey_collection_user_group_name
                    })

    return allowed, access_data

