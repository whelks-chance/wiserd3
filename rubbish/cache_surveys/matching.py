import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')
import django
django.setup()

from dataportal3 import models
import requests
from fuzzywuzzy import fuzz


class CacheSurveyMatcher():
    def __init__(self):
        pass

    def match(self):

        cache_surveys = requests.get('http://localhost:5000/api/3/action/package_search?facet.limit=1000&rows=1000').json()

        for model in models.Survey.objects.all():
            # print('\n', model.survey_title)

            for cs in cache_surveys['result']['results']:
                fuzz_ratio = fuzz.ratio(cs['title'], model.survey_title)

                if fuzz_ratio > 55:
                    question_count = models.Question.objects.filter(survey=model).count()

                    print cs['title'], '<-->', model.survey_title, '(', fuzz_ratio, '% match,', question_count, 'questions)'

                    print ''
                    print ''


if __name__ == "__main__":
    br = CacheSurveyMatcher()
    br.match()
