import json
import os
import pprint

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')

import django
django.setup()

from dataportal3.models import Survey, Question
from django.contrib.gis.db import models


class SurveyJson():
    def __init__(self):
        self.all = []
        self.ignore_fields = ['link_from_question', 'subof_question',
                              'survey', 'qtext_index',
                              'user_id', 'data_entry'

                              ]

    def save(self, object, name):
        with open('survey_{}.json'.format(name), 'w') as all_surveys_file:
            all_surveys_file.write(json.dumps(object, indent=4))

    def is_jsonable(self, x):
        try:
            json.dumps(x)
            return True
        except:
            return False

    def serialise_model(self, model_instance):
        model_dict = {}
        if isinstance(model_instance, models.Model):
            for key in model_instance.__class__._meta.fields:
                if key.name not in self.ignore_fields:
                    attr = getattr(model_instance, key.name)
                    if isinstance(attr, models.Model):
                        print(key, attr, 'is a Model class?')
                        model_dict[key.name] = self.serialise_model(attr)
                    elif self.is_jsonable(attr):
                        model_dict[key.name] = attr
                    else:
                        print('attr is ', attr)
                        # model_dict[key.name] = str.encode(attr, encoding='utf8')
        else:
            print('Not a model instance', model_instance)
        print('\n\n\n')
        return model_dict

    def do_all(self):
        print(pprint.pformat(Question.__dict__))

        print('\n dict')
        for key in Question.__dict__.keys():
            print key

        print('\n fields')

        for key in Question._meta.fields:
            print key.name

        print('\n Many to many')

        for key in Question._meta.many_to_many:
            print key

        print('\n Virtual')

        for key in Question._meta.virtual_fields:
            print key

        print('\n All')

        for key in Question._meta.get_fields(include_hidden=True):
            print(key, type(key))
            print key.__dict__
            print '\n'

        survey_identifiers = [
            'wisid_bes2005oyo',
            # 'wisid_C01WHF'
        ]

        for s in Survey.objects.all().filter(identifier__in=survey_identifiers):
            survey = self.serialise_model(s)

            questions = []
            for q in Question.objects.all():
                serialised_question = self.serialise_model(q)
                serialised_question['response_table'] = self.serialise_model(q.responsetable_set.model)
                questions.append(serialised_question)

            survey['questions'] = questions
            self.save(survey, s.surveyid)
            # self.all.append(survey)


js = SurveyJson()
js.do_all()
# js.save()
