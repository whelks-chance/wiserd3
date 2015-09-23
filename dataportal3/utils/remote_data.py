import pprint
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import json
# from pandasdmx import Request
import requests

__author__ = 'ubuntu'


class RemoteData():
    def __init__(self):
        pass

    def search_datasets(self, search_term):
        # Do keyword search
        r = requests.get('http://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json?search=*{0}*'.format(search_term))
        print r.url
        j = json.loads(r.text)
        s = j['structure']['keyfamilies']['keyfamily']
        datasets = []
        for f in s:
            k = {}
            k['id'] = f['id']
            k['name'] = f['name']['value']
            datasets.append(k)
            print pprint.pformat(k)
        # print json.dumps(s, indent=4)
        return datasets

    def get_dataset_variables(self, dataset_id):
        # Get available variables for dataset
        # id = datasets[0]['id']
        # id = 'NM_621_1'
        r2 = requests.get(
            'https://www.nomisweb.co.uk/api/v01/dataset/{0}/measures.def.sdmx.json'.format(dataset_id)
        )
        # print r2.url, r2.text
        j2 = json.loads(r2.text)
        # print 'measures', json.dumps(j2, indent=4)

        s2 = j2['structure']['codelists']['codelist'][0]['code']
        measures = []
        for f2 in s2:
            k2 = {}
            k2['id'] = f2['value']
            k2['name'] = f2['description']['value']
            measures.append(k2)
            print pprint.pformat(k2)
        return measures

    def get_geography(self, dataset_id):
        # Get available top level geographies for dataset
        r3 = requests.get(
            'https://www.nomisweb.co.uk/api/v01/dataset/{0}/geography.def.sdmx.json'.format(dataset_id)
        )
        # print r3.url, r3.text
        j3 = json.loads(r3.text)
        # print json.dumps(j3, indent=4)

        s3 = j3['structure']['codelists']['codelist'][0]['code']
        regions = []
        for f3 in s3:
            k3 = {}
            k3['id'] = f3['value']
            k3['name'] = f3['description']['value']
            regions.append(k3)
            print pprint.pformat(k3)
        # region = regions[0]['id']
        return regions

    def get_sub_regions(self, dataset_id, region):
        # Get sub regions for parent region, for dataset
        r4 = requests.get(
            'https://www.nomisweb.co.uk/api/v01/dataset/{0}/geography/{1}.def.sdmx.json'.format(dataset_id, region)
        )
        # print r4.url, r4.text
        j4 = json.loads(r4.text)
        # print json.dumps(j4, indent=4)
        s4 = j4['structure']['codelists']['codelist'][0]['code']
        regions = []
        for f4 in s4:
            k4 = {}
            k4['id'] = f4['value']
            k4['name'] = f4['description']['value']
            regions.append(k4)
            print pprint.pformat(k4)
        return regions

    def get_data(self, dataset_id, region_id, measure, limit='10', offset=0):
        # Get data for variable for dataset in region with offsets
        r5 = requests.get(
            'https://www.nomisweb.co.uk/api/v01/dataset/{0}.data.json?'
            'geography={1}&&measures={2}&&RecordLimit={3}&&RecordOffset={4}'.format(dataset_id, region_id, measure, limit, offset)
        )
        print r5.url
        j5 = json.loads(r5.text)
        # print json.dumps(j5, indent=4)
        s5 = j5['obs']
        data_points = []
        for f5 in s5:
            if f5['measures']['value'] == measure:
                k5 = {
                    'value': f5['obs_value']['value'],
                    'name': f5['obs_value']['description'],
                    'geography': f5['geography']['description'],
                    'geography_code': f5['geography']['geogcode'],
                    'geography_id': f5['geography']['value']
                }
                data_points.append(k5)
                print pprint.pformat(k5)
        return data_points

    def get_test_data(self, search_term):
        search_results = self.search_datasets(search_term)
        dataset_id = search_results[0]['id']
        geogs = self.get_geography(dataset_id)
        regions = self.get_sub_regions(dataset_id, '2092957700')
        vars = self.get_dataset_variables(dataset_id)
        data = self.get_data(dataset_id, 'W06000022', vars[0]['id'])


rd = RemoteData()
rd.get_test_data('van')


# def get_remote_data_sdmx(self, survey_id):
#     ecb = Request().get(url='https://www.neighbourhood.statistics.gov.uk/NDE2/Deli')
#     cat_resp = ecb.get(resource_type = 'categoryscheme')
#     print cat_resp.msg.__dict__
