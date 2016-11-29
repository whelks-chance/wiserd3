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


class FullTextSearch():
    def __init__(self):
        pass

    def build_keyword_set(self):

        all_question_words = []

        stop_words = set(stopwords.words('english'))
        stop_words.update(['...', '.', ',', '"', "'", '?', '!', ':', ';',
                           '(', ')', '[', ']', '{', '}', '/', '-', '…?', '…', '£'])
        stop_words.update(['agree', 'disagree', 'please', 'would',
                           'last', 'think', 'much', 'following', 'many', 'item', 'ask', 'show',
                           'say', 'take', 'name', 'like', 'one', 'card',
                           'things', 'first', 'tell', 'tick', 'box'
                           ])

        all_surveys = models.Survey.objects.all()
        for s in all_surveys:
            assert isinstance(s, models.Survey)
            print s.survey_title, '\n'
            keyword_list = []

            keyword_list.extend(s.survey_title.split())

            dublin_core_text = s.dublin_core.description
            if dublin_core_text:
                filtered_words = [i.lower() for i in nltk.wordpunct_tokenize(dublin_core_text) if i.lower() not in stop_words]
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

            # filtered_set = set(filtered_words)
            # keyword_list.extend(list(filtered_set))

            c = Counter(filtered_words)
            most_common = c.most_common(20)
            print most_common

            keyword_list.extend([x[0] for x in most_common])

            subjects = s.dublin_core.subjects.all()
            for sub in subjects:
                keyword_list.append(sub.tag_text)

            print keyword_list

            s.keywords = u' '.join(keyword_list)
            s.save()

        conn_queries = connections['new'].queries
        for q in conn_queries:
            print q, '\n'
        print 'qual conn num end', len(conn_queries)

        c = Counter(all_question_words)
        most_common = c.most_common(30)
        print most_common

    def test_search(self):
        all_surveys = models.Survey.objects.search('care', raw=True)
        print all_surveys
        print all_surveys.count()


if __name__ == '__main__':
    nltk.download("stopwords")

    fts = FullTextSearch()
    fts.build_keyword_set()
    # fts.test_search()