# from cStringIO import StringIO
import os
import pprint
import urllib3.contrib.pyopenssl
from dataportal3.utils.spatial_search.spatial_search import geometry_columns
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

        try:
            # Do keyword search
            r = requests.get(
                'http://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json?search=*{0}*'.format(search_term),
                timeout=10)
            print r.url
            j = json.loads(r.text)
            datasets = []

            if j['structure']['keyfamilies'] is None:
                return datasets
            s = j['structure']['keyfamilies']['keyfamily']
            for f in s:

                text1 = ''
                text2 = ''
                link = ''

                for anno1 in f['annotations']['annotation']:
                    if anno1['annotationtitle'] == 'MetadataText0':
                        text1 = anno1['annotationtext']

                    if anno1['annotationtitle'] == 'MetadataText1':
                        text2 = anno1['annotationtext']

                k = {
                    'id': f['id'],
                    'name': f['name']['value'],
                    'source': 'Nomis',
                    'text1': text1,
                    'text2': text2,
                    'link': link
                }
                datasets.append(k)
                # print pprint.pformat(k)
            # print json.dumps(s, indent=4)
            return datasets, r
        except Exception as e:
            raise e

    def get_codelist_for_concept(self, concept_id, codelist_ref):
        item_url = 'https://www.nomisweb.co.uk/api/v01/codelist/{0}.def.sdmx.json'.format(concept_id)

        r6 = requests.get(item_url)
        print r6.url
        j6 = json.loads(r6.text)

        s2 = j6['structure']['codelists']['codelist'][0]['code']
        measures = []
        for f2 in s2:
            if 'All categories' not in f2['description']['value']:
                k2 = {
                    'id': f2['value'],
                    'name': f2['description']['value']
                }
                measures.append(k2)
                # print pprint.pformat(k2)

        measures_def = {
            'name': j6['structure']['codelists']['codelist'][0]['name']['value'],
            'concept': codelist_ref,
            'measures': measures
        }

        # print pprint.pformat(measures_def)
        return measures_def

    def get_dataset_overview(self, dataset_id):

        # item_url = 'https://www.nomisweb.co.uk/api/v01/dataset/{0}.overview.json'.format(dataset_id)
        # r6 = requests.get(item_url)
        # print r6.url
        # j6 = json.loads(r6.text)
        # print 'items', json.dumps(j6, indent=4)

        # print '\n\n\n'

        item_url = 'https://www.nomisweb.co.uk/api/v01/dataset/{0}/def.sdmx.json'.format(dataset_id)
        r6 = requests.get(item_url)
        print r6.url
        j6 = json.loads(r6.text)
        # print 'items', json.dumps(j6, indent=4)

        return_data = {
            'concepts': [],
            'codelists': {},
            'name': j6['structure']['keyfamilies']['keyfamily'][0]['name']['value'],
        }

        concepts = j6['structure']['keyfamilies']['keyfamily'][0]['components']['dimension']
        for concept in concepts:
            codelist = concept['codelist']
            codelist_ref = concept['conceptref']

            return_data['concepts'].append({
                'codelist': codelist,
                'codelist_ref': codelist_ref
            })

            if "GEOGRAPHY" not in codelist:
                try:
                    codelist_data = self.get_codelist_for_concept(codelist, codelist_ref)
                    return_data['codelists'][codelist_ref] = codelist_data
                except:
                    print '*** FAIL', codelist

        return return_data

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
            k4['geogcode'] = f4['annotations']['annotation'][2]['annotationtext']
            regions.append(k4)
            print pprint.pformat(k4)
        return regions

    def get_dataset_url(self, dataset_id, region_id, measure, codelist=None, limit=10, offset=0):
        # Get data for variable for dataset in region with offsets
        limit = str(limit)
        offset = str(offset)

        dataset_url = 'https://www.nomisweb.co.uk/api/v01/dataset/{0}.data.json?' \
                      'geography={1}&&uid={4}'
        # &&RecordLimit={2}&&RecordOffset={3}
        dataset_url = dataset_url.format(dataset_id, region_id, limit, offset, settings.nomis_uid)

        codelist_filename = ''
        if codelist:
            # print type(codelist), codelist

            measures_found = False
            for code in codelist:
                if code['option'] == 'MEASURES':
                    measures_found = True

            # print type(codelist), codelist
            if not measures_found:
                codelist.append({
                    'option': 'MEASURES',
                    'variable': '20100'
                })
            for code in codelist:
                if 'option' in code and 'variable' in code:
                    dataset_url += '&&' + str(code['option']) + '=' + str(code['variable'])
                    codelist_filename += str(code['option']) + '=' + str(code['variable']) + '_'

                    # TODO, remove refs to measure not from codelist
                    if code['option'] == 'MEASURES':
                        measure = int(code['variable'])
        else:
            dataset_url += '&&CELL=6'

        return dataset_url, codelist_filename

    def get_data(self, dataset_id, region_id, measure, codelist=None, limit=10, offset=0, search_uuid=None):
        dataset_url, codelist_filename = self.get_dataset_url(dataset_id, region_id, measure, codelist, limit, offset)

        nomis_raw_filename = os.path.join(
            settings.TMP_DIR,
            'nomis_raw_{0}_{1}_{2}.json'.format(
            dataset_id, region_id, codelist_filename)
        )

        # if file exists, load that, otherwise pull from nomis

        if not os.path.isfile(nomis_raw_filename):

            r5 = requests.get(dataset_url, stream=False)
            print r5.url, r5.status_code

            with open(nomis_raw_filename, 'wb') as raw_nomis:
                # f32.write(r5.text)
                for chunk in r5.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        raw_nomis.write(chunk)
                        raw_nomis.flush()

        with open(nomis_raw_filename, 'r') as f:
            j5 = json.load(f)

        # j5 = json.load(nomis_raw_filename)
        s5 = j5['obs']
        data_points = {}

        for code in codelist:
            if code['option'] == 'MEASURES':
                measure = code['variable']

        for f5 in s5:
            # TODO is this == check needed?
            if int(f5['measures']['value']) == int(measure):
                k5 = {
                    'value': f5['obs_value']['value'],
                    'name': f5['obs_value']['description'],
                    'geography': f5['geography']['description'],
                    'geography_code': f5['geography']['geogcode'],
                    'geography_id': f5['geography']['value'],
                    'data_status': f5['obs_status']['value'],
                    'string_data': [
                        {
                            'title': 'Dataset',
                            'value': f5['dataset']['description'],
                        },
                        {
                            'title': 'Licence',
                            'value': f5['obs_conf']['description'],
                        },
                        {
                            'title': 'Description',
                            'value': f5['obs_value']['description']
                        },
                        {
                            'title': 'Data link',
                            'value': j5['header']['uri']
                        }
                    ]

                }
                if search_uuid:
                    k5['search_uuid'] = search_uuid

                # Store by name - possibly open to errors
                try:
                    data_points.get(
                        str(f5['geography']['description']).replace(' ', '')
                    ).append(k5)
                except:
                    data_points[
                        str(f5['geography']['description']).replace(' ', '')
                    ] = [k5]

                # Store by W0..... number, should be more stable
                try:
                    data_points.get(
                        str(f5['geography']['geogcode'])
                    ).append(k5)
                except:
                    data_points[
                        str(f5['geography']['geogcode'])
                    ] = [k5]

                    # print pprint.pformat(k5)
        print 'values len', len(data_points)
        return data_points

    # Returns a dict of format:
    # {(u'geography', u'NAME'): 40, (u'geography', u'ALTNAME'): 10, (u'geography_code', u'CODE'): 44}
    # the key is a set of 2 strings (or unicode) which is:
    # ( remote_data_key , topojson_region_key )

    def match_region_ids(self, remote_data, topojson_region_data):
        # print 'first_remote_data_region_ids', first_remote_data_region_ids

        matches = {}
        loops = 0

        # print 'remote_data', type(remote_data)
        print 'length', len(remote_data)

        for geom_data in remote_data.keys()[:100]:
            loops += 1

            for c in remote_data[geom_data][0]:
                # print 'geom_data', type(remote_data[geom_data][0]), len(remote_data[geom_data][0])

                loops += 1
                for a in topojson_region_data:
                    loops += 1
                    for b in a['properties']:
                        loops += 1
                        # print c, remote_data[geom_data][0][c], b, a['properties'][b]
                        if remote_data[geom_data][0][c] == a['properties'][b]:
                            # print 'found', c, 'matches', b

                            if (c, b) in matches:
                                matches[(c, b)] += 1
                            else:
                                matches[(c, b)] = 1
        print 'matches', matches
        print 'loops', loops
        return matches

    def update_topojson(self, topojson_file, remote_data, measure_is_percentage=False):

        remote_areas = remote_data.keys()
        # print 'remote_areas', remote_areas

        found = 0
        not_found = 0

        with open(topojson_file, 'r') as fd:
            whole_topojson = json.loads(fd.read())
            recent_layer_name = ''

            topojson_region_data = whole_topojson['objects'].itervalues().next()['geometries']
            matching_data_ids = self.match_region_ids(remote_data, topojson_region_data)
            best_key_match = max(matching_data_ids, key=matching_data_ids.get)
            (remote_data_key, topojson_region_key) = best_key_match
            # print remote_data_key, topojson_region_key

            total_number_regions = 0
            for layer_name in whole_topojson['objects']:
                recent_layer_name = layer_name

                total_number_regions += len(whole_topojson['objects'][layer_name]['geometries'])
                for geom in whole_topojson['objects'][layer_name]['geometries']:

                    try:
                        topojson_match_value = geom['properties'][topojson_region_key]
                        discovered = False

                        for remote_data_item_key in remote_data:
                            remote_data_object = remote_data[remote_data_item_key][0]
                            if remote_data_object[remote_data_key] == topojson_match_value:
                                discovered = True
                                geom['properties']['REMOTE_VALUE'] = remote_data_object['value']
                                geom['properties']['AREA_NAME'] = remote_data_item_key
                                geom['properties']['PERCENTAGE'] = measure_is_percentage
                                geom['properties']['DATA_STATUS'] = remote_data_object['data_status']

                                if 'string_data' in remote_data_object:
                                    # print "remote_data_object['string_data']", remote_data_object['string_data']

                                    geom['properties']['STRING_DATA'] = remote_data_object['string_data']
                                if 'data_title' in remote_data_object:
                                    geom['properties']['DATA_TITLE'] = remote_data_object['data_title']

                                if 'data_title_alt1' in remote_data_object:
                                    geom['properties']['DATA_TITLE_ALT1'] = remote_data_object['data_title_alt1']

                                if 'search_uuid' in remote_data_object:
                                    geom['properties']['SEARCH_UUID'] = remote_data_object['search_uuid']

                                if 'data_prefix' in remote_data_object:
                                    geom['properties']['DATA_PREFIX'] = remote_data_object['data_prefix']

                                if 'data_global_average' in remote_data_object:
                                    geom['properties']['DATA_GLOBAL_AVERAGE'] = remote_data_object['data_global_average']
                                if 'data_suffix' in remote_data_object:
                                    geom['properties']['DATA_SUFFIX'] = remote_data_object['data_suffix']

                                found += 1

                        # Separate, because this needs tidying in future
                        # TODO check how smart this is
                        if not discovered:
                            print 'not found, yet', topojson_match_value
                            topojson_match_value = topojson_match_value.replace(' ', '')

                            for remote_data_item_key in remote_data:
                                remote_data_object = remote_data[remote_data_item_key][0]
                                if remote_data_object[remote_data_key].replace(' ', '') == topojson_match_value:
                                    discovered = True
                                    geom['properties']['REMOTE_VALUE'] = remote_data_object['value']
                                    geom['properties']['AREA_NAME'] = remote_data_item_key
                                    geom['properties']['PERCENTAGE'] = measure_is_percentage
                                    geom['properties']['DATA_STATUS'] = remote_data_object['data_status']
                                    if 'string_data' in remote_data_object:
                                        geom['properties']['STRING_DATA'] = remote_data_object['string_data']
                                    if 'data_title' in remote_data_object:
                                        geom['properties']['DATA_TITLE'] = remote_data_object['data_title']

                                    found += 1

                            if not discovered:
                                print '*********', 'not found, error', topojson_match_value

                    except:
                        area_name = ''
                        try:
                            # Try by geocode
                            topojon_area_name = str(geom['properties']['CODE'])
                            area_name = str(geom['properties']['CODE'])
                            # print 'topjson has CODE', topojon_area_name
                        except:
                            try:
                            # try by name
                                topojon_area_name = str(geom['properties']['AREA_NAME']).replace(' ', '')
                                area_name = str(geom['properties']['AREA_NAME'])
                                # print 'using name'
                            except:
                            # try by label?
                                topojon_area_name = str(geom['properties']['LABEL']).replace(' ', '')
                                area_name = str(geom['properties']['LABEL'])
                                # print 'using label'
                        try:
                            # print topojon_area_name in remote_data
                            try:
                                first_remote_data = remote_data[topojon_area_name][0]
                                found += 1
                                remote_areas.remove(topojon_area_name)
                                # print ''
                            except Exception as e789243:
                                print 'topojson name/code error', e789243, type(e789243), \
                                    geom['properties'], \
                                    remote_data[topojon_area_name][0]

                                try:
                                    first_remote_data = remote_data[
                                        str(geom['properties']['NAME'])
                                    ][0]
                                    found += 1
                                    remote_areas.remove(str(geom['properties']['NAME']))
                                except:
                                    # TODO I am so very sorry, future programmer
                                    # At least exception handling in Python is "cheap"
                                    pass

                            # print first_remote_data

                            # print geom['properties']['AREA_NAME'], remote_entry['geography']
                            # if remote_entry['geography'] == geom['properties']['AREA_NAME']:

                            geom['properties']['REMOTE_VALUE'] = first_remote_data['value']
                            # geom['properties']['AREA_NAME'] = geom['properties']['NAME']
                            geom['properties']['AREA_NAME'] = area_name
                            geom['properties']['PERCENTAGE'] = measure_is_percentage
                            geom['properties']['DATA_STATUS'] = first_remote_data['data_status']
                            if 'string_data' in first_remote_data:
                                geom['properties']['STRING_DATA'] = first_remote_data['string_data']
                            if 'data_title' in first_remote_data:
                                geom['properties']['DATA_TITLE'] = first_remote_data['data_title']

                        except Exception as e:
                            print '\n\ntopojson update error', e, type(e), geom['properties']
                            not_found += 1

            # print 'remote data keys not used', len(remote_data.keys()), remote_data.keys()
            print 'success y/n', found, (total_number_regions - found)

            # print whole_json['objects'][recent_layer_name]['geometries']
            return whole_topojson

    def get_dataset_geodata(self, geog_short_code, high=False):

        region_id = ''
        topojson_file = ''
        print 'geog_short_code', geog_short_code

        for topojson_entry in geometry_columns:  # settings.TOPOJSON_OPTIONS:
            if 'geog_short_code' in topojson_entry:
                if topojson_entry['geog_short_code'] == geog_short_code:
                    region_id = topojson_entry['region_id']
                    if high:
                        # high detail topojson file
                        topojson_file = topojson_entry['topojson_file_high']
                    else:
                        topojson_file = topojson_entry['topojson_file']

        # print region_id, topojson_file

        # if geog_short_code == 'pcode':
        #     region_id = '2092957700TYPE276'
        #     topojson_file = '/home/ubuntu/shp/x_sid_liw2007_pcode_/output-fixed-1.json'
        #
        # if geog_short_code == 'lsoa':
        #     region_id = '2092957700TYPE298'
        #     # topojson_file = '/home/ubuntu/shp/x_sid_liw2007_lsoa_/output-fixed-1.json'
        #     topojson_file = settings.TOPOJSON_FILE_LSOA
        #
        # if geog_short_code == 'ua':
        #     region_id = '2092957700TYPE464'
        #     # topojson_file = '/home/ubuntu/shp/x_sid_liw2007_ua_/output-fixed-1.json'
        #     topojson_file = settings.TOPOJSON_FILE_UA
        #
        # if geog_short_code == 'parl':
        #     # boundaries prior to 2010
        #     region_id = '2092957700TYPE460'
        #     topojson_file = '/home/ubuntu/shp/x_sid_liw2007_parl_/output-fixed-1.json'
        #
        # if geog_short_code == 'parl2011':
        #     region_id = '2092957700TYPE460'
        #     topojson_file = settings.TOPOJSON_FILE_PARL_2011

        if region_id == '' or topojson_file == '':
            print 'error figuring out geog'
            raise Exception
        else:
            return region_id, topojson_file

    def get_topojson_with_data(self, dataset_id, geog, nomis_variable, codelist=None, high=False, search_uuid=None):
        region_id, topojson_file = self.get_dataset_geodata(geog, high)
        all_data = self.get_data(dataset_id, region_id, nomis_variable, codelist=codelist, limit=100, offset=0, search_uuid=search_uuid)

        measure_is_percentage = False
        if codelist:
            for code in codelist:
                if code['option'] == 'MEASURES':
                    if code['variable'] == '20301':
                        measure_is_percentage = True

        nomis_cache_file = os.path.join(
            settings.TMP_DIR,
            'nomis_{0}_{1}_{2}.json'.format(
                dataset_id, geog, nomis_variable
            )
        )

        # if codelist:
        #     print type(codelist), codelist
        #     for code in codelist:
        #         if 'option' in code and 'variable' in code:
        #             dataset_url += '&&' + code['option'] + '=' + code['variable']

        print nomis_cache_file
        with open(nomis_cache_file, 'w') as nomis_file:
            nomis_file.write(json.dumps(all_data, indent=4))
        with open(nomis_cache_file, 'r') as nomis_file:
            all_data = json.load(nomis_file)

        return self.update_topojson(topojson_file, all_data, measure_is_percentage)

    def get_test_data(self, search_term, geog='pcode'):
        # region_id, topojson_file = self.get_dataset_geodata(geog)

        search_results = self.search_datasets(search_term)
        dataset_id = search_results[0]['id']

        nomis_variables = self.get_dataset_variables(dataset_id)
        nomis_variable = nomis_variables[0]['id']

        geogs = self.get_geography(dataset_id)
        print search_results[0]

        # regions = self.get_sub_regions(dataset_id, '2092957700TYPE274')

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

        print dataset_id, geog, nomis_variable
        return self.get_topojson_with_data(dataset_id, geog, nomis_variable)

    def get_stored_data(self):
        all_data = {}
        with open('/home/ubuntu/nomis_data_pc4.json', 'r') as nomis_file:
            all_data = json.load(nomis_file)

        topojson_file = '/home/ubuntu/shp/x_sid_liw2007_pcode_/output-fixed-1.json'
        return self.update_topojson(topojson_file, all_data)

    def inspect_topojson(self, topojson_file):
        with open(topojson_file, 'r') as nomis_file:
            all_data = json.load(nomis_file)
            # print all_data.keys()

            for geo_name in all_data['objects'].itervalues().next()['geometries']:
                print geo_name['properties']
                # print geo_name['properties']['AREA_NAME']


