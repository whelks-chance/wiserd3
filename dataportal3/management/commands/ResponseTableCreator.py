import json

from django.core.management.base import BaseCommand

from rubbish.survey_xls.QuestionResponseLinker import QuestionResponseLinker
from rubbish.survey_xls.xls_survey_reader import SurveyReader


class Command(BaseCommand):
    help = 'Create the response table JSON doc from the question bank file, and a redacted response file'

    def add_arguments(self, parser):
        parser.add_argument('--question_bank_file', type=str)
        parser.add_argument('--cohort_response_file', type=str)
        parser.add_argument('--sweep_cohort_filter', type=str)
        parser.add_argument('--output_file_name', type=str)

    def handle(self, *args, **options):
        question_bank_file = options['question_bank_file']
        cohort_response_file = options['cohort_response_file']
        sweep_cohort_filter = options['sweep_cohort_filter']
        output_file_name = options['output_file_name']

        if not sweep_cohort_filter:
            sweep_cohort_filter = None

        if not question_bank_file:
            exit('Need a question bank file')

        if not cohort_response_file:
            exit('Need a response file')

        qrl = QuestionResponseLinker(
            question_bank_file,
            cohort_response_file,
            sweep_cohort_filter
        )

        sample = qrl.run()
        with open(output_file_name, 'w') as outputfile:
            outputfile.write(json.dumps(sample.description(), indent=4))
