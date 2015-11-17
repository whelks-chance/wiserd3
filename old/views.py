import json
import datetime
import pprint
import django
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.db import connections
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
import requests
from dataportal3 import models
from dataportal3.utils.userAdmin import get_anon_user
from old import survey_models as old_models
from django.apps import apps

__author__ = 'ubuntu'

@csrf_exempt
def spatial_search(request):
    # print request.POST

    test_available = False
    search_uid = ''

    response_data = {
        'data': []
    }

    geography_wkt = request.POST.get('geography', '')

    # A test set of data for if we don't want to wait for the DB
    if test_available and (len(request.POST.get('test', '')) or len(geography_wkt) == 0):
        response_data = {'data': [{'area': u'Wales', 'survey_short_title': u'WERS', 'date': '2005 / 04 / 30', 'survey_id': u'sid_wersmq2004', 'survey_id_full': u'sid_wersmq2004                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_412', 'survey_id_full': u'sid_whs2008_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': '', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_03', 'survey_id_full': u'sid_whs2007_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Gwent, Monmouthshire, South East Wales, NP152, South Wales, W01001581', 'survey_short_title': u'LiW Property', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwps2004', 'survey_id_full': u'sid_liwps2004                                                                                                                                                                                                                                                  ', 'areas': [u'NP152', u'Gwent', u'South East Wales', u'Monmouthshire', u'South Wales', u'W01001581']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_03', 'survey_id_full': u'sid_whs2009_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007aq', 'survey_id_full': u'sid_whs2007aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2005 / 09 / 30', 'survey_id': u'sid_whs0306aq', 'survey_id_full': u'sid_whs0306aq                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_03', 'survey_id_full': u'sid_whs2008_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008aq', 'survey_id_full': u'sid_whs2008aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_1315', 'survey_id_full': u'sid_whs2007_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2007 / 07 / 31', 'survey_id': u'sid_liw2007', 'survey_id_full': u'sid_liw2007                                                                                                                                                                                                                                                    ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire 005E', u'Monmouth', u'Gwent', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_1315', 'survey_id_full': u'sid_whs2008_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_412', 'survey_id_full': u'sid_whs2009_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009aq', 'survey_id_full': u'sid_whs2009aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_412', 'survey_id_full': u'sid_whs2007_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2006 / 10 / 13', 'survey_id': u'sid_liwhh2006', 'survey_id_full': u'sid_liwhh2006                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'South Wales', u'Monmouthshire 005E', u'South East Wales', u'NP151']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_1315', 'survey_id_full': u'sid_whs2009_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Monmouthshire, Monmouth, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwhh2004', 'survey_id_full': u'sid_liwhh2004                                                                                                                                                                                                                                                  ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire', u'South East Wales', u'Monmouthshire 005E', u'Monmouth']}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2005 / 08 / 14', 'survey_id': u'sid_liwhh2005', 'survey_id_full': u'sid_liwhh2005                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'Monmouth', u'NP151', u'South Wales', u'Monmouthshire 005E']}], 'success': True}
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")

    # We need a geography to do a spatial search!
    # This may come from the search database, via the front end, in a request (a bit roundabout!)
    elif len(geography_wkt) == 0:
        response_data['success'] = False
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")

    geojson = request.POST.get('geojson', '')


    # If we have a search ID, return the data for that ID
    search_id = request.POST.get('search_id', '')
    if len(search_id):
        pass
    else:
        # If we're missing a search ID, create a new search record for this request

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

        # If we have a center point for this geography, try and find a city/town/etc name for it
        center_lat_lng = request.POST.getlist('centre_lat_lng[]', None)
        if center_lat_lng:
            print center_lat_lng
            lat = center_lat_lng[0]
            lng = center_lat_lng[1]
            nominatim_url = 'http://nominatim.openstreetmap.org/reverse?format=json&lat={0}&lon={1}&zoom=18&addressdetails=1'.format(lat, lng)

            s = requests.Session()
            s.headers.update({'referer': 'data.wiserd.ac.uk'})
            nominatim_request = s.get(nominatim_url)

            # print nominatim_url
            # nominatim_request = requests.request('get', nominatim_url)

            nominatim_json = json.loads(nominatim_request.text)
            print pprint.pformat(nominatim_json)

            if 'state' in nominatim_json['address']:
                search.readable_name = nominatim_json['address']['state']
            if 'county' in nominatim_json['address']:
                search.readable_name = nominatim_json['address']['county']
            if 'city' in nominatim_json['address']:
                search.readable_name = nominatim_json['address']['city']

            geo_area = request.POST.get('geo_area_km2', None)
            if geo_area:
                geo_area = float(geo_area)
                print geo_area

                if geo_area < 20:
                    if 'town' in nominatim_json['address']:
                        search.readable_name = nominatim_json['address']['town']
                    if 'village' in nominatim_json['address']:
                        search.readable_name = nominatim_json['address']['village']

                if geo_area < 10:
                    if 'suburb' in nominatim_json['address']:
                        search.readable_name = nominatim_json['address']['suburb']

        search.save()
        search_uid = str(search.uid)

    response_data['success'] = True
    response_data['uid'] = search_uid

    uid_only = request.POST.get('uid_only', False)
    if uid_only:
        # we only record what was searched for, do not complete the search yet
        pass
    else:

        # cursor = connections['survey'].cursor()

        # table_cols = "SELECT DISTINCT f_table_name, f_geometry_column FROM geometry_columns where f_table_schema = 'public'"
        # cursor.execute(table_cols)
        # tables = cursor.fetchall()
        # # print tables

        geometry_columns = old_models.GeometryColumns.objects.using('survey').filter(f_table_schema='public')

        areas = []
        survey_ids = []
        survey_info = {}

        for geoms in geometry_columns:
            f_table_name = str(geoms.f_table_name).replace('_', '')
            # print f_table_name
            f_geometry_column = geoms.f_geometry_column

            survey_data = {}
            survey_data['areas'] = []

            # try:
            spatial_layer_table = apps.get_model(app_label='old', model_name=f_table_name)

            # intersects = "SELECT area_name from " + f_table_name + \
            #              " WHERE ST_Intersects(ST_Transform(ST_GeometryFromText('" + geography_wkt + "', 27700), 4326)," + f_geometry_column + ")"

            area_names = spatial_layer_table.objects.using('survey').extra(
                select={
                    'geometry': 'ST_Intersects(ST_Transform(ST_GeometryFromText("' + geography_wkt + '", 27700), 4326), ' + geoms.f_geometry_column +')'
                }
            ).values('area_name')

            # print area_names
            # cursor.execute(intersects)
            # area_names = cursor.fetchall()

            area_name = ''
            if len(area_names) > 0:
                # print area_names[0][0].strip()
                areas.append(area_names[0]['area_name'])
                area_name = area_names[0]['area_name']
            survey_data['area'] = area_name

            spatials = old_models.SurveySpatialLink.objects.using('survey').filter(spatial_id=geoms.f_table_name).values_list('surveyid', flat=True)

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

                    area_list = list(set(survey_info[survey_data['survey_id']]['areas']))
                    # cleaned_list = [area for area in area_list if not has_numbers(area)]
                    cleaned_list = area_list

                    survey_info[survey_data['survey_id']]['area'] = ', '.join(cleaned_list)
                else:
                    survey_info[survey_data['survey_id']] = survey_data

            # except Exception as e:
            #     print e

        # response_data['areas'] = areas
        response_data['data'] = survey_info.values()

        # cursor.execute("select table_name from information_schema.tables where table_name like %s limit 30", ['ztab%'])
        # max_value = cursor.fetchone()[0]

        # print response_data

    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


