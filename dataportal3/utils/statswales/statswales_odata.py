import json
import pprint
import requests
from BeautifulSoup import BeautifulStoneSoup, Tag


class StatsWalesOData():

    def __init__(self):
        self.metadata_edmx_url = 'http://open.statswales.gov.wales/en-gb/dataset/$metadata'
        self.metadata_url = 'http://open.statswales.gov.wales/en-gb/discover/metadata'
        self.dataset_url = 'http://open.statswales.gov.wales/en-gb/dataset/{}'
        self.datasetdimensionitems_url = 'http://open.statswales.gov.wales/en-gb/discover/datasetdimensionitems'
        self.filter_prepend = '?$filter={}'
        self.equals_conditional = '%20eq%20'
        self.and_conditional = '%20and%20'
        self.not_equals_conditional = '%20ne%20'
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
        # print dataset_entityset
        entity_type_name = dataset_entityset.get('entitytype').split('.')[1]
        # print entity_type_name

        entitytype = schema.find('entitytype', attrs={'name': entity_type_name})
        # print(entitytype)

        entity_properties = entitytype.findAll('property')
        # print entity_properties

        property_data_types = {}
        for property in entity_properties:
            print property['name'], property['type']
            property_data_types[property['name']] = property['type']
        return property_data_types

    def keyword_search(self, keyword_string, args=None):
        if args is None:
            args = {}
        keyword_list = keyword_string.split('+')

        # Grab the discovery metadata json from StatsWales
        keyword_description = requests.get(self.metadata_url)
        print(self.metadata_url)
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

        # intersect_ids = keyword_dataset_ids.intersection(geog_dataset_ids)
        intersect_ids = keyword_dataset_ids
        print('intersect_ids (keyword+lsoa)', intersect_ids)

        matching_datasets = []
        for dataset_id in datasets_by_id.keys():
            for keyset in datasets_by_id[dataset_id]:
                if keyset['PartitionKey'] in intersect_ids:
                    matching_datasets.append(keyset)

        return matching_datasets

    def get_data_url(self, dataset_id, args=None):
        data_url = self.dataset_url.format(dataset_id)
        data_url += self.filter_prepend.format(self.get_filter_string(args))

        return data_url

    def get_filter_string(self, args=None):
        if args is None:
            args = []

        filter_string = ''

        print args
        counter = 0
        for count, key_value in enumerate(args):
            field = key_value[0]
            conditional = key_value[1]
            value = key_value[2]

            # print(field, conditional, value)

            if isinstance(value, int):
                print (count, key_value, 'int')
                filter_string += '{}{}{}'.format(field, conditional, value)
                if counter < (len(args) - 1):
                    filter_string += self.and_conditional
                counter += 1

        for count, key_value in enumerate(args):
            field = key_value[0]
            conditional = key_value[1]
            value = key_value[2]
            if isinstance(value, str) or isinstance(value, unicode):
                print (count, key_value, 'str')
                value = self.quotes_conditional.format(value)
                filter_string += '{}{}{}'.format(field, conditional, value)
                if counter < (len(args) - 1):
                    filter_string += self.and_conditional
                counter += 1
        # print counter, len(args)

        print filter_string
        return filter_string

        # data_url = self.dataset_url.format(dataset_id)
        # data_url += self.filter_prepend.format(filter_string)
        # return data_url

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

    def get_data_dict(self, dataset_id, options, constants):
        data_list = self.get_data(dataset_id, options)
        return self.odata_to_dict(data_list, options, constants)

    def odata_to_dict(self, all_data_list, options, constants):
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

            string_data = []
            if data_value.get('Indicator_Code', None):

                string_data.append(
                    {
                        'title': 'Category',
                        'value': data_value.get('Indicator_Code', None)
                    }
                )
            for option in options:
                string_data.append(
                    {
                        'title': option[0],
                        'value': option[2]
                    }
                )

            name = data_value.get('Indicator_ItemName_ENG', None)
            if name is None:
                name = data_value['Component_ItemName_ENG']

            data_title = data_value.get('Indicator_ItemName_ENG', None)
            if data_title is None:
                data_title = data_value['Measure_ItemName_ENG']

            data = data_value.get('Data', None)
            if data is None:
                data = data_value['RoundedData']

            data_dict = {
                    "name": name,
                    "value": data,
                    "geography_id": data_value['Area_Code'],
                    "geography_code": data_value['Area_Code'],
                    "data_status": "A",
                    "geography": data_value['Area_ItemName_ENG'],
                    "data_title": data_title,
                    "string_data": string_data
                }

            if constants:
                for key, value in constants.items():
                    data_dict[key] = value

            # why is this in a one item array?
            data_array = [
                data_dict
            ]
            all_data_dict[data_value['Area_Code']] = data_array
        return all_data_dict

    def get_dataset_overview(self, dataset_id):
        data_url = self.get_dataset_overview_url(dataset_id)
        result = requests.get(data_url)
        # print result.text
        print data_url

        result_json = json.loads(result.text)

        dimensions = {}

        for datasetdimensionitem in result_json['value']:
            dimension_name = datasetdimensionitem['DimensionName_ENG']
            if dimension_name in dimensions:
                dimensions[dimension_name]['measures'].append({
                    'id': datasetdimensionitem['Code'],
                    'name': datasetdimensionitem['Description_ENG']
                })
            else:
                dimensions[dimension_name] = {
                    "concept": dimension_name,
                    "name": dimension_name,
                    'measures': [{
                        'id': datasetdimensionitem['Code'],
                        'name': datasetdimensionitem['Description_ENG']
                    }]
                }
            # print datasetdimensionitem

        return_data = {
            'concepts': [],
            'codelists': dimensions
        }

        # return_data['concepts'].append({
        #     'codelist': codelist,
        #     'codelist_ref': codelist_ref
        # })

        return return_data

    def get_dataset_overview_url(self, dataset_id):
        # http: // open.statswales.gov.wales / en - gb / discover / datasetdimensionitems?$filter = Dataset % 20
        # eq % 20 % 27
        # wimd0020 % 27 % 20 and % 20
        # DimensionName_ENG % 20
        # ne % 20 % 27
        # Area % 27

        data_url = self.datasetdimensionitems_url
        # FIXME the lower() is hacky, get the proper format from somewhere
        data_url += self.filter_prepend.format(
            self.get_filter_string(
                [
                    ('Dataset', StatsWalesOData().equals_conditional, str(dataset_id).lower()),
                    ('DimensionName_ENG', StatsWalesOData().not_equals_conditional, 'Area')
                ]
            )
        )

        return data_url



