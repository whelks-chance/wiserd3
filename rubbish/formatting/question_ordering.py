import os
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")


import django
django.setup()

from dataportal3 import models


class QuestionSorter():

    def __init__(self, printout=False):

        self.printout = printout
        self.counter = 0
        self.survey = None
        self.current_question = None
        self.ordered_questions = []
        self.total_ordered = 0
        self.unlinked = 0
        self.text_output = []

    def print_and_log(self, text):
        if self.printout:
            print text
        self.text_output.append(text)

    def output_logs(self):
        return self.text_output

    def get_ordered_questions_in_survey(self, survey):
        self.ordered_questions = []
        assert isinstance(survey, models.Survey)
        self.counter += survey.question_set.count()

        first_questions = survey.question_set.filter(link_from_question=None)

        if len(first_questions) == 1:
            first_question = first_questions[0]

            self.current_question = first_question
            self.ordered_questions.append(first_question.qid)

            while True:
                next_question = self.get_next_question(survey, self.current_question)
                if next_question:
                    self.ordered_questions.append(next_question.qid)
                    self.current_question = next_question
                else:
                    return self.ordered_questions
        else:
            self.print_and_log('There were {} first questions in survey {} out of {} total questions'.format(
                len(first_questions),
                survey.surveyid,
                survey.question_set.count()
            ))
            return self.ordered_questions

    def do_order_questions(self):
        surveys = models.Survey.objects.all()
        self.print_and_log( len(list(surveys)))

        for survey in surveys:
            self.print_and_log( survey.surveyid)
            survey_question_order = self.get_ordered_questions_in_survey(survey)
            self.print_and_log( survey_question_order)
            self.total_ordered += len(survey_question_order)
            self.print_and_log( 'Ordered {} of {} questions. {} unlinked.'.format(
                len(survey_question_order),
                survey.question_set.count(),
                survey.question_set.count() - len(survey_question_order)
            ))
            self.unlinked += survey.question_set.count() - len(survey_question_order)

            self.print_and_log( '******************************************************************')

    def get_next_question(self, survey, current_question):
        try:
            return survey.question_set.get(link_from_question=current_question)
        except:
            return None


if __name__ == "__main__":

    qs = QuestionSorter(True)
    qs.do_order_questions()

    print 'total questions considered', qs.counter

    print 'total questions in table', len(models.Question.objects.all())

    print 'total ordered', qs.total_ordered

    print 'total unlinked', qs.unlinked

    print 'failed to order', qs.counter - qs.total_ordered
