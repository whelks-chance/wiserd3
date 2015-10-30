import json
import os
import pprint
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections, ConnectionRouter, DEFAULT_DB_ALIAS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import django
django.setup()

from old import survey_models as old_models
from dataportal3 import models as new_models


__author__ = 'ubuntu'



def build_ztab_table():

    # query = 'select table_name from information_schema.tables where table_name like %s limit 10'
    # variables = ['ztab_']

    # ztab_tables = models.ztabResponseOptions.objects.db_manager().raw(query, variables)

    from django.db import connection

    cursor = connections['survey'].cursor()

    # qid = 'qid_liw2007q51-s1'
    #
    # cursor.execute("Select table_name, column_name from information_schema.columns " +
    #                "where lower(table_name) in " +
    #                "(select lower(table_ids) from responses where responseID = " +
    #                "( SELECT responseID FROM questions_responses_link where qid = %s)) " +
    #                "and column_name != 'table_pk' and column_name != 'user_id' and " +
    #                "column_name != 'date_time' and column_name != 'res_table_id'", [qid, ])
    #
    # ztab_from_qid = cursor.fetchall()

    cursor.execute("select table_name from information_schema.tables where table_name like %s limit 30", ['ztab%'])
    # max_value = cursor.fetchone()[0]
    ztab_tables = cursor.fetchall()

    print ztab_tables

    for table in ztab_tables:
        print '\n'
        print table
        cursor.execute("select column_name from information_schema.columns where table_name = %s " +
                       "and column_name != 'table_pk' and column_name != 'user_id' and " +
                       "column_name != 'date_time' and column_name != 'res_table_id'", [table[0],])
        column_headers = cursor.fetchall()

        print [a[0] for a in column_headers]

        cursor.execute('select * from ' + table[0], [])
        # print cursor.fetchall()

        desc = cursor.description
        # print pprint.pformat(desc)
        desc_dict = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        # print pprint.pformat(desc_dict, indent=4)

        for option in desc_dict:
            print '\n'
            for header in column_headers:
                print header[0], option[header[0]]

    return True