@csrf_exempt
def survey_dc_data(request, wiserd_id):
    wiserd_id = wiserd_id.strip()
    # survey_dc_models = old_models.DcInfo.objects.using('survey').all().filter(identifier=wiserd_id).values("identifier", "title", "creator", "subject", "description", "publisher", "contributor", "date", "type", "format", "source", "language", "relation", "coverage", "rights", "user_id", "created", "updated")
    survey_dc_models = models.DcInfo.objects.all().filter(identifier=wiserd_id).values("identifier", "title", "creator", "subject", "description", "publisher", "contributor", "date", "type__dc_type_title", "format__dc_format_title", "source", "language__dc_language_title", "relation", "coverage", "rights", "user_id", "created", "updated")

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

    # survey_model_ids = old_models.Survey.objects.using('survey').all().filter(identifier=wiserd_id).values_list("surveyid", flat=True)
    # survey_question_link_models = old_models.SurveyQuestionsLink.objects.using('survey').all().filter(surveyid__in=survey_model_ids).values_list('qid', flat=True)
    # questions_models = old_models.Questions.objects.using('survey').filter(qid__in=survey_question_link_models).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

    survey_model_ids = models.Survey.objects.all().filter(identifier=wiserd_id).values_list("surveyid", flat=True)
    questions_models = models.Survey.objects.get(identifier=wiserd_id).question_set.all().values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type__q_type_text", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

    data = []
    for question_model in questions_models:
        # question_model_tidy = [a.strip() for a in question_model if type(a) == 'unicode']
        question_model['type'] = question_model['type__q_type_text']
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
    # survey_models = old_models.Survey.objects.using('survey').all().filter(identifier=wiserd_id).values("surveyid", "identifier", "survey_title", "datacollector", "collectionstartdate", "collectionenddate", "moc_description", "samp_procedure", "collectionsituation", "surveyfrequency", "surveystartdate", "surveyenddate", "des_weighting", "samplesize", "responserate", "descriptionofsamplingerror", "dataproduct", "dataproductid", "location", "link", "notes", "user_id", "created", "updated", "long", "short_title", "spatialdata")
    survey_models = models.Survey.objects.all().filter(identifier=wiserd_id).values("surveyid", "identifier", "survey_title", "datacollector", "collectionstartdate", "collectionenddate", "moc_description", "samp_procedure", "collectionsituation", "surveyfrequency", "surveystartdate", "surveyenddate", "des_weighting", "samplesize", "responserate", "descriptionofsamplingerror", "dataproduct", "dataproductid", "location", "link", "notes", "user_id", "created", "updated", "long", "short_title", "spatialdata")
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
    question_responses = []

    # question_response_link_models = old_models.QuestionsResponsesLink.objects.using('survey').all().filter(qid=question_id).values('responseid')
    # if len(question_response_link_models):
    #     question_response_models = old_models.Responses.objects.using('survey').all().filter(responseid__in=question_response_link_models).values()
    #     for question_response_model in question_response_models:
    #         question_responses.append({
    #             'data': question_response_model,
    #             'question_id': question_id
    #         })

    question_response_models = models.Response.objects.all().filter(question__qid=question_id).values(
        "responseid", "responsetext", "response_type__response_name", "routetype", "table_ids",
        "computed_var", "checks", "route_notes", "user_id", "created", "updated")

    for question_response_model in question_response_models:
        question_response_model['response_type'] = question_response_model['response_type__response_name']
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


