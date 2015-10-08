# import os
# from django.core.serializers import serialize
# from django.http import HttpResponse

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
# import django
# django.setup()

# from django.contrib.gis.geos import GEOSGeometry
# from dataportal3 import models
# import ijson
import pprint
import ijson.backends.yajl2 as ijson
# import ijson
import time

import json
import requests

__author__ = 'ubuntu'


def stream_ijson(big_file):
    start = time.time()


    # with open(big_file) as f1:
    #     thingy = json.load(f1)
    #     print thingy.keys()

    a_url = 'https://www.nomisweb.co.uk/api/v01/dataset/NM_548_1.data.json?geography=2092957700TYPE298&&measures=20100&&RecordLimit=100&&RecordOffset=0&&uid=0x7065df0e03b2e953ecf3027601a11084f1e87469'
    filename_to_save = '/home/ubuntu/to_save.json'

    # with open(filename_to_save, 'w') as file_to_save:
    #     req = requests.get(a_url, stream=True)
    #     for chunk in req.iter_content(chunk_size=1024):
    #         if chunk: # filter out keep-alive new chunks
    #             file_to_save.write(chunk)
    #             file_to_save.flush()

    complete = {}
    current_object = None

    with open(filename_to_save) as f3:
        t2 = time.time()
        print t2 - start
        skip = False
        for prefix, event, value in ijson.parse(f3):

            # print prefix, event, value

            if prefix == 'obs.item' and event == 'end_map':
                # Tidy away old object
                if current_object is not None:
                    if not skip:
                        if current_object['geography_code'] in complete:
                            print ',',
                            # print 'replacing', current_object['geography_code']
                        else:
                            print len(complete.keys())
                            # print 'creating', current_object['geography_code']

                        complete[current_object['geography_code']] = current_object

                    skip = False


            if not skip:
                if prefix == 'obs.item' and event == 'start_map':
                    # Create a new object to populate
                    current_object = {}

                # Populate object
                if prefix == 'obs.item.geography.description':
                    current_object['geography'] = value

                elif prefix == 'obs.item.geography.geogcode':
                    if value in complete:
                        skip = True

                    current_object['geography_code'] = value

                elif prefix == 'obs.item.geography.value':
                    current_object['geography_id'] = value

                elif prefix == 'obs.item.obs_value.description':
                    current_object['name'] = value

                elif prefix == 'obs.item.obs_value.value':
                    current_object['value'] = value

    t3 = time.time()
    print t3 - t2
    print pprint.pformat(complete)

    t4 = time.time()
    print t4 - t3
    # with open(filename_to_save) as f2:
    #     for item2 in ijson.items(f2, "obs"):
    #         for item in item2:
    #             print type(item)
    #             print len(item)
    #             print item['measures']['value']

                # k5 = {
                #     'value': f5['obs_value']['value'],
                #     'name': f5['obs_value']['description'],
                #     'geography': f5['geography']['description'],
                #     'geography_code': f5['geography']['geogcode'],
                #     'geography_id': f5['geography']['value']
                # }


filename = '/home/ubuntu/nomis_raw.json'

stream_ijson(filename)