def do_test():
    swod = StatsWalesOData()

    keyword_results = swod.keyword_search('deprivation+health', {'Geography', ''})
    print(keyword_results)
    print (len(keyword_results))

    # area_code = 'W01001434'
    dataset_id = list(keyword_results)[0]['PartitionKey']
    print(dataset_id)
    dataset_id = 'wimd0020'

    data_types = swod.get_metadata_for_dataset('wimd0020')

    codelist = [{u'variable': u'AllAges', u'option': u'Age Group'},
     {u'variable': u'INCO', u'option': u'Indicator'},
     {u'variable': u'2015', u'option': u'Year'}]

    filter_options = []
    for code in codelist:
        print 'code', code
        option = str(code['option']).replace(' ', '') + '_Code'
        variable = code['variable']
        filter_options.append([option, swod.equals_conditional, variable])
    print 'filter_options', filter_options

    all_data_list = swod.get_data(
        dataset_id,
        [
            # 'Area_Code': area_code,
            ('Year_Code', StatsWalesOData().equals_conditional, 2014),
            ('AgeGroup_Code', StatsWalesOData().equals_conditional, 'AllAges')
        ]
    )

    all_data_dict = swod.odata_to_dict(all_data_list)

    print(len(all_data_dict))

if __name__ == '__main__':
    do_test()