def get_question_number(qid_start):
    number_string_array = []

    done = False
    while not done:
        if qid_start[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            number_string_array.insert(0, qid_start[-1])
            qid_start = qid_start[0:-1]
        else:
            done = True
    return ''.join(number_string_array), qid_start


def find_parents():

    found_count = 0

    # esseses = ['sssss', 'ssssss', 'sssssss', 'ssssssss', 'sssssssss', 'ssssssssss']

    num_ses = 12

    complete = []

    while num_ses > 3:
        num_ses -= 1

        esses = ''.join('s' for a in range(0, num_ses))
        questions_models = old_models.Questions.objects.using('survey').filter(qid__endswith=esses).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

        print esses, len(esses), len(questions_models)

        one_less_s = ''.join('s' for a in range(0, (num_ses-1)))

        for question in questions_models:
            if question['qid'].strip() not in complete:
                qid = question['qid']

                complete.append(qid.strip())

                print qid.strip()

                qid_start = qid.strip().split('-s')[0]

                question_number, qid_start_without_number = get_question_number(qid_start)

                potential_child_qid = qid_start_without_number + str(int(question_number) -1) + '-' + one_less_s

                questions_parent_models = old_models.Questions.objects.using('survey').filter(qid__startswith=potential_child_qid).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

                if len(questions_parent_models):
                    for parent_question in questions_parent_models:
                        print '*' + parent_question['qid'].strip() + '*'

                        found_count += 1
                else:
                    pass
                    # potential_child_qid_non_decrement = qid_start + '-' + one_less_s
                    # questions_parent_models = old_models.Questions.objects.using('survey').filter(qid__startswith=potential_child_qid_non_decrement).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")
                    #
                    # for parent_question in questions_parent_models:
                    #     print '*-*' + parent_question['qid'].strip() + '*-*'
                    #
                    #     found_count += 1


                print '\n'
    print found_count
    print len(complete)


def find_orphans():

    questions_models = old_models.Questions.objects.using('survey').values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")
    print questions_models.count()

    for question in questions_models:
        question_id = question['qid']
        question_id = question_id.strip()

        question_response_link_models = old_models.QuestionsResponsesLink.objects.using('survey').all().filter(qid__icontains=question_id).values('responseid')

        question_responses = []
        columns = []

        if len(question_response_link_models):
            question_response_models = old_models.Responses.objects.using('survey').all().filter(responseid__in=question_response_link_models).values()

            if question_response_models[0]['table_ids'] != u'N/A':

                # print type(u'N/A'), u'N/A', type(question_response_models[0]['table_ids']), question_response_models[0]['table_ids']

                # print '*' + 'N/A' + '* ' + '*' + question_response_models[0]['table_ids'] + '*'
                #
                # print u'N/A' == question_response_models[0]['table_ids']

                try:
                    cursor = connections['survey'].cursor()
                    cursor.execute("select * from " + question_response_models[0]['table_ids'])
                    ztab_tables = cursor.fetchall()

                    # print ztab_tables

                    for question_response_model in ztab_tables:
                        question_responses.append(question_response_model)

                        # cursor.execute("select column_name from information_schema.columns where table_name = '" + question_response_models[0]['table_ids'] + "'")
                        # column_names = cursor.fetchall()
                        #
                        # # print column_names
                        #
                        # for column_data in column_names:
                        #     columns.append(column_data[0])
                except Exception as e:
                    print e

        print question_id, len(question_responses)


def clean_str(text_input):
    if text_input is None:
        return None
    if len(text_input.strip()) < 1:
        return ''
    else:
        try:
            cleaned = text_input.strip().replace(u"\u2018", "'").replace(u"\u2019", "'")
            return cleaned
        except Exception as ex:
            print '\n******'
            print text_input
            print ex
            print '******\n'
            raise ex


def make_freqs():
    survey_frequecy_models = old_models.SurveyFrequency.objects.using('survey').all().values()
    for f in survey_frequecy_models:
        freq_id = clean_str(f['svyfreqid'])
        new_survey_freq, created = new_models.SurveyFrequency.objects.using('new').get_or_create(svyfreqid=freq_id)
        if created:
            new_survey_freq.svy_frequency_title = clean_str(f['svy_frequency_title'])
            new_survey_freq.svy_frequency_description = clean_str(f['svy_frequency_description'])
            new_survey_freq.save(using='new')
        else:
            print 'already has ' + freq_id


def make_q_types():
    question_types = old_models.QType.objects.using('survey').all().values()
    for f in question_types:
        q_type_id = clean_str(f['q_typeid'])
        new_question_types, created = new_models.QType.objects.using('new').get_or_create(q_typeid=q_type_id)
        if created:
            new_question_types.q_type_text = clean_str(f['q_type_text'])
            new_question_types.q_typedesc = clean_str(f['q_typedesc'])
            new_question_types.save(using='new')
        else:
            print 'already has ' + q_type_id


def make_response_types():
    response_types = old_models.ResponseType.objects.using('survey').all().values()
    for f in response_types:
        responseid = clean_str(f['responseid'])
        new_response_types, created = new_models.ResponseType.objects.using('new').get_or_create(responseid=responseid)
        if created or overwrite == True:
            new_response_types.response_name = clean_str(f['response_name'])
            new_response_types.response_description = clean_str(f['response_description'])
            new_response_types.save(using='new')
        else:
            print 'already has ' + responseid


def make_thematic_groups():
    group = old_models.ThematicGroups.objects.using('survey').all().values()
    for g in group:
        group_id = clean_str(g['tgroupid'])
        new_thematic_group, created = new_models.ThematicGroup.objects.using('new').get_or_create(tgroupid=group_id)
        if created:
            new_thematic_group.grouptitle = clean_str(g['grouptitle'])
            new_thematic_group.groupdescription = clean_str(g['groupdescription'])
            new_thematic_group.save(using='new')
        else:
            print 'already has group' + group_id

    tgs = ['Crime', 'Public Space & Policing', 'Economic Dev & Regeneration']

    for tg in tgs:
        tg_id = 'tg000' + str(tgs.index(tg) + 7)
        new_thematic_group, created = new_models.ThematicGroup.objects.get_or_create(tgroupid=tg_id)
        if created:
            new_thematic_group.groupdescription = tg
            new_thematic_group.grouptitle = tg
            # new_thematic_group.tgroupid = 'tg000' + str(tgs.index(tg) + 7)
            new_thematic_group.save()

def make_thematic_tags():
    group_tags = old_models.GroupTags.objects.using('survey').all().values()
    for f in group_tags:
        tag_id = clean_str(f['tagid'])
        new_thematic_tag, created = new_models.ThematicTag.objects.using('new').get_or_create(tagid=tag_id)
        if created:
            thematic_group = new_models.ThematicGroup.objects.using('new').get(tgroupid=clean_str(f['tgroupid']))

            new_thematic_tag.thematic_group = thematic_group
            new_thematic_tag.tag_text = clean_str(f['tag_text'])
            new_thematic_tag.tag_description = clean_str(f['tag_description'])
            new_thematic_tag.save(using='new')
        else:
            print 'already has ' + tag_id


def make_users():
    users = old_models.UserDetails.objects.using('survey').all().values()
    for f in users:
        user_id = clean_str(f['user_id'])
        new_user, created = new_models.UserDetail.objects.using('new').get_or_create(user_id=user_id)
        if created:
            new_user.user_name = clean_str(f['user_name'])
            new_user.user_email = clean_str(f['user_email'])
            new_user.save(using='new')
        else:
            print 'already has ' + user_id


def find_response():
    responses = old_models.Responses.objects.using('survey').all().values()
    for f in responses:
        responseid = clean_str(f['responseid'])
        new_response, created = new_models.Response.objects.using('new').get_or_create(responseid=responseid)
        if created or overwrite:

            try:
                response_type = new_models.ResponseType.objects.using('new').get(response_name=f['response_type'].strip())
                new_response.response_type = response_type
            except:
                print '\n Error with response_type'
                print f
                pass

            user = new_models.UserDetail.objects.using('new').get(user_id=f['user_id'].strip())
            new_response.user = user

            new_response.responsetext = clean_str(f['responsetext'])
            new_response.routetype = clean_str(f['routetype'])
            new_response.table_ids = clean_str(f['table_ids'])
            new_response.computed_var = clean_str(f['computed_var'])
            new_response.checks = clean_str(f['checks'])
            new_response.route_notes = clean_str(f['route_notes'])
            new_response.created = f['created']
            new_response.updated = f['updated']

            new_response.save(using='new')

            try:
                question_link = old_models.QuestionsResponsesLink.objects.using('survey').get(responseid=f['responseid'])
            except:
                print 'qrl ' + f['responseid']

            try:
                question_model = new_models.Question.objects.using('new').get(qid=question_link.qid)
                question_model.response = new_response
                question_model.save(using='new')
            except ObjectDoesNotExist as odne:
                print 'odne ' + responseid + str(odne)

        else:
            print 'already has response ' + responseid


def make_dc_types():
    dc_types = old_models.DublincoreType.objects.using('survey').all()
    print 'dctypes', dc_types.count()
    for old_dc_type in dc_types:
        type_id = clean_str(old_dc_type.dctypeid)
        new_type, created = new_models.DublincoreType.objects.using('new').get_or_create(dctypeid=type_id)
        if created or overwrite:
            new_type.dc_type_title = clean_str(old_dc_type.dc_type_title)
            new_type.dc_type_description = clean_str(old_dc_type.dc_type_description)
            new_type.save(using='new')
            print new_type
        else:
            print 'already has type ' + type_id


def make_dc_format():
    dc_formats = old_models.DublincoreFormat.objects.using('survey').all()
    print 'dcformats', dc_formats.count()
    for old_dc_format in dc_formats:
        format_id = clean_str(old_dc_format.dcformatid)
        new_format, created = new_models.DublincoreFormat.objects.using('new').get_or_create(dcformatid=format_id)
        if created or overwrite:
            new_format.dc_format_title = clean_str(old_dc_format.dc_format_title)
            new_format.dc_format_description = clean_str(old_dc_format.dc_format_description)
            new_format.save(using='new')
        else:
            print 'already has format ' + format_id


def make_dc_language():
    dc_languages = old_models.DublincoreLanguage.objects.using('survey').all()
    print 'dclanguages', dc_languages.count()
    for old_dc_language in dc_languages:
        language_id = clean_str(old_dc_language.dclangid)
        new_dc_language, created = new_models.DublincoreLanguage.objects.using('new').get_or_create(dclangid=language_id)
        if created or overwrite:
            new_dc_language.dc_language_title = clean_str(old_dc_language.dc_language_title)
            new_dc_language.dc_language_description = clean_str(old_dc_language.dc_language_description)
            new_dc_language.save(using='new')
        else:
            print 'already has language ' + language_id


def make_dcinfos():
    dc_infos = old_models.DcInfo.objects.using('survey').all()

    for old_dc in dc_infos:
        new_dcinfo, created = new_models.DcInfo.objects.get_or_create(identifier=clean_str(old_dc.identifier))
        if created or overwrite:

            # new_dcinfo.identifier = clean_str(old_dc.identifier)
            new_dcinfo.title = clean_str(old_dc.title)
            new_dcinfo.creator = clean_str(old_dc.creator)
            new_dcinfo.subject = clean_str(old_dc.subject)
            new_dcinfo.description = clean_str(old_dc.description)
            new_dcinfo.publisher = clean_str(old_dc.publisher)
            new_dcinfo.contributor = clean_str(old_dc.contributor)
            new_dcinfo.date = old_dc.date
            new_dcinfo.source = clean_str(old_dc.source)
            new_dcinfo.relation = clean_str(old_dc.relation)
            new_dcinfo.coverage = clean_str(old_dc.coverage)
            new_dcinfo.rights = clean_str(old_dc.rights)
            new_dcinfo.created = old_dc.created
            new_dcinfo.updated = old_dc.updated

            try:
                dc_type = new_models.DublincoreType.objects.using('new').get(dc_type_title= clean_str(old_dc.type))
                new_dcinfo.type = dc_type
            except Exception as ex1:
                print ex1

            try:
                dc_format = new_models.DublincoreFormat.objects.using('new').get(dc_format_title= clean_str(old_dc.format))
                new_dcinfo.format = dc_format
            except Exception as ex2:
                print ex2

            try:
                language = new_models.DublincoreLanguage.objects.using('new').get(dc_language_title= clean_str(old_dc.language))
                new_dcinfo.language = language
            except Exception as ex3:
                print ex3

            try:
                user = new_models.UserDetail.objects.using('new').get(user_id= clean_str(old_dc.user_id))
                new_dcinfo.user_id = user
            except:
                print 'cant find user', old_dc.user_id

            new_dcinfo.save()


def link_survey_dcs():

    old_survey_models = old_models.Survey.objects.using('survey').all()
    print 'old surveys ', old_survey_models.count()

    old_dc_models = old_models.DcInfo.objects.using('survey').all()
    print 'old dcs ', old_dc_models.count()

    new_survey_models = new_models.Survey.objects.all()
    print 'new surveys ', new_survey_models.count()

    new_dc_models = new_models.DcInfo.objects.all()
    print 'new dcs ', new_dc_models.count()

    for old_survey in old_survey_models:
        survey_id = old_survey.surveyid
        dc_id = old_survey.identifier

        new_survey = new_models.Survey.objects.get(surveyid=clean_str(survey_id))
        new_dc = new_models.DcInfo.objects.get(identifier=clean_str(dc_id))
        new_survey.dublin_core = new_dc

        # print survey_id, dc_id, clean_str(survey_id) == clean_str(dc_id)
        new_survey.save()


def find_surveys():

    fails = {}
    errors = []
    sub_errors = []
    link_from_errors = []

    survey_model_ids = old_models.Survey.objects.using('survey').all().values()

    # print survey_model_ids

    for s in survey_model_ids:

        clean_sid = s['surveyid'].strip().lower()
        print '*_sid_*' + str(clean_sid)

        new_survey, created = new_models.Survey.objects.using('new').get_or_create(surveyid=clean_sid)

        if created or overwrite:
            frequency = new_models.SurveyFrequency.objects.using('new').get(svy_frequency_title=s['surveyfrequency'].strip())
            new_survey.frequency = frequency

            user = new_models.UserDetail.objects.using('new').get(user_id=s['user_id'].strip())
            new_survey.user = user

            # new_survey.surveyid = clean_str(s['surveyid'])
            new_survey.identifier = clean_str(s['identifier'])
            new_survey.survey_title = clean_str(s['survey_title'])
            new_survey.datacollector = clean_str(s['datacollector'])

            new_survey.collectionstartdate = s['collectionstartdate']
            new_survey.collectionenddate = s['collectionenddate']

            new_survey.moc_description = clean_str(s['moc_description'])
            new_survey.samp_procedure = clean_str(s['samp_procedure'])
            new_survey.collectionsituation = clean_str(s['collectionsituation'])
            new_survey.surveyfrequency = clean_str(s['surveyfrequency'])

            new_survey.surveystartdate = s['surveystartdate']
            new_survey.surveyenddate = s['surveyenddate']

            new_survey.des_weighting = clean_str(s['des_weighting'])
            new_survey.samplesize = clean_str(s['samplesize'])
            new_survey.responserate = clean_str(s['responserate'])
            new_survey.descriptionofsamplingerror = clean_str(s['descriptionofsamplingerror'])
            new_survey.dataproduct = clean_str(s['dataproduct'])
            new_survey.dataproductid = clean_str(s['dataproductid'])
            new_survey.location = clean_str(s['location'])
            new_survey.link = clean_str(s['link'])
            new_survey.notes = clean_str(s['notes'])
            new_survey.user_id = clean_str(s['user_id'])
            new_survey.data_entry = user

            new_survey.created = s['created']
            new_survey.updated = s['updated']

            new_survey.long = clean_str(s['long'])
            new_survey.short_title = clean_str(s['short_title'])
            new_survey.spatialdata = (s['spatialdata'] == 'y')
            new_survey.survey_title = clean_str(s['survey_title'])

            new_survey.save(using='new')
        else:
            print 'already has survey ' + clean_sid

        survey_question_link_models = old_models.SurveyQuestionsLink.objects.using('survey').all().filter(surveyid=s['surveyid']).values_list('qid', flat=True)

        for ql in survey_question_link_models:

            questions_models = old_models.Questions.objects.using('survey').filter(qid=ql).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

            for q in questions_models:
                print '\n\n'
                # print q
                clean_q = q['qid'].strip().lower()

                new_question, q_created = new_models.Question.objects.using('new').get_or_create(qid=clean_q, survey=new_survey)
                if q_created or overwrite:

                    q_type = new_models.QType.objects.using('new').get(q_type_text= clean_str(q['type']))
                    user = new_models.UserDetail.objects.using('new').get(user_id= clean_str(q['user_id']))

                    new_question.thematic_groups = clean_str(q['thematic_groups'])

                    thematic_tags = ''
                    if 'System.Windows' not in clean_str(q['thematic_tags']):
                        thematic_tags = clean_str(q['thematic_tags'])
                    new_question.thematic_tags = thematic_tags

                    new_question.link_from_id = clean_str(q['link_from']).lower()
                    new_question.subof_id = clean_str(q['subof']).lower()

                    new_question.literal_question_text = clean_str(q['literal_question_text'])
                    new_question.questionnumber = clean_str(q['questionnumber'])
                    new_question.type = q_type
                    new_question.variableid = clean_str(q['variableid'])
                    new_question.notes = clean_str(q['notes'])
                    new_question.user_id = user
                    new_question.created = q['created']

                    if len(q['thematic_groups'].strip()):
                        for tg in q['thematic_groups'].strip().split(','):
                            try:
                                tg_model = new_models.ThematicGroup.objects.using('new').get(grouptitle=tg.strip())
                                new_question.thematic_groups_set.add(tg_model)
                            except:
                                errors.append('missing thematic group: ' + str(tg.strip()))
                                pass

                    if len(q['thematic_tags'].strip()):
                        for tag in q['thematic_tags'].strip().split(','):
                            if 'System.Windows' not in tag:
                                try:
                                    tag_model = new_models.ThematicTag.objects.using('new').get(tag_text=tag.strip())
                                    new_question.thematic_tags_set.add(tag_model)
                                except:
                                    errors.append('missing thematic tag: ' + str(tag.strip()))
                                    pass

                    new_question.save(using='new')

                    res_id = ''
                    try:
                        question_link = old_models.QuestionsResponsesLink.objects.using('survey').filter(qid=q['qid'])

                        if question_link.count() > 1:
                            errors.append('qrl multiple links: ' + str(q['qid']))
                        res_id = question_link[0].responseid
                        print question_link[0].qid, question_link[0].responseid

                    # broadened exception
                    except Exception as odne:
                        print 'cant find res *' + q['qid'] + '*'
                        try:
                            question_link = old_models.QuestionsResponsesLink.objects.using('survey').filter(qid__icontains=clean_str(q['qid']).lower())
                            if question_link.count() > 1:
                                errors.append('qrl multiple links (stripped) : ' + str(clean_str(q['qid']).lower()))

                            res_id = question_link[0].responseid
                            print question_link[0].qid, question_link[0].responseid
                        except Exception as odne1:
                            errors.append('cant find res icontains *' + clean_str(q['qid']) + '*')
                            print 'cant find res icontains *' + clean_str(q['qid']) + '*'

                    if len(res_id) < 1:
                        res_id = str('resid_' + q['qid'].strip())
                    res_id = clean_str(res_id)

                    # print len(q['qid']), len(clean_str(q['qid']))
                    # print '#resid_qid_eibselfea1992introi' + '# is like #' + res_id + '#'
                    # for a in range( 0, len('resid_qid_eibselfea1992introi')):
                    #     b = 'resid_qid_eibselfea1992introi'
                    #
                    #     print ord(b[a]), ord(res_id[a])
                    # print 'resid_qid_eibselfea1992introi' == res_id

                    try:
                        old_response_list = old_models.Responses.objects.using('survey').filter(responseid__icontains=res_id).values()
                        # print old_response_list.query
                        # print old_response_list
                        old_response = old_response_list[0]
                    except Exception as e43243:
                        print e43243
                        print old_response_list
                        print clean_q, res_id

                    responseid = clean_str(res_id)
                    new_response, created = new_models.Response.objects.using('new').get_or_create(responseid=responseid)
                    if created or overwrite:
                        try:
                            res_type_name = clean_str(old_response['response_type'])
                            response_type = new_models.ResponseType.objects.using('new').get(response_name=res_type_name)
                            new_response.response_type = response_type
                        except:
                            print 'no restype for ' + old_response['response_type'] + ' on ' + old_response['responseid']

                        user = new_models.UserDetail.objects.using('new').get(user_id=clean_str(old_response['user_id']))
                        new_response.user = user

                        new_response.responsetext = clean_str(old_response['responsetext'])
                        new_response.routetype = clean_str(old_response['routetype'])
                        new_response.table_ids = clean_str(old_response['table_ids'])
                        new_response.computed_var = clean_str(old_response['computed_var'])
                        new_response.checks = clean_str(old_response['checks'])
                        new_response.route_notes = clean_str(old_response['route_notes'])
                        new_response.created = old_response['created']
                        new_response.updated = old_response['updated']

                        new_response.save(using='new')

                    new_question.response = new_response
                    new_question.save(using='new')
                else:
                    print 'already has q_ ' + clean_q

        if question_links:
            questions_models_again = new_models.Question.objects.using('new')
            for qma in questions_models_again:
                # print qma.link_from_id
                if qma.link_from_id is not None:
                    from_question_models = new_models.Question.objects.using('new').filter(qid=clean_str(qma.link_from_id))
                    if from_question_models.count() > 0:
                        qma.link_from_question = from_question_models[0]
                        qma.save(using="new")
                    else:
                        print 'cant find link from ' + str(qma.link_from_id)
                        link_from_errors.append(qma.link_from_id)

                # print qma.subof_id
                if qma.subof_id != 'n/a' and qma.subof_id is not None:
                    subof_question_models = new_models.Question.objects.using('new').filter(qid=clean_str(qma.subof_id))
                    if subof_question_models.count() > 0:
                        qma.subof_question = subof_question_models[0]
                        qma.save(using="new")
                    else:
                        print str(qma.qid) + ' cant find parent, it is sub_of ' + str(qma.subof_id)
                        sub_errors.append(qma.subof_id)

    fails['link_from_errors'] = link_from_errors
    fails['sub_errors'] = sub_errors
    fails['errors'] = errors
    print fails
    with open('error_file.txt', 'r') as err_file:
        err_file.write(json.dumps(fails))

question_links = False
overwrite = False

# make_freqs()
# make_q_types()
# make_users()
# make_thematic_groups()
# make_thematic_tags()
# make_response_types()
# find_surveys()
# find_response()


# make_dc_types()
# make_dc_format()
# make_dc_language()
# make_dcinfos()
link_survey_dcs()


# res_id = 'resid_qid_eibselfea1992introi'
# old_response_list = old_models.Responses.objects.using('survey').filter(responseid__icontains=res_id).values()
# print old_response_list[0]['responseid']

# find_orphans()
# find_parents()
# build_ztab_table()

#
# def test_write():
#     sdc = new_models.Survey()
#     sdc.save()
#
#     q = new_models.Question()
#     q.literal_question_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus quis iaculis mauris. Duis tincidunt, ligula vitae vulputate ultrices, turpis leo luctus lorem, non tempor mi ex at nisl. Quisque varius efficitur augue, non aliquam arcu volutpat sed. Cras dictum nec ante eget bibendum. Vivamus orci sapien, blandit consectetur ultrices nec, cursus ac risus. Curabitur placerat molestie massa. Nunc dui orci, cursus non rhoncus sit amet, dictum quis erat.'
#     q.survey = sdc
#     q.save()
#
# test_write()