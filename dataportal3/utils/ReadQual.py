import json
import pprint
import re

__author__ = 'ubuntu'


class ReadQual():
    def __init__(self):
        self.coverage = ''
        self.coverage_objects = []


    def get_coverage_string(self):
        with open('coverage.txt', 'r') as f:
            self.coverage = f.read()
            return self.coverage

    def get_coverage_items(self, coverage_string):
        coverage_list = coverage_string.split(';')

        # print 'coverage size ', len(coverage_list)

        coverage_objects = []

        for coverage_item in coverage_list:

            # print '\n\n'

            # if len(coverage_item) < 100:
            #     print 'short', '*' + str(coverage_item) + '*'

            pattern = '"{name:(?P<name>.*), data'
            replace = '{"name":"\g<name>", "data"'

            coverage_item = re.sub(pattern, replace, coverage_item)

            coverage_item = coverage_item[0:-2] + '}'

            # print coverage_item

            try:
                coverage_object = json.loads(coverage_item)
                coverage_objects.append(coverage_object)
                # print pprint.pformat(coverage_object, indent=4)
            except:
                pass
                # print 'error:', coverage_item

        self.coverage_objects = coverage_objects
        return self.coverage_objects

    def build_page_count_object(self, page_data, find_word, count_word):
        word_dict = {}
        for word in page_data['data']:
            try:
                word_dict[word[find_word]] = word[count_word]
            except Exception as e984273:
                print e984273, word
        return word_dict

    def read_trans_stats(self, stats):
        stats_objects = []

        stats_singles = stats.split(';')
        for stat in stats_singles[:1]:
            f, s, t = stat.strip().partition(',{')
            t = '{' + t
            pattern = '{name:(?P<name>.*), data'
            replace = '{"name":"\g<name>", "data"'

            stats_text = re.sub(pattern, replace, t)

            try:
                stats_object = json.loads(stats_text, strict=False)
                # print pprint.pformat(stats_object, indent=4)

                stats_object['page_counts'] = self.build_page_count_object(stats_object, 'page', 'count')

                # print pprint.pformat(stats_object)
                stats_objects.append(stats_object)
            except:
                print 'json error: ', stats_text

        return stats_objects

    def get_calais_object(self, calais_text):
        calais_text = calais_text.strip().rstrip(',')
        calais_text = '{"data": [' + calais_text + ']}'
        # print '*' + calais_text + '*'
        calais_object = json.loads(calais_text, strict=False)
        # print pprint.pformat(calais_object, indent=4)
        return calais_object

# rq = ReadQual()
# coverage_string = rq.get_coverage_string()
#
# coverage_objects_1 = rq.get_coverage_items(coverage_string)
#
# print pprint.pformat(coverage_objects_1, indent=4)

