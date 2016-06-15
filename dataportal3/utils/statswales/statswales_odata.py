import json
import pprint
import requests
from BeautifulSoup import BeautifulStoneSoup, Tag


class StatsWalesOData():

    def __init__(self):
        self.metadata_edmx_url = 'http://open.statswales.gov.wales/en-gb/dataset/$metadata'
        self.metadata_url = 'http://open.statswales.gov.wales/en-gb/discover/metadata'
        self.dataset_url = 'http://open.statswales.gov.wales/en-gb/dataset/{}'
        self.filter_prepend = '?$filter={}'
        self.equals_conditional = '%20eq%20'
        self.and_conditional = '%20and%20'
        self.quotes_conditional = '%27{}%27'

        self.available_geographies = {
            'Communities First Areas', 'Local authorities',
            'UK regions', 'Lower-layer super output areas',
            'Strategic regeneration areas', 'Local health boards',
            'EU NUTS3 regions', 'Middle-layer super output areas',
            'Wales', 'No drop down value selected'
        }

    def get_metadata_for_dataset(self, dataset_id):

        metadata_edmx = requests.get(self.metadata_edmx_url)
        bs = BeautifulStoneSoup(metadata_edmx.text, isHTML=False)
        edmx = bs.find('edmx:edmx')

        data_services = edmx.find('edmx:dataservices')

        schema = data_services.find('schema')
        schema_namespace = schema.get('namespace')


        entitycontainer = schema.find('entitycontainer')


        # for item in entitycontainer.findAll(recursive=False):
        #     assert item, Tag
        #     print(type(item))
        #     print(item.name)
        #     print(item.attrs)

        dataset_entityset = entitycontainer.find('entityset', attrs={'name': str(dataset_id).lower()})
        entity_type_name = dataset_entityset.get('entitytype')
        entitytype = schema.find('entityType', Name=entity_type_name.split('.')[1])
        print(entitytype)

    def keyword_search(self, keyword_string, args=None):
        if args is None:
            args = {}
        keyword_list = keyword_string.split('+')

        # Grab the discovery metadata json from StatsWales
        keyword_description = requests.get(self.metadata_url)
        keyword_description_objects = json.loads(keyword_description.text)


        # This is a link from the dataset id to all individual data "keysets" about that metadata
        # {'id': [{}, {}]}
        datasets_by_id = {}
        geographys = []

        # First go through the entire metadata json and sort keysets by dataset id
        for keyset in keyword_description_objects['value']:
            if keyset['PartitionKey'] in datasets_by_id:
                datasets_by_id[keyset['PartitionKey']].append(keyset)
            else:
                datasets_by_id[keyset['PartitionKey']] = [keyset]

            # grab geographies to create a nice list of possibilities
            if 'Tag_ENG' in keyset and keyset['Tag_ENG'] == 'Lowest level of geographical disaggregation':
                geographys.append(keyset['Description_ENG'])

        print('available geogs', set(geographys))

        keyword_dataset_ids = set()
        for dataset_id in datasets_by_id.keys():
            for keyset in datasets_by_id[dataset_id]:
                if 'Description_ENG' in keyset and keyset['TagType_ENG'] == 'Keywords':
                    for find_me in keyword_list:
                        if find_me in str(keyset['Description_ENG']).lower():
                            keyword_dataset_ids.add(keyset['PartitionKey'])

        geog_dataset_ids = set()
        for dataset_id in datasets_by_id.keys():
            for keyset in datasets_by_id[dataset_id]:
                if keyset['Tag_ENG'] == 'Lowest level of geographical disaggregation':

                    if 'Lower-layer super output areas' in keyset['Description_ENG']:
                        geog_dataset_ids.add(keyset['PartitionKey'])

        print('keyword_dataset_ids', keyword_dataset_ids)
        print('lsoa_dataset_ids', geog_dataset_ids)

        intersect_ids = keyword_dataset_ids.intersection(geog_dataset_ids)

        print('intersect_ids (keyword+lsoa)', intersect_ids)

        matching_datasets = []
        for dataset_id in datasets_by_id.keys():
            for keyset in datasets_by_id[dataset_id]:
                if keyset['PartitionKey'] in intersect_ids:
                    matching_datasets.append(keyset)

        return matching_datasets

    def get_data_url(self, dataset_id, args=None):
        if args is None:
            args = {}

        filter_string = ''

        for count, key_value in enumerate(args.items()):
            field = key_value[0]
            value = key_value[1]
            if isinstance(key_value[1], int):
                print (count, key_value, 'int')
                filter_string += '{}{}{}'.format(field, self.equals_conditional, value)
                if count < (len(args) - 1):
                    filter_string += self.and_conditional

        for count, key_value in enumerate(args.items()):
            field = key_value[0]
            value = key_value[1]
            if isinstance(key_value[1], str):
                print (count, key_value, 'str')
                value = self.quotes_conditional.format(value)
                filter_string += '{}{}{}'.format(field, self.equals_conditional, value)
                if count < (len(args) - 1):
                    filter_string += self.and_conditional

        data_url = self.dataset_url.format(dataset_id)
        data_url += self.filter_prepend.format(filter_string)

        return data_url


    def get_data_from_url(self, url):
        print (url)

        data = requests.get(url)
        data_json = json.loads(data.text)

        # for data_value in data_json['value']:
        #     print(pprint.pformat(data_value, indent=4))
        #     print('')

        data_count = data_json['value']
        if 'odata.nextLink' in data_json:
            data_count += self.get_data_from_url(data_json['odata.nextLink'])

        return data_count

    def get_data(self, dataset_id, options):
        data_url = self.get_data_url(dataset_id, options)
        return self.get_data_from_url(data_url)

    def get_data_dict(self, dataset_id, options):
        data_list = self.get_data(dataset_id, options)
        return self.odata_to_dict(data_list)

    def odata_to_dict(self, all_data_list):
        all_data_dict = {}
        # area_codes = []
        for data_value in all_data_list:
            # area_codes.append(data_value['Area_Code'])
            # print(pprint.pformat(data_value, indent=4))
            # print('')

            # We need data this shape for the topojson code to fill
            # {
            #     'w010000000': [
            #         {
            #             "name": "Persons Percent for Wrexham 009B (geography), Very good health (General Health) for 2011 from QS302EW - General health",
            #             "value": 40.5,
            #             "geography_id": 1249935771,
            #             "geography_code": "W01000342",
            #             "data_status": "A",
            #             "geography": "Wrexham 009B"
            #         }
            #     ]
            # }

            # OData is this shape, so we need to rejig it a bit
            # {u'AgeGroup_Code': u'AllAges',
            #  u'AgeGroup_Hierarchy': u'',
            #  u'AgeGroup_ItemName_ENG': u'All Ages',
            #  u'AgeGroup_SortOrder': u'1',
            #  u'Area_AltCode1': u'W01000821',
            #  u'Area_Code': u'W01000821',
            #  u'Area_ItemName_ENG': u'Swansea 009E',
            #  u'Area_SortOrder': u'110415',
            #  u'Data': u'16',
            #  u'Indicator_Code': u'INCO',
            #  u'Indicator_ItemName_ENG': u'Income deprivation (percentage of population)',
            #  u'PartitionKey': u'',
            #  u'RowKey': u'0000000000035928',
            #  u'Year_Code': u'2014',
            #  u'Year_ItemName_ENG': u'2014'}

            data_array = [
                {
                    "name": data_value['Indicator_ItemName_ENG'],
                    "value": data_value['Data'],
                    "geography_id": data_value['Area_Code'],
                    "geography_code": data_value['Area_Code'],
                    "data_status": "A",
                    "geography": data_value['Area_ItemName_ENG']
                }
            ]
            all_data_dict[data_value['Area_Code']] = data_array
        return all_data_dict


def do_test():
    swod = StatsWalesOData()

    keyword_results = swod.keyword_search('deprivation+health', {'Geography', ''})
    # print(keyword_results)
    print (len(keyword_results))

    # area_code = 'W01001434'
    dataset_id = list(keyword_results)[0]['PartitionKey']
    print(dataset_id)
    dataset_id = 'wimd0020'

    swod.get_metadata_for_dataset('WIMD0006')

    all_data_list = swod.get_data(
        dataset_id,
        {
            # 'Area_Code': area_code,
            'Year_Code': 2014,
            'AgeGroup_Code': 'AllAges'
        }
    )

    all_data_dict = swod.odata_to_dict(all_data_list)

    print(len(all_data_dict))

if __name__ == '__main__':
    do_test()