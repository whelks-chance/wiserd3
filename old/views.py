import json
import datetime
import pprint
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.db import connections
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from dataportal3 import models
from dataportal3.utils.userAdmin import get_anon_user
from old import models as old_models

__author__ = 'ubuntu'

@csrf_exempt
def spatial_search(request):

    test_available = False

    response_data = {
        'data': []
    }

    geography_wkt = request.POST.get('geography', '')
    if test_available and (len(request.POST.get('test', '')) or len(geography_wkt) == 0):
        response_data = {'data': [{'area': u'Wales', 'survey_short_title': u'WERS', 'date': '2005 / 04 / 30', 'survey_id': u'sid_wersmq2004', 'survey_id_full': u'sid_wersmq2004                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_412', 'survey_id_full': u'sid_whs2008_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': '', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_03', 'survey_id_full': u'sid_whs2007_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Gwent, Monmouthshire, South East Wales, NP152, South Wales, W01001581', 'survey_short_title': u'LiW Property', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwps2004', 'survey_id_full': u'sid_liwps2004                                                                                                                                                                                                                                                  ', 'areas': [u'NP152', u'Gwent', u'South East Wales', u'Monmouthshire', u'South Wales', u'W01001581']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_03', 'survey_id_full': u'sid_whs2009_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007aq', 'survey_id_full': u'sid_whs2007aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2005 / 09 / 30', 'survey_id': u'sid_whs0306aq', 'survey_id_full': u'sid_whs0306aq                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_03', 'survey_id_full': u'sid_whs2008_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008aq', 'survey_id_full': u'sid_whs2008aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_1315', 'survey_id_full': u'sid_whs2007_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2007 / 07 / 31', 'survey_id': u'sid_liw2007', 'survey_id_full': u'sid_liw2007                                                                                                                                                                                                                                                    ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire 005E', u'Monmouth', u'Gwent', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_1315', 'survey_id_full': u'sid_whs2008_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_412', 'survey_id_full': u'sid_whs2009_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009aq', 'survey_id_full': u'sid_whs2009aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_412', 'survey_id_full': u'sid_whs2007_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2006 / 10 / 13', 'survey_id': u'sid_liwhh2006', 'survey_id_full': u'sid_liwhh2006                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'South Wales', u'Monmouthshire 005E', u'South East Wales', u'NP151']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_1315', 'survey_id_full': u'sid_whs2009_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Monmouthshire, Monmouth, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwhh2004', 'survey_id_full': u'sid_liwhh2004                                                                                                                                                                                                                                                  ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire', u'South East Wales', u'Monmouthshire 005E', u'Monmouth']}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2005 / 08 / 14', 'survey_id': u'sid_liwhh2005', 'survey_id_full': u'sid_liwhh2005                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'Monmouth', u'NP151', u'South Wales', u'Monmouthshire 005E']}], 'success': True}
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
    elif len(geography_wkt) == 0:
        response_data['success'] = False
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")

    search_id = request.POST.get('search_id', '')
    if len(search_id):
        pass
    else:
        print request.user
        user = auth.get_user(request)
        if type(user) is AnonymousUser:
            user = get_anon_user()
        user_profile, created = models.UserProfile.objects.using('new').get_or_create(user=user)
        search = models.Search()
        search.user = user_profile
        search.query = request.POST.get('geography', None)
        search.type = 'spatial'
        search.image_png = request.POST.get('image_png', None)
        search.save()
    response_data['success'] = True

    cursor = connections['survey'].cursor()

    table_cols = "SELECT DISTINCT f_table_name, f_geometry_column FROM geometry_columns where f_table_schema = 'public'"
    cursor.execute(table_cols)
    tables = cursor.fetchall()
    # print tables

    areas = []
    survey_ids = []
    survey_info = {}

    for geoms in tables:
        f_table_name = geoms[0]
        print f_table_name
        f_geometry_column = geoms[1]

        survey_data = {}
        survey_data['areas'] = []

        intersects = "SELECT area_name from " + f_table_name + \
                     " WHERE ST_Intersects(ST_Transform(ST_GeometryFromText('" + geography_wkt + "', 27700), 4326)," + f_geometry_column + ")"

        cursor.execute(intersects)
        area_names = cursor.fetchall()

        area_name = ''
        if len(area_names) > 0:
            # print area_names[0][0].strip()
            areas.append(area_names[0][0])
            area_name = area_names[0][0]
        survey_data['area'] = area_name

        spatials = old_models.SurveySpatialLink.objects.using('survey').filter(spatial_id=geoms[0]).values_list('surveyid', flat=True)

        spatials = list(spatials)

        date = ''
        sid = ''
        survey_short_title = ''
        if len(spatials) > 0:
            # print spatials[0].strip()
            survey_ids.append(spatials[0].strip())
            sid = spatials[0]
            survey_model = old_models.Survey.objects.using('survey').filter(surveyid__in=spatials).values_list('short_title', 'collectionenddate', 'surveyid').distinct()

            for s in survey_model:
                if len(s) > 0:
                    survey_short_title = s[0]
                try:
                    date = s[1].strftime('%Y / %m / %d')
                except:
                    date = ''

        survey_data['survey_short_title'] = survey_short_title
        survey_data['survey_id'] = sid.strip()
        survey_data['survey_id_full'] = sid
        survey_data['date'] = date

        if len(survey_data['survey_id']):
            if survey_info.has_key(survey_data['survey_id']):
                survey_info[survey_data['survey_id']]['areas'].append(survey_data['area'])
                survey_info[survey_data['survey_id']]['area'] = ', '.join(list(set(survey_info[survey_data['survey_id']]['areas'])))
            else:
                survey_info[survey_data['survey_id']] = survey_data

    # response_data['areas'] = areas
    response_data['data'] = survey_info.values()

    # cursor.execute("select table_name from information_schema.tables where table_name like %s limit 30", ['ztab%'])
    # max_value = cursor.fetchone()[0]

    # print response_data

    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


