import json
import pprint
import requests


class StatsWalesOData():

    def __init__(self):
        self.metadata_url = 'http://open.statswales.gov.wales/en-gb/discover/metadata'
        self.dataset_url = 'http://open.statswales.gov.wales/en-gb/dataset/{}'
        self.filter_prepend = '?$filter={}'
        self.equals_conditional = '%20eq%20'
        self.and_conditional = '%20and%20'
        self.quotes_conditional = '%27{}%27'

    def keyword_search(self, keyword_string):
        keyword_list = keyword_string.split('+')

        keyword_description = requests.get(self.metadata_url)
        keyword_description_objects = json.loads(keyword_description.text)

        datasets = []
        for keyset in keyword_description_objects['value']:
            if 'Description_ENG' in keyset and keyset['TagType_ENG'] == 'Keywords':
                datasets.append(keyset)
                # print pprint.pformat(keyset, indent=4)

        matching_datasets = []
        for dataset in datasets:
            for find_me in keyword_list:
                if find_me in str(dataset['Description_ENG']).lower():
                    matching_datasets.append(dataset)

        for d in matching_datasets:
            print (d)
            print ('')

        print (len(matching_datasets))

        return matching_datasets

    def get_data_url(self, dataset_id, args):

        filter_string = ''

        for count, key_value in enumerate(args.items()):
            print (count, key_value)

            field = key_value[0]
            value = key_value[1]
            if isinstance(key_value[1], str):
                value = self.quotes_conditional.format(value)

            filter_string += '{}{}{}'.format(field, self.equals_conditional, value)

            if count < (len(args) - 1):
                filter_string += self.and_conditional

        data_url = self.dataset_url.format(dataset_id)
        data_url += self.filter_prepend.format(filter_string)

        return data_url


swod = StatsWalesOData()

keyword_results = swod.keyword_search('deprivation+health')
print (len(keyword_results))

# area_code = 'W01001434'
dataset_id = keyword_results[0]['Dataset']

data_url = swod.get_data_url(dataset_id, {'Year_Code': 2014, 'Area_Code': 'W01001434'})

print (data_url)

data = requests.get(data_url)

# print(pprint.pformat(data.text))

data_json = json.loads(data.text)

for data_value in data_json['value']:
    print(pprint.pformat(data_value, indent=4))
    print('')


