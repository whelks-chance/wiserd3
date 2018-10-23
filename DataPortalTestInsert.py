import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')
import django
django.setup()

from dataportal3 import models as models
from django.db import connections
import csv


def insert_data_sj():
    #models.******.objects.get accesses the ****** table. e.g. 'Question' below.
    #qid is the field name.
    #__contains is the equivalent of 'like' in SQL.
    # If you want an exact match just do qid = ****
    questions = models.Question.objects.filter(qid__contains='qid_cohort')
    # open the csv lookup file
    importfile = csv.DictReader(open("TestDataInsert.csv"))
    # Iterate through every question in the database.
    for question in questions:
        # To access a field in the question use .fieldname
        questionid = question.qid
        print 'Testing: ',questionid
        #Iterate through every row in the import file
        for row in importfile:
            # Get the new variable name and the qid from the import file.
            varname = row['varname']
            importid = row['qid']
            # If the import file qid matches the database qid
            if importid == questionid:
                print 'importid matches: ', importid
                # Update the database.
                # Find the correct question ID to update. Update the variable name in that question
                models.Question.objects.filter(qid=questionid).update(variableid=varname)
                # print 'Output question: ',question
            else:
                # Otherwise, move on to next record.
                pass
    ### for row in importfile:
    ###     print row['ID']


if __name__ == "__main__":
    insert_data_sj()


