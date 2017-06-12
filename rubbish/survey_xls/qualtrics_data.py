import json
import pprint
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class QualtricsReader():
    def __init__(self):
        pass

    def read(self, filename):
        with open(filename) as qsf:
            blob = json.load(qsf)

            survey_elements = blob['SurveyElements']
            for survey_element in survey_elements:
                # print survey_element['Element']
                payload = survey_element['Payload']

                if survey_element['Element'] == 'SQ':
                    print '....'
                    # print payload['QuestionDescription']
                    print strip_tags(payload['QuestionText'])

                    if 'Choices' in payload:
                        for choice in payload['Choices']:
                            print choice, payload['Choices'][choice]['Display']

                if survey_element['Element'] == 'BL':

                    print len(payload)
                    print payload.keys()
                    # print pprint.pformat(payload)

                    for q_name in payload.keys():
                        element = payload[q_name]
                        print q_name
                        print pprint.pformat(element)

                        print element['Description']

                        if element['BlockElements']:
                            for question in element['BlockElements']:
                                print pprint.pformat(question)

                        print '\n***\n'

if __name__ == '__main__':
    print 'QualtricsReader'

    # filename = 'C:\Users\Ian\OneDrive - Cardiff University\Dataportal\Cohort_B_year_10.qsf'
    # filename = 'C:\Users\Ian\OneDrive - Cardiff University\Dataportal\Cohort_C_year_12.qsf'
    filename = '/home/kdickson/wedata/Cohort_B_year_10.qsf'
    # filename = 'C:\Users\Ian\OneDrive - Cardiff University\Dataportal\cohort_E_year_7.txt'

    qr = QualtricsReader()
    qr.read(filename)
