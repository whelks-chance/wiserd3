import os

from django.db import connections

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')

import django
django.setup()

from dataportal3.models import ResponseTable, Question, Response
from old import models as old_models


def do_store(blob, response):

    if response:
        rt, created = ResponseTable.objects.get_or_create(response=response)
    else:
        rt = ResponseTable()
    rt.feature_attributes = blob
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


class NoLegacyResTableException(Exception):
    def __init__(self, response, ztab_name):
        self.ztab_name = ztab_name
        self.response = response

    def __repr__(self):
        return str((self.response.responseid, self.response.response_type, self.ztab_name))


class NoResponseException(Exception):
    def __init__(self, qid):
        self.qid = qid


def do_find_question(qid):
    cursor = connections['survey'].cursor()

    questions = Question.objects.filter(qid=qid)
    missing_response = []
    for q in questions:
        assert isinstance(q, Question)
        response = q.response

        if response:
            assert(response, Response)
            res_id = response.responseid

            res_table_links = old_models.ResponsesTablesLink.objects.filter(responseid=res_id)
            if len(res_table_links) == 0:
                raise NoLegacyResTableException(response, None)

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

                # print column_names
                # print clean_column_names
                # print ''

                try:
                    cursor.execute("select * from " + res_table_id)
                except:
                    raise NoLegacyResTableException(response, res_table_id)

                table_contents = dictfetchall(cursor)

                print res_id, res_table_id, len(table_contents), len(clean_column_names)

                for row in table_contents:
                    blob_row = {}
                    # print row
                    # print ''

                    for a_col in clean_column_names:
                        # print row[a_col]
                        blob_row[a_col] = row[a_col]

                    blob.append(blob_row)

                #     todo replace
                do_store(blob, response)

            # There should only be one of each of these if we get to here
            return (res_id, res_table_id, len(table_contents), len(clean_column_names))
        else:
            raise NoResponseException(qid)

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

    res_issues = []
    res_table_issues = []

    ok = []
    ok_ztabs = []
    for q in Question.objects.all():
        # qid_bes2005oyoq11
        try:
            res_id, res_table_id, len_table_contents, len_clean_column_names = do_find_question(q.qid)
            ok.append(q.qid)
            ok_ztabs.append(res_table_id)
        except NoResponseException as nre:
            res_issues.append(nre.qid)

        except NoLegacyResTableException as nlrt:
            # ignore non existing tables for open ended questions, obviously
            if nlrt.response.response_type and nlrt.response.response_type.id not in [9, 8]:
                # These should have a ztab_ responseTable but we couldn't find it
                res_table_issues.append(nlrt)

    print 'ok', len(ok)
    print 'res_issues', len(res_issues), res_issues
    print 'res_table_issues', len(res_table_issues), res_table_issues

    cursor = connections['survey'].cursor()
    cursor.execute(
        "select table_name from information_schema.columns where table_name ilike '%ztab_%'"
    )
    table_names_complex = cursor.fetchall()

    table_names = [item[0] for item in table_names_complex]

    all_ztabs = set(table_names)

    print '\n\n\n\n'
    # print all_ztabs
    missing = all_ztabs - set(ok_ztabs)
    print 'total ztabs', len(all_ztabs), 'total created', len(ok_ztabs)
    print 'orphaned/ unused old ztab_ tables', len(missing)
    # print missing