@csrf_exempt
def survey_dc_data(request, wiserd_id):
    wiserd_id = wiserd_id.strip()
    survey_dc_models = old_models.DcInfo.objects.using('survey').all().filter(identifier=wiserd_id).values("identifier", "title", "creator", "subject", "description", "publisher", "contributor", "date", "type", "format", "source", "language", "relation", "coverage", "rights", "user_id", "created", "updated")
    surveys = []
    for dc_model in survey_dc_models:
        surveys.append({
            'data': dc_model,
            'wiserd_id': wiserd_id
        })
    api_data = {
        'url': request.get_full_path(),
        'method': 'survey_dc_data',
        'search_result_data': surveys,
        'results_count': len(surveys),
    }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


@csrf_exempt
def survey_questions(request, wiserd_id):
    wiserd_id = wiserd_id.strip()
    survey_model_ids = old_models.Survey.objects.using('survey').all().filter(identifier=wiserd_id).values_list("surveyid", flat=True)
    survey_question_link_models = old_models.SurveyQuestionsLink.objects.using('survey').all().filter(surveyid__in=survey_model_ids).values_list('qid', flat=True)
    questions_models = old_models.Questions.objects.using('survey').filter(qid__in=survey_question_link_models).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")
    data = []
    for question_model in questions_models:
        # question_model_tidy = [a.strip() for a in question_model if type(a) == 'unicode']
        data.append(question_model)
    api_data = {
        'url': request.get_full_path(),
        'method': 'survey_questions',
        'search_result_data': data,
        'results_count': len(data),
        'wiserd_id': wiserd_id,
        'survey_id': list(survey_model_ids)
    }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


@csrf_exempt
def survey_metadata(request, wiserd_id):
    wiserd_id = wiserd_id.strip()
    survey_models = old_models.Survey.objects.using('survey').all().filter(identifier=wiserd_id).values("surveyid", "identifier", "survey_title", "datacollector", "collectionstartdate", "collectionenddate", "moc_description", "samp_procedure", "collectionsituation", "surveyfrequency", "surveystartdate", "surveyenddate", "des_weighting", "samplesize", "responserate", "descriptionofsamplingerror", "dataproduct", "dataproductid", "location", "link", "notes", "user_id", "created", "updated", "long", "short_title", "spatialdata")
    surveys = []
    for survey_model in survey_models:
        surveys.append({
            'data': survey_model,
            'wiserd_id': wiserd_id
        })
    api_data = {
        'url': request.get_full_path(),
        'method': 'survey_metadata',
        'search_result_data': surveys,
        'results_count': len(surveys),
    }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


