import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd3.settings")
import django
django.setup()

import pprint
from dataportal3.utils.spatial_search.spatial_search import find_intersects, get_data_for_regions

wkt_region = '''[u&#39;POLYGON ((298297.78502920375 181841.18597899398,298678.28101712064 200807.17836275577,317658.0002661088 200461.67790279497,317348.79709203186 181495.20467829853,298297.78502920375 181841.18597899398))&#39;]'''

b = find_intersects(wkt_region)

print pprint.pformat(b)

for boundary_type in b['boundary_surveys'].keys():

    print 'boundary type', boundary_type
    for survey in b['boundary_surveys'][boundary_type]['table_options'].keys():
        print 'survey', survey
        data_name = b['boundary_surveys'][boundary_type]['table_options'][survey][0]
        regions = b['boundary_surveys'][boundary_type]['intersects']

        data = get_data_for_regions(survey, data_name, regions)

        # print pprint.pformat(data, indent=4)
        print data