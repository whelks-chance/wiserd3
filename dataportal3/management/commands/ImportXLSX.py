from django.core.management.base import BaseCommand

from rubbish.survey_xls.xls_survey_reader import SurveyReader


class Command(BaseCommand):
    help = 'Import an XLSX'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str)

        parser.add_argument('--description_file', type=str)

    def handle(self, *args, **options):
        filename = options['filename']

        if options['description_file']:
            print('Will build surveys from description file')
            description_file = options['description_file']

            sr = SurveyReader(filename)
            sr.build_from_description_file(
                description_file,
                '4',
                'A'
            )

