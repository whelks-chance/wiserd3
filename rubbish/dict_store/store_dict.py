import os

from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')

import django
django.setup()

from dataportal3.models import ResponseTable, Question, Response
from old import models as old_models


def do_store(blob, response):
    rt = ResponseTable()
    rt.feature_attributes = blob
    if response:
        rt.response = response
    rt.save(using='new')


def do_find(key, value):

    # rts = ResponseTable.objects.using('new').filter(feature_attributes__contains={'1': {'category': 'Always'}})
    # rts = ResponseTable.objects.using('new').filter(feature_attributes__values__contains=['Always'])

    rts = ResponseTable.objects.using('new').all()

    for rt in rts:
        attr = rt.feature_attributes

        print attr
        print ''

        for itr in attr:
            print itr.keys()
            print itr
            print ''


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]


def do_find_question(qid):
    cursor = connections['survey'].cursor()

    questions = Question.objects.filter(qid=qid)
    for q in questions:
        assert isinstance(q, Question)
        response = q.response

        if response:
            assert(response, Response)
            res_id = response.responseid
            print res_id

            res_table_links = old_models.ResponsesTablesLink.objects.filter(responseid=res_id)
            for res_table_link in res_table_links:

                blob = []

                assert(res_table_link, old_models.ResponsesTablesLink)
                res_table_id = res_table_link.restableid

                # print res_table_id

                cursor.execute(
                    "select column_name from information_schema.columns where table_name = '" + res_table_id + "'"
                )
                column_names = cursor.fetchall()
                clean_column_names = []
                for col in column_names:
                    if col[0] not in ['table_pk', 'res_table_id', 'user_id', 'date_time']:
                        clean_column_names.append(col[0])

                print column_names
                print clean_column_names
                print ''

                cursor.execute("select * from " + res_table_id)
                table_contents = dictfetchall(cursor)

                # print table_contents

                for row in table_contents:
                    blob_row = {}
                    print row
                    print ''

                    for a_col in clean_column_names:
                        print row[a_col]
                        blob_row[a_col] = row[a_col]

                    blob.append(blob_row)
                do_store(blob, response)


if __name__ == '__main__':

    blob = [
        {
            'id': '1',
            'category': 'Always',
            'description': 'I always do the thing'
        },
        {
            'id': '2',
            'category': 'Sometimes',
            'description': 'I sometimes do the thing'
        },
        {
            'id': '3',
            'category': 'Never',
            'description': 'I never do the thing.'
        }
    ]

    api_data = {
        'columns': ['id', 'category', 'description'],
        'search_result_data': blob
    }

    # do_store(blob)

    # do_find('category', 'Sometimes')

    for q in Question.objects.all()[:1000]:
        # qid_bes2005oyoq11
        do_find_question(q.qid)