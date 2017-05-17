import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiserd3.settings')
import django
django.setup()

from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from dataportal3 import models as models
from django.db import connections


class SurveyReader:
    def __init__(self, filename):
        self.filename = filename

    def read_and_write(self):
        filename1 = self.filename
        wb1 = load_workbook(filename1)

        print wb1.get_sheet_names()

        ws = wb1[wb1.get_sheet_names()[0]]

        print type(ws)

        assert isinstance(ws, Worksheet)

        colA = ws['A']
        colB = ws['B']
        colC = ws['C']
        colD = ws['D']
        colE = ws['E']

        num_questions = len(ws['A']) - 1

        print 'This xls has {} questions'.format(num_questions)

        print colA[0].value, colB[0].value, colC[0].value

        for i in range(1, num_questions):
            q_num = colA[i].value
            q_text = colB[i].value

            print 'Question {} has question text {}'.format(q_num, q_text)

            new_q = models.Question()
            new_q.qid = '{}_{}'.format(q_num, q_text)
            new_q.survey = models.Survey.objects.all()[0]
            new_q.questionnumber = q_num
            new_q.literal_question_text = q_text

            new_q.save('new')
            print 'Saved question {}'.format(i)

        # print '', connections['new'].queries


if __name__ == "__main__":

    filename = '/home/kdickson/text_survey.xlsx'

    sr = SurveyReader(filename)
    sr.read_and_write()
