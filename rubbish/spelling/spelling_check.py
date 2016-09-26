import os
import string

import re
from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')

import django
django.setup()

from dataportal3.models import ResponseTable, Question, Response
import enchant

d = enchant.Dict("en_GB")
d.add('dont')
d.add('aq')
d.add('bq')
d.add('dk')
d.add('hrp')


def is_valid_word(word):
    return d.check(word)

# string.punctuation without ' and `
punctuation = """!"#$%&()*+,-./:;<=>?@[\]^_{|}~"""


def cleanup(word):
    for punc in punctuation:
        word = word.replace(punc, '')
    for num in string.digits:
        word = word.replace(num, '')
    for wsp in string.whitespace:
        word = word.replace(wsp, '')

    # if word.startswith("'"):
    word = word.lstrip("'")
    word = word.rstrip("'")

    re.sub(r"\s+", "", word, flags=re.UNICODE)
    return word


def do_spell_check_responses():

    wrongs = []
    all_responses = ResponseTable.objects.all()
    for r in all_responses:
        assert isinstance(r, ResponseTable)

        data = r.feature_attributes

        for d in data:
            for k in d.keys():

                for word in re.findall(r"[\w']+", d[k]):
                    word = cleanup(word)

                    if len(word):
                        is_ok = is_valid_word(word)
                        if not is_ok:
                            err = (word, r.id, r.response.responseid, d[k])
                            print err
                            print ''
                            wrongs.append(err)
    print len(wrongs)


def do_spell_check_questions():

    wrongs = []
    all_questions = Question.objects.all()
    for q in all_questions:
        if q.literal_question_text:
            for word in re.findall(r"[\w']+", q.literal_question_text):
                word = cleanup(word)

                if len(word):
                    is_ok = is_valid_word(word)
                    if not is_ok:
                        err = (word, q.qid, q.literal_question_text)
                        print err
                        print ''
                        wrongs.append(err)
    print len(wrongs)


if __name__ == '__main__':
    # do_spell_check_questions()
    do_spell_check_responses()