# 2092957700TYPE276 post code sector
# 2092957700TYPE298 lsoa
# 2092957700TYPE464 ua ????

# rd = RemoteData()
# topojson_file = '/home/ubuntu/DataPortalGeographies/11Wales_lsoa_2011/output-fixed-1-k.json'
# topojson_file = '/home/ubuntu/DataPortalGeographies/05Wales_pcd_2012/output-fixed-1.json'

# rd.inspect_topojson(topojson_file)
# rd.get_sub_regions('NM_548_1', '2092957700TYPE460')
# geogs = rd.get_geography('NM_144_1')
# rd.get_sub_regions('NM_144_1', '2092957700')

#
# rd.get_dataset_overview('NM_548_1')
# items = rd.get_dataset_items('NM_548_1', '2092957700TYPE460')
# rd.get_sub_regions('NM_548_1', '2092957700')
# rd.get_sub_regions('NM_548_1', '2092957700TYPE275')
# rd.get_sub_regions('NM_548_1', '2092957700TYPE276')
# rd.get_sub_regions('NM_548_1', '2092957700TYPE464')

# rd.get_test_data('van', 'parl2011')

# a = rd.get_topojson_with_data('NM_548_1', 'parl2011', '20100')

# rd.update_topojson('/home/ubuntu/shp/x_sid_liw2007_lsoa_/output-fixed-0.1.json', '')


# def get_remote_data_sdmx(self, survey_id):
#     ecb = Request().get(url='https://www.neighbourhood.statistics.gov.uk/NDE2/Deli')
#     cat_resp = ecb.get(resource_type = 'categoryscheme')
#     print cat_resp.msg.__dict__