def text_search(search_terms):
    fields = ("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "type", "notes", "updated")

    # q_terms = []
    # for term in search_terms.split():
    #     q_terms.append(Q())

    search_terms = search_terms.replace(' ', ' & ')
    search_terms = search_terms.replace('+', ' & ')

    # questions_models = old_models.Questions.objects.search(search_terms, raw=True).using('survey').values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")
    questions_models = models.Question.objects.search(search_terms, raw=True).distinct("qid").values("survey__identifier", "survey__collectionstartdate", "survey__survey_title", "qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type__q_type_text", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

    print questions_models.query

    data = []
    for question_model in questions_models:
        # question_model_tidy = [a.strip() for a in question_model if type(a) == 'unicode']
        question_model['type'] = question_model['type__q_type_text']
        # data.append(question_model)
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
    # elif isinstance(obj, django.db.models.query.ValuesQuerySet):
    #     return '##DB object##'
    # Let the base class default method raise the TypeError
    else:
        print 'err type', type(obj)
        print 'err obj', obj
        print pprint.pformat(obj.__dict__)
        enc = json.JSONEncoder()
        return enc.default(enc, obj)
        # return obj


@csrf_exempt
def survey_question(request, question_id):
    # questions_models = old_models.Questions.objects.using('survey').filter(qid=question_id).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")
    questions_models = models.Question.objects.filter(qid=question_id).values("survey__identifier", "qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type__q_type_text", "variableid", "notes", "user_id", "created", "updated", "qtext_index", "survey__surveyid")
    data = []
    for question_model in questions_models:
        # question_model_tidy = [a.strip() for a in question_model if type(a) == 'unicode']
        question_model['type'] = question_model['type__q_type_text']
        data.append(question_model)
    api_data = {
        'url': request.get_full_path(),
        'method': 'question_data',
        'survey': questions_models[0]['survey__identifier'],
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