@csrf_exempt
def survey_questions_results(request, question_id):
    question_id = question_id.strip()
    question_response_link_models = old_models.QuestionsResponsesLink.objects.using('survey').all().filter(qid=question_id).values('responseid')
    question_responses = []
    if len(question_response_link_models):
        question_response_models = old_models.Responses.objects.using('survey').all().filter(responseid__in=question_response_link_models).values()
        for question_response_model in question_response_models:
            question_responses.append({
                'data': question_response_model,
                'question_id': question_id
            })
    api_data = {
        'url': request.get_full_path(),
        'method': 'survey_questions_results',
        'search_result_data': question_responses,
        'results_count': len(question_responses),
    }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


def search_survey_question(request):
    search_terms = request.GET.get('search_terms', '')

    print pprint.pformat(request.GET)

    ors = search_terms.split(',')
    api_data = text_search(search_terms)
    api_data['url'] = request.get_full_path()
    return render(request, 'index.html',
                  {'data': api_data},
                  context_instance=RequestContext(request))


def text_search(search_terms):
    fields = ("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "type", "notes", "updated")

    # q_terms = []
    # for term in search_terms.split():
    #     q_terms.append(Q())

    search_terms = search_terms.replace(' ', ' & ')
    search_terms = search_terms.replace('+', ' & ')

    questions_models = old_models.Questions.objects.search(search_terms, raw=True).using('survey').values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

    data = []
    for question_model in questions_models:
        if question_model['thematic_tags'] == 'System.Windows.Forms.ListBox+SelectedObjectCollection':
            question_model['thematic_tags'] = ''
        data.append(question_model)

    api_data = {
        'fields': fields,
        'method': 'search_survey_question',
        'search_result_data': data,
        'results_count': len(data),
        'search_term': search_terms
    }
    return api_data


def date_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d T %H:%M:%S %Z')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    # Let the base class default method raise the TypeError
    else:
        print (type(object), object)
        print pprint.pformat(object.__dict__)
        enc = json.JSONEncoder()
        return enc.default(enc, obj)
        # return obj


@csrf_exempt
def survey_question(request, question_id):
    questions_models = old_models.Questions.objects.using('survey').filter(qid=question_id).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")
    data = []
    for question_model in questions_models:
        # question_model_tidy = [a.strip() for a in question_model if type(a) == 'unicode']
        data.append(question_model)
    api_data = {
        'url': request.get_full_path(),
        'method': 'question_data',
        'search_result_data': data,
        'results_count': len(data),
        'question_id': question_id,
    }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")


@csrf_exempt
def survey_questions_results_table(request, question_id):
    question_id = question_id.strip()

    question_response_link_models = old_models.QuestionsResponsesLink.objects.using('survey').all().filter(qid=question_id).values('responseid')

    question_responses = []
    columns = []
    results_with_keys = []

    if len(question_response_link_models):
        question_response_models = old_models.Responses.objects.using('survey').all().filter(responseid__in=question_response_link_models).values()

        cursor = connections['survey'].cursor()
        cursor.execute("select * from " + question_response_models[0]['table_ids'])
        ztab_tables = cursor.fetchall()

        # print ztab_tables

        for question_response_model in ztab_tables:
            question_responses.append(question_response_model)

        cursor.execute("select column_name from information_schema.columns where table_name = '" + question_response_models[0]['table_ids'] + "'")
        column_names = cursor.fetchall()

        # print column_names

        for column_data in column_names:
            columns.append(column_data[0])

        for res in question_responses:
            entry = {}
            for a in range(0, len(columns)):
                entry[columns[a]] = res[a]
            results_with_keys.append(entry)

    api_data = {
        'url': request.get_full_path(),
        'method': 'survey_questions_results_table',
        # 'search_result_data': question_responses,
        'search_result_data': results_with_keys,
        'columns': columns,
        'results_count': len(results_with_keys),
    }

    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")
