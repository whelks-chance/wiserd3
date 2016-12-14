# coding=utf-8
import os
from collections import Counter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')

import django
django.setup()

import nltk
from django.db import connections
from dataportal3 import models
from nltk.corpus import stopwords
import pprint


class FullTextSearch():
    def __init__(self):
        self.survey_common_words = {}
        self.survey_names = []
        self.survey_question_num = {}

    def build_keyword_set(self, csv_records=200, csv_num_words=50, search_string=None, use_weighting=False):

        all_question_words = []

        stop_words = set(stopwords.words('english'))
        stop_words.update(['...', '.', ',', '"', "'", '?', '!', ':', ';',
                           '(', ')', '[', ']', '{', '}', '.)', ')?', '=',
                           '/', '-', '–', '…?', '…', '£', '\u2026', '\u2013'])
        stop_words.update(['12', '10', '0', '2'])
        stop_words.update(['agree', 'disagree', 'please', 'would',
                           'last', 'think', 'much', 'following', 'many', 'item', 'ask', 'show',
                           'say', 'take', 'name', 'like', 'one', 'card',
                           'things', 'first', 'tell', 'tick', 'box', 'answer', '?(', 'use',
                           'long', 'yes', 'whether', 'non', 'total', 'give', 'could', 'ever',
                           'get', 'made', 'often', 'may', 'way'
                           ])

        if not search_string:
            all_surveys = models.Survey.objects.all()
        else:
            all_surveys = models.Survey.objects.search(search_string, raw=True)

        for s in all_surveys:
            assert isinstance(s, models.Survey)

            clean_survey_name = s.survey_title.replace(',', '')

            self.survey_names.append(clean_survey_name)
            self.survey_question_num[clean_survey_name] = s.question_set.count()

            print '\n----\n', s.survey_title, '\n'
            keyword_list = []

            keyword_list.extend(s.survey_title.split())

            dublin_core_text = s.dublin_core.description
            if dublin_core_text:
                filtered_words = [i.lower() for i in nltk.wordpunct_tokenize(dublin_core_text.replace(',', '')) if i.lower() not in stop_words]
                keyword_list.extend(filtered_words)

            questions = s.question_set.all()
            all_question_string = ''
            for q in questions:
                assert isinstance(q, models.Question)
                if q.literal_question_text:
                    all_question_string += q.literal_question_text

            filtered_words = [i.lower() for i in nltk.wordpunct_tokenize(all_question_string) if
                              i.lower() not in stop_words]

            all_question_words.extend(filtered_words)

            c = Counter(filtered_words)
            most_common = c.most_common(30)
            print most_common

            for smc in most_common:
                if self.survey_common_words.has_key(smc[0]):
                    self.survey_common_words[smc[0]][s.survey_title.replace(',', '')] = smc[1]
                else:
                    self.survey_common_words[smc[0]] = {s.survey_title.replace(',', ''): smc[1]}

            keyword_list.extend([x[0] for x in most_common])

            subjects = s.dublin_core.subjects.all()
            for sub in subjects:
                keyword_list.append(sub.tag_text)

            print keyword_list

            s.keywords = u' '.join(keyword_list)
            s.save()

        # conn_queries = connections['new'].queries
        # for q in conn_queries:
        #     print q, '\n'
        # print 'conn num end', len(conn_queries)

        all_common_words = {}

        c = Counter(all_question_words)
        most_common = c.most_common(csv_num_words)
        print most_common
        for mc in most_common:
            print mc

            if self.survey_common_words.has_key(mc[0]):
                all_common_words[(mc[1], mc[0])] = self.survey_common_words[mc[0]]

        print '\n\n'

        # print pprint.pformat(self.survey_common_words)
        print pprint.pformat(all_common_words)

        num_records = csv_records

        with open('../../dataportal3/static/test_data/data.csv', 'w') as dat:
            dat.write('word,' + ','.join(self.survey_names[:num_records]) + '\n')

            for word in all_common_words:
                sur_words = []
                for sur in self.survey_names[:num_records]:
                    if sur in all_common_words[word]:

                        if use_weighting:
                            weighting = float(all_common_words[word][sur]) / self.survey_question_num[sur] * 100
                        else:
                            weighting = all_common_words[word][sur]

                        sur_words.append(
                            str(weighting).encode('utf-8'))
                    else:
                        sur_words.append('0')

                comma = ','.encode('utf-8')
                dat.writelines(word[1].encode('utf-8') + ',' + comma.join(sur_words) + '\n')

    def test_search(self, search_string):
        all_surveys = models.Survey.objects.search(search_string, raw=True)
        print all_surveys
        print all_surveys.count()


if __name__ == '__main__':
    nltk.download("stopwords")

    fts = FullTextSearch()
    fts.build_keyword_set(csv_records=200, csv_num_words=30)
    search_string = "how | many | people"
    # fts.test_search(search_string)