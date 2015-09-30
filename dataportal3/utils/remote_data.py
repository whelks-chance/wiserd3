# from cStringIO import StringIO
import pprint
import urllib3.contrib.pyopenssl
from wiserd3 import settings

urllib3.contrib.pyopenssl.inject_into_urllib3()
# import ijson.backends.yajl2 as ijson

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
            # print pprint.pformat(k)
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
        # r3_1 = requests.get(
        #     'https://www.nomisweb.co.uk/api/v01/dataset/{0}/geography.def.sdmx.json'.format(dataset_id)
        # )
        # print r3_1.url, r3_1.text
        # j3_1 = json.loads(r3_1.text)
        # print json.dumps(j3_1, indent=4)

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
        print r4.url
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

    def get_data(self, dataset_id, region_id, measure, limit=10, offset=0):
        # Get data for variable for dataset in region with offsets
        limit = str(limit)
        offset = str(offset)

        if True:
            r5 = requests.get(
                'https://www.nomisweb.co.uk/api/v01/dataset/{0}.data.json?'
                'geography={1}&&measures={2}&&RecordLimit={3}&&RecordOffset={4}&&uid={5}'.format(
                    dataset_id, region_id, measure, limit, offset, settings.nomis_uid
                ), stream=True
            )
            print r5.url

            with open('/home/ubuntu/nomis_raw.json', 'wb') as f:
                for chunk in r5.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()

        with open('/home/ubuntu/nomis_raw.json', 'r') as f:
            j5 = json.load(f)

        s5 = j5['obs']
        data_points = {}

        # print s5[0]

        for f5 in s5:
            if f5['measures']['value'] == measure:
                k5 = {
                    'value': f5['obs_value']['value'],
                    'name': f5['obs_value']['description'],
                    'geography': f5['geography']['description'],
                    'geography_code': f5['geography']['geogcode'],
                    'geography_id': f5['geography']['value']
                }
                try:
                    data_points.get(
                        str(f5['geography']['description']).replace(' ', '')
                    ).append(k5)
                except:
                    data_points[
                        str(f5['geography']['description']).replace(' ', '')
                    ] = [k5]

                    # print pprint.pformat(k5)
        print 'values len', len(data_points)
        return data_points

    def update_topojson(self, topojson_file, remote_data):

        found = 0
        not_found = 0

        with open(topojson_file, 'r') as fd:
            whole_topojson = json.loads(fd.read())
            recent_layer_name = ''

            for layer_name in whole_topojson['objects']:
                recent_layer_name = layer_name

                # print 'remote data keys', len(remote_data.keys()), remote_data.keys()

                for geom in whole_topojson['objects'][layer_name]['geometries']:
                    topojon_area_name = str(geom['properties']['AREA_NAME']).replace(' ', '')
                    # print '***' + topojon_area_name + '***'

                    try:
                        # print topojon_area_name in remote_data
                        first_remote_data = remote_data[topojon_area_name][0]
                        # print first_remote_data

                        # print geom['properties']['AREA_NAME'], remote_entry['geography']
                        # if remote_entry['geography'] == geom['properties']['AREA_NAME']:

                        found += 1
                        geom['properties']['REMOTE_VALUE'] = first_remote_data['value']
                    except Exception as e:
                        print 'error', e
                        not_found += 1
                    # print '\n'

            print 'success y/n', found, not_found
            print 'remote data keys', len(remote_data.keys()), remote_data.keys()

            # print '\n***\n'
            # print whole_json['objects'][recent_layer_name]['geometries']
            return whole_topojson

    def get_test_data(self, search_term):
        search_results = self.search_datasets(search_term)
        dataset_id = search_results[0]['id']
        print search_results[0]

        geogs = self.get_geography(dataset_id)
        # regions = self.get_sub_regions(dataset_id, '2092957700TYPE274')
        vars = self.get_dataset_variables(dataset_id)

        # all_data = {}
        # for d in [0, 5, 10]:
        all_data = self.get_data(dataset_id, '2092957700TYPE276', vars[0]['id'], limit=100, offset=0)
        # all_data.update(data)
        # print len(all_data.keys())

        # regions = [
        #     {'id': 1149239309, 'name': u'CF - Cardiff'},
        #     {'id': 1149239343, 'name': u'LD - Llandrindod Wells'},
        #     {'id': 1149239345, 'name': u'LL - Llandudno'},
        #     {'id': 1149239356, 'name': u'NP - Newport'},
        #     {'id': 1149239369, 'name': u'SA - Swansea'}
        # ]
        #
        # all_data = {}
        # for region in regions:
        #     region_id = str(region['id'])
        #     data = self.get_data(dataset_id, region_id, vars[0]['id'])
        #     all_data.update(data)

        with open('/home/ubuntu/nomis_data_pc4.json', 'w') as nomis_file:
            nomis_file.write(json.dumps(all_data, indent=4))

        with open('/home/ubuntu/nomis_data_pc4.json', 'r') as nomis_file:
            all_data = json.load(nomis_file)

        topojson_file = '/home/ubuntu/shp/x_sid_liw2007_pcode_/output-fixed-1.json'
        return self.update_topojson(topojson_file, all_data)

    def get_stored_data(self):
        all_data = {}
        with open('/home/ubuntu/nomis_data_pc4.json', 'r') as nomis_file:
            all_data = json.load(nomis_file)

        topojson_file = '/home/ubuntu/shp/x_sid_liw2007_pcode_/output-fixed-1.json'
        return self.update_topojson(topojson_file, all_data)


# 2092957700TYPE276 post code sector
# 2092957700TYPE298 lsoa

# rd = RemoteData()
# geogs = rd.get_geography('NM_548_1')
# rd.get_sub_regions('NM_548_1', '2092957700')
# rd.get_sub_regions('NM_548_1', '2092957700TYPE274')
# rd.get_sub_regions('NM_548_1', '2092957700TYPE275')
# rd.get_sub_regions('NM_548_1', '2092957700TYPE276')

# rd.get_test_data('van')

# rd.update_topojson('/home/ubuntu/shp/x_sid_liw2007_lsoa_/output-fixed-0.1.json', '')


# def get_remote_data_sdmx(self, survey_id):
#     ecb = Request().get(url='https://www.neighbourhood.statistics.gov.uk/NDE2/Deli')
#     cat_resp = ecb.get(resource_type = 'categoryscheme')
#     print cat_resp.msg.__dict__
